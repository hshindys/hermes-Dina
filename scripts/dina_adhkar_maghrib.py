#!/usr/bin/env python3
import runpy, sys, os
base = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["dina_adhkar_evening.py"]
runpy.run_path(os.path.join(base, "dina_adhkar_evening.py"), run_name="__main__")
