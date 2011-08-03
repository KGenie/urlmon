import unittest
from util import get_controller_class_name, is_authorized

class TestUtilFunctions(unittest.TestCase):

    def test_is_authorized(self):
        user_roles = ['moderator', 'normal']
        authorized_roles = ['moderator']
        denied_roles = []
        result = is_authorized(user_roles,authorized_roles,denied_roles)
        self.assertTrue(result)

        user_roles = ['admin', 'normal']
        authorized_roles = ['admin']
        denied_roles = ['*']
        result = is_authorized(user_roles,authorized_roles,denied_roles)
        self.assertFalse(result)

        user_roles = ['admin', 'moderator']
        authorized_roles = ['*']
        denied_roles = ['admin', 'moderator']
        result = is_authorized(user_roles,authorized_roles,denied_roles)
        self.assertFalse(result)

        user_roles = ['admin']
        authorized_roles = ['*']
        denied_roles = ['moderator']
        result = is_authorized(user_roles,authorized_roles,denied_roles)
        self.assertTrue(result)

        user_roles = ['normal']
        authorized_roles = ['admin', 'moderator']
        denied_roles = []
        result = is_authorized(user_roles,authorized_roles,denied_roles)
        self.assertFalse(result)
        

    def test_get_controller_class_name(self):
        name = get_controller_class_name('some_controller')
        self.assertEqual('SomeControllerController', name)
        name = get_controller_class_name('other-witH_daSHes-and-underscores')
        self.assertEqual('OtherWithDashesAndUnderscoresController', name)
        name = get_controller_class_name('simple')
        self.assertEqual('SimpleController', name)
