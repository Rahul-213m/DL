import os
import tempfile
# This is loaded before application modules. Tests must never touch the
# developer's configured attendance.db file or their real ENROLL_PHOTOS tree.
os.environ["DATABASE_URL"] = "sqlite://"
_TEST_ROOT = tempfile.mkdtemp(prefix="attendance-tests-")
os.environ["STORAGE_ROOT"] = os.path.join(_TEST_ROOT, "data")
os.environ["ENROLLMENT_PHOTOS_ROOT"] = os.path.join(_TEST_ROOT, "ENROLL_PHOTOS")
