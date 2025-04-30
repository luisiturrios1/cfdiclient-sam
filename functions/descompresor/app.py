import boto3
import os
from aws_lambda_powertools import Logger
import zipfile
import tempfile

DOCUMENTOS_BUCKET_NAME = os.environ.get("DOCUMENTOS_BUCKET_NAME")

logger = Logger()


@logger.inject_lambda_context
def lambda_handler(event, context):
    # Obtener el nombre del bucket y el nombre del archivo zip del evento
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    zip_file_key = event['Records'][0]['s3']['object']['key']
    rfc, fecha, id_solicitud, paquete = zip_file_key.split('/')

    logger.info(zip_file_key)

    # Configurar el cliente de S3
    s3 = boto3.client('s3')

    # Descargar el archivo zip en un directorio temporal
    with tempfile.TemporaryDirectory() as temp_dir:
        local_zip_path = os.path.join(temp_dir, 'temp.zip')
        s3.download_file(source_bucket, zip_file_key, local_zip_path)

        # Descomprimir el archivo zip
        with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Subir el contenido descomprimido al nuevo bucket
        for extracted_file in os.listdir(temp_dir):
            if extracted_file == "temp.zip":
                continue
            extracted_file_path = os.path.join(temp_dir, extracted_file)
            if os.path.isfile(extracted_file_path):
                # Nombre de archivo resultante en el nuevo bucket
                new_key = f"{rfc}/{fecha}/{extracted_file}"
                # Subir el archivo al nuevo bucket
                s3.upload_file(extracted_file_path,
                               DOCUMENTOS_BUCKET_NAME, new_key)

    return {}
