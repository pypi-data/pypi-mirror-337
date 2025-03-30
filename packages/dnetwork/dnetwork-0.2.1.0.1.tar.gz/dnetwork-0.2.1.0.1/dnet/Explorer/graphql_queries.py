GET_BLOCKCHAIN_EXPLORER = """
query GetBlockByHeight($height: Int!) {
    block(height: $height) {
        blockHeader {
            version
            blockHash
            prevBlockHash
            merkleRoot
            timestamp
            bits
            nonce
        }
        blockSize
        height
        txCount
        txs {
            txId
            version
            lockTime
            txIns {
                prevIndex
                prevTx
                sequence
                scriptSig {
                    cmds
                }
            }
            txOuts {
                amount
                scriptPubkey {
                    cmds
                }
            }
        }
    }
}
"""



GET_BLOCKCHAIN_EXPLORER_BY_SEARCH = """
   query GetBlockchainExplorerBySearch($input: SearchInput!) {
  search(input: $input) {
    __typename           
    success
    error
    data {
      __typename      
      
      ... on BlockInfo {
        blockHeader {
          version
          blockHash
          prevBlockHash
          merkleRoot
          timestamp
          bits
          nonce
        }
        blockSize
        height
        coinId
        txCount
        txs {
          txId
          version
          lockTime
          coinId
          txIns {
            prevIndex
            prevTx
            sequence
            scriptSig {
              cmds
            }
          }
          txOuts {
            amount
            scriptPubkey {
              cmds
                minerAddress
            }
          }
        }
      }

      ... on Transaction {
        txId
        version
        lockTime
        coinId
        fee
        block {
          height
          blockHash
          timestamp
        }
        userTransaction {
          transactionId
          amount
          status
          transactionType
          timestamp
          linkedFeeTxId
          linkedAltTxId
          senderWallet {
            ...walletDetails
          }
          recipientWallet {
            ...walletDetails
          }
        }
        txIns {
          prevIndex
          prevTx
          sequence
          scriptSig {
            cmds
          }
        }
        txOuts {
          amount
          scriptPubkey {
            cmds
          }
        }
        coin {
          ...coinDetails  
        }
      }

      ... on WalletTypes {
        ...walletDetails
        rawBalance
        updatedAt
        coin {
          ...coinDetails  
        }
      }

      ... on CoinTypes {
        ...coinDetails  
      }
    }
  }
}
    fragment walletDetails on WalletTypes {
        id
        publicAddress
        balance
        label
        transactionCount
        previousTransactions
        aggregatedRewards
        balanceBreakdown
    }


    fragment coinDetails on CoinTypes {
        id
        name
        symbol
        maxSupply
        totalSupply
        decimals
        contractAddress
        governanceModel
        transactionFee
        visibility
        coinMetadata
        createdTime
        price
        change24h
        priceChangeUsd
        volume1hr
        volume24h
        marketCap
        prices7d
        circulatingSupply
        typicalHoldTime
        volumeMarketCapRatio
        trendingActivity
        popularity
        allTimeHigh
        rank
        orderBook
        candlesticks
        historicalData
    }

"""


