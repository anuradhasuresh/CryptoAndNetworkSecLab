import requests
import time

API_KEY = '2TF3RVBP65RY5TFHRAE3KIVGEIYZC3HXRE'

def get_bytecode(contract_address):
    url = f'https://api.etherscan.io/api?module=proxy&action=eth_getCode&address={contract_address}&apikey={API_KEY}'
    response = requests.get(url)
    return response.json()['result']

def download_bytecode():
    i, j = 0, 0
    with open('contract_address_list', 'r') as f:
        contract_addresses = f.read().split(',')
    print(len(contract_addresses), contract_addresses[-1])
    contract_addresses = contract_addresses[:1000]
    for addr in contract_addresses:
        # contract_addr = '0x' + ''.join(random.choices('0123456789abcdefABCDEF', k=40))
        contract_addr = addr
        bytecode = get_bytecode(contract_addr)
        j+=1
        if j % 5 == 0:
            j = 0
            time.sleep(1)
            # EtherScan's free API allows only for 5 API calls per second
        if len(bytecode) <= 2:
            continue
        i+=1
        with open(f'contracts/test{i}.contract.code', 'w') as f:
            f.write(bytecode[2:])
        print(f'Downloaded bytecode for contract {i} with address {contract_addr} ')

# get_bytecode('0x91bCB26A393D17AfA7460d00EEA3F604C53f67c9')
download_bytecode()