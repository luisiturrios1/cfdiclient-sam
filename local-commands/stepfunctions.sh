aws stepfunctions --endpoint http://localhost:8083 create-state-machine --definition "{\
  \"Comment\": \"A Hello World example of the Amazon States Language using an AWS Lambda Local function\",\
  \"StartAt\": \"PlanificadorFunction\",\
  \"States\": {\
    \"PlanificadorFunction\": {\
      \"Type\": \"Task\",\
      \"Resource\": \"arn:aws:lambda:us-east-1:123456789012:function:PlanificadorFunction\",\
      \"End\": true\
    }\
  }\
}" --name "PlanificadorFunction" --role-arn "arn:aws:iam::012345678901:role/PlanificadorFunction"

awslocal stepfunctions list-state-machines

awslocal stepfunctions start-execution --state-machine-arn "arn:aws:states:us-east-1:123456789012:stateMachine:PlanificadorFunction"

awslocal stepfunctions describe-state-machine --state-machine-arn arn:aws:states:us-east-1:000000000000:stateMachine:dev-cfdiclient-sam-CfdiClientStateMachine-25eba27e
