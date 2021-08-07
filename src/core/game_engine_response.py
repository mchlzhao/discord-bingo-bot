class GameEngineResponse:
    def __init__(self, response: dict = None, *, display_error: str = None):
        self.response = response
        self.display_error = display_error
