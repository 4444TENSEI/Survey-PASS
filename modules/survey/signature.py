import os
import requests
from modules.config.config import load_config


config = load_config()
base_url = config["base_url"]
upload_signature_img_url = base_url + config["upload_signature_img_url"]

signature_img_file_path = config["signature_img_file_path"]


def upload_signature_img(jwt_token):

    # 使用with语句打开文件, 确保文件在使用后关闭
    with open(signature_img_file_path, "rb") as file:
        files = {"file": (os.path.basename(signature_img_file_path), file, "image")}
        headers = {"Authorization": f"Bearer {jwt_token}"}

        response = requests.post(upload_signature_img_url, headers=headers, files=files)

    return response.text
