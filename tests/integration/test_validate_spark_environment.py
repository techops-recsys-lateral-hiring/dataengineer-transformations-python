import os
import re
import subprocess

import pytest


def test_java_home_is_set():
    java_home = os.environ.get("JAVA_HOME")
    assert java_home is not None, "Environment variable 'JAVA_HOME' is not set but is required by pySpark to work."


def test_java_version_is_greater_or_equal_11():
    version_regex = re.compile(r'version "(?P<major>\d+)\.(?P<minor>\d+)\.\d+"')

    java_version_output = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT).decode("utf-8")
    print(f"\n`java -version` returned\n{java_version_output}")

    version_line = next((line for line in java_version_output.splitlines() if "version" in line), None)

    if not version_line:
        pytest.fail("Couldn't find version information in `java -version` output.")

    regex_match = version_regex.search(version_line)
    if not regex_match:
        pytest.fail(f"Couldn't parse Java version from {version_line} using {version_regex=}.")

    actual_major_version = int(regex_match["major"])

    if actual_major_version == 1:
        actual_major_version = int(regex_match["minor"])

    expected_major_version = 11
    assert actual_major_version >= expected_major_version, (f"Major version {actual_major_version} is not recent enough, "
                                                     f"we need at least version {expected_major_version}.")
