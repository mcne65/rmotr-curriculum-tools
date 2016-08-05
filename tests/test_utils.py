import unittest
from rmotr_curriculum_tools.utils import (
    slugify, get_order_from_numbered_object_directory_name,
    generate_lesson_dot_rmotr_file)
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


class GenerateLessonDotRmotrTestCase(unittest.TestCase):
    def test_generate_lesson_dot_rmotr_file_reading_lesson(self):
        dot_rmotr = generate_lesson_dot_rmotr_file(
            name="Demo lesson", _type="reading",
            uuid='1ced4cef-8137-4a8a-a259-61c994a9cacb')
        self.assertEqual(
            dot_rmotr,
"""type = "reading"
uuid = "1ced4cef-8137-4a8a-a259-61c994a9cacb"
name = "Demo lesson"
"""
        )

    def test_generate_lesson_dot_rmotr_file_assignment_lesson(self):
        dot_rmotr = generate_lesson_dot_rmotr_file(
            name="Demo lesson", _type="assignment",
            uuid='1ced4cef-8137-4a8a-a259-61c994a9cacb')
        self.assertEqual(
            dot_rmotr,
"""type = "assignment"
uuid = "1ced4cef-8137-4a8a-a259-61c994a9cacb"
name = "Demo lesson"
"""
        )

    def test_generate_lesson_dot_rmotr_file_external_assignment_lesson(self):
        dot_rmotr = generate_lesson_dot_rmotr_file(
            name="Demo lesson", _type="external_assignment",
            uuid='1ced4cef-8137-4a8a-a259-61c994a9cacb',
            repo='https://github.com/rmotr-individual-assignments/pyp-test-assignment')
        self.assertEqual(
            dot_rmotr,
"""assignment_repo_name = "pyp-test-assignment"
type = "external_assignment"
uuid = "1ced4cef-8137-4a8a-a259-61c994a9cacb"
assignment_repo_org = "rmotr-individual-assignments"
name = "Demo lesson"
"""
        )


class SlugifyTestCase(unittest.TestCase):
    def test_slugs(self):
        self.assertEqual(
            slugify('Advanced Python Programming'),
            'advanced-python-programming')
