aws cloudformation create-stack --stack-name ApexLegendsRanking-dynamodb --template-body file://cron/stack/dynamodb/template.yml --parameters file://cron/stack/dynamodb/parameters.json 
aws cloudformation update-stack --stack-name ApexLegendsRanking-dynamodb --template-body file://cron/stack/dynamodb/template.yml --parameters file://cron/stack/dynamodb/parameters.json 
aws cloudformation delete-stack --stack-name ApexLegendsRanking-dynamodb

aws cloudformation create-stack --stack-name ApexLegendsRanking-samPackage --template-body file://cron/stack/s3/template.yml  
aws cloudformation delete-stack --stack-name ApexLegendsRanking-samPackage

# sam package --template-file ./cron/stack/lambda/template.yml --output-template-file ./cron/stack/lambda/packaged.yml --s3-bucket apexlegendsranking-sampackage
# sam deploy --stack-name ApexLegendsRanking-cron --template-file ./cron/stack/lambda/packaged.yml
sam deploy --stack-name ApexLegendsRanking-cron --template-file ./cron/stack/lambda/template.yml
aws cloudformation delete-stack --stack-name ApexLegendsRanking-cron
