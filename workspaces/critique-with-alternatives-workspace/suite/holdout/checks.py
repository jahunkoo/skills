"""Programmatic checks for the suite-holdout set: the suite's checks.py, reading the check specs of this folder.

The check kinds and scripts are the suite's (../checks.py); only the folder of check-specs/ differs.
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("suite_checks_holdout", HERE.parent / "checks.py")
_suite = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_suite)
_suite.HERE = HERE  # check-specs/<set>.json are read from this folder

PACKET_FILES = _suite.PACKET_FILES
check = _suite.check
