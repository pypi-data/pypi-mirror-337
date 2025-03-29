from pip._internal.metadata import get_environment
from pip._internal.operations.freeze import FrozenRequirement
from pip._vendor.packaging.utils import canonicalize_name


def freeze_one(name: str, paths=None) -> str:
    """
    Return the pip-freeze style line for a single installed package.
    """
    env = get_environment(paths)
    canonical_target = canonicalize_name(name)

    for dist in env.iter_installed_distributions(
        local_only=False, skip=(), user_only=False
    ):
        if dist.canonical_name == canonical_target:
            return str(FrozenRequirement.from_dist(dist)).rstrip()

    raise ValueError(f"Package {name!r} not found in environment")
