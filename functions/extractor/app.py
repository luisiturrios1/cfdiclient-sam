import os
import boto3
import xml.etree.ElementTree as ET
from aws_lambda_powertools import Logger

from parser33 import parser33
from parser40 import parser40

DOCUMENTOS_TABLE_NAME = os.environ.get("DOCUMENTOS_TABLE_NAME")

logger = Logger()
s3 = boto3.client('s3')


def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    response = s3.get_object(Bucket=bucket_name, Key=object_key)

    xml_content = response['Body'].read().decode('utf-8')

    root = ET.fromstring(xml_content)

    version = root.attrib.get('Version')

    logger.info(f"File: {object_key} Version: {version}")

    if version == '4.0':
        campos_cfdi = parser40(root)
    elif version == '3.3':
        campos_cfdi = parser33(root)
    else:
        raise Exception(
            f"CFDI {object_key} Version {version} parser no implementado")

    # Guardar path en S3
    campos_cfdi["object_key"] = object_key

    # Guardar los campos extraídos en una tabla DynamoDB u otra acción deseada
    # Por ejemplo, guardarlos en una tabla DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DOCUMENTOS_TABLE_NAME)
    table.put_item(Item=campos_cfdi)

    return {}
