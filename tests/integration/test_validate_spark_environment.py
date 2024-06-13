import os
import subprocess


def test_java_home_is_set():
    java_home = os.environ.get("JAVA_HOME")
    assert java_home is not None, "Environment variable 'JAVA_HOME' is not set but is required by pySpark to work."


def test_java_version_is_greater_or_equal_11():
    java_version = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT).decode("utf-8")
    print(f"\n`java -version` returned\n{java_version}")
    version_number = java_version.splitlines()[0].split('"')[1].strip('"')
    print(f"Assuming {version_number=} is the version to check.")
    version_identifier_at_idx_0, version_identifier_at_idx_1, _ = version_number.split('.')
    if eval(version_identifier_at_idx_0) == 1:
        print(
            f"Found {version_identifier_at_idx_0=}, this is not the major version. Using {version_identifier_at_idx_1=} to check version requirements.")
        actual_major_version = eval(version_identifier_at_idx_1)
    else:
        actual_major_version = eval(version_identifier_at_idx_0)
    expected_major_version = 11
    assert actual_major_version >= expected_major_version, f"Major version {actual_major_version} is not recent enough, we need at least version {expected_major_version}."
