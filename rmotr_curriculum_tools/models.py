import pytoml as toml
from pathlib import Path

from .utils import slugify

ASSIGNMENT = 'assignment'
READING = 'reading'


class BaseTrackObject(object):
    def __str__(self):
        return "({}) - {} - {}".format(
            self.__class__.__name__, self.name, self.uuid
        )

    def _slugify_wiht_order(self, prefix, order, name):
        return '{prefix}-{order}{slug}'.format(
            prefix=prefix,
            order=order,
            slug=((name and '-' + slugify(name)) or '')
        )

    __unicode__ = __str__
    __repr__ = __str__

    @property
    def directory_path(self):
        return self._directory_path

    @directory_path.setter
    def directory_path(self, path):
        self._directory_path = (isinstance(path, Path) and path) or Path(path)

    @property
    def is_created(self):
        return self._directory_path is not None


class Course(BaseTrackObject):
    def __init__(self, directory_path, uuid, name, track):
        self._directory_path = directory_path
        self.uuid = uuid
        self.name = name
        self.track = track

        self._units = []

    def add_unit(self, unit):
        self._units.append(unit)

    def unit_count(self):
        return len(self._units)

    def iter_units(self):
        for unit in sorted(self._units, key=lambda u: u.order):
            yield unit

    @property
    def last_unit(self):
        if not self._units:
            return None

        return sorted(self._units, key=lambda u: u.order)[-1]


class Unit(BaseTrackObject):
    def __init__(self, course, uuid, name, order, directory_path=None):
        self.course = course
        self._directory_path = directory_path
        self.slug = self._slugify_wiht_order('unit', order, name)
        self.uuid = uuid
        self.name = name
        self.order = order

        self._lessons = []

    def add_lesson(self, lesson):
        self._lessons.append(lesson)

    def get_dot_rmotr_as_toml(self):
        return toml.dumps({
            'uuid': self.uuid,
            'name': self.name
        })

    def lesson_count(self):
        return len(self._lessons)

    def iter_lessons(self):
        for lesson in sorted(self._lessons, key=lambda l: l.order):
            yield lesson

    @property
    def is_dirty(self):
        return not self.is_created or self.new_order

    @property
    def new_order(self):
        return False

class Lesson(BaseTrackObject):
    def __init__(self, unit, uuid, name, order,
                 directory_path=None, readme_path=None, readme_content=None):
        self.unit = unit
        self._directory_path = directory_path
        self.slug = self._slugify_wiht_order('lesson', order, name)
        self.uuid = uuid
        self.name = name
        self.order = order
        self.readme_path = readme_path
        self.readme_content = readme_content

    def get_dot_rmotr_as_toml(self):
        return toml.dumps({
            'uuid': self.uuid,
            'name': self.name,
            'type': self.type
        })


class ReadingLesson(Lesson):
    def __init__(self, *args, **kwargs):
        super(ReadingLesson, self).__init__(*args, **kwargs)
        self.type = READING


class AssignmentLesson(Lesson):
    def __init__(self, *args, **kwargs):
        # self.main_content = kwargs.pop('main_content')
        # self.tests_content = kwargs.pop('tests_content')

        super(AssignmentLesson, self).__init__(*args, **kwargs)
        self.type = ASSIGNMENT
