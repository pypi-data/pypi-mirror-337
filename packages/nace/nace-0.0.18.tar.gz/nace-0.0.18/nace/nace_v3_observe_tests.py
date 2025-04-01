import copy
import random

import nace

from nace.nace_v3 import _predict_next_world_state, _refine_rules_from_changesets, _build_change_sets, _observe_v2
from nace.test_utilities import convert_focus_set_to_internal_mapping, convert_rules_to_internal_mapping

from nace.agent_module import Agent
from nace.test_utilities import (convert_focus_set_to_internal_mapping, convert_rules_to_internal_mapping,
                                 convert_rule_evidence_to_internal_mapping,
                                 convert_rules_to_char_or_int_mappings)

def place_agent_and_object(input_world_str_list, input_agent, desired_agent_rc_loc, desired_object_rc_loc, object_char, agent_char, int_2from_char_mapping):
    world_str_list = copy.deepcopy(input_world_str_list)
    world_str_list[desired_agent_rc_loc[0]] = world_str_list[desired_agent_rc_loc[0]][:desired_agent_rc_loc[1]] + agent_char + world_str_list[desired_agent_rc_loc[0]][desired_agent_rc_loc[1] + 1:]
    world_str_list[desired_object_rc_loc[0]] = world_str_list[desired_object_rc_loc[0]][:desired_object_rc_loc[1]] + object_char + world_str_list[desired_object_rc_loc[0]][desired_object_rc_loc[1] + 1:]
    world, _ = nace.world_module_numpy.NPWorld.from_string(
        world_str_list,
        view_dist_x=12,
        view_dist_y=5,
        agent_char_code_list=[agent_char], # must match actual agent char
        observed_times_str_list=[],
        int_2from_char_mapping=int_2from_char_mapping
    )
    agent = Agent(desired_agent_rc_loc, input_agent.get_score(), input_agent.get_terminated(), input_agent.get_values_exc_prefix())
    return world, agent


