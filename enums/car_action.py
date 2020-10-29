from enum import Enum


class CAR_ACTION(Enum):
    FORWARD = 'FORWARD'
    BACKWARD = 'BACKWARD'

    def __repr__(self):
        return self.value

    def change_action(self):
        if self == CAR_ACTION.FORWARD:
            return CAR_ACTION.BACKWARD
        return CAR_ACTION.FORWARD