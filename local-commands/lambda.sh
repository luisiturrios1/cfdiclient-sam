# Listar lambdas
awslocal lambda list-functions

# Invokar una lambda
awslocal lambda invoke --function-name "dev-cfdiclient-sam-PlanificadorFunction-2d23ce18" /dev/stdout


awslocal lambda get-function --function-name cfdiclient-sam-DescargarPaqueteFunction-5f6c9ea8
awslocal lambda get-function --function-name cfdiclient-sam-DescargarPaqueteFunction-5f6c9ea8 --query 'Code.Location'