def t3_cup_on_table():
    """
    Test we add rules that add +1 to score for putting the cup on the table.
    @return:
    """

    original_focus_set = {'T': 0, 'u': 9, 'x': 65}
    original_rule_evidence = {(('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0, 0))): (1, 0), (('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0, 0))): (1, 0), (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))): (1, 0), (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))): (1, 0), (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))): (1, 0), (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))): (1, 0), (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0, 0))): (1, 0), (('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0, 0))): (1, 0), (('left', (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0, 0))): (1, 0), (('up', (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0, 0))): (1, 0), (('right', (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0, 0))): (1, 0), (('down', (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0, 0))): (1, 0), (('down', (0,), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0, 0))): (1, 0), (('left', (0,), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0, 0))): (1, 0), (('up', (0,), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0, 0))): (1, 0), (('right', (0,), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0, 0))): (2, 0), (('down', (0,), (0, 0, 'x'), (1, 0, 'T')), (0, 0, 'x', (0, 0))): (1, 0), (('left', (0,), (0, -1, 'T'), (0, 0, 'x')), (0, 0, 'x', (0, 0))): (1, 0), (('up', (0,), (-1, 0, 'T'), (0, 0, 'x')), (0, 0, 'x', (0, 0))): (1, 0), (('right', (0,), (0, 0, 'x'), (0, 1, 'T')), (0, 0, 'x', (0, 0))): (1, 0), (('down', (0,), (-1, 0, 'x'), (0, 0, 'T')), (0, 0, 'T', (0, 0))): (1, 0), (('left', (0,), (0, 0, 'T'), (0, 1, 'x')), (0, 0, 'T', (0, 0))): (1, 0), (('up', (0,), (0, 0, 'T'), (1, 0, 'x')), (0, 0, 'T', (0, 0))): (1, 0), (('right', (0,), (0, -1, 'x'), (0, 0, 'T')), (0, 0, 'T', (0, 0))): (1, 0), (('right', (0,), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0, 0))): (1, 0), (('down', (0,), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0, 0))): (1, 0), (('left', (0,), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0, 0))): (1, 0), (('up', (0,), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0, 0))): (1, 0)}
    original_rules = {(('left', (0,), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0, 0))), (('up', (0,), (0, 0, 'T'), (1, 0, 'x')), (0, 0, 'T', (0, 0))), (('right', (0,), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0, 0))), (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))), (('left', (0,), (0, 0, 'T'), (0, 1, 'x')), (0, 0, 'T', (0, 0))), (('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0, 0))), (('up', (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0, 0))), (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0, 0))), (('left', (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0, 0))), (('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0, 0))), (('right', (0,), (0, 0, 'x'), (0, 1, 'T')), (0, 0, 'x', (0, 0))), (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))), (('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0, 0))), (('left', (0,), (0, -1, 'T'), (0, 0, 'x')), (0, 0, 'x', (0, 0))), (('right', (0,), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0, 0))), (('down', (0,), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0, 0))), (('up', (0,), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0, 0))), (('up', (0,), (-1, 0, 'T'), (0, 0, 'x')), (0, 0, 'x', (0, 0))), (('down', (0,), (-1, 0, 'x'), (0, 0, 'T')), (0, 0, 'T', (0, 0))), (('down', (0,), (0, 0, 'x'), (1, 0, 'T')), (0, 0, 'x', (0, 0))), (('right', (0,), (0, -1, 'x'), (0, 0, 'T')), (0, 0, 'T', (0, 0))), (('left', (0,), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0, 0))), (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))), (('right', (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0, 0))), (('down', (0,), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0, 0))), (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))), (('down', (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0, 0))), (('up', (0,), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0, 0)))}

    original_agent = nace.agent_module.Agent(rc_loc=[2, 10], score=0, terminated=0, values_excluding_prefix=[0])
    new_agent = nace.agent_module.Agent(rc_loc=[2, 9], score=1, terminated=0, values_excluding_prefix=[0])
    predicted_agent = nace.agent_module.Agent(rc_loc=[2, 9], score=1, terminated=0, values_excluding_prefix=[0])
    action = 'left'
    original_negrules = set()

    oldworld_string_list = (
        ['oooooooooooo','o          o','o        uxo','o     ooooTo','o          o','o          o','oooooooooooo'],
        (0, 0), ['38,44,49,54,59,64,65,67,67,67,67,67','38,44,49,54,59,64,65,67,67,67,67,67','38,44,49,54,59,64,65,67,67,67,67,67','38,44,49,54,59,64,65,67,67,67,67,67','38,44,49,54,59,64,64,67,67,67,67,67','34,34,34,34,34,34,34,31,30,29,28,27','33,33,33,33,33,33,33,31,30,29,28,27'])
    oldworld, old_agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        oldworld_string_list[0],
        view_dist_x=3,
        view_dist_y=2,
        agent_char_code_list=['x'],
        observed_times_str_list=oldworld_string_list[2]
    )

    newworld_string_list = (
        ['oooooooooooo','o          o','o        xuo','o     ooooTo','o          o','o          o','oooooooooooo'],
        (0,0), ['38,44,49,54,59,64,65,68,68,68,68,68','38,44,49,54,59,64,65,68,68,68,68,68','38,44,49,54,59,64,65,68,68,68,68,68','38,44,49,54,59,64,65,68,68,68,68,68','38,44,49,54,59,64,64,68,68,68,68,68','34,34,34,34,34,34,34,31,30,29,28,27','33,33,33,33,33,33,33,31,30,29,28,27'])
    newworld, new_agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        newworld_string_list[0],
        view_dist_x=3,
        view_dist_y=2,
        agent_char_code_list=['x'],
        observed_times_str_list=oldworld_string_list[2])


    encoded_focus_set = convert_focus_set_to_internal_mapping(original_focus_set, oldworld)
    encoded_rules = convert_rules_to_internal_mapping(original_rules, oldworld)
    encoded_negrules = convert_rules_to_internal_mapping(original_negrules, oldworld)



    # Call observe in order to learn dynamics
    calculated_focus_set, calculated_rule_evidence, calculated_new_rules, calculated_new_negrules = _observe_v2(
        encoded_focus_set, original_rule_evidence, oldworld, action, newworld, encoded_rules, encoded_negrules,
        newworld, pre_action_agent=original_agent, ground_truth_post_action_agent=new_agent,
        predicted_agent=predicted_agent,
        unobserved_code='.',
        object_count_threshold=1
    )

    print("New Rules:")
    rules_that_increase_score_count = 0
    for rule in calculated_new_rules:
        prediction_state_value_deltas = rule[1]
        state_value_deltas = prediction_state_value_deltas[-1]
        # print('prediction_state_value_deltas', prediction_state_value_deltas)
        if state_value_deltas[0] > 0:
            rules_that_increase_score_count += 1
            line = nace.prettyprint.prettyprint_rule(rule_evidence=calculated_rule_evidence,
                                                     Hypothesis_TruthValue=nace.hypothesis.Hypothesis_TruthValue,
                                                     rule=rule
                                                     )
            print(line)

    print("INFO rules_that_increase_score_count", rules_that_increase_score_count)
    assert rules_that_increase_score_count == 2 # was 8, will be 2 if we do not assume eucldian rules.
    # ideally we would rebuild or edit all the rules to include the terminated flag in precondition. # expect 2 rules for each action (1 for source cell, 1 for dest) * 4 actions == 8 new rules



