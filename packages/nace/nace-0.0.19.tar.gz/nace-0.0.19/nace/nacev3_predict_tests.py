import copy

import nace
from nace.nace_v3 import _plan, _predict_next_world_state
from nace.test_utilities import (convert_focus_set_to_internal_mapping, convert_rules_to_internal_mapping,
                                 get_xy_delta_for_action_list)

def t1_predict():
    world_str_list = [
        'AAAAAAAA..',
        'AcEaaaaa..',
        'Aaaaaaaa..',
        'Aaaabaaa..',
        'Aaaaaaba..', '..........', '..........',
                      '..........', '..........', '..........']
    focus_set = {'A': 0, 'E': 3, 'a': 0, 'b': 0, 'C': 8, 'c': 2, 'H': 4, 'B': 5, 'G': 1}
    rules = [

        # if the agents state is included in the rules, it must match the actual agent state (including score),
        # otherwise the action does not fire.

        # action,agent,   precon_1,      precon_n,       consequences
        #        state                                   world       agent
        #                                                            reward, v0, v1...
        (('down', (0,1),    (1, 0, 'a'),  (0, 0, 'E')),     (0, 0, 'a', (1.0,))),  # new rule
        (('down', (0,1),    (-1, 0, 'E'), (0, 0, 'a')),     (0, 0, 'E', (1.0,))),  # new rule
    ] #            ^- terminted == 0
    #                ^___ arbritary agent value (passed into agent constructor as well)
    world_state_values = {'int_2from_rgb_list': [],
                          'int_2from_char_list': [(-1, 'A'), (-2, '.'), (2617493089, 'B'), (3144150970, 'C'),
                                                  (3712765165, 'D'), (2460067371, 'E'), (961690427, 'F'),
                                                  (1630428625, 'G'), (442688737, 'H'), (1147995044, 'a'),
                                                  (2117949728, 'b'), (1992348315, 'c')], 'raw_cell_shape': (64, 64, 3),
                          'raw_nptype': "<class 'numpy.uint8'>"}
    agent = nace.agent_module.Agent(rc_loc=(1, 2), score=0.0, terminated=0, values_excluding_prefix=[1])


    # hand coded after this line

    observed_times_str_list=[
        '10,10,10,10,10,10,10,10,-inf,-inf',
        '10,12,12,10,10,10,10,10,-inf,-inf',
        '10,10,10,10,10,10,10,10,-inf,-inf',
        '10,10,10,10,10,10,10,10,-inf,-inf',
        '10,10,10,10,10,10,10,10,-inf,-inf',
        '-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf',
        '-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf',
        '-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf',
        '-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf',
        '-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf,-inf',
    ]

    agent_char = world_str_list[agent.get_rc_loc()[0]][agent.get_rc_loc()[1]]

    world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        world_str_list,
        view_dist_x=12,
        view_dist_y=5,
        agent_char_code_list=[agent_char], # must match actual agent char
        observed_times_str_list=observed_times_str_list,
        int_2from_char_mapping=world_state_values["int_2from_char_list"]
    )
    world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])

    # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
    new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
    new_rules = convert_rules_to_internal_mapping(rules, world)

    plan_actions = ["down"]
    planworld = copy.deepcopy(world)
    planagent = copy.deepcopy(agent)
    for i in range(0, len(plan_actions)):
        planworld, planagent, _, __, agent_values_delta, score_delta = nace.nace_v3._predict_next_world_state(
            new_focus_set,
            copy.deepcopy(planworld), plan_actions[i], new_rules, planagent
        )
    world.multiworld_print([{"Caption": f"Start:",
                             "World": world,
                             "Color": nace.color_codes.color_code_white_on_black},
                            {"Caption": f"At end of plan:\n" + str(
                                nace.prettyprint.prettyprint_all_actions(plan_actions)),
                             "World": planworld,
                             "Color": nace.color_codes.color_code_white_on_red},
                            ]
                           )

    ch = planworld.get_char_at_rc(2,2, agent_indication_embedded_value_list=[])
    print("ch",ch)
    print("agent_values_delta",agent_values_delta)
    assert ch == 'E'
    assert agent_values_delta == [1.0, 0, 0] # score increase by 1 even though 2 rules fired.

    # test part b - two moves down
    print("________________________________")

    world.multiworld_print([{"Caption": f"Start:",
                             "World": world,
                             "Color": nace.color_codes.color_code_white_on_black},
                            ]
                           )
    plan_actions = ["down", "down"]
    planworld = copy.deepcopy(world)
    planagent = copy.deepcopy(agent)
    for i in range(0, len(plan_actions)):
        planworld, planagent, _, __, agent_values_delta, score_delta = nace.nace_v3._predict_next_world_state(
            new_focus_set,
            copy.deepcopy(planworld), plan_actions[i], new_rules, planagent
        )

        world.multiworld_print([
                                {"Caption": f"after move:"+str(i)+"\n" + str(
                                    nace.prettyprint.prettyprint_all_actions(plan_actions)),
                                 "World": planworld,
                                 "Color": nace.color_codes.color_code_white_on_red},
                                ]
                               )

    ch = planworld.get_char_at_rc(3, 2, agent_indication_embedded_value_list=[])
    print("ch",ch)
    assert ch == 'E'
    assert agent_values_delta == [1.0, 0, 0]  # score increase by 1 even though 2 rules fired.

    print()









