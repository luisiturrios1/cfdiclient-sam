import base64
import json
import os
import uuid

import boto3

BUCKET_NAME = os.getenv('BUCKET_NAME')
STATE_MACHINE_ARN = os.getenv('STATE_MACHINE_ARN')

stepfunctions = boto3.client('stepfunctions')
s3 = boto3.resource('s3')


def lambda_handler(event, context):
    """Sample Lambda function which mocks the operation of buying a random number
    of shares for a stock.

    For demonstration purposes, this Lambda function does not actually perform any
    actual transactions. It simply returns a mocked result.

    Parameters
    ----------
    event: dict, required
        Input event to the Lambda function

    context: object, required
        Lambda Context runtime methods and attributes

    Returns
    ------
        dict: Object containing details of the stock buying transaction
    """
    datos_de_descarga = json.loads(event["body"])

    rfc = datos_de_descarga["rfc"]

    path = f"field/{rfc}/{rfc}.cer"
    obj = s3.Object(BUCKET_NAME, path)
    obj.put(Body=base64.b64decode(datos_de_descarga["fiel_cer"]))
    datos_de_descarga["fiel_cer"] = path

    path = f"field/{rfc}/{rfc}.key"
    obj = s3.Object(BUCKET_NAME, path)
    obj.put(Body=base64.b64decode(datos_de_descarga["fiel_key"]))
    datos_de_descarga["fiel_key"] = path

    response = stepfunctions.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        name=f"{rfc}_{str(uuid.uuid4())}",
        input=json.dumps(datos_de_descarga)
    )

    return {
        "statusCode": 200,
        "body": json.dumps({})
    }
