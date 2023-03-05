from pybithumb import Bithumb
import sqlite3
import os
import json
import random

def create_coins_db():
    con = sqlite3.connect('coins.db')
    cur = con.cursor()

    # Create table
    cur.execute("CREATE TABLE coins (name PRIMARY KEY, source NOT NULL, post, link NOT NULL)")
    con.commit()

    # insert first values
    query = "INSERT INTO coins VALUES (?, ?, ?, ?)"
    for coin in coins.items():
        params = (coin[0], coin[1]["source"], coin[1]["post"], coin[1]["link"])
        cur.execute(query, params)
    con.commit()
    con.close()
def update_post(post, coin):
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    query = "UPDATE coins SET post = ? WHERE name = ?"
    cur.execute(query, (json.dumps(post, ensure_ascii = False), coin))
    con.commit()
    con.close()
def get_coin(coin):
    # Import DB to get coin information
    con = sqlite3.connect(os.path.abspath('coins.db'))
    cur = con.cursor()
    query = "SELECT * FROM coins WHERE name = ?"
    item = cur.execute(query, (coin,)).fetchone()
    con.close()
    return {
            "name": item[0],
            "source": item[1],
            "post": item[2],
            "link": item[3]
        }
def get_all_coins():
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    item = cur.execute("SELECT * FROM coins").fetchall()
    con.close()
    try:
        res = []
        for i in item:
            res.append({
            "name": i[0],
            "source": i[1],
            "post": i[2],
            "link": i[3]
            })
        return res
    except:
        return None

# Deprecated
def insert_coin(coins):
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    query = "INSERT INTO coins VALUES (?, ?, ?, ?, ?, ?)"

    for coin in coins.items():
        params = list((coin[0], coin[1]["source"], coin[1]["link"], coin[1]["selector"], coin[1]["post"], coin[1]["groups"]))
        cur.execute(query, params)
    con.commit()
    con.close()
def get_ticker():
    tickers = {}
    tickers["KRW"] = Bithumb.get_tickers('KRW')
    tickers["BTC"] = list((btc_ticker for btc_ticker in Bithumb.get_tickers('btc') if btc_ticker not in tickers['KRW']))
    return tickers
def get_working_proxy():
    con = sqlite3.connect(os.path.abspath('coins.db'))
    cur = con.cursor()
    proxls = cur.execute("SELECT * FROM working_proxy").fetchall()
    con.close()
    if len(proxls) != 0:
        return proxls[random.randint(0, len(proxls) - 1)][0]
    else:
        return None
def write_proxy(proxy):
    con = sqlite3.connect(os.path.abspath('coins.db'))
    cur = con.cursor()
    query = "INSERT INTO working_proxy VALUES (?)"
    cur.execute(query, (proxy, ))
    con.commit()
    con.close()
def delete_proxy(proxy):
    con = sqlite3.connect(os.path.abspath('coins.db'))
    cur = con.cursor()
    query = "DELETE FROM working_proxy WHERE proxy = ?"
    cur.execute(query, (proxy, ))
    con.commit()
    con.close()
def reset_proxy():
    con = sqlite3.connect(os.path.abspath('coins.db'))
    cur = con.cursor()
    cur.execute("DELETE FROM working_proxy")
    con.commit()
    con.close()
def overhaul_post(coin, name):
    con = sqlite3.connect('coins.db')
    cur = con.cursor()
    query = "UPDATE coins SET source = ?, link = ?, selector = ?, post = ?, groups = ? WHERE name = ?"
    cur.execute(query, (coin['source'], coin['link'], coin['selector'], coin['post'], coin['groups'], name))
    con.commit()
    con.close()

