#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

# greengrassHelloWorld.py
# Demonstrates a simple publish to a topic using Greengrass core sdk
# This lambda function will retrieve underlying platform information and send
# a hello world message along with the platform information to the topic 'hello/world'
# The function will sleep for five seconds, then repeat.  Since the function is
# long-lived it will run forever when deployed to a Greengrass core.  The handler
# will NOT be invoked in our example since the we are executing an infinite loop.
#
# This can be found on the AWS IoT Console.

import greengrasssdk
import platform
from threading import Timer
import time
import load_model
import sys

# Creating a greengrass core sdk client
client = greengrasssdk.client('iot-data')

model_path = '/greengrass-machine-learning/mxnet/inception_bn/'
global_model = load_model.ImagenetModel(model_path + 'synset.txt', model_path + 'Inception_BN')

def greengrass_hello_world_run():
    if global_model is not None:
        try:
            predictions = global_model.predict_from_cam()
	    print predictions
            #publish predictions
            client.publish(topic='hello/world', payload='New Prediction: {}'.format(str(predictions)))
        except:
            e = sys.exc_info()[0]
            print("Exception occured during prediction: %s" % e)
            
    # Asynchronously schedule this function to be run again in 5 seconds
    Timer(5, greengrass_hello_world_run).start()


# Execute the function above
greengrass_hello_world_run()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return