from nace.hypothesis import Hypothesis_TruthValue
from nace.prettyprint import prettyprint_rule

def t1_pp_rule():
    rule_evidence = {(('right', (0,), (0, 0, 'x'), (0, 1, 'o')), (0, 0, ' ', (-1, 0))): (1, 0)}
    rule = (('right', (0,), (0, 0, 'x'), (0, 1, 'o')), (0, 0, ' ', (-1, 0)))
    line = prettyprint_rule(rule_evidence, Hypothesis_TruthValue, rule)
    print(line)
    assert line == "<(AgentStatePreCon=[0], rc[ 0, 0 ]=x, rc[ 0, 1 ]=o, right)=/> (AgentStatePreCon=[0], rc[ 0, 0 ]= , score+=-1)>. TruthValue=(1.0, 0.5)"

if __name__ == "__main__":
    t1_pp_rule()

