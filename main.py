import click

from rmotr_curriculum_tools import io
from rmotr_curriculum_tools.models import READING, ASSIGNMENT


@click.group()
def rmotr_curriculum_tools():
    pass


@rmotr_curriculum_tools.command()
@click.argument('path_to_course', type=click.Path(exists=True))
@click.argument('name', type=str)
@click.option('-o', '--order', default=None, type=int)
def create_unit(path_to_course, name, order):
    io.add_unit_to_course(path_to_course, name, order)


@rmotr_curriculum_tools.command()
@click.argument('path_to_unit', type=click.Path(exists=True))
@click.argument('name', type=str)
@click.option('-o', '--order', default=None, type=int)
@click.option('-t', '--type',
              type=click.Choice([READING, ASSIGNMENT]), required=True)
def create_lesson(path_to_unit, name, type, order):
    io.add_lesson_to_unit(path_to_unit, name, type, order)


if __name__ == '__main__':
    rmotr_curriculum_tools()
