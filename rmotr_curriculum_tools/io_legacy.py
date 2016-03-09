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


def _create_assignment_lesson_files(lesson):
    py_paths = [
        lesson.directory_path / MAIN_PY_NAME,
        lesson.directory_path / TEST_PY_NAME
    ]
    for path in py_paths:
        with path.open('w') as fp:
            fp.write('# Empty')


def _create_lesson(lesson):
    lesson.directory_path = (
        lesson.unit.directory_path /
        utils.generate_lesson_directory_name(lesson.name, lesson.order)
    )
    lesson.directory_path.mkdir()
    dot_rmotr_path = lesson.directory_path / DOT_RMOTR_FILE_NAME
    with dot_rmotr_path.open(mode='w') as fp:
        fp.write(lesson.get_dot_rmotr_as_toml())

    readme_path = lesson.directory_path / README_FILE_NAME
    with readme_path.open(mode='w') as fp:
        fp.write(lesson.readme_content or '')

    if lesson.type == ASSIGNMENT:
        _create_assignment_lesson_files(lesson)

    return lesson


def flush_lesson(lesson):
    if not lesson.is_created:
        _create_lesson(lesson)


def _create_unit(unit):
    unit.directory_path = (
        unit.course.directory_path /
        utils.generate_unit_directory_name(unit.name, unit.order)
    )
    unit.directory_path.mkdir()
    dot_rmotr_path = unit.directory_path / DOT_RMOTR_FILE_NAME
    with dot_rmotr_path.open(mode='w') as fp:
        fp.write(unit.get_dot_rmotr_as_toml())


def flush_unit(unit):
    if not unit.is_created:
        _create_unit(unit)
    if unit.new_order:
        _rename_unit(unit)
    for lesson in unit.iter_lessons():
        flush_lesson(lesson)


def flush_course(course):
    for unit in course.iter_units():
        if unit.is_dirty:
            flush_unit(unit)
