import subprocess
import json
import argparse
import os


class exif_agent():

    def __init__(self, fname):
        self.fname = fname

    def read(self, tag_name):
        cmd = ['exiftool', '-j', '-n', f'-{tag_name}', self.fname]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        metadata = json.loads(result.stdout)

        if metadata and tag_name in metadata[0]:
            return metadata[0][tag_name]
        else:
            return None

    def write(self, tag_name, tag_value):
        cmd = ['exiftool', f'-{tag_name}={tag_value}', '-overwrite_original', self.fname]
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Successfully wrote '{tag_value}' to tag '{tag_name}' in '{self.fname}'.")


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


devices = {'Encoder': 'DJI OsmoAction4', 'DeviceModelName': 'FDR-AX43A', 'Model': 'iPhone 13 mini'}


def get_model(f):
    f_exif = exif_agent(f)
    for tag, v in devices.items():
        if v == f_exif.read(tag):
            return tag, v

    cmd = ['exiftool', '-G', '-s', f]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    n, ext = os.path.splitext(f)
    log = f'{n}_exif.txt'
    with open(log, 'w') as f:
        f.write(result.stdout)
    cmd = ['vi', log]
    subprocess.run(cmd)
    assert False


def get_model2(f):
    f_exif = exif_agent(f)
    model = f_exif.read('Model')
    if model in devices.values():
        return model
    return None


def set_model(f, v):
    f_exif = exif_agent(f)
    f_exif.write('Model', v)


def copy_model(src, dst, dry=False):
    src_tag, src_model = get_model(src)
    dst_model = get_model2(dst)
    if src_model == dst_model:
        return f'skip: exif model match {src_model}'
    else:
        if dry:
            return f'copy(dry): exif model {src_model} -> {dst_model}'
        else:
            set_model(dst, src_model)
            assert (src_model == get_model2(dst))
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
