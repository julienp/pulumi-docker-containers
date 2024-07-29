#!/usr/bin/env python
# Create a matrix wihout any variables. Each desired combination is explicitly listed as an include.
# https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs#example-adding-configurations
#
# matrix = {
#     "include": [
#         {"sdk": "go",     "arch": "amd64", "language_version": "1.21.1", "default": True   "suffix": "-1.21.1"},
#         {"sdk": "go",     "arch": "ard64", "language_version": "1.21.1", "default": True   "suffix": "-1.21.1"},
#         {"sdk": "python", "arch": "amd64", "language_version": "3.9",    "default": True,  "suffix": "-3.9"},
#         {"sdk": "python", "arch": "arm64", "language_version": "3.9",    "default": True,  "suffix": "-3.9"},
#         {"sdk": "python", "arch": "amd64", "language_version": "3.10",   "default": False, "suffix": "-3.10"},
#         {"sdk": "python", "arch": "arm64", "language_version": "3.10",   "default": False, "suffix": "-3.10"},
#         ...
#     ]
# }
#
# `suffix` is an optional suffix to append to the image name, for example `-3.9` to generate `pulumi-python-3.9`.
# `default` indicates that this is the default language_version, and we will push two tags for the image, once
# with and once without the suffix in the name, for example `pulumi-python-3.9` and `pulumi-python`.
#
# When running this script, pass `--no-arch` to exclude the `arch` field from the matrix. This is used in the
# release job when building the manifests.
#
import json
import sys

INCLUDE_ARCH = False if len(sys.argv) > 1 and sys.argv[1] == "--no-arch" else True

matrix = {"include": []}
archs = ["amd64", "arm64"] if INCLUDE_ARCH else [None]
sdks = {
    "python": "3.9",
    # "nodejs": "18",
    # "go": "1.21.1",
    # "dotnet": "6.0",
    # "java": "not-versioned",
}
python_additional_versions = ["3.10" , "3.11"] #, "3.12"]
node_additional_versions = ["18", "20", "22"]

def make_entry(sdk, arch, language_version, default):
    entry = {
        "sdk": sdk,
        "language_version": language_version,
        "suffix": f"-{language_version}",
        "default": default,
    }
    if arch is not None:
        entry["arch"] = arch
    return entry

for (sdk, language_version) in sdks.items():
    for arch in archs:
        matrix["include"].append(make_entry(sdk, arch, language_version, True))

for version in python_additional_versions:
    for arch in archs:
        matrix["include"].append(make_entry("python", arch, version, False))

# for version in node_additional_versions:
#     for arch in archs:
#         matrix["include"].append({
#             "sdk": "nodejs",
#             "arch": arch,
#             "language_version": version,
#             "suffix": f"-{version}",
#             "default": False,
#         })

print(f"matrix={json.dumps(matrix)}")