def t1_simple_move_left():
    """
    Move left, check new rules are derived.

    @return:
    """

    original_focus_set = { 'x': 65}
    original_rule_evidence = {}
    original_rules = set()

    old_agent = nace.agent_module.Agent(rc_loc=[2, 9], score=0, terminated=0, values_excluding_prefix=[0])
    new_agent = nace.agent_module.Agent(rc_loc=[2, 8], score=0, terminated=0, values_excluding_prefix=[0])
    action = 'left'
    original_negrules = set()

    oldworld_string_list = (
        ['oooooooooooo','o          o','o        x o','o          o','o          o','o          o','oooooooooooo'],
        (0, 0), ['38,44,49,54,59,64,65,67,67,67,67,67','38,44,49,54,59,64,65,67,67,67,67,67','38,44,49,54,59,64,65,67,67,67,67,67','38,44,49,54,59,64,65,67,67,67,67,67','38,44,49,54,59,64,64,67,67,67,67,67','34,34,34,34,34,34,34,31,30,29,28,27','33,33,33,33,33,33,33,31,30,29,28,27'])

    oldworld, old_agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        oldworld_string_list[0],
        view_dist_x=3,
        view_dist_y=2,
        agent_char_code_list=['x'],
        observed_times_str_list=oldworld_string_list[2]
    )

    newworld_string_list = (
        ['oooooooooooo','o          o','o       x  o','o          o','o          o','o          o','oooooooooooo'],
        (0,0), ['38,44,49,54,59,64,65,68,68,68,68,68','38,44,49,54,59,64,65,68,68,68,68,68','38,44,49,54,59,64,65,68,68,68,68,68','38,44,49,54,59,64,65,68,68,68,68,68','38,44,49,54,59,64,64,68,68,68,68,68','34,34,34,34,34,34,34,31,30,29,28,27','33,33,33,33,33,33,33,31,30,29,28,27'])
    new_world, new_agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        newworld_string_list[0],
        view_dist_x=3,
        view_dist_y=2,
        agent_char_code_list=['x'],
        observed_times_str_list=newworld_string_list[2]
    )

    encoded_focus_set = convert_focus_set_to_internal_mapping(original_focus_set, oldworld)
    encoded_rules = convert_rules_to_internal_mapping(original_rules, oldworld)
    encoded_negrules = convert_rules_to_internal_mapping(original_negrules, oldworld)
    encoded_rule_evidence = original_rule_evidence
    predicted_world, predicted_agent, _, __, values, predicted_score_delta = _predict_next_world_state(
        encoded_focus_set,
        copy.deepcopy(oldworld), action, encoded_rules, old_agent
    )

    new_world.multiworld_print([
        {"World": oldworld,       "Caption":"Old",  "Color": nace.color_codes.color_code_white_on_blue},
        {"World": predicted_world, "Caption":"Pred\nNo Rule, Empty Pred", "Color": nace.color_codes.color_code_white_on_blue},
        {"World": new_world,       "Caption":"New",  "Color": nace.color_codes.color_code_white_on_blue},
    ])

    # Call the function
    calculated_focus_set, calculated_rule_evidence, calculated_new_rules, calculated_new_negrules = _observe_v2(
        encoded_focus_set, encoded_rule_evidence, oldworld, action, new_world, encoded_rules, encoded_negrules,
        predicted_world, pre_action_agent=old_agent, ground_truth_post_action_agent=new_agent,
        predicted_agent=predicted_agent,
        unobserved_code='.',
        object_count_threshold=1
    )

    print("About to check the rules with the action 'left', We expect 8 rules in total, but only if rules are expanded for eurclidean space, 2 rules where the action is left, One for where the agent was, one for where the agent goes to.")
    print("calculated_new_rules",calculated_new_rules)
    assert len(calculated_new_rules) == 2
    left_rule_count = 0
    for rule in calculated_new_rules:
        if rule[0][0] == action:
            nace.prettyprint.prettyprint_rule(rule_evidence=calculated_rule_evidence,
                                              Hypothesis_TruthValue=nace.hypothesis.Hypothesis_TruthValue,
                                              rule=rule
                                              )
            prediction_state_value_deltas = rule[1]
            state_value_deltas = prediction_state_value_deltas[-1]
            left_rule_count += 1
    assert left_rule_count == 2 # we expect 2 rules, i.e. 2 cell values change


def t2_simple_move_left_get_moved_left_and_down():
    """
    Move left, check new rules are derived.

    @return:
    """


    original_focus_set = {}
    original_rule_evidence = {}
    oldrules = set()

    old_agent = nace.agent_module.Agent(rc_loc=[2, 9], score=0, terminated=0, values_excluding_prefix=[0])
    new_agent = nace.agent_module.Agent(rc_loc=[3, 8], score=0, terminated=0, values_excluding_prefix=[0])
    action = 'left'
    oldnegrules = set()

    oldworld_string_list = (
        ['oooooooooooo','o          o','o        x o','o          o','o          o','o          o','oooooooooooo'],
        (0, 0), ['38,44,49,54,59,64,65,67,67,67,67,67','38,44,49,54,59,64,65,67,67,67,67,67','38,44,49,54,59,64,65,67,67,67,67,67','38,44,49,54,59,64,65,67,67,67,67,67','38,44,49,54,59,64,64,67,67,67,67,67','34,34,34,34,34,34,34,31,30,29,28,27','33,33,33,33,33,33,33,31,30,29,28,27'])
    old_world, _2 = nace.world_module_numpy.NPWorld.from_string(
        oldworld_string_list[0],
        view_dist_x=30,
        view_dist_y=20,
        agent_char_code_list=['x'],
        observed_times_str_list=oldworld_string_list[2]
    )

    newworld_string_list = (
        ['oooooooooooo','o          o','o          o','o       x  o','o          o','o          o','oooooooooooo'],
        (0,0), ['38,44,49,54,59,64,65,68,68,68,68,68','38,44,49,54,59,64,65,68,68,68,68,68','38,44,49,54,59,64,65,68,68,68,68,68','38,44,49,54,59,64,65,68,68,68,68,68','38,44,49,54,59,64,64,68,68,68,68,68','34,34,34,34,34,34,34,31,30,29,28,27','33,33,33,33,33,33,33,31,30,29,28,27'])
    new_world, _1 = nace.world_module_numpy.NPWorld.from_string(
        newworld_string_list[0],
        view_dist_x=30,
        view_dist_y=20,
        agent_char_code_list=['x'],
        observed_times_str_list=oldworld_string_list[2]
    )

    predicted_world, predicted_agent, _, __, values, predicted_score_delta = _predict_next_world_state(
        original_focus_set,
        copy.deepcopy(old_world), action, oldrules, old_agent
    )

    new_world.multiworld_print([
        {"World": old_world,       "Caption":"Old",  "Color": nace.color_codes.color_code_white_on_blue},
        {"World": predicted_world, "Caption":"Pred", "Color": nace.color_codes.color_code_white_on_blue},
        {"World": new_world,       "Caption":"New",  "Color": nace.color_codes.color_code_white_on_blue},
    ])


    # # call the split method
    # calculated_focus_set_v2, calculated_rule_evidence_v2, calculated_new_rules_v2, calculated_new_negrules_v2 = _observe_v2(
    #     copy.deepcopy(original_focus_set), copy.deepcopy(original_rule_evidence), old_world, action, new_world, copy.deepcopy(oldrules), copy.deepcopy(oldnegrules),
    #     predicted_world, pre_action_agent=old_agent, ground_truth_post_action_agent=new_agent, unobserved_code='.',
    #     object_count_threshold=1
    # )
    #
    # #

    # # # call the function in 2 parts.
    new_focus_set, adjacent_change_sets, changeset0len = _build_change_sets(
        original_focus_set,
        old_world,
        action,
        new_world,
        predicted_world,
    )
    assert len(adjacent_change_sets) == 1
    assert adjacent_change_sets[0] == {(2,8), (2, 9), (3, 8)} # ideally would only be 2 cells (2, 9), (3, 8)

    adjacent_change_sets = [{(2, 9), (3, 8)}]
    changeset0len = 2

    calculated_focus_set2, calculated_rule_evidence2, calculated_new_rules2, calculated_new_negrules2 = _refine_rules_from_changesets(original_focus_set,
                                  original_rule_evidence,
                                  old_world,
                                  action,
                                  new_world,
                                  oldrules,
                                  old_agent,
                                  new_agent,
                                  predicted_agent,
                                  adjacent_change_sets,
                                  copy.deepcopy(oldnegrules),
                                  changeset0len
    )

    print("About to check the rules with the action 'left', We expect 2/8 rules to be left.")
    left_rule_count = 0
    for rule in calculated_new_rules2:
        if rule[0][0] == action:
            line = nace.prettyprint.prettyprint_rule(rule_evidence=calculated_rule_evidence2,
                                                     Hypothesis_TruthValue=nace.hypothesis.Hypothesis_TruthValue,
                                                     rule=rule
                                                     )
            print(line)
            prediction_state_value_deltas = rule[1]
            state_value_deltas = prediction_state_value_deltas[-1]
            left_rule_count += 1
    assert left_rule_count == 2 # we expect 2 rules, i.e. 2 cell values change




