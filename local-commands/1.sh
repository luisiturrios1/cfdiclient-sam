# aws dynamodb list-tables
DYNAMO_DB_TABLE="dev-cfdiclient-sam-EmpresaDBTable-1TOJCZLCTFNL1"

# aws s3 ls
FIRMAS_BUCKET="dev-cfdiclient-sam-firmasbucket-zxlvg1psfnw7"

PLAIFICADOR_LAMBDA="dev-cfdiclient-sam-PlanificadorFunction-icyuQ54Cbbst"

# aws s3 cp iual9406031k3.cer s3://$FIRMAS_BUCKET/IUAL9406031K3/IUAL9406031K3.cer
# aws s3 cp Claveprivada_FIEL_IUAL9406031K3_20231025_135809.key s3://$FIRMAS_BUCKET/IUAL9406031K3/IUAL9406031K3.key

# aws dynamodb put-item --table-name $DYNAMO_DB_TABLE \
#     --item \
#     '{                                             
#         "rfc": {"S": "IUAL9406031K3"},
#         "nombre": {"S": "Luis Jesus Iturrios Alcaraz"},
#         "activo": {"BOOL": true},
#         "fiel_cer": {"S": "IUAL9406031K3/IUAL9406031K3.cer"},
#         "fiel_key": {"S": "IUAL9406031K3/IUAL9406031K3.key"},
#         "fiel_pass": {"S": "koy12345"},
#         "ultima_descarga_recibidos": {"S": "2024-01-01T00:00:01"},
#         "ultima_descarga_emitidos": {"S": "2024-01-01T12:00:01"},
#         "procesando_recibidos": {"BOOL": false},
#         "procesando_emitidos": {"BOOL": false}
#     }'

aws lambda invoke --function-name "$PLAIFICADOR_LAMBDA" /dev/stdout
