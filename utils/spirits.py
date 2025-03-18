from basic_classes import Spirit

class PoShi(Spirit):
    def __call__(self, trigger_flag):
        if trigger_flag == '3':
            return 0.4
        else:
            return 0