def t4_learn_to_drop_agent_preconditions():
    """
    Move left, check new rules are derived.

    @return:
    """
    # nace.hypothesis.Hypothesis_DisableLRUDMovementOpAssumptions()
    # nace.hypothesis.Hypothesis_UseLRUDMovementOpAssumptions(
    #     'left',
    #     'right',
    #     'up',
    #     'down',
    #     nace.world_module.drop,
    #     DisableLRUDOpSymmetryAssumptionFlag=False,
    # )

    original_focus_set = { 'x': 65}
    original_rule_evidence = {}
    original_rules = set()

    old_agent = nace.agent_module.Agent(rc_loc=[2, 9], score=0, terminated=0, values_excluding_prefix=[0])
    new_agent = nace.agent_module.Agent(rc_loc=[2, 8], score=0, terminated=0, values_excluding_prefix=[0])
    action = 'left'
    original_negrules = set()

    oldworld_string_list = (
        ['oooooooooooo','o          o','o        x o','o          o','o          o','o          o','oooooooooooo'],
        (0, 0), ['38,44,49,54,59,64,65,67,67,67,67,67','38,44,49,54,59,64,65,67,67,67,67,67','38,44,49,54,59,64,65,67,67,67,67,67','38,44,49,54,59,64,65,67,67,67,67,67','38,44,49,54,59,64,64,67,67,67,67,67','34,34,34,34,34,34,34,31,30,29,28,27','33,33,33,33,33,33,33,31,30,29,28,27'])

    oldworld, old_agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        oldworld_string_list[0],
        view_dist_x=3,
        view_dist_y=2,
        agent_char_code_list=['x'],
        observed_times_str_list=oldworld_string_list[2]
    )

    newworld_string_list = (
        ['oooooooooooo','o          o','o       x  o','o          o','o          o','o          o','oooooooooooo'],
        (0,0), ['38,44,49,54,59,64,65,68,68,68,68,68','38,44,49,54,59,64,65,68,68,68,68,68','38,44,49,54,59,64,65,68,68,68,68,68','38,44,49,54,59,64,65,68,68,68,68,68','38,44,49,54,59,64,64,68,68,68,68,68','34,34,34,34,34,34,34,31,30,29,28,27','33,33,33,33,33,33,33,31,30,29,28,27'])
    new_world, new_agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        newworld_string_list[0],
        view_dist_x=3,
        view_dist_y=2,
        agent_char_code_list=['x'],
        observed_times_str_list=newworld_string_list[2]
    )

    encoded_focus_set = convert_focus_set_to_internal_mapping(original_focus_set, oldworld)
    encoded_rules = convert_rules_to_internal_mapping(original_rules, oldworld)
    encoded_negrules = convert_rules_to_internal_mapping(original_negrules, oldworld)
    encoded_rule_evidence = original_rule_evidence
    predicted_world, predicted_agent, _, __, values, predicted_score_delta = _predict_next_world_state(
        encoded_focus_set,
        copy.deepcopy(oldworld), action, encoded_rules, old_agent
    )

    new_world.multiworld_print([
        {"World": oldworld,       "Caption":"Old",  "Color": nace.color_codes.color_code_white_on_blue},
        {"World": predicted_world, "Caption":"Pred\nNo Rule, Empty Pred", "Color": nace.color_codes.color_code_white_on_blue},
        {"World": new_world,       "Caption":"New",  "Color": nace.color_codes.color_code_white_on_blue},
    ])

    # copy values to check are not being mutataed.
    backup_encoded_focus_set = copy.deepcopy(encoded_focus_set)
    backup_encoded_rule_evidence = copy.deepcopy(encoded_rule_evidence)
    backup_oldworld = copy.deepcopy(oldworld)
    backup_new_world = copy.deepcopy(new_world)
    backup_encoded_rules = copy.deepcopy(encoded_rules)
    backup_encoded_negrules = copy.deepcopy(encoded_negrules)
    backup_predicted_world = copy.deepcopy(predicted_world)
    backup_old_agent = copy.deepcopy(old_agent)
    backup_new_agent = copy.deepcopy(new_agent)

    # Call the function
    calculated_focus_set, calculated_rule_evidence, calculated_new_rules, calculated_new_negrules = _observe_v2(
        encoded_focus_set, encoded_rule_evidence, oldworld, action, new_world, encoded_rules, encoded_negrules,
        predicted_world, pre_action_agent=old_agent, ground_truth_post_action_agent=new_agent,
        predicted_agent=predicted_agent,
        unobserved_code='.',
        object_count_threshold=1
    )

    # check to see we mutataed nothing
    assert backup_encoded_focus_set == encoded_focus_set
    assert backup_encoded_rule_evidence == encoded_rule_evidence
    assert backup_oldworld == oldworld
    assert backup_new_world == new_world
    assert backup_encoded_rules == encoded_rules
    assert backup_encoded_negrules == encoded_negrules
    assert backup_predicted_world == predicted_world
    assert backup_old_agent == old_agent
    assert backup_new_agent == new_agent

    print("About to check the rules with the action 'left', We expect 2 rules in total as there was no movement assumptions")
    left_rule_count = 0
    for rule in calculated_new_rules:
        if rule[0][0] == action:
            line = nace.prettyprint.prettyprint_rule(
                  rule_evidence=calculated_rule_evidence,
                  Hypothesis_TruthValue=nace.hypothesis.Hypothesis_TruthValue,
                  rule=rule
                  )
            print(line)
            prediction_state_value_deltas = rule[1]
            state_value_deltas = prediction_state_value_deltas[-1]
            left_rule_count += 1
    assert left_rule_count == 2 # we expect 2 rules, i.e. 2 cell values change

    # perturb the agent so that agent precondition(s) don't match current rules and call _observe() (again),
    # and check rules were updated in the correct way
    print("INFO -------- new test start ------")
    perturbed_agent = copy.deepcopy(new_agent)
    perturbed_agent.set_values_inc_prefix((1, 1)) # score += 1, state[0] += 1

    calculated_focus_set_2, calculated_rule_evidence_2, calculated_new_rules_2, calculated_new_negrules_2 = _observe_v2(
        encoded_focus_set, encoded_rule_evidence, oldworld, action, new_world, encoded_rules, encoded_negrules,
        predicted_world, pre_action_agent=old_agent, ground_truth_post_action_agent=perturbed_agent,
        predicted_agent=predicted_agent,
        unobserved_code='.',
        object_count_threshold=1
    )

    # assert score and state0 of agent rules were both 0 in original rules.
    for rule in calculated_new_rules:
        assert rule[1][3][0] == 0
        assert rule[1][3][1] == 0

    # assert score and state0 of agent rules are now both 1 in both rules.
    for rule in calculated_new_rules_2:
        assert rule[1][3][0] == 1
        assert rule[1][3][1] == 1
    print("test passed")


