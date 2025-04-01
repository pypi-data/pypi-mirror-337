import nace

from nace.world_module_numpy import NPWorld
from nace.numpy_utils import convert_string_list_to_cells

def t1_from_string_list():
    str_list = [
        ['oooooooooooo',
         'o          o',
         'o X        o',
         'o          o',
         'o          o',
         'o          o',
         'oooooooooooo'], (),
        ['0,0,0,0,0,0,0,0,0,0,0,0,',
         '0,0,0,0,0,0,0,0,0,0,0,0,',
         '0,0,0,0,0,0,0,0,0,0,0,0,',
         '0,0,0,0,0,0,0,0,0,0,0,0,',
         '0,0,0,0,0,0,0,0,0,0,0,0,',
         '0,0,0,0,0,0,0,0,0,0,0,0,',
         '0,0,0,0,0,0,0,0,0,0,0,0,']]
    # old_world = NPWorld.from_string_list(old_world_str_list)

    view_dist_x=12
    view_dist_y=5
    board_list_of_str = str_list[0]
    cell_shape_rc=(45, 180, 3)
    char_to_rgb_mapping, rgb_to_char_mapping, raw_rgb_array = convert_string_list_to_cells(board_list_of_str, cell_shape_rc=cell_shape_rc)

    assert raw_rgb_array.shape == (315,2160,3)

    # lookup the rgb ndarray value of the agent
    agent_indication_raw_value_list = [char_to_rgb_mapping["X"]]

    # a map can be created with no board
    world = NPWorld(with_observed_time=True, name="from_string()",
                    initial_value=nace.world_module_numpy.UNOBSERVED_BOARD_VALUE,
                    view_dist_x=view_dist_x, view_dist_y=view_dist_y,
                    rgb_to_char_mapping=rgb_to_char_mapping,
                    raw_nptype=type(raw_rgb_array[0][0][0]),
                    raw_cell_shape=cell_shape_rc,
                    agent_indication_raw_value_list=agent_indication_raw_value_list

                    )

    world.multiworld_print([
        {"Caption": f"Blank Expected (no board):",
         "World": world,
         "Color": nace.color_codes.color_code_white_on_black},
    ], agent_indication_raw_value_list=agent_indication_raw_value_list)

    world.update_world_from_ground_truth_NPArray(
        raw_rgb_array,
        update_mode='VIEW',
        wall_code=nace.world_module_numpy.EMBEDDED_WALL_CODE,
        observed_at=float('-inf'),  # -inf == never seen
        agent_indication_raw_value_list=agent_indication_raw_value_list,
        cell_shape_rc = (45, 180, 3)
        )

    world.multiworld_print([
        {"Caption": f"Should have a board:",
         "World": world,
         "Color": nace.color_codes.color_code_white_on_black},
    ], agent_indication_raw_value_list=agent_indication_raw_value_list)


    return world

def t2_from_string_list():

    str_list = \
        ['oooooooooooo',
         'o          o',
         'o X        o',
         'o          o',
         'o          o',
         'o          o',
         'oooooooooooo']

    world, agent_indication_raw_value_list = NPWorld.from_string(str_list, agent_char_code_list=['X'])
    world.multiworld_print([
        {"Caption": f"Should have a board:",
         "World": world,
         "Color": nace.color_codes.color_code_white_on_black},
    ], agent_indication_raw_value_list=agent_indication_raw_value_list)

    location = world.extract_agent_location_raw(agent_indication_raw_value_list)
    print(location)
    assert location == (2,2)


if __name__ == "__main__":
    t1_from_string_list()
    t2_from_string_list()