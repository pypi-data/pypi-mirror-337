import copy
import glob
from collections import defaultdict

import gymnasium as gym
import numpy as np

import nace

"""

Inprogress: code to find movement action effects from actions, 
i.e. was trying to not need to know the meaning of 'up', but learn it from experience.

"""


def perform_actions_find_location_deltas(env_name, cell_shape_rc, action_number_list=(1,)):
    """
    Perform all the actions in the list on a newly initialised world. Return the agent location.

    :param env_name:
    :param action_number_list:
    :return:
    """
    # check the agents location is where it is expected.
    agent_indication_raw_value_list = []
    fn_list = glob.glob("./data/agents/*.npy")
    for fn in fn_list:
        cell = np.load(fn)
        agent_indication_raw_value_list.append(cell)
    env = gym.make(env_name, render_mode="rgb_array")
    env.reset()
    env_rendered = env.render()
    external_ground_truth_npworld = nace.world_module_numpy.NPWorld(with_observed_time=False,
                                                                    name="external ground truth")
    original_agent_location, _, _, _ = external_ground_truth_npworld.update_world_from_ground_truth_NPArray(
        env_rendered,
        update_mode='ALL',
        cell_shape_rc=cell_shape_rc,
        add_surrounding_walls=True,
        wall_code=nace.world_module_numpy.EMBEDDED_WALL_CODE,
        agent_indication_raw_value_list=agent_indication_raw_value_list,
        observed_at=1
    )
    if len(original_agent_location) == 0:
        raise Exception("Could not find agent")

    original_agent_location = original_agent_location[-1]
    locations = [original_agent_location]
    embedded_values = [
        external_ground_truth_npworld.get_embedded_val_rc(original_agent_location[0], original_agent_location[1])]
    for observed_at, action_number in enumerate(action_number_list):
        env.step(action_number)  # 0 == up?
        env_rendered = env.render()
        external_ground_truth_npworld = nace.world_module_numpy.NPWorld(with_observed_time=False,
                                                                        name="external ground truth")
        _, _, _, _ = (external_ground_truth_npworld.update_world_from_ground_truth_NPArray(
            env_rendered,
            update_mode='ALL',
            cell_shape_rc=cell_shape_rc,
            add_surrounding_walls=True,
            wall_code=nace.world_module_numpy.EMBEDDED_WALL_CODE,
            agent_indication_raw_value_list=agent_indication_raw_value_list,
            observed_at=observed_at
        ))
        location = external_ground_truth_npworld.extract_agent_location_raw(agent_indication_raw_value_list)
        locations.append(location)
        embedded_value = external_ground_truth_npworld.get_embedded_val_rc(location[0], location[1])
        embedded_values.append(embedded_value)

    if location == (-1, -1):
        return None, False
    if len(original_agent_location) > 0 and location == original_agent_location[0]:
        return None, False

    last_move_delta = (locations[-1][0] - locations[-2][0], locations[-1][1] - locations[-2][1])

    embedding_change = (embedded_values[-2], embedded_values[-1])

    return last_move_delta, embedding_change


