## Uses Jupyter Notebook to Cloudformation stacks for demo of Inference @ Edge using Greengrass

This is a guided demo on how to run Machine Learning Inference at Edge with AWS IoT Greengrass.

The notebook [GreengrassConfig.ipynb](GreengrassConfig.ipynb) contains the steps, and it will create 2 stacks as follows:

* Stack 1 - Creates AWS IoT Thing and Greengrass core
* Stack 2 - Creates an AWS EC2 with Greengrass software

## Step 1 - Create an AWS EC2 with Jupyter Notebook

|AWS Region|Region|CloudFormation|
|-|-|-|
|US East (Ohio)|us-east-2|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=aws-iot-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|US East (N. Virginia)|us-east-1|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=aws-iot-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|US West (Oregon)|us-west-2|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=aws-iot-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|Asia Pacific (Mumbai)|ap-south-1|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?stackName=aws-iot-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|Asia Pacific (Seoul)|ap-northeast-2|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?stackName=aws-iot-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|Asia Pacific (Singapore)|ap-southeast-1|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?stackName=aws-iot-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|Asia Pacific (Sydney)|ap-southeast-2|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=aws-iot-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|Asia Pacific (Tokyo)|ap-northeast-1|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=aws-iot-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|China (Beijing)|cn-north-1|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=cn-north-1#/stacks/new?stackName=aws-iot-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|EU (Frankfurt)|eu-central-1|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?stackName=aws-iot-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|EU (Ireland)|eu-west-1|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=aws-iot-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|EU (London)|eu-west-2|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?stackName=aws-iot-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|

## Step 2 - Clone this repository

1. Create a new Python 3 notebook
2. In the empty cell, enter the following command to clone this repository along with the sub modules

```
!git clone --recursive https://github.com/kangks/aws-greengrass-mxnet-inception.git
```