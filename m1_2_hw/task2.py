"""
2. Спросите пользователя, идет ли дождь.
Преобразуйте его ответ к нижнему регистру.
Если пользователь ответит «yes», спросите, ветрено ли на улице.
Если пользователь ответит «yes» и на второй вопрос, выведите сообщение «It is too windy for an umbrella»;
в противном случае выведите сообщение «Take an umbrella».
Если же пользователь не дал положительного ответа на первый вопрос, выведите сообщение «Enjoy your day»
"""




if input("Идет ли дождь ? < yes|no >: ").lower()  == "yes":
    if input("Ветрено ли на улице ? < yes|no >: ").lower() == "yes":
        print("It is too windy for an umbrella")
    else:
        print("Take an umbrella")
else:
    print("Enjoy your day")
