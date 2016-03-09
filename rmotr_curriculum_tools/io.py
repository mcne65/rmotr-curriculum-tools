import pytoml as toml

from .models import *
from . import utils
from . import exceptions

UNIT_GLOB = 'unit-*'
LESSON_GLOB = 'lesson-*'
DOT_RMOTR_FILE_NAME = '.rmotr'
README_FILE_NAME = 'README.md'
MAIN_PY_NAME = 'main.py'
TEST_PY_NAME = 'tests.py'


def read_dot_rmotr_file(path):
    dot_rmotr_path = path / DOT_RMOTR_FILE_NAME
    with dot_rmotr_path.open('r') as fp:
        dot_rmotr_content = toml.loads(fp.read())
    return dot_rmotr_content


def get_lesson_class_from_type(_type):
    if _type == READING:
        return ReadingLesson
    elif _type == ASSIGNMENT:
        return AssignmentLesson

    raise exceptions.InvalidLessonTypeException(
        '{} is not a valid lesson type'.format(_type))


def read_lesson(unit, lesson_path):
    order = utils.get_order_from_numbered_object_directory_name(
        lesson_path.name)
    dot_rmotr = read_dot_rmotr_file(lesson_path)

    LessonClass = get_lesson_class_from_type(dot_rmotr['type'])

    readme_path = lesson_path / README_FILE_NAME
    with readme_path.open(mode='r') as fp:
        readme_content = fp.read()

    lesson = LessonClass(
        unit=unit,
        directory_path=lesson_path,
        uuid=dot_rmotr['uuid'],
        name=dot_rmotr['name'],
        order=order,
        readme_path=readme_path,
        readme_content=readme_content
    )

    return lesson


def read_lessons(unit):
    lessons_glob = unit.directory_path.glob(LESSON_GLOB)
    return [read_lesson(unit, lesson_path) for lesson_path in lessons_glob]


def read_unit(course, unit_path):
    order = utils.get_order_from_numbered_object_directory_name(unit_path.name)
    dot_rmotr = read_dot_rmotr_file(unit_path)
    unit = Unit(
        course=course,
        directory_path=unit_path,
        uuid=dot_rmotr['uuid'],
        name=dot_rmotr['name'],
        order=order
    )
    unit._lessons = read_lessons(unit)
    return unit


def read_units(course):
    units_glob = course.directory_path.glob(UNIT_GLOB)
    return [read_unit(course, unit_path) for unit_path in units_glob]


def read_course_from_path(course_directory_path):
    dot_rmotr = read_dot_rmotr_file(course_directory_path)

    course = Course(
        directory_path=course_directory_path,
        uuid=dot_rmotr['uuid'],
        name=dot_rmotr['name'],
        track=dot_rmotr['track']
    )
    course._units = read_units(course)

    return course


def get_last_unit(course_directory_path):
    read_units(course_directory_path)


def get_last_unit_order(course_directory_path):
    if has_units(course_directory_path):
        last_unit = get_last_unit(course_directory_path)
        order = get_order(last_unit)
        return order + 1
    return 1


def create_unit(course_directory_path, name, order):
    unit_directory_path = (
        course_directory_path /
        utils.generate_unit_directory_name(name, order)
    )

    unit_directory_path.mkdir()
    dot_rmotr_path = unit_directory_path / DOT_RMOTR_FILE_NAME
    with dot_rmotr_path.open(mode='w') as fp:
        fp.write(utils.generate_unit_dot_rmotr_file(name=name))

    return unit_directory_path


def add_unit_to_course(course_directory_path, name, order=None):
    if not isinstance(course_directory_path, Path):
        course_directory_path = Path(course_directory_path)

    course = read_course_from_path(course_directory_path)

    last_unit = course.last_unit
    last_unit_order = (last_unit and last_unit.order) or 0

    if order is None:
        order = last_unit_order + 1

    rename = (order <= last_unit_order)

    return create_unit(course_directory_path, name, order)
