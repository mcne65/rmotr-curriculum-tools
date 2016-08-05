import click
from pathlib import Path
import markdown

from rmotr_curriculum_tools import io, utils
from rmotr_curriculum_tools.models import READING, ASSIGNMENT, EXTERNAL_ASSIGNMENT


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
              type=click.Choice([READING, ASSIGNMENT, EXTERNAL_ASSIGNMENT]),
              required=True)
@click.option('-r', '--repo', default=None, type=str,
              callback=utils.validate_gh_url,
              help="Github repository URL. ie: https://github.com/:org/:repo")
def create_lesson(path_to_unit, name, type, order, repo):
    if type == EXTERNAL_ASSIGNMENT and not repo:
        raise click.BadParameter(
            'Repository URL must be provided (--repo) when creating an '
            'external assignment lesson')
    io.add_lesson_to_unit(path_to_unit, name, type, order, repo)


@rmotr_curriculum_tools.command()
@click.argument('path_to_unit', type=click.Path(exists=True))
def remove_unit(path_to_unit):
    io.remove_unit_from_directory(path_to_unit)


@rmotr_curriculum_tools.command()
@click.argument('path_to_lesson', type=click.Path(exists=True))
def remove_lesson(path_to_lesson):
    io.remove_lesson_from_directory(path_to_lesson)


@rmotr_curriculum_tools.command()
@click.argument('path_to_lesson', type=click.Path(exists=True))
def count_words(path_to_lesson):
    """Count words ignoring code"""
    path = Path(path_to_lesson)
    if not path.exists() or not path.is_file():
        raise click.BadArgumentUsage("The path should be a markdown file")
    with path.open('r') as fp:
        content = fp.read()
    word_count = utils.count_words(
        markdown.markdown(content, extensions=['gfm']))
    click.echo("Word count: {}".format(
        click.style(str(word_count), fg='green')))


if __name__ == '__main__':
    rmotr_curriculum_tools()
