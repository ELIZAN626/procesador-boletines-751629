import os
import boto3
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Config con variables de entorno
tabla_db = os.getenv("DYNAMO_TABLE")
region = os.getenv("AWS_REGION", "us-east-1")

@app.get("/boletines/{boletinid}")
async def ver_boletin(boletinid: str, correo: str):
    # buscar boletin
    res = tabla.get_item(Key={"boletin_id": boletinid})
    if "Item" not in res:
        raise HTTPException(status_code=404, detail="boletin no encontrado")
    
    item = res["Item"]
    if item["correo"] != correo:
        raise HTTPException(status_code=403, detail="acceso denegado")
    
    # marcar como leido
    tabla.update_item(
        Key={"boletin_id": boletinid},
        UpdateExpression="SET leido = :l",
        ExpressionAttributeValues={":l": True}
    )
    
    return {
        "imagen": item["url_imagen"],
        "mensaje": item["mensaje"]
    }