from dotenv import dotenv_values


class Dotenv:
    def __init__(self):
        self.config = dotenv_values(".env")

        #? common variables
        self.environment = self.get("ENVIRONMENT")


    def get(self, key_name: str):
        dotenv_value = self.config.get(key_name)

        if dotenv_value is None:
            print(f"🔴 key {key_name} in .env file isn't found!")
            return None

        elif "," in dotenv_value:
            dotenv_value = self.get_list(dotenv_value, key_name)

        return dotenv_value

    #? splits string intro array by "," and return stripped strings 
    @staticmethod
    def get_list(data: str, key_name: str = None):
        items = [item.strip() for item in data.split(",")] 

        if "id" in key_name or "ID" in key_name:
            items = [int(item) for item in items]

        return items
