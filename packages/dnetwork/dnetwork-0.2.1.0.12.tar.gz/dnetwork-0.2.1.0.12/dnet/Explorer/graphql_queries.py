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
        txCount
       
        txs {
          ...transactionDetails
        }
        
      }

      ... on Transaction {
        ...transactionDetails
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
        mempoolTxids
        mempoolTxCount
    }
    
    fragment transactionDetails on Transaction {
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
            minerAddress
          }
        }
        coin {
          ...coinDetails
        }
      }


"""



GET_NEW_BLOCK_SUBSCRIPTION = """
subscription GetNewBlock {
    new_block {
        block_header {
            version
            block_hash
            prev_block_hash
            merkle_root
            timestamp
            bits
            nonce
        }
        block_size
        height
        tx_count
        txs {
            tx_id
            version
            lock_time
        }
    }
}
"""