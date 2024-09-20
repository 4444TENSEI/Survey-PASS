import requests
from modules.config.config import load_config
from modules.login.codekey.analytic import get_captcha

config = load_config()

base_url = config["base_url"]
code_key_ocr_url = base_url + config["code_key_ocr_url"]
get_code_key_url = config["get_code_key_url"]

min_code_key_length = config.get("min_code_key_length")


def get_code_key():
    # 使用requests获取OCR识别的验证码URL
    try:
        response = requests.get(code_key_ocr_url)
        if response.status_code == 200:
            response_data = response.json()
            code_key = response_data["data"]["codeKey"]
            imgVCode = None
            retry_count = 0
            while True:
                retry_count += 1
                # 获取验证码图片
                imgVCode, error = get_captcha(get_code_key_url, code_key)
                if imgVCode:
                    # 如果配置中有min_code_key_length, 则检查长度
                    if min_code_key_length is not None:
                        if len(imgVCode) == min_code_key_length:
                            break
                        else:
                            print(
                                f"第{retry_count}次尝试 - 验证码长度与配置文件长度不符, 期望: {min_code_key_length}, 实际: {len(imgVCode)}, "
                            )
                    else:
                        break
                else:
                    print(f"{error} (第{retry_count}次尝试)")
                    return None, None
            return code_key, imgVCode
        else:
            print(f"无法获取codeKey, 服务器响应状态码: {response.status_code}")
            return None, None
    except Exception as e:
        print(str(e))
        return None, None


# 测试获取验证码图片的接口并且解析的调试语句
# code_key, imgVCode = get_code_key()
# if code_key and imgVCode:
#     print(f"\nCode Key: {code_key}")
#     print(f"\nImage VCode: {imgVCode}")
# else:
#     print("未能获取有效的Code Key或Image VCode")
