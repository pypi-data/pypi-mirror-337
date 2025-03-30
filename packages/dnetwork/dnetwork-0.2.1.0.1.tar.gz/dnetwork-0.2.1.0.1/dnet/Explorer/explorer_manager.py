

import json
import logging

from dnet.Api.api_manager import ApiManager
from dnet.Explorer.graphql_queries import GET_BLOCKCHAIN_EXPLORER, GET_BLOCKCHAIN_EXPLORER_BY_SEARCH

class ExplorerManager:
    def __init__(self, api_manager: ApiManager):
        """
        Initialize the CoinManager with an instance of ApiManager.
        :param api_manager: Instance of ApiManager for executing GraphQL operations.
        """
        self.api_manager = api_manager
        

    def get_blockchain_explorer(self, height):
        
        
        variables = {
            "height": height
        }
    
        response = self.api_manager._execute_graphql(GET_BLOCKCHAIN_EXPLORER, variables)
        
        return response
    
    def get_blockchain_explorer_by_search(self, address=None, block=None, tx_hash=None, token=None):
        """
        Searches the blockchain explorer based on various parameters.
        The search input should be a dictionary containing one of the following keys:
          - address
          - block
          - tx_hash
          - token
        
        :param search: dict with the search parameters.
        :return: GraphQL response for the search query.
        """
        variables = {
            "input": {
                "address": address,
                "block": block,
                "txHash": tx_hash,
                "token": token
                }
            
        }
        response = self.api_manager._execute_graphql(GET_BLOCKCHAIN_EXPLORER_BY_SEARCH, variables)
        return response