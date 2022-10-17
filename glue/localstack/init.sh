#!/bin/bash
# Create bucket
aws --endpoint-url=http://localstack:4566 s3 mb s3://bkt --region sa-east-1

# List buckets
aws --endpoint-url=http://localstack:4566 s3 ls --summarize --recursive --human-readable
aws --endpoint-url=http://localstack:4566 s3api put-bucket-acl --bucket bkt --acl public-read-write


aws --endpoint-url=http://localstack:4566 s3api list-objects --bucket bkt