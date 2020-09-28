# Want to show your support? Donate via PayPal or Bitcoin
# 1BHD7LQS9UkZvDXtoNjKrFMogJjPxz6aMj
# Have comments or questions? https://github.com/tg12


#/usr/bin/env python
import random
import decimal
import time
import datetime
import os
import sys
# Never run more than one instance at a time because we need the payment
# to confirm first

pid = str(os.getpid())
pidfile = "/tmp/mydaemon.pid"

if os.path.isfile(pidfile):
    print (pidfile + " already exists, exiting")
    sys.exit()
open(pidfile, 'w').write(pid)
try:

    # Do some actual work here
    # Authenticate First Step

    from coinbase.wallet.client import Client

    client = Client( << REMOVED>>, << REMOVED>>, api_version='2017-11-20')
    accounts = client.get_accounts()
    currency_code = 'GBP'  # can also use EUR, CAD, etc.

    for x in range(1):
        # Make the request
        #price = client.get_spot_price(currency=currency_code)
        #print ('Current bitcoin price in ' +  currency_code + " " +  price.amount)
        #price = client.get_buy_price(currency_pair = 'BTC-GBP')
        #print ('Current BTC BUY price in ' +  currency_code + " " +  price.amount)
        price = client.get_sell_price(currency_pair='BTC-GBP')
        print (
            'Current BTC SELL price in ' +
            currency_code +
            " " +
            price.amount)

    account_ = client.get_account("BTC")
    balance = account_.balance
    acc_id = str(account_.id)
    print ("DEBUG : account.balance " + str(balance.amount))

    # for account_ in accounts.data:
    #balance = account_.balance
    #print ("DEBUG : account.balance " + str(balance))
    #print (account.name, balance.amount, balance.currency)
    #print (account.get_transactions())

#**********************TESTING************************
#**********************TESTING************************
#**********************TESTING************************
#**********************TESTING************************

    # for x in range(100):
    #test_amount_btc = (format(random.uniform(0.001, 0.006),'.8f'))
    #amount_in_gbp_fiat = float(test_amount_btc) * float(price.amount)
    #print (test_amount_btc + "BTC is worth " +  format(amount_in_gbp_fiat,'.2f') + " GBP")

    # for x in range(5):
    #print("DEBUG ****END OF UNIT TEST*** float.price is " + price.amount)

#**********************TESTING************************
#**********************TESTING************************
#**********************TESTING************************
#**********************TESTING************************

