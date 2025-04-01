import copy
import math
import json
import time
import random
import xxhash
import os.path
import traceback
import collections
from typing import Type, Dict, Tuple, Set, Any, Union, List

import numpy as np
import nace

import nace.color_codes
from nace.agent_module import Agent
# from nace.hypothesis import *
from nace.hypothesis import Hypothesis_BestSelection, Hypothesis_ValidCondition, Hypothesis_Confirmed, \
    Hypothesis_Contradicted, Hypothesis_TruthValue
from nace.prettyprint import prettyprint_all_actions, prettyprint_rule
from nace.world_module_numpy import NPWorld
from nace.test_utilities import convert_rules_to_char_or_int_mappings, convert_rule_evidence_to_char_or_int_mappings


# used in place of randome actions, to ensure we cycle through all actions.
last_action_in_situation = collections.defaultdict(int)


# See nace.py for type and data structure descriptions


def _get_rc_delta_for_action_list(action_list):
    # ignores walls etc. Only use this for testing.
    c = 0
    r = 0
    for action in action_list:
        if action == 'down':
            r += 1
        if action == 'up':
            r -= 1
        if action == 'left':
            c -= 1
        if action == 'right':
            c += 1
    return r, c


def _plan(world: Type[NPWorld],
          active_rules: set,
          actions,  # : Union[List[function], List[NoneType], List[int], List[str]]
          focus_set,
          agent: Type[Agent],
          max_num_actions: int = 12,
          max_queue_length: int = 300,
          custom_goal = None,
          continue_planning_threshold: float = 0.51,  # planning stops in conf drops below this. why 0.5?
          short_curcuit_planning: bool = True,
          shuffle_actions: bool = True,
          brute_force_focus_next_step: bool = False,
          minimum_cell_predict_confidence_threshold: float = 0.0,
          rules_excluded:set = set(),
          circular_action_sequences = [("turn_left", "turn_right"), ("turn_right", "turn_left"), ("turn_right", "turn_right", "turn_right", "turn_right"), ("turn_left", "turn_left", "turn_left", "turn_left")],
          gather_trace_info=False
          ):
    """
    Plan forward searching for situations of highest reward or lowest AIRIS confidence or oldest age.

    We place len(actions) items on the queue for every one we take off, and there is a queue length limit, so
    increasing the number of actions potentially stops us finding the optimal solution.


    Open Question(s):
        Does this routine need to support a no-op? i.e. do not move or do anything?

    Returns:
    - lowest_conf_actions: List of actions leading to the lowest AIRIS confidence
    - lowest_AIRIS_confidence: The lowest AIRIS confidence score (highest reward for exploring)
    - oldest_age_actions: Actions leading to the oldest world state
    - smallest_time: time the oldest world state encountered
    """
    queue = collections.deque([(copy.deepcopy(world), copy.deepcopy(agent.get_values_inc_prefix()), [], 0, "Initialization Value")])  # (world_state, actions, depth, debug_data)
    encountered = {}  # used to short-circuit search
    encountered_rc = {} # used to sort-circuit search
    end_situation_evaluation_count = 0
    evaluation_count_at_which_reward_found = -1
    evaluation_count_at_which_lower_AIRIS_confidence_found = -1
    evaluation_count_at_which_older_found = -1
    actions = copy.deepcopy(actions)
    if shuffle_actions:
        random.shuffle(actions) # shuffle the actions, but keep them in the same random order for this whole function.
    else:
        print("WARN shuffling of action order is disabled.")

    lowest_conf_actions = []
    lowest_AIRIS_confidence = float("inf")  # smaller is better
    lowest_conf_predicted_score_delta = 0.0
    lowest_conf_stopping_reason = "NI"

    max_conf_actions = []

    oldest_age_actions = []
    oldest_age = -1  # if we see an age (time difference) greater than this, we store it.
    oldest_age_predicted_score_delta = 0.0
    oldest_age_stopping_reason = "NI"

    dead_plans = []
    off_map_edge_count = 0

    biggest_predicted_score_delta_actions = []
    biggest_predicted_score_delta = -0.000001
    biggest_predicted_score_delta_stopping_reason = "NI"

    smallest_predicted_score_delta_actions = []
    smallest_predicted_score_delta = 0.000001
    smallest_predicted_score_delta_stopping_reason = "NI"
    predict_next_world_state_call_count = 0
    temp_stop_reason_rc = [[[]]*world.board.shape[1]]*world.board.shape[0]
    if agent.get_score() >= 1:
        pass
    trace_string = ""
    starting_situations_evaluated = 0
    while queue:  # queue size = number of actions * roll out length
        (current_world, current_agent_values, planned_actions, depth, stopping_reason) = queue.popleft()
        starting_situations_evaluated += 1
        if gather_trace_info:
            trace_string += "starting_situations_evaluated=" + str(starting_situations_evaluated) + "\n"

        # need to store agent values on the queue as well, and add the values delta to them.
        if depth >= max_num_actions:
            # print(f"Max depth of {max_num_actions} reached, stopping search.")
            if gather_trace_info:
                t_stopping_reason = "Max depth"
                dead_plan_list = planned_actions
                rc_delta = _get_rc_delta_for_action_list(dead_plan_list)
                dead_plans.append((rc_delta, t_stopping_reason, dead_plan_list))
                trace_string += "  depth >= max_num_actions" + "\n"
            continue # don't add this or children to the queue, i.e. stop exploring from here

        world_state = (current_world.get_board_hashcode(), tuple(current_agent_values[1:]))
        # skip search from here, if not needed via world state hashcodes
        _should_skip_state = world_state in encountered and depth >= encountered[world_state]
        if gather_trace_info:
            trace_string += "  _should_skip_state=" + str(_should_skip_state) + "\n"
        if _should_skip_state:
            # skip states already evaluated (optimisation)
            # print(f"Skipping state")
            if gather_trace_info:
                t_stopping_reason = "Skipping state - been here before"  # i.e. [left, right, left] after a [left] was evaluated.
                dead_plan_list = planned_actions
                rc_delta = _get_rc_delta_for_action_list(dead_plan_list)
                dead_plans.append((rc_delta, t_stopping_reason, dead_plan_list))
                trace_string += "  _should_skip_state" + "\n"
            continue # don't add this or children to the queue, i.e. stop exploring from here

        encountered[world_state] = depth # store that we have been here to prune the search space and avoid loops

        for action in actions:  # check each action in turn from a known state
            new_planned_actions = planned_actions + [action]
            new_planned_actions_rc_delta = _get_rc_delta_for_action_list(new_planned_actions)
            end_rc_location =  agent.get_rc_loc()[0]+new_planned_actions_rc_delta[0], agent.get_rc_loc()[1]+new_planned_actions_rc_delta[1]
            predicted_world, predicted_agent, new_AIRIS_confidence, __age, agent_values_delta, predicted_score_delta = (
                _predict_next_world_state(
                    focus_set,
                    current_world, action, active_rules, agent, custom_goal,
                    brute_force_focus_next_step=brute_force_focus_next_step,
                    minimum_cell_predict_confidence_threshold=minimum_cell_predict_confidence_threshold
                ))
            predict_next_world_state_call_count += 1
            if gather_trace_info:
                trace_string +=  "  new_planned_actions=" + str(prettyprint_all_actions(new_planned_actions)) + "\n" + \
                    "  new_AIRIS_confidence=" + str(new_AIRIS_confidence) + "\n" + \
                    "  new_planned_actions_rc_delta=" + str(new_planned_actions_rc_delta) +"\n" + \
                    "  end_rc_location="+str(end_rc_location) +"\n" + \
                    "  current_world=" +current_world.debug_board +"\n"+ \
                    "  new_world=" + predicted_world.debug_board + "\n"
            if 0 <= end_rc_location[0] < world.board.shape[0] and 0 <= end_rc_location[1] < world.board.shape[1]:
                is_off_map_edge = False
                new_oldest_age = current_world.get_newest_time() - current_world.get_time_at_rc(end_rc_location[0],end_rc_location[1])
            else:
                off_map_edge_count += 1
                is_off_map_edge = True
                new_oldest_age = 0

            # if predicted_score_delta > 0.0:
            #     print("DEBUG REF178 predicted_score_delta > 0.0")
            # if new_AIRIS_confidence < 1.0:
            #     print("DEBUG REF180 new_AIRIS_confidence < 1.0")

            is_circular_action_sequence = False
            for sequence in circular_action_sequences:
                if len(new_planned_actions) >= len(sequence):
                    match = True
                    for i in range(len(sequence)):
                        if sequence[i] != new_planned_actions[-(len(sequence)) + i ]:
                            match = False
                            break
                    if match:
                        is_circular_action_sequence = True
                        break
            if is_circular_action_sequence:
                continue  # no need to continue evaluating (optimisation) this action
                # as the combination of actions redundant, so should be explored elsewhere.

            is_no_board_or_agent_state_change = (predicted_world.get_board_hashcode() == current_world.get_board_hashcode() and
                    sum(agent_values_delta)==0 )

            if predicted_agent.get_terminated() >= 1 and new_AIRIS_confidence >= continue_planning_threshold:
                if gather_trace_info:
                    t_stopping_reason = "agent terminated"
                    dead_plan_list = copy.deepcopy(new_planned_actions)
                    dead_plans.append((new_planned_actions_rc_delta, t_stopping_reason, dead_plan_list))
                    trace_string += "  "+t_stopping_reason + "\n"
                continue  # no need to continue evaluating (optimisation) this action as we just died


            if ((predicted_score_delta < smallest_predicted_score_delta) or
                    (predicted_score_delta == smallest_predicted_score_delta and
                     len(new_planned_actions) < len(smallest_predicted_score_delta_actions) )):
                smallest_predicted_score_delta_actions = copy.deepcopy(new_planned_actions)
                smallest_predicted_score_delta = predicted_score_delta
                smallest_predicted_score_delta_stopping_reason = "smallest score delta"
                # If we know to die on this move, stop exploring
                # if smallest_predicted_score_delta <= -1.0: # TODO magic number, should be passed in or better learnt.
                #     continue  # no need to continue evaluating (optimisation) this action, as we've stored it as current
                    # worse, and would rather not explore beyond

            if predicted_score_delta > biggest_predicted_score_delta or (predicted_score_delta == biggest_predicted_score_delta and len(new_planned_actions) < len(biggest_predicted_score_delta_actions) ):
                biggest_predicted_score_delta_actions = copy.deepcopy(new_planned_actions)
                biggest_predicted_score_delta = predicted_score_delta
                biggest_predicted_score_delta_stopping_reason = "biggest score delta"
                if evaluation_count_at_which_reward_found == -1:
                    evaluation_count_at_which_reward_found = end_situation_evaluation_count

            if new_AIRIS_confidence <= 1.0 and _is_lower_airis_confidence(new_AIRIS_confidence, lowest_AIRIS_confidence, new_planned_actions,
                                          lowest_conf_actions):  # lower or equal confidence and fewer actions
                lowest_conf_actions = new_planned_actions
                lowest_AIRIS_confidence = new_AIRIS_confidence
                lowest_conf_predicted_score_delta = predicted_score_delta
                lowest_conf_stopping_reason = "lower conf"
                if new_AIRIS_confidence < 1.0 and (evaluation_count_at_which_lower_AIRIS_confidence_found == -1):
                    # only recored the first lower than zero time step
                    evaluation_count_at_which_lower_AIRIS_confidence_found = end_situation_evaluation_count

            if _is_max_airis_confidence(new_AIRIS_confidence, new_planned_actions,
                                          max_conf_actions):  # max confidence and more actions
                max_conf_actions = new_planned_actions

            if _is_older_age(new_oldest_age, oldest_age, new_planned_actions, oldest_age_actions):
                oldest_age_actions = new_planned_actions
                oldest_age = new_oldest_age
                oldest_age_predicted_score_delta = predicted_score_delta
                oldest_age_stopping_reason = "is older"
                if evaluation_count_at_which_older_found == -1: # only set once
                    evaluation_count_at_which_older_found = end_situation_evaluation_count

            if world_state not in encountered_rc:
                encountered_rc[world_state] = set()
                if new_planned_actions_rc_delta in encountered_rc[world_state]:
                    if gather_trace_info:
                        dead_plan_list = copy.deepcopy(new_planned_actions)
                        t_stopping_reason = "hash code and xy delta seen before"
                        dead_plans.append((new_planned_actions_rc_delta, t_stopping_reason, dead_plan_list))
                        temp_stop_reason_rc[end_rc_location[0]][end_rc_location[1]].append(t_stopping_reason)
                        temp_stop_reason_rc[end_rc_location[0]][end_rc_location[1]] = list(
                            set(temp_stop_reason_rc[end_rc_location[0]][end_rc_location[1]]))
                        trace_string += "  new_planned_actions_rc_delta in encountered_rc[world_state]" + "\n"
                    continue # no need to continue evaluating (optimisation) this action
                else:
                    encountered_rc[world_state].add(new_planned_actions_rc_delta)

            # if (is_no_board_or_agent_state_change):  # no effect (e.g. hit a wall ) AND no change in score, keys etc
            #     # if we are wrong about this, unit we attempt this and get more info, so this heuristic may be harmful
            #     if gather_trace_info:
            #         dead_plan_list = copy.deepcopy(new_planned_actions)
            #         t_stopping_reason = "action triggered no change (i.e. hit wall)"
            #         dead_plans.append((new_planned_actions_rc_delta, t_stopping_reason, dead_plan_list))
            #         trace_string += "  "+t_stopping_reason + "\n"
            #     continue  # no need to continue evaluating on this path (optimisation)

            if (new_AIRIS_confidence == float("inf")):
                # something bad happens, avoid. This used to be set if reward for step was -ve. however many
                # environments have -ve reward in usual circumstances, ideally we should be agnostic to
                # reward sign or scale.
                # NOTE this code now unlikely/impossible to trigger
                if gather_trace_info:
                    t_stopping_reason = "something bad happens (-ve score)"
                    dead_plan_list = copy.deepcopy(new_planned_actions)
                    dead_plans.append((new_planned_actions_rc_delta, t_stopping_reason, dead_plan_list))
                    trace_string += "  "+t_stopping_reason + "\n"
                continue  # no need to continue evaluating (optimisation) this action

            if new_AIRIS_confidence >= continue_planning_threshold and not is_off_map_edge:
                # calc value deltas together
                agent_values = list(copy.deepcopy(current_agent_values))
                for i, v in enumerate(agent_values_delta):
                    if i < len(agent_values):
                        agent_values[i] += v
                if starting_situations_evaluated < max_queue_length:
                    # add this to the queue to have extra steps added (confidence of 1 means certain, so keep planning)
                    queue.append((predicted_world, agent_values, new_planned_actions, depth + 1, stopping_reason))
                else:
                    if gather_trace_info:
                        dead_plan_list = copy.deepcopy(new_planned_actions)
                        t_stopping_reason = "No longer adding to queue"
                        trace_string += "  " + t_stopping_reason + "\n"
                        dead_plans.append((new_planned_actions_rc_delta, t_stopping_reason, dead_plan_list))

            else: # confidence dropped, or we are off the board do not search further
                # do not add this result to the queue, so it stops being explored further
                if gather_trace_info:
                    dead_plan_list = copy.deepcopy(new_planned_actions)
                    t_stopping_reason = "AIRIS confidence dropped below 1.0"
                    dead_plans.append((new_planned_actions_rc_delta, t_stopping_reason, dead_plan_list))
                    trace_string += "  "+t_stopping_reason + "\n"

            end_situation_evaluation_count += 1
            if end_situation_evaluation_count % 50 == 0 and end_situation_evaluation_count > 0:
                print("DEBUG _plan() end_situation_evaluation_count=",end_situation_evaluation_count,"len(queue)=",len(queue),"starting_situations_evaluated=",starting_situations_evaluated, str(new_planned_actions))
            trace_string += "end_situation_evaluation_count=" + str(end_situation_evaluation_count) + "\n"

            if new_AIRIS_confidence == float("-inf") and predicted_score_delta <= 0.0:
                print("logic error REF342 REF160")

            if short_curcuit_planning:
                if (( evaluation_count_at_which_reward_found > -1 and biggest_predicted_score_delta > 0.0 ) and
                    # as the confidence in dynamics increases search further
                        ((evaluation_count_at_which_lower_AIRIS_confidence_found > -1 and new_AIRIS_confidence < 0.5 and end_situation_evaluation_count > (len(actions)*1) ) or
                    (evaluation_count_at_which_lower_AIRIS_confidence_found > -1 and new_AIRIS_confidence < 0.6 and end_situation_evaluation_count > (len(actions) * 3)) or
                    (evaluation_count_at_which_lower_AIRIS_confidence_found > -1 and new_AIRIS_confidence < 0.7 and end_situation_evaluation_count > (len(actions) * 9)))
                        and
                    (evaluation_count_at_which_older_found > -1 and oldest_age > 1)):
                    print("INFO short circuiting search as 3 of 3 major conditions found.")
                    queue = collections.deque([])
                    break

    print("INFO _plan() len(queue) at completion=", len(queue), "biggest_score_action_length=",len(biggest_predicted_score_delta_actions),
          "starting_situations_evaluated=",starting_situations_evaluated,
          "number of times _predict() called=",predict_next_world_state_call_count
          )

    planning_statistics = {}
    planning_statistics["plan.evaluation_count"] = end_situation_evaluation_count
    planning_statistics["plan.total_items_placed_on_queue"] = starting_situations_evaluated

    max_evaluation_count = max([evaluation_count_at_which_reward_found,evaluation_count_at_which_lower_AIRIS_confidence_found,evaluation_count_at_which_older_found])

    planning_statistics["plan.short_circuit_advantage"] = max(0,(end_situation_evaluation_count-max_evaluation_count))/(end_situation_evaluation_count +1)
    planning_statistics["plan.queue_at_completion"] = len(queue)
    planning_statistics["plan.biggest_score_action_length"] = len(biggest_predicted_score_delta_actions)
    planning_statistics["plan.evaluation_count_at_which_reward_found"] = evaluation_count_at_which_reward_found
    planning_statistics["plan.evaluation_count_at_which_lower_AIRIS_confidence_found"] = evaluation_count_at_which_lower_AIRIS_confidence_found
    planning_statistics["plan.evaluation_count_at_which_older_found"] = evaluation_count_at_which_older_found
    planning_statistics["plan.predict_next_world_state_call_count_during_plan"] = predict_next_world_state_call_count
    planning_statistics["plan.lowest_AIRIS_confidence"] = lowest_AIRIS_confidence

    if gather_trace_info:
        trace_string += json.dumps(planning_statistics)
        with open(os.path.expanduser("./data/temp.txt"),"w") as f:
            f.writelines(trace_string)

    queue = None

    return (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_predicted_score_delta, lowest_conf_stopping_reason,
            oldest_age_actions, oldest_age, oldest_age_predicted_score_delta, oldest_age_stopping_reason,
            biggest_predicted_score_delta_actions, biggest_predicted_score_delta, biggest_predicted_score_delta_stopping_reason,
            smallest_predicted_score_delta_actions, smallest_predicted_score_delta, smallest_predicted_score_delta_stopping_reason,
            planning_statistics
            )


