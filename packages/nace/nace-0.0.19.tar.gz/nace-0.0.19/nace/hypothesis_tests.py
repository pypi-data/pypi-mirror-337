
import nace
from nace.hypothesis import (Hypothesis_BestSelection, Hypothesis_Confirmed, Hypothesis_TruthValue)


def t1_hypothesis():

    rules = \
        {(('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0, 0))),
         (('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0, 0))),
         (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))),
         (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))),
         (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0, 0))),
         (('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0, 0))),
         (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))),
         (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0)))}
    rules_excluded = set()
    rule_evidence = \
        {(('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0, 0))): (1, 0),
         (('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0, 0))): (1, 0),
         (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))): (1, 0),
         (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))): (1, 0),
         (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))): (1, 5), # neg > pos evidence
         (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))): (1, 0),
         (('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0, 0))): (1, 0),
         (('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0, 0))): (1, 0)}
    stayed_the_same = False


    print("Rules with evidence:")
    for rule in rules:
        line = nace.prettyprint.prettyprint_rule(rule_evidence, Hypothesis_TruthValue, rule, print_evidence=True)
        print(line)

    new_rules, rules_excluded = Hypothesis_BestSelection(rules, rules_excluded, rule_evidence, stayed_the_same)

    print("Rules Excluded:")
    for rule in rules_excluded:
        line = nace.prettyprint.prettyprint_rule(rule_evidence, Hypothesis_TruthValue, rule, print_evidence=True)
        print(line)

    # expect 1 line to be excluded as it had more -ve evidence.
    assert len(rules_excluded) == 1


def t2_hypothesis():
    focus_set = {'x': 1}
    negruleset = set()
    rule = (('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0, 0)))
    rule_evidence = {}
    rule_set = set()

    rule_evidence, ruleset = Hypothesis_Confirmed(focus_set, rule_evidence, rule_set, negruleset, rule,
                                                  val_to_char_mappings={})
    assert len(rule_evidence) == 1  # 1 action, 1 rule
    # could also assert that they are all symmetrical


if __name__ == "__main__":
    t1_hypothesis()
    t2_hypothesis()
