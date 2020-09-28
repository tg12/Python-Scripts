# This graphs the UK National Grid Demand for Energy, Fun project. Produces nice graphs.
# Various debugging bit's and bobs in this file, Code is hacky in some parts but solid.
# Play around with the variables to produce pretty graphs based on the National Grid (UK) Power usage.
# You will need an API key from Elexon, It's free as far as I can tell.
# https://www.elexon.co.uk/documents/training-guidance/bsc-guidance-notes/bmrs-api-and-data-push-user-guide-2/

#!/usr/env/bin python3
from colorama import Fore, Style, init, Back
import colorama
import scipy.stats as stats
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time
import json
import pprint
import xmltodict
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# from scipy.signal import find_peaks #reserved for future use
# Scikit's LinearRegression model
# from sklearn.linear_model import LinearRegression #reserved for future use
# On Windows, calling init() will filter ANSI escape sequences out of any
# text sent to stdout or stderr, and replace them with equivalent Win32
# calls.
init()

# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL
# Now regular ANSI codes should work, even in Windows
CLEAR_SCREEN = "\033[2J"
RED = "\033[31m"  # mode 31 = red forground
RESET = "\033[0m"  # mode 0  = reset


API_VERSION = "v1"
KEY = "<<INSERT KEY HERE>>"
DAYS_TO_LOOK_BACK = 25


def ceil_dt(dt, delta):
    return dt + (datetime.min - dt) % delta


half_hour = [
    "%s:%s%s" % (h, m, ap)
    for ap in ("am", "pm")
    for h in ([12] + list(range(1, 12)))
    for m in ("00", "30")
]
today = datetime.now()

for i in range(0, DAYS_TO_LOOK_BACK):

    today += timedelta(days=-1)
    req_str = (
        "https://api.bmreports.com/BMRS/SYSDEM/"
        + str(API_VERSION)
        + "?APIKey="
        + str(KEY)
        + "&FromDate="
        + str(str(today.strftime("%Y-%m-%d")))
        + "&ToDate="
        + str(today.strftime("%Y-%m-%d"))
        + "&ServiceType=xml"
    )
    # verify=False is needed for some crappy interception proxys. Are you behind a corporate firewall perhaps?. Should be
    # fine without it on Home connections
    data = requests.get(
        req_str,
        headers={"Content-Type": "application/xml; charset=UTF-8"},
        verify=False,
    )
    json_data = json.dumps(xmltodict.parse(data.text))
    system_demand = json.loads(json_data)["response"]
    pp = pprint.PrettyPrinter(indent=2)
    # print(pp.pprint(json.loads(json_data)["response"]))

    x = []
    y = []

    for each in system_demand["responseBody"]["responseList"]["item"]:
        # print (half_hour[int(each["settlementPeriod"]) -1 ]) #-1 because you
        # know, it's a list!
        dt_tm_string = half_hour[int(each["settlementPeriod"]) - 1]
        dt_tm_string = datetime.strptime(dt_tm_string, "%I:%M%p").strftime("%I:%M%p")
        x.append(dt_tm_string)
        # print (float(each["demand"]))
        y.append(float(each["demand"]))

    averages = {}
    counts = {}
    for name, value in zip(x, y):
        if name in averages:
            averages[name] += value
            counts[name] += 1
        else:
            averages[name] = value
            counts[name] = 1
    for name in averages:
        averages[name] = averages[name] / float(counts[name])

    x = [k for k in averages]
    y = [v for v in averages.values()]

    plt.plot(x, y, "--", label=str(today.strftime("%A %Y-%m-%d")))

plt.xticks(rotation=90, fontsize=12)
plt.legend(loc="upper left")
plt.grid()
plt.show()

