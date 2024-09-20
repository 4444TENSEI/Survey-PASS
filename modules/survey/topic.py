import requests
from modules.config.config import load_config
from modules.survey.signature import upload_signature_img


config = load_config()
base_url = config["base_url"]
get_planid_url = config["get_planid_url"]
get_detail_url = config["get_detail_url"]


def get_request_with_jwt(url, jwt_token):
    headers = {"Authorization": f"Bearer {jwt_token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查HTTP请求的状态码
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误: {http_err}")
        print(f"状态码: {response.status_code}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"连接错误: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"请求超时: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"请求错误: {req_err}")
    except ValueError as json_err:
        print(f"JSON解析错误: {json_err}")
        print(f"响应内容: {response.text}")
    return None


def get_plan_and_scale_ids(jwt_token):
    # 初始化plan_id和scale_id
    plan_id = None
    scale_id = None

    # 获取planID
    response1 = get_request_with_jwt(base_url + get_planid_url, jwt_token)
    if response1 and response1.get("code") == 0 and response1.get("data"):
        items = response1["data"].get("items")
        if items:
            plan_id = items[0]["planID"]

            # 获取scaleId
            url2 = f"{base_url}{get_detail_url}?id={plan_id}"
            response2 = get_request_with_jwt(url2, jwt_token)
            if response2 and response2.get("code") == 0 and response2.get("data"):
                plan_detail = response2["data"][0]
                scale_list = plan_detail.get("scaleList")
                if scale_list:
                    scale_id = scale_list[0]["scaleId"]

    # 输出获取到的plan_id和scale_id，或者提醒
    if plan_id and scale_id:
        print(f"获取到的plan_id: {plan_id}, scale_id: {scale_id}")
        response_text = upload_signature_img(jwt_token)
        print(f"上传签名图片响应: {response_text}")
    else:
        message = "获取目标: "
        message += f"plan_id: {plan_id}" if plan_id else "未获取到plan_id "
        message += ", " if plan_id and scale_id is not None else ""
        message += f"scale_id: {scale_id}" if scale_id else " - 未获取到scale_id"
        print(message)

    return plan_id, scale_id