def _is_lower_airis_confidence(new_score, best_score, new_actions, best_actions):
    return (new_score < best_score or
            (new_score == best_score and len(new_actions) < len(best_actions)))

def _is_max_airis_confidence(new_score, new_actions, best_actions):
    # 100% confident, and longer
    return (new_score == 1.0 and len(new_actions) > len(best_actions))


def _is_older_age(new_age, oldest_age, new_actions, best_actions):
    """
    Ages are the difference in the time counter. 0 is now, 1 is 1 time step ago, -inf is the start of time.
    @param new_age:
    @param oldest_age:
    @param new_actions:
    @param best_actions:
    @return:
    """
    return (new_age > oldest_age or
            (new_age == oldest_age and len(new_actions) < len(best_actions)))


def _print_score(score):
    """
    Print score value taking its semantics regarding its value range semantics for planning into account

    @param score:
    @return:
    """
    if 0.0 <= score <= 1.0:
        print("certainty:", score)
    else:
        print("desired: True")


def nacev3_get_next_action(
        time_counter,
        focus_set,
        rule_evidence,
        rc_locations,
        internal_world_model: Type[NPWorld],
        rules_in,
        external_ground_truth_world_model: Type[NPWorld],
        print_debug_info,
        stayed_the_same: bool,
        agent: Type[Agent],
        full_action_list: list,  # used during babling
        agent_indication_raw_value_list: list, # embedded value
        max_num_actions: int, # maximum number of actions in plan
        max_queue_length: int # planning queue depth
):
    """
    Determine the next action for the NACE agent based on current observations and rules.

    Steps:
    1. Limit the agent's field of view (partial observability)
    2. Refine rules based on evidence
    3. Plan forward to calculate favored actions and scores

    :param time_counter: Current time
    :param focus_set: Used in subroutine
    :param rule_evidence: Evidence for rules
    :param rc_locations: Tuple(r, c) list of agent's locations (0,0 is top left)
    :param internal_world_model: Agent's view of the world (mutated)
    :param rules_in: Input rules
    :param external_ground_truth_world_model: Current world state (mutated)
    :param  print_debug_info,
    :param stayed_the_same: bool,
    :param agent,
    :return: Tuple(plan, action, rules_excluded, behavior)


    Notes
        The number of state values that the agent stores, and the number of value delta in the rules must match.
    """

    unittest_code_str = ""

    # Step 1: Update agent's field of view
    if external_ground_truth_world_model is not None:
        modified_count, _ = internal_world_model.update_world_from_ground_truth(
            time_counter,
            external_ground_truth_world_model,
            rc_locations=rc_locations,
            agent_indication_raw_value_list=agent_indication_raw_value_list
        )

    # Step 2: Refine rules based on evidence
    active_rules, rules_excluded = Hypothesis_BestSelection(
        rules=copy.deepcopy(rules_in),
        rules_excluded=set(),
        rule_evidence=rule_evidence,
        include_random_rules=stayed_the_same)
    if agent.get_score() >= 1.0:
        pass

    # Step 3: Plan forward
    (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_predicted_score_delta, lowest_conf_stopping_reason,
     oldest_age_actions, oldest_age, oldest_age_predicted_score_delta, oldest_age_stopping_reason,
     biggest_predicted_score_delta_actions, biggest_predicted_score_delta, biggest_predicted_score_delta_stopping_reason,
     smallest_predicted_score_delta_actions, smallest_predicted_score_delta, smallest_predicted_score_delta_stopping_reason,
     statistics) = (
        _plan(
            internal_world_model,
            active_rules,
            copy.deepcopy(full_action_list),
            focus_set,
            agent=agent,
            custom_goal=None,
            max_num_actions= max_num_actions,
            max_queue_length= max_queue_length,
            rules_excluded=rules_excluded
        ))

    # Determine available actions
    actions_to_pick_from = _get_remaining_actions(active_rules, full_action_list)
    if len(actions_to_pick_from) == 0:
        all_actions_tried = True
        actions_to_pick_from = copy.deepcopy(full_action_list) # set back to the bigger list so one can be picked at random
    else:
        all_actions_tried = False

    # if len(full_action_list) != 3:
    #     print("login error REF515")

    world_and_agent_hc = xxhash.xxh32(bytes(internal_world_model.board.data) + bytes(agent.get_values_for_precondition())).intdigest()  # should be repeatable between restarts.

    # Determine behavior and action
    behavior, whole_plan = _determine_behavior_and_action(
        lowest_AIRIS_confidence, lowest_conf_actions, lowest_conf_predicted_score_delta, lowest_conf_stopping_reason,
        oldest_age_actions, oldest_age, oldest_age_predicted_score_delta, oldest_age_stopping_reason,
        biggest_predicted_score_delta_actions, biggest_predicted_score_delta,
        biggest_predicted_score_delta_stopping_reason,
        smallest_predicted_score_delta_actions, smallest_predicted_score_delta,
        smallest_predicted_score_delta_stopping_reason,
        all_actions_tried, # True if all possible actions were in the set of applicable rules
        available_actions=actions_to_pick_from,
        full_action_list=full_action_list,
        world_and_agent_hc=world_and_agent_hc,
        print_debug_info=print_debug_info
    )

    if print_debug_info:
        # roll forward the world according to the plan
        predicted_world = copy.deepcopy(internal_world_model)
        planagent = copy.deepcopy(agent)
        for i in range(0, len(whole_plan)):
            predicted_world, planagent, _, __, ___, ____ = _predict_next_world_state(
                focus_set,
                copy.deepcopy(predicted_world), whole_plan[i], active_rules, planagent
            )

        internal_world_model.multiworld_print([{"Caption": f"Internal\nBefore plan:",
                                                "World": internal_world_model,
                                                "Color": nace.color_codes.color_code_white_on_black},
                                               {"Caption": f"At end of plan:\n"+str(prettyprint_all_actions(whole_plan)),
                                                "World": predicted_world,
                                                "Color": nace.color_codes.color_code_white_on_red},
                                               ]
                                              )

        from nace.test_utilities import convert_focus_set_to_char_mapping, convert_rules_to_char_or_int_mappings
        char_focus_set =  convert_focus_set_to_char_mapping(focus_set, internal_world_model)
        char_active_rules, _2 = convert_rules_to_char_or_int_mappings(active_rules, internal_world_model)

        # char_rule_evidence = {}
        # for rule in rule_evidence.keys():
        #     t_char_rules, t_encoded_rules = convert_rules_to_char_or_int_mappings([rule], internal_world_model)
        #     char_rule_evidence[t_encoded_rules[0]] = rule_evidence[rule]

        char_rule_evidence = convert_rule_evidence_to_char_or_int_mappings(rule_evidence, internal_world_model)

        char_world = internal_world_model.debug_board
        unittest_code_str = "world_str_list = "+str(char_world.split("\n")) +"\n"
        unittest_code_str += "focus_set = "+str(char_focus_set)+"\n"
        unittest_code_str += "active_rules = "+str(char_active_rules) + " # subset of rule_evidence \n"
        unittest_code_str += "rule_evidence = "+str(char_rule_evidence) + "\n"

        unittest_code_str += "world_state_values = " +  str(internal_world_model.get_internal_state()) + "\n"

        # (rc_loc=(3,1), score=-696.0, values_exc_score=[])
        unittest_code_str += "agent = nace.agent_module.Agent(rc_loc=" + str(agent.get_rc_loc()) +", score=" + str(agent.get_score()) +", terminated=" + str(agent.get_terminated()) +", values_excluding_prefix=" + str(agent.get_values_exc_prefix()) + " )\n"
        unittest_code_str += "actions = " +str(full_action_list) +"\n"
        unittest_code_str += "behavior_returned = '" + behavior +"'\n" # US spelling no 'u'
        unittest_code_str += "whole_plan_returned = " + str(whole_plan) +"\n"


        # HINT: copy the value of code_str if you want to make a unit test based on the current state.
        print("")

    return whole_plan, rules_excluded, behavior, statistics, unittest_code_str


