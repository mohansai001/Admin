from fastapi import APIRouter, HTTPException
from vida.utils.AzureSecrets import get_all_azure_secrets,get_azure_secret_value, set_azure_secret, delete_azure_secret

router = APIRouter()

@router.get("/secrets_list")
def secrets_list():
    secrets = get_all_azure_secrets()
    return {"secrets": secrets}

@router.get("/get_secret_value/{secret_name}")
def get_secret_value(secret_name: str):
    secret_value = get_azure_secret_value(secret_name)
    if secret_value is None:
        raise HTTPException(status_code=404, detail="Secret not found")
    return {"secret_name": secret_name, "secret_value": secret_value}

@router.post("/set_secret")
def set_secret(secret_name: str, secret_value: str):
    set_azure_secret(secret_name, secret_value)
    return {"message": "Secret set successfully"}

@router.delete("/delete_secret/{secret_name}")
def delete_secret(secret_name: str):
    delete_azure_secret(secret_name)
    return {"message": "Secret deleted successfully"}