from threading import Thread
from keyboard import add_hotkey
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from bot_engine.utils.Dotenv import Dotenv
from bot_engine.utils.Logger import Logger


#! Это просто заготовка класса сервера на FastAPI, который можно переиспользовать
#! Класс сервера можно написать самому, исходя из ваших нужд и выбранного вами сервера
class Server:
    def __init__(self):
        self.log = Logger().info
        self.dotenv = Dotenv()

        #! remove this after dotenv has .environment
        self.environment: str = self.dotenv.get("ENVIRONMENT")

        # self.time = Time()
        # self.bot = Bot()
        
        # threads 
        self.bot_thread = None
        self.listener_thread = None
        
        self.app = FastAPI(lifespan=self.start_server)
        
        
        
    @asynccontextmanager
    async def start_server(self, app: FastAPI):
        self.log("сервер FastAPI / uvicorn включён 👀")
        
        self.start_threads()

        try:
            yield  
        
        except KeyboardInterrupt:
            self.log("Manual shutdown triggered.")
        
        finally:
            self.shut_server_down()
            


    def start_threads(self):
        if self.environment == "development":
            self.start_ctrl_c_thread()

        # if self.environment == "production":
        #     self.time.set_scheduled_tasks()
        
        self.start_bot_thread()


    def start_bot_thread(self):
        pass
        # database = Database()
        # database.sync_cache_and_remote_users()

        # create days
        # database.mongoDB.ScheduleDays.check_days_integrity()
        
        # BotDialogs().enable_dialogs()
        
        # self.bot_thread = Thread(target=self.bot.start_bot)
        # self.bot_thread.start()
        

    def start_ctrl_c_thread(self):
        self.listener_thread = Thread(target=self.handle_ctrl_c)
        self.listener_thread.start()
        

    def handle_ctrl_c(self):
        add_hotkey("ctrl+c", self.shut_server_down)
        
        
    def shut_server_down(self):
        # self.bot.disconnect_bot()
        uvicorn.server.Server.should_exit = True
        
        if self.environment == "development":
            self.listener_thread.join()
            
        if self.environment == "production":
            self.time.scheduler.remove_all_jobs()
          
        # self.bot_thread.join()  
        self.log("Сервер выключен ❌")
        
