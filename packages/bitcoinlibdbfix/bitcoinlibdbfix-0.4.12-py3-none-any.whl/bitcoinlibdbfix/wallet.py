from typing import Dict, List, Optional, Tuple
import json
from bitcoinlib.wallets import Wallet, wallet_delete, wallets_list
from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.keys import HDKey
from bitcoinlib.main import DEFAULT_DATABASE, BCL_DATABASE_DIR

class WalletManager:
    def __init__(self, args):
        self.args = args
        self.wallet_name = args.wallet_name
        self.network = args.network or 'bitcoin'

    def create_wallet(self):
        """Create a new wallet based on provided arguments"""
        if self.args.create_multisig:
            self._create_multisig_wallet()
        else:
            self._create_standard_wallet()

    def _create_standard_wallet(self):
        """Create a standard single-signature wallet"""
        passphrase = self.args.passphrase or Mnemonic().generate(strength=self.args.passphrase_strength)

        Wallet.create(
            name=self.wallet_name,
            keys=passphrase,
            network=self.network,
            witness_type=self.args.witness_type,
            db_uri=self.args.database
        )
        print(f"Wallet '{self.wallet_name}' created successfully")
        print(f"Passphrase: {passphrase}")

    def _create_multisig_wallet(self):
        """Create a multisig wallet"""
        # Implementation for multisig wallet creation
        pass

    def list_wallets(self):
        """List all available wallets"""
        wallets = wallets_list(db_uri=self.args.database)
        for wallet in wallets:
            print(f"{wallet['id']}: {wallet['name']} ({wallet['network']})")

    def generate_key(self):
        """Generate a new master key"""
        passphrase = Mnemonic().generate(strength=self.args.passphrase_strength)
        key = HDKey.from_passphrase(passphrase)

        print(f"Passphrase: {passphrase}")
        print(f"WIF: {key.wif()}")
        print(f"Public Account Key: {key.public_master().wif()}")

    def import_transaction_file(self, filename: str):
        """Import transaction from file"""
        try:
            with open(filename, 'r') as f:
                tx_data = json.load(f)

            wallet = Wallet(self.wallet_name, db_uri=self.args.database)
            tx = wallet.transaction_import(tx_data)

            print(f"Transaction imported successfully: {tx.hash}")
            if self.args.push:
                tx.send()
                print("Transaction pushed to network")
        except Exception as e:
            raise Exception(f"Failed to import transaction: {str(e)}")

    def send_transaction(self, outputs: List[Tuple[str, str]], fee: Optional[int], push: bool):
        """Send a transaction"""
        wallet = Wallet(self.wallet_name, db_uri=self.args.database)

        output_list = [(address, int(float(amount) * 100000000)) for address, amount in outputs]

        tx = wallet.send_to(output_list, fee=fee, broadcast=push)

        print(f"Transaction created: {tx.hash}")
        if push:
            print("Transaction pushed to network")
