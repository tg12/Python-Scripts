from scipy import stats
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from collections import defaultdict
import boto3
import sys
import datetime
from datetime import datetime, timedelta
import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# If you are using an intercepton proxy (you trust), You'll understand the
# need for this!
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 30 days, per day (30, 86400)
DAYS_BACK_PERIOD = 365
INTERVAL_PERIOD = 86400  # in seconds, 3600 (seconds). Hour. 86400. day

# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/viewing_metrics_with_cloudwatch.html
# Other metrics available


def get_cpu_util(instanceID, startTime, endTime):

    client = boto3.client('cloudwatch', verify=False)
    response = client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instanceID
            },
        ],

        StartTime=startTime,
        EndTime=endTime,
        Period=INTERVAL_PERIOD,
        Statistics=[
            'Average',
        ],
        Unit='Percent'
    )

    return response.items()
    # for k, v in response.items():
    # if k == 'Datapoints':
    # for y in v:
    # return "{0:.2f}".format(y['Average'])


aws_ec2_ids = []
# verify=False is needed for Proxys, Interception breaks things!
ec2 = boto3.resource('ec2', verify=False)

# Get information for all running instances
running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

ec2info = defaultdict()
for instance in running_instances:
    tmp_lst = []
    tmp_lst.append(str(instance.id))
    for tag in instance.tags:
        if 'Name' in tag['Key']:
            tmp_lst.append(str(tag['Value']))
    aws_ec2_ids.append(tmp_lst)

endTime = datetime.fromisoformat(str(datetime.now()))
startTime = datetime.fromisoformat(
    str(datetime.now() - timedelta(days=DAYS_BACK_PERIOD)))

# print (type(endTime)) #debugging
# print (type(startTime)) #debugging
# print (endTime) #debugging
# print (startTime) #debugging

# Create CloudWatch client
cloudwatch = boto3.client('cloudwatch', verify=False)

# List metrics through the pagination interface
# paginator = cloudwatch.get_paginator('list_metrics')
# for response in paginator.paginate(Dimensions=[{'Name': 'LogGroupName'}],
# MetricName='IncomingLogEvents',
# Namespace='AWS/Logs'):
# print(response['Metrics'])

coords = []
objects = []
performance = []

# Sort by Tag name, YOU MUST HAVE YOUR TAGS IN ORDER!! Name - ServerNameHere
aws_ec2_ids.sort(key=lambda x: x[1])
# YOU MUST HAVE YOUR TAGS IN ORDER!! Name - ServerNameHere
# YOU MUST HAVE YOUR TAGS IN ORDER!! Name - ServerNameHere
# YOU MUST HAVE YOUR TAGS IN ORDER!! Name - ServerNameHere

with PdfPages('AWS_EC2_CPU_Report.pdf') as pdf:
    d = pdf.infodict()
    d['Title'] = 'EC2 CPU Monitoring Report'
    d['Author'] = u'https://github.com/tg12'
    d['Subject'] = 'EC2 CPU Monitoring Report'
    d['Keywords'] = 'EC2 CPU Monitoring Report https://github.com/tg12'
    d['CreationDate'] = datetime.now()
    d['ModDate'] = datetime.now()
    for ec2_inst in aws_ec2_ids:
        try:
            if "Prod" in str(ec2_inst[1]):
                print("[+]debug, ..." + str(ec2_inst[1]))
                objects.append(str(ec2_inst[1]))
                # print(get_cpu_util(ec2_inst[0],startTime,endTime)) #debugging
                x = []
                y = []
                for k, v in get_cpu_util(ec2_inst[0], startTime, endTime):
                    if k == 'Datapoints':
                        for a in v:
                            # print("{0:.2f}".format(a['Average'])) #debugging
                            # print (datetime.isoformat(a['Timestamp']))
                            # #debugging
                            x.append(datetime.isoformat(a['Timestamp']))
                            y.append(float(a['Average']))
                both_coords = []
                both_coords.append(x)
                both_coords.append(y)
                coords.append(both_coords)
                fig1 = plt.figure(figsize=(15, 7))
                # ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO)) #This doesnt work with Hi Res Dates/Times. No idea why!
                # ax.xaxis.set_major_formatter(mdates.DateFormatter('%a %d\n%b
                # %Y')) #This doesnt work with Hi Res Dates/Times. No idea why!
                plt.plot(x, y, '-')
                xi = range(len(y))
                res = stats.theilslopes(y, xi)
                plt.plot(xi, res[1] + res[0] * xi, '--',
                         label=str("Avg CPU: " + str(round(res[1], 2))))
                plt.plot(xi, res[1] + res[2] * xi, '--')
                plt.plot(xi, res[1] + res[3] * xi, '--')
                plt.yticks(np.arange(0, 100, step=3))
                plt.xticks(rotation=90, fontsize=4)
                plt.legend(loc='upper left')
                plt.title(str(ec2_inst[1]) + " - " + str(ec2_inst[0]))
                pdf.savefig(fig1)
                # time to write buffers etc, probably not needed!
                time.sleep(1)
                # plt.show() #debugging
                plt.close()
                performance.append(np.average(y))
                print("##############")
        except BaseException:
            pass

# print(len(objects)) #debugging
# print(len(performance)) #debugging

y_pos = np.arange(len(objects))
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.yticks(np.arange(0, 100, step=5))
plt.xticks(y_pos, objects)
plt.xticks(rotation=90)
plt.ylabel('CPU')
plt.title('Instance')
plt.show()
