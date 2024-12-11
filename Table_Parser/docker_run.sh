#!/bin/bash
cd /workspace/Table_Parser && nohup python manage_table_parser.py >/dev/null 2>&1 &
echo "server runing"
/bin/bash


