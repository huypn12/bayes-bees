import re
import sys

f0 = '{ ( -1 ) p^5 + 5 p^4 - 10 p^3 + 10 p^2 - 5 p + 1  }'
f1 = '{ 5 q1^4 * p^5 - 20 q1^3 * p^5 - 20 q1^4 * p^4 + 30 q1^2 * p^5 + 80 q1^3 * p^4 + 30 q1^4 * p^3 - 20 q1 * p^5 - 120 q1^2 * p^4 - 120 q1^3 * p^3 - 20 q1^4 * p^2 + 5 p^5 + 80 q1 * p^4 + 180 q1^2 * p^3 + 80 q1^3 * p^2 + 5 q1^4 * p - 20 p^4 - 120 q1 * p^3 - 120 q1^2 * p^2 - 20 q1^3 * p + 30 p^3 + 80 q1 * p^2 + 30 q1^2 * p - 20 p^2 - 20 q1 * p + 5 p }'
f2 = '{ ( -5 ) q1^4 * p^5 - 5 q2 * q1^3 * p^5 - 5 q2^2 * q1^2 * p^5 - 5 q2^3 * q1 * p^5 + 20 q1^3 * p^5 + 20 q2 * q1^2 * p^5 + 20 q2^2 * q1 * p^5 + 10 q2^3 * p^5 + 20 q1^4 * p^4 + 20 q2 * q1^3 * p^4 + 20 q2^2 * q1^2 * p^4 + 20 q2^3 * q1 * p^4 - 30 q1^2 * p^5 - 30 q2 * q1 * p^5 - 30 q2^2 * p^5 - 80 q1^3 * p^4 - 80 q2 * q1^2 * p^4 - 80 q2^2 * q1 * p^4 - 30 q2^3 * p^4 - 30 q1^4 * p^3 - 30 q2 * q1^3 * p^3 - 30 q2^2 * q1^2 * p^3 - 30 q2^3 * q1 * p^3 + 20 q1 * p^5 + 30 q2 * p^5 + 120 q1^2 * p^4 + 120 q2 * q1 * p^4 + 90 q2^2 * p^4 + 120 q1^3 * p^3 + 120 q2 * q1^2 * p^3 + 120 q2^2 * q1 * p^3 + 30 q2^3 * p^3 + 20 q1^4 * p^2 + 20 q2 * q1^3 * p^2 + 20 q2^2 * q1^2 * p^2 + 20 q2^3 * q1 * p^2 - 10 p^5 - 80 q1 * p^4 - 90 q2 * p^4 - 180 q1^2 * p^3 - 180 q2 * q1 * p^3 - 90 q2^2 * p^3 - 80 q1^3 * p^2 - 80 q2 * q1^2 * p^2 - 80 q2^2 * q1 * p^2 - 10 q2^3 * p^2 - 5 q1^4 * p - 5 q2 * q1^3 * p - 5 q2^2 * q1^2 * p - 5 q2^3 * q1 * p + 30 p^4 + 120 q1 * p^3 + 90 q2 * p^3 + 120 q1^2 * p^2 + 120 q2 * q1 * p^2 + 30 q2^2 * p^2 + 20 q1^3 * p + 20 q2 * q1^2 * p + 20 q2^2 * q1 * p - 30 p^3 - 80 q1 * p^2 - 30 q2 * p^2 - 30 q1^2 * p - 30 q2 * q1 * p + 10 p^2 + 20 q1 * p }'
f3 = '{ 5 q2 * q1^3 * p^5 + 5 q2^2 * q1^2 * p^5 + 5 q3 * q2 * q1^2 * p^5 + 5 q2^3 * q1 * p^5 + 5 q3 * q2^2 * q1 * p^5 + 5 q3^2 * q2 * q1 * p^5 - 20 q2 * q1^2 * p^5 - 20 q2^2 * q1 * p^5 - 20 q3 * q2 * q1 * p^5 - 10 q2^3 * p^5 - 10 q3 * q2^2 * p^5 - 10 q3^2 * q2 * p^5 - 20 q2 * q1^3 * p^4 - 20 q2^2 * q1^2 * p^4 - 20 q3 * q2 * q1^2 * p^4 - 20 q2^3 * q1 * p^4 - 20 q3 * q2^2 * q1 * p^4 - 20 q3^2 * q2 * q1 * p^4 + 30 q2 * q1 * p^5 + 30 q2^2 * p^5 + 30 q3 * q2 * p^5 + 10 q3^2 * p^5 + 80 q2 * q1^2 * p^4 + 80 q2^2 * q1 * p^4 + 80 q3 * q2 * q1 * p^4 + 30 q2^3 * p^4 + 30 q3 * q2^2 * p^4 + 30 q3^2 * q2 * p^4 + 30 q2 * q1^3 * p^3 + 30 q2^2 * q1^2 * p^3 + 30 q3 * q2 * q1^2 * p^3 + 30 q2^3 * q1 * p^3 + 30 q3 * q2^2 * q1 * p^3 + 30 q3^2 * q2 * q1 * p^3 - 30 q2 * p^5 - 20 q3 * p^5 - 120 q2 * q1 * p^4 - 90 q2^2 * p^4 - 90 q3 * q2 * p^4 - 20 q3^2 * p^4 - 120 q2 * q1^2 * p^3 - 120 q2^2 * q1 * p^3 - 120 q3 * q2 * q1 * p^3 - 30 q2^3 * p^3 - 30 q3 * q2^2 * p^3 - 30 q3^2 * q2 * p^3 - 20 q2 * q1^3 * p^2 - 20 q2^2 * q1^2 * p^2 - 20 q3 * q2 * q1^2 * p^2 - 20 q2^3 * q1 * p^2 - 20 q3 * q2^2 * q1 * p^2 - 20 q3^2 * q2 * q1 * p^2 + 10 p^5 + 90 q2 * p^4 + 40 q3 * p^4 + 180 q2 * q1 * p^3 + 90 q2^2 * p^3 + 90 q3 * q2 * p^3 + 10 q3^2 * p^3 + 80 q2 * q1^2 * p^2 + 80 q2^2 * q1 * p^2 + 80 q3 * q2 * q1 * p^2 + 10 q2^3 * p^2 + 10 q3 * q2^2 * p^2 + 10 q3^2 * q2 * p^2 + 5 q2 * q1^3 * p + 5 q2^2 * q1^2 * p + 5 q3 * q2 * q1^2 * p + 5 q2^3 * q1 * p + 5 q3 * q2^2 * q1 * p + 5 q3^2 * q2 * q1 * p - 20 p^4 - 90 q2 * p^3 - 20 q3 * p^3 - 120 q2 * q1 * p^2 - 30 q2^2 * p^2 - 30 q3 * q2 * p^2 - 20 q2 * q1^2 * p - 20 q2^2 * q1 * p - 20 q3 * q2 * q1 * p + 10 p^3 + 30 q2 * p^2 + 30 q2 * q1 * p }'
f4 = '{ ( -5 ) q3 * q2 * q1^2 * p^5 - 5 q3 * q2^2 * q1 * p^5 - 5 q3^2 * q2 * q1 * p^5 - 5 q4 * q3 * q2 * q1 * p^5 + 20 q3 * q2 * q1 * p^5 + 10 q3 * q2^2 * p^5 + 10 q3^2 * q2 * p^5 + 10 q4 * q3 * q2 * p^5 + 20 q3 * q2 * q1^2 * p^4 + 20 q3 * q2^2 * q1 * p^4 + 20 q3^2 * q2 * q1 * p^4 + 20 q4 * q3 * q2 * q1 * p^4 - 30 q3 * q2 * p^5 - 10 q3^2 * p^5 - 10 q4 * q3 * p^5 - 80 q3 * q2 * q1 * p^4 - 30 q3 * q2^2 * p^4 - 30 q3^2 * q2 * p^4 - 30 q4 * q3 * q2 * p^4 - 30 q3 * q2 * q1^2 * p^3 - 30 q3 * q2^2 * q1 * p^3 - 30 q3^2 * q2 * q1 * p^3 - 30 q4 * q3 * q2 * q1 * p^3 + 20 q3 * p^5 + 5 q4 * p^5 + 90 q3 * q2 * p^4 + 20 q3^2 * p^4 + 20 q4 * q3 * p^4 + 120 q3 * q2 * q1 * p^3 + 30 q3 * q2^2 * p^3 + 30 q3^2 * q2 * p^3 + 30 q4 * q3 * q2 * p^3 + 20 q3 * q2 * q1^2 * p^2 + 20 q3 * q2^2 * q1 * p^2 + 20 q3^2 * q2 * q1 * p^2 + 20 q4 * q3 * q2 * q1 * p^2 - 5 p^5 - 40 q3 * p^4 - 5 q4 * p^4 - 90 q3 * q2 * p^3 - 10 q3^2 * p^3 - 10 q4 * q3 * p^3 - 80 q3 * q2 * q1 * p^2 - 10 q3 * q2^2 * p^2 - 10 q3^2 * q2 * p^2 - 10 q4 * q3 * q2 * p^2 - 5 q3 * q2 * q1^2 * p - 5 q3 * q2^2 * q1 * p - 5 q3^2 * q2 * q1 * p - 5 q4 * q3 * q2 * q1 * p + 5 p^4 + 20 q3 * p^3 + 30 q3 * q2 * p^2 + 20 q3 * q2 * q1 * p }'
f5 = '{ 5 q4 * q3 * q2 * q1 * p^5 - 10 q4 * q3 * q2 * p^5 - 20 q4 * q3 * q2 * q1 * p^4 + 10 q4 * q3 * p^5 + 30 q4 * q3 * q2 * p^4 + 30 q4 * q3 * q2 * q1 * p^3 - 5 q4 * p^5 - 20 q4 * q3 * p^4 - 30 q4 * q3 * q2 * p^3 - 20 q4 * q3 * q2 * q1 * p^2 + p^5 + 5 q4 * p^4 + 10 q4 * q3 * p^3 + 10 q4 * q3 * q2 * p^2 + 5 q4 * q3 * q2 * q1 * p }'


