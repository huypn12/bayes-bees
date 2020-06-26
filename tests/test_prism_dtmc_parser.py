from scripts.models.prism_utils.prism_dtmc_parser import PrismDtmcParser

import pytest


@pytest.fixture
def dtmc_parser():
    parser = PrismDtmcParser("data/prism/bee_multiparam_synchronous_3.pm")
    return parser


def test_gcmd_cleanup(dtmc_parser):
    gcmd_str = """a0 = 3 & a1 = 3  & a2 = 3  & b = 0 -> 1.0*r_0*r_0*r_0: (a0'=1) & (a1'=1) & (a2'=1) + 3.0*r_0*r_0*(1-r_0): (a0'=1) & (a1'=1) & (a2'=0) + 3.0*r_0*(1-r_0)*(1-r_0): (a0'=1) & (a1'=0) & (a2'=0) + 1.0*(1-r_0)*(1-r_0)*(1-r_0): (a0'=0) & (a1'=0) & (a2'=0);"""
    gcmd_str = gcmd_str.rstrip().lstrip()
    gcmd_str = dtmc_parser.clean_gcommand_line(gcmd_str)
    gcmd_str = dtmc_parser.replace_select_op(gcmd_str)
    assert(gcmd_str == 'a0=3&a1=3&a2=3&b=0->1.0*r_0*r_0*r_0:(a0=1)&(a1=1)&(a2=1)$3.0*r_0*r_0*(1-r_0):(a0=1)&(a1=1)&(a2=0)$3.0*r_0*(1-r_0)*(1-r_0):(a0=1)&(a1=0)&(a2=0)$1.0*(1-r_0)*(1-r_0)*(1-r_0):(a0=0)&(a1=0)&(a2=0)')


def test_process_state_label(dtmc_parser):
    sstate = 'a0 = 3 & a1 = 3  & a2 = 3  & b = 0'
    sstate = dtmc_parser.clean_gcommand_line(sstate)
    state_label, _ = dtmc_parser.process_state_label(sstate)
    assert(state_label == 'a0=3,a1=3,a2=3,b=0')
    sstate = "(a0'=1) & (a1'=1) & (a2'=1)"
    sstate = dtmc_parser.clean_gcommand_line(sstate)
    state_label, _ = dtmc_parser.process_state_label(sstate)
    assert(state_label == 'a0=1,a1=1,a2=1,b=0')


def test_extract_state(dtmc_parser):
    dtmc_parser.process()
    assert(len(dtmc_parser.state_list) == 11)
    print('BSCC list of size \n',
          len(dtmc_parser.bscc_list),
          dtmc_parser.bscc_list)


def test_extract_bscc(dtmc_parser):
    for b in dtmc_parser.bscc_list:
        assert(b in dtmc_parser.state_list)


def test_extract_edges(dtmc_parser):
    pass


def test_expr_process(dtmc_parser):
    expr_str = '3.0*r_0*r_0*(1-r_0)'
    assert(dtmc_parser.process_expression(expr_str) == '3.0*r[0]*r[0]*(1-r[0])')


def test_simplify(dtmc_parser):
    expr_str = '1.0*(1-r_0)*(1-r_0)*(1-r_0)'
    dtmc_parser.can_simplify = True
    expr_str = dtmc_parser.process_expression(expr_str)
    expr_str = expr_str.replace(' ', '')
    expected = '-1.0*(r[0]-1)**3'
    assert(expr_str == expected)


def test_build_vector(dtmc_parser):
    pass

def test_build_matrix(dtmc_parser):
    dtmc_parser.process()
    print('Initial vector:')
    for iv in dtmc_parser.init_str_pfuncs:
        print(iv)
    print('Transition matrix:')
    for row in dtmc_parser.trans_str_pfuncs:
        print(row)
