import os


def walk_up_folder(path, depth=1):
    """Ref: https://stackoverflow.com/a/39097487/3003438"""
    _cur_depth = 1
    while _cur_depth < depth:
        path = os.path.dirname(path)
        _cur_depth += 1
    return path
