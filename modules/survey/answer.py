import random
import json
from modules.survey.topic import get_request_with_jwt
from modules.config.config import load_config


config = load_config()
base_url = config["base_url"]
answer_url = config["answer_url"]


def get_first_option_ids_and_count(plan_id, scale_id, jwt_token):
    # 构造获取题目详情的URL
    get_question_url = f"{base_url}{answer_url}?planid={plan_id}&scaleId={scale_id}"

    # 发送带有JWT的GET请求
    response = get_request_with_jwt(get_question_url, jwt_token)

    # 初始化题目数量和选项列表
    question_count = 0
    question_option_list = []

    # 初始化返回状态和消息
    success = False
    message = "操作成功"

    # 检查响应是否成功
    if response is not None and response.get("code") == 0 and "data" in response:
        question_list = response["data"]["questionList"]
        question_count = len(question_list)  # 统计题目数量

        # 遍历题目列表, 收集每个题目的第一个选项ID
        for question in question_list:
            first_option = question["optionList"][0]
            question_option_list.append(
                {
                    "questionId": question["questionId"],
                    "optionId": first_option["optionId"],
                }
            )
        success = True
    else:
        success = False
        message = "获取题目列表失败或响应无效"

    # 生成随机数作为useTime, 100代表一分钟
    use_time = random.randint(301, 2999)

    # 构造最终的JSON格式数据
    output_data = {
        "planId": plan_id,
        "scaleId": scale_id,
        "useTime": use_time,
        "questionCount": question_count,
        "questionList": question_option_list,
    }

    # 将字典转换为JSON格式的字符串
    output_json = json.dumps(output_data, ensure_ascii=False)

    return output_json