def _get_remaining_actions(rules, action_list):
    result = copy.deepcopy(action_list)
    for rule in rules:
        precondition, _ = rule
        action = precondition[0]
        if action in result:
            result.remove(action)
    return result


def _determine_behavior_and_action_v0(
                                    # airis_score,
        # favored_actions, favored_actions_for_revisit, oldest_age,
        #                                all_actions_tried: bool, board_value_transition: tuple,
        #                                print_debug_info: bool = False,
                                   lowest_AIRIS_conf,
                                   lowest_AIRIS_conf_actions,
                                   lowest_conf_predicted_score_delta:float,
                                   lowest_AIRIS_conf_stopping_reason: str,
                                   oldest_actions,
                                   oldest_age,
                                   oldest_age_predicted_score_delta:float,
                                   oldest_age_stopping_reason: str,
                                   biggest_predicted_score_delta_actions:list,
                                   biggest_predicted_score_delta:float,
                                   biggest_predicted_score_delta_stopping_reason:str,
                                   smallest_predicted_score_delta_actions:list,
                                   smallest_predicted_score_delta:float,
                                   smallest_predicted_score_delta_stopping_reason:str,
                                   all_actions_tried: bool,
                                   available_actions: list,
                                   full_action_list: list,
                                   world_and_agent_hc,
                                   print_debug_info: bool = False
                                      ):
    """

    Indeterministic if all_actions_tried == FALSE

    @param airis_score: == lowest_AIRIS_conf
    @param favored_actions: lowest_AIRIS_conf_actions or biggest_predicted_score_delta_actions
    @param favored_actions_for_revisit: == oldest_actions
    @param oldest_age: oldest observed age (smaller == older)
    @param all_actions_tried: True if all possible actions were in the set of applicable rules
    @param babbling_rates: dict of rates e.g. : {'curiosity': 0.5, 'exploit': 1.0, 'explore': 0.5}
    @param board_value_transition: tuple ( char, char) from to values of a board transition.
    @param print_debug_info:
    @return:
    """
    plan = []

    favoured_actions = lowest_AIRIS_conf_actions
    # favoured_actions = biggest_predicted_score_delta_actions

    favoured_actions_for_revisit = oldest_actions

    explore_curiosity_modulator = (
        1.0 if all_actions_tried else 0.5
    )  # 1.0 if all_actions_tried and world_is_novel else 0.5
    curiosity_babble_rate, exploit_babble_rate, explore_babble_rate = (
        explore_curiosity_modulator,
        1.0,
        explore_curiosity_modulator,
    )
    exploit_babble = random.random() > (
        exploit_babble_rate
        if lowest_AIRIS_conf == float("-inf")
        else curiosity_babble_rate
    )  # babbling when wanting to achieve something or curious about something, and babbling when exploring:
    explore_babble = (
            random.random() > explore_babble_rate
    )  # since it might not know yet about all ops, exploring then can be limited
    if lowest_AIRIS_conf >= 0.9 or exploit_babble or len(favoured_actions) == 0:
        if (
                not exploit_babble
                and not explore_babble
                and oldest_age > 0.0
                and lowest_AIRIS_conf == 1.0
                and len(favoured_actions_for_revisit) != 0
        ):
            behavior = "EXPLORE"
            # print(
            #     behavior,
            #     Prettyprint_Plan(favoured_actions_for_revisit),
            #     "age:",
            #     oldest_age,
            # )
            action = favoured_actions_for_revisit[0]
            plan = favoured_actions_for_revisit
        else:
            behavior = "BABBLE"
            action = random.choice(available_actions)  # motorbabbling
    else:
        behavior = "ACHIEVE" if lowest_AIRIS_conf == float("-inf") else "CURIOUS"
        # print(behavior, Prettyprint_Plan(favoured_actions), end=" ")
        # NACE_PrintScore(airis_score)
        action = favoured_actions[0]
        plan = favoured_actions

    if print_debug_info:
        print("behavior", behavior,
              "airis_score", lowest_AIRIS_conf,
              "favoured_actions", favoured_actions,
              "favoured_actions_for_revisit", favoured_actions_for_revisit, "oldest_age>0", (oldest_age > 0.0)
              )
    whole_plan = [action] + plan
    return behavior, whole_plan

