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


def Prettyprint_Plan(actionlist):
    return [get_pretty_action(x) for x in actionlist[1:]]


def prettyprint_all_actions(actionlist):
    return [get_pretty_action(x) for x in actionlist]


def pp_val(val, val_to_char_mappings):
    # return the char value of the board (if there is one), rather than the internal int value
    if val in val_to_char_mappings:
        return f"'{val_to_char_mappings[val]}'"
    else:
        return f"{val}"


def prettyprint_rule(rule_evidence, Hypothesis_TruthValue, rule, val_to_char_mappings={},
                     print_evidence=False, print_truth_value=True):

    assert rule in rule_evidence

    actions_values_preconditions = rule[0]
    action = get_pretty_action(actions_values_preconditions[0])
    precons = actions_values_preconditions[2:]
    line = "<("
    line += "AgentStatePreCon=" + str(list(actions_values_preconditions[1]))+", "

    for i, x in enumerate(precons):
        line += f"{_prettyTriplet(x, val_to_char_mappings)}"
        if i != len(precons) - 1:
            line += f", "

    scoreInc = f"score+={rule[1][3][0]}"
    keys = f"AgentStatePreCon={list(rule[1][3][1:])}"
    action = action.rjust(6) # print actions with same width

    evidence = ""
    truth_value = ""
    if print_evidence:
        evidence = " evidence="+str(rule_evidence[rule])
    if print_truth_value:
        truth_value = " TruthValue="+str(Hypothesis_TruthValue(rule_evidence[rule]))

    line += (","+ action +  ")" +
             "=/> (" + keys + ", " + str(_prettyTriplet(rule[1],val_to_char_mappings)) + ", " + scoreInc + ")>."
               +truth_value+evidence)

    # print(line)
    return line


def _prettyTriplet(triplet, val_to_char_mappings):
    (r, c, value) = triplet[:3]
    if r >= 0: r = " " + str(r)
    if c >= 0: c = " " + str(c)
    str_val = pp_val(value, val_to_char_mappings)
    return "rc[" + str(r) + "," + str(c) + f" ]={str_val}"


def get_pretty_action(action):
    if str(action).find("<function ") > -1:
        return "" + str(action).split("<function ")[1].split(" at")[0]
    else:
        return "" + str(action)
