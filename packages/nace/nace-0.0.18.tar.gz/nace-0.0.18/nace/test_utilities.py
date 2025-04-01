"""

utilities to aid in test classes.

"""
import copy
import numpy as np

import nace
# from nace.nace_v3 import _get_rc_delta_for_action_list

def convert_focus_set_to_internal_mapping(focus_set, world):
    result = {}
    for ch in focus_set.keys():
        val = world.get_val_for_char(ch)
        result[val] = focus_set[ch]
    return result

def convert_focus_set_to_char_mapping(focus_set, world):
    # defining things in chars is nice for unit tests, but useless in practice as too few states can be held.
    # give a way to convert rules that are used in prod into a nice unit test version.

    mappings = world.get_val_to_char_mappings(list_of_extra_values = [ k for k in focus_set.keys()])
    result = {}
    for val in focus_set.keys():
        if val in mappings:
            ch = mappings[val]
        else:
            print("ERROR R26")

        result[ch] = focus_set[val]
    return result


def convert_rules_to_internal_mapping(rules, world):
    result = set()
    for rule in rules:
        precondition, effect = rule
        new_precondition = list(precondition)
        new_effect = list(effect)
        new_effect[2] = world.get_val_for_char(new_effect[2])
        new_effect = tuple(new_effect)
        for outer_index, element in enumerate(new_precondition):
            if isinstance(element, tuple):
                if len(element) == 3:
                    element = list(element)
                    element[2] = world.get_val_for_char(element[2])
                    new_precondition[outer_index] = tuple(element)
        result.add( (tuple(new_precondition), new_effect )  )
    return result

def convert_rule_evidence_to_internal_mapping(rule_evidence, world):
    result = {}
    for rule in rule_evidence.keys():
        precondition, effect = rule
        new_precondition = list(precondition)
        new_effect = list(effect)
        new_effect[2] = world.get_val_for_char(new_effect[2])
        new_effect = tuple(new_effect)
        for outer_index, element in enumerate(new_precondition):
            if isinstance(element, tuple):
                if len(element) == 3:
                    element = list(element)
                    element[2] = world.get_val_for_char(element[2])
                    new_precondition[outer_index] = tuple(element)
        new_rule = tuple((tuple(new_precondition), new_effect ))
        result[new_rule] = rule_evidence[rule]
    return result


def convert_rule_evidence_to_char_or_int_mappings(rule_evidence, world, dest="CHAR"):
    char_rule_evidence = {}
    for rule in rule_evidence.keys():
        t_char_rules, t_encoded_rules = convert_rules_to_char_or_int_mappings([rule], world, dest=dest)
        char_rule_evidence[t_encoded_rules[0]] = rule_evidence[rule]
    return char_rule_evidence


def convert_rules_to_char_or_int_mappings(rules, world, dest="CHAR"):
    # defining things in chars is nice for unit tests, but useless in practice as too few states can be held.
    # give a way to convert rules that are used in prod into a nice unit test version.


    # NOTE the row and column in the effect are always zero and not currently used.

    list_of_extra_values = [rule[1][2] for rule in rules if rule is not None]
    mappings = world.get_val_to_char_mappings(list_of_extra_values)
    initial_results = []
    values_to_order_by = []
    for rule in rules:
        precondition, effect = rule
        new_precondition = list(precondition)
        new_precondition[0] = nace.prettyprint.get_pretty_action(new_precondition[0])
        new_effect = list(effect)
        if dest == "CHAR":
            if new_effect[2] in mappings:
                new_effect[2] = mappings[new_effect[2]]
            else:
                pass # we can not decode the item, leave it in its raw state.
        else:
            if isinstance(new_effect[2], int):
                pass # already an int
            else:
                new_effect[2] = new_effect[2].item()
        for outer_index, element in enumerate(new_precondition):
            if isinstance(element, tuple):
                if len(element) == 3:
                    if dest == "CHAR":
                        element = list(element)
                        if element[2] in mappings:
                            element[2] = mappings[element[2]]
                            values_to_order_by.append(element[2])
                        else:
                            mappings2 = world.get_val_to_char_mappings(list_of_extra_values=[element[2]])
                            if element[2] in mappings2:
                                element[2] = mappings2[element[2]]
                                values_to_order_by.append(element[2])
                            else:
                                _ = world.get_val_for_char(element[2])
                                print("WARN: error converting value to char, being left as is.", element[2])
                    else:
                        # INT
                        element = list(element)
                        if isinstance(element[2], int):
                            pass # already an int
                        else:
                            element[2] = element[2].item()
                        values_to_order_by.append(element[2])
                    new_precondition[outer_index] = tuple(element)
        initial_results.append( (tuple(new_precondition), tuple(new_effect) )  )

    # get an ordered set of all the chars at 0,0 in each rule
    values_to_order_by = list(set(values_to_order_by))
    for i, result in enumerate(copy.deepcopy(initial_results)):
        precondition, effect = result
        for condition in precondition[2:]:
            if condition[0] == 0 and condition[1] == 0:
                values_to_order_by.append(condition[2])
    values_to_order_by = list(set(values_to_order_by))
    try:
        values_to_order_by.sort()
    except TypeError as e:
        print("WARN trying to sort str and int caused an error which has been supressed.")
        pass # had mixed typed in the list. this is a temp work around.

    # order the rules (for ease of debugging)
    ordered_results = []
    order_results_as_str = "[\n"
    for value in values_to_order_by:
        not_yet_commented = True
        for i, result in enumerate(copy.deepcopy(initial_results)):
            precondition, effect = result
            matches = False
            for condition in precondition[2:]:
                if condition[0] == 0 and condition[1] == 0 and condition[2] == value:
                    matches = True
            if matches:
                ordered_results.append(result)
                order_results_as_str += str(result)+","
                if not_yet_commented:
                    not_yet_commented = False
                    order_results_as_str += " # "+str(value)
                order_results_as_str += "\n"

        for result in ordered_results:
            if result in initial_results:
                initial_results.remove(result)

    order_results_as_str += "]"
    assert len(initial_results) == 0

    return order_results_as_str, ordered_results






def get_xy_delta_for_action_list(action_list):
    # DO NOT call this routine, we are moving to r,c everywhere
    # ignores walls etc.
    print("WARN: MOVE to rc, do not use xy.")
    r,c = get_rc_delta_for_action_list(action_list)
    return (c,r)

def get_rc_delta_for_action_list(action_list):
    # ignores walls etc. only good for test code
    return nace.nace_v3._get_rc_delta_for_action_list(action_list)

def get_time_and_board_at_destination(list_of_xy: list, world: nace.world_module_numpy.NPWorld):
    x = sum([r[0] for r in list_of_xy])
    y = sum([r[1] for r in list_of_xy])
    return world.times[y][x], world.board[y][x]

