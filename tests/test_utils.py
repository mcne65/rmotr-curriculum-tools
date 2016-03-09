import unittest
from rmotr_curriculum_tools.utils import (
    slugify, get_order_from_numbered_object_directory_name)
from rmotr_curriculum_tools.exceptions import InvalidUnitNameException


class UtilsTestCase(unittest.TestCase):
    def test_get_order_from_unit_dir_name(self):
        self.assertEqual(
            get_order_from_numbered_object_directory_name('unit-1-data-types'), 1)
        self.assertEqual(
            get_order_from_numbered_object_directory_name('unit-7-data-types'), 7)
        self.assertEqual(
            get_order_from_numbered_object_directory_name('unit-19-data-types'), 19)

        self.assertEqual(
            get_order_from_numbered_object_directory_name('unit-1'), 1)
        self.assertEqual(
            get_order_from_numbered_object_directory_name('unit-7'), 7)
        self.assertEqual(
            get_order_from_numbered_object_directory_name('unit-19'), 19)

        with self.assertRaises(InvalidUnitNameException):
            get_order_from_numbered_object_directory_name('unit-')

        with self.assertRaises(InvalidUnitNameException):
            get_order_from_numbered_object_directory_name('unit-a-something')


class SlugifyTestCase(unittest.TestCase):
    def test_slugs(self):
        self.assertEqual(
            slugify('Advanced Python Programming'),
            'advanced-python-programming')
