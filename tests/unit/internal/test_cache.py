from unittest.mock import patch, call

from spccore.internal.cache import *
from spccore.internal.cache import _cache_dirs, _get_modified_time, _normalize_path, _is_modified, _write_cache_map_to,\
_get_cache_map_at, _get_all_non_modified_paths


# test _cache_dirs
def test_private_cache_dirs_empty():
    with patch.object(os, "listdir", return_value=list()) as mock_listdir:
        dirs = _cache_dirs(SYNAPSE_DEFAULT_CACHE_ROOT_DIR)
        assert len(list(dirs)) == 0
        mock_listdir.assert_called_once_with(SYNAPSE_DEFAULT_CACHE_ROOT_DIR)


def test_private_cache_dirs_with_invalid_dirs():
    with patch.object(os, "listdir", side_effect=[["123", "fake_name", "another1"],
                                                  ["987123", "other", "567123"]]) as mock_listdir,\
         patch.object(os.path, "isdir", return_value=True) as mock_isdir:
        dirs = _cache_dirs(SYNAPSE_DEFAULT_CACHE_ROOT_DIR)
        assert list(dirs) == [os.path.join(SYNAPSE_DEFAULT_CACHE_ROOT_DIR, "123", "987123"),
                              os.path.join(SYNAPSE_DEFAULT_CACHE_ROOT_DIR, "123", "567123")]
        assert mock_listdir.call_args_list == [call(SYNAPSE_DEFAULT_CACHE_ROOT_DIR),
                                               call(os.path.join(SYNAPSE_DEFAULT_CACHE_ROOT_DIR, "123"))]
        assert mock_isdir.call_args_list == [call(os.path.join(SYNAPSE_DEFAULT_CACHE_ROOT_DIR, "123")),
                                             call(os.path.join(SYNAPSE_DEFAULT_CACHE_ROOT_DIR, "123", "987123")),
                                             call(os.path.join(SYNAPSE_DEFAULT_CACHE_ROOT_DIR, "123", "other")),
                                             call(os.path.join(SYNAPSE_DEFAULT_CACHE_ROOT_DIR, "123", "567123")),
                                             call(os.path.join(SYNAPSE_DEFAULT_CACHE_ROOT_DIR, "fake_name")),
                                             call(os.path.join(SYNAPSE_DEFAULT_CACHE_ROOT_DIR, "another1"))]


# test _get_modified_time
def test_private_get_modified_time_with_non_exist_path():
    with patch.object(os.path, "exists", return_value=False) as mock_exists, \
            patch.object(os.path, "getmtime", return_value=1) as mock_getmtime:
        assert _get_modified_time("some_path") is None
        mock_exists.assert_called_once_with("some_path")
        mock_getmtime.assert_not_called()


def test_private_get_modified_time_with_exist_path():
    with patch.object(os.path, "exists", return_value=True) as mock_exists, \
            patch.object(os.path, "getmtime", return_value=1) as mock_getmtime:
        assert _get_modified_time("some_path") == 1
        mock_exists.assert_called_once_with("some_path")
        mock_getmtime.assert_called_once_with("some_path")


# test _normalize_path
def test_private_normalize_path_with_none():
    with patch.object(os.path, "abspath") as mock_abspath, \
            patch.object(os.path, "normcase") as mock_normcase:
        assert _normalize_path(None) is None
        mock_abspath.assert_not_called()
        mock_normcase.assert_not_called()


def test_private_normalize_path_with_unix_path():
    with patch.object(os.path, "abspath", return_value="/home/ubuntu/") as mock_abspath, \
            patch.object(os.path, "normcase", return_value="/home/ubuntu/") as mock_normcase:
        assert _normalize_path("/home/ubuntu/") == "/home/ubuntu/"
        mock_abspath.assert_called_once_with("/home/ubuntu/")
        mock_normcase.assert_called_once_with("/home/ubuntu/")


def test_private_normalize_path_with_windows_path():
    with patch.object(os.path, "abspath", return_value="C:\Administrator\Documents") as mock_abspath, \
            patch.object(os.path, "normcase", return_value="C:\Administrator\Documents") as mock_normcase:
        assert _normalize_path("C:\Administrator\Documents") == "C:/Administrator/Documents"
        mock_abspath.assert_called_once_with("C:\Administrator\Documents")
        mock_normcase.assert_called_once_with("C:\Administrator\Documents")


# test _is_modified


# test _write_cache_map_to

# test _get_cache_map_at

# test _get_all_non_modified_paths


class TestCache:

    # test constructor
    def test_constructor(self):
        pass

    # test get_default_file_path

    # test get_cached_file_path

    # test get_all_cached_file_path

    # test register

    # test remove

    # test purge
