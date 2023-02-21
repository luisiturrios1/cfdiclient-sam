import logging

import boto3
import dateutil
from cfdiclient import Autenticacion, Fiel, SolicitaDescarga

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
    fecha_inicial = dateutil.parser.isoparse(event["fecha_inicial"])
    fecha_final = dateutil.parser.isoparse(event["fecha_final"])
    rfc_receptor = event.get("rfc_receptor", None)
    rfc_emisor = event.get("rfc_emisor", None)
    tipo_solicitud = event["tipo_solicitud"]
    fiel_cer = event["fiel_cer"]
    fiel_key = event["fiel_key"]
    fiel_pass = event["fiel_pass"]

    fiel, token = get_token(fiel_cer, fiel_key, fiel_pass)

    descarga = SolicitaDescarga(fiel)

    solicitud = descarga.solicitar_descarga(
        token, rfc,
        fecha_inicial,
        fecha_final,
        rfc_receptor=rfc_receptor,
        rfc_emisor=rfc_emisor,
        tipo_solicitud=tipo_solicitud
    )

    return solicitud
