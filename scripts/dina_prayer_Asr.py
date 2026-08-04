#!/usr/bin/env python3
import runpy, sys, os
base = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["dina_prayer_check.py", "Asr"]
runpy.run_path(os.path.join(base, "dina_prayer_check.py"), run_name="__main__")
