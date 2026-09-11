import os

# This is loaded before application modules. Tests must never touch the
# developer's configured attendance.db file.
os.environ["DATABASE_URL"] = "sqlite://"