def _determine_behavior_and_action(lowest_AIRIS_conf,
                                   lowest_AIRIS_conf_actions,
                                   lowest_conf_predicted_score_delta:float,
                                   lowest_AIRIS_conf_stopping_reason: str,
                                   oldest_actions,
                                   oldest_age,
                                   oldest_age_predicted_score_delta:float,
                                   oldest_age_stopping_reason: str,
                                   biggest_predicted_score_delta_actions:list,
                                   biggest_predicted_score_delta:float,
                                   biggest_predicted_score_delta_stopping_reason:str,
                                   smallest_predicted_score_delta_actions:list,
                                   smallest_predicted_score_delta:float,
                                   smallest_predicted_score_delta_stopping_reason:str,
                                   all_actions_tried: bool,
                                   available_actions: list,
                                   full_action_list: list,
                                   world_and_agent_hc,
                                   print_debug_info: bool = False):
    return _determine_behavior_and_action_v2(lowest_AIRIS_conf,
                                   lowest_AIRIS_conf_actions,
                                   lowest_conf_predicted_score_delta,
                                   lowest_AIRIS_conf_stopping_reason,
                                   oldest_actions,
                                   oldest_age,
                                   oldest_age_predicted_score_delta,
                                   oldest_age_stopping_reason,
                                   biggest_predicted_score_delta_actions,
                                   biggest_predicted_score_delta,
                                   biggest_predicted_score_delta_stopping_reason,
                                   smallest_predicted_score_delta_actions,
                                   smallest_predicted_score_delta,
                                   smallest_predicted_score_delta_stopping_reason,
                                   all_actions_tried,
                                   available_actions,
                                   full_action_list,
                                             world_and_agent_hc,
                                   print_debug_info)




def _determine_behavior_and_action_v2(lowest_AIRIS_conf,
                                   lowest_AIRIS_conf_actions,
                                   lowest_conf_predicted_score_delta:float,
                                   lowest_AIRIS_conf_stopping_reason: str,
                                   oldest_actions,
                                   oldest_age,
                                   oldest_age_predicted_score_delta:float,
                                   oldest_age_stopping_reason: str,
                                   biggest_predicted_score_delta_actions:list,
                                   biggest_predicted_score_delta:float,
                                   biggest_predicted_score_delta_stopping_reason:str,
                                   smallest_predicted_score_delta_actions:list,
                                   smallest_predicted_score_delta:float,
                                   smallest_predicted_score_delta_stopping_reason:str,
                                   all_actions_tried: bool,
                                   available_actions: list,
                                   full_action_list: list,
                                   world_and_agent_hc,
                                   print_debug_info: bool = False):
    """

    Nondeterministic if all_actions_tried == FALSE

    Open questions:

    1) Early on in training lowest_AIRIS_conf is high, the system thinks it knows the dynamics fully, yet it doesn't.
    Could this be improved with a familiarity ratting? Is there anything in the literature? We are in an unfamilar situation, proceed with caution?

    2) If a system has a certain amount of stochastic behavior it means the lowest_AIRIS_conf never goes to 1.0, perhaps
    it hovers at 0.33, will be never attempt to achieve?

    3) is it logical to remember what was last done in this situation? Is this over-reliance on heuristics?
    Leading to suboptimal decision-making due to heuristic application?



    EXPLORE  - Refresh old knowledge
    CURIOUS - Go for part of world most uncertain about
    ACHIEVE  - Increase reward
    BABBLE   - Random action


    @param lowest_AIRIS_conf:
    @param lowest_AIRIS_conf_actions:
    @param oldest_actions:
    @param oldest_age: oldest observed age (smaller == older)
    @param all_actions_tried: True if all possible actions were in the set of applicable rules
    @param babbling_rates: dict of rates e.g. : {'curiosity': 0.5, 'exploit': 1.0, 'explore': 0.5}
    @param print_debug_info:
    @return:
    """

    # if all_actions_tried evaluates to False else TRUE randomly 33% of time
    babble_during_explore = False if all_actions_tried else random.random() < 0.33
    explore_during_curious = random.random() < 0.5

    if biggest_predicted_score_delta > 0.0: # TODO: Issue, we will never achieve something with a 0 reward.
        behavior = "ACHIEVE"
        whole_plan = biggest_predicted_score_delta_actions
        action = whole_plan[0]
        reason = "Biggest Score Delta"
    elif lowest_conf_predicted_score_delta > 0.0:
        behavior = "ACHIEVE"
        whole_plan = lowest_AIRIS_conf_actions
        action = whole_plan[0]
        reason = "Score via Lowest AIRIS conf."
    elif oldest_age_predicted_score_delta > 0.0:
        behavior = "EXPLORE"
        whole_plan = oldest_actions
        action = whole_plan[0]
        reason = "Score via oldest age"
    else:
        if (lowest_AIRIS_conf >= 0.90 # we think we model the world well
                or babble_during_explore     # random
                or len(lowest_AIRIS_conf_actions) == 0 # we think we know the world well
        ):
            # EXPLORE or BABBLE
            if (oldest_age > 0.0 and           # we have an old knowledge to recheck
                len(oldest_actions) != 0 and   # we have an old knowledge to recheck
                lowest_AIRIS_conf == 1.0 and   # we think we know the dynamics fully
                not babble_during_explore      # we are not taking a random action
            ):
                behavior = "EXPLORE"
                reason = "OLDEST_CELLS"
                whole_plan = oldest_actions
                action = whole_plan[0]
            else:
                behavior = "BABBLE"
                if len(available_actions) > 0:
                    action = _choose_babble_action(available_actions=available_actions, world_and_agent_hc=world_and_agent_hc)
                else:
                    print("WARN - no actions to pick from, using full list", full_action_list)
                    action = _choose_babble_action(available_actions=full_action_list, world_and_agent_hc=world_and_agent_hc)
                reason = "RANDOM_ACTION"
                whole_plan = [action]
        else:
            # lowest_AIRIS_conf must be < 0.90
            # the oscillation path on world 2 runs through here always selecting lowest_AIRIS_conf_actions
            if explore_during_curious:
                behavior = "EXPLORE"
                reason = "OLDEST_CELLS"
                whole_plan = oldest_actions
                action = whole_plan[0]
            else:
                behavior = "CURIOUS"
                whole_plan = lowest_AIRIS_conf_actions
                action = whole_plan[0]
                reason = "Lowest AIRIS conf."

    if print_debug_info:
        print("DEBUG _determine_behavior_and_action()", "airis_score=", lowest_AIRIS_conf, "lowest_AIRIS_conf_actions=", nace.prettyprint.prettyprint_all_actions(lowest_AIRIS_conf_actions) )
        print("DEBUG _determine_behavior_and_action()", "oldest_age= ", (oldest_age), "oldest_actions=", nace.prettyprint.prettyprint_all_actions(oldest_actions))
        print("DEBUG _determine_behavior_and_action()", "biggest_predicted_score_delta=", biggest_predicted_score_delta,
              "biggest_predicted_score_delta_actions=",
              nace.prettyprint.prettyprint_all_actions(biggest_predicted_score_delta_actions)
              )

    print("INFO _determine_behavior_and_action()", behavior, nace.prettyprint.prettyprint_all_actions([action]),
          "Reason=", reason,
          "Lowest_AIRIS_Conf=", lowest_AIRIS_conf,
          "rest_of_plan=", nace.prettyprint.prettyprint_all_actions(whole_plan),
          "oldest_age=", oldest_age,
          "Lowest_age_reason=", lowest_AIRIS_conf_stopping_reason,
          "oldest_age_stopping_reason=", oldest_age_stopping_reason)
    return behavior, whole_plan


def _choose_babble_action(available_actions, world_and_agent_hc=0, use_random=False):
    if len(available_actions) == 0:
        print("logic error REF 569")

    if use_random:
        return random.choice(available_actions)
    else:
        # be deterministic, i.e. don't do the same as last time, return the next action in the possible actions (will be problematic in continious action spaces)
        # improvement, once the state cache becomes a certain size, switch to random.
        global last_action_in_situation
        index = last_action_in_situation[world_and_agent_hc] % len(available_actions)
        last_action_in_situation[world_and_agent_hc] += 1
        if last_action_in_situation[world_and_agent_hc] > 1:
            print("DEBUG REF842 ")
        return available_actions[index]


def _create_explanation_graphs():
    """
    Hold some things constant, then produce graphs to try an explain how airis score based on synthetic inputs
    e.g.: all_actions_tried, age etc relate to each other
    @return:
    """
    # Calculate babbling rates
    all_results = {}
    num_repeats = 100
    number_airis_bins = 20
    description = ""

    for oldest_age in [10]:
        for all_actions_tried in [True, False]:
            results = []
            for i in range(number_airis_bins + 1):
                airis_score = i / float(number_airis_bins)
                action_type_counts = collections.defaultdict(int)
                behavior_counts = collections.defaultdict(int)

                for run in range(num_repeats):
                    # Determine behavior and action
                    behavior, whole_plan = _determine_behavior_and_action(
                        airis_score,
                        lowest_AIRIS_conf_actions=["FA[0]", "FA[1]"],
                        oldest_actions=["FAFR[0]", "FAFR[1]"],
                        oldest_age=oldest_age,
                        available_actions=["FA[0]", "FA[1]", "FAFR[0]", "FAFR[1]"],
                        full_action_list=["FA[0]", "FA[1]", "FAFR[0]", "FAFR[1]"],
                        all_actions_tried=all_actions_tried,
                    )
                    action = whole_plan[0]
                    behavior_counts[behavior] += 1
                    if action.find("FAFR[") > -1:
                        action_type_counts["favored_actions_for_revisit"] += 1
                    elif action.find("FA[") > -1:
                        action_type_counts["favored_actions"] += 1

                description = "oldest_age:" + str(oldest_age) + " all_actions_tried:" + str(all_actions_tried)
                results.append({"airis_score": airis_score,
                                "CURIOUS": behavior_counts["CURIOUS"],
                                "ACHIEVE": behavior_counts["ACHIEVE"],
                                "BABBLE": behavior_counts["BABBLE"],
                                "EXPLORE": behavior_counts["EXPLORE"],
                                "favored_actions_for_revisit": action_type_counts["favored_actions_for_revisit"],
                                "favored_actions": action_type_counts["favored_actions"],
                                "description": description,
                                'all_actions_tried': all_actions_tried,
                                'oldest_age': oldest_age
                                })
            print("________________ results:")
            print(results)
            all_results[description] = results
    print("________________ all results:")
    print(all_results)
    # return plan, action, rules_excluded, behavior