if __name__ == "__main__":

    while True:

        ####################
        # Grab today's data
        ####################
        today = datetime.now()
        req_str = (
            "https://api.bmreports.com/BMRS/ROLSYSDEM/"
            + str(API_VERSION)
            + "?APIKey="
            + str(KEY)
            + "&FromDateTime="
            + str(str(today.strftime("%Y-%m-%d")) + " 00:01:01")
            + "&ToDateTime="
            + str(today.strftime("%Y-%m-%d %H:%M:%S"))
            + "&ServiceType=xml"
        )
        # verify=False is needed for some shitty interception proxys. Should be
        # fine without it on Home connections
        data = requests.get(
            req_str,
            headers={"Content-Type": "application/xml; charset=UTF-8"},
            verify=False,
        )
        json_data = json.dumps(xmltodict.parse(data.text))
        system_demand = json.loads(json_data)["response"]

        time_graph = []
        gen_graph = []
        for each in system_demand["responseBody"]["responseList"]["item"]:
            time_graph.append(
                datetime.strftime(
                    ceil_dt(
                        datetime.strptime(
                            each["publishingPeriodCommencingTime"], "%H:%M:%S"
                        ),
                        timedelta(minutes=15),
                    ),
                    "%H:%M",
                )
            )
            gen_graph.append(float(each["fuelTypeGeneration"]))

        print(time_graph[-1])
        print(gen_graph[-1])
        print(stats.zscore(gen_graph, ddof=1)[-1])  # zscore deviation
        current_z_score = stats.zscore(gen_graph, ddof=1)[-1]
        ####################
        # Grab today's data
        ####################

        today = datetime.now()
        ys = []
        z_scores = []

        for i in range(0, DAYS_TO_LOOK_BACK):

            today += timedelta(days=-7)
            # nb, If you do days=-7 you will get the same day of the week to compare to.
            # if you do days=-1 you will get different days of the week counting
            # backwards

            req_str = (
                "https://api.bmreports.com/BMRS/ROLSYSDEM/"
                + str(API_VERSION)
                + "?APIKey="
                + str(KEY)
                + "&FromDateTime="
                + str(str(today.strftime("%Y-%m-%d")) + " 00:01:01")
                + "&ToDateTime="
                + str(today.strftime("%Y-%m-%d %H:%M:%S"))
                + "&ServiceType=xml"
            )
            # verify=False is needed for some shitty interception proxys.
            # Should be fine without it on Home connections
            data = requests.get(
                req_str,
                headers={"Content-Type": "application/xml; charset=UTF-8"},
                verify=False,
            )
            json_data = json.dumps(xmltodict.parse(data.text))
            # print(pp.pprint(json.loads(json_data)["response"]))
            system_demand = json.loads(json_data)["response"]

            time_graph = []
            gen_graph = []
            for each in system_demand["responseBody"]["responseList"]["item"]:
                # print(each["fuelTypeGeneration"]) #debugging
                # print(each["publishingPeriodCommencingTime"]) #debugging
                time_graph.append(
                    datetime.strftime(
                        ceil_dt(
                            datetime.strptime(
                                each["publishingPeriodCommencingTime"], "%H:%M:%S"
                            ),
                            timedelta(minutes=15),
                        ),
                        "%H:%M",
                    )
                )
                gen_graph.append(float(each["fuelTypeGeneration"]))
                ys.append(float(each["fuelTypeGeneration"]))
                # print("#########") #debugging

            # plt.plot(time_graph, gen_graph, '--', label=str(today.strftime("%A %Y-%m-%d"))) #debugging
            # plt.plot(time_graph, gen_graph, '--',
            # label=str(today.strftime("%A %Y-%m-%d"))) #debugging
            z_scores.extend(stats.zscore(gen_graph, ddof=1))
            plt.plot(
                time_graph,
                stats.zscore(gen_graph, ddof=1),
                "--",
                label=str(today.strftime("%A %Y-%m-%d")),
            )  # debugging
            # peaks, _ = find_peaks(gen_graph)
            # peaks = [gen_graph[b] for b in peaks]
            # print(peaks)
            # plt.plot(
            # time_graph,
            # gen_graph,
            # '--',
            # label=str(
            # today.strftime("%A %Y-%m-%d")))

            ###############################################################
            # xi = range(0,len(gen_graph))
            # slope, intercept, r_value, p_value, std_err = stats.linregress(xi,gen_graph)
            # print (stats.linregress(xi,gen_graph))
            # line = slope*xi+intercept
            # plt.plot(xi,line,xi,gen_graph)
            ###############################################################

        # plt.yticks(np.arange(min(ys), max(ys), step=500))
        # # plt.axhline(y=min(ys), color='r', linestyle='--')
        # # plt.axhline(y=max(ys), color='b', linestyle='--')
        ##############################################################
        plt.axhline(y=min(z_scores), color="r", linestyle="--")
        plt.axhline(y=max(z_scores), color="b", linestyle="--")
        plt.axhline(y=np.median(z_scores), color="b", linestyle="--")
        plt.xticks(rotation=90, fontsize=12)
        plt.legend(loc="upper left")
        plt.grid()
        plt.show()
        today = datetime.now()
        # print ("[+]debug, mean of z_scores..." + str(np.median(z_scores)))
        # print ("[+]debug, mean of z_scores..." + str(np.median(z_scores)))
        # print ("[+]debug, mean of z_scores..." + str(np.median(z_scores)))
        if float(current_z_score) > float(np.median(z_scores)):
            print(
                Fore.RED
                + "[+]debug, energy use high for an average "
                + today.strftime("%A")
                + ",Last Checked @ "
                + today.strftime("%H:%M:%S")
            )
        else:
            print(
                Fore.GREEN
                + "[+]debug, energy use low/OK for a "
                + today.strftime("%A")
                + ",Last Checked @ "
                + today.strftime("%H:%M:%S")
            )

        time.sleep(60)
