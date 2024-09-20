from modules.login.codekey.getcode import get_code_key
from modules.login.excel import read_excel
from modules.login.login import login_user
from modules.survey.topic import get_plan_and_scale_ids
from modules.survey.answer import get_first_option_ids_and_count
from modules.survey.submit import post_request_with_jwt
from modules.config.log import clear_log_file, mark_end_of_program

# 主程序
if __name__ == "__main__":
    users_account = read_excel()
    clear_log_file()
    # 按照用户列表的顺序执行登录尝试
    for user in users_account:
        login_name = user["login_name"]
        password = user["password"]
        codeKey, imgVCode = get_code_key()
        jwt_token = login_user(login_name, password, codeKey, imgVCode)
        if jwt_token:

            plan_id, scale_id = get_plan_and_scale_ids(jwt_token)
            if plan_id and scale_id:
                output_data = get_first_option_ids_and_count(
                    plan_id, scale_id, jwt_token
                )

                print(output_data)
                response = post_request_with_jwt(jwt_token, output_data)
                print(f"问卷已提交, 响应: {response.status_code}")
                print(response.json())

    mark_end_of_program()
