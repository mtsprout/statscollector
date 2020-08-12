#!/usr/bin/env python

import boto3
import commands
import uuid

# Global variables 
ec2 = boto3.resource('ec2')
ami = 'ami-0bbe28eb2173f6167'
default_instance_type = 't2.micro'
deploymentUUID = str(uuid.uuid1())
keyFileName = deploymentUUID + '.pem'

def create_keypair():
    keyfile    = open(keyFileName,'w')
    keypair    = ec2.create_key_pair(KeyName=deploymentUUID)
    KeyPairOut = keypair.key_material
    keyfile.write(KeyPairOut)
    chmod = commands.getoutput("chmod 400 " + keyFileName + ".pem")
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
        KeyName = deploymentUUID,
        MinCount = 1,
        MaxCount = 1,
        SecurityGroups=[
            'SSH Only'
        ]
    )

if __name__ == "__main__":
    create_keypair()
    create_instance()
