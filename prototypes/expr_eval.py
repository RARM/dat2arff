import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("expression", help="Expression to check.")
args = parser.parse_args()

if re.match(r"^[a-zA-Z_]\w*([<>=]|<=|>=)[0-9]+(\.[0-9]+)?\?[a-zA-Z_]\w*:[a-zA-Z_]\w*$", args.expression):
    print("Expression OK.")
else:
    print("Error: Expression didn't match.")