def _match_hypotheses(focus_set:dict, world:Type[NPWorld], action:any, rules:set, old_agent: Type[Agent], brute_force_focus_next_step:bool):
    """
    Get a map of the grid locations and find the rule with the greatest 'Match Quotient' at each location.
    These are the rules that will actually be applied to the world, and the locations they will be applied in.

    focus_set: seems to only have keys for elements that entered the viewport one at a time,
               i.e. excludes walls or free space.

    This function identifies locations on the grid that are relevant based on
    recent updates and the focus set. It then evaluates how well each rule's
    preconditions match the current state at those locations, assigning a
    "Match Quotient" (Q) for rule r, and cell c. based on the proportion of matched preconditions.

    Note: this routine was called '_MatchHypotheses' in the original code.

    From the paper:
    for each cell (c) we utilize only the rule (r) with Q(r,c) = 1 and maximum fexp(r), meaning the rule preconditions
    not only match perfectly to the given state and the action that has been considered, but also has the
    highest truth expectation among these rule candidates.

    Note: rules are expected to already be filtered for those with the greatest truth expectation

    Problem - there's a q on the map. its position will be empty cause no rules deal with a q. hmmm.


    Args:
        focus_set: A dictionary representing the currently focused elements.
                   Keys are element values, values are counts seen inside viewport, when they appeared 1 at a time.
        world: The current state of the world.
        action: The action to be taken.
        rules: The set of all known rules. Each rule is expected to be a tuple of (precondition, consequence).
               Precondition format: (action, [agent_state_values], (y_rel, x_rel, required_state), ...)
        old_agent: The agent's state in the previous time step.

    Returns:
        A tuple containing:
        - positionscores: A dictionary where keys are (y, x) coordinates and
                         values are tuples of (scores, highscore, highscorerule).
                         'scores' is a dictionary mapping rules to their Match Quotient.
                         'highscore' is the highest Match Quotient at that location.
                         'highscorerule' is the rule with the highest Match Quotient.
        - highesthighscore: The highest Match Quotient found across all locations.


    """


    position_scores = dict([])
    highest_highscore = 0.0
    positions = set([])

    # record locations on the board, whose value is in the focus_set values.
    # Add any surrounding locations from the location deltas in the pre-conditions of any rules.
    height, width = world.get_height_width()
    if brute_force_focus_next_step:
        for y in range(height): # for y,x in rc_locations:
            for x in range(width):
                positions.add((y, x))
    else:
        # attempt to limit locations evaluated to around the focus set
        for y in range(height): # for y,x in rc_locations:
            for x in range(width):
                if world.board[y, x].item() in focus_set:
                    positions.add((y, x))
                    for rule in rules:
                        if action == rule[0][0]:
                            (precondition, consequence) = rule
                            action_and_preconditions = list(precondition)
                            for y_rel, x_rel, requiredstate in action_and_preconditions[
                                                               2:
                                                               ]:
                                positions.add((y + y_rel, x + x_rel))

    # randomised_positions = list(positions)
    # random.shuffle(randomised_positions)


    # find which rules
    for y,x in positions:
        scores = dict([])
        position_scores[(y, x)] = scores
        highscore = 0.0
        highscorerule = None
        rule = None
        for rule in rules:
            (precondition, consequence) = rule
            action_and_preconditions = list(precondition)
            values_excl_score = action_and_preconditions[1] # preconditions exclude the score
            if action_and_preconditions[0] == action:                 # check the ACTION
                scores[rule] = 0.0
            else:
                continue # wrong action - skip to next rule
            if len(values_excl_score) != len(old_agent.get_values_for_precondition()):
                continue  # rule has wrong number of agent values in it - skip to next rule

            CONTINUE = False

            precontions_count = 0
            for i in range(len(values_excl_score)):                             # check the AGENT VALUES against precon
                if len(values_excl_score) != len(old_agent.get_values_for_precondition()):
                    print("WARN Length mis-match REF988 values_excl_score=", values_excl_score,"old_agent.get_values_exc_score()", old_agent.get_values_for_precondition())
                precontions_count += 1
                if  i < len(old_agent.get_values_for_precondition()) and values_excl_score[i] == old_agent.get_values_for_precondition()[
                    i]:  # LHS should not include score, as it is not a state (and should not be) that we condition on)
                    scores[rule] += 1.0  # increment the number of matched preconditions

            for y_rel, x_rel, requiredstate in action_and_preconditions[2:]:# check all precon actually ON BOARD
                if (
                        y + y_rel >= height
                        or y + y_rel < 0
                        or x + x_rel >= width
                        or x + x_rel < 0
                ):
                    CONTINUE = True # if any not on board, skip
                    break
            if CONTINUE:
                continue
            for y_rel, x_rel, requiredstate in action_and_preconditions[
                                               2:]:  # count number of matching preconditions excl action and reward
                    precontions_count += 1
                    if world.board[y + y_rel, x + x_rel] == requiredstate:
                        scores[rule] += 1.0  # increment the number of matched preconditions

            # Q(r,c) - Match Quotient (-2 as it excludes the action and RL reward, but includeds all the agent state values )
            scores[rule] /= precontions_count

            # check the rule has an effect in the 0,0 location or on agent state
            zero_zero_precond = [(y_rel, x_rel, requiredstate) for y_rel, x_rel, requiredstate in
                                 action_and_preconditions[2:] if y_rel == 0 and x_rel == 0]
            has_board_effect = zero_zero_precond[0][2] != consequence[2]
            has_agent_effect = sum([abs(delta) for delta in consequence[3]]) != 0.0

            if scores[rule] > 0.0 and (
                    scores[rule] > highscore
                    # or (
                    #         scores[rule] == highscore
                    #         and highscorerule is not None
                    #         and len(rule[0]) > len(highscorerule[0])
                    # )
                    or (
                            scores[rule] == highscore
                            and (has_board_effect or has_agent_effect)
                            and len(rule[0]) >= len(highscorerule[0])
                    )
            ):
                highscore = scores.get(rule, 0.0)
                highscorerule = rule

        # TODO delete the next block of code - which only creates a human readable version of the rule
        pp_highscore_rule = ""
        if highscorerule is not None:
            try:
                _, char_rules = nace.test_utilities.convert_rules_to_char_or_int_mappings(rules=[highscorerule], world=world)
                char_rule = char_rules[0]
                pp_highscore_rule = nace.prettyprint.prettyprint_rule(rule_evidence={char_rule: (1, 1)},
                                                                      Hypothesis_TruthValue=Hypothesis_TruthValue,
                                                                      rule=char_rule, val_to_char_mappings={},
                                                                      print_evidence=False, print_truth_value=False)
            except Exception as e:
                print("ERROR can not create debugging info."+str(traceback.format_exc()))

        # TODO END of delete code.
        position_scores[(y, x)] = (scores, highscore, highscorerule , pp_highscore_rule)

        if highscore > highest_highscore:
            highest_highscore = highscore
    return (position_scores, highest_highscore)




def _rule_applicable(scores, highscore, highesthighscore, rule):  # called _RuleApplicable in old system
    """
    # Whether a rule is applicable: only if it matches better than not at all, and as well as the best matching rule

    @param scores:
    @param highscore:
    @param highesthighscore:
    @param rule:
    @return:
    """
    if highscore > 0.0 and scores.get(rule, 0.0) == highesthighscore:
        return True
    return False


def _apply_position_match_quotient_scores_to_world_and_agent(
        world,
        agent,
        position_match_quotient_scores,
        highest_match_quotient_highscore,
        action,
        minimum_cell_predict_confidence_threshold,
        custom_goal=None,
    ):
    """
    apply all highest confidence rule for each cell location in that location.
    only rules of the highest confidence will be applied.

    @param world:
    @param agent:
    @param position_match_quotient_scores:
    @param highest_match_quotient_highscore:
    @param action:
    @param minimum_cell_predict_confidence_threshold: only apply a rule to a cell if the confidence is above this value
    @return:
    """
    new_world = copy.deepcopy((world))
    new_agent = copy.deepcopy(agent)
    used_rules_sum_quotient_score = 0
    used_rule_count = 0
    agent_state_increment_counts = [0] * len(new_agent.get_values_inc_prefix())
    debug_rules_applied = []
    for (y, x) in position_match_quotient_scores.keys():
        match_quotient_scores, match_quotient_highscore, rule, pp_rule = position_match_quotient_scores[(y, x)]
        if rule is not None and rule[0][0] == action:
            debug_rule = nace.test_utilities.convert_rules_to_char_or_int_mappings([rule], world) if rule is not None else ""
            if _rule_applicable(match_quotient_scores, match_quotient_highscore, highest_match_quotient_highscore, rule):
                if match_quotient_scores.get(rule, 0.0) > minimum_cell_predict_confidence_threshold:
                    #
                    #
                    # increment the agent state values, and count how many were changed
                    new_agent.accumulate_values_incl_prefix(rule[1][3])  # new agent score should be considered delta (should we call increment_values_including_score?)
                    for i in range(len(rule[1][3])): # count how many times each value is incremented by non zero value
                        if rule[1][3][i] != 0:
                            agent_state_increment_counts[i] += 1
                    # set the value in this cell location
                    new_world.set_embedded_val_rc(y+rule[1][0], x+rule[1][1], rule[1][2], ) # this changes the world value # NOTE effect (r,c) (rule[1][0] and rule[1][1]) are always (0,0) in this impl
                    # gather stats so that confidence can be calculated
                    used_rules_sum_quotient_score += match_quotient_scores.get(rule, 0.0)
                    used_rule_count += 1
                    debug_rules_applied.append( (y, x, debug_rule) )
                    # debugging code - so the map can be viewed. The next line can and should be removed for performnce reasons
                    new_world.debug_board = new_world.board_as_string(
                        agent_indication_embedded_value_list=[] # unknown at this point, rely on enough mapping values being stored
                    )

    new_world.debug_board = new_world.board_as_string(
        agent_indication_embedded_value_list=[] # unknown at this point, rely on enough mapping values being stored
    )

    AIRIS_confidence = (
        used_rules_sum_quotient_score / used_rule_count if used_rule_count > 0 else 1.0 # No rules used, so we have high confidence.
    )

    if (custom_goal and custom_goal(new_world)):
        new_agent.set_score(new_agent.get_score() + 1.0)  # newagent score should be considered as a delta here

    # calculate agent delta values
    agent_value_deltas =  [0]*len(new_agent.get_values_inc_prefix())
    for i in range(len(agent_value_deltas)):
        if agent_state_increment_counts[i] != 0:
            agent_value_deltas[i] = (new_agent.get_values_inc_prefix()[i] - agent.get_values_inc_prefix()[i]) / agent_state_increment_counts[i]
        else:
            agent_value_deltas[i] = (new_agent.get_values_inc_prefix()[i] - agent.get_values_inc_prefix()[
                i])

    return (new_world,
            new_agent,
            AIRIS_confidence,
            None, # unused
            agent_value_deltas,  # delta of all values including score
            agent_value_deltas[0] # score is the first agent value
            )


