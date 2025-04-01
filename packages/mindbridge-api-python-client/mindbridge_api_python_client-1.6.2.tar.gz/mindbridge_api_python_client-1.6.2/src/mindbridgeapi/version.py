#
#  Copyright MindBridge Analytics Inc. all rights reserved.
#
#  This material is confidential and may not be copied, distributed,
#  reversed engineered, decompiled or otherwise disseminated without
#  the prior written consent of MindBridge Analytics Inc.
#
from importlib.metadata import version
from typing import cast


def get_package_name() -> str:
    return "mindbridge-api-python-client"


def get_version() -> str:
    return version(get_package_name())


def get_version_tuple() -> tuple[int, int, int]:
    version_list_str = get_version().split(".")
    if len(version_list_str) != 3 or not all(x.isdigit() for x in version_list_str):
        raise ValueError(
            f"Unexpected version for {get_package_name()!r}: {get_version()!r}"
        )

    return cast("tuple[int, int, int]", tuple(int(x) for x in version_list_str))
