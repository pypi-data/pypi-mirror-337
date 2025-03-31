# -*- coding: utf-8 -*-
#
#    BitcoinLib - Python Cryptocurrency Library
#    Update database
#    © 2025 Gordon Lawson <gordonlawson@gmail.com

import os
import sys
import argparse
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from shutil import move
from bitcoinlib.main import DEFAULT_DATABASE, BCL_DATABASE_DIR, BITCOINLIB_VERSION
from bitcoinlib.db import Base, DbWallet, DbKey, DbKeyMultisigChildren, DbConfig
from bitcoinlib.db import Base, DbConfig, DbWallet, DbKey, DbKeyMultisigChildren
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

class DatabaseVersionChecker:
    def __init__(self, database=None):
        self.database_file = database if database else 'sqlite:///' + DEFAULT_DATABASE
        self._normalize_database_path()
        self.engine = create_engine(self.database_file)
        self.session = sessionmaker(bind=self.engine)()

    def _normalize_database_path(self):
        """Ensure database path is properly formatted"""
        if not self.database_file.startswith('sqlite:///'):
            if not os.path.isfile(self.database_file):
                self.database_file = os.path.join(BCL_DATABASE_DIR, self.database_file)
            self.database_file = 'sqlite:///' + self.database_file

    def check_database_version(self):
        """Check if database needs migration before proceeding"""
        # Create tables if they don't exist
        Base.metadata.create_all(self.engine)

        version_db = self.session.query(DbConfig.value).filter_by(variable='version').scalar()

        if not version_db:
            # New database, set current version
            self.session.add(DbConfig(variable='version', value=BITCOINLIB_VERSION))
            self.session.commit()
            return True

        if version_db[:3] == '0.4' and BITCOINLIB_VERSION[:3] >= '0.5':
            raise ValueError(
                "Old database version found (<0.4.19). Cannot convert to >0.5 version database automatically.\n"
                "Please run 'clw update' command first to migrate your database."
            )

        return True

    def close(self):
        """Clean up database connections"""
        self.session.close()
        self.engine.dispose()

