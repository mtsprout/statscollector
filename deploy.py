#!/usr/bin/env python

import boto3
import commands

# Global variables 
ec2 = boto3.resource('ec2')
ami = 'ami-0bbe28eb2173f6167'
default_instance_type = 't2.micro'

def create_keypair():
    keyfile    = open('ec2-keypair.pem','w')
    keypair    = ec2.create_key_pair(KeyName='ec2-keypair')
    KeyPairOut = keypair.key_material
    keyfile.write(KeyPairOut)
    chmod = commands.getoutput("chmod 400 ec2-keypair.pem")
    keyfile.close()

def create_instance():
    userDataFile = open('files/user-data', 'r')
    userDataList = list(userDataFile)
    userDataString = "".join(userDataList)
    instance = ec2.create_instances(
        BlockDeviceMappings=[
            {
                 'DeviceName': '/dev/xvda',
                 'VirtualName' : 'Root Partition',
                 'Ebs' : {
                     'VolumeSize' : 20,
                     'VolumeType' : 'standard'
                  },
             }
        ],
        ImageId = ami,
        InstanceType = default_instance_type,
        UserData=userDataString,
        KeyName = 'ec2-keypair',
        MinCount = 1,
        MaxCount = 1,
        SecurityGroups=[
            'SSH Only'
        ]
    )

if __name__ == "__main__":
    create_keypair()
    create_instance()
