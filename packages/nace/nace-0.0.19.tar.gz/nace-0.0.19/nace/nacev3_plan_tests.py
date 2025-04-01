import json
import sys
import copy
import nace
import collections
import nace.color_codes

from nace.nace_v3 import _plan, _determine_behavior_and_action, _get_remaining_actions, nacev3_get_next_action, _predict_next_world_state
from nace.test_utilities import (convert_focus_set_to_internal_mapping, convert_rules_to_internal_mapping,
                                 get_xy_delta_for_action_list, convert_rule_evidence_to_internal_mapping)
from nace.hypothesis import Hypothesis_BestSelection

"""
Planning tests.


Note: the stub of a test can be easily created by code in nace.nace_v3.get_next_action() method, by playing a break point,
and copying the code_str variable, and pasting it into a test method.

"""

def t1_plan_will_go_for_food_over_varying_distances(check_oldest_cell_as_well=True):
    """
    Check a known world, that we will go for the food over varying distances.
    The food stays in the same location, the agents start position is moved.

    To debug, increase max_queue_len_score, max_queue_len_age until particular test passed.

    The table on congif tests give an idea of the value needed for the queue size given
    the distance to the next goal if the task is simple.


    @return:
    """

    world_str_list = [
        ['oooooooooooo',
         'o   o f    o',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o          o',
         'oooooooooooo'],
        (),
        ['25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
       '25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
       '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
       '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
       '20.0,21.0,22.0,23.0,24.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,',
       '19.0,19.0,19.0,19.0,19.0,19.0,19.0,16.0,15.0,14.0,13.0,14.0,',
       '18.0,18.0,18.0,18.0,18.0,18.0,18.0,16.0,15.0,14.0,14.0,14.0,']]
    rules = {
        # 0,0 == Free (' ') vs agent    x, y
        (('left', (0,),  (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
        (('up', (0,),    (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,0,))),
        (('down', (0,),  (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
        (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
        # 0,0 == unknown (u) vs agent
        (('left', (0,),  (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
        (('right', (0,), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
        (('down', (0,),  (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
        (('up', (0,),    (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,0,))),
        # 0,0 = wall (o) vs agent
        (('up', (0,),    (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,0,))),
        (('left', (0,),  (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,0,))),
        (('right', (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),
        (('down', (0,),  (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),
        # 0,0 == agent vs space
        (('down', (0,),  (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,0,))),
        (('up', (0,),    (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),
        (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,0,))),
        (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),
        # 0,0 == agent vs unknown (u)
        (('up', (0,),    (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),
        (('right', (0,), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,0,))),
        (('left', (0,),  (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),
        (('down', (0,),  (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,0,))),
        # 0,0 == agent vs wall (o)
        (('up', (0,),    (-1, 0, 'o'), (0, 0, 'x')), (0, 0, 'x', (0,0,))),
        (('right', (0,), (0, 0, 'x'), (0, 1, 'o')), (0, 0, 'x', (0,0,))),
        (('left', (0,),  (0, -1, 'o'), (0, 0, 'x')), (0, 0, 'x', (0,0,))),
        (('down', (0,),  (0, 0, 'x'), (1, 0, 'o')), (0, 0, 'x', (0,0,))),
        # 0,0 == agent vs food(f)
        (('down', (0,),  (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,0,))),
        (('left', (0,),  (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,0,))),
        (('up', (0,),    (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,0,))),
        (('right', (0,), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,0,))),
        # 0,0 == food vs agent (x)
        (('left', (0,),  (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,0,))),
        (('up', (0,),    (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,0,))),
        (('down', (0,),  (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,0,))),
        (('right', (0,), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,0,))),
    }

    actions = ['left', 'right', 'up', 'down']
    focus_set = {'f': 1, 'u': 1, 'x': 9}
    food_xy = (6, 1)
    oldest_cell_xy = (10, 5)
    totals = collections.defaultdict(float)
    test_count = 0

    # the max_queue_len needed to solve a prob appears to be about 2.8*action_length^4

    for (x, y, view_dist_x, view_dist_y, max_queue_len_score, max_queue_len_age) in [
        #                                                                               Action
        #                                                                               Length
        (7, 1,  3,  2,  11  ,  11 ) ,# food next to agent, (small) view distance            2
        (8, 1,  3,  2,  11  ,  11 ) ,# food near in the (small) view distance               2
        (3, 4, 30, 30,  77  , 120 ), # food not too far away in the (huge) view distance    6
        (1, 3, 30, 30, 102  , 150 ), # food not too far away in the (huge) view distance    7
        (2, 4, 30, 30,  81 ,  110 ), # food not too far away in the (huge) view distance    7
        (4, 4, 30, 30, 100,    68 ), # food not too far away in the (huge) view distance    7
        (1, 4, 30, 30, 100 ,  120 ), # food not too far away in the (huge) view distance    8
        (5, 4, 30, 30, 120 ,   80 ), # food not too far away in the (huge) view distance    8
        (6, 4, 30, 30, 200 ,  110 ), # food not too far away in the (huge) view distance    9
        (1, 5, 30, 30, 100 ,   72 ), # food not too far away in the (huge) view distance    9
        (7, 4, 30, 30, 300 ,  185 ), # food not too far away in the (huge) view distance   10
        (9, 4, 30, 30, 430 ,  270 ), # food not too far away in the (huge) view distance   12
        (8, 5, 30, 30, 480,   300 ), # food far away in the (huge) view distance           12
        ]:


        max_queue_len = max_queue_len_score
        if check_oldest_cell_as_well:
            max_queue_len = max(max_queue_len_score, max_queue_len_age)
        print("Testing", x, y, view_dist_x, view_dist_y, "Testing max_queue_len=",max_queue_len)
        test_count += 1
        t_world_str_list = copy.deepcopy(world_str_list)
        # insert the new agent
        new_line = world_str_list[0][y][:x] + 'x' + world_str_list[0][y][x + 1:]
        t_world_str_list[0][y] = new_line
        agent = nace.agent_module.Agent((y, x), 0, 0, ())
        world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
            t_world_str_list[0],
            view_dist_x=view_dist_x,
            view_dist_y=view_dist_y,
            agent_char_code_list=['x'],
            observed_times_str_list=world_str_list[2]
        )

        # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
        new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
        new_rules = convert_rules_to_internal_mapping(rules, world)

        world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])
        (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason,
         oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason,
         biggest_predicted_score_delta_actions, biggest_predicted_score_delta,
         biggest_predicted_score_delta_stopping_reason,
         smallest_predicted_score_delta_actions, smallest_predicted_score_delta,
         smallest_predicted_score_delta_stopping_reason,
         debugging_data) = (
            _plan(
                world,
                new_rules,
                actions,
                new_focus_set,
                agent,
                max_queue_length=max_queue_len))

        for k in debugging_data.keys():
            totals[k] += debugging_data[k]

        # check biggest score delta
        assert biggest_predicted_score_delta == 1
        dt1 = get_xy_delta_for_action_list(biggest_predicted_score_delta_actions)
        expected_deltas_for_goal = (food_xy[0] - x, food_xy[1] - y)
        assert dt1 == expected_deltas_for_goal

        # dt2 = get_xy_delta_for_action_list(lowest_conf_actions) # this may change when code logic short circuit removed
        # assert dt2 == expected_deltas
        # assert lowest_conf_achieves_goal

        # if we can see the oldest cell, we should find it.
        if check_oldest_cell_as_well:
            oldest_cell_xy_delta = get_xy_delta_for_action_list(oldest_age_actions)
            expected_deltas_for_oldest_cell = (oldest_cell_xy[0] - x, oldest_cell_xy[1] - y)
            if abs(expected_deltas_for_oldest_cell[0]) <= view_dist_x and abs(
                    expected_deltas_for_oldest_cell[1]) <= view_dist_y:
                if oldest_cell_xy_delta != expected_deltas_for_oldest_cell:
                    print("Oldest cell check passed.")
                    print("Oldest cell: got", oldest_cell_xy_delta, 'expected', expected_deltas_for_oldest_cell)
                assert oldest_cell_xy_delta == expected_deltas_for_oldest_cell


        print("___")

        for k in debugging_data.keys():
            print (k,"total=", totals[k], "n=", test_count, "average=", totals[k]/test_count)

    print("test complete")



def t2_plan_find_required_queue_length():
    """
    For a known world and goal, find the smallest queue length that succeeds.
    The food stays in the same location, the agents start position is moved.

    @return:
    """
    world_str_list = [
        ['oooooooooooo',
         'o   o f    o',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o          o',
         'oooooooooooo'], (), ['25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,',
                               '19.0,19.0,19.0,19.0,19.0,19.0,19.0,16.0,15.0,14.0,13.0,14.0,',
                               '18.0,18.0,18.0,18.0,18.0,18.0,18.0,16.0,15.0,14.0,14.0,14.0,']]
    rules = {
        # 0,0 == Free (' ') vs agent    x, y
        (('left', (),  (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))),
        (('up', (),    (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,))),
        (('down', (),  (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
        (('right', (), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
        # 0,0 == unknown (u) vs agent
        (('left', (),  (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,))),
        (('right', (), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
        (('down', (),  (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
        (('up', (),    (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,))),
        # 0,0 = wall (o) vs agent
        (('up', (),    (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,))),
        (('left', (),  (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,))),
        (('right', (), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
        (('down', (),  (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
        # 0,0 == agent vs space
        (('down', (),  (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,))),
        (('up', (),    (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
        (('right', (), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,))),
        (('left', (), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
        # 0,0 == agent vs unknown (u)
        (('up', (),    (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
        (('right', (), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,))),
        (('left', (),  (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
        (('down', (),  (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,))),
        # 0,0 == agent vs wall (o)
        (('up', (),    (-1, 0, 'o'), (0, 0, 'x')), (0, 0, 'x', (0,))),
        (('right', (), (0, 0, 'x'), (0, 1, 'o')), (0, 0, 'x', (0,))),
        (('left', (),  (0, -1, 'o'), (0, 0, 'x')), (0, 0, 'x', (0,))),
        (('down', (),  (0, 0, 'x'), (1, 0, 'o')), (0, 0, 'x', (0,))),
        # 0,0 == agent vs food(f)
        (('down', (),  (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
        (('left', (),  (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
        (('up', (),    (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
        (('right', (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
        # 0,0 == food vs agent (x)
        (('left', (),  (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
        (('up', (),    (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
        (('down', (),  (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
        (('right', (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
    }

    actions = ['left', 'right', 'up', 'down']
    focus_set = {'f': 1, 'u': 1, 'x': 9}
    food_xy = (6, 1)
    oldest_cell_xy = (10, 5)
    totals = collections.defaultdict(float)
    test_count = 0

    # the max_queue_len needed to solve a prob appears to be about 2.8*action_length^4

    results = {}

    for config_tuple in [                                                           #  food distance
        (8, 1,  3,  2, 11     ), # food near in the (small) view distance                2
        (3, 4, 30, 30, 77     ), # food not too far away in the (huge) view distance     6
        (1, 3, 30, 30, 102    ), # food not too far away in the (huge) view distance     7
        (2, 4, 30, 30, 81     ), # food not too far away in the (huge) view distance     7
        (4, 4, 30, 30, 68     ), # food not too far away in the (huge) view distance     7
        (1, 4, 30, 30, 81     ), # food not too far away in the (huge) view distance     8
        (5, 4, 30, 30, 80     ), # food not too far away in the (huge) view distance     8
        (6, 4, 30, 30, 110    ), # food not too far away in the (huge) view distance     9
        (1, 5, 30, 30, 72     ), # food not too far away in the (huge) view distance     9
        (7, 4, 30, 30, 185     ), # food not too far away in the (huge) view distance    10
        (9, 4, 30, 30, 270     ), # food not too far away in the (huge) view distance    12
        (8, 5, 30, 30, 300     ), # food far away in the (huge) view distance            12

    ]:
        (x, y, view_dist_x, view_dist_y, max_queue_len) = config_tuple
        check_biggest_score = True
        check_oldest_cell = True

        success = True
        results[config_tuple] = {}

        while success and max_queue_len > 10:
            print("Testing max_queue_len=", max_queue_len)
            print("Testing", x, y, view_dist_x, view_dist_y, max_queue_len)
            test_count += 1
            t_world_str_list = copy.deepcopy(world_str_list)
            new_line = world_str_list[0][y][:x] + 'x' + world_str_list[0][y][x + 1:]
            t_world_str_list[0][y] = new_line
            agent = nace.agent_module.Agent((y, x), 0, 0, ())

            world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
                t_world_str_list[0],
                view_dist_x=view_dist_x,
                view_dist_y=view_dist_y,
                agent_char_code_list=['x'],
                observed_times_str_list=world_str_list[2]
            )

            # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
            new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
            new_rules = convert_rules_to_internal_mapping(rules, world)

            world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])
            (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason,
             oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason,
             biggest_predicted_score_delta_actions, biggest_predicted_score_delta,
             biggest_predicted_score_delta_stopping_reason,
             smallest_predicted_score_delta_actions, smallest_predicted_score_delta,
             smallest_predicted_score_delta_stopping_reason,
             debugging_data) = (
                _plan(
                    world,
                    new_rules,
                    actions,
                    new_focus_set,
                    agent,
                    max_queue_length=max_queue_len))

            for k in debugging_data.keys():
                totals[k] += debugging_data[k]

            if check_biggest_score:
                best_score_delta_xy = get_xy_delta_for_action_list(biggest_predicted_score_delta_actions)
                expected_deltas_for_goal = (food_xy[0] - x, food_xy[1] - y)
                if best_score_delta_xy != expected_deltas_for_goal or biggest_predicted_score_delta != 1 :
                    success = False
                    print("best_score_delta_xy failed")

            if check_oldest_cell:
                # if we can see the oldest cell, we should find it.
                oldest_cell_delta_xy = get_xy_delta_for_action_list(oldest_age_actions)
                expected_deltas_for_oldest_cell = (oldest_cell_xy[0] - x, oldest_cell_xy[1] - y)
                if abs(expected_deltas_for_oldest_cell[0]) <= view_dist_x and abs(
                        expected_deltas_for_oldest_cell[1]) <= view_dist_y:
                    if oldest_cell_delta_xy != expected_deltas_for_oldest_cell:
                        success = False
                        print("Oldest cell: got", oldest_cell_delta_xy, 'expected', expected_deltas_for_oldest_cell)
                        print("oldest_cell_delta_xy failed")
                else:
                    print("not testing - view distance too small")

            if success:
                if check_oldest_cell:
                    results[config_tuple]["check_oldest_cell"] = max_queue_len
                if check_biggest_score:
                    results[config_tuple]["check_biggest_score"] = max_queue_len
            else:
                print("Results", results)
                for k in results.keys():
                    print(k, results[k])


            max_queue_len = int(max_queue_len*0.95)

    print("results", results)

    print("test complete")




def t11_plan_no_food_full_observation():
    """
    @return:
    """
    world_str_list = [
        ['oooooooooooo',
         'o   o   x  o',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o          o',
         'oooooooooooo'], (), ['25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,',
                               '20.0,19.0,19.0,19.0,19.0,19.0,19.0,16.0,15.0,14.0,13.0,20.0,', # <- goes for the 4th from left in this row
                               '20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,']]
    #                                                              Score
    #                                                              Delta
    rules = {(('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,0,))),
             (('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,0,))),
             (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),

             (('left', (0,), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,0,))),
             (('left', (0,), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),
             (('up', (0,), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,0,))),

             (('up', (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),
             (('left', (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),

             # (('left', (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
             # (('up', (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
             # (('left', (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             # (('down', (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
             # (('down', (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             # (('up', (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             # (('right', (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
             # (('right', (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             }
    actions = ['left', 'right', 'up', 'down']
    focus_set = {'u': 1, 'x': 5}
    agent = nace.agent_module.Agent((1, 8), 0, 0, ())

    world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        world_str_list[0],
        view_dist_x=100,
        view_dist_y=100,
        agent_char_code_list=['x'],
        observed_times_str_list=world_str_list[2]
    )
    world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])

    # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
    new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
    new_rules = convert_rules_to_internal_mapping(rules, world)


    (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason,
     oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason,
     biggest_predicted_score_delta_actions, biggest_predicted_score_delta, biggest_predicted_score_delta_stopping_reason,
     smallest_predicted_score_delta_actions, smallest_predicted_score_delta,
     smallest_predicted_score_delta_stopping_reason,
     debbugging_data) = (
        _plan(
            world,
            new_rules,
            actions,
            new_focus_set,
            agent,
            max_num_actions = 16
        ))

    rc_uncertain_actions = nace.test_utilities.get_rc_delta_for_action_list(lowest_conf_actions)
    rc_oldest_actions = nace.test_utilities.get_rc_delta_for_action_list(oldest_age_actions)

    print("rc_oldest_actions",rc_oldest_actions,"lowest_AIRIS_confidence",lowest_AIRIS_confidence,"rc_uncertain_actions",rc_uncertain_actions,"oldest_age",oldest_age)

    assert rc_uncertain_actions in [(0, -1), (1,0), (0,1), (-1, 0) ]  # random action in actions list
    assert lowest_AIRIS_confidence == 1.0
    assert rc_oldest_actions == (4, 2)  # nearest old square, observed at t=16  ( 4 , -1)
    assert oldest_age == 13 # = 26-13


def t1_plan_no_food_partial_observation():
    """
    @return:
    """
    world_str_list = [
        ['oooooooooooo',
         'o   o   x  o',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o          o',
         'oooooooooooo'], (), ['25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '26.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '26.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '26.0,21.0,22.0,23.0,24.0,25.0,25.0,25.0,25.0,25.0,25.0,26.0,',
                               '26.0,19.0, 0.0,19.0,19.0,19.0,19.0,16.0,15.0,14.0,13.0,26.0,',
                               '26.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,']]
    #                                                              Score
    #                                                              Delta
    rules = {(('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,0,))),
             (('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,0,))),
             (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),

             (('left', (0,), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,0,))),
             (('left', (0,), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),
             (('up', (0,), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,0,))),

             (('up', (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),
             (('left', (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),

             # (('left', (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
             # (('up', (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
             # (('left', (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             # (('down', (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
             # (('down', (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             # (('up', (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             # (('right', (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
             # (('right', (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             }
    actions = ['left', 'right', 'up', 'down']
    focus_set = {'u': 1, 'x': 5}
    agent = nace.agent_module.Agent((1, 8), 0, 0, ())

    world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        world_str_list[0],
        view_dist_x=4,
        view_dist_y=4,
        agent_char_code_list=['x'],
        observed_times_str_list=world_str_list[2]
    )
    world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])

    # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
    new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
    new_rules = convert_rules_to_internal_mapping(rules, world)

    (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason,
     oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason,
     biggest_predicted_score_delta_actions, biggest_predicted_score_delta, biggest_predicted_score_delta_stopping_reason,
     smallest_predicted_score_delta_actions, smallest_predicted_score_delta,
     smallest_predicted_score_delta_stopping_reason,
     debbugging_data) = (
        _plan(
            world,
            new_rules,
            actions,
            new_focus_set,
            agent))

    oldest_age_actions_delta_xy = get_xy_delta_for_action_list(oldest_age_actions)
    print("oldest age xy delta", oldest_age_actions_delta_xy)
    print("biggest_predicted_score_delta_actions",biggest_predicted_score_delta_actions)
    assert oldest_age_actions_delta_xy == (-6, 4)  # nearest un observed cell
    assert lowest_AIRIS_confidence == 1.0 # fully understood dynamics
    assert len(biggest_predicted_score_delta_actions) == 1  # no food, not best score actions, a 0 score will return an action


def t2_plan_reward_and_unknown_value():
    """
    If unknown value (q) introduced nearer the agent than the known food,
    best_actions still goes for the food (but may not be found if far away),
    but best_action_combination_for_revisit will go for the unobserved spot.

    @return:
    """
    world_str_list = [
        ['oooooooooooo',
         'o   o   x  o',
         'o         qo', # q does not exist in rules, and so has low confidence
         'o   oooooooo',
         'o          o',
         'o      f   o',  # food should give a reward.
         'oooooooooooo'], (), ['25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,',
                               '19.0,19.0,19.0,19.0,19.0,19.0,19.0,16.0,15.0,14.0,13.0,12.0,',
                               '18.0,18.0,18.0,18.0,18.0,18.0,18.0,16.0,15.0,14.0,13.0,12.0,']]
    rules = {

        # open space
        (('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,))),
        (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
        (('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,))),
        (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
        (('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))),
        (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
        (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
        (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,))),

        # walls
        (('up', (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,))),
        (('up', (0,), (-1, 0, 'o'), (0, 0, 'x')), (0, 0, 'x', (0,))),
        (('right', (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
        (('right', (0,), (0, 0, 'x'), (0, 1, 'o')), (0, 0, 'x', (0,))),
        (('left', (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,))),
        (('left', (0,), (0, -1, 'o'), (0, 0, 'x')), (0, 0, 'x', (0,))),
        (('down', (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
        (('down', (0,), (0, 0, 'x'),  (-1, 0, 'o')), (0, 0, 'x', (0,))),

        # food
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
    focus_set = {'f': 1, 'x': 9,  'q': 1}
    agent = nace.agent_module.Agent((1, 8), 0, 0, ())
    world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        world_str_list[0],
        view_dist_x=50,
        view_dist_y=50,
        agent_char_code_list=['x'],
        observed_times_str_list=world_str_list[2],
    )
    world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])

    assert world.get_char_at_rc(agent.get_rc_loc()[0],agent.get_rc_loc()[1], agent_indication_embedded_value_list=[]) == 'x'

    # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
    new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
    new_rules = convert_rules_to_internal_mapping(rules, world)


    # _plan fires the rule for the food when the agent is no where near the food. Why? what should it do?

    (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason,
     oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason,
     biggest_predicted_score_delta_actions, biggest_predicted_score_delta, biggest_predicted_score_delta_stopping_reason,
     smallest_predicted_score_delta_actions, smallest_predicted_score_delta,
     smallest_predicted_score_delta_stopping_reason,
     debbugging_data) = (
        _plan(
            world,
            new_rules,
            actions,
            new_focus_set,
            agent,
            max_num_actions=20,
            max_queue_length=20,
            shuffle_actions=False,
            short_curcuit_planning=False,
            brute_force_focus_next_step=True,
            continue_planning_threshold=0.5
        )
    )

    print("debugging data:",json.dumps(debbugging_data, indent=2))

    rc_lowest_conf = nace.test_utilities.get_rc_delta_for_action_list(lowest_conf_actions)
    print("rc_lowest_conf",rc_lowest_conf, "lowest_AIRIS_confidence", lowest_AIRIS_confidence)
    rc_biggest_score = nace.test_utilities.get_rc_delta_for_action_list(biggest_predicted_score_delta_actions)
    print("biggest_predicted_score_delta=",biggest_predicted_score_delta, "rc", rc_biggest_score) # expect 1

    assert rc_lowest_conf == (1, 2)  # finds uncertain cell location 'q', or first action location (i.e left (0,-1))


    # assert rc_biggest_score == (4, -1)  # ideally would get food, but unknown q means dynamics are not known
    # so hallucinations start, including assigning the unknown q a reward

    print("")


def t12_go_for_unobserved():
    """
    If no food and unobserved introduced near (time == -inf), go for unobserved.
    best_actions == best_action_combination_for_revisit

    @return:
    """
    world_str_list = [
        ['oooooooooooo',
         'o   o  kx  o',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o          o',
         'oooooooooooo'], (), ['25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '25.0,25.0,25.0,23.0,24.0,26.0, 0.0,26.0,27.0,26.0,26.0,26.0,', # <- agent on the 27 <- oldest observed on the 0.0
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,', #
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,',
                               '19.0,19.0,19.0,19.0,19.0,19.0,19.0,16.0,15.0,14.0,13.0,12.0,',
                               '18.0,18.0,18.0,18.0,18.0,18.0,18.0,16.0,15.0,14.0,13.0,12.0,']]
    rules = {(('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
             (('left', (0,), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,0,))),
             (('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
             (('left', (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,0,))),
             (('left', (0,), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),
             (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),
             (('up', (0,), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),

             # (('left', (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))), # f is not on the map, so has no encoding.
             # (('left', (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             # (('up', (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
             # (('up', (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             # (('down', (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
             # (('down', (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             # (('right', (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             # (('right', (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
             }
    actions = ['left', 'right', 'up', 'down']
    focus_set = {'u': 1, 'x': 9, 'k':1 }
    agent = nace.agent_module.Agent((1, 8), 0, 0, ())

    world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        world_str_list[0],
        view_dist_x=4,
        view_dist_y=4,
        agent_char_code_list=['x'],
        observed_times_str_list=world_str_list[2]
    )

    # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
    new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
    new_rules = convert_rules_to_internal_mapping(rules, world)

    (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason,
     oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason,
     biggest_predicted_score_delta_actions, biggest_predicted_score_delta, biggest_predicted_score_delta_stopping_reason,
     smallest_predicted_score_delta_actions, smallest_predicted_score_delta,
     smallest_predicted_score_delta_stopping_reason,
     debbugging_data) = (
        _plan(
            world,
            new_rules,
            actions,
            new_focus_set,
            agent))

    rc_delta_oldest = nace.test_utilities.get_rc_delta_for_action_list(oldest_age_actions)
    print("rc_delta_oldest",rc_delta_oldest)
    print("oldest cell rc location ",agent.get_rc_loc()[0] + rc_delta_oldest[0], agent.get_rc_loc()[1] + rc_delta_oldest[1])

    rc_delta_uncertain = nace.test_utilities.get_rc_delta_for_action_list(lowest_conf_actions)
    print("rc_delta_uncertain",rc_delta_uncertain)  # should go for the k
    assert rc_delta_oldest == (0, -2) # should be -2, the location of the 0.0
    assert rc_delta_uncertain == (0, -1)
    print("")


def t4_food_too_far_away_go_for_oldest_observed():
    """
    If food too far away and with 'u' nearby,

    oldest_age_actions ==  go for furthest point on board with oldest age we can reach

    @return:
    """
    world_str_list = [
        ['oooooooooooo',
         'o   o   x  o',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o       f  o',
         'oooooooooooo'], (),
        ['25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
         '25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,27.0,26.0,26.0,26.0,', # < agent on the 27
         '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
         '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
         '20.0,21.0,22.0,23.0,24.0,25.0,25.0,25.0,25.0,25.0,25.0,20.0,',
         '19.0,19.0,19.0,19.0,19.0,19.0,17.0,16.0,15.0,14.0,13.0,20.0,', # <- get to the 17 on this line
         '20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,20.0,']]
    rules = {
        (('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
        (('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,0,))),
        (('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,0,))),
        (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),
        (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
        (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
        (('up', (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,0,))),
        (('right', (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),
        (('left', (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,0,))),
        (('down', (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),
        (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),

        (('left', (0,), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
        (('right', (0,), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
        (('down', (0,), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,0,))),
        (('down', (0,), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
        (('left', (0,), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),
        (('up', (0,), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,0,))),
        (('up', (0,), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),
        (('right', (0,), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,0,))),
        (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,0,))),

        (('left', (0,), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,0,))),
        (('left', (0,), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,0,))),
        (('up', (0,), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,0,))),
        (('up', (0,), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,0,))),
        (('down', (0,), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,0,))),
        (('down', (0,), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,0,))),
        (('right', (0,), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,0,))),
        (('right', (0,), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,0,))),
    }
    actions = ['left', 'right', 'up', 'down']
    focus_set = {'f': 1, 'u': 1, 'x': 9}
    agent_initial_xy_loc = (8, 1)
    agent = nace.agent_module.Agent( (agent_initial_xy_loc[1],agent_initial_xy_loc[0] ), 0, 0, ())

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


    (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason,
     oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason,
     biggest_predicted_score_delta_actions, biggest_predicted_score_delta, biggest_predicted_score_delta_stopping_reason,
     smallest_predicted_score_delta_actions, smallest_predicted_score_delta,
     smallest_predicted_score_delta_stopping_reason,
     debbugging_data) = (
        _plan(
            world,
            new_rules,
            actions,
            new_focus_set,
            agent,
            max_num_actions=12 # food to far away - so we won't find it.
        ))

    xy_dt_bc = get_xy_delta_for_action_list(oldest_age_actions)
    xy_dt_ba = get_xy_delta_for_action_list(lowest_conf_actions)

    time_at_destination, board_value = nace.test_utilities.get_time_and_board_at_destination([agent_initial_xy_loc, xy_dt_bc], world)
    print("time_at_destination",time_at_destination,"board_value",board_value)
    assert time_at_destination == 17  # cant walk into walls, so the oldest non wall cell it can reach with search


def t5_equal_distance_food():
    """
    @return:
    """
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
         '20,21,22,23,24,26,9999,26,26,26,26,26,',
         '20,21,22,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,25,25,25,25,25,25,25,',
         '19,19,19,19,19,19,19,16,15,14,13,12,',
         '18,18,18,18,18,18,18,16,15,14,13,12,']]
    rules = {(('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
             (('left', (0,), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,0,))),
             (('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
             (('left', (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,0,))),
             (('left', (0,), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),
             (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),
             (('up', (0,), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),

             (('left', (0,), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,0,))),
             (('left', (0,), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,0,))),
             (('up', (0,), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,0,))),
             (('up', (0,), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,0,))),
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


    (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason,
     oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason,
     biggest_predicted_score_delta_actions, biggest_predicted_score_delta, biggest_predicted_score_delta_stopping_reason,
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
    assert xy_dt2 in [(1,1),(-1, 1)]  # go for food - we can not be sure which it will go for.
    assert biggest_predicted_score_delta == 1


def t6_oldest_age_and_goal_same_square():
    """

    oldest age and goal are in the same square, how / what does the code return?

    @return:
    """
    world_str_list = [
        ['oooooooooooo',
         'o   o     xo',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o         fo',
         'oooooooooooo'], (),
        ['25,25,25,23,24,26,26,26,26,26,26,26,',
         '25,25,25,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,25,25,25,25,25,25,25,',
         '19,19,19,19,19,19,19,16,15,14,13,25,',
         '25,25,25,25,25,25,25,25,25,25,25,25,']]
    rules = {(('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
             (('left', (0,), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,0,))),
             (('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
             (('left', (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,0,))),
             (('left', (0,), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),
             (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),
             (('up', (0,), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),

             (('left', (0,), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,0,))),
             (('left', (0,), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,0,))),
             (('up', (0,), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,0,))),
             (('up', (0,), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,0,))),
             }
    actions = ['left', 'right', 'up', 'down']
    focus_set = {'f': 1, 'u': 1, 'x': 9}
    agent = nace.agent_module.Agent((1, 10), 0, 0, ())

    world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        world_str_list[0],
        view_dist_x=12,
        view_dist_y=5,
        agent_char_code_list=['x'],
        observed_times_str_list=world_str_list[2]
    )
    world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])

    assert world.get_char_at_rc(agent.get_rc_loc()[0], agent.get_rc_loc()[1],
                                agent_indication_embedded_value_list=[]) == 'x'

# convert focus_set and rules to use embeddings rather than char (which is used for convenience)
    new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
    new_rules = convert_rules_to_internal_mapping(rules, world)


    (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason,
     oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason,
     biggest_predicted_score_delta_actions, biggest_predicted_score_delta, biggest_predicted_score_delta_stopping_reason,
     smallest_predicted_score_delta_actions, smallest_predicted_score_delta,
     smallest_predicted_score_delta_stopping_reason,
     debbugging_data) = (
        _plan(
            world,
            new_rules,
            actions,
            new_focus_set,
            agent,
        max_num_actions=22,
        max_queue_length=55000))

    xy_goal = get_xy_delta_for_action_list(biggest_predicted_score_delta_actions)
    xy_oldest = get_xy_delta_for_action_list(oldest_age_actions)

    assert xy_goal == (0, 4)
    print("xy_oldest",xy_oldest)
    assert xy_oldest == (0, 4)
    assert biggest_predicted_score_delta == 1


def t7_fully_known_world_and_rules_but_no_score_increasing_target():
    """
    Oldest age is far away. there is no food.  Does the code behave?
    @return:
    """
    world_str_list = [
        ['oooooooooooo',
         'o   o     xo',
         'o          o',
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
    rules = {(('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
             (('left', (0,), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,0,))),
             (('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
             (('left', (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,0,))),
             (('left', (0,), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),
             (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),
             (('up', (0,), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),

             # (('left', (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
             # (('left', (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             # (('up', (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
             # (('up', (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             # (('down', (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
             # (('down', (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             # (('right', (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             # (('right', (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
             }
    actions = ['left', 'right', 'up', 'down']
    focus_set = {'u': 1, 'x': 9}
    agent = nace.agent_module.Agent((1, 10), 0, 0, ())

    world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        world_str_list[0],
        view_dist_x=12,
        view_dist_y=5,
        agent_char_code_list=['x'],
        observed_times_str_list=world_str_list[2]
    )
    world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])

    assert world.get_char_at_rc(agent.get_rc_loc()[0], agent.get_rc_loc()[1],
                                agent_indication_embedded_value_list=[]) == 'x'

    # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
    new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
    new_rules = convert_rules_to_internal_mapping(rules, world)


    (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason, oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason,
     biggest_predicted_score_delta_actions, biggest_predicted_score_delta, biggest_predicted_score_delta_stopping_reason,
     smallest_predicted_score_delta_actions, smallest_predicted_score_delta,
     smallest_predicted_score_delta_stopping_reason,
     debbugging_data) = (
        _plan(
            world,
            new_rules,
            actions,
            new_focus_set,
            agent,
            max_num_actions=11,
        ))

    xy_lowest_conf = get_xy_delta_for_action_list(lowest_conf_actions)
    xy_oldest = get_xy_delta_for_action_list(oldest_age_actions)
    print("xy_oldest",xy_oldest)
    print("xy_lowest_conf",xy_lowest_conf)
    print("oldest_age.item()",oldest_age.item())
    print("lowest_AIRIS_confidence",lowest_AIRIS_confidence)

    assert xy_lowest_conf in [(-1, 0), (0,-1), (1,0), (0,1) ]  # this can move to 1 step in any direction
    assert xy_oldest == (-7, 4)
    assert oldest_age.item() == (26.0 - 19.0)
    assert lowest_AIRIS_confidence == 1.0  # the rules are fully known, and may well to world.


def t14_plan_no_food_partial_observation_best_for_revisit():
    """
    @return:
    """
    world_str_list = [
        ['oooooooooooo',
         'o   o   x  o',
         'o          o',
         'o   oooooooo',
         'o       q  o', # u is in rules, q is not.
         'o       u  o', # u is on oldest square
         'oooooooooooo'], (), ['25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,',
                               '25.0,25.0,24.0,23.0,22.0,21.0,20.0,19.0,15.0,25.0,25.0,25.0,',
                               '25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,']]
    #                                                              Score
    #                                                              Delta
    rules = {(('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,0,))),
             (('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,0,))),
             (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),

             (('left', (0,), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,0,))),
             (('left', (0,), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,0,))),
             (('up', (0,), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,0,))),

             (('up', (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),
             (('left', (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),

             # (('left', (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
             # (('up', (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
             # (('left', (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             # (('down', (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
             # (('down', (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             # (('up', (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             # (('right', (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
             # (('right', (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             }
    actions = ['left', 'right', 'up', 'down']
    focus_set = { 'u': 1, 'x': 5, 'q':1}
    agent = nace.agent_module.Agent((1, 8), 0, 0, ())

    for i in range(1):  # seems stable, I thought it wasn't

        world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
            world_str_list[0],
            view_dist_x=4,
            view_dist_y=4,
            agent_char_code_list=['x'],
            observed_times_str_list=world_str_list[2]
        )
        world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])

        assert world.get_char_at_rc(agent.get_rc_loc()[0], agent.get_rc_loc()[1],
                                    agent_indication_embedded_value_list=[]) == 'x'

        # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
        new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
        new_rules = convert_rules_to_internal_mapping(rules, world)

        (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason, oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason,
         biggest_predicted_score_delta_actions, biggest_predicted_score_delta, biggest_predicted_score_delta_stopping_reason,
         smallest_predicted_score_delta_actions, smallest_predicted_score_delta,
         smallest_predicted_score_delta_stopping_reason,
         debbugging_data) = (
            _plan(
                world,
                new_rules,
                actions,
                new_focus_set,
                agent,
                max_queue_length=300,
                max_num_actions=14
            ))

        rc_delta_oldest = nace.test_utilities.get_rc_delta_for_action_list(oldest_age_actions)

        print("rc_delta_oldest", rc_delta_oldest) # returns (4, -1)
        print("oldest_age", oldest_age)
        assert rc_delta_oldest in [(4, 0)] # u?  If we do not serach far enough, this is not found (max_num_actions < 14)

        rc_lowest_conf = nace.test_utilities.get_rc_delta_for_action_list(lowest_conf_actions)
        assert rc_lowest_conf in [(3, 0)]  # q
        print("")



def t9_actual_example_where_we_fail_1():
    """
    @return:
    """
    time = 26
    world_str_list = [
        ['oooooooooooo',
         'o   o      o',
         'o       x  o',
         'o   oooooooo',
         'o       u  o',
         'o     ......',
         '............'], (),

        [
            '7,   8,  10,  11,  12,  14,  14,  14,  14,  14,  14,  14,',
            '7,   8,  10,  11,  12,  14,  14,  14,  14,  14,  14,  14,',
            '7,   8,  10,  11,  12,  14,  14,  14,  15,  14,  14,  14,',  # <- agent is on the 15
            '7,   8,  10,  11,  12,  14,  14,  14,  14,  14,  14,  14,',
            '7,   8,   9,   9,   9,  14,  14,  14,  14,  14,  14,  14,',
            '5,   5,   5,   5,   5,   5, -inf, -inf, -inf, -inf, -inf, -inf,',
            '0,   0,   0,   0,   0,   0, -inf, -inf, -inf, -inf, -inf, -inf,'
        ],

    ]
    #                                                              Score
    #                                                              Delta
    rules = {(('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,0,))),
             (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),
             (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,0,))),
             (('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,0,))),
             (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,0,))),
             (('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,0,))),
             (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,0,))),
             (('up', (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,0,))),
             (('left', (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,0,))),

             # (('up', (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1, 0))),
             # (('left', (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1, 0))),
             # (('up', (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1, 0))),
             # (('right', (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1, 0))),
             # (('left', (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1, 0))),
             # (('down', (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1, 0))),
             # (('right', (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1, 0))),
             # (('down', (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1, 0)))

             }

    actions = ['left', 'right', 'up', 'down']
    focus_set = { 'x': 11}
    agent = nace.agent_module.Agent((2, 8), 0, 0, ())

    for i in range(1):  # seems stable, I thought it wasn't

        world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
            world_str_list[0],
            view_dist_x=30,
            view_dist_y=20,
            agent_char_code_list=['x'],
            observed_times_str_list=world_str_list[2]
        )
        world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])

        # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
        new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
        new_rules = convert_rules_to_internal_mapping(rules, world)

        (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason,
         oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason,
         biggest_predicted_score_delta_actions, biggest_predicted_score_delta, biggest_predicted_score_delta_stopping_reason,
         smallest_predicted_score_delta_actions, smallest_predicted_score_delta,
         smallest_predicted_score_delta_stopping_reason,
         debbugging_data) = (
            _plan(
                world,
                new_rules,
                actions,
                new_focus_set,
                agent))

        dxdy_best_revisit = get_xy_delta_for_action_list(oldest_age_actions)

        print("dxdy best for revist", dxdy_best_revisit)
        print("lowest_AIRIS_confidence",lowest_AIRIS_confidence)
        assert dxdy_best_revisit in [(-2, 3),  # nearest -inf cell
                                     (-5, 4),  # nearest '.' cell
                                     (-5, 3),  # near '.' cell
                                     ]
        assert lowest_AIRIS_confidence == 0.6666666666666666 # maybe if this was 0.5 as it was originally, comparison between cells would be better?


def t9_actual_example_where_we_oscillate_1():
    # this happens in the cups on table challenge.
    # if the cup is on row 4, the agent has not learnt it can move the cup up and down (i guess)
    # possibility 2: when we find the score increasing action, we do not exit the search at that stage.
    # NOTE: None of the rules in this cause a +1 to the score, and hence will fail

    # # Configure hypotheses to use Euclidean space properties if desired
    # nace.hypothesis.Hypothesis_UseLRUDMovementOpAssumptions(
    #     'left',
    #     'right',
    #     'up',
    #     'down',
    #     nace.world_module.drop,
    #     "DisableOpSymmetryAssumption" in sys.argv,
    # )
    nace.world_module.World_objective = nace.world_module.World_CupIsOnTable

    time = 79
    world_str_list = [
        ['oooooooooooo',
         'o          o',
         'o          o',
         'o     ooooTo',
         'o ux       o',
         'o          o',
         'oooooooooooo'], (),
        [
            '78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,',
            '78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,',
            '78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,',
            '78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,',
            '78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,',
            '78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,',
            '78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,'
        ],

    ]
    #                                                              Score
    #                                                              Delta
    rules_a = {(('down', (0,), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0, 0))),
               (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))),
               (('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0, 0))),
               (('right', (0,), (0, 0, 'x'), (0, 1, 'T')), (0, 0, 'x', (0, 0))),
               (('up', (0,), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0, 0))),
               (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))),
               (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0, 0))),
               (('left', (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0, 0))),
               (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))),
               (('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0, 0))),
               (('down', (0,), (0, 0, 'u'), (1, 0, 'T')), (0, 0, ' ', (0, 0))),
               (('down', (0,), (-1, 0, 'x'), (0, 0, 'T')), (0, 0, 'T', (0, 0))),
               (('down', (0,), (0, 0, 'x'), (1, 0, 'T')), (0, 0, 'x', (0, 0))),
               (('right', (0,), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0, 0))),
               (('right', (0,), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0, 0))),
               (('down', (0,), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0, 0))),
               (('left', (0,), (0, -1, 'T'), (0, 0, 'x')), (0, 0, 'x', (0, 0))),
               (('left', (0,), (0, 0, 'T'), (0, 1, 'x')), (0, 0, 'T', (0, 0))),
               (('down', (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0, 0))),
               (('up', (0,), (0, 0, 'u'), (1, 0, 'T')), (0, 0, ' ', (0, 0))),
               (('right', (0,), (0, -1, 'x'), (0, 0, 'T')), (0, 0, 'T', (0, 0))),
               (('up', (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0, 0))),
               (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))),
               (('up', (0,), (0, 0, 'T'), (1, 0, 'x')), (0, 0, 'T', (0, 0))),
               (('up', (0,), (-1, 0, 'T'), (0, 0, 'x')), (0, 0, 'x', (0, 0))),
               (('right', (0,), (0, 0, 'u'), (1, 0, 'T')), (0, 0, ' ', (0, 0))),
               (('right', (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0, 0))),
               (('left', (0,), (0, 0, 'u'), (1, 0, 'T')), (0, 0, ' ', (0, 0))),
               (('up', (0,), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0, 0))),
               (('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0, 0)))}

    actions = ['left', 'right', 'up', 'down']
    focus_set = {'T': 0, 'u': 31, 'x': 76}
    agent = nace.agent_module.Agent((4, 3), 2, 0, (0,))

    world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        world_str_list[0],
        view_dist_x=30,
        view_dist_y=20,
        agent_char_code_list=['x'],
        observed_times_str_list=world_str_list[2]
    )
    world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])

    # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
    new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
    new_rules_a = convert_rules_to_internal_mapping(rules_a, world)


    (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason,
     oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason,
     biggest_predicted_score_delta_actions, biggest_predicted_score_delta, biggest_predicted_score_delta_stopping_reason,
     smallest_predicted_score_delta_actions, smallest_predicted_score_delta, smallest_predicted_score_delta_stopping_reason,
     debbugging_data) = (
        _plan(
            world,
            new_rules_a,
            actions,
            new_focus_set,
            agent))

    # lowest_conf_actions == left, lowest_AIRIS_confidence==0.5, lowest_conf_stopping_reason= 'na 1'

    time_b = 80
    world_str_list_b = [
        ['oooooooooooo',
         'o          o',
         'o          o',
         'o     ooooTo',
         'o xu       o',
         'o          o',
         'oooooooooooo'], (),
        [
            '79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,',
            '79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,',
            '79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,',
            '79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,',
            '79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,',
            '79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,',
            '79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,'
        ],

    ]

    # world_b = NPWorld.from_string_list(world_str_list_b, view_dist_x=30, view_dist_y=20)
    world_b, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        world_str_list_b[0],
        view_dist_x=30,
        view_dist_y=20,
        agent_char_code_list=['x'],
        observed_times_str_list=world_str_list_b[2]
    )
    world_b.multiworld_print([{"World": world_b, "Color": nace.color_codes.color_code_white_on_blue}])

    rules_b = {(('down', (0,), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0, 0))),
               (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))),
               (('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0, 0))),
               (('right', (0,), (0, 0, 'x'), (0, 1, 'T')), (0, 0, 'x', (0, 0))),
               (('up', (0,), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0, 0))),
               (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))),
               (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0, 0))),
               (('left', (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0, 0))),
               (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))),
               (('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0, 0))),
               (('down', (0,), (0, 0, 'u'), (1, 0, 'T')), (0, 0, ' ', (0, 0))),
               (('down', (0,), (-1, 0, 'x'), (0, 0, 'T')), (0, 0, 'T', (0, 0))),
               (('down', (0,), (0, 0, 'x'), (1, 0, 'T')), (0, 0, 'x', (0, 0))),
               (('right', (0,), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0, 0))),
               (('right', (0,), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0, 0))),
               (('down', (0,), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0, 0))),
               (('left', (0,), (0, -1, 'T'), (0, 0, 'x')), (0, 0, 'x', (0, 0))),
               (('left', (0,), (0, 0, 'T'), (0, 1, 'x')), (0, 0, 'T', (0, 0))),
               (('down', (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0, 0))),
               (('up', (0,), (0, 0, 'u'), (1, 0, 'T')), (0, 0, ' ', (0, 0))),
               (('right', (0,), (0, -1, 'x'), (0, 0, 'T')), (0, 0, 'T', (0, 0))),
               (('up', (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0, 0))),
               (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))),
               (('up', (0,), (0, 0, 'T'), (1, 0, 'x')), (0, 0, 'T', (0, 0))),
               (('up', (0,), (-1, 0, 'T'), (0, 0, 'x')), (0, 0, 'x', (0, 0))),
               (('right', (0,), (0, 0, 'u'), (1, 0, 'T')), (0, 0, ' ', (0, 0))),
               (('right', (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0, 0))),
               (('left', (0,), (0, 0, 'u'), (1, 0, 'T')), (0, 0, ' ', (0, 0))),
               (('up', (0,), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0, 0))),
               (('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0, 0)))}

    actions_b = ['right', 'left', 'up', 'down']
    focus_set_b = {'T': 0, 'u': 32, 'x': 77}
    agent_b = nace.agent_module.Agent((2, 4), 2, 0, (0,))

    # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
    new_focus_set_b = convert_focus_set_to_internal_mapping(focus_set_b, world)
    new_rules_b = convert_rules_to_internal_mapping(rules_b, world)

    (lowest_conf_actions_b, lowest_AIRIS_confidence_b, lowest_conf_achieves_goal_b, lowest_conf_stopping_reason_b, oldest_age_actions_b, oldest_age_b, oldest_age_achieves_goal_b, oldest_age_stopping_reason_b,
     biggest_predicted_score_delta_actions_b, biggest_predicted_score_delta_b, biggest_predicted_score_delta_stopping_reason_b,
     smallest_predicted_score_delta_actions_b, smallest_predicted_score_delta_b, smallest_predicted_score_delta_stopping_reason_b,
     debbugging_data) = (
        _plan(
            world_b,
            new_rules_b,
            actions_b,
            new_focus_set_b,
            agent_b))

    dxdy_oldest = get_xy_delta_for_action_list(oldest_age_actions)
    dxdy_oldest_b = get_xy_delta_for_action_list(oldest_age_actions_b)

    dxdy_lowest_conf = get_xy_delta_for_action_list(lowest_conf_actions)
    dxdy_lowest_conf_b = get_xy_delta_for_action_list(lowest_conf_actions_b)

    assert dxdy_oldest == dxdy_oldest_b
    assert dxdy_lowest_conf == dxdy_lowest_conf_b


def t10_fully_known_rules_does_the_agent_always_go_for_score_increasing_target():
    """
    @return:
    """
    world_str_list = [
        ['oooooooooooo',
         'of  o      o',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o      x   o',
         'oooooooooooo'], (),
        ['25,25,25,25,25,25,25,25,25,25,25,25,',
         '25,25,25,25,25,25,25,25,25,25,25,25,',
         '25,25,25,25,25,25,25,25,25,25,25,25,',
         '25,25,25,25,25,25,25,25,25,25,25,25,',
         '25,25,25,25,25,25,25,25,25,25,25,25,',
         '25,25,25,25,25,25,25,25,25,25,13,25,',
         '20,20,20,20,20,20,20,20,20,20,20,20,']]
    rules = {

        (('left', (0,), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,))),   # cup
        (('right', (0,), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
        (('down', (0,), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,))),
        (('down', (0,), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
        (('right', (0,), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,))),
        (('left', (0,), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
        (('up', (0,), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,))),
        (('up', (0,), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),

        (('left', (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))), # space
        (('right', (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,))),
        (('up', (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,))),
        (('up', (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
        (('down', (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
        (('right', (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
        (('left', (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))),
        (('down', (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,))),

        (('left', (0,), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),  # f
        (('left', (0,), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
        (('up', (0,), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
        (('up', (0,), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
        (('down', (0,), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
        (('down', (0,), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
        (('right', (0,), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
        (('right', (0,), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),

        (('right', (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),  # wall o
        (('up', (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,))),
        (('left', (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,))),
        (('down', (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),

    }
    actions = ['left', 'right', 'up', 'down']
    focus_set = {'f': 1, 'u': 1, 'x': 9}
    agent = nace.agent_module.Agent((5, 7), 0, 0, ())

    world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        world_str_list[0],
        view_dist_x=12,
        view_dist_y=5,
        agent_char_code_list=['x'],
        observed_times_str_list=world_str_list[2]
    )
    world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])

    assert world.get_char_at_rc(agent.get_rc_loc()[0],agent.get_rc_loc()[1], agent_indication_embedded_value_list=[]) == 'x'

    # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
    new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
    new_rules = convert_rules_to_internal_mapping(rules, world)

    (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason,
     oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason,
     biggest_predicted_score_delta_actions, biggest_predicted_score_delta, biggest_predicted_score_delta_stopping_reason,
     smallest_predicted_score_delta_actions, smallest_predicted_score_delta,
     smallest_predicted_score_delta_stopping_reason,
     debbugging_data) = (
        _plan(
            world,
            new_rules,
            actions,
            new_focus_set,
            agent))

    rc_lowest_conf = nace.test_utilities.get_rc_delta_for_action_list(lowest_conf_actions)
    rc_oldest = nace.test_utilities.get_rc_delta_for_action_list(oldest_age_actions)

    print("rc_lowest_conf",rc_lowest_conf)
    print("rc_oldest",rc_oldest)
    print("oldest_age",oldest_age)
    print("lowest_AIRIS_confidence",lowest_AIRIS_confidence)
    assert rc_lowest_conf in [(0, 1),(0,-1),(-1,0), (1,0)]  # could this move? apparently yes - could be one step in any direction
    assert rc_oldest == (0, 3)  # go for the oldest cell we can move to. bottom right, age 13.
    assert oldest_age == (25.0 - 13.0)
    assert lowest_AIRIS_confidence == 1.0  # the rules are fully known (except for moving on/off walls?)


def t17_why_frozen_lake_is_inefficient():
    world_str_list = ['AAAAAAAAAA', 'ADaaaaaaaA', 'AaaaaaaaaA', 'AaaabaaaaA', 'AaaaaabaaA', 'AaaabaaaaA', 'AabbaaabaA',
                      'AabaababaA', 'AaaabaaadA', 'AAAAAA....']
    time_str_list = []
    focus_set = {'A': 0, 'E': 279, 'a': 0, 'b': 0, 'C': 228, 'c': 67, 'H': 237, 'B': 182, 'D': 66, 'd': 0}
    rules = [
        (('down', (6,), (-1, 0, 'A'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),  # B
        (('left', (32,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('right', (1,), (0, -1, 'c'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (4,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('left', (6,), (0, -1, 'a'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (4,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (25,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (14,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (17,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (56,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('right', (22,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('down', (13,), (0, -1, 'a'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (4,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (38,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('up', (32,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('up', (38,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('up', (17,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('left', (21,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('up', (40,), (0, -1, 'A'), (0, 0, 'B'), (0, 1, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('left', (13,), (0, -1, 'a'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (3,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('up', (11,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'b')), (0, 0, 'a', (0.0, -8))),
        (('right', (8,), (0, -1, 'A'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (33,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('left', (9,), (-2, 0, 'A'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('down', (11,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'b')), (0, 0, 'a', (0.0, -8))),
        (('down', (40,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (38,), (0, -1, 'a'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (24,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('right', (56,), (0, 0, 'B'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (12,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('down', (11,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('left', (30,), (0, -1, 'b'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (32,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (38,), (0, 0, 'B'), (1, 0, 'b'), (2, 0, 'b')), (0, 0, 'a', (-1.0, 8))),
        (('down', (33,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('right', (56,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('left', (1,), (0, -2, 'A'), (0, -1, 'c'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('down', (21,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('up', (25,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('up', (25,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('up', (2,), (0, -2, 'c'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('right', (30,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (4,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (38,), (0, -1, 'a'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (24,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (25,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (2,), (0, -2, 'c'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('right', (38,), (0, -1, 'a'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (4,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (3,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'b')), (0, 0, 'a', (0.0, 8))),
        (('right', (9,), (0, 0, 'B'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (37,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (11,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'b')), (0, 0, 'a', (0.0, -8))),
        (('left', (32,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (56,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('right', (2,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (24,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (22,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('down', (2,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (37,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (21,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('right', (17,), (0, -1, 'a'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (3,), (0, -1, 'a'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (12,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('left', (30,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (3,), (0, -1, 'a'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (24,), (0, -1, 'A'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (4,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('left', (9,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('down', (10,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('right', (16,), (0, -1, 'A'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (10,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('up', (1,), (-1, 0, 'A'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'C', (0.0, 0))),
        (('down', (22,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('up', (12,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('up', (40,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (33,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('up', (56,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('left', (9,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (9,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (22,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('up', (30,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (40,), (0, -1, 'A'), (0, 0, 'B'), (0, 1, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('left', (4,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('up', (3,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('left', (37,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (6,), (0, -1, 'a'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (30,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (40,), (0, -1, 'A'), (0, 0, 'B'), (0, 1, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('up', (33,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('up', (38,), (0, 0, 'B'), (1, 0, 'b'), (2, 0, 'b')), (0, 0, 'a', (-1.0, 8))),
        (('left', (25,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('down', (25,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (32,), (0, -1, 'A'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (25,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('down', (8,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (2,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (14,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (16,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (56,), (0, 0, 'B'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (14,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (10,), (0, -1, 'a'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('down', (1,), (-1, 0, 'A'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (9,), (0, 0, 'B'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (12,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('up', (10,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('up', (9,), (-2, 0, 'A'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('up', (8,), (-2, 0, 'A'), (-1, 0, 'c'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('up', (30,), (0, -1, 'b'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (10,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('up', (2,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (25,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('down', (3,), (0, -1, 'a'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (11,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('down', (32,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('left', (17,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('right', (37,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (32,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('right', (13,), (0, -1, 'a'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (10,), (0, -1, 'a'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (30,), (0, -1, 'b'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (21,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -8))),
        (('left', (14,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (32,), (0, -1, 'A'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (38,), (0, 0, 'B'), (1, 0, 'b'), (2, 0, 'b')), (0, 0, 'a', (-1.0, 8))),
        (('left', (38,), (0, 0, 'B'), (1, 0, 'b'), (2, 0, 'b')), (0, 0, 'a', (-1.0, 8))),
        (('right', (32,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (2,), (0, -2, 'c'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('left', (11,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('down', (25,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'B')), (0, 0, 'a', (0.0, -1))),
        (('up', (16,), (-1, 0, 'a'), (0, 0, 'B'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (13,), (0, -1, 'a'), (0, 0, 'B'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (3,), (0, 0, 'B'), (1, 0, 'a'), (2, 0, 'b')), (0, 0, 'a', (0.0, 8))),
        (('left', (39,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),  # C
        (('down', (26,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -8))),
        (('down', (14,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('left', (16,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (7,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'A')), (0, 0, 'H', (0.0, 0))),
        (('down', (18,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -8))),
        (('left', (3,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('down', (18,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('left', (17,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (26,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -8))),
        (('right', (14,), (0, 0, 'C'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (24,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (10,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (25,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (9,), (0, 0, 'C'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (8,), (0, 0, 'C'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (22,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (6,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (12,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('right', (4,), (0, 0, 'C'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (6,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (9,), (0, 0, 'C'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (22,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (17,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (5,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('up', (4,), (0, 0, 'C'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (25,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (1,), (0, -1, 'c'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (39,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('right', (26,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -8))),
        (('up', (10,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('up', (16,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (9,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('down', (7,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'A')), (0, 0, 'H', (0.0, 0))),
        (('left', (6,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (40,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'b')), (0, 0, 'B', (0.0, 0))),
        (('left', (8,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'B', (0.0, 0))),
        (('right', (30,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -8))),
        (('up', (25,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -8))),
        (('down', (10,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (5,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('right', (0,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'c', (0.0, 1))),
        (('left', (48,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('left', (24,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (22,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (13,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('up', (6,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (0,), (-1, 0, 'A'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'c', (0.0, 8))),
        (('down', (12,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('up', (9,), (-2, 0, 'A'), (-1, 0, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -8))),
        (('left', (16,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (48,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('left', (26,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -8))),
        (('up', (3,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (4,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('up', (14,), (0, 0, 'C'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (48,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('up', (14,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('down', (14,), (0, 0, 'C'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (25,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('right', (12,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('up', (7,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'A')), (0, 0, 'H', (0.0, 0))),
        (('down', (3,), (0, 0, 'C'), (1, 0, 'a'), (2, 0, 'b')), (0, 0, 'a', (0.0, 8))),
        (('down', (30,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -8))),
        (('down', (13,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('up', (5,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('left', (25,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -8))),
        (('up', (30,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -8))),
        (('right', (5,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('down', (16,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (18,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('up', (8,), (-2, 0, 'A'), (-1, 0, 'c'), (0, 0, 'C')), (0, 0, 'a', (0.0, -8))),
        (('right', (2,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (16,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (14,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('up', (13,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('left', (24,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (18,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -8))),
        (('right', (17,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (3,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (4,), (0, 0, 'C'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (30,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -8))),
        (('left', (22,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (22,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (25,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (24,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (1,), (-1, 0, 'A'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (40,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'b')), (0, 0, 'B', (0.0, 0))),
        (('left', (0,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'D', (0.0, 0))),
        (('left', (2,), (0, -2, 'c'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('left', (18,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('right', (40,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'b')), (0, 0, 'B', (0.0, 0))),
        (('up', (17,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('left', (13,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('up', (24,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (2,), (0, 0, 'C'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (12,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('right', (7,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'A')), (0, 0, 'H', (0.0, 0))),
        (('right', (8,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (17,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('right', (48,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('down', (4,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('left', (1,), (0, -2, 'A'), (0, -1, 'c'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('up', (24,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (4,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('down', (39,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('right', (3,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (9,), (0, 0, 'C'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (16,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (9,), (0, 0, 'C'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (18,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -8))),
        (('down', (4,), (0, 0, 'C'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (2,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (25,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (39,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('left', (40,), (0, -1, 'A'), (0, 0, 'C'), (0, 1, 'b')), (0, 0, 'B', (0.0, 0))),
        (('down', (24,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (10,), (0, -1, 'a'), (0, 0, 'C'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('right', (14,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -1))),
        (('up', (18,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'C')), (0, 0, 'a', (0.0, -8))),
        (('left', (25,), (-1, 0, 'a'), (0, 0, 'C'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (0,), (0, -1, 'A'), (0, 0, 'D'), (0, 1, 'a')), (0, 0, 'c', (0.0, 1))),  # D
        (('up', (0,), (-1, 0, 'A'), (0, 0, 'D'), (1, 0, 'a')), (0, 0, 'C', (0.0, 0))),
        (('down', (0,), (-1, 0, 'A'), (0, 0, 'D'), (1, 0, 'a')), (0, 0, 'c', (0.0, 8))),
        (('down', (26,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'b')), (0, 0, 'a', (0.0, 8))),  # E
        (('left', (48,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (48,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('right', (33,), (0, 0, 'E'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, -8))),
        (('down', (17,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (0,), (0, -1, 'A'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'D', (0.0, 0))),
        (('left', (57,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('right', (39,), (0, 0, 'E'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, -1))),
        (('right', (21,), (0, 0, 'E'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (26,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -1))),
        (('up', (25,), (-2, 0, 'A'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -1))),
        (('right', (40,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (24,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'A')), (0, 0, 'a', (0.0, 1))),
        (('down', (57,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, -1))),
        (('down', (30,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('up', (33,), (-2, 0, 'b'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, 1))),
        (('down', (8,), (-1, 0, 'A'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (40,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (17,), (0, 0, 'E'), (0, 1, 'a'), (0, 2, 'A')), (0, 0, 'a', (0.0, -1))),
        (('left', (34,), (0, -1, 'b'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (-1.0, 1))),
        (('right', (8,), (0, -1, 'A'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (24,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (25,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('down', (45,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('down', (24,), (-1, 0, 'A'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (22,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (9,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (16,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'A')), (0, 0, 'a', (0.0, 1))),
        (('up', (0,), (-1, 0, 'A'), (0, 0, 'E'), (1, 0, 'b')), (0, 0, 'B', (0.0, 0))),
        (('down', (17,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'A')), (0, 0, 'a', (0.0, -1))),
        (('left', (21,), (0, -2, 'a'), (0, -1, 'b'), (0, 0, 'E')), (0, 0, 'a', (-1.0, 8))),
        (('down', (11,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (34,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'b')), (0, 0, 'a', (0.0, -8))),
        (('up', (8,), (-1, 0, 'A'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'B', (0.0, 0))),
        (('down', (8,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (22,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (16,), (-1, 0, 'A'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (56,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (24,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'A')), (0, 0, 'a', (0.0, 1))),
        (('up', (47,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('left', (48,), (0, -1, 'b'), (0, 0, 'E'), (0, 1, 'A')), (0, 0, 'a', (-1.0, 1))),
        (('up', (18,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('left', (47,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, -8))),
        (('right', (21,), (0, 0, 'E'), (0, 1, 'b'), (0, 2, 'a')), (0, 0, 'a', (-1.0, 8))),
        (('right', (32,), (0, -1, 'A'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (32,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (16,), (-1, 0, 'A'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'B', (0.0, 0))),
        (('left', (25,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -1))),
        (('up', (40,), (-1, 0, 'A'), (0, 0, 'E'), (1, 0, 'b')), (0, 0, 'B', (0.0, 0))),
        (('right', (11,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (40,), (-1, 0, 'b'), (0, 0, 'E'), (1, 0, 'A')), (0, 0, 'a', (-1.0, 1))),
        (('up', (30,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'b')), (0, 0, 'a', (0.0, 1))),
        (('down', (26,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, -1))),
        (('down', (8,), (0, 0, 'E'), (1, 0, 'c'), (2, 0, 'A')), (0, 0, 'a', (0.0, -8))),
        (('up', (48,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('left', (16,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'A')), (0, 0, 'a', (0.0, 1))),
        (('right', (38,), (0, 0, 'E'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, -8))),
        (('right', (12,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (48,), (0, 0, 'E'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, -8))),
        (('up', (30,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('down', (0,), (-1, 0, 'b'), (0, 0, 'E'), (1, 0, 'A')), (0, 0, 'B', (0.0, 0))),
        (('up', (18,), (-1, 0, 'b'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (-1.0, 1))),
        (('right', (25,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (8,), (0, 0, 'E'), (0, 1, 'c'), (0, 2, 'A')), (0, 0, 'a', (0.0, -8))),
        (('left', (20,), (0, -2, 'a'), (0, -1, 'b'), (0, 0, 'E')), (0, 0, 'a', (-1.0, -1))),
        (('up', (10,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('up', (39,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -1))),
        (('left', (8,), (0, -2, 'A'), (0, -1, 'c'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('up', (33,), (-2, 0, 'b'), (-1, 0, 'b'), (0, 0, 'E')), (0, 0, 'a', (-1.0, 8))),
        (('right', (30,), (0, 0, 'E'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, -8))),
        (('right', (40,), (0, -1, 'b'), (0, 0, 'E'), (0, 1, 'A')), (0, 0, 'B', (0.0, 0))),
        (('left', (33,), (0, -2, 'b'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, 1))),
        (('up', (11,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -1))),
        (('up', (17,), (-2, 0, 'A'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -1))),
        (('right', (16,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'A')), (0, 0, 'B', (0.0, 0))),
        (('up', (9,), (-2, 0, 'A'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('left', (33,), (0, -2, 'b'), (0, -1, 'b'), (0, 0, 'E')), (0, 0, 'a', (-1.0, 8))),
        (('up', (8,), (-2, 0, 'A'), (-1, 0, 'c'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('up', (0,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('left', (31,), (0, -1, 'A'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'H', (0.0, 0))),
        (('up', (48,), (-1, 0, 'b'), (0, 0, 'E'), (1, 0, 'A')), (0, 0, 'a', (-1.0, 1))),
        (('down', (20,), (0, 0, 'E'), (1, 0, 'b'), (2, 0, 'a')), (0, 0, 'a', (-1.0, -1))),
        (('left', (17,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -1))),
        (('right', (0,), (0, -1, 'b'), (0, 0, 'E'), (0, 1, 'A')), (0, 0, 'B', (0.0, 0))),
        (('right', (48,), (0, -1, 'A'), (0, 0, 'E'), (0, 1, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('right', (40,), (0, -1, 'A'), (0, 0, 'E'), (0, 1, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('down', (34,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('left', (8,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'A')), (0, 0, 'a', (0.0, 1))),
        (('down', (0,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('down', (25,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'A')), (0, 0, 'a', (0.0, -1))),
        (('left', (8,), (0, -1, 'A'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'B', (0.0, 0))),
        (('up', (24,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('left', (0,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, -8))),
        (('down', (48,), (-1, 0, 'A'), (0, 0, 'E'), (1, 0, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('left', (18,), (0, -1, 'b'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (-1.0, 1))),
        (('up', (45,), (-1, 0, 'b'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (-1.0, 1))),
        (('down', (32,), (-1, 0, 'A'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (11,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -1))),
        (('right', (26,), (0, 0, 'E'), (0, 1, 'a'), (0, 2, 'b')), (0, 0, 'a', (0.0, 8))),
        (('left', (40,), (0, -1, 'b'), (0, 0, 'E'), (0, 1, 'A')), (0, 0, 'a', (-1.0, 1))),
        (('left', (32,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'A')), (0, 0, 'a', (0.0, 1))),
        (('down', (31,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'A')), (0, 0, 'H', (0.0, 0))),
        (('right', (9,), (0, 0, 'E'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (33,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'b')), (0, 0, 'a', (0.0, 1))),
        (('left', (26,), (0, -2, 'b'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, 8))),
        (('down', (24,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (31,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'A')), (0, 0, 'H', (0.0, 0))),
        (('down', (24,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'A')), (0, 0, 'B', (0.0, 0))),
        (('left', (24,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (30,), (-1, 0, 'b'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (11,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (14,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (12,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -1))),
        (('right', (0,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, -8))),
        (('left', (30,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('left', (30,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'b')), (0, 0, 'a', (0.0, 1))),
        (('left', (24,), (0, -1, 'A'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'B', (0.0, 0))),
        (('up', (40,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (20,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('down', (16,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (45,), (0, -1, 'b'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (-1.0, 1))),
        (('down', (16,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'A')), (0, 0, 'B', (0.0, 0))),
        (('down', (20,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('down', (25,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('down', (40,), (-1, 0, 'b'), (0, 0, 'E'), (1, 0, 'A')), (0, 0, 'B', (0.0, 0))),
        (('right', (24,), (0, -1, 'A'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (16,), (0, -1, 'A'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (40,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (40,), (-1, 0, 'A'), (0, 0, 'E'), (1, 0, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('down', (0,), (-1, 0, 'A'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'c', (0.0, 8))),
        (('right', (33,), (0, 0, 'E'), (0, 1, 'b'), (0, 2, 'b')), (0, 0, 'a', (-1.0, 8))),
        (('down', (23,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'A')), (0, 0, 'H', (0.0, 0))),
        (('left', (21,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, 1))),
        (('down', (11,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, -1))),
        (('up', (24,), (-1, 0, 'A'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'B', (0.0, 0))),
        (('down', (33,), (0, 0, 'E'), (1, 0, 'b'), (2, 0, 'b')), (0, 0, 'a', (-1.0, 8))),
        (('up', (8,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, 8))),
        (('right', (48,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (25,), (0, 0, 'E'), (0, 1, 'a'), (0, 2, 'A')), (0, 0, 'a', (0.0, -1))),
        (('up', (20,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('right', (23,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'A')), (0, 0, 'H', (0.0, 0))),
        (('down', (24,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('up', (12,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('down', (18,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('up', (21,), (-2, 0, 'a'), (-1, 0, 'b'), (0, 0, 'E')), (0, 0, 'a', (-1.0, 8))),
        (('left', (33,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('down', (48,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('right', (8,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'A')), (0, 0, 'B', (0.0, 0))),
        (('left', (14,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (24,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('left', (33,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -1))),
        (('right', (24,), (0, 0, 'E'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, -8))),
        (('right', (0,), (0, -1, 'A'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'c', (0.0, 1))),
        (('down', (22,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (33,), (0, 0, 'E'), (0, 1, 'a'), (0, 2, 'A')), (0, 0, 'a', (0.0, -1))),
        (('left', (39,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -1))),
        (('left', (12,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -1))),
        (('left', (40,), (0, -1, 'A'), (0, 0, 'E'), (0, 1, 'b')), (0, 0, 'B', (0.0, 0))),
        (('down', (10,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (23,), (0, -1, 'A'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'H', (0.0, 0))),
        (('left', (9,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -1))),
        (('up', (17,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('down', (14,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (18,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (18,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('up', (33,), (-2, 0, 'A'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -1))),
        (('up', (8,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'A')), (0, 0, 'a', (0.0, 1))),
        (('down', (48,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (26,), (0, 0, 'E'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, -1))),
        (('up', (25,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('right', (47,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, -8))),
        (('up', (32,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('left', (8,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, 8))),
        (('right', (56,), (0, 0, 'E'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (34,), (-1, 0, 'b'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (-1.0, 1))),
        (('up', (23,), (-1, 0, 'A'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'H', (0.0, 0))),
        (('left', (0,), (0, -1, 'A'), (0, 0, 'E'), (0, 1, 'b')), (0, 0, 'B', (0.0, 0))),
        (('up', (32,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'A')), (0, 0, 'a', (0.0, 1))),
        (('up', (21,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, 1))),
        (('right', (10,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (18,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (18,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -1))),
        (('down', (33,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('right', (33,), (0, 0, 'E'), (0, 1, 'a'), (0, 2, 'b')), (0, 0, 'a', (0.0, 1))),
        (('up', (38,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('left', (56,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, 1))),
        (('up', (20,), (-2, 0, 'a'), (-1, 0, 'b'), (0, 0, 'E')), (0, 0, 'a', (-1.0, -1))),
        (('right', (30,), (0, -1, 'b'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (21,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (22,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (34,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('down', (8,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'A')), (0, 0, 'B', (0.0, 0))),
        (('up', (26,), (-2, 0, 'b'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, 8))),
        (('down', (21,), (0, 0, 'E'), (1, 0, 'b'), (2, 0, 'a')), (0, 0, 'a', (-1.0, 8))),
        (('down', (13,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (31,), (-1, 0, 'A'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'H', (0.0, 0))),
        (('left', (38,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('down', (47,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('right', (24,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'A')), (0, 0, 'B', (0.0, 0))),
        (('down', (18,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (0,), (-1, 0, 'A'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'C', (0.0, 0))),
        (('right', (57,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('up', (26,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -1))),
        (('left', (16,), (0, -1, 'A'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'B', (0.0, 0))),
        (('left', (10,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('right', (45,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('down', (25,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (56,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, 1))),
        (('up', (57,), (-1, 0, 'a'), (0, 0, 'E'), (1, 0, 'a')), (0, 0, 'a', (0.0, -1))),
        (('down', (33,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'A')), (0, 0, 'a', (0.0, -1))),
        (('up', (33,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'E')), (0, 0, 'a', (0.0, -8))),
        (('right', (17,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (20,), (0, 0, 'E'), (0, 1, 'b'), (0, 2, 'a')), (0, 0, 'a', (-1.0, -1))),
        (('down', (39,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, -1))),
        (('down', (38,), (0, 0, 'E'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('right', (20,), (0, 0, 'E'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, -8))),
        (('right', (14,), (0, -1, 'a'), (0, 0, 'E'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (18,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'b')), (0, 0, 'a', (-1.0, 1))),  # H
        (('right', (13,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (57,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('up', (31,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (18,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('left', (33,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -8))),
        (('right', (34,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'b')), (0, 0, 'a', (-1.0, 8))),
        (('up', (57,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('down', (7,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('left', (23,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (5,), (-1, 0, 'A'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (4,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('right', (18,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('left', (33,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('left', (25,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('right', (34,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'b')), (0, 0, 'a', (0.0, -1))),
        (('up', (6,), (-1, 0, 'A'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'C', (0.0, 0))),
        (('right', (25,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -8))),
        (('down', (2,), (0, 0, 'H'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (3,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('down', (6,), (-1, 0, 'A'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'C', (0.0, 0))),
        (('down', (10,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (4,), (0, 0, 'H'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (13,), (-2, 0, 'A'), (-1, 0, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -8))),
        (('left', (13,), (-2, 0, 'A'), (-1, 0, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -8))),
        (('left', (31,), (0, -2, 'b'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('left', (2,), (0, -2, 'c'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('up', (33,), (0, 0, 'H'), (1, 0, 'b'), (2, 0, 'b')), (0, 0, 'a', (-1.0, 8))),
        (('up', (31,), (0, -2, 'b'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('down', (34,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'b')), (0, 0, 'a', (-1.0, 8))),
        (('up', (34,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'b')), (0, 0, 'a', (-1.0, 8))),
        (('right', (5,), (-1, 0, 'A'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (5,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('right', (26,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('down', (7,), (-1, 0, 'A'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'C', (0.0, 0))),
        (('up', (4,), (0, 0, 'H'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (26,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -8))),
        (('right', (23,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('down', (26,), (0, 0, 'H'), (1, 0, 'a'), (2, 0, 'b')), (0, 0, 'a', (0.0, 8))),
        (('down', (15,), (0, 0, 'H'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (11,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'b')), (0, 0, 'a', (-1.0, 8))),
        (('left', (15,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('right', (4,), (0, 0, 'H'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (26,), (0, 0, 'H'), (1, 0, 'a'), (2, 0, 'b')), (0, 0, 'a', (0.0, 8))),
        (('left', (14,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (2,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (3,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (11,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (2,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (25,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -8))),
        (('up', (14,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (18,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'b')), (0, 0, 'a', (-1.0, 1))),
        (('up', (23,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (5,), (-1, 0, 'A'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (57,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('left', (26,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('up', (10,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('up', (9,), (-2, 0, 'A'), (-1, 0, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -8))),
        (('down', (31,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (26,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -8))),
        (('up', (1,), (-1, 0, 'A'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'C', (0.0, 0))),
        (('up', (12,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('down', (11,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'b')), (0, 0, 'a', (-1.0, 8))),
        (('right', (10,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (22,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('left', (3,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (3,), (-1, 0, 'A'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'C', (0.0, 0))),
        (('up', (9,), (0, 0, 'H'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (33,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -8))),
        (('right', (18,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -8))),
        (('left', (9,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('down', (18,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (15,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('left', (22,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('right', (57,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('left', (25,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -8))),
        (('up', (18,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -8))),
        (('up', (22,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('down', (25,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (17,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (39,), (0, 0, 'H'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (12,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('left', (7,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('down', (3,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (11,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'b')), (0, 0, 'a', (-1.0, 8))),
        (('left', (34,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'b')), (0, 0, 'a', (0.0, -1))),
        (('right', (4,), (0, 0, 'H'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, 1))),
        (('left', (33,), (0, 0, 'H'), (1, 0, 'b'), (2, 0, 'b')), (0, 0, 'a', (-1.0, 8))),
        (('right', (6,), (-1, 0, 'A'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'C', (0.0, 0))),
        (('left', (12,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('down', (3,), (-1, 0, 'A'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'C', (0.0, 0))),
        (('down', (18,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -8))),
        (('up', (34,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'b')), (0, 0, 'a', (0.0, -1))),
        (('down', (1,), (-1, 0, 'A'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (11,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'b')), (0, 0, 'a', (-1.0, 8))),
        (('down', (14,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('right', (33,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -8))),
        (('right', (23,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (3,), (0, 0, 'H'), (1, 0, 'a'), (2, 0, 'b')), (0, 0, 'a', (0.0, 8))),
        (('left', (13,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (1,), (0, -2, 'A'), (0, -1, 'c'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('up', (26,), (-2, 0, 'a'), (-1, 0, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -8))),
        (('left', (4,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('up', (17,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, -8))),
        (('right', (14,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (23,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (39,), (0, 0, 'H'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (9,), (0, 0, 'H'), (0, 1, 'a'), (0, 2, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (13,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (39,), (0, 0, 'H'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (9,), (0, 0, 'H'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (1,), (0, -1, 'c'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('up', (15,), (0, 0, 'H'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('up', (39,), (0, 0, 'H'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('down', (17,), (-1, 0, 'a'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('left', (3,), (-1, 0, 'A'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'C', (0.0, 0))),
        (('down', (15,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('up', (7,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('right', (12,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('right', (33,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('left', (11,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('up', (13,), (-2, 0, 'A'), (-1, 0, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -8))),
        (('down', (12,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('up', (23,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('down', (9,), (0, 0, 'H'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (15,), (0, 0, 'H'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (15,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('up', (4,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('down', (33,), (0, 0, 'H'), (1, 0, 'b'), (2, 0, 'b')), (0, 0, 'a', (-1.0, 8))),
        (('up', (4,), (0, 0, 'H'), (1, 0, 'a'), (2, 0, 'a')), (0, 0, 'a', (0.0, 8))),
        (('right', (13,), (-2, 0, 'A'), (-1, 0, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -8))),
        (('right', (25,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, 1))),
        (('down', (22,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('up', (7,), (-1, 0, 'A'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'C', (0.0, 0))),
        (('left', (10,), (0, -1, 'a'), (0, 0, 'H'), (0, 1, 'a')), (0, 0, 'a', (0.0, -1))),
        (('left', (17,), (0, -2, 'A'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('right', (33,), (0, 0, 'H'), (1, 0, 'b'), (2, 0, 'b')), (0, 0, 'a', (-1.0, 8))),
        (('left', (6,), (-1, 0, 'A'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'C', (0.0, 0))),
        (('left', (3,), (0, 0, 'H'), (1, 0, 'a'), (2, 0, 'b')), (0, 0, 'a', (0.0, 8))),
        (('up', (2,), (-1, 0, 'A'), (0, 0, 'H'), (1, 0, 'a')), (0, 0, 'C', (0.0, 0))),
        (('left', (23,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('down', (18,), (0, -2, 'a'), (0, -1, 'a'), (0, 0, 'H')), (0, 0, 'a', (0.0, -1))),
        (('right', (31,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),  # a
        (('left', (33,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'C', (0.0, -8))),
        (('right', (9,), (0, -1, 'E'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (12,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (6,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (3,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (14,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (37,), (0, -1, 'B'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (13,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('down', (12,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('up', (3,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (30,), (0, 0, 'a'), (0, 1, 'B'), (0, 2, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (32,), (0, 0, 'a'), (0, 1, 'E'), (0, 2, 'A')), (0, 0, 'H', (0.0, 1))),
        (('right', (16,), (0, -2, 'A'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (5,), (-2, 0, 'A'), (-1, 0, 'H'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (56,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (24,), (0, -1, 'E'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'C', (0.0, -8))),
        (('left', (12,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('left', (10,), (0, 0, 'a'), (0, 1, 'C'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('left', (6,), (0, 0, 'a'), (0, 1, 'B'), (0, 2, 'A')), (0, 0, 'E', (0.0, 8))),
        (('up', (12,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('up', (15,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('up', (2,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'E', (0.0, 8))),
        (('left', (12,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('left', (25,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('left', (16,), (0, 0, 'a'), (0, 1, 'B'), (0, 2, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (24,), (-2, 0, 'a'), (-1, 0, 'C'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (57,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('left', (25,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (30,), (0, -2, 'b'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (33,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('left', (26,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'C', (0.0, -8))),
        (('right', (32,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('up', (3,), (-1, 0, 'b'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'E', (0.0, 8))),
        (('down', (2,), (-1, 0, 'B'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (14,), (0, 0, 'a'), (1, 0, 'E'), (2, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (31,), (-2, 0, 'a'), (-1, 0, 'H'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (21,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('right', (2,), (0, -1, 'c'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('left', (11,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('down', (25,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('right', (5,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('right', (33,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('down', (2,), (-1, 0, 'H'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (3,), (0, -1, 'b'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'E', (0.0, 8))),
        (('down', (3,), (-1, 0, 'C'), (0, 0, 'a'), (1, 0, 'b')), (0, 0, 'E', (0.0, 8))),
        (('up', (14,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'E', (0.0, 8))),
        (('right', (25,), (0, -1, 'E'), (0, 0, 'a'), (0, 1, 'A')), (0, 0, 'B', (0.0, -1))),
        (('down', (20,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('down', (8,), (-1, 0, 'C'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (12,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'B', (0.0, -1))),
        (('up', (3,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('up', (26,), (-1, 0, 'b'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'E', (0.0, 8))),
        (('down', (24,), (-2, 0, 'A'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (5,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('up', (18,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'C', (0.0, -8))),
        (('left', (5,), (0, 0, 'a'), (0, 1, 'C'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('up', (23,), (0, 0, 'a'), (1, 0, 'H'), (2, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (56,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'H', (0.0, 1))),
        (('left', (7,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('left', (8,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'E', (0.0, 8))),
        (('right', (32,), (0, -2, 'A'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (25,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (7,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('right', (40,), (0, -2, 'a'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (25,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('up', (6,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'A')), (0, 0, 'E', (0.0, 8))),
        (('down', (26,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'C', (0.0, -8))),
        (('up', (30,), (0, 0, 'a'), (1, 0, 'E'), (2, 0, 'b')), (0, 0, 'H', (0.0, 1))),
        (('up', (17,), (-1, 0, 'A'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'B', (0.0, -1))),
        (('down', (22,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('down', (12,), (0, 0, 'a'), (1, 0, 'C'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('right', (3,), (0, -1, 'B'), (0, 0, 'a'), (0, 1, 'b')), (0, 0, 'E', (0.0, 8))),
        (('right', (11,), (0, -2, 'a'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (39,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('down', (0,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (2,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'E', (0.0, 8))),
        (('up', (9,), (-1, 0, 'A'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'C', (0.0, -8))),
        (('left', (17,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('down', (48,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (25,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (13,), (-2, 0, 'a'), (-1, 0, 'H'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (16,), (-2, 0, 'a'), (-1, 0, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (2,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (16,), (0, 0, 'a'), (0, 1, 'C'), (0, 2, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (1,), (0, -2, 'c'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (5,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('up', (25,), (-1, 0, 'A'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'B', (0.0, -1))),
        (('up', (33,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'C', (0.0, -8))),
        (('right', (30,), (0, -2, 'b'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (23,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('right', (6,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (26,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'C', (0.0, -8))),
        (('right', (0,), (0, -2, 'A'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (48,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'C', (0.0, -8))),
        (('down', (21,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (17,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('left', (0,), (0, 0, 'a'), (0, 1, 'D'), (0, 2, 'A')), (0, 0, 'E', (0.0, 8))),
        (('left', (24,), (0, 0, 'a'), (0, 1, 'E'), (0, 2, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (17,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (5,), (0, -2, 'A'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (38,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (47,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('down', (3,), (-1, 0, 'B'), (0, 0, 'a'), (1, 0, 'b')), (0, 0, 'E', (0.0, 8))),
        (('up', (14,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (3,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (21,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('left', (48,), (0, 0, 'a'), (0, 1, 'E'), (0, 2, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (12,), (0, 0, 'a'), (1, 0, 'H'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('left', (12,), (0, 0, 'a'), (1, 0, 'C'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('down', (30,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('right', (12,), (0, -2, 'a'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (23,), (-2, 0, 'a'), (-1, 0, 'H'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (16,), (0, -2, 'A'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (16,), (0, 0, 'a'), (1, 0, 'E'), (2, 0, 'A')), (0, 0, 'H', (0.0, 1))),
        (('left', (15,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('down', (14,), (-1, 0, 'B'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (23,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('left', (14,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('right', (24,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (26,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('right', (16,), (0, -2, 'A'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (48,), (0, -2, 'a'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (56,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('up', (6,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (24,), (0, 0, 'a'), (1, 0, 'E'), (2, 0, 'A')), (0, 0, 'H', (0.0, 1))),
        (('up', (13,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (10,), (-2, 0, 'a'), (-1, 0, 'C'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (23,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('right', (6,), (0, -2, 'A'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (10,), (0, 0, 'a'), (0, 1, 'B'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('up', (22,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('down', (24,), (-2, 0, 'a'), (-1, 0, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (2,), (0, -1, 'c'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('right', (15,), (0, -1, 'H'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (30,), (0, -2, 'b'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (26,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'b')), (0, 0, 'E', (0.0, 8))),
        (('right', (22,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('left', (25,), (0, 0, 'a'), (0, 1, 'C'), (0, 2, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (15,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('left', (33,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'C', (0.0, -8))),
        (('up', (0,), (0, 0, 'a'), (1, 0, 'E'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('down', (11,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (24,), (0, 0, 'a'), (1, 0, 'C'), (2, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (25,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'A')), (0, 0, 'B', (0.0, -1))),
        (('right', (39,), (0, -1, 'E'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'B', (0.0, -1))),
        (('right', (3,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (33,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'A')), (0, 0, 'B', (0.0, -1))),
        (('up', (30,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'C', (0.0, -8))),
        (('right', (25,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (10,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('down', (32,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (2,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (4,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('left', (3,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (1,), (0, 0, 'a'), (0, 1, 'B'), (0, 2, 'A')), (0, 0, 'E', (0.0, 8))),
        (('down', (5,), (0, 0, 'a'), (0, 1, 'C'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('left', (17,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('up', (4,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('up', (34,), (0, 0, 'a'), (1, 0, 'E'), (2, 0, 'b')), (0, 0, 'C', (0.0, -8))),
        (('down', (14,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('left', (32,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'E', (0.0, 8))),
        (('down', (30,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'C', (0.0, -8))),
        (('left', (8,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'E', (0.0, 8))),
        (('right', (33,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'C', (0.0, -8))),
        (('up', (39,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'B', (0.0, -1))),
        (('left', (18,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'C', (0.0, -8))),
        (('up', (10,), (0, 0, 'a'), (1, 0, 'E'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('up', (1,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'A')), (0, 0, 'E', (0.0, 8))),
        (('right', (14,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (4,), (-1, 0, 'H'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (47,), (0, 0, 'a'), (0, 1, 'E'), (0, 2, 'a')), (0, 0, 'C', (0.0, -8))),
        (('up', (57,), (0, 0, 'a'), (1, 0, 'E'), (2, 0, 'a')), (0, 0, 'B', (0.0, -1))),
        (('right', (10,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (40,), (0, 0, 'a'), (0, 1, 'B'), (0, 2, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (25,), (-2, 0, 'a'), (-1, 0, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (9,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'E', (0.0, 8))),
        (('left', (13,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (20,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'C', (0.0, -8))),
        (('up', (33,), (-1, 0, 'A'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'B', (0.0, -1))),
        (('left', (0,), (0, 0, 'a'), (0, 1, 'C'), (0, 2, 'A')), (0, 0, 'E', (0.0, 8))),
        (('left', (14,), (0, 0, 'a'), (0, 1, 'E'), (0, 2, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (22,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('up', (30,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'C', (0.0, -8))),
        (('right', (5,), (0, 0, 'a'), (0, 1, 'C'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('right', (10,), (0, -2, 'a'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (15,), (-1, 0, 'H'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (5,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (25,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'C', (0.0, -8))),
        (('right', (30,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (26,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'B', (0.0, -1))),
        (('down', (16,), (-2, 0, 'a'), (-1, 0, 'C'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (34,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'b')), (0, 0, 'B', (0.0, -1))),
        (('left', (38,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('up', (32,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('left', (37,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'E', (0.0, 8))),
        (('down', (17,), (-2, 0, 'a'), (-1, 0, 'H'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (16,), (-2, 0, 'A'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (2,), (0, -1, 'B'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (14,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (9,), (0, -1, 'H'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (8,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'E', (0.0, 8))),
        (('right', (11,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (25,), (0, 0, 'a'), (1, 0, 'C'), (2, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (0,), (0, 0, 'a'), (1, 0, 'D'), (2, 0, 'A')), (0, 0, 'E', (0.0, 8))),
        (('up', (26,), (-1, 0, 'b'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'E', (0.0, 8))),
        (('up', (17,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('right', (23,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (10,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (24,), (0, -2, 'A'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (17,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'B', (0.0, -1))),
        (('left', (30,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'C', (0.0, -8))),
        (('down', (33,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('up', (12,), (0, 0, 'a'), (1, 0, 'C'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('left', (57,), (0, 0, 'a'), (0, 1, 'E'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('down', (12,), (-2, 0, 'a'), (-1, 0, 'H'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (12,), (0, 0, 'a'), (1, 0, 'H'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('up', (38,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (25,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (32,), (0, 0, 'a'), (1, 0, 'E'), (2, 0, 'A')), (0, 0, 'H', (0.0, 1))),
        (('right', (39,), (0, -1, 'H'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (0,), (-2, 0, 'A'), (-1, 0, 'D'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (40,), (0, 0, 'a'), (1, 0, 'E'), (2, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (4,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'E', (0.0, 8))),
        (('down', (26,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'B', (0.0, -1))),
        (('right', (26,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'C', (0.0, -8))),
        (('right', (56,), (0, -1, 'E'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (30,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (10,), (0, 0, 'a'), (0, 1, 'B'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('left', (24,), (0, -2, 'A'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (9,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (12,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('up', (8,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'E', (0.0, 8))),
        (('right', (11,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'b')), (0, 0, 'C', (0.0, -8))),
        (('down', (26,), (-1, 0, 'H'), (0, 0, 'a'), (1, 0, 'b')), (0, 0, 'E', (0.0, 8))),
        (('right', (24,), (0, -2, 'A'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (11,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('up', (47,), (0, 0, 'a'), (1, 0, 'E'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('down', (30,), (-2, 0, 'b'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (8,), (0, -2, 'A'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (33,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('up', (0,), (0, 0, 'a'), (1, 0, 'C'), (2, 0, 'A')), (0, 0, 'E', (0.0, 8))),
        (('left', (0,), (0, 0, 'a'), (0, 1, 'E'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('up', (57,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('right', (14,), (0, -1, 'B'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (32,), (0, -2, 'A'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (1,), (0, -2, 'A'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (17,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (14,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (8,), (0, -2, 'A'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (33,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('down', (12,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('up', (22,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (9,), (-1, 0, 'B'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (1,), (0, -2, 'c'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (4,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('right', (1,), (0, -2, 'A'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (24,), (0, -2, 'A'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (14,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('up', (33,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('up', (24,), (0, -2, 'A'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (4,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('right', (33,), (0, -1, 'E'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'C', (0.0, -8))),
        (('right', (9,), (0, -1, 'B'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (11,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'b')), (0, 0, 'C', (0.0, -8))),
        (('right', (26,), (0, -1, 'H'), (0, 0, 'a'), (0, 1, 'b')), (0, 0, 'E', (0.0, 8))),
        (('right', (57,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('right', (3,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (38,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'C', (0.0, -8))),
        (('down', (22,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (13,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('left', (1,), (0, 0, 'a'), (0, 1, 'C'), (0, 2, 'A')), (0, 0, 'E', (0.0, 8))),
        (('left', (22,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('down', (21,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('right', (1,), (0, -2, 'A'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (11,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'B', (0.0, -1))),
        (('down', (18,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('up', (13,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('right', (25,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('down', (14,), (-1, 0, 'C'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (38,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('up', (32,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'C', (0.0, -8))),
        (('left', (22,), (0, 0, 'a'), (0, 1, 'E'), (0, 2, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (48,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('right', (39,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('right', (10,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('down', (1,), (-2, 0, 'A'), (-1, 0, 'C'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (11,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('right', (32,), (0, -1, 'B'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (18,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (1,), (0, 0, 'a'), (1, 0, 'C'), (2, 0, 'A')), (0, 0, 'E', (0.0, 8))),
        (('down', (24,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (12,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'B', (0.0, -1))),
        (('left', (6,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (33,), (0, -1, 'b'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'H', (0.0, 1))),
        (('down', (1,), (-2, 0, 'A'), (-1, 0, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (12,), (0, 0, 'a'), (1, 0, 'H'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('right', (22,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (3,), (-1, 0, 'H'), (0, 0, 'a'), (1, 0, 'b')), (0, 0, 'E', (0.0, 8))),
        (('up', (16,), (0, -2, 'A'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (39,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'E', (0.0, 8))),
        (('left', (9,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'B', (0.0, -1))),
        (('down', (4,), (-1, 0, 'B'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (13,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (30,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'C', (0.0, -8))),
        (('left', (30,), (0, 0, 'a'), (0, 1, 'E'), (0, 2, 'b')), (0, 0, 'H', (0.0, 1))),
        (('right', (56,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('left', (6,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (18,), (-2, 0, 'a'), (-1, 0, 'H'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (40,), (-2, 0, 'a'), (-1, 0, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (18,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'C', (0.0, -8))),
        (('up', (33,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'C', (0.0, -8))),
        (('up', (38,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('up', (33,), (-1, 0, 'b'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'H', (0.0, 1))),
        (('left', (22,), (0, 0, 'a'), (0, 1, 'C'), (0, 2, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (4,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'E', (0.0, 8))),
        (('down', (15,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('up', (38,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'C', (0.0, -8))),
        (('left', (39,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('left', (3,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('down', (8,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (9,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'E', (0.0, 8))),
        (('right', (22,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('up', (9,), (-1, 0, 'A'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'C', (0.0, -8))),
        (('left', (8,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'E', (0.0, 8))),
        (('down', (40,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (3,), (0, -1, 'C'), (0, 0, 'a'), (0, 1, 'b')), (0, 0, 'E', (0.0, 8))),
        (('down', (30,), (-2, 0, 'a'), (-1, 0, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (17,), (0, 0, 'a'), (1, 0, 'E'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('right', (12,), (0, 0, 'a'), (1, 0, 'C'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('left', (4,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('down', (13,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (4,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('right', (17,), (0, -1, 'E'), (0, 0, 'a'), (0, 1, 'A')), (0, 0, 'B', (0.0, -1))),
        (('left', (22,), (0, 0, 'a'), (1, 0, 'C'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('down', (57,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'B', (0.0, -1))),
        (('right', (4,), (0, -1, 'B'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (11,), (0, 0, 'a'), (1, 0, 'E'), (2, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (25,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'B', (0.0, -1))),
        (('right', (18,), (0, -2, 'a'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (18,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'C', (0.0, -8))),
        (('down', (25,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (2,), (-1, 0, 'C'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (16,), (0, 0, 'a'), (1, 0, 'E'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('up', (56,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('up', (34,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'b')), (0, 0, 'B', (0.0, -1))),
        (('left', (34,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'b')), (0, 0, 'B', (0.0, -1))),
        (('down', (17,), (-2, 0, 'a'), (-1, 0, 'C'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (11,), (0, 0, 'a'), (1, 0, 'H'), (2, 0, 'b')), (0, 0, 'C', (0.0, -8))),
        (('up', (4,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('up', (5,), (0, 0, 'a'), (1, 0, 'H'), (2, 0, 'A')), (0, 0, 'E', (0.0, 8))),
        (('right', (38,), (0, -1, 'E'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'C', (0.0, -8))),
        (('up', (31,), (0, -1, 'b'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('up', (40,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (24,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'C', (0.0, -8))),
        (('left', (9,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'E', (0.0, 8))),
        (('right', (13,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (33,), (0, -1, 'E'), (0, 0, 'a'), (0, 1, 'b')), (0, 0, 'H', (0.0, 1))),
        (('right', (10,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (10,), (0, 0, 'a'), (0, 1, 'E'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('left', (25,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'C', (0.0, -8))),
        (('down', (4,), (-1, 0, 'C'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (13,), (-1, 0, 'A'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'C', (0.0, -8))),
        (('up', (22,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('up', (5,), (0, 0, 'a'), (0, 1, 'C'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('right', (17,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (3,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (33,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'B', (0.0, -1))),
        (('right', (9,), (0, -1, 'C'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (8,), (0, 0, 'a'), (1, 0, 'E'), (2, 0, 'A')), (0, 0, 'H', (0.0, 1))),
        (('up', (3,), (-1, 0, 'b'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'E', (0.0, 8))),
        (('right', (17,), (0, -2, 'a'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (14,), (0, -2, 'a'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (23,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (16,), (0, -2, 'A'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (18,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (21,), (0, -1, 'E'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (9,), (-1, 0, 'H'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (14,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'E', (0.0, 8))),
        (('right', (24,), (0, -2, 'a'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (15,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'E', (0.0, 8))),
        (('up', (4,), (0, -1, 'H'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (22,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('up', (9,), (-1, 0, 'A'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('left', (25,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'C', (0.0, -8))),
        (('up', (14,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('right', (0,), (0, -2, 'A'), (0, -1, 'D'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (13,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (2,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'E', (0.0, 8))),
        (('down', (8,), (-2, 0, 'A'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (17,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (2,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'E', (0.0, 8))),
        (('up', (18,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'C', (0.0, -8))),
        (('down', (10,), (-2, 0, 'a'), (-1, 0, 'H'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (26,), (0, -1, 'E'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'B', (0.0, -1))),
        (('down', (6,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (25,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'C', (0.0, -8))),
        (('right', (22,), (0, -2, 'a'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (11,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'b')), (0, 0, 'C', (0.0, -8))),
        (('left', (40,), (0, 0, 'a'), (0, 1, 'E'), (0, 2, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (9,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'E', (0.0, 8))),
        (('down', (17,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'A')), (0, 0, 'B', (0.0, -1))),
        (('right', (11,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('left', (9,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('up', (10,), (0, 0, 'a'), (1, 0, 'H'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('up', (25,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('down', (6,), (-2, 0, 'A'), (-1, 0, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (2,), (0, -1, 'c'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('up', (24,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'C', (0.0, -8))),
        (('right', (30,), (0, -1, 'E'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'C', (0.0, -8))),
        (('down', (32,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('up', (37,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'E', (0.0, 8))),
        (('down', (57,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('right', (33,), (0, -1, 'E'), (0, 0, 'a'), (0, 1, 'A')), (0, 0, 'B', (0.0, -1))),
        (('up', (4,), (0, -1, 'C'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (18,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'B', (0.0, -1))),
        (('left', (10,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('down', (18,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'C', (0.0, -8))),
        (('left', (32,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('up', (11,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'B', (0.0, -1))),
        (('down', (33,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'b')), (0, 0, 'H', (0.0, 1))),
        (('down', (25,), (-2, 0, 'a'), (-1, 0, 'H'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (8,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'E', (0.0, 8))),
        (('down', (33,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('left', (10,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'a')), (0, 0, 'B', (0.0, -1))),
        (('up', (24,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('right', (56,), (0, -1, 'B'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (2,), (0, -1, 'c'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('up', (10,), (0, 0, 'a'), (1, 0, 'C'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('left', (26,), (0, -1, 'b'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'E', (0.0, 8))),
        (('down', (8,), (-1, 0, 'B'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (21,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'H', (0.0, 1))),
        (('up', (39,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'E', (0.0, 8))),
        (('right', (20,), (0, -1, 'E'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'C', (0.0, -8))),
        (('up', (22,), (0, 0, 'a'), (1, 0, 'E'), (2, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (56,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'H', (0.0, 1))),
        (('right', (16,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (18,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'C', (0.0, -8))),
        (('down', (22,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (2,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'E', (0.0, 8))),
        (('up', (17,), (0, 0, 'a'), (1, 0, 'C'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('right', (12,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('right', (13,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('down', (39,), (-1, 0, 'H'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (16,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('down', (26,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'C', (0.0, -8))),
        (('left', (9,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('up', (25,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('left', (26,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'B', (0.0, -1))),
        (('down', (9,), (-1, 0, 'C'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (47,), (0, -2, 'a'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('right', (18,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('down', (1,), (-2, 0, 'A'), (-1, 0, 'H'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (26,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'C', (0.0, -8))),
        (('right', (17,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('left', (31,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (32,), (-1, 0, 'B'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (13,), (-1, 0, 'A'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'C', (0.0, -8))),
        (('down', (17,), (-2, 0, 'a'), (-1, 0, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (18,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('down', (10,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (57,), (0, -2, 'a'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'B', (0.0, -1))),
        (('left', (25,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('up', (12,), (0, 0, 'a'), (1, 0, 'H'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('left', (2,), (0, -1, 'c'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('left', (20,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'C', (0.0, -8))),
        (('down', (10,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (13,), (-1, 0, 'A'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'C', (0.0, -8))),
        (('left', (31,), (0, -1, 'b'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('left', (32,), (0, -2, 'A'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (5,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'A')), (0, 0, 'E', (0.0, 8))),
        (('down', (37,), (-1, 0, 'B'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (26,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'C', (0.0, -8))),
        (('left', (24,), (0, 0, 'a'), (0, 1, 'E'), (0, 2, 'A')), (0, 0, 'H', (0.0, 1))),
        (('up', (9,), (-1, 0, 'A'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'C', (0.0, -8))),
        (('left', (3,), (0, -1, 'b'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'E', (0.0, 8))),
        (('up', (30,), (0, -2, 'b'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (7,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('down', (56,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('left', (8,), (0, 0, 'a'), (0, 1, 'E'), (0, 2, 'A')), (0, 0, 'H', (0.0, 1))),
        (('right', (8,), (0, -2, 'A'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (26,), (0, -1, 'E'), (0, 0, 'a'), (0, 1, 'b')), (0, 0, 'E', (0.0, 8))),
        (('down', (22,), (-2, 0, 'a'), (-1, 0, 'C'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (18,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (39,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('right', (13,), (-1, 0, 'A'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'C', (0.0, -8))),
        (('right', (24,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (18,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'C', (0.0, -8))),
        (('down', (0,), (-2, 0, 'A'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (25,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'C', (0.0, -8))),
        (('left', (3,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('right', (14,), (0, -1, 'C'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (4,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'B', (0.0, -1))),
        (('up', (5,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (9,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'E', (0.0, 8))),
        (('left', (24,), (0, 0, 'a'), (0, 1, 'C'), (0, 2, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (14,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'E', (0.0, 8))),
        (('up', (12,), (0, 0, 'a'), (1, 0, 'E'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('up', (48,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'C', (0.0, -8))),
        (('up', (3,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('left', (16,), (0, 0, 'a'), (0, 1, 'E'), (0, 2, 'A')), (0, 0, 'H', (0.0, 1))),
        (('left', (3,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'C')), (0, 0, 'B', (0.0, -1))),
        (('right', (3,), (0, -1, 'H'), (0, 0, 'a'), (0, 1, 'b')), (0, 0, 'E', (0.0, 8))),
        (('right', (25,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('left', (9,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('right', (30,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'C', (0.0, -8))),
        (('right', (21,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('down', (16,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (25,), (0, -2, 'a'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (0,), (0, -2, 'A'), (0, -1, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (0,), (-2, 0, 'A'), (-1, 0, 'C'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (26,), (0, -1, 'b'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'E', (0.0, 8))),
        (('left', (9,), (-1, 0, 'A'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('down', (32,), (-2, 0, 'A'), (-1, 0, 'E'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (4,), (0, -1, 'C'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'H', (0.0, 1))),
        (('right', (3,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (1,), (0, 0, 'a'), (1, 0, 'H'), (2, 0, 'A')), (0, 0, 'E', (0.0, 8))),
        (('right', (16,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (25,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'C')), (0, 0, 'C', (0.0, -8))),
        (('left', (38,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (4,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'E', (0.0, 8))),
        (('down', (24,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('up', (31,), (0, 0, 'a'), (1, 0, 'H'), (2, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('down', (13,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (10,), (0, 0, 'a'), (1, 0, 'B'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('right', (40,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (17,), (0, -2, 'a'), (0, -1, 'B'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('up', (3,), (-1, 0, 'b'), (0, 0, 'a'), (1, 0, 'B')), (0, 0, 'E', (0.0, 8))),
        (('down', (39,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'B', (0.0, -1))),
        (('right', (26,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('left', (24,), (0, 0, 'a'), (0, 1, 'B'), (0, 2, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (39,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'E')), (0, 0, 'B', (0.0, -1))),
        (('right', (48,), (0, -1, 'E'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'C', (0.0, -8))),
        (('left', (18,), (0, 0, 'a'), (0, 1, 'E'), (0, 2, 'a')), (0, 0, 'E', (0.0, 8))),
        (('left', (22,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (17,), (0, 0, 'a'), (1, 0, 'H'), (2, 0, 'a')), (0, 0, 'C', (0.0, -8))),
        (('left', (25,), (0, -1, 'A'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'B', (0.0, -1))),
        (('left', (3,), (0, -1, 'b'), (0, 0, 'a'), (0, 1, 'H')), (0, 0, 'E', (0.0, 8))),
        (('up', (9,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'H')), (0, 0, 'E', (0.0, 8))),
        (('left', (2,), (0, -1, 'a'), (0, 0, 'a'), (0, 1, 'B')), (0, 0, 'E', (0.0, 8))),
        (('down', (56,), (0, -1, 'B'), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'H', (0.0, 1))),
        (('down', (11,), (-1, 0, 'E'), (0, 0, 'a'), (1, 0, 'a')), (0, 0, 'B', (0.0, -1))),
        (('left', (1,), (0, 0, 'a'), (0, 1, 'H'), (0, 2, 'A')), (0, 0, 'E', (0.0, 8))),
        (('down', (25,), (-2, 0, 'a'), (-1, 0, 'C'), (0, 0, 'a')), (0, 0, 'E', (0.0, 8))),
        (('right', (1,), (0, -2, 'c'), (0, -1, 'C'), (0, 0, 'a')), (0, 0, 'H', (0.0, 1))),
        (('up', (21,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'H', (0.0, 1))),
        (('up', (25,), (-1, 0, 'a'), (0, 0, 'a'), (1, 0, 'E')), (0, 0, 'C', (0.0, -8))),
        (('down', (45,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),  # b
        (('up', (40,), (0, 0, 'b'), (1, 0, 'E'), (2, 0, 'A')), (0, 0, 'F', (-1.0, 1))),
        (('up', (33,), (-1, 0, 'H'), (0, 0, 'b'), (1, 0, 'b')), (0, 0, 'F', (-1.0, 8))),
        (('right', (40,), (0, -2, 'A'), (0, -1, 'B'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('left', (21,), (0, -1, 'a'), (0, 0, 'b'), (0, 1, 'E')), (0, 0, 'F', (-1.0, 8))),
        (('left', (38,), (-1, 0, 'B'), (0, 0, 'b'), (1, 0, 'b')), (0, 0, 'F', (-1.0, 8))),
        (('left', (48,), (0, 0, 'b'), (0, 1, 'E'), (0, 2, 'A')), (0, 0, 'F', (-1.0, 1))),
        (('up', (33,), (-1, 0, 'b'), (0, 0, 'b'), (1, 0, 'E')), (0, 0, 'F', (-1.0, 8))),
        (('up', (11,), (-2, 0, 'a'), (-1, 0, 'H'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 8))),
        (('up', (48,), (0, -2, 'A'), (0, -1, 'C'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('down', (18,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('left', (20,), (0, -1, 'a'), (0, 0, 'b'), (0, 1, 'E')), (0, 0, 'F', (-1.0, -1))),
        (('down', (48,), (-2, 0, 'A'), (-1, 0, 'E'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('right', (20,), (0, -1, 'E'), (0, 0, 'b'), (0, 1, 'a')), (0, 0, 'F', (-1.0, -1))),
        (('right', (38,), (-1, 0, 'B'), (0, 0, 'b'), (1, 0, 'b')), (0, 0, 'F', (-1.0, 8))),
        (('left', (40,), (0, 0, 'b'), (0, 1, 'E'), (0, 2, 'A')), (0, 0, 'F', (-1.0, 1))),
        (('down', (38,), (-1, 0, 'B'), (0, 0, 'b'), (1, 0, 'b')), (0, 0, 'F', (-1.0, 8))),
        (('up', (34,), (-2, 0, 'a'), (-1, 0, 'H'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 8))),
        (('right', (48,), (0, -2, 'A'), (0, -1, 'E'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('right', (33,), (-1, 0, 'H'), (0, 0, 'b'), (1, 0, 'b')), (0, 0, 'F', (-1.0, 8))),
        (('up', (40,), (0, -2, 'A'), (0, -1, 'B'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('right', (18,), (0, -2, 'a'), (0, -1, 'H'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('left', (48,), (0, -2, 'A'), (0, -1, 'C'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('right', (11,), (-2, 0, 'a'), (-1, 0, 'H'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 8))),
        (('down', (33,), (-1, 0, 'H'), (0, 0, 'b'), (1, 0, 'b')), (0, 0, 'F', (-1.0, 8))),
        (('left', (33,), (0, -1, 'b'), (0, 0, 'b'), (0, 1, 'E')), (0, 0, 'F', (-1.0, 8))),
        (('up', (34,), (0, 0, 'b'), (1, 0, 'E'), (2, 0, 'a')), (0, 0, 'F', (-1.0, 1))),
        (('down', (33,), (-1, 0, 'E'), (0, 0, 'b'), (1, 0, 'b')), (0, 0, 'F', (-1.0, 8))),
        (('right', (34,), (0, -2, 'a'), (0, -1, 'E'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('down', (20,), (-1, 0, 'E'), (0, 0, 'b'), (1, 0, 'a')), (0, 0, 'F', (-1.0, -1))),
        (('down', (11,), (-2, 0, 'a'), (-1, 0, 'H'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 8))),
        (('right', (40,), (0, -2, 'A'), (0, -1, 'E'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('down', (18,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('up', (21,), (-1, 0, 'a'), (0, 0, 'b'), (1, 0, 'E')), (0, 0, 'F', (-1.0, 8))),
        (('right', (34,), (-2, 0, 'a'), (-1, 0, 'H'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 8))),
        (('down', (18,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('left', (40,), (0, -2, 'A'), (0, -1, 'B'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('right', (48,), (0, -2, 'A'), (0, -1, 'C'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('right', (18,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('left', (18,), (0, 0, 'b'), (0, 1, 'E'), (0, 2, 'a')), (0, 0, 'F', (-1.0, 1))),
        (('right', (33,), (0, -1, 'E'), (0, 0, 'b'), (0, 1, 'b')), (0, 0, 'F', (-1.0, 8))),
        (('up', (48,), (0, 0, 'b'), (1, 0, 'E'), (2, 0, 'A')), (0, 0, 'F', (-1.0, 1))),
        (('down', (21,), (-1, 0, 'E'), (0, 0, 'b'), (1, 0, 'a')), (0, 0, 'F', (-1.0, 8))),
        (('left', (33,), (-1, 0, 'H'), (0, 0, 'b'), (1, 0, 'b')), (0, 0, 'F', (-1.0, 8))),
        (('up', (18,), (0, 0, 'b'), (1, 0, 'E'), (2, 0, 'a')), (0, 0, 'F', (-1.0, 1))),
        (('up', (38,), (-1, 0, 'B'), (0, 0, 'b'), (1, 0, 'b')), (0, 0, 'F', (-1.0, 8))),
        (('right', (45,), (0, -2, 'a'), (0, -1, 'E'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('down', (48,), (0, -2, 'A'), (0, -1, 'C'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('left', (11,), (-2, 0, 'a'), (-1, 0, 'H'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 8))),
        (('left', (18,), (0, -2, 'a'), (0, -1, 'C'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('left', (45,), (0, 0, 'b'), (0, 1, 'E'), (0, 2, 'a')), (0, 0, 'F', (-1.0, 1))),
        (('down', (40,), (-2, 0, 'A'), (-1, 0, 'E'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('right', (21,), (0, -1, 'E'), (0, 0, 'b'), (0, 1, 'a')), (0, 0, 'F', (-1.0, 8))),
        (('down', (34,), (-2, 0, 'a'), (-1, 0, 'H'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 8))),
        (('right', (18,), (0, -2, 'a'), (0, -1, 'E'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('down', (34,), (-2, 0, 'a'), (-1, 0, 'E'), (0, 0, 'b')), (0, 0, 'F', (-1.0, 1))),
        (('up', (45,), (0, 0, 'b'), (1, 0, 'E'), (2, 0, 'a')), (0, 0, 'F', (-1.0, 1))),
        (('up', (20,), (-1, 0, 'a'), (0, 0, 'b'), (1, 0, 'E')), (0, 0, 'F', (-1.0, -1))),
        (('left', (34,), (0, 0, 'b'), (0, 1, 'E'), (0, 2, 'a')), (0, 0, 'F', (-1.0, 1))),
        (('up', (8,), (-1, 0, 'A'), (0, 0, 'c'), (1, 0, 'E')), (0, 0, 'C', (0.0, -8))),  # c
        (('left', (8,), (0, -1, 'A'), (0, 0, 'c'), (0, 1, 'E')), (0, 0, 'C', (0.0, -8))),
        (('up', (8,), (-1, 0, 'A'), (0, 0, 'c'), (1, 0, 'C')), (0, 0, 'C', (0.0, -8))),
        (('up', (8,), (-1, 0, 'A'), (0, 0, 'c'), (1, 0, 'B')), (0, 0, 'C', (0.0, -8))),
        (('right', (8,), (0, -1, 'E'), (0, 0, 'c'), (0, 1, 'A')), (0, 0, 'C', (0.0, -8))),
        (('left', (1,), (0, -1, 'A'), (0, 0, 'c'), (0, 1, 'B')), (0, 0, 'D', (0.0, -1))),
        (('left', (1,), (0, -1, 'A'), (0, 0, 'c'), (0, 1, 'C')), (0, 0, 'D', (0.0, -1))),
        (('left', (1,), (0, -1, 'A'), (0, 0, 'c'), (0, 1, 'H')), (0, 0, 'D', (0.0, -1))),
        (('down', (8,), (-1, 0, 'E'), (0, 0, 'c'), (1, 0, 'A')), (0, 0, 'C', (0.0, -8))),
    ]
    world_state_values = {'int_2from_rgb_list': [],
                          'int_2from_char_list': [(-1, 'A'), (-2, '.'), (2617493089, 'B'), (3144150970, 'C'),
                                                  (3712765165, 'D'), (2460067371, 'E'), (961690427, 'F'),
                                                  (1630428625, 'G'), (442688737, 'H'), (1147995044, 'a'),
                                                  (2117949728, 'b'), (1992348315, 'c'), (1868170614, 'd')],
                          'raw_cell_shape': (64, 64, 3), 'raw_nptype': "<class 'numpy.uint8'>"}
    agent = nace.agent_module.Agent(rc_loc=(1, 1), score=-24.0, terminated=0, values_excluding_prefix=[0])


    # hand coded code after this line

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

    ch = planworld.get_char_at_rc(2,2, agent_indication_embedded_value_list=[])
    # assert ch == 'E'
    print()


    actions = ['left', 'down', 'right', 'up']


    (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason,
     oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason,
     biggest_predicted_score_delta_actions, biggest_predicted_score_delta, biggest_predicted_score_delta_stopping_reason,
     smallest_predicted_score_delta_actions, smallest_predicted_score_delta,
     smallest_predicted_score_delta_stopping_reason,
     debbugging_data) = (
        _plan(
            planworld,
            new_rules,
            actions,
            new_focus_set,
            planagent))

    rc_lowest_conf = nace.test_utilities.get_rc_delta_for_action_list(lowest_conf_actions)
    rc_oldest = nace.test_utilities.get_rc_delta_for_action_list(oldest_age_actions)
    print("rc_lowest_conf",rc_lowest_conf)
    print("rc_oldest",rc_oldest)
    print("")



def t3_duplicate_predicted_agents_possible():
    """
    If unknown value (q) introduced nearer the agent than the known food,
    best_actions still goes for the food,
    but best_action_combination_for_revisit will go for the unobserved spot.

    Code used to create more than 1 agent on prediction, it no longer does, under this case, but it is valid if dynamics are not fully known.




    @return:
    """
    world_str_list = [
        ['ooooooo',
         'o     o',
         'o   xqo', # q does not exist in rules.
         'ooooooo'], (),
        ['26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
         '26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
         '26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
         '18.0,18.0,16.0,15.0,14.0,13.0,12.0,']]
    rules = {

        # open space
        (('down', (), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,))),
        (('down', (), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
        (('up', (), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,))),
        (('up', (), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
        (('left', (), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))),
        (('left', (), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
        (('right', (), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
        (('right', (), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,))),

        # walls
        (('up', (), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,))),
        (('up', (), (-1, 0, 'o'), (0, 0, 'x')), (0, 0, 'x', (0,))),
        (('right', (), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
        (('right', (), (0, 0, 'x'), (0, 1, 'o')), (0, 0, 'x', (0,))),
        (('left', (), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,))),
        (('left', (), (0, -1, 'o'), (0, 0, 'x')), (0, 0, 'x', (0,))),
        (('down', (), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
        (('down', (), (0, 0, 'x'),  (-1, 0, 'o')), (0, 0, 'x', (0,))),
        }
    actions = ['right', 'left', 'up', 'down']
    focus_set = {'x': 9, 'q': 1}
    agent = nace.agent_module.Agent((2, 4), 0, 0, ())
    world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        world_str_list[0],
        view_dist_x=50,
        view_dist_y=50,
        agent_char_code_list=['x'],
        observed_times_str_list=world_str_list[2],
    )
    world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])

    assert world.get_char_at_rc(agent.get_rc_loc()[0],agent.get_rc_loc()[1], agent_indication_embedded_value_list=[]) == 'x'

    nace.hypothesis.Hypothesis_UseLRUDMovementOpAssumptions(
        'left',
        'right',
        'up',
        'down',
        nace.world_module.drop,
        DisableLRUDOpSymmetryAssumptionFlag=False,
    )

    # convert focus_set and rules to use embeddings rather than char (which is used for convenience)
    new_focus_set = convert_focus_set_to_internal_mapping(focus_set, world)
    new_rules = convert_rules_to_internal_mapping(rules, world)

    action = 'right'
    custom_goal = None
    current_world = copy.deepcopy(world)
    new_world, planagent, new_AIRIS_confidence, __age, agent_values_delta, predicted_score_delta = (
        nace.nace_v3._predict_next_world_state(
            focus_set,
            current_world, action, rules, agent, custom_goal,
            brute_force_focus_next_step=True
        ))

    assert new_world.debug_board.count('x') == 1 # we desire only 1 agent

    print("________________")

    (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason,
     oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason,
     biggest_predicted_score_delta_actions, biggest_predicted_score_delta, biggest_predicted_score_delta_stopping_reason,
     smallest_predicted_score_delta_actions, smallest_predicted_score_delta,
     smallest_predicted_score_delta_stopping_reason,
     debbugging_data) = (
        _plan(
            world,
            new_rules,
            actions,
            new_focus_set,
            agent,
            max_num_actions=20,
            max_queue_length=2000,
            shuffle_actions=False,
            short_curcuit_planning=False,
            brute_force_focus_next_step=True
        )
    )

    print("debugging data:",json.dumps(debbugging_data, indent=2))

    rc_lowest_conf = nace.test_utilities.get_rc_delta_for_action_list(lowest_conf_actions)
    print("rc_lowest_conf",rc_lowest_conf, "lowest_AIRIS_confidence", lowest_AIRIS_confidence)
    rc_biggest_score = nace.test_utilities.get_rc_delta_for_action_list(biggest_predicted_score_delta_actions)
    print("biggest_predicted_score_delta=",biggest_predicted_score_delta, "rc", rc_biggest_score) # expect 0 there is no food

    assert rc_lowest_conf == (0,1) # go for the unknown 'q'

    # there are no asserts in this test, as I am unsure it it is as design.
    # this test triggeres the case when predict_next world places
    # multiple agents on the board, do to rules, which are the most confident,
    # but do not have all their pre conditions met, being fired.

    # SHould plan have different behaviour based on whether we are obseriving and learning?



def t15_agent_should_avoid_termination_when_it_knows_better():
    """

    After the agent hits water and dies, it should not do it immediately afterwards, which it appears to do.
    This unit test it to check it does avoid certain death quickly.

    @return:
    """

    world_str_list = [
        'AAAAAAA..',
        'Aaabbbb..',
        'AaeFcdd..',
        'Aaedcdd..',
        'Aaedddd..',
        '.........',
        '.........',
                      '.........', '.........']

    focus_set = {'b': 18, 'a': 16, 'F': 5, 'H': 2, 'd': 12, 'c': 2, 'e': 7, 'f': 1, 'I': 1}
    rules = [
        (('^turn_right', (0,), (-1, 1, 'b'), (0, 0, 'F'), (1, -1, 'a')), (0, 0, 'H', (0.0,0,))),  # F
        (('^turn_left', (0,), (0, -1, 'a'), (0, 0, 'F'), (1, 1, 'd')), (0, 0, 'I', (0.0,0,))),
        (('^forward', (0,), (-1, 0, 'b'), (0, 0, 'F'), (1, 0, 'd')), (0, 0, 'e', (0.0,0,))),
        (('^turn_left', (0,), (-1, 1, 'a'), (0, 0, 'H'), (1, -1, 'b')), (0, 0, 'F', (0.0,0,))),  # H
        (('^turn_right', (0,), (0, -1, 'b'), (0, 0, 'I'), (1, 1, 'e')), (0, 0, 'F', (0.0,0,))),  # I
        (('^turn_left', (0,), (0, -1, 'a'), (0, 0, 'a')), (0, 0, 'b', (0.0,0,))),  # a
        (('^turn_left', (0,), (0, 0, 'a'), (1, -1, 'H')), (0, 0, 'b', (0.0,0,))),
        (('^turn_left', (0,), (0, 0, 'a'), (0, 1, 'F')), (0, 0, 'b', (0.0,0,))),
        (('^turn_right', (0,), (-1, 1, 'F'), (0, 0, 'a')), (0, 0, 'b', (0.0,0,))),
        (('^turn_left', (0,), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'b', (0.0,0,))),
        (('^turn_right', (0,), (0, 0, 'b'), (1, -1, 'F')), (0, 0, 'a', (0.0,0,))),  # b
        (('^forward', (0,), (0, 0, 'b'), (1, 0, 'F'), (2, 0, 'd')), (0, 0, 'a', (0.0,0,))),
        (('^turn_right', (0,), (0, -1, 'b'), (0, 0, 'b')), (0, 0, 'b', (0.0,0,))),
        (('^turn_right', (0,), (0, 0, 'b'), (0, 1, 'I')), (0, 0, 'a', (0.0,0,))),
        (('^turn_left', (0,), (-1, 1, 'H'), (0, 0, 'b')), (0, 0, 'a', (0.0,0,))),
                                                                                   # c added ( c== water)
        (('^forward', (0,), (0, 0, 'c'), (0, -1, 'F'), (0, -2, 'e')), (0, 0, 'D', (-1.0, 1,))),  # <= become terminated on this rule - we expect this to fire

        (('^forward', (0,), (-2, 0, 'b'), (-1, 0, 'F'), (0, 0, 'd')), (0, 0, 'e', (0.0,0,))),  # d
        (('^turn_left', (0,), (-1, -1, 'F'), (0, 0, 'd')), (0, 0, 'e', (0.0,0,))),
        (('^forward', (0,), (-1, 0, 'd'), (0, 0, 'd')), (0, 0, 'e', (0.0,0,))),
        (('^forward', (0,), (-1, 1, 'd'), (0, 0, 'd'), (1, 0, 'd')), (0, 0, 'e', (0.0,0,))),
        (('^forward', (0,), (0, 0, 'd'), (1, -1, 'd')), (0, 0, 'F', (0.0,0,))),
        (('^turn_right', (0,), (-1, -1, 'I'), (0, 0, 'e')), (0, 0, 'd', (0.0,0,))),  # e
        (('^turn_right', (0,), (0, 0, 'e'), (0, 1, 'e')), (0, 0, 'd', (0.0,0,))),
        (('^turn_right', (0,), (-1, 0, 'e'), (0, 0, 'e')), (0, 0, 'd', (0.0,0,))),
        (('^turn_right', (0,), (-1, 1, 'f'), (0, -1, 'e'), (0, 0, 'e')), (0, 0, 'd', (0.0,0,))),
        (('^turn_right', (0,), (0, 0, 'e'), (1, 0, 'e')), (0, 0, 'd', (0.0,0,))),
        (('^turn_right', (0,), (0, 0, 'f'), (1, -1, 'e')), (0, 0, 'c', (0.0,0,))),  # f
    ]
    rule_evidence = {
         (('^turn_right', (0,), (-1, 1, 'F'), (0, 0, 'a')), (0, 0, 'b', (0.0,0,))): (2, 0),
         (('^turn_right', (0,), (0, 0, 'b'), (1, -1, 'F')), (0, 0, 'a', (0.0,0,))): (2, 0),
         (('^turn_right', (0,), (-1, 1, 'b'), (0, 0, 'F'), (1, -1, 'a')), (0, 0, 'H', (0.0,0,))): (2, 0),
         (('^turn_right', (0,), (0, 0, 'b'), (0, 1, 'b')), (0, 0, 'a', (0.0,0,))): (2, 4),
         (('^turn_right', (0,), (0, -1, 'b'), (0, 0, 'b')), (0, 0, 'a', (0.0,0,))): (5, 5),
         (('^turn_left', (0,), (-1, 1, 'H'), (0, 0, 'b')), (0, 0, 'a', (0.0,0,))): (2, 0),
         (('^turn_left', (0,), (0, 0, 'a'), (1, -1, 'H')), (0, 0, 'b', (0.0,0,))): (2, 0),
         (('^turn_left', (0,), (-1, 1, 'a'), (0, 0, 'H'), (1, -1, 'b')), (0, 0, 'F', (0.0,0,))): (2, 0),
         (('^turn_left', (0,), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'b', (0.0,0,))): (2, 1),
         (('^turn_left', (0,), (0, -1, 'a'), (0, 0, 'a')), (0, 0, 'b', (0.0,0,))): (2, 0),
         (('^forward', (0,), (-2, 0, 'b'), (-1, 0, 'F'), (0, 0, 'd')), (0, 0, 'e', (-1.0,0,))): (1, 1),
         (('^forward', (0,), (0, 0, 'b'), (1, 0, 'F'), (2, 0, 'd')), (0, 0, 'a', (-1.0,0,))): (1, 1),
         (('^forward', (0,), (-1, 0, 'b'), (0, 0, 'F'), (1, 0, 'd')), (0, 0, 'e', (-1.0,0,))): (1, 1),
         (('^forward', (0,), (0, 0, 'c'), (0, -1, 'F'), (0, -2, 'e')), (0, 0, 'D', (-1.0,1,))): (2, 1),    # <= become terminated on this rule
         (('^forward', (0,), (-1, 1, 'c'), (0, 0, 'd'), (1, 0, 'd')), (0, 0, 'e', (-1.0,0,))): (1, 1),
         (('^forward', (0,), (-1, 0, 'd'), (0, 0, 'd')), (0, 0, 'e', (-1.0,0,))): (1, 5),
         (('^turn_left', (0,), (0, 0, 'c'), (1, -1, 'd')), (0, 0, 'f', (0.0,0,))): (1, 2),
         (('^turn_left', (0,), (0, 0, 'd'), (0, 1, 'd')), (0, 0, 'e', (0.0,0,))): (1, 7),
         (('^turn_left', (0,), (-1, 1, 'c'), (0, -1, 'd'), (0, 0, 'd')), (0, 0, 'e', (0.0,0,))): (1, 2),
         (('^turn_left', (0,), (-1, -1, 'F'), (0, 0, 'd')), (0, 0, 'e', (0.0,0,))): (1, 0),
         (('^turn_left', (0,), (0, 0, 'a'), (0, 1, 'F')), (0, 0, 'b', (0.0,0,))): (1, 0),
         (('^turn_left', (0,), (0, -1, 'a'), (0, 0, 'F'), (1, 1, 'd')), (0, 0, 'I', (0.0,0,))): (1, 0),
         (('^turn_left', (0,), (-1, 0, 'd'), (0, 0, 'd')), (0, 0, 'e', (0.0,0,))): (1, 5),
         (('^turn_left', (0,), (0, 0, 'd'), (1, 0, 'd')), (0, 0, 'e', (0.0,0,))): (1, 5),
         (('^turn_right', (0,), (0, 0, 'f'), (1, -1, 'e')), (0, 0, 'c', (0.0,0,))): (1, 0),
         (('^turn_right', (0,), (0, 0, 'e'), (0, 1, 'e')), (0, 0, 'd', (0.0,0,))): (1, 0),
         (('^turn_right', (0,), (-1, 1, 'f'), (0, -1, 'e'), (0, 0, 'e')), (0, 0, 'd', (0.0,0,))): (1, 0),
         (('^turn_right', (0,), (-1, -1, 'I'), (0, 0, 'e')), (0, 0, 'd', (0.0,0,))): (1, 0),
         (('^turn_right', (0,), (0, 0, 'b'), (0, 1, 'I')), (0, 0, 'a', (0.0,0,))): (1, 0),
         (('^turn_right', (0,), (0, -1, 'b'), (0, 0, 'I'), (1, 1, 'e')), (0, 0, 'F', (0.0,0,))): (1, 0),
         (('^turn_right', (0,), (-1, 0, 'e'), (0, 0, 'e')), (0, 0, 'd', (0.0,0,))): (1, 0),
         (('^turn_right', (0,), (0, 0, 'e'), (1, 0, 'e')), (0, 0, 'd', (0.0,0,))): (1, 0),
         (('^turn_right', (0,), (0, -1, 'b'), (0, 0, 'b')), (0, 0, 'b', (0.0,0,))): (5, 3),
         (('^forward', (0,), (-2, 0, 'b'), (-1, 0, 'F'), (0, 0, 'd')), (0, 0, 'e', (0.0,0,))): (1, 0),
         (('^forward', (0,), (0, 0, 'b'), (1, 0, 'F'), (2, 0, 'd')), (0, 0, 'a', (0.0,0,))): (1, 0),
         (('^forward', (0,), (-1, 0, 'b'), (0, 0, 'F'), (1, 0, 'd')), (0, 0, 'e', (0.0,0,))): (1, 0),
         (('^forward', (0,), (0, 0, 'd'), (1, -1, 'd')), (0, 0, 'F', (0.0,0,))): (1, 0),
         (('^forward', (0,), (-1, 1, 'd'), (0, 0, 'd'), (1, 0, 'd')), (0, 0, 'e', (0.0,0,))): (1, 0),
         (('^forward', (0,), (-1, 0, 'd'), (0, 0, 'd')), (0, 0, 'e', (0.0,0,))): (1, 0)
         }
    world_state_values = {'int_2from_rgb_list': [],
                          'int_2from_char_list': [(-1, 'A'), (-2, '.'), (823474807, 'B'), (362910338, 'C'),
                                                  (69488790, 'D'), (2829951097, 'E'), (3539787669, 'F'),
                                                  (1867891296, 'G'), (1704944625, 'H'), (3665670421, 'I'),
                                                  (1484579719, 'a'), (2204181460, 'b'), (3044822657, 'c'),
                                                  (2407174942, 'd'), (1152208772, 'e'), (71253317, 'f')],
                          'raw_cell_shape': (32, 32, 3), 'raw_nptype': "<class 'numpy.uint8'>"}
    agent = nace.agent_module.Agent(rc_loc=(2, 3), score=-1.0, terminated=0, values_excluding_prefix=[])

    # note: If there are any rules with MORE precondition, they will have higher confidence, and fire,
    # and rules with fewer preconditions will not.

    # hand-coded code after this line
    # convert into internal values
    # hand-coded code after this line
    # convert into internal values
    # Info (check image in tmp dir with same name as internal encoding to get this mapping (should be deterministic and stationary between restarts)
    # (-1, 'A'),              Outermost wall (synthesised)
    # (-2, '.'),              Unobserved value
    # (823474807, 'B'),       Agent facing Right
    # (362910338, 'C'),       Agent Facing Down   (on water)
    # (69488790, 'D'),        Agent Facing Right  (on water)
    # (2829951097, 'E'),      Agent Facing Left
    # (3539787669, 'F'),      Agent Facing Right (black background)
    # (1867891296, 'G'),      Agent Facing Down  (green background) (success)
    # (1704944625, 'H'),      Agent Facing Down  (black background)
    # (3665670421, 'I'),      Agent Facing Up    (black background)
    # (1484579719, 'a'),      Black square       (start location)
    # (2204181460, 'b'),      Grey  square       Traversable Cell
    # (3044822657, 'c'),      Blue with Waves    water
    # (2407174942, 'd')       Black square with grey edges top and left


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
    new_rule_evidence = convert_rule_evidence_to_internal_mapping(rule_evidence, world)
    actions = ['^turn_left', '^turn_right', '^forward']

    nace.world_module.set_full_action_list(actions)





    # Now do the actual testing

    # check forward would kill us

    # Step 2: Refine rules based on evidence
    active_rules, rules_excluded = Hypothesis_BestSelection(
        rules=copy.deepcopy(new_rules),
        rules_excluded=set(),
        rule_evidence=new_rule_evidence,
        include_random_rules=False)

    terminated_predicted_world, terminated_predicted_agent, terminated_new_AIRIS_confidence, terminated__age, terminated_agent_values_delta, terminated_predicted_score_delta = (
        _predict_next_world_state(
            copy.deepcopy(new_focus_set),
            copy.deepcopy(world),
            action="^forward",
            rules=copy.deepcopy(active_rules),
            agent=copy.deepcopy(agent),
            custom_goal=None,
            brute_force_focus_next_step=False,
            minimum_cell_predict_confidence_threshold=0.0
        ))
    world.multiworld_print([{"World": terminated_predicted_world, "Color": nace.color_codes.color_code_white_on_blue, "Caption":"Predicted world"}])
    assert terminated_predicted_agent.get_terminated() == 1.0

    # Now check we would do something else rather than die.
    results = []
    for i in range(1):
        whole_plan, rules_excluded, behavior, statistics, _1 = nacev3_get_next_action(
            time_counter=world.get_newest_time()+1,
            focus_set=new_focus_set,
            rule_evidence=new_rule_evidence,
            rc_locations=[agent.get_rc_loc()],
            internal_world_model=world,
            rules_in=new_rules,
            external_ground_truth_world_model=None,
            print_debug_info=False,
            stayed_the_same=False, # ?
            agent=agent,
            full_action_list=actions,  # used during babling
            agent_indication_raw_value_list=[], # embedded values
            max_num_actions=1, # planning search depth
            max_queue_length=70 # planning queue depth
        )
        action = whole_plan[0]
        results.append( (action, behavior) )
        print(action, behavior)
    for r in results:
        print(r)

    print("action", action)
    assert action != "forward" and action != "^forward"


    # how should termination be stored? learnt? Currently learned at -1 reward.
    # so it will be uncertain next time we will terminate. We get 'forward' CURIOUS returned.
    # We should get a high confidence, but low score from the first forward.


def t16_understanding_planning():
    # not actual unit test
    world_str_list = ['AAAAAA...', 'Aabbbb...', 'AaFcdd...', 'Aadcdd...', 'Aadcdd...', '.........', '.........',
                      '.........', '.........']
    time_str_list = []
    focus_set = {'b': 7, 'a': 7, 'F': 1, 'H': 1}
    active_rules = [
        (('turn_right', (0,), (-1, 1, 'b'), (0, 0, 'F'), (1, -1, 'a')), (0, 0, 'H', (0.0,0,))),  # F
        (('turn_left', (0,), (-1, 1, 'a'), (0, 0, 'H'), (1, -1, 'b')), (0, 0, 'F', (0.0,0,))),  # H
        (('turn_right', (0,), (-1, 1, 'F'), (0, 0, 'a')), (0, 0, 'b', (0.0,0,))),  # a
        (('turn_left', (0,), (0, 0, 'a'), (1, -1, 'H')), (0, 0, 'b', (0.0,0,))),
        (('turn_left', (0,), (0, -1, 'a'), (0, 0, 'a')), (0, 0, 'b', (0.0,0,))),
        (('turn_right', (0,), (0, 0, 'b'), (1, -1, 'F')), (0, 0, 'a', (0.0,0,))),  # b
        (('turn_left', (0,), (-1, 1, 'H'), (0, 0, 'b')), (0, 0, 'a', (0.0,0,))),
        (('turn_right', (0,), (0, -1, 'b'), (0, 0, 'b')), (0, 0, 'a', (0.0,0,))),
        (('turn_right', (0,), (0, 0, 'b'), (0, 1, 'b')), (0, 0, 'a', (0.0,0,))),
    ]  # subset of rule_evidence
    rule_evidence = {(('turn_right', (0,), (-1, 1, 'F'), (0, 0, 'a')), (0, 0, 'b', (0.0,0,))): (1, 0),
                     (('turn_right', (0,), (0, 0, 'b'), (1, -1, 'F')), (0, 0, 'a', (0.0,0,))): (1, 0),
                     (('turn_right', (0,), (-1, 1, 'b'), (0, 0, 'F'), (1, -1, 'a')), (0, 0, 'H', (0.0,0,))): (1, 0),
                     (('turn_right', (0,), (0, 0, 'b'), (0, 1, 'b')), (0, 0, 'a', (0.0,0,))): (1, 0),
                     (('turn_right', (0,), (0, -1, 'b'), (0, 0, 'b')), (0, 0, 'a', (0.0,0,))): (1, 0),
                     (('turn_left', (0,), (-1, 1, 'H'), (0, 0, 'b')), (0, 0, 'a', (0.0,0,))): (1, 0),
                     (('turn_left', (0,), (0, 0, 'a'), (1, -1, 'H')), (0, 0, 'b', (0.0,0,))): (1, 0),
                     (('turn_left', (0,), (-1, 1, 'a'), (0, 0, 'H'), (1, -1, 'b')), (0, 0, 'F', (0.0,0,))): (1, 0),
                     (('turn_left', (0,), (0, 0, 'a'), (0, 1, 'a')), (0, 0, 'b', (0.0,0,))): (1, 1),
                     (('turn_left', (0,), (0, -1, 'a'), (0, 0, 'a')), (0, 0, 'b', (0.0,0,))): (1, 0)}
    world_state_values = {'int_2from_rgb_list': [],
                          'int_2from_char_list': [(-1, 'A'), (-2, '.'), (823474807, 'B'), (362910338, 'C'),
                                                  (69488790, 'D'), (2829951097, 'E'), (3539787669, 'F'),
                                                  (1867891296, 'G'), (1704944625, 'H'), (3665670421, 'I'),
                                                  (1484579719, 'a'), (2204181460, 'b'), (3044822657, 'c'),
                                                  (2407174942, 'd')], 'raw_cell_shape': (32, 32, 3),
                          'raw_nptype': "<class 'numpy.uint8'>"}
    agent = nace.agent_module.Agent(rc_loc=(2, 2), score=0.0, terminated=0, values_excluding_prefix=[])
    actions = ['turn_left', 'turn_right', 'forward']
    behaviour_returned = 'BABBLE'
    whole_plan_returned = ['forward']

    # hand-coded code after this line
    # convert into internal values
    # Info (check image in tmp dir with same name as internal encoding to get this mapping (should be deterministic and stationary between restarts)
    # (-1, 'A'),              Outermost wall (synthesised)
    # (-2, '.'),              Unobserved value
    # (823474807, 'B'),       Agent facing Right
    # (362910338, 'C'),       Agent Facing Down   (on water)
    # (69488790, 'D'),        Agent Facing Right  (on water)
    # (2829951097, 'E'),      Agent Facing Left
    # (3539787669, 'F'),      Agent Facing Right (black background)
    # (1867891296, 'G'),      Agent Facing Down  (green background) (success)
    # (1704944625, 'H'),      Agent Facing Down  (black background)
    # (3665670421, 'I'),      Agent Facing Up    (black background)
    # (1484579719, 'a'),      Black square       (start location)
    # (2204181460, 'b'),      Grey  square       Traversable Cell
    # (3044822657, 'c'),      Blue with Waves    water
    # (2407174942, 'd')       Black square with grey edges top and left

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
    new_active_rules = convert_rules_to_internal_mapping(active_rules, world)
    new_rule_evidence = convert_rule_evidence_to_internal_mapping(rule_evidence, world)

    nace.world_module.set_full_action_list(actions)

    # Now do the actual testing
    results = collections.defaultdict(int)
    behavior_results = collections.defaultdict(int)
    for i in range(20):
        whole_plan, rules_excluded, behavior, statistics, _1 = nacev3_get_next_action(
            time_counter=world.get_newest_time() + 1,
            focus_set=new_focus_set,
            rule_evidence=new_rule_evidence,
            rc_locations=[agent.get_rc_loc()],
            internal_world_model=world,
            rules_in=new_active_rules,
            external_ground_truth_world_model=None,
            print_debug_info=False,
            stayed_the_same=False,  # ?
            agent=agent,
            full_action_list=actions,  # used during babling
            agent_indication_raw_value_list=[],  # embedded values
            max_num_actions=5,  # planning search depth
            max_queue_length=70  # planning queue depth
        )
        action = whole_plan[0]
        results[ (action, behavior) ] += 1
        behavior_results[behavior] += 1
        print(action, behavior)

    print("results",results)
    print("behavior_results",behavior_results)

    assert behavior_results["BABBLE"] >= 0
    assert behavior_results["CURIOUS"] >= 0
    assert behavior_results["EXPLORE"] >= 0


    print("")


if __name__ == "__main__":


    # underway
    t1_plan_will_go_for_food_over_varying_distances(check_oldest_cell_as_well=True)  # passes
    t1_plan_will_go_for_food_over_varying_distances(check_oldest_cell_as_well=False)  # passes


    # oldest cell tests
    t12_go_for_unobserved()  # passes


    # path tests
    # t1_plan_will_go_for_food_over_varying_distances(check_oldest_cell_as_well=False)  # passes
    t2_plan_reward_and_unknown_value()                 # usually passes - unless dynamics not fully known and predict_next_state leaves 2 agents on map.
    t3_duplicate_predicted_agents_possible() # now passed on predict, but still get duplicate values on plan.
    t4_food_too_far_away_go_for_oldest_observed()  # passes
    t5_equal_distance_food()                       # passes
    t6_oldest_age_and_goal_same_square()           # passes
    t7_fully_known_world_and_rules_but_no_score_increasing_target() # passes

    # oldest cell tests
    # t1_plan_will_go_for_food_over_varying_distances(check_oldest_cell_as_well=True)  # passes
    t9_actual_example_where_we_fail_1()    # passes
    t10_fully_known_rules_does_the_agent_always_go_for_score_increasing_target()  # passes
    t11_plan_no_food_full_observation()  # passes
    t12_go_for_unobserved()  # passes
    t14_plan_no_food_partial_observation_best_for_revisit()  # passes

    # termination
    t15_agent_should_avoid_termination_when_it_knows_better()

    # planning
    t16_understanding_planning()

    # utilities
    # t2_plan_find_required_queue_length()

    # in progress
    # t9_actual_example_where_we_oscillate_1() # know what to assert, now understand, stick plans should sort this.
    t17_why_frozen_lake_is_inefficient()
