awslocal dynamodb  list-tables

awslocal dynamodb put-item --table-name dev-cfdiclient-sam-EmpresaDBTable-1cc6ca86 \
    --item \
    '{                                             
        "rfc": {"S": "IUAL9406031K3"},
        "fiel_cer": {"S": "iual9406031k3.cer"},
        "fiel_key": {"S": "Claveprivada_FIEL_IUAL9406031K3_20231025_135809.key"},
        "fiel_pass": {"S": "koy12345"},
        "ultima_descarga": {"S": "2024-04-18T01:51:00"},
        "activo": {"BOOL": true},
        "procesando": {"BOOL": false}
    }'

awslocal dynamodb create-table \
    --table-name Empresa \
    --attribute-definitions \
        AttributeName=rfc,AttributeType=S \
    --key-schema \
        AttributeName=rfc,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

awslocal dynamodb describe-table --table-name Empresa

awslocal dynamodb delete-table --table-name Empresa

awslocal dynamodb put-item --table-name Empresa     \
    --item                                          \
    '{                                             
        "rfc": {"S": "IUAL9406031K3"},
        "fiel_cer": {"S": "fiel/cer/IUAL9406031K3.cer"},
        "fiel_key": {"S": "fiel/key/IUAL9406031K3.key"},
        "fiel_pass": {"S": "koy123453"},
        "ultima_descarga": {"S": "2024-04-04T22:32:07.767894-06:00"},
        "activo": {"BOOL": true},
        "procesando": {"BOOL": false}
    }'

awslocal dynamodb get-item  \
    --table-name Empresa    \
    --key '{"rfc": {"S": "IUAL9406031K3"}}' \
    --consistent-read

awslocal dynamodb scan                                             \
    --table-name Empresa                                           \
    --filter-expression "activo=:activo"                         \
    --expression-attribute-values '{":activo":{"BOOL":true}}'

awslocal dynamodb query                                                                    \
    --table-name Empresa                                                                   \
    --key-condition-expression "activo = :activo"                 \
    --expression-attribute-values'{":procesando":{"BOOL":false}}'

awslocal dynamodb delete-item \
    --table-name Empresa \
    --key '{"rfc": {"S": "IUAL9406031K23"}}'



aws --endpoint-url http://127.0.0.1:8000 dynamodb create-table \
    --table-name Empresa \
    --attribute-definitions \
        AttributeName=rfc,AttributeType=S \
    --key-schema \
        AttributeName=rfc,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST



aws --endpoint-url http://127.0.0.1:8000 dynamodb scan                                             \
    --table-name Empresa  


awslocal dynamodb update-item \
    --table-name Empresa \
    --key '{"rfc":{"S":"IUAL9406031K3"}}' \
    --update-expression \
    "SET procesando = :procesando, ultima_descarga = :ultima_descarga" \
    --expression-attribute-values \
    '{":procesando": {
		"BOOL": false
	},
	":ultima_descarga": {
		"S": "12"
	}}'
    
