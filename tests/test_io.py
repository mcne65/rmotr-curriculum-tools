import unittest
from pathlib import Path
import tempfile
import shutil

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

from rmotr_curriculum_tools.models import *


class WriteCourseToDiskTestCase(BaseIOTestCase):
    def setUp(self):
        self.course_uuid = 'a7c2574a-a28b-4b19-bb64-c1feaa05dd52'
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

        self.course = Course(
            directory_path=self.course_directory_path,
            uuid=self.course_uuid,
            name=self.course_name,
            track='python'
        )

    def tearDown(self):
        shutil.rmtree(str(self.course_directory_path.absolute()))

    def test_flush_new_reading_lesson_creates_it_correctly(self):
        unit_1_path = self._create_testing_unit(
            'Python Introduction', 'unit-1-python-introduction',
            'f4ed574a-a11b-4119-bb64-c1feaa05ea55')

        unit = Unit(
            course=self.course,
            directory_path=unit_1_path,
            uuid='f4ed574a-a11b-4119-bb64-c1feaa05ea55',
            name="Python Introduction",
            order=1
        )
        self.course.add_unit(unit)

        lesson = ReadingLesson(
            unit=unit,
            uuid='0d900c98-935c-4f00-aa4d-cb626409e756',
            name='Python intro',
            order=1
        )
        self.assertFalse(lesson.is_created)

        io.flush_lesson(lesson)

        lesson_path = unit_1_path / 'lesson-1-python-intro'
        dot_rmotr_path = lesson_path / '.rmotr'

        self.assertDirectoryExists(lesson_path)
        self.assertFileExists(dot_rmotr_path)

        with dot_rmotr_path.open() as fp:
            dot_rmotr_content = toml.loads(fp.read())
            self.assertEqual(
                dot_rmotr_content,
                {
                    'uuid': '0d900c98-935c-4f00-aa4d-cb626409e756',
                    'name': 'Python intro',
                    'type': 'reading'
                }
            )

        self.assertFileExists(lesson_path / 'README.md')

    def test_flush_lessons_with_unit_not_empty(self):
        unit_1_path = self._create_testing_unit(
            'Python Introduction', 'unit-1-python-introduction',
            'f4ed574a-a11b-4119-bb64-c1feaa05ea55')

        lesson_1_path = self._create_testing_assignment_lesson(
            unit_1_path, 'Python intro', 'leson-1-python-intro',
            '0d900c98-935c-4f00-aa4d-cb626409e756',
            "README", "# main.py", "# tests.py"
        )

        unit = Unit(
            course=self.course,
            directory_path=unit_1_path,
            uuid='f4ed574a-a11b-4119-bb64-c1feaa05ea55',
            name="Python Introduction",
            order=1
        )
        self.course.add_unit(unit)

        lesson = AssignmentLesson(
            unit=unit,
            uuid='22c10c98-935c-4f00-c8ad-cb6264097d9a',
            name='Data Types',
            order=2
        )
        self.assertFalse(lesson.is_created)

        io.flush_lesson(lesson)

        lesson_path = unit_1_path / 'lesson-2-data-types'
        dot_rmotr_path = lesson_path / '.rmotr'

        self.assertDirectoryExists(lesson_path)
        self.assertFileExists(dot_rmotr_path)

        with dot_rmotr_path.open() as fp:
            dot_rmotr_content = toml.loads(fp.read())
            self.assertEqual(
                dot_rmotr_content,
                {
                    'uuid': '22c10c98-935c-4f00-c8ad-cb6264097d9a',
                    'name': 'Data Types',
                    'type': 'assignment'
                }
            )

        self.assertFileExists(lesson_path / 'main.py')
        self.assertFileExists(lesson_path / 'README.md')
        self.assertFileExists(lesson_path / 'tests.py')

    def test_flush_multiple_new_lessons(self):
        unit_1_path = self._create_testing_unit(
            'Python Introduction', 'unit-1-python-introduction',
            'f4ed574a-a11b-4119-bb64-c1feaa05ea55')

        unit = Unit(
            course=self.course,
            directory_path=unit_1_path,
            uuid='f4ed574a-a11b-4119-bb64-c1feaa05ea55',
            name="Python Introduction",
            order=1
        )
        self.course.add_unit(unit)

        lesson_1 = AssignmentLesson(
            unit=unit,
            uuid='0d900c98-935c-4f00-aa4d-cb626409e756',
            name='Python intro',
            order=1
        )

        lesson_2 = AssignmentLesson(
            unit=unit,
            uuid='22c10c98-935c-4f00-c8ad-cb6264097d9a',
            name='Data Types',
            order=2
        )
        unit.add_lesson(lesson_1)
        unit.add_lesson(lesson_2)

        self.assertFalse(lesson_1.is_created)
        self.assertFalse(lesson_2.is_created)

        io.flush_unit(unit)

        # Unit 2
        lesson_path = unit_1_path / 'lesson-2-data-types'
        dot_rmotr_path = lesson_path / '.rmotr'

        self.assertDirectoryExists(lesson_path)
        self.assertFileExists(dot_rmotr_path)

        with dot_rmotr_path.open() as fp:
            dot_rmotr_content = toml.loads(fp.read())
            self.assertEqual(
                dot_rmotr_content,
                {
                    'uuid': '22c10c98-935c-4f00-c8ad-cb6264097d9a',
                    'name': 'Data Types',
                    'type': 'assignment'
                }
            )

        self.assertFileExists(lesson_path / 'main.py')
        self.assertFileExists(lesson_path / 'README.md')
        self.assertFileExists(lesson_path / 'tests.py')

    def test_add_flush_unit(self):
        unit = Unit(
            course=self.course,
            uuid='f4ed574a-a11b-4119-bb64-c1feaa05ea55',
            name="Python Introduction",
            order=1
        )
        self.assertFalse(unit.is_created)

        io.flush_unit(unit)

        unit_path = self.course_directory_path / 'unit-1-python-introduction'
        dot_rmotr_path = unit_path / '.rmotr'

        self.assertDirectoryExists(unit_path)
        self.assertFileExists(dot_rmotr_path)

        with dot_rmotr_path.open() as fp:
            dot_rmotr_content = toml.loads(fp.read())
            self.assertEqual(
                dot_rmotr_content,
                {
                    'uuid': 'f4ed574a-a11b-4119-bb64-c1feaa05ea55',
                    'name': 'Python Introduction'
                }
            )

    def test_add_unit_at_the_end_with_empty_course(self):
        unit = Unit(
            course=self.course,
            uuid='f4ed574a-a11b-4119-bb64-c1feaa05ea55',
            name="Python Introduction",
            order=1
        )
        self.course.add_unit(unit)

        self.assertFalse(unit.is_created)

        io.flush_course(self.course)

        unit_path = self.course_directory_path / 'unit-1-python-introduction'
        dot_rmotr_path = unit_path / '.rmotr'

        self.assertDirectoryExists(unit_path)
        self.assertFileExists(dot_rmotr_path)

        with dot_rmotr_path.open() as fp:
            dot_rmotr_content = toml.loads(fp.read())
            self.assertEqual(
                dot_rmotr_content,
                {
                    'uuid': 'f4ed574a-a11b-4119-bb64-c1feaa05ea55',
                    'name': 'Python Introduction'
                }
            )


class RenameCourseToDiskTestCase(BaseIOTestCase):
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

        unit = Unit(
            course=course,
            uuid='f4ed574a-a11b-4119-bb64-c1feaa05ea55',
            name="Collections",
            order=3
        )
        course.add_unit(unit)
