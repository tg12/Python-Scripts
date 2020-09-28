# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND
# NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE
# DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY,
# WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Dont forget to tip your server!
# Bitcoin Cash (BCH)   qpz32c4lg7x7lnk9jg6qg7s4uavdce89myax5v5nuk
# Ether (ETH) -        0x843d3DEC2A4705BD4f45F674F641cE2D0022c9FB
# Litecoin (LTC) -     Lfk5y4F7KZa9oRxpazETwjQnHszEPvqPvu
# Bitcoin (BTC) -      34L8qWiQyKr8k4TnHDacfjbaSqQASbBtTd

from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import datetime
import boto3
from tabulate import tabulate
import numpy as np
import pprint
import json
import matplotlib.pyplot as plt

plt.rcdefaults()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
pp = pprint.PrettyPrinter(indent=4)

ssm = boto3.client("ssm", verify=False)


class Regions:
    @classmethod
    def get_regions(cls):
        short_codes = cls._get_region_short_codes()

        regions = [
            {"name": cls._get_region_long_name(sc), "code": sc} for sc in short_codes
        ]

        regions_sorted = sorted(regions, key=lambda k: k["name"])

        return regions_sorted

    @classmethod
    def _get_region_long_name(cls, short_code):
        param_name = (
            "/aws/service/global-infrastructure/regions/" f"{short_code}/longName"
        )
        response = ssm.get_parameters(Names=[param_name])
        return response["Parameters"][0]["Value"]

    @classmethod
    def _get_region_short_codes(cls):
        output = set()
        for page in ssm.get_paginator("get_parameters_by_path").paginate(
            Path="/aws/service/global-infrastructure/regions"
        ):
            output.update(p["Value"] for p in page["Parameters"])

        return output


pricing_client = boto3.client("pricing", region_name="us-east-1", verify=False)
ondem_price = 0


def nested_dict_print(d):
    for k, v in d.items():
        if isinstance(v, dict):
            nested_dict_print(v)
        else:
            # if str(k) == "description": #debugging
            # print("{0} : {1}".format(k, v)) #debugging
            if str(k) == "USD":
                # hack, you figure out why! the price data is buried that far
                # in the dictionary(s) this is a reasonable hack!
                global ondem_price
                ondem_price = float(v)


def get_products(region_code, region, inst_type):
    paginator = pricing_client.get_paginator("get_products")
    tmp_lst = []

    response_iterator = paginator.paginate(
        ServiceCode="AmazonEC2",
        Filters=[
            {"Type": "TERM_MATCH", "Field": "location", "Value": region},
            {"Type": "TERM_MATCH", "Field": "instanceType", "Value": inst_type},
            {"Type": "TERM_MATCH", "Field": "capacitystatus", "Value": "Used"},
            {"Type": "TERM_MATCH", "Field": "tenancy", "Value": "Shared"},
            {"Type": "TERM_MATCH", "Field": "preInstalledSw", "Value": "NA"},
            {"Type": "TERM_MATCH", "Field": "operatingSystem", "Value": "Windows"},
        ],
        PaginationConfig={"PageSize": 100},
    )

    products = []
    for response in response_iterator:
        for priceItem in response["PriceList"]:
            # pp.pprint(json.loads(priceItem)) #debugging
            priceItemJson = json.loads(priceItem)
            # pp.pprint(priceItemJson["terms"]["OnDemand"]) #debugging
            price_dict = priceItemJson["terms"]["OnDemand"]
            tmp_lst.append(region_code)
            tmp_lst.append(inst_type)
            # bit hacky, set's a global variable. Should tidy it up later.
            nested_dict_print(price_dict)
            tmp_lst.append(ondem_price)
            # products.append(priceItemJson) #debugging

    if len(tmp_lst) > 0:
        return tmp_lst  # region,inst type,on demand price (list)


aws_ec2_types = []
ec2 = boto3.resource("ec2", verify=False)

# Get information for all running instances
running_instances = ec2.instances.filter(
    Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
)

for instance in running_instances:
    # print (instance.instance_type)
    aws_ec2_types.append(instance.instance_type)

aws_ec2_types = list(set(aws_ec2_types))

# client = boto3.client('ec2', verify=False)
# regions = [x["RegionName"] for x in client.describe_regions()["Regions"]]
# debugging
# prefixes = ('eu')
# regions = [x for x in regions if x.startswith(
# prefixes)]  # only check out eu regions

for type in aws_ec2_types:

    print("Instance: %s" % type)  # console debugging
    lst_data = []
    for region in Regions.get_regions():
        try:
            # if "eu" in str(region["code"]): #eu,us,etc etc #optional
            tmp_lst = []
            tmp_lst = get_products(region["code"], region["name"], type)
            if len(tmp_lst) == 3:  # region, type, price
                lst_data.append(tmp_lst)
        except Exception as e:
            # print("[+]debug, error..." + str(e)) #debugging
            print(
                "[+]debug, error...check this instance type is available in this region, or connection error etc"
            )
            continue

    print(lst_data)
    lst_data = sorted(lst_data, key=lambda x: x[2])
    print("###############")  # console debugging
    print("###############")  # console debugging
    print("###############")  # console debugging
    print("###############")  # console debugging
    instance_type_data = []
    price_data = []

    for i in range(len(lst_data)):
        string_result = str(lst_data[i][0] + "/" + lst_data[i][1])
        instance_type_data.append(string_result)
        price_data.append(float(lst_data[i][2]))

    y_pos = np.arange(len(instance_type_data))
    bars = plt.bar(y_pos, price_data, align="center", alpha=0.5, width=0.4)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x(), yval + 0.005, yval)
    plt.yticks(np.arange(np.min(price_data), np.max(price_data), step=0.1))
    plt.xticks(y_pos, instance_type_data, rotation=45, fontsize=8)
    plt.grid(True)
    plt.ylabel("Price Per Hour (On Demand)")
    plt.title("On Demand/Instance Hour")
    plt.show()
