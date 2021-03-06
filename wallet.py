import subprocess
import json
from constants import *
from dotenv import load_dotenv
from web3 import Web3
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
import os

from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

w3.middleware_onion.inject(geth_poa_middleware, layer=0)


load_dotenv()
mnemonic = os.getenv('MNEMONIC' , 'dawn early execute magic lounge share leopard window method venue scan grace trust cart theme')


def derive_wallets(mnemonic, coin, numderive):
    command = f'php ./derive -g --mnemonic="{mnemonic}" --numderive={numderive} --coin={coin} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return keys

coin_types = {"eth", "btc-test", "btc"}

coins = {}
for coin in coin_types:
    coins[coin]= derive_wallets(mnemonic, coin, numderive=3)

eth_PrivateKey = coins["eth"][0]['privkey']
btc_PrivateKey = coins['btc-test'][0]['privkey']


def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account,privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

def create_tx(coin, account, to, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas({"from":eth_acc.address, "to": to, "value": amount})
        
        return{
            "from": eth_acc.address,
            "to" : to,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(eth_acc.address)
        }
    
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])

def send_tx(coin, account, to, amount):
    raw_tx = create_tx(coin, account, to, amount)
    if coin == ETH:
        tx_sign = eth.acc.sign_transaction(raw_tx)
        result = w3.eth.sendRawTransaction(tx_sign.rawTransaction)
        print(result.hex())
        return result.hex()
    elif coin == BTCTEST:
        tx_sign = account.sign_transaction(raw_tx)
        return NetworkAPI.broadcast_tx_testnet(tx_sign)
    
    