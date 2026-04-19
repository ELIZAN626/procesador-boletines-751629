from fastapi import FastAPI, HTTPException
import boto3

app = FastAPI()
dynamo = boto3.resource("dynamodb", region_name="us-east-1")
tabla = dynamo.Table("boletines")

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