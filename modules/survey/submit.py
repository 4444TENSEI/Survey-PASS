import requests
from modules.config.config import load_config


config = load_config()
base_url = config["base_url"]
submit_url = base_url + config["submit_url"]


def post_request_with_jwt(jwt_token, output_data):

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json;charset=UTF-8",
    }

    data = output_data

    response = requests.post(submit_url, headers=headers, data=data)

    return response
