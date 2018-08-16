import web3

from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source, link_code
from web3.contract import ConciseContract

from helper import deploy_contract

contract_source_code = open('powh3d.sol', 'r').read()
compiled_sol = compile_source(contract_source_code) # Compiled source code

w3 = Web3(TestRPCProvider())

Hourglass_addr, Hourglass = deploy_contract(w3, compiled_sol['<stdin>:Hourglass'])

purchase_eth = 10000

my_account = w3.eth.accounts[0]
initial_eth_balance = w3.eth.getBalance(my_account)

# Send 10,000 ETH to the contract
w3.eth.sendTransaction({'to': Hourglass_addr, 'from': my_account, 'value': w3.toWei(purchase_eth,'ether'), 'gas': 1000000})

# Sell all P3D
Hourglass.sell(Hourglass.balanceOf(my_account), transact={'from': my_account})

# Withdraw dividends
Hourglass.withdraw(transact={'from': my_account})

final_eth_balance = w3.eth.getBalance(my_account)

print('Change in ETH own balance:', (final_eth_balance-initial_eth_balance)*1e-18)
print('P3D balance:', Hourglass.balanceOf(my_account)*1e-18)
print('Contract ETH balance:', Hourglass.totalEthereumBalance()*1e-18)
print('Contract P3D supply:', Hourglass.totalSupply()*1e-18)



