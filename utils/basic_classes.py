from typing import Optional, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


class State(ABC):
    """
    状态的抽象类。
    name：str，状态的名称
    duration：int，状态的持续时间
    attribute：str，状态作用的属性
    value：int or float，状态作用的数值
    """

    def __init__(self, name: str,
                 duration: Optional[int] = None,
                 attribute: Optional[str] = None,
                 value: Union[int, float, None] = None):
        self.name = name
        self.duration = duration
        self.attribute = attribute
        self.value = value

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """
        结算状态效果
        """
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        """
        状态更新
        """
        pass


class Spirit(ABC):
    """
    御魂效果的抽象类，部分御魂效果的实现实质上是为式神添加对应的状态，因此初始化时需要传入状态相关的参数
    name：str，御魂的名称
    duration：int，御魂效果的持续时间
    attribute：str，御魂效果作用的属性
    value：int or float，御魂效果作用的数值
    """

    def __init__(self, name: str,
                 duration: Optional[int] = None,
                 attribute: Optional[str] = None,
                 value: Union[int, float, None] = None):
        self.name = name
        self.duration = duration
        self.attribute = attribute
        self.value = value

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """
        Call the spirit
        """
        pass


class Env(ABC):
    """
    结界/幻境等场地效果的抽象类
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """
        Call the environment
        """
        return None

    @abstractmethod
    def update(self):
        """
        Update the environment
        """
        pass


class Skill(ABC):
    """
    Abstract class for skills
    """

    def __init__(self, name: str, skill_type: int, cooldown: int, cost: int = 0):
        self.name = name
        self.skill_type = skill_type
        self.cooldown = cooldown
        self.cost = cost

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """
        Call the skill
        """
        pass

    def negative_effect(self):
        """
        Negative effect of the skill
        """
        pass


@dataclass
class CategoryInfo:
    state_list: list[str] = field(
        default_factory=lambda: [],
        metadata={'help': '状态名称列表'}
    )
    sign_list: list[str] = field(
        default_factory=lambda: [],
        metadata={'help': '印记名称列表'}
    )
    general_power: list[str] = field(
        default_factory=lambda: [],
        metadata={'help': '印记名称列表'}
    )
    unable_action: list[str] = field(
        default_factory=lambda: [],
        metadata={'help': '无法行动的状态名称列表'}
    )
    unable_clear: list[str] = field(
        default_factory=lambda: [],
        metadata={'help': '无法驱散的负面状态名称列表'}
    )
    unable_release: list[str] = field(
        default_factory=lambda: [],
        metadata={'help': '无法解除的状态名称列表'}
    )


class Character(ABC):
    """
    Abstract class for characters
    """
    def __init__(self, name: str, health: Optional[int], attack: Optional[int], defense: Optional[int],
                 speed: Optional[int], critical_rate: Optional[int], critical_damage: Optional[int],
                 effect_rate: Optional[int], effect_resistance: Optional[int], states: Optional[list]):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.critical_rate = critical_rate
        self.critical_damage = critical_damage
        self.effect_rate = effect_rate
        self.effect_resistance = effect_resistance
        self.states = states
        self.critical_resistance = 0
        self.damage_multiplier = 1
        self.healing_multiplier = 1
        self.shell_multiplier = 1

    def update_state(self):
        """
        Update the state of the character
        """
        if isinstance(self.states, list):
            for state in self.states:
                state.update()

    def update_attribute(self):
        """
        Update the health of the character
        """
        pass

    def add_state(self, state: State):
        """
        Add state to the character
        """
        pass

    def action(self):
        """
        Action of the character
        """
        pass


class Shikigami(Character):
    def __init__(self):
        super().__init__()
        pass

    @abstractmethod
    def skill_choice(self):
        """
        Choose the skill
        """
        pass


class Sumon(Character):
    def __init__(self):
        super().__init__()
        self.replace_target = None
        pass

    @abstractmethod
    def  __call__(self):
        pass


class PowerManager:
    """
    Abstract class for power manager
    """

    def __init__(self, init_power=4, max_power=8, with_power=0, max_with_power=8, fake_power=0):
        self.power = init_power
        self.max_power = max_power
        self.with_power = with_power
        self.max_with_power = max_with_power
        self.fake_power = fake_power
        self.loop_count = 1
        self.process_count = 1
        self.activate_with_power = False

    def add_power(self, power_unit=1, method='step'):
        """
        增加鬼火的函数。当发生需要增加鬼火的事件时（含义火和愿力），调用此函数
        输入参数：
        power_unit: int, 增加的鬼火数量
        method: str, 增加鬼火的方式，包括'step'（推进鬼火条），'fake'（增加义火），'spirit'（御魂效果），'skill'(技能效果)等
        输出参数：
        int, 溢出的鬼火数量
        """
        if method == 'fake':
            self.fake_power += min(power_unit, self.power)
            self.power = max(self.power - power_unit, 0)

        if activate_with_power and (method == 'spirit' or method == 'wish'):
            current_wish_power = self.with_power + power_unit
            self.with_power = min(current_wish_power, self.max_with_power)
            current_power = self.init_power + max(current_wish_power - self.max_with_power, 0)
        else:
            current_power = self.power + power_unit
            self.power = min(current_power, self.max_power)
        return current_power - self.max_power

    def step(self, step_unit=1):
        """
        模拟鬼火条推进的函数。在式神的回合开始前，鬼火条会推进，并在满足计数要求后获得鬼火
        """
        pass
        if self.process_count + step_unit <= 5:
            self.process_count += step_unit
        else:
            if loop_power == 1:
                self.add_power(power_unit=3)
            elif loop_power == 2:
                self.add_power(power_unit=4)
            else:
                self.add_power(power_unit=5)
            self.loop_count += 1
            self.process_count = self.process_count + step_unit - 5

    def consume_power(self, is_enemy=False, power_count=1) -> tuple[bool, bool, int]:
        """
        执行游戏中各种“扣除”鬼火机制的函数。
        “扣除”鬼火的机制包括但不限于：释放技能，木魅御魂，鬼金羊二技能等
        输入参数：
        is_enemy: bool, 是否是敌方触发的扣除效果
        power_count: int, 扣除的鬼火数量
        输出参数：
        tuple[是否扣除义火， 是否扣除愿力， 扣除的义火数量]
        """
        if is_enemy:
            self.power = max(self.power - power_count, 0)
            return False, False, 0
        else:
            if power_count <= self.fake_power + self.power + self.with_power:
                if fake_power > 0:
                    if power_count <= self.fake_power:
                        self.fake_power = self.fake_power - power_count
                        return True, False, power_count
                    elif power_count <= self.fake_power + self.power:
                        self.power = self.fake_power + self.power - power_count
                        return True, False, self.fake_power
                    else:
                        self.power = 0
                        self.with_power = self.fake_power + self.power + self.with_power - power_count
                        return True, True, self.fake_power
                else:
                    if power_count <= self.power:
                        self.power = self.power - power_count
                        return False, True, 0
                    else:
                        self.power = 0
                        self.with_power = self.with_power + self.power - power_count
                        return False, True, 0
            else:
                return False, False, 0


class Team:
    """
    Abstract class for teams
    """

    def __init__(self, name: str):
        self.name = name
        self.members = []
        self.envs = []
        self.power_manager = PowerManager()

    def add_member(self, member: Shikigami):
        """
        Add character to the team
        """
        self.members.append(member)

    def add_env(self, env: Env):
        """
        Add env to the team
        """
        self.envs.append(env)

    def replace_member(self, target: Shikigami, new_member: Sumon):
        """
        Replace the target with the Sumon
        """

        # get the index of the target
        member_index = 6
        target_member = self.members[6]
        for ind, member in enumerate(self.members):
            if member.name == target.name:
                member_index = ind
                target_member = member
                break

        # replace the target with the new member
        new_member.replace_target = target_member
        self.members[member_index] = new_member

    def search_member(self, attribute: str) -> list[tuple[int, Union[int, str, list]]]:
        """
        extract specific attribute info(index, value) from the team and sort them
        """
        # create a list of tuples(index, value) for non-None attribute
        indexed_attribute_list = [(ind, getattr(member, attribute, None)) for ind, member in enumerate(self.members) if
                                  getattr(member, attribute, None) is not None]

        # sort the list by the value
        sorted_indexed_attribute_list = sorted(indexed_attribute_list, key=lambda x: x[1])
        return sorted_indexed_attribute_list

    def extract_env_info(self) -> dict:
        """
        Update the team
        """
        env_info = {}
        for env in self.envs:
            if env.linked_attribute is not None:
                for attribute_name, attribute_value in env.attribute_info:
                    if attribute_name not in env_info.keys():
                        env_info[attribute_name] = [attribute_value]
                    else:
                        env_info[attribute_name].append(attribute_value)
        return env_info
