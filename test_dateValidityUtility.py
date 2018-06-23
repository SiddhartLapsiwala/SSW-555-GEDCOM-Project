from unittest import TestCase
from sprint1 import dateValidityUtility


class TestDateValidityUtility(TestCase):

    def setUp(self):
        pass

    def test_is_date1_greater_than_date2_success1(self):
        is_invalid_date = dateValidityUtility()
        self.assertEqual(is_invalid_date.is_date1_greater_than_date2(date1= '02 Dec 1991', date2= '01 Dec 1991'), True)

    def test_is_date1_greater_than_date2_success2(self):
        is_invalid_date = dateValidityUtility()
        self.assertEqual(is_invalid_date.is_date1_greater_than_date2(date1= '02 Dec 1991', date2= '17 Jan 1971'), True)

    def test_is_date1_less_than_date_failure1(self):
        is_invalid_date = dateValidityUtility()
        self.assertEqual(is_invalid_date.is_date1_greater_than_date2(date1='02 Dec 1991', date2='02 Dec 2011'), False)

    def test_is_date1_less_than_date_failure2(self):
        is_invalid_date = dateValidityUtility()
        self.assertEqual(is_invalid_date.is_date1_greater_than_date2(date1='02 Dec 1991', date2='30 Dec 2018'), False)
