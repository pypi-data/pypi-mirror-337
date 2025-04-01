"""
 * The MIT License
 *
 * Copyright (c) 2024 Patrick Hammer
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 * """

import random
import sys
from copy import deepcopy

# from numba import jit

from nace.prettyprint import prettyprint_rule


    # global DisableLRUDOpSymmetryAssumption
    # DisableLRUDOpSymmetryAssumption = True # hmmm bad double negative



# @jit(nopython=True)
def Hypothesis_TruthValue(wpn):
    """
    # The truth value of a hypothesis can be obtained directly from the positive and negative evidence counter

    @param wpn:
    @return:
    """
    (wp, wn) = wpn
    frequency = wp / (wp + wn)
    confidence = (wp + wn) / (wp + wn + 1)
    return frequency, confidence


# @jit(nopython=True)
def _TruthExpectation(tv):
    """
    # The truth expectation calculation based on the truth value (frequency, confidence) tuple

    @param tv: truth value made up from frequency and confidence
    @return:
    """
    (f, c) = tv
    return c * (f - 0.5) + 0.5


def _Choice(rule_evidence, rule1, rule2):
    """
    # When two hypotheses predict a different outcome for the same conditions, the higher truth exp one is chosen

    @param rule_evidence:
    @param rule1:
    @param rule2:
    @return:
    """
    if rule1 in rule_evidence and rule2 not in rule_evidence:  # dv added (no longer triggered)
        return rule1
    if rule1 not in rule_evidence and rule2 in rule_evidence:  # dv added (no longer triggered)
        return rule2
    if rule1 not in rule_evidence and rule2 not in rule_evidence:  # dv added (no longer triggered)
        # panic
        print("ERROR this suggests a logic error in calling code.")
        return rule2

    t1 = Hypothesis_TruthValue(rule_evidence[rule1])
    t2 = Hypothesis_TruthValue(rule_evidence[rule2])
    if _TruthExpectation(t1) > _TruthExpectation(t2):
        return rule1
    return rule2


def Hypothesis_Contradicted(rule_evidence, ruleset, negruleset, rule, val_to_char_mappings):  # this mutates returned copy of rule_evidence
    """
    # Negative evidence was found for the hypothesis/rule

    @param rule_evidence:
    @param ruleset:
    @param negruleset:
    @param rule:
    @return:
    """
    rule_evidence = _AddEvidence(rule_evidence, rule, False)  # mutates returned copy of rule_evidence
    if "silent" not in sys.argv:
        print("Neg. revised: ", end="")
        line = prettyprint_rule(rule_evidence, Hypothesis_TruthValue, rule, val_to_char_mappings)
        print(line)
        # in a deterministic setting this would have sufficed however
        # simply excluding rules does not work in non-deterministic ones
        # if rule in ruleset:
        #    print("RULE REMOVAL: ", end=""); Prettyprint_rule(rule_evidence, Hypothesis_TruthValue, rule)
        #    ruleset.remove(rule)
        # negruleset.add(rule)
    return rule_evidence, ruleset, negruleset


def Hypothesis_Confirmed(  # this mutates the returned rule_evidence and ruleset
        FocusSet, rule_evidence, ruleset, negruleset, rule, val_to_char_mappings:dict
):
    """
    # Positive evidence was found for the hypothesis/rule
    # Confirm rule against +ve and -ve evidence, add variants (i.e. transforms) to newrules.

    @param FocusSet:
    @param rule_evidence: dict[rule:(+ve_evidence, -ve_evidence)]
    @param ruleset:
    @param negruleset:
    @param rule:
    @return:
    """

    rule_evidence = deepcopy(rule_evidence)  # dv added this line
    # try location symmetry
    variants = [rule]

    for i, r in enumerate(variants):
        if i > 0:  # abduced hypotheses
            if r in rule_evidence:  # this derived hypothesis already exists
                continue
        rule_evidence = _AddEvidence(rule_evidence, r, True)  # mutates returned copy of rule_evidence
        if "silent" not in sys.argv:
            print("Pos. revised: ", end="")
            line = prettyprint_rule(rule_evidence, Hypothesis_TruthValue, r, val_to_char_mappings)
            print(line)
        if r not in negruleset:
            if r not in ruleset:
                # print("RULE ADDITION: ", end=""); Prettyprint_rule(rule)
                ruleset.add(r)
    return rule_evidence, ruleset


