#!/bin/bash
cd /workspace/Formula_Server && nohup python manage_formula_server.py >/dev/null 2>&1 &
echo "server runing"
/bin/bash