coins = {
    "META": {
    "source": "brunch",
    "link": "https://brunch.co.kr/magazine/metadium-info",
    "post": ""
    },
    "EGLD": {
    "source": "github",
    "link": "https://github.com/ElrondNetwork/elrond-go/releases/latest",
    "post": ""
    },
    "THETA": {
    "source": "github",
    "link": "https://github.com/thetatoken/theta-protocol-ledger/releases/latest",
    "post": ""
    },
    "TFUEL": {
    "source": "github",
    "link": "https://github.com/thetatoken/theta-protocol-ledger/releases/latest",
    "post": ""
    },
    "TDROP": {
    "source": "github",
    "link": "https://github.com/thetatoken/theta-protocol-ledger/releases/latest",
    "post": ""
    },
    "CTXC": {
    "source": "github",
    "link": "https://github.com/CortexFoundation/CortexTheseus/releases/latest",
    "post": ""
    },
    "MEDI": {
    "source": "github_repo",
    "link": "https://github.com/medibloc/panacea-governance/tree/main/proposals",
    "post": ""
    },
    "XYM": {
    "source": "github",
    "link": "https://github.com/symbol/symbol/releases/latest",
    "post": ""
    },
    "ATOLO": {
    "source": "mintscan",
    "link": "https://www.mintscan.io/rizon/proposals",
    "post": ""
    },"HIVE": {
    "source": "github",
    "link": "https://github.com/openhive-network/hive/releases/latest",
    "post": ""
    },"QKC": {
    "source": "github_repo",
    "link": "https://github.com/QuarkChain/QCEPs/tree/master/QCEP",
    "post": ""
    },"ZIL": {
    "source": "github",
    "link": "https://github.com/Zilliqa/Zilliqa/releases/latest",
    "post": ""
    },"XTZ": {
    "source": "xtz_agora",
    "link": "https://www.tezosagora.org/period/",
    "post": ""
    },"ICX": {
    "source": "icx_forum",
    "link": "https://forum.icon.community/search?expanded=true&q=hard%20fork",
    "post": ""
    },"VET": {
    "source": "github",
    "link": "https://github.com/vechain/thor/releases/latest",
    "post": ""
    },"XEC": {
    "source": "github",
    "link": "https://github.com/Bitcoin-ABC/bitcoin-abc/releases/latest",
    "post": ""
    },"SNX": {
    "source": "snx_blog",
    "link": "https://blog.synthetix.io/author/synthetix/",
    "post": ""
    },"ALGO": {
    "source": "github",
    "link": "https://github.com/algorand/go-algorand/releases/latest",
    "post": ""
    },"ONT": {
    "source": "github",
    "link": "https://github.com/ontio/ontology/releases/latest",
    "post": ""
    },"ONG": {
    "source": "github",
    "link": "https://github.com/ontio/ontology/releases/latest",
    "post": ""
    },"BNB": {
    "source": "github",
    "link": "https://github.com/bnb-chain/node/releases/latest",
    "post": ""
    },"IOST": {
    "source": "github",
    "link": "https://github.com/iost-official/go-iost/releases/latest",
    "post": ""
    },"QTUM": {
    "source": "github",
    "link": "https://github.com/qtumproject/qtum/releases/latest",
    "post": ""
    },"CTK": {
    "source": "github_repo",
    "link": "https://github.com/ShentuChain/mainnet",
    "post": ""
    },"VELO": {
    "source": "github",
    "link": "https://github.com/stellar/stellar-core/releases/latest",
    "post": ""
    },"CENNZ": {
    "source": "github",
    "link": "https://github.com/cennznet/cennznet/releases/latest",
    "post": ""
    },"ETC": {
    "source": "xangle",
    "link": "https://xangle.io/insight/disclosure?search=etc&category=network_fork",
    "post": ""
    },"CSPR": {
    "source": "github_wiki",
    "link": "https://github.com/casper-network/casper-node/wiki",
    "post": ""
    },"REI": {
    "source": "github",
    "link": "https://github.com/REI-Network/rei/releases/latest",
    "post": ""
    },"CKB": {
    "source": "github",
    "link": "https://github.com/nervosnetwork/ckb/releases/latest",
    "post": ""
    },"ELF": {
    "source": "github",
    "link": "https://github.com/AElfProject/AElf/releases/latest",
    "post": ""
    },"KCT-7": {
    "source": "github",
    "link": "https://github.com/klaytn/klaytn/releases/latest",
    "post": ""
    },"TRC-20": {
    "source": "github",
    "link": "https://github.com/tronprotocol/java-tron/releases/latest",
    "post": ""
    },"BEP-20": {
    "source": "github",
    "link": "https://github.com/bnb-chain/bsc/releases/latest",
    "post": ""
    },"ERC-20": {
    "source": "github",
    "link": "https://github.com/ethereum/go-ethereum/releases/latest",
    "post": ""
    },"COINDAR HARD FORK DISCLOSURE": {
    "source": "coindar",
    "link": "https://coindar.org/en/search?page=1&text=&start=2021-12-04&cats=10&im=&rs=0&fav=0&coins=&cap_from=0&cap_to=9999999999999&vol_from=0&vol_to=9999999999999&ex=1249,1308,1312&sort=1&order=1",
    "post": ""
    }, "XANGLE TOKEN SWAP DISCLOSURE": {
    "source": "xangle_swap",
    "link": "https://xangle.io/insight/disclosure?category=token_swap",
    "post": ""
    }, "XANGLE TOKEN REBRAND DISCLOSURE": {
    "source": "xangle_rebrand",
    "link": "https://xangle.io/insight/disclosure?category=token_rebranding",
    "post": ""
    }
}

if __name__ == "__main__":
    create_coins_db()