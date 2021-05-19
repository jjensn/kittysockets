'''
FS iterators contains fields that are based on files.

* :class:`katnip.templates.fs_iterators.FsNames` will return file names from the system based on its configuration.
* :class:`katnip.templates.fs_iterators.FsContent` will return the content of files from the system.

'''
import os
from fnmatch import fnmatch
from kitty.core import KittyObject, KittyException
from kitty.model.low_level import BaseField
from kitty.model.low_level import ENC_STR_DEFAULT, StrEncoder


class _FsIterator(KittyObject):
    '''
    This class is able to iterate in a reproducible and consistent way over
    files in a directory, it is used by the kitty fields that are defined in
    this module.
    '''

    def __init__(self, path, name_filter, recurse=False):
        '''
        :param path: base path to iterate over files
        :param name_filter: string to filter filenames, same as shell, not regex
        :param recurse: should iterate inner directories (default: False)

        :example:

            Iterate all log files in current directory
            >> _FsIterator('.', '*.log')
        '''
        super(_FsIterator, self).__init__('_FsIterator')
        self._path = path
        self._name_filter = name_filter
        self._recurse = recurse
        self._path_list = []
        self._filename_dict = {}
        self._count = 0
        self._index = -1
        self._path_index = 0
        self._file_index = 0
        self._enumerate()

    def _enumerate(self):
        self._count = 0
        if self._recurse:
            for path, _, files in os.walk(self._path):
                current = sorted(self._filter_filenames(files))
                if len(current):
                    self._path_list.append(path)
                    self._filename_dict[path] = current
                    self._count += len(current)
            self._path_list = sorted(self._path_list)
        else:
            files = os.listdir(self._path)
            self._path_list = [self._path]
            current = sorted(self._filter_filenames(files))
            self._filename_dict[self._path] = current
            self._count += len(current)

    def _matches(self, filename):
        return fnmatch(filename, self._name_filter)

    def _filter_filenames(self, filenames):
        return [f for f in filenames if self._matches(f)]

    def count(self):
        return self._count

    def reset(self):
        self._index = -1
        self._path_index = 0
        self._file_index = 0

    def current(self):
        '''
        :return: tuple (path, filename) of current case
        '''
        if self._index == -1:
            path = self._path_list[0]
            return path, self._filename_dict[path][0]
        elif self._index < self._count:
            path = self._path_list[self._path_index]
            files = self._filename_dict[path]
            return path, files[self._file_index]
        else:
            raise KittyException('Current is invalid!')

    def next(self):
        '''
        Move to next case

        :return: True if there's another case, False otherwise
        '''
        if self._index == self._count - 1:
            return False
        else:
            self._index += 1
            if self._index > 0:
                path = self._path_list[self._path_index]
                files = self._filename_dict[path]
                if self._file_index < len(files) - 1:
                    self._file_index += 1
                else:
                    self._file_index = 0
                    self._path_index += 1
            return True

    def skip(self, count):
        '''
        Skip up to [count] cases

        :count: number of cases to skip
        :rtype: int
        :return: number of cases skipped
        '''
        left = self.count - self._index - 1
        if count > left:
            return left
        else:
            # progress here
            to_skip = count
            while to_skip:
                path = self._path_list[self._path_index]
                files = self._filename_dict[path]
                len_files = len(files[self._file_index:])
                if len_files > to_skip:
                    self._path_index += 1
                    self._file_index = 0
                    self._index += len_files
                    to_skip -= len_files
                else:
                    self._file_index += to_skip
                    self._index += to_skip
                    to_skip = 0
            return count


class FsNames(BaseField):
    '''
    This field mutations are the file names in a given directory.
    It is pretty useful if you have files that were generated by a different
    fuzzer, and you only need to pass their name to your target.
    You can filter the files based on the file name (name_filter),
    you can recurse into subdirectories (recurse) and
    you can pass full path or only the file name (full_path),
    '''

    _encoder_type_ = StrEncoder

    def __init__(self, path, name_filter, recurse=False, full_path=True, encoder=ENC_STR_DEFAULT, fuzzable=True, name=None):
        '''
        :param path: base path to iterate over files
        :param name_filter: string to filter filenames, same as shell, not regex
        :param recurse: should iterate inner directories (default: False)
        :param full_path: should include full path rather than only file name (default: True)
        :type encoder: :class:`~kitty.model.low_level.encoder.StrEncoder`
        :param encoder: encoder for the field
        :param fuzzable: is field fuzzable (default: True)
        :param name: name of the object (default: None)
        '''
        self._fsi = _FsIterator(path, name_filter, recurse)
        self._full_path = full_path
        if self._full_path:
            default_value = os.path.join(*self._fsi.current())
        else:
            default_value = self._fsi.current()[1]
        super(FsNames, self).__init__(default_value, encoder, fuzzable, name)
        self._num_mutations = self._fsi.count()

    def _mutate(self):
        if self._fsi.next():
            path, name = self._fsi.current()
            if self._full_path:
                name = os.path.join(path, name)
            self._current_value = name

    def reset(self):
        super(FsNames, self).reset()
        self._fsi.reset()

    def skip(self, count):
        skipped = self._fsi.skip(count)
        self._current_index += skipped
        return skipped

    def get_info(self):
        info = super(FsNames, self).get_info()
        info['filepath'], info['filename'] = self._fsi.current()
        return info


class FsContent(BaseField):
    '''
    This field mutations are the contents of files in a given directory.
    It is pretty useful if you have files that were generated by a different
    fuzzer.
    You can filter the files based on the file name (name_filter),
    you can recurse into subdirectories (recurse) and
    you can pass full path or only the file name (full_path),
    '''

    _encoder_type_ = StrEncoder

    def __init__(self, path, name_filter, recurse=False, encoder=ENC_STR_DEFAULT, fuzzable=True, name=None):
        '''
        :param path: base path to iterate over files
        :param name_filter: string to filter filenames, same as shell, not regex
        :param recurse: should iterate inner directories (default: False)
        :type encoder: :class:`~kitty.model.low_level.encoder.StrEncoder`
        :param encoder: encoder for the field
        :param fuzzable: is field fuzzable (default: True)
        :param name: name of the object (default: None)
        '''
        self._fsi = _FsIterator(path, name_filter, recurse)
        super(FsContent, self).__init__(b'', encoder, fuzzable, name)
        self._num_mutations = self._fsi.count()

    def _mutate(self):
        if self._fsi.next():
            full_path = os.path.join(*self._fsi.current())
            self._current_value = open(full_path, 'rb').read()

    def reset(self):
        super(FsContent, self).reset()
        self._fsi.reset()

    def skip(self, count):
        skipped = self._fsi.skip(count)
        self._current_index += skipped
        return skipped

    def get_info(self):
        info = super(FsContent, self).get_info()
        info['filepath'], info['filename'] = self._fsi.current()
        return info
