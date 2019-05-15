
class GenerateResponseMessage():

    def __init__(self, message):
        self.user_message = message

    def generate_response(self):
        """ユーザーからの発話をオウム返しで返す
        """
        if not self.user_message:
            return
        return f"オオム返し {self.user_message}"
