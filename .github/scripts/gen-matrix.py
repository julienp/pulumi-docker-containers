#!/usr/bin/env python
# Create a matrix wihout any variables. Each desired combination is explicitly listed as an include.
# https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs#example-adding-configurations
#
# matrix = {
#     "include": [
#         {"sdk": "go",     "arch": "amd64", "language_version": "1.21.1", "default": True},
#         {"sdk": "go",     "arch": "arm64", "language_version": "1.21.1", "default": True},
#         {"sdk": "python", "arch": "amd64", "language_version": "3.9",    "default": True,  "suffix": "-3.9"},
#         {"sdk": "python", "arch": "arm64", "language_version": "3.9",    "default": True,  "suffix": "-3.9"},
#         {"sdk": "python", "arch": "amd64", "language_version": "3.10",   "default": False, "suffix": "-3.10"},
#         {"sdk": "python", "arch": "arm64", "language_version": "3.10",   "default": False, "suffix": "-3.10"},
#         ...
#     ]
# }
#
#  * `language_version` is the version of the language runtime to use, for example `3.9` for Python.
#  * `suffix` is an optional suffix to append to the image name, for example `-3.9` to generate `pulumi-python-3.9`.
#  * `default` indicates that this is the default language_version. We will push two tags for the image, once
#     with and once without the suffix in the name, for example `pulumi-python-3.9` and `pulumi-python`.
#
# When running this script, pass `--no-arch` to exclude the `arch` field from the matrix. This is used in the
# release job when building the manifests.
#
import json
import sys

INCLUDE_ARCH = False if len(sys.argv) > 1 and sys.argv[1] == "--no-arch" else True

archs = ["amd64", "arm64"] if INCLUDE_ARCH else [None]
matrix = {"include": []}

# SDKs without version suffixes
# sdks = ["nodejs", "go", "dotnet", "java"]
sdks = {
    "nodejs": "18",
    "go": "1.21.1",
    "dotnet": "6.0",
    "java": "not-used-yet",
}
# Python versions
python_default_version = "3.9"
python_additional_versions = ["3.10", "3.11", "3.12"]


def make_entry(*, sdk, arch, default, language_version, suffix=None):
    entry = {
        "sdk": sdk,
        "default": default,
    }
    if language_version is not None:
        entry["language_version"] = language_version
    if arch is not None:
        entry["arch"] = arch
    if suffix is not None:
        entry["suffix"] = suffix
    return entry


for arch in archs:

    for sdk, version in sdks:
        matrix["include"].append(
            make_entry(sdk=sdk, arch=arch, default=True, language_version=version)
        )

    # Default Python version
    matrix["include"].append(
        make_entry(
            sdk="python",
            arch=arch,
            language_version=python_default_version,
            default=True,
            suffix=f"-{python_default_version}",
        )
    )
    # Additional Python versions
    for version in python_additional_versions:
        matrix["include"].append(
            make_entry(
                sdk="python",
                arch=arch,
                language_version=version,
                default=False,
                suffix=f"-{version}",
            )
        )

print(f"matrix={json.dumps(matrix)}")
