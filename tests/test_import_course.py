import unittest
import tempfile
from pathlib import Path

from rmotr_curriculum_tools.units import (
    create_unit, generate_unit_directory_name, resolve_unit_order)

from base_tests import IOTestCase


class UnitDirectoryNameTestCases(unittest.TestCase):
    def test_unit_names_generation(self):
        self.assertEqual(
            generate_unit_directory_name('Python Introduction', 1),
            'unit-1-python-introduction')
        self.assertEqual(
            generate_unit_directory_name('Python', 1),
            'unit-1-python')

        self.assertEqual(
            generate_unit_directory_name('Python Introduction', 3),
            'unit-3-python-introduction')
        self.assertEqual(
            generate_unit_directory_name('Python', 3),
            'unit-3-python')

        self.assertEqual(
            generate_unit_directory_name('Python Introduction', 3, False),
            'unit-3')
        self.assertEqual(
            generate_unit_directory_name('Python', 3, False),
            'unit-3')


class UnitOrderTestCase(IOTestCase):
    def setUp(self):
        self.course_name = 'Advanced Python Programming'
        self.course_slug = 'advanced-python-programming'
        self.course_directory_path = Path(
            tempfile.mkdtemp(prefix=self.course_slug))

        # Preconditions
        self.assertDirectoryExists(self.course_directory_path)

    def tearDown(self):
        shutil.rmtree(str(self.course_directory_path.absolute()))

    def test_order_none_empty_course_returns_1(self):
        self.assertEqual(
            resolve_unit_order(self.course_directory_path, None), 1)

    def test_order_none_not_empty_course_returns_last(self):
        # Preconditions
        unit_1_path = (self.course_directory_path /
                       'unit-1-python-introduction')
        unit_1_path.mkdir()
        unit_2_path = (self.course_directory_path /
                       'unit-2-data-types')
        unit_2_path.mkdir()

        self.assertDirectoryExists(unit_1_path)
        self.assertDirectoryExists(unit_2_path)

        # Main test
        self.assertEqual(
            resolve_unit_order(self.course_directory_path, None), 3)

    def test_order_rearranges_other_units(self):
        # Preconditions
        unit_1_path = (self.course_directory_path /
                       'unit-1-python-introduction')
        unit_1_path.mkdir()
        unit_2_path = (self.course_directory_path /
                       'unit-2-data-types')
        unit_2_path.mkdir()

        self.assertDirectoryExists(unit_1_path)
        self.assertDirectoryExists(unit_2_path)

        # Main test
        self.assertEqual(
            resolve_unit_order(self.course_directory_path, 2), 2)
        #
        # # Postconditions
        # self.assertDirectoryExists(
        #     (self.course_directory_path / 'unit-1-python-introduction'))
        # self.assertDirectoryExists(
        #     (self.course_directory_path / 'unit-1-python-introduction'))


class CreateUnitTestCase(IOTestCase):
    def setUp(self):
        self.course_name = 'Advanced Python Programming'
        self.course_slug = 'advanced-python-programming'
        self.course_directory_path = Path(
            tempfile.mkdtemp(prefix=self.course_slug))

        # Preconditions
        self.assertDirectoryExists(self.course_directory_path)

    def tearDown(self):
        shutil.rmtree(str(self.course_directory_path.absolute()))

    def test_create_unit_to_empty_course_order_default(self):
        """Should create unit with Order 1 if course is empty"""
        create_unit(self.course_directory_path, 'Python Introduction')
        unit_path = self.course_directory_path / 'unit-1-python-introduction'
        self.assertDirectoryExists(unit_path)

        dot_rmotr_path = unit_path / '.rmotr'
        self.assertFileExists(dot_rmotr_path)
        with dot_rmotr_path.open() as fp:
            dot_rmotr_contents = toml.loads(fp.read())

        self.assertTrue('uuid' in dot_rmotr_contents)
        self.assertTrue('name' in dot_rmotr_contents)
        self.assertEqual(dot_rmotr_contents['name'], 'Python Introduction')

    def test_create_unit_to_not_empty_course_appends_at_end(self):
        """Should create unit with Order 1 if course is empty"""
        # Preconditions
        self.unit_1_path = (self.course_directory_path /
                            'unit-1-python-introduction')
        self.unit_1_path.mkdir()
        self.assertDirectoryExists(self.unit_1_path)
        create_unit(self.course_directory_path, 'Data Types')

        unit_path = self.course_directory_path / 'unit-2-data-types'
        self.assertDirectoryExists(unit_path)

        # Main test
        dot_rmotr_path = unit_path / '.rmotr'
        self.assertFileExists(dot_rmotr_path)
        with dot_rmotr_path.open() as fp:
            dot_rmotr_contents = toml.loads(fp.read())

        self.assertTrue('uuid' in dot_rmotr_contents)
        self.assertTrue('name' in dot_rmotr_contents)
        self.assertEqual(dot_rmotr_contents['name'], 'Data Types')
