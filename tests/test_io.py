import unittest
from pathlib import Path
import tempfile
import shutil
import pytoml as toml

from base_tests import IOTestCase
from rmotr_curriculum_tools import io


class BaseIOTestCase(IOTestCase):
    def _create_testing_unit(self, name, slug, uuid):
        unit_path = self.course_directory_path / slug
        unit_path.mkdir()
        unit_dot_rmotr_path = unit_path / '.rmotr'
        with unit_dot_rmotr_path.open('w') as fp:
            fp.write("""
uuid = "{uuid}"
name = "{name}"
""".format(uuid=uuid, name=name))
        return unit_path

    def _create_testing_lesson(self, unit_path, name, slug,
                               uuid, readme_content, lesson_type):
        lesson_path = unit_path / slug
        lesson_path.mkdir()
        dot_rmotr_path = lesson_path / '.rmotr'
        with dot_rmotr_path.open('w') as fp:
            fp.write("""
uuid = "{uuid}"
name = "{name}"
type = "{lesson_type}"
""".format(uuid=uuid, name=name, lesson_type=lesson_type))

        readme_path = lesson_path / 'README.md'
        with readme_path.open('w') as fp:
            fp.write(readme_content)

        return lesson_path

    def _create_testing_reading_lesson(self, unit_path, name, slug,
                                       uuid, readme_content):
        return self._create_testing_lesson(
            unit_path, name, slug, uuid, readme_content, 'reading')

    def _create_testing_assignment_lesson(self, unit_path, name, slug, uuid,
                                          readme_content, main_content,
                                          test_content):
        lesson_path = self._create_testing_lesson(
            unit_path, name, slug, uuid, readme_content, 'assignment')

        main_path = lesson_path / 'main.py'
        with main_path.open('w') as fp:
            fp.write(main_content)

        tests_path = lesson_path / 'tests.py'
        with tests_path.open('w') as fp:
            fp.write(test_content)

        return lesson_path