def replace_ops(bscc_str):
    bscc_str = bscc_str.replace('{', r'(')
    bscc_str = bscc_str.replace('}', r')')
    bscc_str = bscc_str.replace('^', r'**')
    return bscc_str


def replace_var(bscc_str):
    bscc_str = bscc_str.replace('p', r'p[0]')
    pattern = re.compile(r'([q])(\d*)')
    bscc_str = pattern.sub(r"p[\2]", bscc_str)
    return bscc_str


def replace_implicit_op(bscc_str):
    pattern = re.compile(r'(\d|\)) ([a-z])')
    bscc_str = pattern.sub(r"\1 * \2", bscc_str)
    return bscc_str


def parse_bscc_str(bscc_str):
    bscc_str = replace_ops(bscc_str)
    bscc_str = replace_var(bscc_str)
    bscc_str = replace_implicit_op(bscc_str)
    return bscc_str


def test1():
    bscc_str = '{ ( -1 ) q12^5 + 5 q1^4 - 10 p^3 + 10 p^2 - 5 p + 1  }'
    print('Original: {}'.format(bscc_str))
    bscc_str = bscc_str.replace('{', r'(')
    bscc_str = bscc_str.replace('}', r')')
    bscc_str = bscc_str.replace('^', r'**')
    print('replaced ops: {}'.format(bscc_str))
    # qi to p[i]
    bscc_str = bscc_str.replace('p', r'p[0]')
    pattern = re.compile(r'([q])(\d*)')
    bscc_str = pattern.sub(r"p[\2]", bscc_str)
    print('replaced vars: {}'.format(bscc_str))
    # add * if needed
    pattern = re.compile(r'(\d|\)) ([a-z])')
    bscc_str = pattern.sub(r"\1 * \2", bscc_str)
    print('replaced implicit ops: {}'.format(bscc_str))
    expected = '( ( -1 ) * p[12]**5 + 5 * p[1]**4 - 10 * p[0]**3 + 10 * p[0]**2 - 5 * p[0] + 1  )'
    assert(bscc_str == expected)


bscc_pfunc_template = """

    def f_bscc_{bscc[idx]}(self, p):
        f = {bscc[expr]}
        return f

"""

bscc_file_template = """

    import numpy as np

"""



def test2():
    generated_py = ""
    expressions = [f0, f1, f2, f3, f4, f5]
    for idx, expr_str in enumerate(expressions):
        bscc_str = parse_bscc_str(expr_str)
        generated_py += bscc_pfunc_template.format(bscc={
            'idx': idx,
            'expr': bscc_str})
    filename = "semisync_5.py"
    with open(filename, "w") as fptr:
        fptr.write(generated_py)

def test10():
    generated_py = ""
    from multiparam_semisynchronous_10 import f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11
    expressions = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11]
    for idx, expr_str in enumerate(expressions):
        bscc_str = parse_bscc_str(expr_str)
        generated_py += bscc_pfunc_template.format(bscc={
            'idx': idx,
            'expr': bscc_str})
    filename = "semisync_10.py"
    with open(filename, "w") as fptr:
        fptr.write(generated_py)

def main():
    test10()


if __name__ == "__main__":
    sys.exit(main())