def _predict_next_world_state(focus_set,
                              world,
                              action,
                              rules,
                              agent,
                              custom_goal=None,
                              brute_force_focus_next_step=False,
                              minimum_cell_predict_confidence_threshold:float=0.0
                              ):  # called NACE_Predict in old system
    """
    Returns the world as predicted after 'action' is applied to 'oldWorld'.
    It does this by applying rules that have been previously learnt.

    How: Apply the move to the predicted world model whereby we use the learned rules to decide how grid elements might
    most likely change.

    From the paper:
    for each cell we utilize only the rule r with Q(r,c) = 1 and maximum fexp(r), meaning the rule preconditions
    not only match perfectly to the given state and the action that has been considered, but also has the
    highest truth expectation among these rule candidates.


    From AIRIS video: https://youtu.be/40W2OmV_rm0?t=371



    :param focus_set: - Note: NOT updated by this routine.
    :param world:
    :param action:
    :param rules:
    :param custom_goal: function that will increase the RL reward score if evalutes to true (takes world as a single param)
    brute_force_next_step: if true evaluates for all cells, not just those derived from focus_set
    minimum_cell_predict_confidence_threshold: only apply a rule to a cell if the confidence is above this value
    :return:
    """

    (position_match_quotient_scores, highest_match_quotient_highscore) = _match_hypotheses(
        focus_set,
        world,
        action,
        rules,
        agent,
        brute_force_focus_next_step=brute_force_focus_next_step # if true use my focus set rather than patricks
    )
    return _apply_position_match_quotient_scores_to_world_and_agent(
        world,
        agent,
        position_match_quotient_scores,
        highest_match_quotient_highscore,
        action,
        minimum_cell_predict_confidence_threshold,
        custom_goal=None)


def _add_to_adjacent_set(adjacent_change_sets: list, newEntry: tuple, MaxCapacity: int, CanCreateNewSet: bool,
                         maximum_distance: int = 1, max_dist_one_dim=True):  # called _AddToAdjacentSet in the old system
    """


    If there are no entries in the adjacent_change_sets create a new one with the new point.
    If the new point if not adjacent to any of the existing sets create a new set containing it.
    If the new point is adjacent to a point in the existing sets, add it to that set if
              there are less than 3 points in it.

    @param adjacent_change_sets:
    @param newEntry:
    @param MaxCapacity:
    @param CanCreateNewSet:
    @param maximum_distance:
    @return:
    """
    (y, x) = newEntry
    AdjacentToAnySet = False
    for consideredSet in adjacent_change_sets:
        consideredSetFrozen = copy.deepcopy(consideredSet)
        for ys, xs in consideredSetFrozen:
            if max_dist_one_dim:
                if abs(y - ys) + abs(x - xs) <= maximum_distance:
                    if len(consideredSet) < MaxCapacity:
                        consideredSet.add(newEntry)
                    AdjacentToAnySet = True
            elif abs(y - ys) <= maximum_distance and abs(x - xs) <= maximum_distance:
                if len(consideredSet) < MaxCapacity:
                    consideredSet.add(newEntry)
                AdjacentToAnySet = True

    if not AdjacentToAnySet and CanCreateNewSet:
        adjacent_change_sets.append({newEntry})


def _is_presently_observed(Time, world, y, x):
    """
    # Whether the grid cell has been observed now (not all have been, due to partial observability)

    NOTE world.get_locations_updated_tminus() can be far more efficient.

    @param Time:
    @param world:
    @param y:
    @param x:
    @return:
    """
    diff = Time - world.times[y][x]
    return diff == 0.0


def _build_change_sets(
        focus_set,
        oldworld,
        action,
        newworld,
        predictedworld,
        object_count_threshold=1,
        agent_rc_location = None
):
    """
    calc value_counts : counts each board value has been seen.

    This routine maintains the 'focus_set' - a list of board values, and the count of times they have changed IFF there
    was only 1 occurrence of the value in the view port.
    in other words: focus set is a set of things that came into the viewport one by one at some stage.

    adjacent_change_sets : sets of 2 to 3 locations that are adjacent to each other in the plane, i.e. {(2,2),(2,3)}
    or {(2,2),(2,1),(2,3)}

    Currently, does not support diagonally adjacent locations.


    @param focus_set:
    @param oldworld:
    @param action:
    @param newworld:
    @param predictedworld:
    @param object_count_threshold:
    @return:
    """
    # Keep track of cell type counts - count of each cell type
    # in world keyed by the chars in the world map
    value_counts = collections.defaultdict(int)
    height, width = oldworld.get_height_width()
    for y in range(height):
        for x in range(width):
            val = oldworld.board[y, x].item()
            value_counts[val] = +1
    # Update focus_set based on unique values and unique changing values.
    # focus_set : keyed by the char in a map location.
    #         Value == the number of time steps this value has been one that has changed (and there was only 1 of them)
    # if the world is huge, is this realistic, or work out from current location till N are found ...
    #
    pass
    # only consider cells that were observed in both newworld and oldworld in the most recent upadate of each,
    # if there is only 1 cell of this type (why?) add this, or increment this in the focus set.
    # Optimisation : Code could be changed to pull this set of locations from the worlds utilizing fast np operations.
    # current_time = newworld.get_newest_time()
    difference_count_checksum =  0

    _a = newworld.get_locations_updated_tminus(0)
    _b = newworld.get_locations_updated_tminus(1)

    recently_observed_rc_locations = _a + _b
    recently_observed_rc_locations = list(set(recently_observed_rc_locations))

    # reduce the set to those changed. This code prevents locations that were unobserved last timestep,
    # but now are (is this intentional) (if not only targets that are now observed should be used?)
    recently_observed_rc_locations = [ (r,c) for (r,c) in recently_observed_rc_locations if oldworld.board[r, c].item() != newworld.board[r, c].item() and oldworld.board[r, c].item() != oldworld.get_unobserved_code() ]

    if len(recently_observed_rc_locations) == 0:
        print("WARN _build_change_sets() No recently updated cells, nothing to learn.")

    for (r,c) in set(recently_observed_rc_locations):
        val = oldworld.board[r, c].item()  # value in the map
        if val not in focus_set:  # if 'val' is new, init focus set
            focus_set[val] = 0
        if val != newworld.board[r, c].item():  # only when it comes into view first time
            if 1 <= value_counts[val] <= object_count_threshold:  # unique - why check for uniqueness?
                # this makes no sense. # dv-5/Aug # Patrick said implementation detail, it meant that it would only
                # trigger if there was 1 new value within visible window
                focus_set[val] += 1  # can happen when already set to 0, or over multiple time steps.
                # because we may focus over multiple time frames?
            difference_count_checksum += 1

    print("DEBUG _build_change_sets() Number of differences between old and new world", difference_count_checksum )

    if agent_rc_location is not None:
        current_agent_locations = [agent_rc_location]
    else:
        current_agent_locations = []


    # create adjacent change sets
    adjacent_change_sets = []
    for (r,c) in recently_observed_rc_locations:
        if (  # if different and observed code
                oldworld.board[r, c].item() != newworld.board[r, c].item()
                and oldworld.board[r, c].item() != oldworld.get_unobserved_code()
        ):
            # mutate changesets adding values to it.
            _add_to_adjacent_set(
                adjacent_change_sets, (r, c), MaxCapacity=3, CanCreateNewSet=True, maximum_distance=1, max_dist_one_dim=False
                # MaxCapacity=3 as 3 things need to have changed for more complex rules to be induced.
                # TODO 3 and 1 are magic numbers.
            )

    changesetslen = len(adjacent_change_sets)  # the length of change set only
    changeset0len = 0  # length of changeset 0 (the first changeset) Possibly this should be the max changeset length?
    if changesetslen > 0:
        changeset0len = len(
            adjacent_change_sets[0]
        )  # temporary fix: 3 things need to have changed at least to allow for the more complex rules to be induced
    # Add prediction mismatch entries to adjacent change set entry (using newworld for observation times)

    for (r,c) in recently_observed_rc_locations:
        if (
                predictedworld
                and predictedworld.board[r, c].item() != newworld.board[r, c].item()
                and oldworld.board[r, c].item() != oldworld.get_unobserved_code()
        ):
            _add_to_adjacent_set(
                adjacent_change_sets, (r, c), MaxCapacity=2, CanCreateNewSet=True, maximum_distance=1
                # MaxCapacity is one less than it was. hmmm...
            )


    # Does the following code fail if (say) the action was right which took effect, but the agent was also
    # forced down?
    # if there was a change next to a focus set element (spatial dependency) add it to the changeSet.
    # this will add
    chgsets = copy.deepcopy(adjacent_change_sets)  #chgsets
    for changeset in chgsets:
        # given a point, and action, generate all the points that could be eligible for use in a rule into a set
        for y, x in changeset:

            # if touching the agent, and the agent location not in change set, add it to the change set.
            for (agent_r,agent_c) in current_agent_locations:
                if math.sqrt(((y-agent_r)*(y-agent_r)) + ((x-agent_c)*(x-agent_c))) <= 1.0:
                    _add_to_adjacent_set(
                        adjacent_change_sets, (agent_r,agent_c), MaxCapacity = 3, CanCreateNewSet = False, maximum_distance = 2
                    )


            if (
                    (action in ['left','right'])
                    and x > 0  # assumes there will be a wall round the board
                    and newworld.board[y, x-1] in focus_set # set of cell values that have changed, but not too many at the same time
                    and oldworld.board[y, x-1] != oldworld.get_unobserved_code()
            ):
                _add_to_adjacent_set(
                    adjacent_change_sets, (y, x - 1), MaxCapacity=3, CanCreateNewSet=False, maximum_distance=1
                )
            if (
                    (action in ['left','right'])
                    and x < width - 1  # assumes there will be a wall round the board
                    and newworld.board[y, x+1] in focus_set
                    and oldworld.board[y, x+1] != oldworld.get_unobserved_code()
            ):
                _add_to_adjacent_set(
                    adjacent_change_sets, (y, x + 1), MaxCapacity=3, CanCreateNewSet=False, maximum_distance=1
                )
            if (
                    (action in ['up','down']) # also had drop in this list
                    and y > 0  # assumes there will be a wall round the board
                    and newworld.board[y-1, x] in focus_set
                    and oldworld.board[y-1, x] != oldworld.get_unobserved_code()
            ):
                _add_to_adjacent_set(
                    adjacent_change_sets, (y - 1, x), MaxCapacity=3, CanCreateNewSet=False, maximum_distance=1
                )
            if (
                    (action  in ['up','down'])
                    and y < height - 1  # assumes there will be a wall round the board
                    and newworld.board[y+1, x] in focus_set
                    and oldworld.board[y+1, x] != oldworld.get_unobserved_code()
            ):
                _add_to_adjacent_set(
                    adjacent_change_sets, (y + 1, x), MaxCapacity=3, CanCreateNewSet=False, maximum_distance=1
                )
            # the next line can add diagonals. (untested)
            # if (
            #         0 < x < width -1  # assumes there will be a wall round the board
            #         and 0 < y < height - 1  # assumes there will be a wall round the board
            # ):
            #     for delta_r, delta_c in [(+1,+1),(-1,-1), (+1,-1), (-1,+1)]:
            #         if (newworld.board[y + delta_r, x+ delta_c] in focus_set
            #         and oldworld.board[y + delta_r, x+ delta_c] != unobserved_code
            #         and (y + delta_r, x+ delta_c) in recently_observed_rc_locations):
            #             _add_to_adjacent_set(
            #                 adjacent_change_sets, (y + delta_r, x+ delta_c), MaxCapacity=3, CanCreateNewSet=True, maximum_distance=1, max_dist_one_dim=False
            #             )



    # Change sets are now built ready to be used.
    print("INFO _build_change_sets() Adjacent change sets have been built:", adjacent_change_sets)
    return focus_set, adjacent_change_sets, changeset0len


