import os
import re
import subprocess

import pytest


def test_java_home_is_set():
    java_home = os.environ.get("JAVA_HOME")
    assert java_home is not None, "Environment variable 'JAVA_HOME' is not set but is required by pySpark to work."


def test_java_version_is_greater_or_equal_11():
    version_regex = re.compile(r'(?P<major>\d+)\.(?P<minor>\d+)\.\w+')

    java_version_output = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT).decode("utf-8")
    print(f"\n`java -version` returned\n{java_version_output}")

    version_number = java_version_output.splitlines()[0].split('"')[1].strip('"')
    print(f"Assuming {version_number=} is the version to check.")

    regex_match = version_regex.search(version_number)
    if not regex_match:
        pytest.fail(f"Couldn't parse Java version from {version_number=} using {version_regex=}.")
    if regex_match["major"] == "1":
        # we need to jump this hoop due to Java version naming conventions - it's fun:
        # https://softwareengineering.stackexchange.com/questions/175075/why-is-java-version-1-x-referred-to-as-java-x
        actual_major_version = int(regex_match["minor"])
    else:
        actual_major_version = int(regex_match["major"])
    expected_major_version = 11
    assert actual_major_version >= expected_major_version, (f"Major version {actual_major_version} is not recent "
                                                            f"enough, we need at least version {expected_major_version}.")
