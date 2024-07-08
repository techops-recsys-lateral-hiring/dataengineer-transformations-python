import os
import re
import subprocess

import pytest


def test_java_home_is_set():
    java_home = os.environ.get("JAVA_HOME")
    assert java_home is not None, "Environment variable 'JAVA_HOME' is not set but is required by pySpark to work."


def test_java_version_is_greater_or_equal_11():
    java_version_output = get_java_version_output()
    print(f"\n`java -version` returned\n{java_version_output}")

    version_line = extract_version_line(java_version_output)
    if not version_line:
        pytest.fail("Couldn't find version information in `java -version` output.")

    major_version = parse_major_version(version_line)
    if major_version is None:
        pytest.fail(f"Couldn't parse Java version from {version_line}.")

    expected_major_version = 11
    assert major_version >= expected_major_version, (f"Major version {major_version} is not recent enough, "
                                                     f"we need at least version {expected_major_version}.")


def get_java_version_output():
    return subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT).decode("utf-8")


def extract_version_line(java_version_output):
    for line in java_version_output.splitlines():
        if "version" in line:
            return line
    return None


def parse_major_version(version_line):
    version_regex = re.compile(r'version "(?P<major>\d+)\.(?P<minor>\d+)\.\d+"')
    match = version_regex.search(version_line)
    if not match:
        return None
    major_version = int(match.group("major"))
    if major_version == 1:
        major_version = int(match.group("minor"))
    return major_version
