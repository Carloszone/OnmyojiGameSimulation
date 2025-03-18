from utils.basic_classes import State
from dataclasses import dataclass, field


class JudgeState(State):
    def __call__(self):
        pass

    def update(self):
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