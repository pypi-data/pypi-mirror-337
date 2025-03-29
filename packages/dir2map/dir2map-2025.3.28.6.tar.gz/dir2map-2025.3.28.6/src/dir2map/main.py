import os
from pathlib import Path
import argparse

base_root_path = None


def _ignore_dir(dir_path: Path, exclude_dirs: list, ):
    if not dir_path.is_dir():
        return False

    for exclude_dir in exclude_dirs:
        exclude_dir_path = base_root_path / exclude_dir
        try:
            dir_path.relative_to(exclude_dir_path)
            return True
        except ValueError:
            continue
    return False


def get_directory_structure(root_dir, prefix="", exclude_dirs=None):
    """
    :param root_dir:
    :param prefix:
    :param exclude_dirs:
    :return:
    """
    global base_root_path
    if not base_root_path:
        base_root_path = Path(root_dir)
    result = []
    if exclude_dirs is None:
        exclude_dirs = []

    try:
        items = os.listdir(root_dir)
    except PermissionError:
        result.append(f"There is no permission to access {root_dir}, so this directory will be skipped.")
        return result

    for index, item in enumerate(items):
        item_path = os.path.join(root_dir, item)

        if _ignore_dir(Path(str(item_path)), exclude_dirs, ):
            continue

        is_last = index == len(items) - 1
        connector = "└── " if is_last else "├── "
        line = prefix + connector + item
        result.append(line)
        if os.path.isdir(item_path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            sub_result = get_directory_structure(item_path, new_prefix, exclude_dirs)
            result.extend(sub_result)
    return result


def get_params():
    parser = argparse.ArgumentParser(description='获取目录相关参数')
    parser.add_argument('-r', '--root_dir', type=Path, required=False,
                        help='根目录路径')
    parser.add_argument('-e', '--exclude_dirs', type=str, default='',
                        help='要排除的目录，多个目录用逗号分隔')
    parser.add_argument('-o', '--out_path', type=Path, default=None, required=False,
                        help='把结果保存到此文件')
    args = parser.parse_args()

    root_dir = args.root_dir
    if not root_dir:
        root_dir = '.'

    out_path = args.out_path
    if args.exclude_dirs:
        exclude_dirs = args.exclude_dirs.split(',')
    else:
        exclude_dirs = []

    return root_dir, exclude_dirs, out_path


def main():
    params = get_params()
    root_dir, exclude_dirs, out_path = params
    # root_dir = r'D:\A\dirtree\src'
    # exclude_dirs = [
    #     '.git',
    #     '.next',
    #     '.idea',
    #     'node_modules',
    #     # 'dirtree/t1/t2',  # As an example
    # ]
    result = get_directory_structure(root_dir=root_dir, exclude_dirs=exclude_dirs, )
    result = [Path(root_dir).absolute().name] + result
    result = '\n'.join(result)
    print(result)
    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        with open(str(out_path), 'w', encoding='utf8', ) as file_obj:
            file_obj.write(result)
