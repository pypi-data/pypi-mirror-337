from bridgepy.exception import BizException


class BridgeEnvGameNotReadyToStart(BizException):
    def __init__(self):
        super().__init__(11001, "Game not ready to start!")

class BridgeEnvGameInvalidAction(BizException):
    def __init__(self):
        super().__init__(11002, "Game invalid action!")

class BridgeEnvGameAlreadyTerminalState(BizException):
    def __init__(self):
        super().__init__(11003, "Game already terminal state!")
