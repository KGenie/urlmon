import unittest
from util import get_controller_class_name, is_authorized, get_page_range

class TestUtilFunctions(unittest.TestCase):

    def test_get_page_range(self):
        total_pages = 12
        current_page = 5
        range_size = 5
        result = get_page_range(total_pages, current_page, range_size)
        self.assertEqual([3,4,5,6,7], result)

        total_pages = 12
        current_page = 6
        range_size = 6
        result = get_page_range(total_pages, current_page, range_size)
        self.assertEqual([4,5,6,7,8,9], result)

        total_pages = 3
        current_page = 1
        range_size = 5
        result = get_page_range(total_pages, current_page, range_size)
        self.assertEqual([1,2,3], result)

        total_pages = 3
        current_page = 3
        range_size = 5
        result = get_page_range(total_pages, current_page, range_size)
        self.assertEqual([1,2,3], result)

     
        


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