def _refine_rules_from_changesets(
        focus_set, # not mutated in this routine or sub routines.
        rule_evidence, # mutated
        oldworld,      # not mutated
        action,        # not mutated
        newworld,      # not mutated
        oldrules,      # copied into new var, mutated and returned
        pre_action_agent,                # not mutated
        ground_truth_post_action_agent,  # not mutated
        predicted_agent,                 # not mutated
        adjacent_change_sets,            # not mutated
        new_negrules,                    # mutated and returned
        changeset0len:int, # ideally we get rid of this parameter. not mutated
                                  ):
    # Build rules based on changes and prediction-observation mismatches
    # Algo: Within each changeset, Compare all changes to all other changes,
    #
    new_rules = copy.deepcopy(oldrules)

    if (predicted_agent.get_values_inc_prefix() != ground_truth_post_action_agent.get_values_inc_prefix()):
        print("DEBUG difference in predicted and actual agent detected. Should be learned in following code.")

    agent_observed_deltas = tuple(  # this stores agent value deltas (inc score)
        [post_v - pre_v for (post_v, pre_v) in (
            zip(ground_truth_post_action_agent.get_values_inc_prefix(),
                pre_action_agent.get_values_inc_prefix()))]  # get the delta of each value inc score
    )

    # STEP 1: Create, and add new rules to new_rules
    for changeset in adjacent_change_sets:
        for y1_abs, x1_abs in changeset:
            action_values_precondition = [action,
                                          tuple(pre_action_agent.get_values_for_precondition())]  # values excluding score
            preconditions = []
            CONTINUE = False
            for y2_abs, x2_abs in changeset:
                (y2_rel, x2_rel) = (y2_abs - y1_abs, x2_abs - x1_abs)  # relative to changeset 1
                condition = (y2_rel, x2_rel, oldworld.board[y2_abs, x2_abs])
                if (
                        oldworld.board[y2_abs, x2_abs] == oldworld.get_unobserved_code()
                ):  # NECESSARY FOR EPISODE RESET ONLY
                    CONTINUE = True  # old world at this location was or now is unobserved. Stop processing this location
                    break
                if Hypothesis_ValidCondition(condition):  # close by (0-2 in distance)
                    preconditions.append(condition)
                    # if current location in old_board has the same object on it in the newworld,
                    # we can skip forward - oct-11 - really? why?
                    if y2_rel == 0 and x2_rel == 0:
                        if (oldworld.board[y2_abs, x2_abs]
                                == newworld.board[y1_abs, x1_abs]):
                            #
                            CONTINUE = True # no change at this location. Stop processing this x,y, location
                            break
            if CONTINUE:
                continue  # skip forward to next location
            preconditions = sorted(preconditions)
            for pr in preconditions:
                action_values_precondition.append(pr)
            rule = (
                tuple(action_values_precondition),
                (
                    0,
                    0,
                    newworld.board[y1_abs, x1_abs],
                    agent_observed_deltas,
                ),
            )
            if len(preconditions) >= 1 and (changeset0len == 3 or len(preconditions) <= 3):
                val_to_char_mappings = newworld.get_val_to_char_mappings()
                rule_evidence, new_rules = Hypothesis_Confirmed(  # Mutates returned copy of rule_evidence and ruleset
                    focus_set, rule_evidence, new_rules, new_negrules, rule, val_to_char_mappings # dv changed to new_rules from oldrules, wed 18th dec 11pm.
                    # note newrules can be mutated in this routine.
                )
        # break  # speedup (dv-this looks odd, why have the outer loop if we always break and only process first element?)
        # The line above means it will only ever process the first changeset


    # STEP 2: create rules for those partialy met, or different outcome
    # if rule conditions are only partly met or the predicted outcome is different from observed,
    # build a specialized rule which has the precondition and conclusion corrected!
    max_focus = None
    if len(focus_set) > 0:
        max_focus = max(focus_set, key=lambda m: focus_set[m])
    (positionscores_v1, highesthighscore_v1) = _match_hypotheses(  # scores == Match Quotient
        focus_set,
        oldworld, action, new_rules, pre_action_agent,
        brute_force_focus_next_step=False
    )

    positionscores =  positionscores_v1
    highesthighscore = highesthighscore_v1

    height, width = oldworld.get_height_width()
    current_time = newworld.get_newest_time()
    val_to_char_mappings = newworld.get_val_to_char_mappings()

    for y in range(height):
        for x in range(width):
            if (y, x) not in positionscores:
                continue
            if (
                    not _is_presently_observed(current_time, newworld, y, x)
                    and oldworld.board[y, x].item() != max_focus
                    and not (
                    newworld.board[y, x].item() == oldworld.get_unobserved_code() and oldworld.board[y, x].item() != oldworld.get_unobserved_code())
            ):
                continue
            scores, highscore, rule, pp_rule = positionscores[(y, x)]
            # for rule in new_rules: # changed from oldrules to new_rules jan 28 (presumeably after copy() was added above) Note: this foreloop was commented out in Patricks code, so we used rule from position scores
            if _rule_applicable(scores, highscore, highesthighscore, rule): # best matching rule
                rule_value_deltas = rule[1][3]
                board_value = newworld.board[y, x]
                if rule[1][2] != board_value or rule_value_deltas != agent_observed_deltas:
                    (precondition, consequence) = rule
                    action_score_and_preconditions = list(precondition)
                    # values = action_score_and_preconditions[1]  # dv commented out as not used 3/aug/2024
                    corrected_preconditions = []
                    CONTINUE = False
                    is_max_focus_value = False
                    for y_rel, x_rel, requiredstate in action_score_and_preconditions[
                                                       2:
                                                       ]:
                        if (
                                y + y_rel >= height
                                or y + y_rel < 0
                                or x + x_rel >= width
                                or x + x_rel < 0
                        ):
                            CONTINUE = True
                            break
                        if oldworld.board[y + y_rel, x + x_rel] == max_focus:
                            is_max_focus_value = True
                        if oldworld.board[y + y_rel, x + x_rel] == oldworld.get_unobserved_code():
                            CONTINUE = True
                            break
                        corrected_preconditions.append(
                            (y_rel, x_rel, oldworld.board[y + y_rel, x + x_rel])
                        )
                    corrected_preconditions = sorted(corrected_preconditions)
                    if CONTINUE or not is_max_focus_value: # do not skip if cell value is max focus
                        continue
                    rule_new = (
                        tuple(
                            [
                                action_score_and_preconditions[0],
                                action_score_and_preconditions[1],
                            ]
                            + corrected_preconditions
                        ),
                        tuple(
                            [
                                rule[1][0],
                                rule[1][1],
                                newworld.board[y, x].item(),
                                tuple( # this takes the diff between last and now,
                                    # Possible ENHANCEMENT:
                                    # adjust the run by how far we are out, last 0.0, now 1.0, predicted was 0.75
                                    # then add 0.25 (now-predicted) to rule location.
                                    [post_v - pre_v for (post_v, pre_v) in (
                                        zip(ground_truth_post_action_agent.get_values_inc_prefix(),
                                            pre_action_agent.get_values_inc_prefix()))]
                                    # get the delta of each value inc score
                                ),
                            ]
                        ),
                    )
                    # print("RULE CORRECTION ", y, x, xy_loc, worldchange);
                    # Prettyprint_rule(rule);
                    # Prettyprint_rule(rule_new)
                    rule_evidence, new_rules = Hypothesis_Confirmed(
                        # Mutates returned copy of rule_evidence and ruleset
                        focus_set, rule_evidence, new_rules, new_negrules, rule_new, val_to_char_mappings
                    )
                    break

    # STEP 3: Add negative evidence for rules which prediction contradicts observation
    # Crisp match: (in a classical AIRIS implementation restricted to deterministic worlds: this part would remove
    # contradicting rules from the rule set and would ensure they can't be re-induced)
    for y in range(height):
        for x in range(width):
            if (
                    not _is_presently_observed(current_time, newworld, y, x)
                    and oldworld.board[y, x].item() != max_focus
                    and not (
                    newworld.board[y, x].item() == newworld.get_unobserved_code() and oldworld.board[y, x].item() != oldworld.get_unobserved_code())
            ):
                continue
            for (
                    rule
            ) in (
                    new_rules # changed from oldrules to new_rules jan 28 (presumeably after copy() was added above)
            ):  # find rules which don't work, and add negative evidence for them (classical AIRIS:
                # remove them and add them to newnegrules)
                (precondition, consequence) = rule
                action_valsExScore_and_preconditions = list(precondition)
                valsExScore = action_valsExScore_and_preconditions[1]
                CONTINUE = False
                if action_valsExScore_and_preconditions[0] != action:  # rule did not apply
                    continue
                for i in range(len(valsExScore)):
                    if (
                            i < len(pre_action_agent.get_values_for_precondition()) and valsExScore[i] != pre_action_agent.get_values_for_precondition()[i]  #
                    ):  # value didn't match, rule did not apply
                        CONTINUE = True
                        break
                for y_rel, x_rel, requiredstate in action_valsExScore_and_preconditions[2:]:
                    if (
                            y + y_rel >= height
                            or y + y_rel < 0
                            or x + x_rel >= width
                            or x + x_rel < 0
                    ):
                        CONTINUE = True
                        break
                    if oldworld.board[y + y_rel, x + x_rel] != requiredstate:
                        CONTINUE = True
                        break
                if CONTINUE:
                    continue
                if rule[1][3][0] != ground_truth_post_action_agent.get_score() - pre_action_agent.get_score():
                    val_to_char_mappings = newworld.get_val_to_char_mappings()
                    rule_evidence, new_rules, new_negrules = Hypothesis_Contradicted(
                        # Mutates returned copy of rule_evidence
                        rule_evidence, new_rules, new_negrules, rule, val_to_char_mappings
                    )  # score increase did not happen
                    continue
                num_values = max(len(rule[1][3]), len(ground_truth_post_action_agent.get_values_inc_prefix()))
                if num_values != len(rule[1][3]):
                    # num states does not match between rule and agent, skip this rule
                    CONTINUE = True
                    break

                for k in range(1, num_values):  # wrong value (not score) prediction (we start at index 1)
                    agent_value_k = ground_truth_post_action_agent.get_values_inc_prefix()[k]
                    rule_value_k = rule[1][3][k]
                    if rule_value_k != agent_value_k:
                        val_to_char_mappings = newworld.get_val_to_char_mappings()
                        rule_evidence, new_rules, new_negrules = Hypothesis_Contradicted(
                            # Mutates returned copy of rule_evidence
                            rule_evidence, new_rules, new_negrules, rule, val_to_char_mappings
                        )
                        CONTINUE = True
                        break
                if CONTINUE:
                    continue
                if rule[1][2] != newworld.board[y, x].item():
                    val_to_char_mappings = newworld.get_val_to_char_mappings()
                    rule_evidence, new_rules, new_negrules = Hypothesis_Contradicted(
                        # Mutates returned copy of rule_evidence
                        rule_evidence, new_rules, new_negrules, rule, val_to_char_mappings
                    )
    return focus_set, rule_evidence, new_rules, new_negrules


