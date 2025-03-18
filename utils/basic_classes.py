from typing import Optional, Union
from abc import ABC, abstractmethod


class State(ABC):
    """
    状态的抽象类。
    name：str，状态的名称
    state_type：int，状态的类型: 1为增益状态，2为减益状态，3为其他特殊状态
    state_kind: int: 状态的种类， 1为状态，2为印记，3为御魂效果，4为场地效果，5为其他特殊效果
    level：int，状态的等级, 默认为None(仅“毒”状态为数值)
    removable：bool，状态是否可以被解除
    dispellable：bool，状态是否可以被驱散
    duration：int，状态的持续时间, 默认为None(永久状态)。无法为负数，为零时状态不生效
    attribute：str，状态作用的属性, 默认为None(无关联属性，常见于各种控制效果)
    value：int or float，状态作用的数值
    count：int，状态的层数
    trigger_moment: list[int], 状态触发的时机
    source: Character，状态的来源
    end_character: Character，状态自然结算的参考对象： self or self.source. 基于此对象对状态层数进行结算。
    如果为self，则自身回合结束后，状态层数减一；如果为self.source，则状态来源的回合结束后，状态层数减一
    """

    def __init__(self, name: str,
                 state_type: int,
                 state_kind: int,
                 level: Optional[int] = None,
                 removable: bool = True,
                 dispellable: bool = True,
                 duration: Optional[int] = None,
                 attribute: Optional[str] = None,
                 value: Union[int, float, None] = None,
                 source: Optional["Character"] = None,
                 count: Optional[int] = None,
                 trigger_moment: Optional[list[int]] = None):
        self.name = name
        self.type = state_type
        self.kind = state_kind
        self.level = level
        self.removable = removable
        self.dispellable = dispellable
        self.duration = duration
        self.linked_attribute = attribute
        self.value = value
        self.source = source
        self.count = count
        self.trigger_moment = trigger_moment

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """
        触发状态效果
        """
        pass

    @abstractmethod
    def subscribe(self, *args, **kwargs):
        """
        订阅事件触发器
        """
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        """
        状态更新
        """
        pass

    def fade(self, *args, **kwargs):
        """
        状态消退
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
                 activate: bool = True,
                 duration: Optional[int] = None,
                 attribute: Optional[str] = None,
                 value: Union[int, float, None] = None):
        self.name = name
        self.activate = activate
        self.duration = duration
        self.attribute = attribute
        self.value = value

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """
        结算御魂效果的抽象类
        """
        pass


class Env(ABC):
    """
    结界/幻境等场地效果的抽象类
    name：str，场地效果的名称
    duration：int，场地效果的持续时间
    """

    def __init__(self, name: str, duration: int):
        self.name = name
        self.duration = 1

    def get_effect(self, *args, **kwargs) -> list:
        """
        获取并返回场地效果
        """
        pass

    @abstractmethod
    def update(self):
        """
        结界/幻境的更新逻辑
        """
        pass


class Skill(ABC):
    """
    技能的抽象类.
    name: str, 技能的名称
    skill_type: int, 技能的类型, 0为普通攻击, 1为主动技能, 2为被动技能
    cooldown: int, 技能的冷却时间
    cost: int, 技能的消耗
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


