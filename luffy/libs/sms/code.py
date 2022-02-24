import random


# 生成4，或5位的验证码
def gen_code(length=4):
    code_str = ''
    for i in range(length):
        code_str += str(random.randrange(0, 9))  # python 是动态强类型，所以需要转换

    return code_str
