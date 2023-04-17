import requests
import time

API_KEY = '2TF3RVBP65RY5TFHRAE3KIVGEIYZC3HXRE'

start_block = 4650000
end_block = 46530000

# url = f'https://api.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&apikey={API_KEY}&blockno='
url = f'https://api.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&boolean=true&apikey={API_KEY}&tag='

valid_contract_addresses = []

for block_number in range(start_block, end_block):
    if block_number%5 == 0:
        time.sleep(1)
    block_hex = hex(block_number)
    print(block_hex)
    response = requests.get(str(url + block_hex))
    block = response.json()
    block = block['result']
    transactions = block['transactions']
    i = 0
    for transaction in transactions:
        if transaction['to'] == None: # Contract creation transaction
            print(transaction)
            contract_address = transaction['from']
            code_response = requests.get(f'https://api.etherscan.io/api?module=proxy&action=eth_getCode&apikey={API_KEY}&address={contract_address}&tag={block_hex}')
            i+=1
            if i%5 ==0:
                time.sleep(1)
                # EtherScan's API free tier only allows 5 API calls per second.
                i = 0
            code = code_response.json()
            print(code)
            code = code['result']
            if code != '0x': # Valid contract address
                valid_contract_addresses.append(contract_address)
    if len(valid_contract_addresses) == 1000:
        break

print(valid_contract_addresses)