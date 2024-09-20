import os, datetime

# 日志文件路径
data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
log_file_path = os.path.join(data_dir, "login_log.txt")


def log_to_file(message):
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")
    print(message)


def is_message_in_log(message):
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w", encoding="utf-8"):
            pass
    with open(log_file_path, "r", encoding="utf-8") as log_file:
        return message in log_file.read()


def update_log_file_counters(success_count, failure_count):
    global log_file_path  # 引入全局变量以修改文件内容
    with open(log_file_path, "r+", encoding="utf-8") as log_file:
        content = log_file.readlines()
        # 移除旧的计数器信息
        content = [line for line in content if not line.startswith("**")]

        # 插入新的计数器信息
        content.insert(0, f"\n** 成功数量: {success_count}")
        content.insert(1, f"\n** 失败数量: {failure_count}")

        # 将文件指针移回文件开始
        log_file.seek(0)
        log_file.writelines(content)
        log_file.truncate()  # 截断文件以移除旧内容


def clear_log_file():
    # 清空日志文件
    with open(log_file_path, "w", encoding="utf-8"):
        pass


def mark_end_of_program():
    global log_file_path  # 引入全局变量以修改文件内容
    # 在程序结束时写入日期时间到日志文件顶部
    with open(log_file_path, "r+", encoding="utf-8") as log_file:
        content = log_file.readlines()
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content.insert(0, f"** {current_datetime}\n请注意每次运行程序都会清空日志!\n")
        log_file.seek(0)
        log_file.writelines(content)
        log_file.truncate()
