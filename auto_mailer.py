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

# -*- coding: utf-8 -*-
import smtplib
import time
import random
import names
from random import randint
from time import sleep

from email.Header import Header
from email.mime.text import MIMEText

# Open a file for reading

lines = open("/root/MyPythonCode/testdata.txt").read().splitlines()
me = "<<REMOVED>>"  # change to your email
p_reader = open("<<REMOVED>>", "rb")  # edit for your password
cipher = p_reader.read()

while True:
    email = random.choice(lines)
    firstname = names.get_first_name()
    recipients = [email]  # enter recipients here
    fp = open("message.txt", "rb")
    # multipart class is for multiple recipients
    msg = MIMEText(fp.read(), "html", "utf-8")
    fp.close()
    thread_number = random.randint(0, 10000)
    msg["Subject"] = Header("Hi " + firstname + ",  Hi!", "utf-8")
    msg["From"] = me
    msg["To"] = ", ".join(recipients)
    s = smtplib.SMTP(host="smtp.gmail.com", port=587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(me, cipher)
    s.sendmail(me, recipients, msg.as_string())

    print "Email sent to: " + ", ".join(recipients)
    s.quit()
    time.sleep(randint(1, 100))  # change rate of fire here
