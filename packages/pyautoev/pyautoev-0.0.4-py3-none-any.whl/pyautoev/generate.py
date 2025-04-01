# -*- coding: utf-8 -*-
def generate_sequence(r, n):
    """
        r: Str
        n: sequence num
        eg: generate_sequence('XXX001', 2)
            out: ['XXX001', 'XXX002']
    """
    if n == 1:
        return [r]
    # 提取前缀（不包含最后两个字符的其余部分）
    prefix = r[:-2]
    # 提取最后两位数字并转换为整数
    last_two_digits = int(r[-2:])
    # 生成范围内的序列列表
    sequence = [f"{prefix}{str(i).zfill(2)}" for i in range(last_two_digits, n+1)]
    # 生成最终的字符串，格式为 '开始-结束'
    # return f"{r}-{sequence[-1]}"
    return sequence


def sql_column_get(column):
    column_list = column.split('.')
    if len(column_list) == 1:
        return column_list[0]
    else:
        return column_list[1]


def format_msg(input_str):
    """
    根据输入字符串中的符号格式化消息。

    如果输入字符串以 '<' 或 '>' 开头，函数会提取数字部分，并根据符号返回一个范围列表。
    - 对于 '<'，返回从数字减去30到数字的范围（不包括数字本身）。
    - 对于 '>'，返回从数字到数字加上30的范围（不包括数字本身）。
    如果输入字符串没有以 '<' 或 '>' 开头，则直接返回输入字符串作为列表的元素。

    参数:
    input_str (str): 需要格式化的输入字符串。

    返回:
    list: 格式化后的消息列表。
    """
    if any(char in input_str for char in ['<', '>']):
        # 提取符号和数字部分
        symbol = input_str[0]
        number = int(input_str[1:])

        # 使用字典映射符号对应的范围
        range_map = {
            '<': range(number - 30, number),
            '>': range(number, number + 30)
        }

        # 根据符号返回对应的范围列表
        return list(range_map.get(symbol, []))
    else:
        # 如果输入字符串没有特定符号，则直接返回输入字符串作为列表元素
        return [input_str]
