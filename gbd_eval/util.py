import sys


def name(name: str):
    dict = {
    }
    if name in dict:
        return dict[name]
    else:
        return name

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
