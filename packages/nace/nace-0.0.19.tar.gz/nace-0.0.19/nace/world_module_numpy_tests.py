import nace
import glob
import json
import numpy as np
import gymnasium as gym



def t2_can_find_agent(path ="./data/agents/*.npy"):
    # check the agents location is where it is expected.
    agent_indication_raw_value_list=[]
    fn_list = glob.glob(path)
    for fn in fn_list:
        cell =  np.load(fn)
        agent_indication_raw_value_list.append(cell)

    env = gym.make("CliffWalking-v0",
                   render_mode="rgb_array",
                   )
    env.reset()

    observation, gym_reward, terminated, truncated, info = env.step(0) # 0 == up
    env_rendered = env.render()
    external_ground_truth_npworld = nace.world_module_numpy.NPWorld(with_observed_time=False, name="external ground truth")
    pre_update_agent_location_embedded_space_list, post_update_agent_location_embedded_space_list, modified_count, pre_update_world = external_ground_truth_npworld.update_world_from_ground_truth_NPArray(
        env_rendered,
        update_mode="VIEW",
        cell_shape_rc=(60,60,3),
        add_surrounding_walls=True,
        wall_code=nace.world_module_numpy.EMBEDDED_WALL_CODE,
        agent_indication_raw_value_list=agent_indication_raw_value_list,
        observed_at=1
    )
    locations = external_ground_truth_npworld.extract_agent_location_raw(agent_indication_raw_value_list)
    assert locations == (3,1)

def t1_world_print(path = "./data/agents/*.npy"):
    agent_indication_raw_value_list=[]
    fn_list = glob.glob(path)
    for fn in fn_list:
        cell =  np.load(fn)
        agent_indication_raw_value_list.append(cell)

    env = gym.make("CliffWalking-v0", #"CliffWalking-v0",
                   render_mode="rgb_array",
                   )
    env.reset()

    observation, gym_reward, terminated, truncated, info = env.step(0) # 0 == up
    env_rendered = env.render()
    external_ground_truth_npworld = nace.world_module_numpy.NPWorld(with_observed_time=False, name="external ground truth")
    pre_update_agent_location_embedded_space_list, post_update_agent_location_embedded_space_list, modified_count, pre_update_world = external_ground_truth_npworld.update_world_from_ground_truth_NPArray(
        env_rendered,
        update_mode="VIEW",
        cell_shape_rc=(60, 60, 3),
        add_surrounding_walls=True,
        wall_code=nace.world_module_numpy.EMBEDDED_WALL_CODE,
        agent_indication_raw_value_list=agent_indication_raw_value_list,
        observed_at=1
    )

    external_ground_truth_npworld.multiworld_print([
        {"Caption": f"External:",
         "World": external_ground_truth_npworld,
         "Color": nace.color_codes.color_code_white_on_black},
    ], agent_indication_raw_value_list=agent_indication_raw_value_list)



def t3_from_string_works():
    world_str_list = [
        ['oooooooooooo',
         'of  o      o',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o      X   o',
         'oooooooooooo'], (),
        ['25,25,25,23,24,26,26,26,26,26,26,26,',
         '25,25,25,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,25,25,25,25,25,25,25,',
         '19,19,19,19,19,19,19,16,15,14,13,12,',
         '18,18,18,18,18,18,18,16,15,14,13,12,']]

    world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        world_str_list[0],
        view_dist_x=12,
        view_dist_y=5,
        agent_char_code_list=['X'],
        observed_times_str_list=world_str_list[2]
    )
    world.multiworld_print([{"World": world, "Color": nace.color_codes.color_code_white_on_blue}])

    # check all agent mappings are correct and match
    print(agent_indication_raw_value_list[0].sum())
    assert agent_indication_raw_value_list[0].sum() == 5025090 # ensure we get the same raw agent value each time.
    agent_embedded_value = world.get_val_for_rgb_cell(agent_indication_raw_value_list[0])
    v = world.get_embedded_val_rc(5,7)
    v2 = world.get_val_for_char('X')
    assert v2 == v

    # check bottom right cell has correct time
    assert world.get_time_at_rc(6,11) == 12




def t8_windowsing_function():


    world_str_list = [
        ['oooooooooooo',
         'of  o      o',
         'o   a      o',
         'o   oooooooo',
         'o   b   u  o',
         'o   c  X   o',
         'oooooooooooo'], (),
        ['25,25,25,23,24,26,26,26,26,26,26,26,',
         '25,25,25,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,25,25,25,25,25,25,25,',
         '19,19,19,19,19,19,19,16,15,14,13,12,',
         '18,18,18,18,18,18,18,16,15,14,13,12,']]

    world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        world_str_list[0],
        agent_char_code_list=['X'],
        observed_times_str_list=world_str_list[2],
    )

    # check points to copy windows correctly
    points_to_copy = world._get_windowed_rc_locations(rc_locations=[(3,3)], whole_screen_raw_width=12, whole_screen_raw_height=7, cell_width=1, cell_height=1)
    assert (0, 0) in points_to_copy
    assert (5, 5) in points_to_copy

    # create e new world, copy from ground truth into it
    internal_world = nace.world_module_numpy.NPWorld(with_observed_time=True, name="self.internal_world", view_dist_x=3,
                                  view_dist_y=2,
                                  )
    internal_world.update_world_from_ground_truth(1, external_ground_truth_world_model=world, rc_locations=[(3,5)], agent_indication_raw_value_list=[])

    internal_world.multiworld_print([{"World": internal_world, "Color": nace.color_codes.color_code_white_on_blue}])

    # check that if we request a line we actually get it
    (line, len) = internal_world.get_board_line(3, color=None, agent_indication_embedded_value_list=['x'], no_color_on_oldest=False)
    assert  line == "..  ooooo..."




def t4_creating_a_new_world_from_string_preserves_char_mappings():
    # debug string and encodings are what was passed in

    input_world_str_list = ['.........AAAAA',
                      'AcbcbcbcbcbcbA',
                      'AbcbcbcbcbcbcA',
                      'APdededededebA',
                      'AgffffffffffhA',
                      'AAAAAAAAAAAAAA']

    world, agent_indication_raw_value_list = nace.world_module_numpy.NPWorld.from_string(
        input_world_str_list,
        view_dist_x=3,
        view_dist_y=2,
        agent_char_code_list=['P'],
        observed_times_str_list=None
    )

    result_board_str_list = world.debug_board.split("\n")

    for i in range (max(len(result_board_str_list), len(input_world_str_list))):
        input_line = ""
        if i < len(input_world_str_list):
            input_line = input_world_str_list[i]

        result_line = ""
        if i < len(result_board_str_list):
            result_line = result_board_str_list[i]

        print(i, input_line.rjust(40), result_line.rjust(40), "SAME" if input_line==result_line else "DIFF")



    assert world.debug_board.split("\n") == input_world_str_list



if __name__ == "__main__":
    t4_creating_a_new_world_from_string_preserves_char_mappings()
    t8_windowsing_function()


    t3_from_string_works()
    t2_can_find_agent("../data/agents/*.npy")
    t1_world_print("../data/agents/*.npy")
