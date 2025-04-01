import copy
import random

import nace
from nace.agent_module import Agent
from nace.test_utilities import (convert_focus_set_to_internal_mapping, convert_rules_to_internal_mapping,
                                 convert_rule_evidence_to_internal_mapping,
                                 convert_rules_to_char_or_int_mappings)






def t3_why_frozen_lake_is_inefficient():

    """
    WARNING - If too much state is stored in the agent, the number of rules explode




    @return:
    """

    world_str_list = ['AAAAAA....', 'Acaaaa....', 'Aaaaaa....', 'Aaaaba....', 'Aaaaaa....', 'AaEaba....', 'Aabbaa....',
                      'Aabaab....', '..........', '..........']
    time_str_list = []
    focus_set = {'E': 7, 'D': 1, 'a': 7, 'c': 2, 'H': 1, 'C': 1, 'B': 2}
    active_rules = [
        (('down', (0,), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'c', (0.0, 1))),  # C
        (('down', (0,), (0, 0, 'D'), (0, 1, 'a')), (0, 0, 'c', (0.0, 1))),  # D
        (('down', (0,), (0, -1, 'D'), (0, 0, 'a')), (0, 0, 'E', (0.0, 1))),  # a
        (('down', (0,), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'E', (0.0, 1))),
        (('down', (0,), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 1))),
    ]  # subset of rule_evidence
    rule_evidence = {(('left', (0,), (0, 0, 'E')), (0, 0, 'D', (0.0, 0))): (1, 0),
                     (('down', (0,), (0, 0, 'D'), (0, 1, 'a')), (0, 0, 'c', (0.0, 1))): (1, 0),
                     (('down', (0,), (0, -1, 'D'), (0, 0, 'a')), (0, 0, 'E', (0.0, 1))): (1, 0),
                     (('right', (1,), (0, 0, 'E')), (0, 0, 'H', (0.0, 0))): (1, 1),
                     (('down', (1,), (0, 0, 'c'), (0, 1, 'H')), (0, 0, 'E', (0.0, -1))): (1, 1),
                     (('down', (1,), (0, -1, 'c'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))): (1, 1),
                     (('down', (0,), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'c', (0.0, 1))): (1, 0),
                     (('down', (0,), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 1))): (1, 0),
                     (('up', (1,), (0, 0, 'c'), (0, 1, 'E')), (0, 0, 'C', (0.0, -1))): (1, 1),
                     (('up', (1,), (0, -1, 'c'), (0, 0, 'E')), (0, 0, 'a', (0.0, -1))): (1, 1),
                     (('down', (0,), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'c', (0.0, 1))): (1, 0),
                     (('down', (0,), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'E', (0.0, 1))): (1, 0),
                     (('left', (1,), (0, 0, 'E')), (0, 0, 'B', (0.0, 0))): (1, 1),
                     (('left', (0,), (0, 0, 'E')), (0, 0, 'B', (0.0, 0))): (1, 0),
                     (('down', (1,), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))): (1, 1),
                     (('down', (1,), (-1, 0, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))): (1, 1),
                     (('down', (9,), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))): (1, 1),
                     (('down', (9,), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))): (1, 1),
                     (('down', (0,), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 8))): (1, 0),
                     (('left', (17,), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))): (1, 1),
                     (('left', (17,), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'B', (0.0, 8))): (1, 1),
                     (('down', (25,), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))): (1, 1),
                     (('down', (25,), (-1, 0, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))): (1, 1)}
    world_state_values = {'int_2from_rgb_list': [],
                          'int_2from_char_list': [(-1, 'A'), (-2, '.'), (2617493089, 'B'), (3144150970, 'C'),
                                                  (3712765165, 'D'), (2460067371, 'E'), (961690427, 'F'),
                                                  (1630428625, 'G'), (442688737, 'H'), (1147995044, 'a'),
                                                  (2117949728, 'b'), (1992348315, 'c')], 'raw_cell_shape': (64, 64, 3),
                          'raw_nptype': "<class 'numpy.uint8'>"}
    agent = nace.agent_module.Agent(rc_loc=(5, 2), score=0.0, terminated=0, values_excluding_prefix=[33])
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
    (442688737,  'H'),  Agent, looking right, white background
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
        agent_char_code_list=[agent_char], # must match actual agent char
        observed_times_str_list=[],
        int_2from_char_mapping=world_state_values["int_2from_char_list"]
    )
    world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])

    # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
    new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
    new_rules = convert_rules_to_internal_mapping(rules, world)

    plan_actions = [nace.world_module.down]

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

    ch = planworld.get_char_at_rc(2,1, agent_indication_embedded_value_list=[])
    assert ch == 'a' # should not be 'a', should be a
    print()