def t5_learn_agent_status_change_key_pickup():
    """
    pick up a key, learn agent state changes.

    @return:
    """
    # nace.hypothesis.Hypothesis_DisableLRUDMovementOpAssumptions()
    # nace.hypothesis.Hypothesis_UseLRUDMovementOpAssumptions(
    #     'left',
    #     'right',
    #     'up',
    #     'down',
    #     nace.world_module.drop,
    #     DisableLRUDOpSymmetryAssumptionFlag=False,
    # )

    original_focus_set = {'x': 65, 'k':1}
    original_rule_evidence = {}
    original_rules = set()

    old_agent = nace.agent_module.Agent(rc_loc=[2, 9], score=0, terminated=0, values_excluding_prefix=[0])
    new_agent = nace.agent_module.Agent(rc_loc=[2, 9], score=0, terminated=0, values_excluding_prefix=[1])
    action = "pickUpKey"
    original_negrules = set()

    oldworld_string_list = (
        ['oooooooooooo', 'o          o', 'o        xko', 'o          o', 'o          o', 'o          o',
         'oooooooooooo'],
        (0, 0), ['38,44,49,54,59,64,65,67,67,67,67,67', '38,44,49,54,59,64,65,67,67,67,67,67',
                 '38,44,49,54,59,64,65,67,67,67,67,67', '38,44,49,54,59,64,65,67,67,67,67,67',
                 '38,44,49,54,59,64,64,67,67,67,67,67', '34,34,34,34,34,34,34,31,30,29,28,27',
                 '33,33,33,33,33,33,33,31,30,29,28,27'])

    oldworld, old_agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        oldworld_string_list[0],
        view_dist_x=3,
        view_dist_y=2,
        agent_char_code_list=['x'],
        observed_times_str_list=oldworld_string_list[2]
    )

    newworld_string_list = (
        ['oooooooooooo', 'o          o', 'o        x o', 'o          o', 'o          o', 'o          o',
         'oooooooooooo'],
        (0, 0), ['38,44,49,54,59,64,65,68,68,68,68,68', '38,44,49,54,59,64,65,68,68,68,68,68',
                 '38,44,49,54,59,64,65,68,68,68,68,68', '38,44,49,54,59,64,65,68,68,68,68,68',
                 '38,44,49,54,59,64,64,68,68,68,68,68', '34,34,34,34,34,34,34,31,30,29,28,27',
                 '33,33,33,33,33,33,33,31,30,29,28,27'])
    new_world, new_agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        newworld_string_list[0],
        view_dist_x=3,
        view_dist_y=2,
        agent_char_code_list=['x'],
        observed_times_str_list=newworld_string_list[2]
    )

    encoded_focus_set = convert_focus_set_to_internal_mapping(original_focus_set, oldworld)
    encoded_rules = convert_rules_to_internal_mapping(original_rules, oldworld)
    encoded_negrules = convert_rules_to_internal_mapping(original_negrules, oldworld)
    encoded_rule_evidence = original_rule_evidence
    predicted_world, predicted_agent, _, __, values, predicted_score_delta = _predict_next_world_state(
        encoded_focus_set,
        copy.deepcopy(oldworld), action, encoded_rules, old_agent
    )

    new_world.multiworld_print([
        {"World": oldworld, "Caption": "Old", "Color": nace.color_codes.color_code_white_on_blue},
        {"World": predicted_world, "Caption": "Pred\nNo Rule, Empty Pred",
         "Color": nace.color_codes.color_code_white_on_blue},
        {"World": new_world, "Caption": "New", "Color": nace.color_codes.color_code_white_on_blue},
    ])

    # copy values to check are not being mutataed.
    backup_encoded_focus_set = copy.deepcopy(encoded_focus_set)
    backup_encoded_rule_evidence = copy.deepcopy(encoded_rule_evidence)
    backup_oldworld = copy.deepcopy(oldworld)
    backup_new_world = copy.deepcopy(new_world)
    backup_encoded_rules = copy.deepcopy(encoded_rules)
    backup_encoded_negrules = copy.deepcopy(encoded_negrules)
    backup_predicted_world = copy.deepcopy(predicted_world)
    backup_old_agent = copy.deepcopy(old_agent)
    backup_new_agent = copy.deepcopy(new_agent)

    # Call the function
    calculated_focus_set, calculated_rule_evidence, calculated_new_rules, calculated_new_negrules = _observe_v2(
        encoded_focus_set, encoded_rule_evidence, oldworld, action, new_world, encoded_rules, encoded_negrules,
        predicted_world, pre_action_agent=old_agent, ground_truth_post_action_agent=new_agent,
        predicted_agent=predicted_agent,
        unobserved_code='.',
        object_count_threshold=1
    )

    # check to see we mutated nothing
    assert backup_encoded_focus_set == encoded_focus_set
    assert backup_encoded_rule_evidence == encoded_rule_evidence
    assert backup_oldworld == oldworld
    assert backup_new_world == new_world
    assert backup_encoded_rules == encoded_rules
    assert backup_encoded_negrules == encoded_negrules
    assert backup_predicted_world == predicted_world
    assert backup_old_agent == old_agent
    assert backup_new_agent == new_agent

    print(
        "About to check the rules with the action 'left', We expect 2 rules in total as there was no movement assumptions")
    rule_count = 0
    for rule in calculated_new_rules:
        if rule[0][0] == action:
            line = nace.prettyprint.prettyprint_rule(
                rule_evidence=calculated_rule_evidence,
                Hypothesis_TruthValue=nace.hypothesis.Hypothesis_TruthValue,
                rule=rule
            )
            print(line)
            prediction_state_value_deltas = rule[1]
            state_value_deltas = prediction_state_value_deltas[-1]
            rule_count += 1
    assert rule_count == 1  # we expect 1 rule
    assert state_value_deltas[0] == 0 # no change in RL reward
    assert state_value_deltas[1] == 0 # no change in termination state
    assert state_value_deltas[2] == 1  # we now have a key, indicated in agent state location 1.

    # perturb the agent so that agent precondition(s) don't match current rules and call _observe() (again),
    # and check rules were updated in the correct way
    print("INFO -------- new test start ------")
    perturbed_agent = copy.deepcopy(new_agent)
    perturbed_agent.set_values_inc_prefix((1, 0, 1))  # score += 1, still have a key (no change in keys held)

    calculated_focus_set_2, calculated_rule_evidence_2, calculated_new_rules_2, calculated_new_negrules_2 = _observe_v2(
        encoded_focus_set, encoded_rule_evidence, oldworld, action, new_world, encoded_rules, encoded_negrules,
        predicted_world, pre_action_agent=old_agent, ground_truth_post_action_agent=perturbed_agent,
        predicted_agent=predicted_agent,
        unobserved_code='.',
        object_count_threshold=1
    )

    # assert score and state0 of agent rules were both 0 in original rules.
    for rule in calculated_new_rules:
        assert rule[1][3][0] == 0 # score
        assert rule[1][3][1] == 0 # terminated
        assert rule[1][3][2] == 1 # key

    # assert score and state0 of agent rules are now both 1 in both rules (i.e. we now get reward we we get the key).
    for rule in calculated_new_rules_2:
        assert rule[1][3][0] == 1 # score
        assert rule[1][3][1] == 0 # terminated
        assert rule[1][3][2] == 1 # key
    print("test passed")