def find_gym_action_mappings(env_name="CliffWalking-v0", num_actions=4, cell_shape_rc=(60, 60)):
    """
    determine which actions are up down left right.
    :return:
    """
    results1 = {}
    embedding_change_by_action1 = {}
    for action_number_1 in range(num_actions):
        movement_delta, agent_embedding_change = perform_actions_find_location_deltas(env_name=env_name,
                                                                                      cell_shape_rc=cell_shape_rc,
                                                                                      action_number_list=[
                                                                                          action_number_1])
        if movement_delta is not None:
            if not (movement_delta[0] == 0 and movement_delta[1] == 0):
                if abs(movement_delta[0]) + abs(movement_delta[1]) == 1:
                    results1[action_number_1] = movement_delta
            if movement_delta == (0, 0) and agent_embedding_change[0] != agent_embedding_change[1]:
                if action_number_1 not in embedding_change_by_action1:
                    embedding_change_by_action1[action_number_1] = []
                embedding_change_by_action1[action_number_1].append(agent_embedding_change)

    results2 = {}
    embedding_change_by_action2 = {}
    for action_number_1 in results1.keys():
        for action_number_2 in range(num_actions):
            movement_delta, agent_embedding_change = perform_actions_find_location_deltas(env_name="CliffWalking-v0",
                                                                                          cell_shape_rc=cell_shape_rc,
                                                                                          action_number_list=[
                                                                                              action_number_1,
                                                                                              action_number_2])
            if movement_delta is not None:
                if not (movement_delta[0] == 0 and movement_delta[1] == 0):
                    if abs(movement_delta[0]) + abs(movement_delta[1]) == 1:
                        results2[action_number_2] = movement_delta
                if movement_delta == (0, 0) and agent_embedding_change[0] != agent_embedding_change[1]:
                    if action_number_2 not in embedding_change_by_action2:
                        embedding_change_by_action2[action_number_2] = []
                    embedding_change_by_action2[action_number_2].append(agent_embedding_change)

    results3 = {}
    embedding_change_by_action3 = {}
    for action_number_1 in results1.keys():
        for action_number_2 in results2.keys():
            for action_number_3 in range(num_actions):
                movement_delta, agent_embedding_change = perform_actions_find_location_deltas(
                    env_name="CliffWalking-v0", cell_shape_rc=cell_shape_rc,
                    action_number_list=[action_number_1, action_number_2, action_number_3])
                if movement_delta is not None:
                    if not (movement_delta[0] == 0 and movement_delta[1] == 0):
                        if abs(movement_delta[0]) + abs(movement_delta[1]) == 1:
                            results3[action_number_3] = movement_delta
                if movement_delta == (0, 0) and agent_embedding_change[0] != agent_embedding_change[1]:
                    if action_number_3 not in embedding_change_by_action3:
                        embedding_change_by_action3[action_number_3] = []
                    embedding_change_by_action3[action_number_3].append(agent_embedding_change)

    results4 = {}
    embedding_change_by_action4 = {}
    for action_number_1 in results1.keys():
        for action_number_2 in results2.keys():
            for action_number_3 in results3.keys():
                for action_number_4 in range(num_actions):
                    movement_delta, agent_embedding_change = perform_actions_find_location_deltas(
                        env_name="CliffWalking-v0", cell_shape_rc=cell_shape_rc,
                        action_number_list=[action_number_1, action_number_2, action_number_3, action_number_4])
                    if movement_delta is not None:
                        if not (movement_delta[0] == 0 and movement_delta[1] == 0):
                            if abs(movement_delta[0]) + abs(movement_delta[1]) == 1:
                                results4[action_number_4] = movement_delta
                    if movement_delta == (0, 0) and agent_embedding_change[0] != agent_embedding_change[1]:
                        if action_number_4 not in embedding_change_by_action4:
                            embedding_change_by_action4[action_number_4] = []
                        embedding_change_by_action4[action_number_4].append(agent_embedding_change)

    # print( json.dumps(results, indent=2))
    # print( json.dumps(results2, indent=2))
    # print( json.dumps(results3, indent=2))
    # print( json.dumps(results4, indent=2))
    #  we expect {0:nace.world_module.up, 1:nace.world_module.right, 2:nace.world_module.down, 3:nace.world_module.left}
    #                 -1,0                     0,1                        1,0                       0,-1

    all_deltas = {}
    all_deltas.update(results1)
    all_deltas.update(results2)
    all_deltas.update(results3)
    all_deltas.update(results4)
    # print( json.dumps(all, indent=2))

    agent_embedding_change = {}
    for d in [embedding_change_by_action1, embedding_change_by_action2, embedding_change_by_action3,
              embedding_change_by_action4]:
        for k in d.keys():
            if k not in agent_embedding_change:
                agent_embedding_change[k] = []
            agent_embedding_change[k].extend(d[k])

    # reformat into which number do which actions
    movement_action_list = [None] * num_actions
    for k in all_deltas.keys():
        if all_deltas[k] == (-1, 0):
            movement_action_list[k] = nace.world_module.up
        if all_deltas[k] == (1, 0):
            movement_action_list[k] = nace.world_module.down
        if all_deltas[k] == (0, -1):
            movement_action_list[k] = nace.world_module.left
        if all_deltas[k] == (0, 1):
            movement_action_list[k] = nace.world_module.right

    # movement_action_list : list, the left, right, up, down action occuring in each location in the coresponing to the gym_action_number
    # agent_embedding_change for each gym_action_number, i.e. for action 0, the agent embedding might change efrom 1 to 2 0:(1,2)
    return movement_action_list, agent_embedding_change


