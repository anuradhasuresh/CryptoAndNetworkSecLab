import requests
from bs4 import BeautifulSoup

# url = 'https://gist.github.com/tayvano/7f8373a290a21568f2666929677daf54'
# block_num = 4650000

contract_addresses = []

for block_num in range(4650000, 4653000):
    url = f'https://etherscan.io/txs?block={block_num}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    contract_table = soup.find_all('table')[0]
    contract_rows = contract_table.find_all('tr')[1:]  # skip header row


    for row in contract_rows:
        columns = row.find_all('td')
        address_column = columns[1]
        to_column = columns[7]
        address = address_column.find_all('a')[0].string
        contract_addresses.append(address)

    if len(contract_addresses) == 500:
        break  # stop scraping after 500 addresses

with open('contract_address_list', 'w') as f:
    for addr in contract_addresses:
        f.write(addr+',')