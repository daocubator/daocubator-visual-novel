#!/usr/bin/env python3
"""Rewrite an exported Cloud Build trigger YAML to use a user-managed service account.

Usage: fix_trigger.py trigger.yaml projects/<proj>/serviceAccounts/<email>
"""
import sys

try:
    import yaml
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "-q", "pyyaml"])
    import yaml

path, sa = sys.argv[1], sys.argv[2]
d = yaml.safe_load(open(path))
d["serviceAccount"] = sa
# A user-specified service account requires explicit logging on inline builds.
if isinstance(d.get("build"), dict):
    d["build"].setdefault("options", {})["logging"] = "CLOUD_LOGGING_ONLY"
yaml.safe_dump(d, open(path, "w"), sort_keys=False)
