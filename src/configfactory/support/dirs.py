import os


def root_dir(target=None):
    """
    Returns root directory.
    """
    root = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__)
            )
        )
    )
    return target_dir(root, target)


def package_dir(target=None):
    root = os.path.dirname(
        os.path.dirname(__file__)
    )
    return target_dir(root, target)


def target_dir(root, target=None):
    if target:
        return os.path.join(root, target)
    return root