def check_database_version_before_command(database_path=None):
    """Decorator to check database version before executing any command"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            checker = DatabaseVersionChecker(database_path)
            try:
                checker.check_database_version()
                return func(*args, **kwargs)
            finally:
                checker.close()
        return wrapper
    return decorator

class DatabaseUpdater:
    def __init__(self, database=None):
        self.database_file = database if database else 'sqlite:///' + DEFAULT_DATABASE
        if not self.database_file.startswith('sqlite:///'):
            if not os.path.isfile(self.database_file):
                self.database_file = os.path.join(BCL_DATABASE_DIR, self.database_file)
            self.database_file = 'sqlite:///' + self.database_file
        self.original_db_path = self.database_file.replace('sqlite:///', '')
        self.database_backup_file = self.original_db_path + '.backup-' + datetime.now().strftime("%Y%m%d-%H%M")

    @staticmethod
    def convert_value(value, field_name=None):
        """Convert values to proper types for SQLite insertion based on field name"""
        if value is None:
            return None

        binary_fields = ['public', 'private', 'wif', 'hash', 'block_hash',
                       'prev_hash', 'spending_txid', 'latest_txid', 'raw']
        boolean_fields = ['compressed', 'is_private', 'used', 'multisig', 'sort_keys',
                         'coinbase', 'verified', 'double_spend', 'spent']
        numeric_fields = ['balance', 'address_index', 'depth', 'change', 'purpose',
                         'account_id', 'version', 'locktime', 'confirmations', 'block_height',
                         'size', 'fee', 'input_total', 'output_total', 'value', 'sequence',
                         'output_n', 'index_n', 'key_order', 'multisig_n_required']

        if field_name in binary_fields:
            if isinstance(value, (bytes, memoryview)):
                return bytes(value)
            elif isinstance(value, str):
                if all(c in '0123456789abcdefABCDEF' for c in value) and len(value) % 2 == 0:
                    try:
                        return bytes.fromhex(value)
                    except ValueError:
                        return value.encode('utf-8')
                return value.encode('utf-8')
            return str(value).encode('utf-8')

        if field_name in boolean_fields:
            if isinstance(value, bool):
                return value
            if isinstance(value, (int, float)):
                return bool(value)
            if isinstance(value, str):
                value = value.strip().lower()
                if value in ('1', 'true', 't', 'yes', 'y'):
                    return True
                if value in ('0', 'false', 'f', 'no', 'n'):
                    return False
            return bool(value)

        if field_name in numeric_fields:
            try:
                return int(value)
            except (ValueError, TypeError):
                return 0

        if isinstance(value, (bytes, memoryview)):
            try:
                return value.decode('utf-8')
            except UnicodeDecodeError:
                return value.hex()
        elif isinstance(value, (int, float)):
            return value

        return str(value)

    def process_key_fields(self, fields):
        """Process and clean key fields before insertion"""
        if 'key' in fields:
            if fields.get('is_private'):
                fields['private'] = self.convert_value(fields['key'], 'private')
            else:
                fields['public'] = self.convert_value(fields['key'], 'public')
            del fields['key']

        processed_fields = {}
        for field_name, value in fields.items():
            processed_fields[field_name] = self.convert_value(value, field_name)

        if 'used' not in processed_fields:
            processed_fields['used'] = False
        if 'balance' not in processed_fields:
            processed_fields['balance'] = 0
        if 'witness_type' not in processed_fields:
            processed_fields['witness_type'] = 'legacy'
        if 'encoding' not in processed_fields:
            processed_fields['encoding'] = 'base58'
        if 'key_type' not in processed_fields:
            processed_fields['key_type'] = 'bip32'
        if 'compressed' not in processed_fields:
            processed_fields['compressed'] = True

        return processed_fields

    def process_wallet_fields(self, fields):
        """Process and clean wallet fields before insertion"""
        processed_fields = {}
        for field_name, value in fields.items():
            processed_fields[field_name] = self.convert_value(value, field_name)

        if 'scheme' not in processed_fields:
            processed_fields['scheme'] = 'bip32'
        if 'witness_type' not in processed_fields:
            processed_fields['witness_type'] = 'legacy'
        if 'encoding' not in processed_fields:
            processed_fields['encoding'] = 'base58'
        if 'multisig' not in processed_fields:
            processed_fields['multisig'] = False
        if 'sort_keys' not in processed_fields:
            processed_fields['sort_keys'] = False

        return processed_fields

    def update_database(self):
        """Main method to update the database"""
        print("\nWallet and Key data will be copied to new database. Transaction data will NOT be copied")
        print("Updating database file: %s" % self.original_db_path)
        print("Old database will be backed up to %s" % self.database_backup_file)

        if input("Type 'y' or 'Y' to continue or any other key to cancel: ").lower() != 'y':
            print("Aborted by user")
            return False

        try:
            move(self.original_db_path, self.database_backup_file)
        except Exception as e:
            print(f"Error creating backup: {str(e)}")
            return False

        try:
            engine = create_engine(self.database_file)
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()

            engine_backup = create_engine('sqlite:///' + self.database_backup_file)
            Session_backup = sessionmaker(bind=engine_backup)
            session_backup = Session_backup()

            # Migrate wallets
            wallets = session_backup.execute(text("SELECT * FROM wallets"))
            for wallet in wallets:
                fields = {key: value for key, value in wallet._mapping.items()}
                fields = self.process_wallet_fields(fields)
                db_field_names = [column.name for column in DbWallet.__table__.columns]
                for field in list(fields.keys()):
                    if field not in db_field_names:
                        del fields[field]
                session.add(DbWallet(**fields))
            session.commit()

            # Migrate keys in batches
            batch_size = 100
            offset = 0
            while True:
                keys = session_backup.execute(text(f"SELECT * FROM keys LIMIT {batch_size} OFFSET {offset}"))
                keys = keys.fetchall()
                if not keys:
                    break

                for key in keys:
                    fields = {key: value for key, value in key._mapping.items()}
                    fields = self.process_key_fields(fields)
                    db_field_names = [column.name for column in DbKey.__table__.columns]
                    for field in list(fields.keys()):
                        if field not in db_field_names:
                            del fields[field]
                    session.add(DbKey(**fields))

                session.commit()
                offset += batch_size

            # Migrate multisig children
            keysubs = session_backup.execute(text("SELECT * FROM key_multisig_children"))
            for keysub in keysubs:
                fields = {key: self.convert_value(value, key) for key, value in keysub._mapping.items()}
                session.add(DbKeyMultisigChildren(**fields))
            session.commit()

            # Update version info
            version_config = session.query(DbConfig).filter(DbConfig.variable == 'version').first()
            if version_config:
                version_config.value = BITCOINLIB_VERSION
            else:
                session.add(DbConfig(variable='version', value=BITCOINLIB_VERSION))

            session.add(DbConfig(variable='upgrade_date', value=str(datetime.now())))
            session.commit()

            print("\nDatabase %s has been successfully updated!" % self.original_db_path)
            print("Backup of old database created at %s" % self.database_backup_file)
            print("You may need to rescan your wallets to rebuild transaction data")
            return True

        except Exception as e:
            print("\nError occurred during database update:", str(e))
            print("Restoring original database from backup...")
            if os.path.exists(self.database_backup_file):
                try:
                    move(self.database_backup_file, self.original_db_path)
                    print("Original database has been restored. No changes were made.")
                except Exception as restore_error:
                    print(f"Failed to restore original database: {str(restore_error)}")
                    print(f"Manual restoration required. Backup exists at: {self.database_backup_file}")
            else:
                print("Backup file not found. Manual restoration required.")
            return False
        finally:
            if 'session' in locals():
                session.close()
            if 'session_backup' in locals():
                session_backup.close()

def add_update_parser(subparsers):
    update_parser = subparsers.add_parser('update', help='Update database to latest version')
    update_parser.add_argument('--database', '-d', default=None,
                             help="Path to database file (default: bitcoinlib.sqlite)")
    return update_parser

def main_update(args):
    print("Database should update automatically when using BitcoinLib. If automatic update fails you can run this.")
    updater = DatabaseUpdater(args.database)
    return updater.update_database()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BitcoinLib Database update script')
    parser.add_argument('--database', '-d', default=None,
                      help="Path to database file (default: bitcoinlib.sqlite)")
    args = parser.parse_args()
    main_update(args)