def perform_actions_find_observation_deltas(env_name, action_number_list=[1]):
    """
    Perform all the actions in the list on a newly initialised env. find changes in the observations.

    :param env_name:
    :param action_number_list:
    :return:
    """

    env = gym.make(env_name, render_mode="rgb_array")
    observation, info = env.reset()
    list_of_observations = [observation]
    env_rendered = env.render()

    observation_deltas = {}

    for action in action_number_list:
        post_action_observation, reward, terminated, truncated, info = env.step(action)
        list_of_observations.append(post_action_observation)

        if action not in observation_deltas:
            observation_deltas[action] = []

        observation_deltas[action].append(list_of_observations[-1] - list_of_observations[-2])

    return observation_deltas


def _find_action_observation_relationships(node, env_name="CliffWalking-v0", num_actions=4, action_prefixes=[]):
    for action in range(num_actions):
        action_list = copy.deepcopy(action_prefixes)
        action_list.append(action)

        x = perform_actions_find_observation_deltas(env_name, action_list)
        if x[action][-1] != 0:
            if action in node:
                node[action]["deltas"].append(x[action][-1])
            else:
                result = {"next": {}, "deltas": [x[action][-1]]}
                node[action] = result

    print()


def find_action_observation_relationships(env_name="CliffWalking-v0", num_actions=4):
    """
    Do a small amount of structured exploration, to get an idea of which actions affect which parts of the observation space.
    @param env_name:
    @param num_actions:
    @return:
    """
    parent_node = {}
    _find_action_observation_relationships(parent_node, env_name=env_name, num_actions=num_actions, action_prefixes=[])

    a1 = ""
    for a0 in parent_node.keys():
        child_node = parent_node[a0]["next"]
        _find_action_observation_relationships(child_node, env_name=env_name, num_actions=num_actions,
                                               action_prefixes=[a0])

        for a1 in child_node.keys():
            c1_node = child_node[a1]["next"]
            _find_action_observation_relationships(c1_node, env_name=env_name, num_actions=num_actions,
                                                   action_prefixes=[a0, a1])

    deltas_sums = {}
    delta_counts = defaultdict(int)
    for a0 in parent_node.keys():
        delta_counts[a0] += 1
        if a1 not in deltas_sums:
            deltas_sums[a0] = parent_node[a0]["deltas"]
        else:
            for i in range(len(deltas_sums[a0])):
                deltas_sums[a0][i] += parent_node[a0]["deltas"][i]

        for a1 in parent_node[a0]["next"].keys():
            delta_counts[a1] += 1
            if a1 not in deltas_sums:
                deltas_sums[a1] = parent_node[a0]["next"][a1]["deltas"]
            else:
                for i in range(len(deltas_sums[a0])):
                    deltas_sums[a1][i] += parent_node[a0]["next"][a1]["deltas"][i]

            for a2 in parent_node[a0]["next"][a1]["next"].keys():
                delta_counts[a2] += 1
                if a2 not in deltas_sums:
                    deltas_sums[a2] = parent_node[a0]["next"][a1]["next"][a2]["deltas"]
                else:
                    for i in range(len(deltas_sums[a0])):
                        deltas_sums[a2][i] += parent_node[a0]["next"][a1]["next"][a2]["deltas"][i]

    averages = {}
    for action in delta_counts.keys():
        averages[action] = copy.deepcopy(deltas_sums[action])
        for i in range(len(averages[action])):
            averages[action][i] = averages[action][i] / delta_counts[action]

    # It should be possible to tell from the averages which action is the inverse of which.
    # It might be possible to tell that action a,b and inverse, and symmetrical to actions c,d
    # if 1) they affect the same observation value with some scale factor , or
    # 2) they affect different (and possibly orthogonal) observations with some scale factor.

    """
    Return average observation change for each action.
    """
    return averages
