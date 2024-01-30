import argparse
import re

def get_create_expr(token) -> dict:
    create_expr = {}

    # Getting tokens when transforming number to nominal.
    if re.match(r"^[a-zA-Z_]\w*([<>=]|<=|>=)[0-9]+(\.[0-9]+)?\?[a-zA-Z_]\w*:[a-zA-Z_]\w*$", token):
        end_of_comp_pos = re.search(r"\?", expr).start(0)
        
        comparison = expr[:end_of_comp_pos]
        results = expr[end_of_comp_pos + 1:]

        comp_op_reg = re.search(r"([<>=]|<=|>=)", comparison)
        comp_op = comp_op_reg.group(0)
        comp_op_pos = comp_op_reg.start(0)
        attr_name = comparison[:comp_op_pos]
        comp_to = comparison[comp_op_pos + 1:]

        res_sep_pos = re.search(r":", results).start(0)
        rit = results[:res_sep_pos]
        rif = results[res_sep_pos + 1:]

        create_expr = {
            "attr_name": attr_name,
            "comp_op": comp_op,
            "comp_to": comp_to,
            "if_true": rit,
            "if_false": rif
        }
    else:
        pass
    return create_expr

parser = argparse.ArgumentParser()
parser.add_argument("expression", help="Expression to check.")
args = parser.parse_args()
expr = args.expression

if re.match(r"^[a-zA-Z_]\w*([<>=]|<=|>=)[0-9]+(\.[0-9]+)?\?[a-zA-Z_]\w*:[a-zA-Z_]\w*$", expr):
    print("Expression OK.")
    
    expr_dict = get_create_expr(expr)
    print("Attribute to compare: '" + expr_dict["attr_name"] + "'")
    print("Comparison operator '" + expr_dict["comp_op"] + "'")
    print("Comparing to: '" + expr_dict["comp_to"] + "'")
    print("Result if true: '" + expr_dict["if_true"] + "'")
    print("Result if false: '" + expr_dict["if_false"] + "'")

else:
    print("Error: Expression didn't match.")