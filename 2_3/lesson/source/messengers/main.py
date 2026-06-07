from messengers.Telegram import Telegram
from messengers.WatsUp import WatsUp

messagers = [Telegram('Телеграмм'),WatsUp('WatsUp')]
for messager in messagers:
    messager.send_message()
    messager.get_message()
    print("*" * 50)