from data.env import SUPER_ADMIN_ID
from bot.Bot import Bot

bot = Bot()

super_admin_messages = ["Привет, Дамир!\nБот запущен!"]
admin_messages = ["Привет, админ!\nБот запущен!"]
# bot._send_messages(chat_id=SUPER_ADMIN_ID, messages=messages)
bot.tell_super_admin(super_admin_messages)

not_formatted_messages = ["Привет, {}", "Я - бот-помощник {}!"]
format_variables = ["Юзер", "Дамира"]
# bot.tell_admins(admin_messages)

bot.start_bot()

# bot._send_messages(
#     chat_id=SUPER_ADMIN_ID,
#     messages=not_formatted_messages,
#     format_variables=format_variables,
# )