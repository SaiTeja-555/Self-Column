from logic import *

symbols = []
people = ["A","B","C","D"]
for person in people:
    symbols.append(Symbol(f"{person}_knight"))
    symbols.append(Symbol(f"{person}_knave"))
    
knowledge_base = And()

for person in people:
    knowledge_base.add(Or(Symbol(f"{person}_knight"),Symbol(f"{person}_knave")))
    knowledge_base.add(Biconditional(Symbol(f"{person}_knight"),Not(Symbol(f"{person}_knave"))))
    
A_statement = Or(Symbol("A_knight"),Symbol("A_knave"))
B_statement = 
B_statement2 = Symbol("C_knave")
C_statement = Symbol("A_knight")


knowledge_base.add(Implication(A_statement,Symbol("A_knight")))
knowledge_base.add(Implication(Not(A_statement),Symbol("A_knave")))
knowledge_base.add(Implication(And(B_statement,B_statement2),Symbol("B_knight")))
knowledge_base.add(Implication(And(Not(B_statement),Not(B_statement2)),Symbol("B_knave")))
knowledge_base.add(Implication(C_statement,Symbol("C_knight")))
knowledge_base.add(Implication(Not(C_statement),Symbol("C_knave")))


if model_check(knowledge_base,Symbol("A_knight")):
    print("A is knight")
elif model_check(knowledge_base,Symbol("A_knave")):
    print("A is knave")
else:
    print("....")

if model_check(knowledge_base,Symbol("B_knight")):
    print("B is knight")
elif model_check(knowledge_base,Symbol("B_knave")):
    print("B is knave")
else:
    print("....")
