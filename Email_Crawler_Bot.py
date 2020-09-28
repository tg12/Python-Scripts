# Want to show your support? Donate via PayPal or Bitcoin
# 1BHD7LQS9UkZvDXtoNjKrFMogJjPxz6aMj
# Have comments or questions? https://github.com/tg12

import urllib
import httplib
import urllib2
import re
import os
import ssl
import socket
import time
from platform import system
from random import randint

socket.setdefaulttimeout(15)
ctx = None
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE
# opener = urllib2.build_opener(urllib2.HTTPSHandler(context=None))
# opener.addheaders = [('Mozilla/4.0 (compatible; MSIE 7.0; America Online Browser 1.1; Windows NT 5.1; (R1 1.5); .NET CLR 2.0.50727; InfoPath.1)')]
opener = urllib2.build_opener()
opener.addheaders = [
    (
        "Mozilla/4.0 (compatible; MSIE 7.0; America Online Browser 1.1; Windows NT 5.1; (R1 1.5); .NET CLR 2.0.50727; InfoPath.1)"
    )
]
headers = {
    "User-agent": "Mozilla/4.0 (compatible; MSIE 7.0; America Online Browser 1.1; Windows NT 5.1; (R1 1.5); .NET CLR 2.0.50727; InfoPath.1)"
}
try:
    open("collections.txt", "r").close()
except BaseException:
    open("collections.txt", "w+").close()
