'''THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND
NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE
DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY,
WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

# Bitcoin Cash (BCH)   qpz32c4lg7x7lnk9jg6qg7s4uavdce89myax5v5nuk
# Ether (ETH) -        0x843d3DEC2A4705BD4f45F674F641cE2D0022c9FB
# Litecoin (LTC) -     Lfk5y4F7KZa9oRxpazETwjQnHszEPvqPvu
# Bitcoin (BTC) -      34L8qWiQyKr8k4TnHDacfjbaSqQASbBtTd

# contact :- github@jamessawyer.co.uk



# Want to show your support? Donate via PayPal or Bitcoin
# 1BHD7LQS9UkZvDXtoNjKrFMogJjPxz6aMj
# Have comments or questions? https://github.com/tg12

import random
import decimal
import time

# Authenticate First Step

from coinbase.wallet.client import Client

client = Client("<<REMOVED>>", "<<REMOVED>>", api_version="2017-11-20")

accounts = client.get_accounts()

for account in accounts.data:
    balance = account.balance
    # print (account.name, balance.amount, balance.currency)
    # print (account.get_transactions())
    # print (account.name, balance.amount, balance.currency)

# account = client.create_account(name="New Wallet")
# balance = account.balance

# Generate a new bitcoin address for your primary account:
primary_account = client.get_primary_account()

address = account.create_address()

# View the last transaction
# print primary_account.get_transactions()[-1]
# After some time, the transaction should complete and your balance should update
# primary_account.refresh()
# balance = primary_account.balance
# print "%s: %s %s" % (primary_account.name, balance.amount, balance.currency)

# **********************************************************

# Two variables
# One is randomly generated amount (donate_amount)
# other is read in from text file (email)

for x in range(15):
    lines = open("/root/MyPythonCode/testdata.txt").read().splitlines()
    email = random.choice(lines)

    value = format(random.uniform(0.001, 0.006), ".8f")

    print("DEBUG!!!" + email + " " + value)

    tx = primary_account.request_money(
        to=email,
        amount=value,
        currency="BTC",
        description="Please can you spare some change?",
    )

    word_file = "/usr/share/dict/words"
    WORDS = open(word_file).read().split()
    words = " ".join(random.choice(WORDS) for i in range(5))

    print("DEBUG!!!" + email + " " + words)

    # tx = primary_account.request_money(to=email, amount=0.00000010, currency='BTC', description=word_string)
    time.sleep(random.randint(1, 120))
