from fastapi import FastAPI, File, Response, UploadFile, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from botocore.exceptions import NoCredentialsError
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
import boto3
import os

from app.connectionConfig import connect

app = FastAPI()

aws_access_key_id = 'AKIAV5IV5U6P5NEVGDGV'
aws_secret_access_key = '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'
aws_bucket_name = 'mybucketlabnemer'

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

conn = connect()

@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):

    query="insert into file (name,extension) values (%s,%s)"
    print(conn)
    print(conn.server_host)
    try:
        
        file_extension = file.filename.split(".")[-1]
        s3.upload_fileobj(file.file, aws_bucket_name, file.filename)

        if(conn.is_connected):
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS file(id INT AUTO_INCREMENT PRIMARY KEY, name varchar(50), extension varchar(50))")
            values = (file.filename,file_extension)
            cursor.execute(query,values)
            conn.commit()
            return {'message': 'Archivo subido exitosamente', 'file_name': file.filename}
        else:
            print("no se conecto bobo")
    except NoCredentialsError:
        raise HTTPException(
            status_code=500,
            detail='No se encontraron credenciales de AWS. Verifica tu configuración de credenciales.'
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Error al subir el archivo: {str(e)}'
        )
    finally:
        conn.close()

@app.get("/list_files")
async def list_files():
    try:
        response = s3.list_objects_v2(Bucket=aws_bucket_name)
        files = [obj['Key'] for obj in response.get('Contents', [])]
        return {"files": files}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Error al listar archivos: {str(e)}'
        )

@app.get('/download/{file_name}')
async def download(file_name: str):
    try:
        
        response = s3.get_object(Bucket=aws_bucket_name, Key=file_name)
        file_data = response['Body'].read()

        return Response(
            content=file_data,
            headers={
                'Content-Disposition': f'attachment; filename={file_name}',
                'Content-Type': 'application/octet-stream',
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Error al descargar el archivo: {str(e)}'
        )