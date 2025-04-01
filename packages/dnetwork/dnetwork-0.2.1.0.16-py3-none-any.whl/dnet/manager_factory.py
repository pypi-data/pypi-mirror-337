# dnet/manager_factory.py

from dnet.Api.api_manager import ApiManager
from dnet.Coin.coin_manager import CoinManager
from dnet.Transaction.transaction_manager import TransactionManager
from dnet.Wallet.wallet_manager import WalletManager
from dnet.Explorer.explorer_manager import ExplorerManager


class DNetManager:
    """
    Central manager that initializes all sub‑managers.
    Users need only supply their API key.
    """

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API_KEY is required to initialize DNetManager.")
        self.base_url = "http://203.0.113.2:8000/api"  # Internal configuration
        wb_base_url = "ws://203.0.113.2:8000/api/"
        self.api_manager = ApiManager(self.base_url, api_key)
        self.wb_api_manager = ApiManager(wb_base_url, api_key)

        # Initialize sub‑managers
        self.wallet_manager = WalletManager(self.api_manager)
        self.coin_manager = CoinManager(self.api_manager)
        self.transaction_manager = TransactionManager(self.api_manager)
        self.explorer_manager = ExplorerManager(self.wb_api_manager, self.wb_api_manager)

    def get_wallet_manager(self):
        return self.wallet_manager

    def get_coin_manager(self):
        return self.coin_manager

    def get_transaction_manager(self):
        return self.transaction_manager
    
    def get_explorer_manager(self):
        return self.explorer_manager
