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



#!/usr/bin/python

# Want to show your support? Donate via PayPal or Bitcoin
# 1BHD7LQS9UkZvDXtoNjKrFMogJjPxz6aMj
# Have comments or questions? https://github.com/tg12

import os
import sys
import getopt
import ecdsa
import urllib2
import binascii
import hashlib
import random
import requests
import base58

word_file = "/root/MASTER.txt"
WORDS = open(word_file).read().splitlines()

b58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def base58encode(n):
    result = ""
    while n > 0:
        result = b58[n % 58] + result
        n /= 58
    return result


def base256decode(s):
    result = 0
    for c in s:
        result = result * 256 + ord(c)
    return result


def countLeadingChars(s, ch):
    count = 0
    for c in s:
        if c == ch:
            count += 1
        else:
            break
    return count


def base58CheckEncode(version, payload):
    s = chr(version) + payload
    checksum = hashlib.sha256(hashlib.sha256(s).digest()).digest()[0:4]
    result = s + checksum
    leadingZeros = countLeadingChars(result, "\0")
    return "1" * leadingZeros + base58encode(base256decode(result))


secp256k1curve = ecdsa.ellipticcurve.CurveFp(
    115792089237316195423570985008687907853269984665640564039457584007908834671663,
    0, 7)
secp256k1point = ecdsa.ellipticcurve.Point(
    secp256k1curve,
    0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
)
secp256k1 = ecdsa.curves.Curve("secp256k1", secp256k1curve, secp256k1point,
                               (1, 3, 132, 0, 10))


def privateKeyToWif(key_hex):
    return base58CheckEncode(0x80, key_hex.decode("hex"))


def addy(pk):
    pko = ecdsa.SigningKey.from_secret_exponent(pk, secp256k1)
    pubkey = binascii.hexlify(pko.get_verifying_key().to_string())
    pubkey2 = hashlib.sha256(binascii.unhexlify("04" + pubkey)).hexdigest()
    pubkey3 = hashlib.new("ripemd160", binascii.unhexlify(pubkey2)).hexdigest()
    pubkey4 = hashlib.sha256(binascii.unhexlify("00" + pubkey3)).hexdigest()
    pubkey5 = hashlib.sha256(binascii.unhexlify(pubkey4)).hexdigest()
    pubkey6 = pubkey3 + pubkey5[:8]
    pubnum = int(pubkey6, 16)
    pubnumlist = []
    while pubnum != 0:
        pubnumlist.append(pubnum % 58)
        pubnum /= 58
    address = ""
    for l in [
            "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"[x]
            for x in pubnumlist
    ]:
        address = l + address
    return "1" + address


# if __name__ == "__main__":
# if len(sys.argv) != 2:
# sys.exit("ERROR: Provide brainwallet string as parameter\n./brainwallet-check.py 'Satoshi Nakamoto'")
while True:
    passphrase = random.choice(WORDS)
    privatekey = int(hashlib.sha256(passphrase).hexdigest(), 16)
    privatekeysha = (hashlib.sha256(passphrase)).hexdigest()
    bcaddy = addy(privatekey)
    word = str(passphrase)
    try:
        firstseen = requests.get("https://blockchain.info/q/addressfirstseen/" +
                                 bcaddy)
        amount = requests.get("https://blockchain.info/rawaddr/" + bcaddy)
    except BaseException:
        print("ERROR!!")

    # print "-----------------------------------------------------"
    print "brainwallet string: " + str(word)
    print "private key: " + str(privatekeysha)
    print "WIF format " + str(privateKeyToWif(privatekeysha))
    print "bitcoin address: " + str(bcaddy)
    try:
        if str(firstseen) == "null":
            print "[ADDRESS ISN'T IN USE ACCORDING TO BLOCKCHAIN.INFO]"
        else:
            # first_seen = float(r.json()['final_balance'])
            # print "First seen according to blockchain.info: " +  first_seen
            acc_bal = float(amount.json()["final_balance"])
            print "Wallet amount: " + str(acc_bal)
        print "-----------------------------------------------------"
    except BaseException:
        print("ERROR!!")
