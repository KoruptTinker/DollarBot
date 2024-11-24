echo "Waking up DollarBot..."

if [ $# -eq 0 ]
then
    python3 code/code.py --bot discord
else
    python3 code/code.py --bot "$1"
fi