def _observe_v2( # new version which splits old into 2 parts for testing purposes
        focus_set,
        rule_evidence,
        oldworld,
        action,
        newworld,
        oldrules,
        oldnegrules,
        predictedworld,
        pre_action_agent,
        ground_truth_post_action_agent,
        predicted_agent,
        unobserved_code,
        object_count_threshold,
):
    """
    Extract new rules from the observations by looking only for observed changes and prediction-observation mismatches

    @param focus_set: Set of focus points : set of cell values that have changed, but not too many at the same time
    @param rule_evidence:  dict[rule:(+ve evidence, -ve evidence)]
    @param oldworld: State of the world before the action
    @param action: Action taken
    @param newworld: State of the world after the action
    @param oldrules: Existing rules
    @param oldnegrules: Existing negative rules
    @param predictedworld: Predicted state of the world after the action
    @param pre_action_agent: Agent state before the action
    @param ground_truth_post_action_agent: Ground truth agent state after the action
    @param predicted_agent: what we predicted the agent state to be
    @param unobserved_code: Code representing unobserved states
    @param object_count_threshold: Threshold for object count
    @return: Updated focus_set, rule_evidence, new_rules, new_negrules
    """
    # new_rules = copy.deepcopy(oldrules)
    # new_negrules = copy.deepcopy(oldnegrules)
    focus_set = copy.deepcopy(focus_set)

    focus_set, adjacent_change_sets, changeset0len = _build_change_sets(
        focus_set,
        oldworld,
        action,
        newworld,
        predictedworld,
        object_count_threshold,
        pre_action_agent.get_rc_loc()
    )


    calculated_focus_set, calculated_rule_evidence, calculated_new_rules, calculated_new_negrules = _refine_rules_from_changesets(
          focus_set,
          rule_evidence,
          oldworld,
          action,
          newworld,
          oldrules,
          pre_action_agent,
          ground_truth_post_action_agent,
          predicted_agent,
          adjacent_change_sets,
          oldnegrules,
          changeset0len
    )

    return calculated_focus_set, calculated_rule_evidence, calculated_new_rules, calculated_new_negrules




def nacev3_predict_and_observe(  # called _predict_and_observe in v1
        time_counter,
        focus_set,
        rule_evidence,
        rc_loc,  # pre action agent location note (0,0) is top left
        pre_action_world,  # pre action internal world model (partially observed) before last_action is applied
        rulesin,  # used in part1 and part2
        negrules,
        last_action,
        rulesExcluded,
        post_action_ground_truth_world,  # i.e. this is the post action world model
        pre_action_agent,  # pre action agent
        ground_truth_post_action_agent,  # post action agent
        unobserved_code,  # value which indicates we can not see the true value of the cell
        agent_indication_raw_value_list:list, # raw value of an agent, i.e. 'x', or the rgb value
        object_count_threshold=1,  # how unique values must be before they are considered. was 1, i.e. unique
        print_out_world_and_plan=True):
    """
    Find difference between the actual world, and the predicted world.

    @param time_counter:
    @param focus_set:
    @param rule_evidence:
    @param rc_loc:
    @param pre_action_world:
    @param rulesin:
    @param negrules:
    @param last_action:
    @param rulesExcluded:
    @param post_action_ground_truth_world:
    @param pre_action_agent
    @param ground_truth_post_action_agent
    @param print_out_world_and_plan:
    @return:
    """
    if print_out_world_and_plan:
        t1 = time.time()
        print("INFO nacev3_predict_and_observe() START")
    simulated_world_original = copy.deepcopy(pre_action_world)
    simulated_world_post_action = copy.deepcopy(pre_action_world)
    rc_location_t_minus_1 = simulated_world_original.extract_agent_location_raw(agent_indication_raw_value_list)
    modified_count, _ = simulated_world_post_action.update_world_from_ground_truth(
        time_counter,
        post_action_ground_truth_world,
        [rc_loc, rc_location_t_minus_1],
        agent_indication_raw_value_list=agent_indication_raw_value_list
    )
    predict_next_world_state_call_count_during_observe = 0

    stayed_the_same = modified_count == 0

    active_rules, rulesExcluded = Hypothesis_BestSelection(
        rules=rulesin,
        rules_excluded=rulesExcluded,
        rule_evidence=rule_evidence,
        include_random_rules=stayed_the_same)  # Step 2 # Mutates rules and rulesExcluded by adding and removing items


    predicted_world, predicted_agent, _, __, values, predicted_score_delta = _predict_next_world_state(
        focus_set,
        copy.deepcopy(simulated_world_original), last_action, active_rules, pre_action_agent
    )
    predict_next_world_state_call_count_during_observe += 1

    #debugging code
    if pre_action_agent.get_score() < ground_truth_post_action_agent.get_score():
        pass # place breakpoint here

    # Extract new rules from the observations by looking only for observed changes and prediction-observation mismatches
    focus_set, rule_evidence, newrules, newnegrules = _observe_v2(
        focus_set,
        rule_evidence,
        simulated_world_original,
        last_action,
        simulated_world_post_action,
        active_rules,
        negrules,
        predicted_world,
        pre_action_agent,
        ground_truth_post_action_agent,
        predicted_agent,
        unobserved_code,
        object_count_threshold,
    )
    used_rules = copy.deepcopy(newrules)
    for rule in rulesExcluded:  # add again so we won't lose them
        newrules.add(rule)

    lastplanworld = copy.deepcopy(simulated_world_original)

    if print_out_world_and_plan:
        t2 = time.time()
        print("INFO nacev3_predict_and_observe() END", "time_taken=",(t2-t1))

    stats = {"predict_next_world_state_call_count_during_observe":predict_next_world_state_call_count_during_observe}

    return (
        used_rules,
        focus_set,
        rule_evidence,
        simulated_world_post_action,
        newrules,
        newnegrules,
        values,
        lastplanworld,
        predicted_world,
        stayed_the_same,
        stats
    )

    # return plan, action, rulesExcluded, behavior, simulated_world_staued_the_same_last_time_new_data_copied_in


def print_world_at_plan_end(time_counter, focus_set, pre_action_world, post_action_ground_truth_world, plan, pre_action_agent, active_rules):
    simulated_world_original = copy.deepcopy(pre_action_world)

    # roll forward the world according to the plan
    predicted_world = copy.deepcopy(simulated_world_original)
    for i in range(0, len(plan)):
        lastplanworld = copy.deepcopy(predicted_world)
        predicted_world, predicted_agent, _, __, ___, ____ = _predict_next_world_state(
            focus_set,
            copy.deepcopy(predicted_world), plan[i], active_rules, pre_action_agent
        )

    print("Learning Phase: 1 time step, ground truth, and end of plan.")
    post_action_ground_truth_world.multiworld_print(
        [
            {"Caption": "Internal model:\ndt=-1",
             "World": simulated_world_original,
             "Color": nace.color_codes.color_code_white_on_blue},

            {"Caption": "Predicted\ndt=0\n==GT?",
             "World": predicted_world,
             "Color": nace.color_codes.color_code_white_on_blue},

            {"Caption": f"Ground Truth \ndt=0\nt={time_counter} beliefs={len(active_rules)}:",
             "World": post_action_ground_truth_world,
             "Color": nace.color_codes.color_code_white_on_black},

            {"Caption": "Plan\nsteps=" + str(len(plan)) + "\n" + str(prettyprint_all_actions(plan)),
             "World": predicted_world,
             "Color": nace.color_codes.color_code_white_on_red},
        ]
    )




if __name__ == "__main__":
    _create_explanation_graphs()
