import requests
import base64
import json
import time
import random
from modules.config.config import load_config
from modules.config.log import log_to_file, update_log_file_counters, is_message_in_log
from modules.login.codekey.getcode import get_code_key
import os

# 跳过字典, 包含不需要重试的错误信息关键词
skip_dict = {"密码错误", "频繁"}

# 重试字典, 包含需要重新获取验证码的错误信息关键词
retry_dict = {"证码输入错误"}

# 配置加载
config = load_config()

base_url = config["base_url"]
login_url = base_url + config["login_url"]

retry_num = config["retry_num"]


# 计数器初始化
success_count = 0
failure_count = 0


def should_skip(message):
    for keyword in skip_dict:
        if keyword in message:
            return True
    return False


def should_retry(message):
    for keyword in retry_dict:
        if keyword in message:
            return True
    return False


def login_user(login_name, password, code_key, imgVCode):
    global success_count, failure_count
    login_success = False
    token = None
    retry_count = 0  # 初始化重试次数计数器

    for login_attempts in range(retry_num):
        login_name_encoded = base64.b64encode(login_name.encode("utf-8")).decode(
            "utf-8"
        )
        password_encoded = base64.b64encode(password.encode("utf-8")).decode("utf-8")

        login_data = {
            "login_name": login_name_encoded,
            "password": password_encoded,
            "codeKey": code_key,
            "imgVCode": imgVCode,
        }

        response = requests.post(login_url, data=login_data)

        if response.status_code == 200:
            try:
                response_json = response.json()
                code = response_json.get("code")
                message = response_json.get("message")

                if code != 0:
                    if should_skip(message):
                        log_message = f"用户 {login_name} 登录跳过: {message}"
                        if not is_message_in_log(log_message):
                            log_to_file(log_message)
                        break
                    elif should_retry(message):
                        print(f"\n用户 {login_name} 验证码输入错误，将重新尝试...")
                        code_key, imgVCode = get_code_key()
                        retry_count += 1  # 增加重试次数计数器
                        if retry_count >= retry_num:
                            print(f"用户 {login_name} 达到最大重试次数，将停止尝试。")
                            break
                        continue
                    else:
                        log_message = f"用户 {login_name} 尝试登录失败: {message}"
                        if login_attempts == retry_num - 1 and not is_message_in_log(
                            log_message
                        ):
                            log_to_file(log_message)
                        else:
                            log_to_file(log_message + " 将重试...")
                        random_wait = random.randint(1000, 2000) / 1000.0
                        time.sleep(random_wait)
                        code_key, imgVCode = get_code_key()
                else:
                    token = response_json.get("data", {}).get("token")
                    token_expiration = response_json.get("data", {}).get(
                        "tokenExpiration"
                    )
                    refresh_token = response_json.get("data", {}).get("refreshToken")
                    refresh_token_expiration = response_json.get("data", {}).get(
                        "refreshTokenExpiration"
                    )

                    print(f"\n√√√ 用户: {login_name} 登录成功\n{token}")
                    log_message = f"令牌过期时间: {token_expiration} - 刷新令牌过期时间: {refresh_token_expiration}"
                    print(log_message)
                    success_count += 1
                    login_success = True
                    break
            except json.JSONDecodeError:
                log_message = (
                    f"用户 {login_name} 尝试登录失败: 响应内容不是有效的JSON格式"
                )
                if not is_message_in_log(log_message):
                    log_to_file(log_message)
                break
        else:
            log_message = (
                f"用户 {login_name} 登录请求失败, 状态码: {response.status_code}"
            )
            if not is_message_in_log(log_message):
                log_to_file(log_message)
            break
        if login_success:
            retry_count = 0

    if not login_success:
        failure_count += 1

    update_log_file_counters(success_count, failure_count)
    return token if login_success else None
