import os
import sys
import gzip
import json
import shutil
import codecs
import tarfile
VERSION = sys.version_info.major


class BaseFileSystem(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def check_exist(self):
        if not os.path.exists(self.file_path):
            return False, None
        return True, None

    def file_or_dir(self):
        if not self.check_exist()[0]:
            raise Exception('no such file')
        if os.path.isdir(self.file_path):
            return False, True
        elif os.path.isfile(self.file_path):
            return True, False


class BaseFile(BaseFileSystem):
    def __init__(self, file_path):
        super(BaseFile, self).__init__(file_path)

    def write_to_file(self, content_list):
        """
        :param content_list: each one should be content of a line
        :return:
        """
        with codecs.open(self.file_path, 'w', "utf-8-sig") as f:
            for i in content_list:
                f.write(i + '\n')
        return True, None

    def append_to_file(self, content_list):
        if not self.check_exist()[0]:
            self.create_file()
        """
        :param content_list: each one should be content of a line
        :return:
        """
        with open(self.file_path, 'a') as f:
            for i in content_list:
                f.write(i + '\n')
        return True, None

    def blank(self):
        open(self.file_path, 'w').close()
        return True, None

    def delete(self):
        try:
            os.remove(self.file_path)
        except:
            pass
        return True, None

    def count_lines(self):
        count, error = 0, None
        if VERSION == 2:
            for _ in open(self.file_path).xreadlines():
                count += 1
        elif VERSION == 3:
            with open(self.file_path) as f:
                for _ in f:
                    count += 1
        return count, error

    def read_lastline(self):
        import mmap
        result, error = None, None
        try:
            with open(self.file_path) as source:
                mapping = mmap.mmap(source.fileno(), 0, prot=mmap.PROT_READ)
            result = mapping[mapping.rfind(b'\n', 0, -1) + 1:]
        except Exception as e:
            error = str(e)
        return result, error

    def show_all_file(self):
        with open(self.file_path, 'r') as f:
            print(f.read())

    def create_file(self):
        open(self.file_path, 'a').close()


class BaseDir(BaseFileSystem):
    def __init__(self, file_path):
        super(BaseDir, self).__init__(file_path)

    def create_dir(self):
        os.makedirs(self.file_path)

    def list_dir(self):
        pass

    def delete(self):
        shutil.rmtree(self.file_path, ignore_errors=True)

    def count_certain_filetype_amount(self, prefix=None, suffix=None):
        if not self.check_exist()[0]:
            raise Exception('no such file')
        count = 0
        for file in os.listdir(self.file_path):
            if prefix and file.startswith(prefix):
                count += 1
            elif suffix and file.endswith(suffix):
                count += 1
        return count, None

    def list_certain_filetype_path(self, prefix=None, suffix=None):
        if not self.check_exist()[0]:
            raise Exception('no such file')
        result = []
        for file in os.listdir(self.file_path):
            if prefix and file.startswith(prefix):
                result.append(os.path.join(self.file_path, file))
            elif suffix and file.endswith(suffix):
                result.append(os.path.join(self.file_path, file))
        return result, None


class FileUtil(object):
    @staticmethod
    def prepare(file_path):
        TargetClass = BaseFile if BaseFileSystem(
            file_path).file_or_dir()[0] else BaseDir
        return TargetClass(file_path)

    @staticmethod
    def check_exist(file_path):
        return BaseFileSystem(file_path).check_exist()

    @staticmethod
    def move_file(origin_path, target_path):
        import shutil
        shutil.move(origin_path, target_path)

    @staticmethod
    def move_dir(ipt_dir_path, opt_dir_path):
        import shutil
        ipt_ins = FileUtil.prepare(ipt_dir_path)
        files, err = ipt_ins.list_certain_filetype_path(suffix='.txt')

        opt_ins = FileUtil.prepare(opt_dir_path)
        if opt_ins.check_exist()[1]:
            raise Exception('no opt dir exist')

        for file in files:
            end_path = os.path.join(opt_dir_path, file.split('/')[-1])
            shutil.move(file, end_path)

    @staticmethod
    def create_dir(file_path):
        # recursively create
        os.makedirs(file_path)

    @staticmethod
    def dir_exist_or_create(file_path):
        if not FileUtil.check_exist(file_path)[0]:
            FileUtil.create_dir(file_path)

    @staticmethod
    def list_dir_with_prefix(dir_path, prefix):
        return BaseDir(dir_path).list_certain_filetype_path(prefix=prefix)

    @staticmethod
    def list_dir_with_suffix(dir_path, suffix):
        return BaseDir(dir_path).list_certain_filetype_path(suffix=suffix)

    @staticmethod
    def list_all_directories(parent_path, absolute_path=False):
        try:
            if absolute_path:
                output = [os.path.join(parent_path, dI) for dI in os.listdir(
                    parent_path) if not dI.startswith('__') and os.path.isdir(os.path.join(parent_path, dI))]
            else:
                output = [dI for dI in os.listdir(parent_path) if not dI.startswith(
                    '__') and os.path.isdir(os.path.join(parent_path, dI))]
        except Exception as e:
            return [], e

        return output, None

    @staticmethod
    def write_to_file(file_path, content_list):
        return BaseFile(file_path).write_to_file(content_list)

    @staticmethod
    def write_to_csv(file_path, content_list):
        import csv
        # with codecs.open(file_path, 'w', "utf-8-sig") as f:
        with open(file_path, 'w', encoding='utf_8_sig') as f:
            writer = csv.writer(f)
            writer.writerows(content_list)

    @staticmethod
    def append_to_file(file_path, content_list):
        return BaseFile(file_path).append_to_file(content_list)

    @staticmethod
    def delete_file(file_path):
        return BaseFile(file_path).delete()

    @staticmethod
    def delete_dir(dir_path):
        return BaseDir(dir_path).delete()

    @staticmethod
    def compress_file(inpath, outpath="", compresslevel=9):
        outpath = outpath if outpath else inpath + ".gz"

        try:
            with open(inpath, 'rb') as f_in, gzip.open(outpath, 'wb', compresslevel=compresslevel) as f_out:
                shutil.copyfileobj(f_in, f_out)
        except Exception as e:
            return None, f'zip file fail: {str(e)}'

        if os.path.exists(outpath):
            return outpath, None
        return None, 'file fly away'

    @staticmethod
    def compress_dir(cwd, dir_name):
        """
        :param cwd: parrent directory
        :param dir_name:
        :return:
        """
        from functools import partial
        pjoin = partial(os.path.join, cwd)
        tar = tarfile.open(pjoin(f"{dir_name}.tar.gz"), "w:gz")
        tar.add(pjoin(dir_name), arcname=dir_name)
        tar.close()
        return pjoin(f"{dir_name}.tar.gz")

    @staticmethod
    def md5_sum(filepath):
        import hashlib
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @staticmethod
    def json_dump_file(filepath, data):
        with open(filepath, 'w') as f:
            f.write(json.dumps(data))

    @staticmethod
    def json_load_file(filepath):
        with open(filepath, 'r') as f:
            data = json.loads(f.read())
        return data

    @staticmethod
    def load_file_lines_to_set(filepath) -> set:
        with open(filepath, 'r') as f:
            result = {i.strip() for i in f.readlines()}
        return result
