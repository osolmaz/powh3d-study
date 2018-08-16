import web3

from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source, link_code
from web3.contract import ConciseContract

from helper import deploy_contract
from math import ceil

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Helvetica', 'Arial']


contract_source_code = open('powh3d.sol', 'r').read()
compiled_sol = compile_source(contract_source_code) # Compiled source code

n_installments = [1, 2, 4, 8, 16, 32]
# n_installments = [1, 2, 4]
bricked_eth_ratio = []
start_port = 9000
purchase_eth = 10000

for n_installment in n_installments:
    testrpc_provider = TestRPCProvider(port=start_port)
    start_port += 1
    w3 = Web3(testrpc_provider)

    Hourglass_addr, Hourglass = deploy_contract(w3, compiled_sol['<stdin>:Hourglass'])

    my_account = w3.eth.accounts[0]

    w3.eth.sendTransaction({'to': Hourglass_addr, 'from': my_account, 'value': w3.toWei(purchase_eth,'ether'), 'gas': 1000000})

    p3d_balance = Hourglass.balanceOf(my_account)
    sell_batch = ceil(p3d_balance/n_installment)

    for i in range(n_installment):
        Hourglass.sell(
            min(sell_batch, Hourglass.balanceOf(my_account)),
            transact={'from': my_account})

    balance_before_dividends = w3.eth.getBalance(my_account)
    Hourglass.withdraw(transact={'from': my_account})
    balance_after_dividends = w3.eth.getBalance(my_account)

    dividends = (balance_after_dividends-balance_before_dividends)*1e-18

    bricked_eth = Hourglass.totalEthereumBalance()*1e-18
    bricked_eth_ratio.append(bricked_eth/purchase_eth)

    testrpc_provider.server.shutdown()


# ax.text(0.0, 0.1, "PercentFormatter(xmax=5)",
#         fontsize=15, transform=ax.transAxes)

# plt.loglog(n_installments, bricked_eth_ratio, '-o')
# plt.grid()

# plt.grid(which='minor')
plt.xlabel('# of installments')
plt.title('Percentage of bricked ETH with respect to initial investment')

ax = plt.gca()
# ax.xaxis.set_minor_formatter(ticker.NullFormatter())
# ax.set_xticks(n_installments)
ax.grid(zorder=0)
ax.grid(which='minor', zorder=0, linestyle='--')
# ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))

ax.set_yscale('log')
ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=2))
# ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%.3f"))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

n_installments_str = [str(i) for i in n_installments]
plt.bar(n_installments_str, [100*i for i in bricked_eth_ratio], zorder=3)


plt.savefig('bricked_eth_installments.svg')
# plt.show()

