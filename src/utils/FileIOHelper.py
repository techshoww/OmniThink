import json
import pickle

class FileIOHelper:
    @staticmethod
    def dump_json(obj, file_name, encoding="utf-8"):
        with open(file_name, 'w', encoding=encoding) as fw:
            json.dump(obj, fw, default=FileIOHelper.handle_non_serializable, ensure_ascii=False)

    @staticmethod
    def handle_non_serializable(obj):
        return "non-serializable contents"  # mark the non-serializable part

    @staticmethod
    def load_json(file_name, encoding="utf-8"):
        with open(file_name, 'r', encoding=encoding) as fr:
            return json.load(fr)

    @staticmethod
    def write_str(s, path):
        with open(path, 'w') as f:
            f.write(s)

    @staticmethod
    def load_str(path):
        with open(path, 'r') as f:
            return '\n'.join(f.readlines())

    @staticmethod
    def dump_pickle(obj, path):
        with open(path, 'wb') as f:
            pickle.dump(obj, f)

    @staticmethod
    def load_pickle(path):
        with open(path, 'rb') as f:
            return pickle.load(f)