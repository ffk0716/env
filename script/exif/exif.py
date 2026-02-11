import subprocess
import json
import datetime as dt
import argparse
import os
import exiftool
import atexit


def find_mp4_files():

    mp4_files = []
    for root, _, files in os.walk('.'):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(".mp4"):
                if not 'crf' in file_path:
                    mp4_files.append(file_path)
            if file.lower().endswith(".mov"):
                mp4_files.append(file_path)

    return sorted(mp4_files)


class tag_agent:
    _et = None

    @classmethod
    def get_et(cls):
        if cls._et is None:
            cls._et = exiftool.ExifToolHelper()
            atexit.register(lambda: cls._et.terminate())
        return cls._et

    def __init__(self, fname):
        self.fname = fname
        self.et = self.get_et()
        self.requested_tags = set()
        self._cache = {}

    def get_tag_all(self, tag_names):
        if isinstance(tag_names, str):
            tag_names = [tag_names]

        t_set = set(tag_names)

        missing_tags = t_set - set(self._cache.keys())

        if missing_tags:
            try:
                results = self.et.get_tags(self.fname, list(missing_tags))
                if results:
                    self._cache.update(results[0])
            except Exception as e:
                print(f"讀取 EXIF 失敗: {e}")

        return {t: self._cache.get(t) for t in tag_names if t in self._cache}

    def get_tag(self, tag_name):
        vs = self.get_tag_all(tag_name)
        for v in vs.values():
            return v
        return None

    def set_tag(self, tag_dict, params=["-overwrite_original"]):
        try:
            self.et.set_tags(self.fname, tags=tag_dict, params=params)
            self._cache.clear()
            return True
        except Exception as e:
            print(f"寫入 EXIF 失敗: {e}")
            return False

    def shift_create_date(self, hours):
        tag = "QuickTime:CreateDate"
        raw_date = self.get_tag(tag)

        dt_format = "%Y:%m:%d %H:%M:%S"
        utc = dt.datetime.strptime(raw_date, dt_format)
        utc_new = utc + dt.timedelta(hours=hours)
        new_date_str = utc_new.strftime(dt_format)
        print(f'{utc} -> {utc_new}')

        self.set_tag({tag: new_date_str})
        raw_date = self.get_tag(tag)
        assert raw_date == new_date_str


def get_model(f):
    ta = tag_agent(f)
    return ta.get_tag(["QuickTime:Model", "EXIF:Model", "XML:DeviceModelName", "QuickTime:Encoder"])


def set_model(f, v):
    ta = tag_agent(f)
    ta.set_tag({'QuickTime:Model': v})


def copy_model(src, dst, dry=False):
    src_model = get_model(src)
    dst_model = get_model(dst)
    if src_model is None:
        return f"error: exif model copy failed, None vs {dst_model}"
    if src_model == dst_model:
        return f'skip: exif model match {src_model} == {dst_model}'
    else:
        if dry:
            return f'copy(dry): exif model {src_model} -> {dst_model}'
        else:
            set_model(dst, src_model)
            new_dst_model = get_model(dst)
            if src_model != new_dst_model:
                print(f'{src_model} != {new_dst_model}')
            assert (src_model == new_dst_model)
            return f'copy: exif model {src_model} -> {dst_model}'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='The source MP4 file to read the tag from.')
    parser.add_argument('--output', help='The target MP4 file to write the tag to.')

    args = parser.parse_args()

    source_tag = 'DeviceModelName'
    target_tag = 'Encoder'

    tag_value_to_copy = get_exif_tag(args.input, source_tag)

    if tag_value_to_copy:
        print(f"Read value '{tag_value_to_copy}' from tag '{source_tag}' in '{args.input}'.")

        # 2. 將值寫入 b.mp4 的指定標籤
        if args.output:
            v = get_exif_tag(args.output, target_tag)
            print(v)
            write_exif_tag(args.output, target_tag, tag_value_to_copy)
            v = get_exif_tag(args.output, target_tag)
            print(v)
    else:
        print(f"Could not read value for tag '{source_tag}' from '{args.input}'.")