def t7_pick_up_key_increases_keys_held():
    pass
    # test agent values are learnt correctly when key picked up

    world_str_list = ['.............',
                      '.............',
                      '.aeeeedbb....',
                      'Aaeeecdbb....',
                      'AaeeeRdbb....',
                      'Aabbbbkbb....',
                      'Aaaaaaaaa....',
                      'AAAAAAAAA....']

    focus_set = {'b': 27, 'd': 20, 'c': 1, 'a': 17, 'Q': 3, 'e': 27, 'O': 4, 'R': 2, 'f': 2, 'g': 1, 'h': 1}
    active_rules = [
        (('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, -1, 'b'), (0, 0, 'O'), (1, 1, 'd')),
         (0, 0, 'R', (0.0, 0, 0, 0, 0, 0, 0, 0))),  # O
        (('turn_left', (0, 0, 0, 0, 0, 0, 0), (0, -2, 'd'), (0, 0, 'Q'), (1, -1, 'd')),
         (0, 0, 'O', (0.0, 0, 0, 0, 0, 0, 0, 0))),  # Q
        (('forward', (0, 0, 0, 0, 0, 0, 0), (0, -2, 'e'), (0, -1, 'e'), (0, 0, 'R')),
         (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))),  # R
        (('turn_left', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'a'), (0, 2, 'b'), (1, 1, 'b')),
         (0, 0, 'd', (0.0, 0, 0, 0, 0, 0, 0, 0))),  # a
        (('turn_left', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'a'), (1, -1, 'b'), (1, 0, 'a')),
         (0, 0, 'd', (0.0, 0, 0, 0, 0, 0, 0, 0))),
        (('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, 0, 'a'), (0, -1, 'b'), (0, 0, 'a')),
         (0, 0, 'd', (0.0, 0, 0, 0, 0, 0, 0, 0))),
        (('turn_left', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'b'), (1, -1, 'b')), (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))),  # b
        (('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, 1, 'a'), (0, 0, 'b'), (0, 1, 'a')),
         (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))),
        (('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, -1, 'c'), (0, -2, 'b'), (0, 0, 'b')),
         (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))),
        (('turn_left', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'b'), (1, 1, 'O')), (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))),
        (('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, 1, 'c'), (0, 0, 'b'), (0, 2, 'b')),
         (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))),
        (('turn_left', (0, 0, 0, 0, 0, 0, 0), (0, -2, 'a'), (0, 0, 'b'), (1, -1, 'b')),
         (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))),
        (('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, 1, 'b'), (0, 0, 'b'), (1, -1, 'a')),
         (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))),
        (('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, -1, 'a'), (-1, 1, 'b'), (0, 0, 'b')),
         (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))),
        (('turn_left', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'c'), (1, -1, 'b'), (1, 1, 'b')),
         (0, 0, 'g', (0.0, 0, 0, 0, 0, 0, 0, 0))),  # c
        (('turn_left', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'd'), (0, 2, 'Q'), (1, 1, 'd')),
         (0, 0, 'a', (0.0, 0, 0, 0, 0, 0, 0, 0))),  # d
        (('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, -1, 'O'), (0, 0, 'd')), (0, 0, 'a', (0.0, 0, 0, 0, 0, 0, 0, 0))),
        (('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, -1, 'd'), (-1, 1, 'Q'), (0, 0, 'd')),
         (0, 0, 'a', (0.0, 0, 0, 0, 0, 0, 0, 0))),
        (('forward', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'e'), (0, 1, 'f')), (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))),  # e
        (('forward', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'e'), (0, 1, 'e'), (0, 2, 'R')),
         (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))),
        (('forward', (0, 0, 0, 0, 0, 0, 0), (0, -1, 'e'), (0, 0, 'e'), (0, 1, 'R')),
         (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))),
        (('forward', (0, 0, 0, 0, 0, 0, 0), (0, -1, 'e'), (0, 0, 'f')), (0, 0, 'h', (0.0, 0, 0, 0, 0, 0, 0, 0))),  # f
        (('pickup', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'g')), (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 1, 0))),  # g
    ]  # subset of rule_evidence
    rule_evidence = {(('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, -1, 'c'), (0, -2, 'b'), (0, 0, 'b')),
                      (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('turn_left', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'c'), (1, -1, 'b'), (1, 1, 'b')),
                     (0, 0, 'g', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, 1, 'c'), (0, 0, 'b'), (0, 2, 'b')),
                     (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, 1, 'a'), (0, 0, 'b'), (0, 1, 'a')),
                     (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, 0, 'a'), (0, -1, 'b'), (0, 0, 'a')),
                     (0, 0, 'd', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('turn_left', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'a'), (1, -1, 'b'), (1, 0, 'a')),
                     (0, 0, 'd', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('turn_left', (0, 0, 0, 0, 0, 0, 0), (0, -2, 'd'), (0, 0, 'Q'), (1, -1, 'd')),
                     (0, 0, 'O', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, -1, 'd'), (-1, 1, 'Q'), (0, 0, 'd')),
                     (0, 0, 'a', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('turn_left', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'd'), (0, 2, 'Q'), (1, 1, 'd')),
                     (0, 0, 'a', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('forward', (0, 0, 0, 0, 0, 0, 0), (-1, -1, 'e'), (0, 0, 'e')),
                     (0, 0, 'O', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (
                     ('forward', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'e'), (1, 0, 'e')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 3), (
                     ('forward', (0, 0, 0, 0, 0, 0, 0), (-1, 0, 'e'), (0, 0, 'e'), (1, 1, 'e')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1),
                     (('forward', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'd')), (0, 0, 'a', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 5),
                     (('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, -1, 'b'), (0, 0, 'O'), (1, 1, 'd')),
                      (0, 0, 'R', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, -1, 'O'), (0, 0, 'd')),
                     (0, 0, 'a', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('turn_left', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'b'), (1, 1, 'O')),
                     (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('turn_left', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'a'), (0, 2, 'b'), (1, 1, 'b')),
                     (0, 0, 'd', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('turn_left', (0, 0, 0, 0, 0, 0, 0), (0, -2, 'a'), (0, 0, 'b'), (1, -1, 'b')),
                     (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, -1, 'a'), (-1, 1, 'b'), (0, 0, 'b')),
                     (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('turn_left', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'b'), (1, -1, 'b')),
                     (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, 1, 'b'), (0, 0, 'a')),
                     (0, 0, 'd', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (
                     ('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, 1, 'b'), (0, 0, 'b'), (1, -1, 'a')),
                     (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('turn_left', (0, 0, 0, 0, 0, 0, 0), (-1, 1, 'b'), (0, 0, 'a')),
                     (0, 0, 'a', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (
                     ('forward', (0, 0, 0, 0, 0, 0, 0), (0, -1, 'e'), (0, 0, 'e'), (0, 1, 'R')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('forward', (0, 0, 0, 0, 0, 0, 0), (0, -2, 'e'), (0, -1, 'e'), (0, 0, 'R')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('forward', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'e'), (0, 1, 'e'), (0, 2, 'R')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('forward', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'd'), (0, 1, 'e')),
                     (0, 0, 'a', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (
                     ('forward', (0, 0, 0, 0, 0, 0, 0), (0, -1, 'd'), (0, 0, 'e')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (
                     ('forward', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'e'), (0, 1, 'f')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0), (
                     ('forward', (0, 0, 0, 0, 0, 0, 0), (0, -1, 'e'), (0, 0, 'f')),
                     (0, 0, 'h', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 0),
                     (('pickup', (0, 0, 0, 0, 0, 0, 0), (0, 0, 'g')), (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 1, 0))): (1, 0),
                     (('turn_right', (0, 0, 0, 0, 0, 1, 0), (-1, -1, 'e'), (0, 0, 'b'), (1, 1, 'a')),
                      (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (-1, -1, 'b'), (0, 0, 'a')),
                     (0, 0, 'd', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 4), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'e'), (1, 1, 'b')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (-1, 1, 'e'), (0, 0, 'd'), (1, 1, 'e')),
                     (0, 0, 'a', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (-2, 0, 'e'), (-1, -1, 'd'), (0, 0, 'e')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'e'), (1, -1, 'd'), (2, 0, 'e')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'b'), (0, 1, 'h')),
                     (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (0, -1, 'b'), (0, 0, 'h')),
                     (0, 0, 'f', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (-1, -1, 'e'), (0, 0, 'b'), (1, 1, 'a')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'e'), (1, -1, 'e')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (-1, 1, 'e'), (0, 0, 'e'), (1, -1, 'b')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (-1, 1, 'e'), (0, 0, 'b')),
                     (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (-2, 0, 'b'), (-1, -1, 'a'), (0, 0, 'a')),
                     (0, 0, 'd', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (-1, 1, 'b'), (0, 0, 'a'), (1, 1, 'a')),
                     (0, 0, 'd', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'b'), (1, -1, 'a'), (2, 0, 'a')),
                     (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'e'), (0, 1, 'd')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 3), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (0, -1, 'e'), (0, 0, 'd')),
                     (0, 0, 'a', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 3), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (-1, 1, 'e'), (0, 0, 'b')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (
                     ('turn_right', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'e'), (1, -1, 'e')),
                     (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (
                     ('forward', (0, 0, 0, 0, 0, 1, 0), (-1, -1, 'e'), (0, 0, 'e')),
                     (0, 0, 'Q', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (
                     ('forward', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'e'), (0, 1, 'e')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 4), (
                     ('forward', (0, 0, 0, 0, 0, 1, 0), (0, -1, 'e'), (0, 0, 'e'), (1, 1, 'e')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('forward', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'Q'), (0, 1, 'e'), (0, 2, 'd')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('forward', (0, 0, 0, 0, 0, 1, 0), (0, -1, 'Q'), (0, 0, 'e'), (0, 1, 'd')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('forward', (0, 0, 0, 0, 0, 1, 0), (0, -2, 'Q'), (0, -1, 'e'), (0, 0, 'd')),
                     (0, 0, 'a', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('forward', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'e'), (0, 1, 'e')),
                     (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 4), (
                     ('turn_left', (0, 0, 0, 0, 0, 1, 0), (-1, -1, 'b'), (-1, 1, 'a'), (0, 0, 'b')),
                     (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (
                     ('turn_left', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'b'), (0, 2, 'a'), (1, 1, 'b')),
                     (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('turn_left', (0, 0, 0, 0, 0, 1, 0), (0, -2, 'b'), (0, 0, 'a'), (1, -1, 'b')),
                     (0, 0, 'd', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('turn_left', (0, 0, 0, 0, 0, 1, 0), (-1, 1, 'a'), (0, 0, 'b'), (1, -1, 'Q')),
                     (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('turn_left', (0, 0, 0, 0, 0, 1, 0), (-1, 1, 'b'), (0, 0, 'Q')),
                     (0, 0, 'O', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('turn_left', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'a'), (1, -1, 'b')),
                     (0, 0, 'd', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('turn_left', (0, 0, 0, 0, 0, 1, 0), (-1, 1, 'a'), (0, 0, 'b'), (0, 1, 'a')),
                     (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (
                     ('turn_left', (0, 0, 0, 0, 0, 1, 0), (-1, 0, 'a'), (0, -1, 'b'), (0, 0, 'a')),
                     (0, 0, 'd', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (
                     ('turn_left', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'a'), (1, -1, 'b'), (1, 0, 'a')),
                     (0, 0, 'd', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('turn_left', (0, 0, 0, 0, 0, 1, 0), (0, -2, 'd'), (0, 0, 'e'), (1, -1, 'd')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('turn_left', (0, 0, 0, 0, 0, 1, 0), (-1, -1, 'd'), (-1, 1, 'e'), (0, 0, 'd')),
                     (0, 0, 'a', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('turn_left', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'd'), (0, 2, 'e'), (1, 1, 'd')),
                     (0, 0, 'a', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('forward', (0, 0, 0, 0, 0, 1, 0), (-1, 0, 'e'), (0, 0, 'e'), (1, 1, 'e')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('forward', (0, 0, 0, 0, 0, 1, 0), (-1, -1, 'e'), (0, 0, 'e')),
                     (0, 0, 'O', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 2), (
                     ('forward', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'e'), (1, 0, 'e')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 3), (
                     ('forward', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'e'), (1, 0, 'O'), (2, 0, 'd')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('forward', (0, 0, 0, 0, 0, 1, 0), (-1, 0, 'e'), (0, 0, 'O'), (1, 0, 'd')),
                     (0, 0, 'b', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('forward', (0, 0, 0, 0, 0, 1, 0), (-2, 0, 'e'), (-1, 0, 'O'), (0, 0, 'd')),
                     (0, 0, 'a', (0.0, 0, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('forward', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'e'), (1, 0, 'e')),
                     (0, 0, 'e', (0.0, 0, 0, 0, 0, 0, 0, 0))): (2, 3), (
                     ('toggle/activate', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'b'), (1, 0, 'b'), (1, 1, 'b')),
                     (0, 0, 'e', (0.965625, 1, 0, 0, 0, 0, 0, 0))): (1, 9), (
                     ('toggle/activate', (0, 0, 0, 0, 0, 1, 0), (-1, 0, 'b'), (0, 0, 'b'), (0, 1, 'b')),
                     (0, 0, 'e', (0.965625, 1, 0, 0, 0, 0, 0, 0))): (1, 9), (
                     ('toggle/activate', (0, 0, 0, 0, 0, 1, 0), (-1, -1, 'b'), (0, -1, 'b'), (0, 0, 'b')),
                     (0, 0, 'e', (0.965625, 1, 0, 0, 0, 0, 0, 0))): (1, 9), (
                     ('toggle/activate', (0, 0, 0, 0, 0, 1, 0), (-1, -1, 'b'), (0, 0, 'a')),
                     (0, 0, 'd', (0.965625, 1, 0, 0, 0, 0, 0, 0))): (1, 3), (
                     ('toggle/activate', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'f'), (0, 1, 'b')),
                     (0, 0, 'i', (0.965625, 1, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('toggle/activate', (0, 0, 0, 0, 0, 1, 0), (0, -1, 'f'), (0, 0, 'b'), (1, 1, 'a')),
                     (0, 0, 'e', (0.965625, 1, 0, 0, 0, 0, 0, 0))): (1, 1), (
                     ('toggle/activate', (0, 0, 0, 0, 0, 1, 0), (0, 0, 'b'), (1, 0, 'b'), (1, 1, 'b')),
                     (0, 0, 'b', (0.965625, 1, 0, 0, 0, 0, 0, 0))): (3, 9), (
                     ('toggle/activate', (0, 0, 0, 0, 0, 1, 0), (-1, 0, 'b'), (0, 0, 'b'), (0, 1, 'b')),
                     (0, 0, 'b', (0.965625, 1, 0, 0, 0, 0, 0, 0))): (1, 9), (
                     ('toggle/activate', (0, 0, 0, 0, 0, 1, 0), (-1, -1, 'b'), (0, 0, 'a')),
                     (0, 0, 'a', (0.965625, 1, 0, 0, 0, 0, 0, 0))): (1, 3)}
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
                                                  (808930194, 'j'), (1799812895, 'k')], 'raw_cell_shape': (32, 32, 3),
                          'raw_nptype': "<class 'numpy.uint8'>"}
    agent = nace.agent_module.Agent(rc_loc=(4, 5), score=0.965625, terminated=0,
                                    values_excluding_prefix=[0, 0, 0, 0, 0, 0])
                                    # values_exc_score_exc_term=[0, 0, 0, 0, 0, 0])
    actions = ['turn_left', 'turn_right', 'forward', 'pickup', 'toggle/activate']
    behavior_returned = 'BABBLE'
    whole_plan_returned = ['turn_right']


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
    # why is the keys held not 1? the pickup rule does not have enough preconditions, and hence fires everywhere increasing keys everywhere.
    # more experience reduces this.

    assert sum(planagent.get_values_exc_prefix()) >= 1 # is actually a huge number, not sure why


    # now pick up the key, and compare to what would actually happen to learn rule.

    post_action_world_str_list = ['.............',
                      '.............',
                      '.aeeeedbb....',
                      'Aaeeeedbb....',
                      'AaeeeRdbb....',
                      'Aabbbbkbb....',
                      'Aaaaaaaaa....',
                      'AAAAAAAAA....']

    post_action_ground_truth_world, _ = nace.world_module_numpy.NPWorld.from_string(
        post_action_world_str_list,
        view_dist_x=12,
        view_dist_y=5,
        agent_char_code_list=[agent_char], # must match actual agent char
        observed_times_str_list=[],
        int_2from_char_mapping=world_state_values["int_2from_char_list"]
    )

    ground_truth_post_action_agent = Agent(agent.get_rc_loc(), agent.get_score(), agent.get_terminated(), [0,0,0,0,1,0,0])


    # why do we create a new rule rather than reuse the last one ? different direction?
    #
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
            agent.get_rc_loc(),  # pre action agent location note (0,0) is top left
            world, # pre_action_world,  # pre action internal world model (partially observed) before last_action is applied
            set(new_rules), #rulesin,  # used in part1 and part2
           {}, #negrules,
            'pickup', #'last_action,
        {}, #rulesExcluded,
            post_action_ground_truth_world,  # i.e. this is the post action world model
            agent, #pre_action_agent,  # pre action agent
            ground_truth_post_action_agent,  # post action agent
            -1, #unobserved_code,  # value which indicates we can not see the true value of the cell
            agent_indication_raw_value_list,  # raw value of an agent, i.e. 'x', or the rgb value
            object_count_threshold=1,  # how unique values must be before they are considered. was 1, i.e. unique
            print_out_world_and_plan=True)

    print()




if __name__ == "__main__":
    pass
        # t3_why_frozen_lake_is_inefficient()
        # t7_pick_up_key_increases_keys_held()
        # t8_pick_up_key_increase_keys_held_with_more_experience()

