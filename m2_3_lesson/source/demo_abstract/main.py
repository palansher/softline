from demo_abstract.AdminPage import AdminPage
from demo_abstract.CommonPage import CommonPage
from demo_abstract.User import User

page1 = CommonPage("Главная", "Содержимое в разработке...")
page2 = CommonPage("Услуги", "Содержимое в разработке...")
page3 = CommonPage("Контакты", "Содержимое в разработке...")

page4 = AdminPage("Управление контентом", "Содержимое в разработке...")
page5 = AdminPage("Управление дизайном", "Содержимое в разработке...")
page6 = AdminPage("Управление пользователями", "Содержимое в разработке...")

pages = [page1,page2,page3,page4,page5,page6]

admin1 = User("admin","123")
admin2 = User("admin2","321")

User.add_admin(admin1)
User.add_admin(admin2)


user = User(input('Введите логин\n'),input('Введите пароль\n'))

for page in pages:
    if isinstance(page, AdminPage):
        if user.is_access():
            page.render()
    else:
        page.render()