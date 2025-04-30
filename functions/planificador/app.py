import boto3
from boto3.dynamodb.conditions import Attr
import os
import json
from datetime import datetime
import pytz
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

TIMEZONE = "America/Mexico_City"
TIPO_SOLICITUD = "CFDI"
EMPRESA_TABLE_NAME = os.environ.get("EMPRESA_TABLE_NAME")
CFDI_CLIENT_STATE_MACHINE_ARN = os.environ.get("CFDI_CLIENT_STATE_MACHINE_ARN")

logger = Logger()
client = boto3.resource("dynamodb")
stepfunctions = boto3.client('stepfunctions')


@logger.inject_lambda_context
def lambda_handler(event, context):
    """planificador determina cuales empresas necesitan ser actualizadas.

    Realiza una consulta a DynamoDB para determinar cual empresa requiere ejecutar
    un flujo de actualización

    Parameters
    ----------
    event: dict, required
        Input event to the Lambda function

    context: object, required
        Lambda Context runtime methods and attributes

    Returns
    ------
        dict:
    """

    now_date = datetime.now(pytz.timezone(TIMEZONE))

    table = client.Table(EMPRESA_TABLE_NAME)

    # Consultar empresas activas
    response = table.scan(FilterExpression=Attr("activo").eq(True))

    excutions = []

    logger.info({"toUpdate": len(response["Items"])})

    for item in response["Items"]:

        stepfunction_name = f"{now_date.strftime('%Y-%m-%dT%H-%M-%S')}_{item['rfc']}"

        event = {
            "rfc": item["rfc"],
            "fecha_final": now_date.strftime('%Y-%m-%dT%H:%M:%S'),
            "tipo_solicitud": TIPO_SOLICITUD,
            "fiel_cer": item["fiel_cer"],
            "fiel_key": item["fiel_key"],
            "fiel_pass": item["fiel_pass"],
        }

        logger.info({
            "rfc": item["rfc"],
            "skip_recibidos": item["procesando_recibidos"],
            "skip_emitidos": item["procesando_emitidos"],
        })

        if not item["procesando_recibidos"]:

            event["rfc_receptor"] = item["rfc"]
            event["fecha_inicial"] = item["ultima_descarga_recibidos"]

            response_recibidos = stepfunctions.start_execution(
                stateMachineArn=CFDI_CLIENT_STATE_MACHINE_ARN,
                name=f"{stepfunction_name}_recibidos",
                input=json.dumps(event)
            )

            excutions.append(response_recibidos["executionArn"])

            logger.info({
                "rfc": event["rfc"],
                "Solicitud": "recibidos",
                "tipo_solicitud": event["tipo_solicitud"],
                "fecha_inicial": event["fecha_inicial"],
                "fecha_final": event["fecha_final"],
                'stepFunctionExecutionArn': response_recibidos["executionArn"]
            })

            event.pop("rfc_receptor")
            event.pop("fecha_inicial")

        if not item["procesando_emitidos"]:

            event["rfc_emisor"] = item["rfc"]
            event["fecha_inicial"] = item["ultima_descarga_emitidos"]

            response_emitidos = stepfunctions.start_execution(
                stateMachineArn=CFDI_CLIENT_STATE_MACHINE_ARN,
                name=f"{stepfunction_name}_emitidos",
                input=json.dumps(event)
            )

            excutions.append(response_emitidos["executionArn"])

            logger.info({
                "rfc": event["rfc"],
                "Solicitud": "emitidos",
                "tipo_solicitud": event["tipo_solicitud"],
                "fecha_inicial": event["fecha_inicial"],
                "fecha_final": event["fecha_final"],
                "stepFunctionExecutionArn": response_emitidos["executionArn"]
            })

            event.pop("rfc_emisor")
            event.pop("fecha_inicial")

    return excutions
