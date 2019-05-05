import boto3

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.core.greengrass.discovery.providers import DiscoveryInfoProvider
from AWSIoTPythonSDK.exception.AWSIoTExceptions import DiscoveryInvalidRequestException

import logging
import time
import uuid
import os
import string
import argparse

CERTFOLDER = "./certs/"
GROUPCERTFOLDER = "./groupCerts/"

# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--rootCA", action="store", dest="rootCAPath", default=CERTFOLDER + "AmazonRootCA1.pem", help="Root CA file path, default is " + CERTFOLDER + "AmazonRootCA1.pem")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", default=CERTFOLDER + "cert.pem", help="Certificate file path, default is " + CERTFOLDER + "cert.pem")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", default=CERTFOLDER + "private.key", help="Private key file path, default is " + CERTFOLDER + "private.key")
parser.add_argument("-n", "--thingName", action="store", dest="thingName", default="ggcLocalDevice", help="GreenGrass group thing name, default is ggcLocalDevice")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="hello/world", help="Targeted topic, default is hello/world")

args = parser.parse_args()
rootCAPath = args.rootCAPath
privateKeyPath = args.privateKeyPath
certificatePath = args.certificatePath
topic = args.topic
thingName = args.thingName
clientid = args.thingName

# # Custom MQTT message callback
def subscribeCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

def configureLogger():
    # Configure logging
    global logger
    logger = logging.getLogger("AWSIoTPythonSDK.core")
    logger.setLevel(logging.INFO)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

def getIotCoreEndpoint():
    global iotEndpoint
    client = boto3.client('iot',region_name='us-west-2')
    iotEndpoint = client.describe_endpoint(
        endpointType='iot:Data-ATS'
    ).get("endpointAddress")

def GreenGrassConnect():
    discoveryInfoProvider = DiscoveryInfoProvider()
    discoveryInfoProvider.configureEndpoint(iotEndpoint)
    discoveryInfoProvider.configureCredentials(rootCAPath, certificatePath, privateKeyPath)
    discoveryInfoProvider.configureTimeout(10)  # 10 sec
    try:
        discoveryInfo = discoveryInfoProvider.discover(thingName)
        caList = discoveryInfo.getAllCas()
        coreList = discoveryInfo.getAllCores()

        # We only pick the first ca and core info
        groupId, ca = caList[0]
        coreInfo = coreList[0]
        logger.debug("Discovered GGC: %s from Group: %s" % (coreInfo.coreThingArn, groupId))        
        logger.debug("Saving GGC certificate...")
        groupCA = GROUPCERTFOLDER + groupId + "_CA_" + str(uuid.uuid4()) + ".crt"
        if not os.path.exists(GROUPCERTFOLDER):
            os.makedirs(GROUPCERTFOLDER)
        groupCAFile = open(groupCA, "w")
        groupCAFile.write(ca)
        groupCAFile.close()
        logger.debug("Done saving GGC certificate")

        for connectivityInfo in coreInfo.connectivityInfoList:
            currentHost = connectivityInfo.host 
            currentPort = connectivityInfo.port
            logger.debug("currentHost: %s, currentPort: %s", currentHost, currentPort)
            try:
                iotClient = awsIotClientConnect(currentHost, currentPort, groupCA)
                connected = True
                logger.info("Connected to host %s:%s", currentHost, currentPort)
                break
            except BaseException as e:
                logger.error("Error connecting to host %s:%s", currentHost, currentPort)
                logger.error("Error message: %s" % e.message)            

    except DiscoveryInvalidRequestException as e:
        logger.error("Error GG discovery: %s", e)


def awsIotClientConnect(iotEndpoint, port, caPath):
    logger.info("connecting to %s:%s", iotEndpoint, port)

    iotClient = AWSIoTMQTTClient(clientid)
    # iotClient.onMessage = subscribeCallback

    logger.info("Connecting with caPath: %s, private: %s, certPath: %s", caPath, privateKeyPath, certificatePath)

    iotClient.configureCredentials(caPath, privateKeyPath, certificatePath)
    iotClient.configureEndpoint(iotEndpoint, port)

    iotClient.connect()
    iotClient.subscribe(topic, 0, subscribeCallback)
    return iotClient

configureLogger()
getIotCoreEndpoint()
GreenGrassConnect()

# uncomment to connect to AWS IoT Core
# awsIotClientConnect(iotEndpoint, 8883, rootCAPath)

while True:
    time.sleep(1)