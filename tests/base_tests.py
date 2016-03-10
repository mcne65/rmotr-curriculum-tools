import unittest
import tempfile
from unittest.util import safe_repr
import os
from pathlib import Path


class IOTestCase(unittest.TestCase):
    FILE = 'FILE'
    DIRECTORY = 'DIRECTORY'
    OBJECT_TYPES = [FILE, DIRECTORY]

    def is_file(obj_path):
        if isinstance(obj_path, Path):
            return obj_path.is_file()
        return os.path.isfile(obj_path)

    def is_dir(obj_path):
        if isinstance(obj_path, Path):
            return obj_path.is_dir()
        return os.path.isdir(obj_path)

    def is_empty(self, obj_path):
        if isinstance(obj_path, Path):
            try:
                next(obj_path.iterdir())
            except StopIteration:
                return True
            else:
                return False
        return os.listdir(obj_path) == []

    def _exists(self, obj_path):
        if isinstance(obj_path, Path):
            return obj_path.exists()
        return os.path.exists(obj_path)

    OBJECT_TYPES_MAPPING = {
        FILE: ('File', is_file),
        DIRECTORY: ('Directory', is_dir)
    }

    def _format_msg_existence(self, obj_path, obj_type,
                              msg=None, should_exists=True):

        exists_error_txt = (should_exists and "doesn't") or "does"
        return self._formatMessage(
            msg, '{} {} {} exist'.format(
                obj_type, safe_repr(obj_path), exists_error_txt))

    def _format_msg_type_mismatch(self, obj_path, obj_type,
                                  msg=None, should_match_types=True):
        type_mismatch_error_txt = should_match_types and "isn't" or "is"
        return self._formatMessage(
            msg, '{} {} a {}'.format(
                safe_repr(obj_path), type_mismatch_error_txt, obj_type))

    def _format_msg_emptyness(self, obj_path, msg, should_be_empty):
        emptyness_error_txt = should_be_empty and "isn't" or 'is'
        return self._formatMessage(
            msg, 'Directory {} {} empty'.format(
                safe_repr(obj_path), emptyness_error_txt)
        )

    def _assert_object_existence(self, obj_path, obj_type,
                                 msg=None, should_exist=True):
        assert obj_type in self.OBJECT_TYPES
        type_name, type_check_fn = self.OBJECT_TYPES_MAPPING[obj_type]

        exists = self._exists(obj_path)
        invalid = (
            (should_exist and not exists) or
            not should_exist and exists
        )
        if invalid:
            msg = self._format_msg_existence(
                obj_path, type_name, msg, should_exist)
            raise self.failureException(msg)

    def _assert_object_type(self, obj_path, obj_type,
                            msg=None, should_match_types=True):
        assert obj_type in self.OBJECT_TYPES
        type_name, type_check_fn = self.OBJECT_TYPES_MAPPING[obj_type]

        is_type = type_check_fn(obj_path)

        invalid = (
            (not is_type and should_match_types) or
            (is_type and not should_match_types)
        )
        if invalid:
            msg = self._format_msg_type_mismatch(
                obj_path, type_name, msg, should_match_types)
            raise self.failureException(msg)

    def _assert_object_is_empty(self, obj_path, msg, should_be_empty=True):
        is_empty = self.is_empty(obj_path)
        invalid = (
            (is_empty and not should_be_empty) or
            (not is_empty and should_be_empty)
        )
        if invalid:
            msg = self._format_msg_emptyness(
                obj_path, msg, should_be_empty)
            raise self.failureException(msg)

    def _assert_object_existence_and_type(self, obj_path, obj_type,
                                          msg=None, should_exist=True,
                                          should_match_types=True):
        assert obj_type in self.OBJECT_TYPES
        type_name, type_check_fn = self.OBJECT_TYPES_MAPPING[obj_type]

        self._assert_object_existence(obj_path, obj_type, msg, should_exist)
        self._assert_object_type(obj_path, obj_type, msg, should_match_types)

    def assertDirectoryExists(self, directory_path, msg=None):
        self._assert_object_existence_and_type(
            directory_path, self.DIRECTORY, msg)

    def assertDirectoryDoesntExist(self, directory_path, msg=None):
        self._assert_object_existence(
            directory_path, self.DIRECTORY, msg, should_exist=False)

    def assertIsDirectory(self, directory_path, msg=None):
        self._assert_object_type(directory_path, self.DIRECTORY, msg)

    def assertIsNotDirectory(self, directory_path, msg=None):
        self._assert_object_type(
            directory_path, self.DIRECTORY, msg, should_match_types=False)

    def assertIsFile(self, file_path, msg=None):
        self._assert_object_type(file_path, self.FILE, msg)

    def assertIsNotFile(self, file_path, msg=None):
        self._assert_object_type(
            file_path, self.FILE, msg, should_match_types=False)

    def assertFileExists(self, file_path, msg=None):
        self._assert_object_existence_and_type(
            file_path, self.FILE, msg)

    def assertFileDoesntExist(self, file_path, msg=None):
        self._assert_object_existence(
            file_path, self.FILE, msg, should_exist=False)

    def assertDirectoryIsEmpty(self, dir_path, msg=None):
        self.assertDirectoryExists(dir_path, msg)
        self._assert_object_is_empty(dir_path, msg, should_be_empty=True)

    def assertDirectoryIsNotEmpty(self, dir_path, msg=None):
        self.assertDirectoryExists(dir_path, msg)
        self._assert_object_is_empty(dir_path, msg, should_be_empty=False)