class ReadCourseFromDiskTestCase(BaseIOTestCase):
    def setUp(self):
        self.course_name = 'Advanced Python Programming'
        self.course_slug = 'advanced-python-programming'
        self.course_directory_path = Path(
            tempfile.mkdtemp(prefix=self.course_slug))

        dot_rmotr_path = self.course_directory_path / '.rmotr'
        with dot_rmotr_path.open(mode='w') as fp:
            fp.write("""
uuid = "a7c2574a-a28b-4b19-bb64-c1feaa05dd52"
name = "Advanced Python Programming"
track = "python"
""")

        # Preconditions
        self.assertDirectoryExists(self.course_directory_path)

    def tearDown(self):
        shutil.rmtree(str(self.course_directory_path.absolute()))

    def test_read_empty_course(self):
        course = io.read_course_from_path(self.course_directory_path)

        self.assertEqual(course.directory_path, self.course_directory_path)
        self.assertEqual(course.uuid, "a7c2574a-a28b-4b19-bb64-c1feaa05dd52")
        self.assertEqual(course.name, "Advanced Python Programming")
        self.assertEqual(course.track, 'python')

    def test_read_course_with_one_unit(self):
        unit_1_path = self._create_testing_unit(
            'Python Introduction', 'unit-1-python-introduction',
            'f4ed574a-a11b-4119-bb64-c1feaa05ea55')

        course = io.read_course_from_path(self.course_directory_path)

        self.assertEqual(course.directory_path, self.course_directory_path)
        self.assertEqual(course.uuid, "a7c2574a-a28b-4b19-bb64-c1feaa05dd52")
        self.assertEqual(course.name, "Advanced Python Programming")
        self.assertEqual(course.track, 'python')

        self.assertEqual(course.unit_count(), 1)
        units_iter = course.iter_units()
        unit_1 = next(units_iter)

        self.assertEqual(unit_1.course, course)
        self.assertEqual(unit_1.name, 'Python Introduction')
        self.assertEqual(unit_1.uuid, 'f4ed574a-a11b-4119-bb64-c1feaa05ea55')
        self.assertEqual(unit_1.order, 1)

    def test_read_course_with_multiple_units(self):
        unit_1_path = self._create_testing_unit(
            'Python Introduction', 'unit-1-python-introduction',
            'f4ed574a-a11b-4119-bb64-c1feaa05ea55')
        unit_2_path = self._create_testing_unit(
            'Data types', 'unit-2-data-types',
            '9f34bcd6-cf83-4cd4-983a-9f36c733b29c')

        course = io.read_course_from_path(self.course_directory_path)

        self.assertEqual(course.directory_path, self.course_directory_path)
        self.assertEqual(course.uuid, "a7c2574a-a28b-4b19-bb64-c1feaa05dd52")
        self.assertEqual(course.name, "Advanced Python Programming")
        self.assertEqual(course.track, 'python')

        self.assertEqual(course.unit_count(), 2)
        units_iter = course.iter_units()
        unit_1 = next(units_iter)

        self.assertEqual(unit_1.course, course)
        self.assertEqual(unit_1.name, 'Python Introduction')
        self.assertEqual(unit_1.uuid, 'f4ed574a-a11b-4119-bb64-c1feaa05ea55')
        self.assertEqual(
            unit_1.directory_path,
            course.directory_path / 'unit-1-python-introduction')
        self.assertEqual(unit_1.order, 1)

        unit_2 = next(units_iter)

        self.assertEqual(unit_2.course, course)
        self.assertEqual(unit_2.name, 'Data types')
        self.assertEqual(unit_2.uuid, '9f34bcd6-cf83-4cd4-983a-9f36c733b29c')
        self.assertEqual(
            unit_2.directory_path,
            course.directory_path / 'unit-2-data-types')
        self.assertEqual(unit_2.order, 2)

    def test_read_course_with_one_unit_and_one_reading_lesson(self):
        unit_1_path = self._create_testing_unit(
            'Python Introduction', 'unit-1-python-introduction',
            'f4ed574a-a11b-4119-bb64-c1feaa05ea55')

        self._create_testing_reading_lesson(
            unit_1_path, 'Basic Data Types', 'lesson-1-basic-data-types',
            '0d900c98-935c-4f00-aa4d-cb626409e756',
            """ # Basic Data types
Numbers, strings, booleans""")

        course = io.read_course_from_path(self.course_directory_path)

        self.assertEqual(course.directory_path, self.course_directory_path)
        self.assertEqual(course.uuid, "a7c2574a-a28b-4b19-bb64-c1feaa05dd52")
        self.assertEqual(course.name, "Advanced Python Programming")
        self.assertEqual(course.track, 'python')

        self.assertEqual(course.unit_count(), 1)
        units_iter = course.iter_units()
        unit_1 = next(units_iter)

        self.assertEqual(unit_1.course, course)
        self.assertEqual(unit_1.name, 'Python Introduction')
        self.assertEqual(unit_1.uuid, 'f4ed574a-a11b-4119-bb64-c1feaa05ea55')
        self.assertEqual(unit_1.order, 1)

        self.assertEqual(unit_1.lesson_count(), 1)
        lessons_iter = unit_1.iter_lessons()
        lesson_1 = next(lessons_iter)

        self.assertEqual(lesson_1.name, 'Basic Data Types')
        self.assertEqual(lesson_1.slug, 'lesson-1-basic-data-types')
        self.assertEqual(lesson_1.order, 1)
        self.assertEqual(lesson_1.uuid, '0d900c98-935c-4f00-aa4d-cb626409e756')

    def test_read_course_with_one_unit_and_multiple_lesson(self):
        unit_1_path = self._create_testing_unit(
            'Python Introduction', 'unit-1-python-introduction',
            'f4ed574a-a11b-4119-bb64-c1feaa05ea55')

        self._create_testing_reading_lesson(
            unit_1_path, 'Basic Data Types', 'lesson-1-basic-data-types',
            '0d900c98-935c-4f00-aa4d-cb626409e756',
            """ # Basic Data types
Numbers, strings, booleans""")

        self._create_testing_assignment_lesson(
            unit_1_path, 'Simple assignment', 'lesson-2-simple-assignment',
            'd4500b25-151e-4e5d-9fc1-83feca938c3e',
            """ # Simple Assignment
This is the assignment description""",
            """def main():
    pass""",
            """def test_main():
    assert True""")

        course = io.read_course_from_path(self.course_directory_path)

        self.assertEqual(course.directory_path, self.course_directory_path)
        self.assertEqual(course.uuid, "a7c2574a-a28b-4b19-bb64-c1feaa05dd52")
        self.assertEqual(course.name, "Advanced Python Programming")
        self.assertEqual(course.track, 'python')

        self.assertEqual(course.unit_count(), 1)
        units_iter = course.iter_units()
        unit_1 = next(units_iter)

        self.assertEqual(unit_1.course, course)
        self.assertEqual(unit_1.name, 'Python Introduction')
        self.assertEqual(unit_1.uuid, 'f4ed574a-a11b-4119-bb64-c1feaa05ea55')
        self.assertEqual(unit_1.order, 1)

        self.assertEqual(unit_1.lesson_count(), 2)

        lessons_iter = unit_1.iter_lessons()
        lesson_1 = next(lessons_iter)

        self.assertEqual(lesson_1.name, 'Basic Data Types')
        self.assertEqual(lesson_1.slug, 'lesson-1-basic-data-types')
        self.assertEqual(lesson_1.order, 1)
        self.assertEqual(lesson_1.type, 'reading')
        self.assertEqual(lesson_1.uuid, '0d900c98-935c-4f00-aa4d-cb626409e756')

        lesson_2 = next(lessons_iter)

        self.assertEqual(lesson_2.name, 'Simple assignment')
        self.assertEqual(lesson_2.slug, 'lesson-2-simple-assignment')
        self.assertEqual(lesson_2.order, 2)
        self.assertEqual(lesson_2.type, 'assignment')
        self.assertEqual(lesson_2.uuid, 'd4500b25-151e-4e5d-9fc1-83feca938c3e')