def t6_pick_up_key_increase_keys_held_is_learned():
    world_str_list = ['.............',
                      '.adddddaa....',
                      '.aeeecdbb....',
                      'AaeeeRdbb....',
                      'Aabbbbabb....',
                      'Aabbbbkbb....',
                      'Aaaaaaaaa....',
                      'AAAAAAAAA....']
    time_str_list = []
    focus_set = {'b': 53, 'd': 41, 'c': 1, 'a': 32, 'Q': 4, 'e': 57, 'O': 7, 'R': 5, 'f': 2, 'g': 1, 'h': 1, 'j': 1,
                 'N': 2, 'k': 2, 'l': 1, 'm': 2}
    active_rules = []
    rule_evidence = {}
    world_state_values = {'int_2from_rgb_list': [],
                          'int_2from_char_list': [(-1, 'A'), (-2, '.'), (3215016267, 'B'), (823474807, 'C'),
                                                  (2687125822, 'D'), (362910338, 'E'), (1758885969, 'F'),
                                                  (748094602, 'G'), (3376261930, 'H'), (3305816727, 'I'),
                                                  (854999169, 'J'), (1334950674, 'K'), (69488790, 'L'),
                                                  (2350475356, 'M'), (2829951097, 'N'), (3539787669, 'O'),
                                                  (1867891296, 'P'), (1704944625, 'Q'), (3665670421, 'R'),
                                                  (1484579719, 'a'), (1152208772, 'b'), (2624420647, 'c'),
                                                  (2204181460, 'd'), (2407174942, 'e'), (951216077, 'f'),
                                                  (4000794601, 'g'), (1483862051, 'h'), (2183995252, 'i'),
                                                  (808930194, 'j'), (1799812895, 'k'), (1406248814, 'l'),
                                                  (2624386038, 'm')], 'raw_cell_shape': (32, 32, 3),
                          'raw_nptype': "<class 'numpy.uint8'>"}
    agent = nace.agent_module.Agent(rc_loc=(3, 5), score=0.965625, terminated=0,
                                    values_excluding_prefix=[0, 0, 0, 0, 0, 0])

    # hand coded after this line
    """
    (-1, 'A'),    EXTERNAL WALL
    (-2, '.')     UNOBSERVED
    (3215016267, 'B'), facing down - green RHS
    (823474807,  'C'), facing right - green background
    (2687125822, 'D'), facing up - green tip
    (362910338,  'E'), facing right - on lava/water
    (1758885969, 'F'),  up - red tip
    (748094602,  'G'),  up - lava
    (3376261930, 'H'),  up - grey tip
    (3305816727, 'I'),  right - green door edge on RHS
    (854999169,  'J'), up
    (1334950674, 'K'),  up, grey tip
    (69488790,   'L'),  right on water/lava
    (2350475356, 'M'),  left on lava water
    (2829951097, 'N'), left 
    (3539787669, 'O'), right
    (1867891296, 'P'), down on green background
    (1704944625, 'Q'), down 
    (3665670421, 'R'), up
    (1484579719, 'a'), grey square - can be moved through
    (1152208772, 'b'), black square - can be moved through
    (2624420647, 'c'), grey key
    (2204181460, 'd'), grey square
    (2407174942, 'e'), black square
    (951216077,  'f'), grey door
    (4000794601, 'g'), grey key, dark background
    (1483862051, 'h'), grey door, darker background
    (2183995252, 'i'), dark square, light grey RHS
    (808930194, 'j'),  green key
    (1799812895, 'k'). green door

    """
    agent_char = world_str_list[agent.get_rc_loc()[0]][agent.get_rc_loc()[1]]
    world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        world_str_list,
        view_dist_x=12,
        view_dist_y=5,
        agent_char_code_list=[agent_char], # must match actual agent char
        observed_times_str_list=[],
        int_2from_char_mapping=world_state_values["int_2from_char_list"]
    )
    world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])

    # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
    new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
    new_rules = convert_rules_to_internal_mapping(active_rules, world)
    new_rule_evidence = convert_rule_evidence_to_internal_mapping(rule_evidence, world)


    # now perform meat of the test
    # change world state to grey key (which the rules should know) check predicting picking up the key, results in a held key

    # test that the current rules suggest key count gow up if we pick up a key
    plan_actions = ['pickup']
    planworld = copy.deepcopy(world)
    planagent = copy.deepcopy(agent)
    assert sum(planagent.get_values_exc_prefix()) == 0
    for i in range(0, len(plan_actions)):
        planworld, planagent, _, __, ___, ____ = nace.nace_v3._predict_next_world_state(
            new_focus_set,
            copy.deepcopy(planworld), plan_actions[i], new_rules, planagent
        )

    # repeatedly present the same initial world and agent, and new world and agent, evidence gets more strong, but spurious rules not un-learned.
    world_str_list_with_no_agent = ['.............',
                      '.adddddaa....',
                      '.aeeeedbb....',
                      'Aaeeeedbb....',
                      'Aabbbbabb....',
                      'Aabbbbkbb....',
                      'Aaaaaaaaa....',
                      'AAAAAAAAA....']


    for i in range(15):
        desired_agent_rc_loc = (random.randint(2, 4),random.randint(2, 6))
        desired_object_rc_loc = (desired_agent_rc_loc[0]-1,desired_agent_rc_loc[1])
        below_key = random.random() > 0.5 or i <= 2
        if below_key:
            object_char = 'c' # key
            ground_truth_post_action_agent = Agent(desired_agent_rc_loc, agent.get_score(), agent.get_terminated(),
                                                   [0, 0, 0, 0, 1, 0, 0])
        else:
            object_char = 'c'  # key
            # shift the agent 1 more space down (away from key)
            desired_agent_rc_loc = (desired_agent_rc_loc[0]+1,desired_agent_rc_loc[1]) # agent is too far away for pickup to have effect
            ground_truth_post_action_agent = Agent(desired_agent_rc_loc, agent.get_score(), agent.get_terminated(),
                                                   [0, 0, 0, 0, 0, 0, 0])

        agent_char = 'R' # facing up
        input_pre_action_world, input_agent =  place_agent_and_object(world_str_list_with_no_agent, agent,  desired_agent_rc_loc, desired_object_rc_loc, object_char, agent_char, world_state_values["int_2from_char_list"] )
        post_action_ground_truth_world, _  = place_agent_and_object(world_str_list_with_no_agent, agent,  desired_agent_rc_loc, desired_object_rc_loc, 'b', agent_char, world_state_values["int_2from_char_list"] )

        world.multiworld_print([{"World": input_pre_action_world, "Color": nace.color_codes.color_code_white_on_blue, "Caption":"Pre"},
                                {"World": post_action_ground_truth_world, "Color": nace.color_codes.color_code_white_on_blue, "Caption":"Post"}])

        (
            r_used_rules,
            r_focus_set,
            r_rule_evidence,
            r_simulated_world_post_action,
            r_newrules,
            r_newnegrules,
            r_values,
            r_lastplanworld,
            r_predicted_world,
            r_stayed_the_same,
            r_stats
        ) = nace.nace_v3.nacev3_predict_and_observe(  # called _predict_and_observe in v1
                1, #time_counter,
                new_focus_set,
                new_rule_evidence,
                input_agent.get_rc_loc(),  # pre action agent location note (0,0) is top left
                input_pre_action_world, # pre_action_world,  # pre action internal world model (partially observed) before last_action is applied
                set(new_rules), #rulesin,  # used in part1 and part2
               {}, #negrules,
                'pickup', #'last_action,
            set([]), #rulesExcluded,
                post_action_ground_truth_world,  # i.e. this is the post action world model
                input_agent, #pre_action_agent,  # pre action agent
                ground_truth_post_action_agent,  # post action agent
                -1, #unobserved_code,  # value which indicates we can not see the true value of the cell
                agent_indication_raw_value_list,  # raw value of an agent, i.e. 'x', or the rgb value
                object_count_threshold=1,  # how unique values must be before they are considered. was 1, i.e. unique
                print_out_world_and_plan=True)


        # print the newly updated rules
        print("Learning cycle", i)
        for r in r_rule_evidence.keys():
            _,str_rule = convert_rules_to_char_or_int_mappings([r], world)
            if r not in new_rule_evidence:
                print("INFO.   new rule: ", str_rule ,  r_rule_evidence[r])
            else:
                if r_rule_evidence[r] != new_rule_evidence[r]:
                    print("INFO modified ", str_rule, "was", new_rule_evidence[r], "now", r_rule_evidence[r])

        for r in r_used_rules:
            if r[0][0] == 'pickup':
                _,str_rule = convert_rules_to_char_or_int_mappings([r], world)
                print("INFO.   used rule: ", str_rule  )
        for r in r_newrules:
            if r[0][0] == 'pickup':
                _,str_rule = convert_rules_to_char_or_int_mappings([r], world)
                print("INFO.   r_newrules: ", str_rule )
        for r in r_newnegrules:
            if r[0][0] == 'pickup':
                _,str_rule = convert_rules_to_char_or_int_mappings([r], world)
                print("INFO.   r_newnegrules: ", str_rule )

        # copy output over input for next learning cycle.
        new_rule_evidence = copy.deepcopy(r_rule_evidence)
        new_focus_set = copy.deepcopy(r_focus_set)
        new_rules = copy.deepcopy(list(new_rule_evidence.keys()))


    for k in new_rule_evidence.keys():
        if k[0][0] == 'pickup':
            print("DEBUG ", k)

    # assert we have a rule that when the agent is below the key, and performs 'pickup', the grey key score is incremented.
    # 2624420647 grey key, 1152208772 square that can be moved through.
    assert (('pickup', (0, 0, 0, 0, 0, 0, 0), (0, 0, 2624420647), (1, 0, 3665670421)), (0, 0, 1152208772, (0.0, 0, 0, 0, 0, 0, 1, 0))) in new_rule_evidence
    print("Test Passed")


if __name__ == "__main__":
    t6_pick_up_key_increase_keys_held_is_learned()


    t5_learn_agent_status_change_key_pickup()


    t1_simple_move_left() # passes
    t3_cup_on_table() # passes
    t2_simple_move_left_get_moved_left_and_down() # passes
    t4_learn_to_drop_agent_preconditions()