# Notes
# balance.amount is always the number of BTC you HODL currently, Value is 0.00000000
# price.amount is the value of 1 BTC in nominated currency, This case GBP
# Thus, The math is this Number of Bitcoin's held for now less than 1, times by the price. That is the total value to you in fiat
# Work in fiat, because thats what we want after all, right??

    with open('/root/MyPythonCode/pricehist.txt', 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
        starting_price_fiat = float(last_line)

    # Current Price in GBP from last time
    print (
        "Your starting Fiat Balance is (Last time this script ran)  " +
        str(starting_price_fiat) +
        "GBP")

    # Current price from Exchange
    amount_in_gbp_fiat = float(balance.amount) * float(price.amount)
    print (
        "You current balance is worth in fiat (From the Exchange)  " +
        str(amount_in_gbp_fiat) +
        "GBP")

    # If the amount we have is more than we checked, Work out the price_change
    # and percentage change
    if amount_in_gbp_fiat > starting_price_fiat:
        # work out price increase and it's respective percentage
        price_change = float(amount_in_gbp_fiat - starting_price_fiat)
        percentage = 100 * float(price_change) / float(starting_price_fiat)
        print ("DEBUG: price_change " + str(price_change))
        print ("DEBUG: percentage  " + str(percentage))

        if percentage < -3:
          # Consider buying the dip if the price has gone down by more than 3%
            print ("DEBUG: FUTURE IMPLEMENTATION BTFD!!!")
            print ("Percentage Value was " + str(percentage))
            open('/root/MyPythonCode/tradingbot.log',
                 'a+').write("DEBUG: BTFD PRICE DROP!!! " + str(datetime.datetime) + '\n')
            open('/root/MyPythonCode/tradingbot.log',
                 'a+').write("Percentage Value was " + str(percentage) + '\n')

            #*****IMPLEMENT LATER****
            # 1. Buy a token tenners worth
            # 2. Wait for a bit to the transaction to confirm obvz
            # 3. Write new price to file
            # 4. Profit (Literally)

        elif percentage > 0.3:
            # If it reaches here you are in profit plus a little bit for fee's
            # and stuff
            open('/root/MyPythonCode/tradingbot.log', 'a+').write("DEBUG CONSIDER SELLING!!! " +
                                                                  str(datetime.datetime.now()) +
                                                                  " " +
                                                                  str(price_change) +
                                                                  " Percentage Increase is " +
                                                                  str(percentage) +
                                                                  '\n')
            # Write a little market to the file to signify this fact
            open('/root/MyPythonCode/pricehist.txt',
                 'a+').write("***PROFIT MARKER*** " + str(datetime.datetime.now()) + '\n')

            # Example - DO NOT USE
            #sell = client.sell('2bbf394c-193b-5b2a-9155-3b4732659ede',amount="10",currency="BTC", payment_method="83562370-3e5c-51db-87da-752af5ab9559")
            # DO THE SELL!
            # Is this a float or a string??? Not sure check this out later
            sell = client.sell(
                acc_id,
                total=float(price_change),
                currency="GBP")
            # GET THE SELL ID!
            sell_id = str(sell.id)
            print ("DEBUG: sell_id " + str(sell_id))

            sell_info = client.get_sell(acc_id, sell_id)

            #***FOR SOME REASON THIS DOESNT WORK BUT TRANSACTIONS COMPLETE QUICKLY ANYWAY***
            # while not str(sell_info.status) == "completed" or "cancelled":
        # time.sleep(3)
        #print ("DEBUG: Waiting for 5 seconds and check again, Status is  " + str(sell_info.status) )
        # NOTE: Status is either created, completed, canceled. loop whilst not
        # completed!!!! We need to wait to the transaction is either cancelled
        # or even better completed

            if str(sell_info.status) != "completed":
                print ("DEBUG : " + str(sell_info.status))
                time.sleep(35)

            # Once you have confirmed sale of the difference, There will be a
            # new starting price which we need to write to the file so it is
            # picked up next time
            # Wait a token 3 seconds for price to update before reading it
            time.sleep(3)
            tmp = float(balance.amount) * float(price.amount)
            new_start_price = str(tmp)
            print ("DEBUG: What is my new start price??? " + new_start_price)
            open('/root/MyPythonCode/pricehist.txt',
                 'a+').write(str(new_start_price) + '\n')
            #****Then make sure we never read the Profit market into the variable, Write it to the file.****
            # There you have it, Start again. Done everything we need to at
            # this point, Sold the price difference with Fee's back to start
            # again at this point.
            print ("DEBUG: Status is ... YAY SUCCESS!!!")
    else:
        print (
            "DEBUG: NO PROFIT OPPORTUNITY!!! Price is neither above 1.6% or below -3% to BTFD")
        open('/root/MyPythonCode/tradingbot.log', 'a+').write(str(datetime.datetime.now()) +
                                                              " DEBUG: NO PROFIT OPPORTUNITY!!! Price is neither above 1.6% or below -3% to BTFD" + '\n')
        # Write new starting price for next time no matter what it is.
        tmp = float(balance.amount) * float(price.amount)
        new_start_price = str(tmp)
        print ("DEBUG: What is my new start price??? " + new_start_price)
        open('/root/MyPythonCode/pricehist.txt',
             'a+').write(str(new_start_price) + '\n')

finally:
    os.unlink(pidfile)
