from unittest import TestCase

from unit_test.AdminUsers import AdminUsers
from unit_test.User import User


class TestAdminUsers(TestCase):
    def setUp(self):
        """Метод запускается автоматически перед всеми тестами"""
        self.admin = AdminUsers()

    def test_add_user(self):
        count_users = len(self.admin.users)
        user = User('Вася')
        self.admin.add_user(user)
        self.assertEqual(len(self.admin.users), count_users + 1)

    def test_remove_user(self):
        user = User('Вася')
        self.admin.users.append(user)
        count_users = len(self.admin.users)
        self.admin.remove_user(user)
        self.assertEqual(len(self.admin.users), count_users - 1)

    def tearDown(self):
        """Метод запускается после всех тестов"""
        pass