def Hypothesis_ValidCondition(cond):
    """
    # Valid condition predicate defining the accepted neighbourhood between conclusion and condition cells
    # restrict to neighbours (CA assumption)
    # If 0,1, or 2 in distance in any direction, return True, else False

    @param cond:
    @return:
    """
    (y, x, v) = cond
    if y == 0 and x == 0:  # self
        return True
    if y == 0 and (x == -1 or x == -2):  # left
        return True
    if (y == -1 or y == -2) and x == 0:  # up
        return True
    if y == 0 and (x == 1 or x == 2):  # right
        return True
    if (y == 1 or y == 2) and x == 0:  # down
        return True

    # Does this break the CA assumption? what is the CA assumption?

    if abs(y) == 1 and abs(x) == 1:
        # diagonal is being allowed, dec 2024, for deepsea and frozen lake.
        return True

    return False


def Hypothesis_BestSelection(rules, rules_excluded, rule_evidence,
                             include_random_rules):  # mutates returned rules, returned rulesExcluded
    """

    We exclude rules which have more negative evidence than positive, and choose the highest truth-exp ones whenever
    a different outcome would be predicted for the same conditions

    @param rules:
    @param rules_excluded:
    @param rule_evidence:
    @param include_random_rules: World stayed the same when last ground truth copied in - if true stochastic element added
    @return:
    """
    rules = deepcopy(rules)    # ensure we don't mutated passed in data structures.
    rules_excluded = deepcopy(rules_excluded)
    rule_evidence = deepcopy(rule_evidence)


    rulesin = deepcopy(rules)
    rules_moved_count_1 = 0
    rules_moved_count_2 = 0
    rules_moved_count_3 = 0
    for i, rule1 in enumerate(rulesin):
        # if Hypothesis_TruthExpectation(Hypothesis_TruthValue(rule_evidence[rule1])) <= 0.5: #exclude rules which
        # are not better than exp (only 0.5+ makes sense here)
        if rule1 in rule_evidence:  # dv 8/jul/24 added to stop key not found which hadn't happened before
            te = _TruthExpectation(Hypothesis_TruthValue(rule_evidence[rule1]))
            if te <= 0.5 or (
                    include_random_rules
                    and random.random()
                    > _TruthExpectation(Hypothesis_TruthValue(rule_evidence[rule1]))
            ):
                if rule1 in rules:
                    rules_excluded.add(rule1)
                    rules.remove(rule1)
                    rules_moved_count_1 += 1
    rulesin = deepcopy(rules)
    for i, rule1 in enumerate(rulesin):
        for j, rule2 in enumerate(rulesin):
            if (
                    i != j
            ):  # exclude rules of same precondition which are worse by truth value
                if rule1[0] == rule2[0]:
                    rulex = _Choice(rule_evidence, rule1, rule2)
                    if rulex == rule1:
                        if rule2 in rules:
                            rules_excluded.add(rule2)
                            rules.remove(rule2)
                            rules_moved_count_2 += 1
                            # print("excluded ", end=''); Prettyprint_rule(rule2)
                    else: # best rule is rule2, so remove rule1
                        if rule1 in rules:
                            rules_excluded.add(rule1)
                            rules.remove(rule1)
                            rules_moved_count_3 += 1
                            # print("excluded", end=''); Prettyprint_rule(rule1)
    print("DEBUG Rules excluded for predictions:  rules_less_than_truth_value_less_than_half=", rules_moved_count_1, "same_precondition_worse_truth_value=", (rules_moved_count_2+ rules_moved_count_3), "active_rules=", len(rules) )

    return rules, rules_excluded


def _AddEvidence(rule_evidence, rule, positive, w_max=20):  # Mutates a copy of rule_evidence
    """
    Add positive or negative evidence for a rule, with a certain max. amount of evidence so that non-stationary
    environments can be handled too

    @param rule_evidence:
    @param rule:
    @param positive:
    @param w_max:
    @return:
    """
    rule_evidence = deepcopy(rule_evidence)
    if rule not in rule_evidence:
        rule_evidence[rule] = (0, 0)
    (wp, wn) = rule_evidence[rule]
    if positive:
        if wp + wn <= w_max:
            rule_evidence[rule] = (wp + 1, wn)
        else:
            rule_evidence[rule] = (wp, max(0, wn - 1))
    else:
        if wp + wn <= w_max:
            rule_evidence[rule] = (wp, wn + 1)
        else:
            rule_evidence[rule] = (max(0, wp - 1), wn)
    return rule_evidence
