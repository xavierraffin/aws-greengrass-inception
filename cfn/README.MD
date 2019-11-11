## Uses Jupyter Notebook to Cloudformation stacks for demo of Inference @ Edge using Greengrass

This is a guided demo on how to run Machine Learning Inference at Edge with AWS IoT Greengrass.

The Jupyter notebook [GreengrassConfig.ipynb](GreengrassConfig.ipynb) contains the steps, and it will create 2 stacks as follows:

* Stack 1 - Creates AWS IoT Thing and Greengrass core
* Stack 2 - Creates an AWS EC2 with Greengrass software

## Step 1 - Create an AWS EC2 with Jupyter Notebook

Use one of the Cloudformation templates below to spin up an EC2 with Jupyter. You need to enter a password to access the notebook, minimum length of the password is 12, and allows only letters and numbers.

Once the stack is `CREATE_COMPLETE`, access the notebook from the URL which can be found in the `Outputs` of the stack.

|AWS Region|Region|CloudFormation|
|-|-|-|
|US East (Ohio)|us-east-2|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/new?stackName=ec2-jupyter-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|US East (N. Virginia)|us-east-1|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=ec2-jupyter-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|US West (Oregon)|us-west-2|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/new?stackName=ec2-jupyter-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|Asia Pacific (Mumbai)|ap-south-1|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/new?stackName=ec2-jupyter-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|Asia Pacific (Seoul)|ap-northeast-2|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-2#/stacks/new?stackName=ec2-jupyter-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|Asia Pacific (Singapore)|ap-southeast-1|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-1#/stacks/new?stackName=ec2-jupyter-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|Asia Pacific (Sydney)|ap-southeast-2|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/new?stackName=ec2-jupyter-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|Asia Pacific (Tokyo)|ap-northeast-1|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/new?stackName=ec2-jupyter-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|China (Beijing)|cn-north-1|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=cn-north-1#/stacks/new?stackName=ec2-jupyter-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|EU (Frankfurt)|eu-central-1|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-central-1#/stacks/new?stackName=ec2-jupyter-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|EU (Ireland)|eu-west-1|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=ec2-jupyter-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|
|EU (London)|eu-west-2|[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-2#/stacks/new?stackName=ec2-jupyter-greengrass-mli&templateURL=https://cloudformation-stacks-us-east-1.s3.amazonaws.com/aws-greengrass-mxnet-inception/jupyter-ec2.yaml)|

## Step 2 - Clone this repository

1. In the `Launcher` tab, click on `Python 3` Jupyter notebook to create a new notebook
2. In the empty cell, enter the following command to clone this repository along with the sub modules
```
!git clone --recursive https://github.com/kangks/aws-greengrass-mxnet-inception.git
```
3. From the menu at the top, select `Run`, `Run Selected Cells`
4. This repository should be available in the `File Browser` at the left. Click on the folder `aws-greengrass-mxnet-inception/cfn/`
5. Open the Jupyter notebook `GreengrassConfig.ipynb`
6. Follow the steps in the `GreengrassConfig.ipynb`