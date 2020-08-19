#!/usr/bin/env python

import boto3
import commands
import uuid
import argparse
from os import path

# Global variables 
ec2 = boto3.resource('ec2')
sg  = boto3.client('ec2')
ami = 'ami-0bbe28eb2173f6167'
deploymentUUID = str(uuid.uuid1())
keyFileName = deploymentUUID + ".pem"
influxDBport = 8086

parser = argparse.ArgumentParser()
parser.add_argument('filename', help="Enter path to deployment file.  It should be in .csv format with <hostname>,<ip>.")
parser.add_argument("--size", help="Enter size of AWS instance to use.  The default is t2.micro.", choices=['t2.nano', 't2.micro','t2.small','t2.medium','t2.large','t2.xlarge','t2.2xlarge'], default='t2.micro')
args = parser.parse_args()
filename = args.filename
instance_size = args.size

def parse_deployment_file(deployfile):
    """Parse the specified deployment file and make separate lists for hosts and IPs."""
    deployHosts = []
    deployIPs   = []
    if (path.exists(deployfile)):
        deployfile = open(deployfile, 'r')
        entries = deployfile.readlines()
        for entry in entries:
            hostinfo = entry.split(",")
            deployHosts.append(hostinfo[0])
            deployIPs.append(hostinfo[1].rstrip("\n"))
        return deployHosts, deployIPs
    else:
        exit(deployfile + " does not exist.")
        
def create_security_group(deployIPs):
    """Create security group with IPs from deployment file."""
    secgroup = ec2.create_security_group(
        Description = 'Security group for Deployment ' + deploymentUUID,
        GroupName = deploymentUUID
        )
    secgroupId = secgroup.group_id

    
    for address in deployIPs:
        rules = sg.authorize_security_group_ingress(
            GroupId = secgroupId,
            IpPermissions = [
                {'IpProtocol' : 'TCP',
                 'FromPort' : influxDBport,
                 'ToPort'   : influxDBport,
                 'IpRanges' : [ {'CidrIp' : address } ]
                }
            ]
        )
    return secgroupId

def create_keypair():
    keyfile    = open(keyFileName,'w')
    keypair    = ec2.create_key_pair(KeyName=deploymentUUID)
    KeyPairOut = keypair.key_material
    keyfile.write(KeyPairOut)
    chmod = commands.getoutput("chmod 400 " + keyFileName)
    keyfile.close()

def create_instance(secGroup):
    userDataFile = open('files/user-data', 'r')
    userDataList = list(userDataFile)
    userDataString = "".join(userDataList)
    instance = ec2.create_instances(
        BlockDeviceMappings=[
            {
                 'DeviceName': '/dev/sda1',
                 'VirtualName' : 'Root Partition',
                 'Ebs' : {
                     'VolumeSize' : 20,
                     'VolumeType' : 'standard'
                  },
             }
        ],
        ImageId = ami,
        InstanceType = instance_size,
        UserData=userDataString,
        KeyName = deploymentUUID,
        MinCount = 1,
        MaxCount = 1,
        SecurityGroupIds=[
            'sg-08129536e9da5d891',
            secGroup,
        ]
    )

if __name__ == "__main__":
    hostIPs = parse_deployment_file(filename)
    securityGroup = create_security_group(hostIPs[1])
    create_keypair()
    create_instance(securityGroup)
