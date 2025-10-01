from google.cloud import secretmanager
import json
from utils.config import PROJECT_ID, SECRET_ID

def get_service_account():
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/latest"
    response = client.access_secret_version(request={"name": secret_name})
    sa_dict = json.loads(response.payload.data.decode("UTF-8"))
    print("Sa_dict_wgj", sa_dict)
    return sa_dict
