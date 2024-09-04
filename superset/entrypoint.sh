#!/bin/bash
python /home/superset/custom_scripts/patch_dialect.py

# Continue with normal Superset startup
# superset run -p 8088 --with-threads --reload --debugger