import numpy as np


# 模拟概率
def possibility(input_rate: float):
    return np.random.rand() < input_rate


# 根据id查找英雄
def serach_hero(input_hero_pool, input_id):
    for hero in input_hero_pool:
        if hero.id == input_id:
            return hero


# 自定义排序
def costume_sorted(input_obj):
    return (input_obj.category, input_obj.id)
    

# 属性检查与更新
def state_check(in_hero, in_state_code):
    # 提取对应的基础状态值
    hero_value = 1

    # 提取对应的状态值
    state_values = {}
    for state in in_hero.states:
        if in_state_code in state.category:
            key = state.group
            value = state.value if state.type == 0 else -state.value
            state_values.setdefault(key, []).append(value)

    # 计算最终状态值
    for value in state_values.values():
        if in_state_code in [20, 22]:
            hero_value *= 1/(1 + np.sum(value))
        else:
            hero_value *= (1 + np.sum(value))

    return hero_value