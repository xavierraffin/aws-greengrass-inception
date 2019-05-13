# ML@Edge with AWS GreenGrass Core

ML@Edge Image Classifications example using MXNet pretrained model with GreenGrass Core running on a Rasperry Pi


## Description

This is an example of running Lambda on GreenGrass with MXNet pretrained model Inception v3 for image classification

Details on Inception v3 can be found in https://arxiv.org/abs/1512.00567

## Prerequisite

* Raspberry Pi 3 Model B+ set up and configured for use with AWS IoT Greengrass
* Raspberry Pi Camera Module V2 - 8 Megapixel, 1080p

(Details in https://docs.aws.amazon.com/greengrass/latest/developerguide/ml-console.html#ml-inference-prerequisites)

## Configure Raspberry Pi with the WiFi credential

1. Create a plain text file `wpa_supplicant.conf` in the root of the sd card with contents
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=«your_ISO-3166-1_two-letter_country_code, e.g. CA»

network={
    ssid="«your_SSID»"
    psk="«your_PSK»"
    key_mgmt=WPA-PSK
}
```

## Setup and installation of Greengrass software

### Create a Greengrass group 
1. Goto https://console.aws.amazon.com/iot/home?#/greengrass/grouphub
2. Select `Create Group`
3. Select `Use easy creation`
4. Enter a Group Name, such as `local_image-greengrass-group`, and select `Next`
5. In the next page, accept the default core name `local_image-greengrass-group_Core`, and select `Next`
6. In the screen `Run a scripted easy Group creation`, select `Create Group and Core`
7. In the screen `Connect your Core device`, choose `Download these resources as a tar.gz`
8. Choose `Choose a root CA`,  download the root CA `RSA 2048 bit key: Amazon Root CA 1`
9. We will be installing the Greengrass Core software using Snap so we can skip that step and choose `Finish`

### Setting up GreenGrass on Raspberry Pi
1. From your local computer, copy the resources downloaded in [Setting up Greengrass group and core](#Setting-up-Greengrass-group-and-core) to the Raspberry Pi, e.g. `$ scp <uid>-setup.tar.gz pi@<raspberry pi>:~/` and `$ scp AmazonRootCA1.pem pi@<raspberry pi>:~/`
2. SSH into the Raspberry Pi, follow the steps in https://docs.aws.amazon.com/greengrass/latest/developerguide/module1.html#setup-filter.rpi to prepare the Raspberry Pi for GreenGrass
3. Follow the steps in https://docs.aws.amazon.com/greengrass/latest/developerguide/what-is-gg.html#gg-downloads to install the GreenGrass core software
12. Copy the certificates and config of the Greengrass core into the greengrass folder `$ sudo tar zxvf <uid>-setup.tar.gz -C /greengrass/ && sudo cp ~/AmazonRootCA1.pem /greengrass/certs/root.ca.pem`
13. Making sure the resources are in the correct folders, e.g. `$ ls /greengrass/certs/` and you should see your cert, private key, public key and Amazon CA certs in the folder
14. Starts the Greengrass software `$ sudo /greengrass/ggc/core/greengrassd start` 
15. If the configuration is in place, you should see the GreenGrass core running message, such as
```
$ sudo /greengrass/ggc/core/greengrassd start
Setting up greengrass daemon
Validating hardlink/softlink protection
Waiting for up to 1m10s for Daemon to start

Greengrass successfully started with PID: <PID>
```
16. You should also be able to see that the GreenGrass Core software successfully subscribed to the GreenGrass MQTT Topics
```
$ sudo tail /greengrass/ggc/var/log/system/runtime.log 
[2019-05-10T11:01:02.078-07:00][DEBUG]-Entering OnConnect.	{"clientId": "local_image-greengrass-group_Core"}
[2019-05-10T11:01:02.078-07:00][INFO]-MQTT connection connected. Start subscribing.	{"clientId": "local_image-greengrass-group_Core"}
[2019-05-10T11:01:02.078-07:00][INFO]-Deployment agent connected to cloud.
[2019-05-10T11:01:02.078-07:00][DEBUG]-Subscribe retry configuration.	{"IntervalInSeconds": 60}
[2019-05-10T11:01:02.078-07:00][INFO]-Start subscribing.	{"numOfTopics": 2, "clientId": "local_image-greengrass-group_Core"}
[2019-05-10T11:01:02.079-07:00][INFO]-Trying to subscribe to topic $aws/things/local_image-greengrass-group_Core-gda/shadow/update/delta
[2019-05-10T11:01:02.194-07:00][DEBUG]-Subscribed to topic.	{"topic": "$aws/things/local_image-greengrass-group_Core-gda/shadow/update/delta"}
[2019-05-10T11:01:02.194-07:00][INFO]-Trying to subscribe to topic $aws/things/local_image-greengrass-group_Core-gda/shadow/get/accepted
[2019-05-10T11:01:02.309-07:00][DEBUG]-Subscribed to topic.	{"topic": "$aws/things/local_image-greengrass-group_Core-gda/shadow/get/accepted"}
[2019-05-10T11:01:02.417-07:00][INFO]-All topics subscribed.	{"clientId": "local_image-greengrass-group_Core"}
```

## Setup of image classification software

### Adding Lambda functions and resources to the GreenGrass

#### Create the long-running Lambda function

Create a Lambda function and upload this repository as a zip file

1. Goto https://console.aws.amazon.com/lambda/home
2. Choose `Author from scratch`
2. Function name: `greengrassImageClassification`
3. Runtime: `Python 2.7`
4. Execution role: Create a new role from AWS policy templates
5. Role name: `greenGrassLambdaRole`
5. Choose `Basic Lambda@Edge permissions` from the Policy templates
6. Choose `Create function`
7. In the Function code, upload this repository as a zip file. You need these 2 files `greengrass_main.py`, `load_model.py` and the folder `greengrasssdk/` in the zip file
8. Lambda Handler: `greengrass_main.function_handler`
9. Choose `Save`
10. From the `Actions`, choose `Publish new version`
11. From the `Version: 1`, choose `1` in the `Versions`
12. From the `Actions`, choose `Create alias`
13. Enter a name for the version alias, such as `mlRpi`, and choose `1` in the Version

#### Associate the Lambda to GreenGrass group
1. Goto https://console.aws.amazon.com/iot/home?#/greengrass/grouphub
2. Choose the relevant GreenGrass group 
3. From the menu in the left hand side, select `Lambdas`, `Add Lambda`
4. In the `Add a Lambda to your Greengrass Group`, choose `Use existing Lambda`
5. Choose `greengrassImageClassification`, choose `Next`
6. In the `Select a Lambda version`, choose the Alias, such as `Alias: mlRpi`

#### Update Lambda function Settings
1. Goto https://console.aws.amazon.com/iot/home?#/greengrass/grouphub
2. Choose the relevant GreenGrass group 
3. From the menu in the left hand side, select `Lambdas`, choose the Lambda `greengrassImageClassification`
4. Choose `Edit`
  * Memory limit: 96 MB
  * Timeout: 15 Seconds
  * Lambda lifecycle: Make this function long-lived and keep it running indefinitely
  * Environment variables
     * MXNET_ENGINE_TYPE: NaiveEngine

#### PiCamera device as Local Resources

1. Goto https://console.aws.amazon.com/iot/home?#/greengrass/grouphub
2. Choose the relevant GreenGrass group 
3. From the menu in the left hand side, select `Resources`
4. In the Local, select `Add Local`
5. Create a local resource with the following parameters:
  - Resource name: videoCoreSharedMemory
  - Resource type: Device
  - Device path: /dev/vcsm
  - Group owner file access permission: Automatically add OS group permissions of the Linux group that owns the resource
  - Lambda function affiliations: greengrassObjectClassification
  - Specify the permission this Lambda will have to the resource.: Read and write access
6. Create another local resource with the following parameters:
  - Resource name: videoCoreInterface
  - Resource type: Device
  - Device path: /dev/vchiq
  - Group owner file access permission: Automatically add OS group permissions of the Linux group that owns the resource
  - Lambda function affiliations: greengrassObjectClassification
  - Specify the permission this Lambda will have to the resource.: Read and write access

#### Machine Learning Resource

1. In your local computer, download http://data.mxnet.io/models/imagenet/inception-bn/Inception-BN-symbol.json and http://data.mxnet.io/mxnet/models/imagenet/synset.txt
2. Download http://data.mxnet.io/models/imagenet/inception-bn/Inception-BN-0126.params and rename to Inception-BN-0000.params
3. zip these 3 files as `inception_bn.zip`
1. Goto https://console.aws.amazon.com/iot/home?#/greengrass/grouphub
2. Choose the relevant GreenGrass group 
3. From the menu in the left hand side, select `Resources`
4. In the Local, select `Add Machine Learning`
5. Select `Add machine learning resource`
6. Create a machine learning resource with the following parameters:
  - Resource name: Inception
  - Model source: Upload a model in S3 (including models optimized through Deep Learning Compiler). **Make sure you have the word `greengrass` in your bucket name**
  - Model from S3: (Upload the  inception_bn.zip)
  - Local path: /greengrass-machine-learning/mxnet/inception_bn
  - Lambda function affiliations:greengrassObjectClassification
  - Specify the permission this Lambda will have to the resource.: Read-only access

#### Assume-role for the GreenGrass core
1. Goto https://console.aws.amazon.com/iot/home?#/greengrass/grouphub
2. Choose the relevant GreenGrass group 
3. From the menu in the left hand side, select `Settings`
4. In the `Group role`, choose `Add role`, choose an IAM role that allows principal `greengrass.amazonaws.com` to assume, such as `Greengrass_ServiceRole`
   1. If you are creating a new IAM role for GreenGrass, make sure you have these 2 managed policies to the GreenGrass Service Role: `CloudWatchLogsFullAccess` and `AWSGreengrassResourceAccessRolePolicy`

#### Deploy the GreenGrass configuration to the Raspberry Pi

1. Goto https://console.aws.amazon.com/iot/home?#/greengrass/grouphub
3. From the `Actions` drop down list, select `Deploy`
  4. If this is your first deployment, in `Configure how Devices discover your Core`, choose `Automatic Detection`
  1. In `Grant permission to access other services`, choose `Grant permission`
4. You can monitor the logs locally `sudo tail -F /greengrass/ggc/var/log/system/runtime.log`

### Subscribe to the prediction message using the AWS IoT Core MQTT Test client
4. Goto https://console.aws.amazon.com/iot/home?#/test
5. In the `Subscription topic`, enter `hello/world`
6. If all configuration is correct, an MQTT message with topic "hello/world' should be seen in the AWS IoT Test client, such as 

```
New Prediction: [(0.18657419, 'n02676566 acoustic guitar'), (0.14744462, 'n03929660 pick, plectrum, plectron'), (0.1250492, 'n02787622 banjo'), (0.049499936, 'n03271574 electric fan, blower'), (0.038708802, 'n03476684 hair slide')]
```

### Deploy new version of Lambda to GreenGrass

Should you need to deploy a new version of Lambda function, you need to update the alias to the version using command `aws lambda update-alias --function-name greengrassImageClassification --name mlRpi --function-version 2`

If successfully updated, you should see the response
```
{
    "FunctionVersion": "2",
    "AliasArn": "arn:aws:lambda:us-east-1:159000643575:function:greengrassImageClassification:mlRpi",
    "Name": "mlRpi",
    "Description": ""
}
```

Now that the alias `mlRpi` is pointing to the version, you can proceed to deploy the GreenGrass

### To run the image classification locally in Rapsberry Pi

1. Git clone or download this repository to the Raspberry Pi
2. Install the python 2.7 dependencies `sudo apt-get install -y python-dev python-setuptools python-pip python-picamera`
3. We are still using python 2.7, so we have to install the opencv python library using `sudo apt-get install python-opencv`
4. Install the MXNet Dependencies following the steps in https://docs.aws.amazon.com/greengrass/latest/developerguide/ml-console.html#install-mxnet#install-mxnet
2. Runs the local main python file

```
$ python2.7 local_main.py
```

If configuration is proper, a prediction should be shown, such as

```
[(0.18657419, 'n02676566 acoustic guitar'), (0.14744462, 'n03929660 pick, plectrum, plectron'), (0.1250492, 'n02787622 banjo'), (0.049499936, 'n03271574 electric fan, blower'), (0.038708802, 'n03476684 hair slide')]
```

#### To view the camera preview

* Option 1: Connect the Raspberry Pi to a HDMI display
* Option 2: Install a VNC server on the Raspberry Pi

For Option 2, a display manager is required for the VNC server. lxsession is one of the lightweight display manager.

Steps:
1. `sudo apt-get install realvnc-vnc-server realvnc-vnc-viewer lxsession`
2. `sudo raspi-config`, goes to `Interfacing Options`->`VNC`->`Yes`

However, PiCamera display the image in native renderer, therefore, `direct capture mode` of the RealVNC need to be enabled in order to view the image over VNC

1. From the VNC windows, click on the VNC Connect icon at the lower right
2. From the top right of the VNC Connect windows, click on the expanded menu -> options
3. In the `Troubleshooting`, check on the `Enable direct capture mode`


## GGAD simulation

In this section, we will simulate a local GGAD (Greengrass Aware Devices) that subscribe to the prediction messages from the Lambda running on the GGC, and simulate the local inference when there is no internet connectivity.

### Local subscriber

These steps is to demonstrate the offline capability of ML@Edge of the AWS GreenGrass. You can run the script in the local computer that is in the same network as the Raspberry Pi, to simulate a local device that connects to the GreenGrass core locally.

### Create an IoT Device and add to the GreenGrass Group
1. Goto the correct region of https://console.aws.amazon.com/iot
2. From the left hand side of menu, choose `GreenGrass` -> `Groups`, the correct GreenGrass Group, `Devices`->`Add Device`
3. In the `Add a Device`, choose `Create New Device`, enter a thing name, such as `ggcLocalDevice`
4. In the `Set up security`, choose `Use Defaults` 1-Click
5. Download the certificates into a local folder, such as `<THIS REPOSITORY>/localSubscriber/certs`.
6. Rename the certificate file `<device id>.cert.pem` as  `cert.pem`
7. Rename the certificate file `<device id>.private.key` as  `private.key`
8. Download the RSA 2048 bit key root CA certificate from https://docs.aws.amazon.com/iot/latest/developerguide/managing-device-certs.html#server-authentication, and save in the `<THIS REPOSITORY>/localSubscriber/certs`

### Runs the subscriber.py

1. Create a virtualenv, `$ virtualenv local`
2. Source the virtualenv, `$ source local/bin/activate`
3. Pull in all the requirements, `$ pip install -r requirements.txt`
4. Runs the Python file, `$ python2.7 subscriber.py`
5. If it runs successfully, you should see the prediction messages

```
2019-05-05 11:19:46,792 - AWSIoTPythonSDK.core - INFO - connecting to <GreenGrass Core local IP>:8883
2019-05-05 11:19:46,793 - AWSIoTPythonSDK.core.protocol.mqtt_core - INFO - MqttCore initialized
2019-05-05 11:19:46,793 - AWSIoTPythonSDK.core.protocol.mqtt_core - INFO - Client id: ggcLocalDevice
2019-05-05 11:19:46,793 - AWSIoTPythonSDK.core.protocol.mqtt_core - INFO - Protocol version: MQTTv3.1.1
2019-05-05 11:19:46,793 - AWSIoTPythonSDK.core.protocol.mqtt_core - INFO - Authentication type: TLSv1.2 certificate based Mutual Auth.
2019-05-05 11:19:46,793 - AWSIoTPythonSDK.core - INFO - Connecting with caPath: ./groupCerts/<GreenGrassn Group CA Cert>.crt, private: ./certs/private.key, certPath: ./certs/cert.pem
2019-05-05 11:19:46,793 - AWSIoTPythonSDK.core.protocol.mqtt_core - INFO - Configuring certificates...
2019-05-05 11:19:46,793 - AWSIoTPythonSDK.core.protocol.mqtt_core - INFO - Configuring endpoint...
2019-05-05 11:19:46,794 - AWSIoTPythonSDK.core.protocol.mqtt_core - INFO - Performing sync connect...
2019-05-05 11:19:46,794 - AWSIoTPythonSDK.core.protocol.mqtt_core - INFO - Performing async connect...
2019-05-05 11:19:46,794 - AWSIoTPythonSDK.core.protocol.mqtt_core - INFO - Keep-alive: 600.000000 sec
2019-05-05 11:19:47,017 - AWSIoTPythonSDK.core.protocol.mqtt_core - INFO - Performing sync subscribe...
2019-05-05 11:19:47,035 - AWSIoTPythonSDK.core - INFO - Connected to host <GreenGrass Core local IP>:8883
Received a new message: 
New Prediction: [(0.5641716, 'n04099969 rocking chair, rocker'), (0.20946382, 'n03065424 coil, spiral, volute, whorl, helix'), (0.052156523, 'n03271574 electric fan, blower'), (0.023835631, 'n03201208 dining table, board'), (0.017949697, 'n04009552 projector')]
from topic: 
hello/world
--------------
```

### Simulate local-only network

To simulate the offline mode, remove the internet route from the default route in Raspberry Pi

1. Login to the Raspberry Pi
2. Making sure the default route exists
```
# sudo route -v
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         192.168.1.1     0.0.0.0         UG    303    0        0 wlan0
192.168.1.0     0.0.0.0         255.255.255.0   U     303    0        0 wlan0
```
1. If your route table uses default route for local addresses, add a local route
```
# sudo route add -net 192.168.1.0/24 gw 192.168.1.1
```
3. Double check the route
```
# sudo route -v
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         192.168.1.1     0.0.0.0         UG    303    0        0 wlan0
192.168.1.0     192.168.1.1     255.255.255.0   UG    0      0        0 wlan0
192.168.1.0     0.0.0.0         255.255.255.0   U     303    0        0 wlan0
```
4. Check that the internet route is working as expected
```
# ping amazonaws.com
PING aMaZoNaWs.com (207.171.166.22) 56(84) bytes of data.
64 bytes from 166-22.amazon.com (207.171.166.22): icmp_seq=1 ttl=232 time=111 ms
64 bytes from 166-22.amazon.com (207.171.166.22): icmp_seq=2 ttl=232 time=100 ms
64 bytes from 166-22.amazon.com (207.171.166.22): icmp_seq=3 ttl=232 time=99.8 ms
```
5. Remove the default
```
# sudo route del default
```
6. Your route table should now left with local routes
```
# sudo route -v
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
192.168.1.0     192.168.1.1     255.255.255.0   UG    0      0        0 wlan0
192.168.1.0     0.0.0.0         255.255.255.0   U     303    0        0 wlan0
```
7. Internet route should be lost
```
# ping amazonaws.com
connect: Network is unreachable
```
8. However, the local subscriber should still receiving the predictions, e.g.

```
Received a new message: 
New Prediction: [(0.5417486, 'n04099969 rocking chair, rocker'), (0.2136172, 'n03065424 coil, spiral, volute, whorl, helix'), (0.043906394, 'n03271574 electric fan, blower'), (0.02837033, 'n03201208 dining table, board'), (0.023345523, 'n04009552 projector')]
from topic: 
hello/world
--------------
```

## Troubleshooting

* Greengrass Troubleshooting guides https://docs.aws.amazon.com/greengrass/latest/developerguide/gg-troubleshooting.html
* To check Lambda local execution, the logs can be tailed with command `sudo tail -F /greengrass/ggc/var/log/user/<AWS region>/<account id>/greengrassImageClassification.log`. Successful execution should have a log similar to the following
```
[2019-05-10T19:08:06.401-07:00][INFO]-Lambda.py:92,Invoking Lambda function "arn:aws:lambda:::function:GGRouter" with Greengrass Message "New Prediction: [(0.12387366, 'n04372370 switch, electric switch, electrical switch'), (0.063494414, 'n03929660 pick, plectrum, plectron'), (0.058057442, 'n04254120 soap dispenser'), (0.042390004, 'n04153751 screw'), (0.03408207, 'n15075141 toilet tissue, toilet paper, bathroom tissue')]"
[2019-05-10T19:08:06.405-07:00][INFO]-ipc_client.py:142,Posting work for function [arn:aws:lambda:::function:GGRouter] to http://localhost:8000/2016-11-01/functions/arn:aws:lambda:::function:GGRouter
[2019-05-10T19:08:06.723-07:00][INFO]-ipc_client.py:155,Work posted with invocation id [c5467c56-9121-4bd6-6eb6-a937d8d9bdfb]
[2019-05-10T19:08:06.728-07:00][INFO]-lambda_runtime.py:114,Running [arn:aws:lambda:us-east-1:159000643575:function:greengrassImageClassification:3]
[2019-05-10T19:08:06.73-07:00][INFO]-ipc_client.py:170,Getting work for function [arn:aws:lambda:us-east-1:159000643575:function:greengrassImageClassification:3] from http://localhost:8000/2016-11-01/functions/arn:aws:lambda:us-east-1:159000643575:function:greengrassImageClassification:3/work
[2019-05-10T19:08:15.31-07:00][INFO]-[(0.1262314, 'n04372370 switch, electric switch, electrical switch'), (0.06892826, 'n03929660 pick, plectrum, plectron'), (0.05506966, 'n04254120 soap dispenser'), (0.044870526, 'n04153751 screw'), (0.033377603, 'n15075141 toilet tissue, toilet paper, bathroom tissue')]
[2019-05-10T19:08:15.311-07:00][INFO]-IoTDataPlane.py:115,Publishing message on topic "hello/world" with Payload "New Prediction: [(0.1262314, 'n04372370 switch, electric switch, electrical switch'), (0.06892826, 'n03929660 pick, plectrum, plectron'), (0.05506966, 'n04254120 soap dispenser'), (0.044870526, 'n04153751 screw'), (0.033377603, 'n15075141 toilet tissue, toilet paper, bathroom tissue')]"
```

## References
  * https://github.com/apache/incubator-mxnet/tree/master/example/image-classification