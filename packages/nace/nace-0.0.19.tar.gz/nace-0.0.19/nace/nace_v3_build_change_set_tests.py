from nace.nace_v3 import _build_change_sets
from nace.world_module_numpy import NPWorld
import nace


def t_1_basic():
        old_world_str_list = [
            ['oooooooooooo',
             'o          o',
             'o x        o',
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

        old_world, _1 = NPWorld.from_string(
            old_world_str_list[0],
            view_dist_x=12,
            view_dist_y=5,
            agent_char_code_list=['x'],
            observed_times_str_list=old_world_str_list[2]
        )

        new_world_str_list = [
            ['oooooooooooo',
             'o          o',
             'o  x       o',
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
        new_world, _2 = NPWorld.from_string(
            new_world_str_list[0],
            view_dist_x=12,
            view_dist_y=5,
            agent_char_code_list=['x'],
            observed_times_str_list=new_world_str_list[2])

        predicted_world, _3 = NPWorld.from_string(
            old_world_str_list[0], # NOTE: we pass in old world, i.e. we predicted no change
            view_dist_x=12,
            view_dist_y=5,
            agent_char_code_list=['x'],
            observed_times_str_list=old_world_str_list[2]
        )


        new_world.multiworld_print([
            {"World": old_world,       "Caption":"Old", "Color": nace.color_codes.color_code_white_on_blue},
            {"World": predicted_world, "Caption":"Pred", "Color": nace.color_codes.color_code_white_on_blue},
            {"World": new_world,       "Caption":"New", "Color": nace.color_codes.color_code_white_on_blue},
        ])

        action = 'move'
        focus_set = {}

        # Call the function
        new_focus_set, adjacent_change_sets, changeset0len = _build_change_sets(
            focus_set,
            old_world,
            action,
            new_world,
            predicted_world,
        )

        val = new_world.get_val_for_char('x')
        # Assertions to check the function behavior
        assert val in new_focus_set
        assert new_focus_set[val] == 1
        assert adjacent_change_sets == [{(2, 2), (2, 3)}]


def t2_diagonal_down_right():
    old_world_str_list = [
        ['oooooooooooo',
         'o          o',
         'o x        o',
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

    old_world, _1 = NPWorld.from_string(
        old_world_str_list[0],
        view_dist_x=12,
        view_dist_y=5,
        agent_char_code_list=['x'],
        observed_times_str_list=old_world_str_list[2]
    )

    new_world_str_list = [
        ['oooooooooooo',
         'o          o',
         'o          o',
         'o  x       o',
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
    new_world, _2 = NPWorld.from_string(
        new_world_str_list[0],
        view_dist_x=12,
        view_dist_y=5,
        agent_char_code_list=['x'],
        observed_times_str_list=new_world_str_list[2])

    predicted_world, _3 = NPWorld.from_string(
        old_world_str_list[0],  # NOTE: we pass in old world, i.e. we predicted no change
        view_dist_x=12,
        view_dist_y=5,
        agent_char_code_list=['x'],
        observed_times_str_list=old_world_str_list[2]
    )

    new_world.multiworld_print([
        {"World": old_world, "Caption": "Old", "Color": color_codes.color_code_white_on_blue},
        {"World": predicted_world, "Caption": "Pred", "Color": color_codes.color_code_white_on_blue},
        {"World": new_world, "Caption": "New", "Color": color_codes.color_code_white_on_blue},
    ])

    action = 'move'
    focus_set = {}

    # Call the function
    new_focus_set, adjacent_change_sets, changeset0len = _build_change_sets(
        focus_set,
        old_world,
        action,
        new_world,
        predicted_world,
    )

    val = new_world.get_val_for_char('x')
    # Assertions to check the function behavior
    assert val in new_focus_set
    assert new_focus_set[val] == 1
    expected_change_set = [{(2, 2), (3, 3)}]
    assert len(adjacent_change_sets) == len(expected_change_set)
    for i in range(len(expected_change_set)):
        assert adjacent_change_sets[i] == expected_change_set[i]


if __name__ == '__main__':
    t_1_basic() # passes
    t2_diagonal_down_right()

