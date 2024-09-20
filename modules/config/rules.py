def normal_rule(value):
    return value if value is not None else None


def birthday_rule(id_card):
    if isinstance(id_card, str) and len(id_card) >= 7:
        return id_card[6:14]  # 从第七位开始提取八位数生日号码
    return None
