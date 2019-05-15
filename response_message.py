
class GenerateResponseMessage():

    def __init__(self, message):
        self.user_message = message

    def generate_response(self):
        if not self.user_message:
            return
        return f"オオム返し {self.user_message}"
