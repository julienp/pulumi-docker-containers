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
import json

matrix = {"include": []}
archs = ["amd64", "arm64"]
sdks = {
    "python": "3.9",
    # "nodejs": "18",
    # "go": "1.21.1",
    # "dotnet": "6.0",
    # "java": "not-versioned",
}
python_additional_versions = ["3.10" , "3.11"] #, "3.12"]
node_additional_versions = ["18", "20", "22"]

for (sdk, language_version) in sdks.items():
    for arch in archs:
        matrix["include"].append(
            {
                "sdk": sdk,
                "arch": arch,
                "language_version": language_version,
                "suffix": f"-{language_version}",
                "default": True,
            }
        )

for version in python_additional_versions:
    for arch in archs:
        matrix["include"].append(
            {
                "sdk": "python",
                "arch": arch,
                "language_version": version,
                "suffix": f"-{version}",
                "default": False,
            }
        )

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