class AddUnitToCourseTestCase(BaseIOTestCase):
    def setUp(self):
        self.course_name = 'Advanced Python Programming'
        self.course_slug = 'advanced-python-programming'
        self.course_directory_path = Path(
            tempfile.mkdtemp(prefix=self.course_slug))

        dot_rmotr_path = self.course_directory_path / '.rmotr'
        with dot_rmotr_path.open(mode='w') as fp:
            fp.write("""
uuid = "a7c2574a-a28b-4b19-bb64-c1feaa05dd52"
name = "Advanced Python Programming"
track = "python"
""")

        # Preconditions
        self.assertDirectoryExists(self.course_directory_path)

    def tearDown(self):
        shutil.rmtree(str(self.course_directory_path.absolute()))

    def test_add_unit_to_empty_course(self):
        generated_unit_path = io.add_unit_to_course(
            course_directory_path=self.course_directory_path,
            name='Python Intro')

        unit_path = self.course_directory_path / 'unit-1-python-intro'
        dot_rmotr_path = unit_path / '.rmotr'

        self.assertEqual(generated_unit_path, unit_path)
        self.assertDirectoryExists(unit_path)
        self.assertFileExists(dot_rmotr_path)

        with dot_rmotr_path.open() as fp:
            dot_rmotr_content = toml.loads(fp.read())
            self.assertTrue('uuid' in dot_rmotr_content)
            self.assertEqual(dot_rmotr_content['name'], 'Python Intro')

    def test_add_unit_to_not_empty_course_at_end(self):
        self._create_testing_unit(
            "Python Intro", 'unit-1-python-intro',
            'f4ed574a-a11b-4119-bb64-c1feaa05ea55')

        unit_1_path = self.course_directory_path / 'unit-1-python-intro'
        self.assertDirectoryExists(unit_1_path)

        add_unit_to_course(
            course_directory_path=self.course_directory_path,
            name='Data Types')

        unit_path = self.course_directory_path / 'unit-2-data-types'
        dot_rmotr_path = unit_path / '.rmotr'

        self.assertDirectoryExists(unit_path)
        self.assertFileExists(dot_rmotr_path)

        with dot_rmotr_path.open() as fp:
            dot_rmotr_content = toml.loads(fp.read())
            self.assertTrue('uuid' in dot_rmotr_content)
            self.assertEqual(dot_rmotr_content['name'], 'Data Types')

    def test_add_unit_to_in_between_other_units(self):
        self._create_testing_unit(
            "Python Intro", 'unit-1-python-intro',
            'f4ed574a-a11b-4119-bb64-c1feaa05ea55')
        self._create_testing_unit(
            "Data Types", 'unit-2-data-types',
            '8a22574a-a11b-4119-a964-c1feaa05c833')
        self._create_testing_unit(
            "Collections", 'unit-3-collections',
            'c822574a-a81b-4aa9-a964-c1feaa05a7b2')

        unit_1_path = self.course_directory_path / 'unit-1-python-intro'
        self.assertDirectoryExists(unit_1_path)
        unit_2_path = self.course_directory_path / 'unit-2-data-types'
        self.assertDirectoryExists(unit_2_path)
        unit_3_path = self.course_directory_path / 'unit-3-collections'
        self.assertDirectoryExists(unit_3_path)

        add_unit_to_course(
            course_directory_path=self.course_directory_path,
            name='Interpreters', order=2)

        unit_path = self.course_directory_path / 'unit-2-interpreters'
        dot_rmotr_path = unit_path / '.rmotr'

        self.assertDirectoryExists(unit_path)
        self.assertFileExists(dot_rmotr_path)

        with dot_rmotr_path.open() as fp:
            dot_rmotr_content = toml.loads(fp.read())
            self.assertTrue('uuid' in dot_rmotr_content)
            self.assertEqual(dot_rmotr_content['name'], 'Interpreters')

        # Postconditions
        unit_1_path = self.course_directory_path / 'unit-1-python-intro'
        self.assertDirectoryExists(unit_1_path)
        unit_3_path = self.course_directory_path / 'unit-3-data-types'
        self.assertDirectoryExists(unit_3_path)
        unit_4_path = self.course_directory_path / 'unit-4-collections'
        self.assertDirectoryExists(unit_4_path)
