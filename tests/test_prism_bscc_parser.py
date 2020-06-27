from scripts.models.prism_utils.prism_bscc_parser import PrismBsccParser

import pytest



def eval_bscc_ast_pfuncs(bscc_ast_pfuncs, r):
    aeval = Interpreter()
    aeval.symtable['r'] = r
    return [aeval.run(f) for f in bscc_ast_pfuncs]

def test_15bees():
    parser = PrismBsccParser("models/prism/bee_multiparam_synchronous_10.txt")
    parser.process()
    bscc_ast_pfuncs = parser.bscc_ast_pfuncs
    bscc_str_pfuncs = parser.bscc_str_pfuncs
    print(parser.params_count)
    r = [
        0.01, 0.02, 0.03, 0.04, 0.05,
        0.06, 0.07, 0.08, 0.09, 0.1,
        0.11, 0.12, 0.13, 0.14, 0.15
    ]
    eval_bscc = eval_bscc_ast_pfuncs(bscc_ast_pfuncs, r)
    print(eval_bscc)

def test_stress():
    parser = PrismBsccParser("synchronous_40.txt")
    try:
        parser.process()
    except Exception as ex:
        raise ex
    bscc_ast_pfuncs = parser.bscc_ast_pfuncs
    bscc_str_pfuncs = parser.bscc_str_pfuncs
    print(bscc_str_pfuncs[0])
    aeval = Interpreter()
    aeval.symtable['p'] = 0.3
    aeval.symtable['q'] = 0.7
    for i in range(0, len(bscc_ast_pfuncs)):
        try:
            print(aeval.run(bscc_ast_pfuncs[i]))
        except Exception as ex:
            print(i)


def main():
    test_15bees()
    #   test_stress()

if __name__ == "__main__":
    sys.exit(main())

