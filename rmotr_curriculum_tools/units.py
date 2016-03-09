import uuid as uuid_module
from pathlib import Path
import pytoml as toml

from .utils import slugify, generate_unit_directory_name


def generate_dot_rmotr_content(name, uuid=None):
    return {
        'uuid': str(uuid or uuid_module.uuid4()),
        'name': name
    }


def create_unit_directory(unit_path, unit_name, order):
    unit_path.mkdir()
    dot_rmotr_file_path = unit_path / Path(".rmotr")
    dot_rmotr_file_contents = generate_dot_rmotr_content(unit_name)

    with dot_rmotr_file_path.open(mode='w') as fp:
        fp.write(toml.dumps(dot_rmotr_file_contents))


def resolve_unit_order(course_directory_path, order):
    if has_units(course_directory_path):
        last_unit = get_last_unit(course_directory_path)
        order = get_order(last_unit)
        return order + 1
    return 1


def create_unit(course_directory_path, unit_name, order=None):
    if not isinstance(course_directory_path, Path):
        course_directory_path = Path(course_directory_path)

    order = resolve_unit_order(course_directory_path, order)
    unit_dir_name = generate_unit_directory_name(unit_name, order)
    unit_path = course_directory_path / Path(unit_dir_name)
    create_unit_directory(unit_path, unit_name, order)
