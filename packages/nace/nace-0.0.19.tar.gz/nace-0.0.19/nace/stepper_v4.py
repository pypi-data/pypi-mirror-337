"""
 * The MIT License
 *
 * Copyright (c) 2024 Dwane van der Sluis
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
import copy
import json
import sys
import time
import random
import numpy as np
import collections
from typing import Type

import nace.world_module_numpy
from nace.agent_module import Agent
from nace.nace_v3 import nacev3_get_next_action, nacev3_predict_and_observe, print_world_at_plan_end
from nace.world_module_numpy import NPWorld
from nace.graph_utilities import produce_charts
from nace.rule_evidence_utils import load_rule_evidence_from_disk

# def _get_expected_deltas(nace_action_name):
#     expected_directions = {
#         "^left": (-1, 0),
#         "^right": (1, 0),
#         "^up": (0, -1),
#         "^down": (0, 1)
#     }
#     expected_column_delta, expected_row_delta = expected_directions.get(nace_action_name, (0, 0))
#     return expected_row_delta, expected_column_delta


class StepperV4():
    def __init__(self, agent_indication_raw_value_list:list, seed_value=1, unobserved_code=nace.world_module_numpy.UNOBSERVED_BOARD_VALUE, available_actions_function=None):
        # The world is held externally.
        # The state of the agent (score number of keys held etc.) is held externally
        # Actions are performed on that world externally
        # this class wraps code and expectations that allow it to take one of the passed in worlds and predict forward.
        # partial observation (if it occurs) happens outside this code.

        # This module hole

        # variables set to specific values and passed in
        self.current_behavior = "BABBLE"
        random.seed(seed_value)

        # variables set to empty sets, or lists before the first call of this routine

        # these 4 var are global in the original implementation
        self.focus_set = dict([])
        self.rule_evidence = dict([])
        self.rules = set()
        self.negrules = set()
        self.whole_plan = []
        self.time_counter = -1
        self.unobserved_code = unobserved_code  # indicates we have not seen the maps true value
        self.agent_indication_raw_value_list = agent_indication_raw_value_list # raw value(s) of an agent, i.e rgb np.ndarrays
        self.step_number = 0 # increments each time get_next_Action() is called. Similar, but different to time.
        self.current_plan = [] # plan currently being executed.
        self.rewards = [] # unbounded (warning could grow forever) list of rewards.

        self.anamestr = "1234"

        # variables NOT set before the first call of this routine (in original implementation)
        self.used_rules = None
        self.debuginput = None

        self.rules_excluded = None
        self.stayed_the_same = False  # when last time the new ground truth is copied over it.

        self.post_action_agent = None
        self.pre_action_agent = None

        self.internal_world = None  # working copy

        self.internal_preaction_world = None  # updated each time a best action is predicted
        self.action = None  # predicted best action
        self.available_actions_function = available_actions_function # Will be used to get the available actions
        self.statistics = collections.defaultdict(int)
        self.series_statistics = []

        self.unittest_code_str = ""

    def set_agent_ground_truth_state(self, rc_loc, score, terminated, values_exc_prefix):

        if self.post_action_agent is None:
            self.pre_action_agent = Agent(rc_loc, score, int(terminated), [0 for _ in values_exc_prefix])
            self.post_action_agent = Agent(rc_loc, score,
                                           terminated=int(terminated),
                                           values_excluding_prefix=values_exc_prefix)
        else:
            reward = score - self.post_action_agent.get_score()
            self.rewards.append(reward) # TODO unbounded, will grow forever, also currently unused.
            print("DEBUG rewards max=",max(self.rewards), "min=", min(self.rewards), "mean=", sum(self.rewards)/len(self.rewards))

            self.pre_action_agent = copy.deepcopy(self.post_action_agent)
            self.post_action_agent.set_rc_loc(rc_loc)
            self.post_action_agent.set_values_inc_prefix([score] + [int(terminated)] + list(values_exc_prefix))
        # Possible feature: try and reverse engineer rules that change each value into the description for that value
        # 'kx',left -> 'x ', v[1]+=1   --> pick up k
        # result = {}
        # for i, v in enumerate(self.post_action_agent.values):
        #     if i == Agent.INDEX_SCORE:
        #         result["score"] = {"v": v}
        #     elif i == Agent.INDEX_TERMINATED:
        #         result["terminated"] = {"v": v}
        #     else:
        #         result["v" + str(i)] = {"v": v}
        # return result

    def set_world_ground_truth_state(
            self,
            ground_truth_external_world: Type[NPWorld],
            view_rc_locs: list,
            time_counter:int):
        # Update the world in the region of the agent's field of view
        if ground_truth_external_world is not None:
            modified_count, _ = self.internal_world.update_world_from_ground_truth(
                time_counter,
                ground_truth_external_world,
                rc_locations=view_rc_locs,
            agent_indication_raw_value_list=self.agent_indication_raw_value_list)  # called 3rd Nov


    def get_next_action(self,
                        ground_truth_external_world: Type[NPWorld],
                        new_rc_loc,
                        print_debug_info,
                        time_delay_sec=0.0, view_dist_x=3, view_dist_y=2,
                        max_num_actions: int=12,  # planning search depth
                        max_queue_length: int=70,  # planning queue depth
                        use_sticky_plans:bool =True
                        ):
        self.step_number += 1
        if self.pre_action_agent is None:
            # self.pre_action_agent = Agent(new_rc_loc, score=0, values_exc_score=(0,))
            self.pre_action_agent = Agent.new_default_instance(new_rc_loc)
        if self.internal_world is None:
            self.internal_world = NPWorld(with_observed_time=True, name="self.internal_world", view_dist_x=view_dist_x,
                                          view_dist_y=view_dist_y,
                                          store_raw_cell_data=False # 5th Feb 2024
                                          )


        # new_rc_loc be the single location of the agent we are interested in (if multiple)
        assert isinstance(new_rc_loc, tuple)

        start_time = time.time()
        self.time_counter += 1
        agent = self.post_action_agent if self.post_action_agent is not None else self.pre_action_agent

        if self.available_actions_function is not None:
            full_action_list = self.available_actions_function()
        else:
            raise Exception("Pass the function that returns valid actions to the Stepper constructor.")

        # if we use the difference count, we then want to use which differences matter and which don't,
        # which seems like a step to far without being extremely general.
        differences_count = self.internal_world.get_difference_count(self.internal_preaction_world)
        print("DEBUG world difference count (t-1, and now) =", differences_count,
              " Note: this should never be used in our logic as it it too environment dependent.")

        if (len(self.whole_plan) > 1 and use_sticky_plans):
            # we are executing a previous planed plan,  remove the action just executed. Set the next action.
            self.whole_plan = self.whole_plan[1:]
            self.action = self.whole_plan[0]
            statistics = {}
            print("INFO Using sticky plan ", self.whole_plan)
        else:
            self.whole_plan, self.rules_excluded, self.current_behavior, statistics, unittest_code_str = nacev3_get_next_action(
                self.time_counter,
                self.focus_set,
                self.rule_evidence,  # can be mutated
                [agent.get_rc_loc()],  #
                self.internal_world,  # passed in, has updates from external world applied to it.
                self.rules,
                ground_truth_external_world,  # used to update internal world
                print_debug_info=print_debug_info,
                stayed_the_same=self.stayed_the_same,
                agent=agent,
                full_action_list=full_action_list,
                agent_indication_raw_value_list=self.agent_indication_raw_value_list, # called 3rd Nov
                max_num_actions=max_num_actions, # planning search depth
                max_queue_length=max_queue_length # planning queue depth
            )
            self.action = self.whole_plan[0]
            # store plan
            self.unittest_code_str = unittest_code_str
            for k in statistics.keys():
                self.statistics["nacev3_get_next_action." + k] += statistics[k]
            self.statistics["plan.lowest_AIRIS_confidence"] = statistics["plan.lowest_AIRIS_confidence"]

        self.statistics["nacev3_get_next_action.call_count"] += 1
        self.statistics["plan.behavior.curious"] = 1 if self.current_behavior == "CURIOUS" else 0
        self.statistics["plan.behavior.achieve"] = 1 if self.current_behavior == "ACHIEVE" else 0
        self.statistics["plan.behavior.babble"] = 1 if self.current_behavior == "BABBLE" else 0
        self.statistics["plan.behavior.explore"] = 1 if self.current_behavior == "EXPLORE" else 0
        assert self.current_behavior in ["EXPLORE", "BABBLE", "ACHIEVE", "CURIOUS"]

        series_record = {}
        for k in ["plan.evaluation_count",
                  "plan.total_items_placed_on_queue",
                  "plan.short_circuit_advantage",
                  "plan.evaluation_count_at_which_reward_found",
                  "plan.evaluation_count_at_which_lower_AIRIS_confidence_found",
                  "plan.lowest_AIRIS_confidence",
                  "plan.behavior.achieve",
                  "plan.behavior.babble",
                  "plan.behavior.explore",
                  "plan.behavior.curious",
                  ]:
            v = self.statistics[k] if k in self.statistics else 0
            series_record[k] = v


        self.series_statistics.append(series_record)
        with open("./data/series_statistics.json", "w") as f:
            json.dump(self.series_statistics, f)

        # Store a copy after the external updates are copied in, i.e. the world use to predict on
        self.internal_preaction_world = copy.deepcopy(self.internal_world) # used in predict and observe

        end_time = time.time()
        if "manual" in sys.argv:
            print(self.current_behavior)
        else:
            if print_debug_info:
                from nace.test_utilities import (convert_focus_set_to_char_mapping)
                new_focus_set = convert_focus_set_to_char_mapping(self.focus_set, ground_truth_external_world)
                print("DEBUG get_next_action()", "next_action=", str(self.action),  self.current_behavior, "whole plan=", self.whole_plan)
                # print("INFO get_next_action()", "series_statistics=", self.series_statistics )

        elapsed_time = end_time - start_time
        if (
                elapsed_time < time_delay_sec
                and "nosleep" not in sys.argv
                and "debug" not in sys.argv
                and "manual" not in sys.argv
        ):
            time.sleep(time_delay_sec - elapsed_time)

        return self.action, self.current_behavior

    def overide_best_action(self, action):
        available_actions = self.available_actions_function()
        assert action in available_actions
        print("WARN the action has been overridden from the planned action from ",self.action," to", action)
        self.action = action

    def add_to_series_record(self, dict_of_values, prefix="", create_charts=False ):
        for k in dict_of_values.keys():
            self.series_statistics[-1][k] = dict_of_values[k]

        if create_charts:
            produce_charts(self.series_statistics, prefix)

        save_as = "./data/" + prefix + "_series_data.json"
        with open(save_as, "w") as f:
            json.dump(self.series_statistics, f)


    def predict_and_observe(self,
                            object_count_threshold=1,
                            print_out_world_and_plan=True
                            ):
        """
        Updates the KB of rules and evidence based on the differences between the last state, the predicted state,
        and the actual new state of the environment, and the world.

        Stores as many of the variables in the 'Stepper' object so calling code is simplier.

        @param object_count_threshold: how many new instances can be seen , and be considered, more are ignored
        @return:
        """
        (
            self.used_rules,
            self.focus_set,
            self.rule_evidence,
            predicted_world,
            self.rules,
            self.negrules,
            values,
            _lastplanworld,
            _planworld,
            self.stayed_the_same,
            stats
        ) = nacev3_predict_and_observe(
            self.time_counter,
            self.focus_set,
            self.rule_evidence,
            self.pre_action_agent.get_rc_loc(),
            copy.deepcopy(self.internal_preaction_world),  # pre action world (with times)
            self.rules,  # used in part1 and part2
            self.negrules,
            self.action,
            self.rules_excluded,
            copy.deepcopy(self.internal_world),
            # post action world, can be internal or external, differences are copied in
            pre_action_agent=self.pre_action_agent,  # pre action agent
            ground_truth_post_action_agent=self.post_action_agent,  # post action agent
            unobserved_code=self.unobserved_code,
            agent_indication_raw_value_list = self.agent_indication_raw_value_list,  # called 3rd Nov
            object_count_threshold=object_count_threshold,
            print_out_world_and_plan=print_out_world_and_plan,
        )

        if print_out_world_and_plan and False:
            print_world_at_plan_end(self.time_counter, self.focus_set, pre_action_world=copy.deepcopy(self.internal_preaction_world), post_action_ground_truth_world=copy.deepcopy(self.internal_world), plan=self.whole_plan, pre_action_agent=self.pre_action_agent, active_rules=self.rules)

        for k in stats.keys():
            self.statistics[k] += stats[k]
        self.statistics["observe_call_count"] += 1


    def save_rules_to_file(self, rule_evidence_filename="rule_evidence.json", filename="stepper_state.json"):

        _1, converted_rules = nace.test_utilities.convert_rules_to_char_or_int_mappings(self.rules, self.internal_world, dest="INT")
        _2, converted_negrules = nace.test_utilities.convert_rules_to_char_or_int_mappings(self.negrules, self.internal_world,
                                                                                        dest="INT")
        _3, converted_rule_evidence = nace.test_utilities.convert_rules_to_char_or_int_mappings(self.rule_evidence, self.internal_world,dest="INT")
        _4, converted_rules_excluded = nace.test_utilities.convert_rules_to_char_or_int_mappings(self.rules_excluded, self.internal_world,dest="INT")

        # check each component can be serialed to json
        json.dumps(converted_rules, indent=2)
        json.dumps(converted_negrules, indent=2)
        json.dumps(converted_rule_evidence, indent=2)
        json.dumps(converted_rules_excluded, indent=2)


        _5, converted_rules_char = nace.test_utilities.convert_rules_to_char_or_int_mappings(self.rules, self.internal_world, dest="CHAR")
        _6, converted_negrules_char = nace.test_utilities.convert_rules_to_char_or_int_mappings(self.negrules, self.internal_world,
                                                                                        dest="CHAR")
        _7, converted_rule_evidence_char = nace.test_utilities.convert_rules_to_char_or_int_mappings(self.rule_evidence, self.internal_world,dest="CHAR")
        _8, converted_rules_excluded_char = nace.test_utilities.convert_rules_to_char_or_int_mappings(self.rules_excluded, self.internal_world,dest="CHAR")

        # check each component can be serialed to json
        json.dumps(converted_rules_char, indent=2)
        json.dumps(converted_negrules_char, indent=2)
        json.dumps(converted_rule_evidence_char, indent=2)
        json.dumps(converted_rules_excluded_char, indent=2)


        agent_indication_emdedded_value_list = self.internal_world._convert_raw_to_embedded_values(self.agent_indication_raw_value_list)

        state = {"rules":converted_rules,
                 "negrules":converted_negrules,
                 "rule_evidence":converted_rule_evidence,
                 "rules_excluded":converted_rules_excluded,
                 "time_counter":self.time_counter,
                 "focus_set":self.focus_set,
                 "agent_indication_emdedded_value_list":agent_indication_emdedded_value_list,
                 "world_state":self.internal_world.get_internal_state(),
                 "approx_human_readable":{
                     "rules_char": converted_rules_char,
                     "negrules_char": converted_negrules_char,
                     "rule_evidence_char": converted_rule_evidence_char,
                     "rules_excluded_char": converted_rules_excluded_char,
                 }
                 }

        s = json.dumps(state, indent=2)
        with open(filename, "w") as f:
            f.write(s)

        # rule evidence in machine readable form.
        nace.rule_evidence_utils.save_rule_evidence_to_disk(self.rule_evidence, rule_evidence_filename)

        return s

    def add_rules_and_evidence_from_file_to_memory(self, rule_evidence_filename):
        loaded_rule_evidence = nace.rule_evidence_utils.load_rule_evidence_from_disk(rule_evidence_filename)
        for k in loaded_rule_evidence.keys():
            if k not in self.rule_evidence:
                self.rule_evidence[k] = loaded_rule_evidence[k]
                self.rules.add(k)
            else:
                self.rule_evidence[k] = ( self.rule_evidence[k][0] + loaded_rule_evidence[k][0], self.rule_evidence[k][1] + loaded_rule_evidence[k][1] )



    def save_statistics_to_file(self, filename="data/stepper_statistics.json"):
        s = json.dumps(self.statistics, indent=2)
        with open(filename, "w") as f:
            f.write(s)