try:
    pbin = raw_input("Enable pastebin lookup? (y/n): ")
    slx = raw_input("Enable slexy lookup? (y/n): ")
    debp = raw_input("Enable paste.debian.org lookup? (y/n): ")
    cus = raw_input("Enable custom lookup? (y/n): ")
    srx = raw_input("Enable searx lookup? (y/n): ")
    if srx == "y":
        dork = raw_input(
            "type anything as keyword for the search engine(ex. halloween): "
        )
        pagedepth = int(input("enter amount of pages to look? (in integer number): "))
    prox = raw_input("Enable proxy? (y/n): ")
    if prox == "y":
        prox = "--proxy"
    # that damn blacklist will be created if not in there
    open("blacklist.txt", "a+").close()
    open("sources.txt", "a+").close()
    open("proxies.txt", "a+").close()
    proxies = open("proxies.txt", "r").read().split("\n")
    # Below function is created for extracting emails from specific url

    def getmails(link, proxy):
        # a'right. I gonna check if this link was already visited or not
        if link in open("blacklist.txt", "r").read():
            return
        print "Extracting emails from a webpage...\nSit tight ..."
        if "https://" not in link:
            if "http://" not in link:
                link = "http://" + link
        link = link.replace("\n", "")
        try:
            randomip = proxies[randint(0, len(proxies) - 1)]
            if proxy == "--proxy":
                dataOfLink = urllib.urlopen(link, proxies={"http": randomip}).read()
            else:
                dataOfLink = urllib.urlopen(link).read()
            mailsfound = re.findall('""?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)"?"', dataOfLink)
            for email in mailsfound:
                email = email.replace("\n", "")
                # below goes some banned keywords for email extraction
                # else garbage emails will be crawled
                if ".png" in email:
                    continue
                if ".gif" in email:
                    continue
                if ".jpg" in email:
                    continue
                if "._" in email:
                    continue
                if "@." in email:
                    continue
                if "." not in email:
                    continue
                try:
                    # below condition works to ensure unique emails
                    norepeat = open("collections.txt", "r").read()
                    if email not in norepeat:
                        # open('collections.txt', 'a+').write(email + ', ' + link + '\n')
                        open("collections.txt", "a+").write(email + "\n")
                except IOError:
                    open("collections.txt", "a+")
            # saving as blacklisted now
            open("blacklist.txt", "a+").write(link + "\n")
        except BaseException:
            pass

    # Below function is created for collecting pastebin recent pastes
    # WARNING: pastebin bans IP if much request is sent to their site
    # More info: https://pastebin.com/scraping
    def pastebin(prox):
        pburl = "https://pastebin.com/archive"
        try:
            randomip = proxies[randint(0, len(proxies) - 1)]
            if prox == "--proxy":
                getdata = urllib.urlopen(pburl, proxies={"http": randomip}).read()
            else:
                getdata = urllib.urlopen(pburl).read()
            pasteurl = re.findall('class="i_p0" alt="" /><a href="(.*?)">', getdata)
            for link in pasteurl:
                link = "https://pastebin.com/api_scrape_item.php?i=" + link
                getmails(link, prox)
                time.sleep(2)
        except IOError:
            pass
        except BaseException:
            pass

    # Below function is created for collecting slexy recent pastes
    def slexy(prox):
        pburl = "http://slexy.org/recent"
        try:
            randomip = proxies[randint(0, len(proxies) - 1)]
            if prox == "--proxy":
                getdata = urllib.urlopen(pburl, proxies={"http": randomip}).read()
            else:
                getdata = urllib.urlopen(pburl).read()
            pasteurl = re.findall('<td><a href="/view(.*?)">', getdata)
            for link in pasteurl:
                link = "http://slexy.org/raw" + link
                getmails(link, prox)
        except IOError:
            pass
        except BaseException:
            pass

    # Below function is created for collecting debpaste recent pastes
    def debpaste(prox):
        pburl = "http://paste.debian.net"
        try:
            randomip = proxies[randint(0, len(proxies) - 1)]
            if prox == "--proxy":
                getdata = urllib.urlopen(pburl, proxies={"http": randomip}).read()
            else:
                getdata = urllib.urlopen(pburl).read()
            pasteurl = re.findall("<li><a href='//paste.debian.net(.*?)'>", getdata)
            i = 1
            for link in pasteurl:
                link = "http://paste.debian.net/plain" + link
                getmails(link, prox)
                i += 1
                if i == 11:
                    # those are of no use, so stop
                    break
        except IOError:
            pass
        except BaseException:
            pass

    # this function is designed to extract emails from given urls(one url per
    # line)
    def customurl(prox):
        lines = open("sources.txt", "r").read().split("\n")
        for link in lines:
            link = link.replace("\n", "")
            ink = link.replace("\r", "")
            if "https://" not in link:
                if "http://" not in link:
                    link = "http://" + link
            getmails(link, prox)

    # Below function is created for collecting urls from searx search engines
    def searx(dork, pages, prox):
        sitelist = []
        print "You are searching: " + dork
        print "Page depth: ", pages
        p = 1
        m = pages  # max pages to crawl in the engine result
        while p <= m:
            data = urllib.urlencode(
                {
                    "category_general": "1",
                    "q": dork,
                    "pageno": p,
                    "time_range": "",
                    "language": "all",
                }
            )
            data = data.replace("+", "%20")
            try:
                search = urllib2.Request("https://searx.laquadrature.net/", data)
                req = opener.open(search)
                source = req.read()
                if "we didn't find any results" in source:
                    print "No Result in: " + dork
                    p = 100000000
                sites = re.findall(
                    'class="result_header"><a href="(.*?)" rel="noreferrer">', source
                )
                sitelist.extend(sites)
                if "</span> next page</button>" in source:
                    tp = p
                    p += 1
                    print "Scanned page(s) so far: " + str(tp)
                else:
                    p += 1000000000
            except urllib2.URLError as e:
                continue
            except urllib2.HTTPError as e:
                continue
            except IOError:
                continue
            except httplib.HTTPException:
                continue
            except BaseException:
                continue
        uniqsites = list(set(sitelist))
        for eachsite in uniqsites:
            getmails(eachsite, prox)

    # Main program interface starts from below
    print "Total emails in collections: ", len(
        open("collections.txt", "r+").readlines()
    )
    while True:
        if pbin == "y":
            print "Looking in pastebin ..."
            pastebin(prox)
        if slx == "y":
            print "Looking in slexy ..."
            slexy(prox)
        if debp == "y":
            print "Looking in debpaste"
            debpaste(prox)
        if cus == "y":
            print "Looking in File(sources.txt)"
            customurl(prox)
        if srx == "y":
            print "Attempting scan in Searx"
            searx(dork, pagedepth, prox)
        print "Total emails in collections now: ", len(
            open("collections.txt", "r+").readlines()
        )
        time.sleep(3)
except BaseException:
    print "USAGE: python bot.py"
