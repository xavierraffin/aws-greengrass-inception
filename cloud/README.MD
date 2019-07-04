## Steps

```
$ export S3_OUTPUT_BUCKET=<your s3 buckets to upload the codes>
$ aws s3 mb ${S3_OUTPUT_BUCKET}
```

### With SAM CLI
```
$ sam package --s3-bucket ${S3_OUTPUT_BUCKET} --template-file greengrass-group.sam.yaml --output-template-file output/greengrass.cfn.yaml
$ am deploy --template-file output/greengrass.cfn.yaml --stack-name greengrass --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND
```

### Without SAM CLI
```
$ aws cloudformation package --template-file ./greengrass-group.sam.yaml --s3-bucket ${S3_OUTPUT_BUCKET} --output-template-file output/greengrass.cfn.yaml
$ aws cloudformation deploy --template-file output/greengrass.cfn.yaml --stack-name greengrass --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND
```