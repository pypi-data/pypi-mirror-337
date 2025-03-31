from dotenv import dotenv_values


class Dotenv:
    def __init__(self):
        self.config = dotenv_values(".env")


    def get(self, key_name: str):
        dotenv_value = self.config.get(key_name)

        if dotenv_value is None:
            print(f"🔴 key {key_name} in .env file isn't found!")
            return None

        elif "," in dotenv_value:
            dotenv_value = self.get_list(dotenv_value)

        return dotenv_value

    #? splits string intro array by "," and return stripped strings 
    @staticmethod
    def get_list(data: str):
        return [item.strip() for item in data.split(",")]


#? for testing purposes
# Dotenv()
# print("🐍  config", self.config)
# print("🐍  mongoDB", self.get("MONGODB"))
# print("🐍  user_ids: ", self.get("USER_IDS"))
