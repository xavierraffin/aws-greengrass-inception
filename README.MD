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
