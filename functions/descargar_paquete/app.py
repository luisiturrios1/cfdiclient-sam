import base64
import logging

import boto3
from cfdiclient import Autenticacion, DescargaMasiva, Fiel

BUCKET_NAME = 'cfdiclient-sam'

client = boto3.client('s3')


def get_token(fiel_cer: str, fiel_key: str, fiel_pass: str):
    cer_der = read_file(fiel_cer)
    key_der = read_file(fiel_key)
    fiel = Fiel(cer_der, key_der, fiel_pass)
    auth = Autenticacion(fiel)
    token = auth.obtener_token()
    return fiel, token


def read_file(key: str):
    response = client.get_object(Bucket=BUCKET_NAME, Key=key,)
    return response["Body"].read()


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
    rfc = event["rfc"]
    paquete = event["paquete"]
    fiel_cer = event["fiel_cer"]
    fiel_key = event["fiel_key"]
    fiel_pass = event["fiel_pass"]

    fiel, token = get_token(fiel_cer, fiel_key, fiel_pass)

    descarga = DescargaMasiva(fiel)

    descarga = descarga.descargar_paquete(token, rfc, paquete)

    if descarga["cod_estatus"] != "5000":
        logging.info(descarga)
        exit(1)

    s3_key = f'paquetes/{paquete}.zip'

    client.put_object(
        Body=base64.b64decode(descarga["paquete_b64"]),
        Bucket=BUCKET_NAME,
        Key=s3_key
    )

    return {"s3_key": s3_key}