def t2_check_plan_roll_forward():
    """
    @return:
    """
    print("___________t2_check_plan_roll_forward()________")
    world_str_list = [
        ['oooooooooooo',
         'o   o   x  o',
         'o      f f o',
         'o   oooooooo',
         'o       u  o',
         'o          o',
         'oooooooooooo'], (),
        ['25,25,25,23,24,26,26,26,26,26,26,26,',
         '25,25,25,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,25,25,25,25,25,25,25,',
         '19,19,19,19,19,19,19,16,15,14,13,12,',
         '18,18,18,18,18,18,18,16,15,14,13,12,']]
    rules = {(('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))),
             (('left', (0,), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,))),
             (('up', (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,))),
             (('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,))),
             (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             (('left', (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,))),
             (('left', (0,), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
             (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             (('up', (0,), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,))),
             (('up', (0,), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),

             (('left', (0,), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
             (('left', (0,), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             (('up', (0,), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
             (('up', (0,), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
             }
    actions = ['left', 'right', 'up', 'down']
    focus_set = {'f': 1, 'u': 1, 'x': 9}
    agent = nace.agent_module.Agent((1, 8), 0, 0, ())

    world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        world_str_list[0],
        view_dist_x=12,
        view_dist_y=5,
        agent_char_code_list=['x'],
        observed_times_str_list=world_str_list[2]
    )
    world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])

    # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
    new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
    new_rules = convert_rules_to_internal_mapping(rules, world)


    # ======

    # check  _predict_next_world_state() if gived the exact correct moves gives a +ve score
    # yes this should be a seperate test, but the code is changing so fast.

    w_t_plus_1, planagent_1, new_AIRIS_confidence, __age, agent_values_delta, predicted_score_delta = (
        _predict_next_world_state(
            new_focus_set,
            copy.deepcopy(world), 'left', new_rules, agent, custom_goal=None
        ))
    w_t_plus_2, planagent_2,new_AIRIS_confidence, __age, agent_values_delta, predicted_score_delta = (
        _predict_next_world_state(
            new_focus_set,
            copy.deepcopy(w_t_plus_1), 'down', new_rules, agent, custom_goal=None
        ))
    assert predicted_score_delta == 1.0
    assert agent_values_delta[0] == 1.0

    # =========

    (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason,
     oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason,
     biggest_predicted_score_delta_actions, biggest_predicted_score_delta,
     biggest_predicted_score_delta_stopping_reason,
     smallest_predicted_score_delta_actions, smallest_predicted_score_delta,
     smallest_predicted_score_delta_stopping_reason,
     debbugging_data) = (
        _plan(
            world,
            new_rules,
            actions,
            new_focus_set,
            agent))

    xy_dt2 = get_xy_delta_for_action_list(biggest_predicted_score_delta_actions)
    assert xy_dt2 == (-1, 1) or xy_dt2 == (1, 1) # go for left food (dependent on action order?)
    assert biggest_predicted_score_delta == 1

    # roll forward the world according to the plan
    planworld = copy.deepcopy(world)
    planagent = copy.deepcopy(agent)
    for i in range(0, len(biggest_predicted_score_delta_actions)):
        planworld, planagent, _, __, ___, ____ = nace.nace_v3._predict_next_world_state(
            new_focus_set,
            copy.deepcopy(planworld), biggest_predicted_score_delta_actions[i], new_rules, planagent
        )

    world.multiworld_print([{"Caption": f"Start:",
                             "World": world,
                             "Color": nace.color_codes.color_code_white_on_black},
                            {"Caption": f"At end of plan:\n" + str(
                                nace.prettyprint.prettyprint_all_actions(biggest_predicted_score_delta_actions)),
                             "World": planworld,
                             "Color": nace.color_codes.color_code_white_on_red},
                            ]
                           )

    counts = planworld.get_board_char_counts(agent_indication_embedded_value_list=[])
    print("counts", counts)
    assert counts['f'] == 1  # the x should be over one of the foods.


def t3_frozen_lake_agent_about_to_die():
    world_str_list = ['AAAAAAAA..', 'Acaaaaaa..', 'AaaaEaaa..', 'Aaaabaaa..', '.aaaaaba..', '.aaabaaa..', '..........',
                      '..........', '..........', '..........']
    time_str_list = []
    focus_set = {'E': 3, 'a': 8, 'I': 6, 'b': 1}
    active_rules = [
        (('right', (0,), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'c', (0.0, 0))),  # E
        (('down', (0,), (0, 0, 'E'), (1, 0, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('right', (0,), (0, 0, 'I'), (0, 1, 'a')), (0, 0, 'a', (0.0, 0))),  # I
        (('down', (0,), (0, 0, 'I'), (1, 0, 'a')), (0, 0, 'a', (0.0, 0))),
        (('right', (0,), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'I', (0.0, 0))),  # a
        (('down', (0,), (-1, 0, 'I'), (0, 0, 'a')), (0, 0, 'E', (0.0, 0))),
        (('right', (0,), (0, -1, 'I'), (0, 0, 'a')), (0, 0, 'I', (0.0, 0))),
        (('down', (0,), (-1, 0, 'E'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),  # b
    ]  # subset of rule_evidence
    rule_evidence = {(('right', (0,), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'c', (0.0, 0))): (2, 0),
                     (('right', (0,), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'I', (0.0, 0))): (2, 0),
                     (('right', (0,), (0, 0, 'I'), (0, 1, 'a')), (0, 0, 'a', (0.0, 0))): (4, 0),
                     (('right', (0,), (0, -1, 'I'), (0, 0, 'a')), (0, 0, 'I', (0.0, 0))): (4, 0),
                     (('down', (0,), (-1, 0, 'I'), (0, 0, 'a')), (0, 0, 'E', (0.0, 0))): (2, 0),
                     (('down', (0,), (0, 0, 'I'), (1, 0, 'a')), (0, 0, 'a', (0.0, 0))): (2, 0),
                     (('down', (0,), (0, 0, 'E'), (1, 0, 'b')), (0, 0, 'a', (-1.0, 1))): (1, 0),
                     (('down', (0,), (-1, 0, 'E'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))): (1, 0)}
    world_state_values = {'int_2from_rgb_list': [],
                          'int_2from_char_list': [(-1, 'A'), (-2, '.'), (2617493089, 'B'), (3144150970, 'C'),
                                                  (3712765165, 'D'), (2460067371, 'E'), (961690427, 'F'),
                                                  (1630428625, 'G'), (2625964021, 'H'), (442688737, 'I'),
                                                  (1147995044, 'a'), (2117949728, 'b'), (1992348315, 'c')],
                          'raw_cell_shape': (64, 64, 3), 'raw_nptype': "<class 'numpy.uint8'>"}
    agent = nace.agent_module.Agent(rc_loc=(2, 4), score=-1.0, terminated=0, values_excluding_prefix=[])
    actions = ['left', 'down', 'right', 'up']
    behavior_returned = 'BABBLE'
    whole_plan_returned = ['left']

    # hand coded code after this line
    """
    (-1, 'A'),    EXTERNAL WALL
    (-2, '.')     UNOBSERVED
    (2617493089, 'B'),  Agent looking left, white background
    (3144150970, 'C'),  Agent looking away (up), white background
    (3712765165, 'D'),  Agent looking left, white background 
    (2460067371, 'E'),  Agent looking at up (down), white background
    (961690427,  'F'),  Agent having fallen through Ice
    (1630428625, 'G'),  Agent, looking right, white background 
    (2625964021, 'H'), Agent on Goal cell, white background
    (442688737, 'I'),  Agent, looking right, white background

    (1147995044, 'a'), a (made from char map)
    (2117949728, 'b'), b (made from char map)
    (1992348315, 'c'), c (made from char map)
    (1868170614, 'd'), d (made from char map)
    """

    agent_char = world_str_list[agent.get_rc_loc()[0]][agent.get_rc_loc()[1]]

    world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        world_str_list,
        view_dist_x=12,
        view_dist_y=5,
        agent_char_code_list=[agent_char],  # must match actual agent char
        observed_times_str_list=[],
        int_2from_char_mapping=world_state_values["int_2from_char_list"]
    )
    world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])

    # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
    new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
    new_rules = convert_rules_to_internal_mapping(active_rules, world)

    plan_actions = ['down']
    planworld = copy.deepcopy(world)
    planagent = copy.deepcopy(agent)
    for i in range(0, len(plan_actions)):
        planworld, planagent, _, __, ___, ____ = nace.nace_v3._predict_next_world_state(
            new_focus_set,
            copy.deepcopy(planworld), plan_actions[i], new_rules, planagent
        )

    world.multiworld_print([{"Caption": f"Start:",
                             "World": world,
                             "Color": nace.color_codes.color_code_white_on_black},
                            {"Caption": f"At end of plan:\n" + str(
                                nace.prettyprint.prettyprint_all_actions(plan_actions)),
                             "World": planworld,
                             "Color": nace.color_codes.color_code_white_on_red},
                            ]
                           )

    assert planagent.get_terminated() >= 1
    print("INFO test passed, agent is dead")


if __name__ == "__main__":
    t1_predict()
    t2_check_plan_roll_forward()
    t3_frozen_lake_agent_about_to_die()
    print("TESTS COMPLETE")
