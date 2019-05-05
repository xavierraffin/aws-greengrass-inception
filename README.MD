# ML@Edge with AWS GreenGrass Core

ML@Edge Image Classifications example using MXNet pretrained model with GreenGrass Core running on a Rasperry Pi

## Description

This is an example of running Lambda on GreenGrass with MXNet pretrained model Inception v3 for image classification

Details on Inception v3 can be found in https://arxiv.org/abs/1512.00567

## Prerequisite

* Raspberry Pi 3 Model B+ set up and configured for use with AWS IoT Greengrass
* Raspberry Pi Camera Module V2 - 8 Megapixel, 1080p
* A Greengrass group and a Greengrass core

(Details in https://docs.aws.amazon.com/greengrass/latest/developerguide/ml-console.html#ml-inference-prerequisites)

## Steps

### To run in Rapsberry Pi

* Git clone or download this repository to the Raspberry Pi
* Runs the local main python file

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

### To run in GreenGrass

1. Create a Lambda function and upload this repository as a zip file
2. Create a version and alias pointing to the version
4. Create the Local and Machine Learning resources
5. Add the Lambda to the GreenGrass group and associate the resources to the lambda
6. Deploy
7. If all configuration is correct, an MQTT message with topic "hello/world' should be seen in the AWS IoT Test client, such as 

```
New Prediction: [(0.18657419, 'n02676566 acoustic guitar'), (0.14744462, 'n03929660 pick, plectrum, plectron'), (0.1250492, 'n02787622 banjo'), (0.049499936, 'n03271574 electric fan, blower'), (0.038708802, 'n03476684 hair slide')]
```

## Local subscriber

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