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

    def _exists(self, obj_path):
        if isinstance(obj_path, Path):
            return obj_path.exists()
        return os.path.exists(obj_path)

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


class MetaIOTestCase(IOTestCase):
    def test_file_exists(self):
        """Shouldn't raise an exception if the file exists"""
        with tempfile.NamedTemporaryFile() as fp:
            # Preconditions
            self.assertTrue(os.path.exists(fp.name))
            self.assertFileExists(fp.name)

    def test_is_file_is_correct(self):
        """Shouldn't raise an exception if the object is a file"""
        with tempfile.NamedTemporaryFile() as fp:
            # Preconditions
            self.assertTrue(os.path.exists(fp.name))
            self.assertTrue(os.path.isfile(fp.name))

            self.assertIsFile(fp.name)

    def test_file_exist_raises_if_doesnt_exist(self):
        """Should raise an exception if the file doesn't exist"""
        file_name = os.path.join(
            os.path.expanduser('~'),
            'this-file-shouldnt-exist.python-tests-rmotr')
        self.assertFalse(
            os.path.exists(file_name),
            "Make sure %s doens't exist" % file_name)

        with self.assertRaises(AssertionError) as exc:
            self.assertFileExists(file_name)

        self.assertEqual(
            exc.exception.msg,
            "File '{}' doesn't exist".format(file_name)
        )

    def test_is_file_raises_if_its_not_a_file(self):
        """Should raise an exception if the object is not a file"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Preconditions
            self.assertTrue(os.path.exists(tmp_dir))
            self.assertTrue(os.path.isdir(tmp_dir))

            with self.assertRaises(AssertionError) as exc:
                self.assertIsFile(tmp_dir)

            self.assertEqual(
                exc.exception.msg,
                "'{}' isn't a File".format(tmp_dir)
            )

    def test_file_exists_raises_if_its_not_a_file(self):
        """Should raise an exception if the object is not a file"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Preconditions
            self.assertTrue(os.path.exists(tmp_dir))
            self.assertTrue(os.path.isdir(tmp_dir))

            with self.assertRaises(AssertionError) as exc:
                self.assertFileExists(tmp_dir)
            self.assertEqual(
                exc.exception.msg,
                "'{}' isn't a File".format(tmp_dir)
            )

    def test_assert_file_doesnt_exist_raises(self):
        """Should raise an exception if the file exists"""
        with tempfile.NamedTemporaryFile() as fp:
            # Preconditions
            self.assertTrue(os.path.exists(fp.name))
            self.assertTrue(os.path.isfile(fp.name))

            with self.assertRaises(AssertionError) as exc:
                self.assertFileDoesntExist(fp.name)

            self.assertEqual(
                exc.exception.msg,
                "File '{}' does exist".format(fp.name)
            )

    def test_assert_file_doesnt_exist_passes(self):
        """Shouldn't raise an exception if the file doesn't exist"""
        file_name = os.path.join(
            os.path.expanduser('~'),
            'this-file-shouldnt-exist.python-tests-rmotr')
        self.assertFalse(
            os.path.exists(file_name),
            "Make sure %s doens't exist" % file_name)

        self.assertFileDoesntExist(file_name)

    def test_directory_exists(self):
        """Shouldn't raise an exception if the directory exists"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Preconditions
            self.assertTrue(os.path.exists(tmp_dir))

            self.assertDirectoryExists(tmp_dir)

    def test_is_directory_is_correct(self):
        """Shouldn't raise an exception if the object is a directory"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Preconditions
            self.assertTrue(os.path.exists(tmp_dir))
            self.assertTrue(os.path.isdir(tmp_dir))

            self.assertIsDirectory(tmp_dir)

    def test_directory_exist_raises_if_doesnt_exist(self):
        """Should raise an exception if the directory doesn't exist"""
        dir_name = os.path.join(
            os.path.expanduser('~'),
            'this-directory-shouldnt-exist.python-tests-rmotr')
        self.assertFalse(
            os.path.exists(dir_name),
            "Make sure %s doens't exist" % dir_name)

        with self.assertRaises(AssertionError) as exc:
            self.assertDirectoryExists(dir_name)

        self.assertEqual(
            exc.exception.msg,
            "Directory '{}' doesn't exist".format(dir_name)
        )

    def test_assert_directory_doesnt_exist_raises(self):
        """Should raise an exception if the directory exists"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Preconditions
            self.assertTrue(os.path.exists(tmp_dir))
            self.assertTrue(os.path.isdir(tmp_dir))

            with self.assertRaises(AssertionError) as exc:
                self.assertDirectoryDoesntExist(tmp_dir)

            self.assertEqual(
                exc.exception.msg,
                "Directory '{}' does exist".format(tmp_dir)
            )

    def test_assert_directory_doesnt_exist_passes(self):
        """Shouldn't raise an exception if the directory doesn't exist"""

        dir_name = os.path.join(
            os.path.expanduser('~'),
            'this-directory-shouldnt-exist.python-tests-rmotr')
        self.assertFalse(
            os.path.exists(dir_name),
            "Make sure %s doens't exist" % dir_name)

        self.assertDirectoryDoesntExist(dir_name)

    def test_directory_exists_raises_if_its_not_a_directory(self):
        """Should raise an exception if the object is not a directory"""
        with tempfile.NamedTemporaryFile() as fp:
            # Preconditions
            self.assertTrue(os.path.exists(fp.name))
            self.assertTrue(os.path.isfile(fp.name))

            with self.assertRaises(AssertionError) as exc:
                self.assertDirectoryExists(fp.name)
            self.assertEqual(
                exc.exception.msg,
                "'{}' isn't a Directory".format(fp.name)
            )

    def test_is_directory_raises_if_its_not_a_directory(self):
        """Should raise an exception if the object is not a directory"""
        with tempfile.NamedTemporaryFile() as fp:
            # Preconditions
            self.assertTrue(os.path.exists(fp.name))
            self.assertTrue(os.path.isfile(fp.name))

            with self.assertRaises(AssertionError) as exc:
                self.assertIsDirectory(fp.name)

            self.assertEqual(
                exc.exception.msg,
                "'{}' isn't a Directory".format(fp.name)
            )

    def test_assert_is_not_file_passes(self):
        """Should not raise an exception if object is not a file"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Preconditions
            self.assertTrue(os.path.exists(tmp_dir))
            self.assertTrue(os.path.isdir(tmp_dir))

            self.assertIsNotFile(tmp_dir)

    def test_assert_is_not_file_raises_if_invoked_with_file(self):
        """Should raise an exception if the object is a file"""
        with tempfile.NamedTemporaryFile() as fp:
            # Preconditions
            self.assertTrue(os.path.exists(fp.name))
            self.assertTrue(os.path.isfile(fp.name))

            with self.assertRaises(AssertionError) as exc:
                self.assertIsNotFile(fp.name)

            self.assertEqual(
                exc.exception.msg,
                "'{}' is a File".format(fp.name)
            )

    def test_assert_is_not_dir_passes(self):
        """Should not raise an exception if the object is not a directory"""
        with tempfile.NamedTemporaryFile() as fp:
            # Preconditions
            self.assertTrue(os.path.exists(fp.name))
            self.assertTrue(os.path.isfile(fp.name))

            self.assertIsNotDirectory(fp.name)

    def test_assert_is_not_dir_raises_if_invoked_with_dir(self):
        """Should raise an exception if the object is a directory"""

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Preconditions
            self.assertTrue(os.path.exists(tmp_dir))
            self.assertTrue(os.path.isdir(tmp_dir))

            with self.assertRaises(AssertionError) as exc:
                self.assertIsNotDirectory(tmp_dir)

            self.assertEqual(
                exc.exception.msg,
                "'{}' is a Directory".format(tmp_dir)
            )
