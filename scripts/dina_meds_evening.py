#!/usr/bin/env python3
import runpy, sys, os
base = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["dina_meds_check.py", "evening"]
runpy.run_path(os.path.join(base, "dina_meds_check.py"), run_name="__main__")
