import sys


types = {"Binary": "left: Expr, operator: Token, right: Expr",
         "Grouping": "expression: Expr",
         "Literal": "value: object",
         "Unary": "operator: Token, right: Expr"}

def define_ast(output_dir, base_name, types):
    path = output_dir + "/" + base_name.lower() + ".py"
    print(f"generated AST code at {path}")
    with open(path, "w") as outfile:
        outfile.write("from abc import ABC, abstractmethod\n")
        outfile.write("from token import Token\n")
        outfile.write(f"class {base_name}(ABC):\n")
        outfile.write("    @abstractmethod\n")
        outfile.write("    def __init__(self): pass\n")
        for name, fields in types.items():
            define_type(outfile,name, fields)

def define_type(outfile, name, fields):
    outfile.write(f"class {name}(Expr):\n")
    outfile.write(f"    def __init__(self,{fields}):\n")
    params = [field.strip() for field in fields.split(',')]
    for param in params:
        param=param.split(':')[0].strip()
        outfile.write(f"        self.{param} = {param}\n")

args = sys.argv
base_name = "Expr"

if len(args)==2:
    output_dir = args[1] 
elif len(args)==3:
    base_name = args[1]
    output_dir = args[2]
else:
    print("Usage: generate_ast -BASE_NAME <output_dir>")
    sys.exit(64)
define_ast(output_dir, base_name, types)