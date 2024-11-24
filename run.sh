#!/bin/bash

echo "Waking up DollarBot..."

if [ $# -eq 0 ]
then
    python code/code.py --bot discord
else
    python code/code.py --bot "$1"
fi