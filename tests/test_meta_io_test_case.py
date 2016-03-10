import os
import tempfile
import pytest

from base_tests import IOTestCase

@pytest.mark.meta_test
class MetaIOTestCase(IOTestCase):
    def test_file_exists(self):
        """Shouldn't raise an exception if the file exists"""
        with tempfile.NamedTemporaryFile() as fp:
            # Preconditions
            self.assertTrue(os.path.exists(fp.name))
            self.assertFileExists(fp.name)

    def test_is_file_is_correct(self):
        """Shouldn't raise an exception if the object is a file"""
        with tempfile.NamedTemporaryFile() as fp:
            # Preconditions
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
            # Preconditions
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
            # Preconditions
            self.assertTrue(os.path.exists(tmp_dir))

            self.assertDirectoryExists(tmp_dir)

    def test_is_directory_is_correct(self):
        """Shouldn't raise an exception if the object is a directory"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Preconditions
            self.assertTrue(os.path.exists(tmp_dir))
            self.assertTrue(os.path.isdir(tmp_dir))

            self.assertIsDirectory(tmp_dir)

    def test_assert_directory_is_empty_is_correct(self):
        """Shouldn't raise an exception if the directory is empty"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Preconditions
            self.assertTrue(os.path.exists(tmp_dir))
            self.assertTrue(os.path.isdir(tmp_dir))

            self.assertDirectoryIsEmpty(tmp_dir)

    def test_assert_directory_is_empty_raises_if_not_empty(self):
        """Should raise an exception if the directory is not empty"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            with open(os.path.join(tmp_dir, 'test.py'), 'w') as fp:
                fp.write("# not empty!")

            # Preconditions
            self.assertTrue(os.path.exists(tmp_dir))
            self.assertTrue(os.path.isdir(tmp_dir))
            self.assertFileExists(os.path.join(tmp_dir, 'test.py'))

            with self.assertRaises(AssertionError) as exc:
                self.assertDirectoryIsEmpty(tmp_dir)

            self.assertEqual(
                exc.exception.msg,
                "Directory '{}' isn't empty".format(tmp_dir)
            )

    def test_assert_directory_is_not_empty_correct(self):
        """Shouldn't raise an exception if the directory is not empty"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            with open(os.path.join(tmp_dir, 'test.py'), 'w') as fp:
                fp.write("# not empty!")

            # Preconditions
            self.assertTrue(os.path.exists(tmp_dir))
            self.assertTrue(os.path.isdir(tmp_dir))
            self.assertFileExists(os.path.join(tmp_dir, 'test.py'))

            self.assertDirectoryIsNotEmpty(tmp_dir)

    def test_assert_directory_is_not_empty_raises(self):
        """Shouldn't raise an exception if the directory is empty"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Preconditions
            self.assertTrue(os.path.exists(tmp_dir))
            self.assertTrue(os.path.isdir(tmp_dir))

            with self.assertRaises(AssertionError) as exc:
                self.assertDirectoryIsNotEmpty(tmp_dir)

            self.assertEqual(
                exc.exception.msg,
                "Directory '{}' is empty".format(tmp_dir)
            )

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
            # Preconditions
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
            # Preconditions
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
            # Preconditions
            self.assertTrue(os.path.exists(tmp_dir))
            self.assertTrue(os.path.isdir(tmp_dir))

            with self.assertRaises(AssertionError) as exc:
                self.assertIsNotDirectory(tmp_dir)

            self.assertEqual(
                exc.exception.msg,
                "'{}' is a Directory".format(tmp_dir)
            )
