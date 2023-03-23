import sys


def define_ast(output_dir, base_name, types):
    path = output_dir + "/" + base_name.lower() + ".py"
    print(f"generated AST code at {path}")
    with open(path, "w") as outfile:
        outfile.write("from __future__ import annotations\n")
        outfile.write("from abc import ABC, abstractmethod\n")
        outfile.write("from token import Token\n")
        outfile.write("\n\n")
        outfile.write(f"class {base_name}(ABC):\n")
        # outfile.write("    @abstractmethod\n")
        # outfile.write("    def __init__(self): pass")

         # base (abstract) accept method
        outfile.write("    @abstractmethod\n")
        outfile.write("    def accept(self, visitor: Visitor): pass\n")
        outfile.write("\n\n")

        # each other clas for each type we have
        for name, fields in types.items():
            define_type(outfile,name, fields)

        # each visitor abstract method
        define_visitor(outfile, base_name, types)
       
       

def define_visitor(outfile, base_name, types):
    outfile.write("class Visitor:\n")
    for type_name in types.keys():
        outfile.write("    @abstractmethod\n")
        outfile.write(f"    def visit{type_name}{base_name}(self, {base_name.lower()}: {type_name}): pass")
        outfile.write("\n\n")
    outfile.write("\n\n")


def define_type(outfile, name, fields):
    outfile.write(f"class {name}(Expr):\n")
    # init
    outfile.write(f"    def __init__(self,{fields}):\n")
    params = [field.strip() for field in fields.split(',')]
    for param in params:
        param=param.split(':')[0].strip()
        outfile.write(f"        self.{param} = {param}\n")
    
    # visitor pattern
    outfile.write("\n")
    outfile.write("    def accept(self, visitor: Visitor):\n")
    outfile.write(f"        return visitor.visit{name}{base_name}(self)")
    outfile.write("\n\n")

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


types = {"Binary": f"left: {base_name}, operator: Token, right: {base_name}",
         "Grouping": f"expression: {base_name}",
         "Literal": f"value: object",
         "Unary": f"operator: Token, right: {base_name}"}

define_ast(output_dir, base_name, types)