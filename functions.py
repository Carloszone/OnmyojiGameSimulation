# !/usr/bin/python
# -*- coding: utf-8  -*-
# 模拟过程中需要使用的函数


import numpy as np


# 模拟概率
def possibility(input_rate: float):
    return np.random.rand() < input_rate


# 根据id查找式神对应信息
def search_hero_info(input_hero_pool, input_obj_type, input_obj_id):
    # 调整参数的数据类型
    if type(input_hero_pool) != list:
        input_hero_pool = [input_hero_pool]
    if type(input_obj_id) == int:
        input_obj_id = [input_obj_id]

    # 查找对应的式神信息
    if input_obj_type == 'hero_id':
        for hero in input_hero_pool:
            if hero.id in input_obj_id:
                return hero
        raise ValueError(f'No such hero id: {input_obj_id}!')
    elif input_obj_type == 'item_id':
        for hero in input_hero_pool:
            if hero.item.id in input_obj_id:
                return hero.item
        return 0
    elif input_obj_type == 'state_id':
        intersection_sates = 0
        for hero in input_hero_pool:
            states = [state.id for state in hero.states]
            intersection_sates = list(set(states) & set(input_obj_id))
        if intersection_sates:
            return 1
        return 0


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