class Character(ABC):
    """
    Abstract class for characters
    """

    def __init__(self, name: str, health: Optional[int] = None, attack: Optional[int] = None,
                 defense: Optional[int] = None,
                 speed: Optional[int] = None, ct_rate: Optional[int] = None, ct_damage: Optional[int] = None,
                 effect_rate: Optional[int] = None, effect_resistance: Optional[int] = None,
                 states: Optional[list] = [],
                 available: Optional[bool] = True, attackable: Optional[bool] = True, location: Union[int, float] = 0):
        # basic attributes
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.critical_rate = ct_rate
        self.critical_damage = ct_damage
        self.effect_rate = effect_rate
        self.effect_resistance = effect_resistance
        self.states = states
        self.available = available
        self.attackable = attackable
        self.location = location
        self.current_name = None
        self.current_health = None
        self.current_max_health = None
        self.current_attack = None
        self.current_defense = None
        self.current_speed = None
        self.current_critical_rate = None
        self.current_critical_damage = None
        self.current_effect_rate = None
        self.current_effect_resistance = None
        self.current_states = None
        self.current_available = None
        self.current_attackable = None
        self.current_location = None

        # action related attributes
        self.time_to_act = None

        # battle related attributes
        self.critical_resistance = 0
        self.damage_multiplier = 1
        self.healing_multiplier = 1
        self.shell_multiplier = 1
        self.jump_multiplier = 1
        self.round = 0

        # character related attributes
        self.suffer_fatal_damage = False
        self.is_main_char = True
        self.is_empty = False
        self.linked_character = None

        # team related attributes
        self.team = None

    def update_attributes(self, *args, **kwargs):
        """
        Update the health of the character
        """
        pass

    def add_state(self, state: State):
        """
        Add state to the character
        """
        pass

    def update_state(self):
        """
        Update the state of the character
        """
        if isinstance(self.states, list):
            for state in self.states:
                state.update()

    def make_action_effect(self, *args, **kwargs):
        """
        Make action effect of the character
        """
        pass

    def take_action_effect(self, *args, **kwargs):
        """
        Take action effect of the character
        """
        pass

    def action(self, *args, **kwargs):
        """
        Action of the character
        """
        pass

    def trigger(self, *args, **kwargs):
        """
        Trigger of the character
        """
        pass


class Shikigami(Character):
    def __init__(self, name: str, health: Optional[int], attack: Optional[int], defense: Optional[int],
                 speed: Optional[int], ct_rate: Optional[int], ct_damage: Optional[int],
                 effect_rate: Optional[int], effect_resistance: Optional[int], states: Optional[list] = [],
                 available: Optional[bool] = True, attackable: Optional[bool] = True, location: Union[int, float] = 0):
        super().__init__(name, health, attack, defense, speed, ct_rate, ct_damage, effect_rate, effect_resistance,
                         states, available, attackable, location)
        self.spirit = None

    def update_attributes(self, global_effect, team_effect):
        # applying the global effect

        # apply the team effect

        # apply the state effect
        pass

    def add_spirit(self, spirit_name: str, spirit_cls: tuple):
        spirit_dict = {cls.__name__.lower(): cls for cls in spirit_cls}
        spirit = spirit_dict.get(spirit_name, None)
        if spirit:
            self.spirit = spirit()
        else:
            raise ValueError(f'无法找到御魂{spirit_name}的信息')

    @abstractmethod
    def skill_choice(self):
        """
        Choose the skill
        """
        pass


class Summon(Character):
    def __init__(self, name: str, health: Optional[int] = None, attack: Optional[int] = None,
                 defense: Optional[int] = None,
                 speed: Optional[int] = None, ct_rate: Optional[int] = None, ct_damage: Optional[int] = None,
                 effect_rate: Optional[int] = None, effect_resistance: Optional[int] = None,
                 states: Optional[list] = [],
                 available: Optional[bool] = True, attackable: Optional[bool] = True,
                 location: Union[int, float] = 0):
        super().__init__(name, health, attack, defense, speed, ct_rate, ct_damage, effect_rate, effect_resistance,
                         states, available, attackable, location)
        self.replace_target = None

    def replace_shikigami(self, target: Shikigami):
        self.replace_target = target

    @abstractmethod
    def __call__(self):
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

        if self.activate_with_power and (method == 'spirit' or method == 'wish'):
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
            if self.loop_count == 1:
                self.add_power(power_unit=3)
            elif self.loop_count == 2:
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
                if self.fake_power > 0:
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

    def add_member(self, member: Union[Shikigami, Summon]):
        """
        Add character to the team
        """
        self.members.append(member)
        member.team = self

    def add_env(self, env: Env):
        """
        Add env to the team
        """
        self.envs.append(env)

    def replace_member(self, target: Shikigami, new_member: Summon):
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

    def extract_env_info(self) -> list:
        """
        Update the team
        """
        env_effect = []
        for env in self.envs:
            env_effect += env.get_effect()

        return env_effect

    def trigger(self, stage_id):
        """
        Trigger of the team
        """
        for char in self.members:
            char.trigger(stage_id)

    def update_attributes(self, global_effect):
        """
        Update the attributes of the team
        """
        team_effect = self.extract_env_info()

        for char in self.members:
            char.update_attributes(global_effect, team_effect)


class Game:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def end(self):
        pass
