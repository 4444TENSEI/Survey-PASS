import requests
from ddddocr import DdddOcr
from modules.config.config import load_config


config = load_config()
base_url = config["base_url"]


# 传入url和url中的变量, 进行具体的验证码图片识别
def get_captcha(get_code_key_url, code_key):
    try:
        new_url = f"{base_url}{get_code_key_url}?codeKey={code_key}"
        response_image = requests.get(new_url)
        if response_image.status_code == 200:
            img_bytes = response_image.content
            ocr = DdddOcr(show_ad=False)
            imgVCode = ocr.classification(img_bytes)
            return imgVCode, None
        else:
            return (
                None,
                f"无法获取验证码图片, 服务器响应状态码: {response_image.status_code}",
            )
    except Exception as e:
        return None, str(e)
