import copy
import json
import os.path

import numpy as np
import xxhash
# from nace.numpy_utils import convert_string_list_to_cells
from bidict import bidict

import nace
import nace.color_codes
import nace.numpy_utils

try:
    import cv2  # pip install opencv-python

    is_cv2_installed = True
except ImportError as e:
    is_cv2_installed = False

EMBEDDED_WALL_CODE = -1
UNOBSERVED_BOARD_VALUE = -2


class NPWorld():

    def __init__(self, with_observed_time, name, width=None, height=None,
                 initial_value=UNOBSERVED_BOARD_VALUE,
                 view_dist_x=3, view_dist_y=2,
                 store_raw_cell_data=True,
                 raw_cell_data_location='./data/tmp',
                 rgb_to_char_mapping={},  # used to force a raw value to a certain char for ease of debugging
                 raw_nptype=None,
                 raw_cell_shape=None,
                 agent_indication_raw_value_list=[],  # if known, what the agent can look like is very handy
                 user_set_int_2from_char_mapping=[],  #
                 ):
        self.name = name
        if width is None or height is None:
            self.board = np.zeros((0, 0), dtype=np.int64)
        else:
            self.board = np.zeros((width, height), dtype=np.int64)
            self.board[:] = initial_value

        self.initial_value = initial_value
        self.with_observed_time = with_observed_time

        self.times = np.zeros((0, 0), dtype=np.float16)  # this seems expensive in space, a float16 for each cell. hmmm
        self.times[:] = float('-inf')
        # self.agent_location_column = -1 # if cells, in cell units
        # self.agent_location_row = -1 # if cells, in cell units
        self.view_dist_x = view_dist_x
        self.view_dist_y = view_dist_y
        self.raw_cell_data_location = raw_cell_data_location
        self.store_raw_cell_data = store_raw_cell_data
        self.debug_board = ""

        # Type of the cell in raw input, often set latter, set once, can not be changed.
        self.raw_nptype = raw_nptype  # Must be set if rgb_to_char_mapping is passed in.
        self.raw_cell_shape = raw_cell_shape  # Must be set if rgb_to_char_mapping is passed in.
        if rgb_to_char_mapping is not None and rgb_to_char_mapping != {} and (
                raw_nptype == None or raw_cell_shape is None):
            raise ("If rgb_to_char_mapping is passed in, raw_nptype AND raw_cell_shape must be set as well.")

        self.int_2from_rgb_mapping = bidict()  # updated whenever a hash code is calculated
        self.int_2from_char_mapping = bidict()  # updated when the char encoding is needed.

        # Set special values
        self.int_2from_char_mapping[EMBEDDED_WALL_CODE] = 'A'
        self.int_2from_char_mapping[UNOBSERVED_BOARD_VALUE] = '.'

        for (k, v) in user_set_int_2from_char_mapping:
            assert isinstance(k, int)
            assert isinstance(v, str)
            self.int_2from_char_mapping[k] = v

        # convert external agent images to internal values
        agent_indication_raw_value_list = self._convert_raw_to_embedded_values(agent_indication_raw_value_list)

        # add any hard coded values the user has passes in (i.e. when testing and setting the map)
        for rgb_bytes, ch in rgb_to_char_mapping.items():
            if ch in self.int_2from_char_mapping.values():
                val = self.int_2from_char_mapping.inverse[ch]
            else:
                rgb_cell = self._convert_bytes_to_rgb_ndarray(rgb_bytes)
                val = self.get_val_for_rgb_cell(rgb_cell)

            self.int_2from_rgb_mapping[val] = rgb_bytes
            self.int_2from_char_mapping[val] = ch
            assert ch == self._decode_val_to_char(val, agent_indication_raw_value_list)

    def __eq__(self, other):
        if not isinstance(other, NPWorld):
            # don't attempt to compare against unrelated types
            return NotImplemented

        comparison = self.board == other.board
        board_matches = comparison.all()
        comparison = self.times == other.times
        times_match = comparison.all()

        return (
                board_matches and
                self.initial_value == other.initial_value and
                self.with_observed_time == other.with_observed_time and
                times_match and
                self.view_dist_x == other.view_dist_x and
                self.view_dist_y == other.view_dist_y and
                self.raw_cell_data_location == other.raw_cell_data_location and
                self.store_raw_cell_data == other.store_raw_cell_data and
                self.debug_board == other.debug_board and
                self.raw_nptype == other.raw_nptype and
                self.raw_cell_shape == other.raw_cell_shape and
                self.int_2from_rgb_mapping == other.int_2from_rgb_mapping and
                self.int_2from_char_mapping == other.int_2from_char_mapping
        )

    # ======= START of Value / rgb array / Char Mapping Calculations ========== #

    """
    must have embedded wall value, so it can be added round board
    must have unobserved value, so it can be treated differently (should prevent bugs)
    
    if we want these to be assigned to random rgb values for testing, then we need RGB <> Int <> Char mappings
    
    """

    def _get_new_non_reserved_char(self, v):
        # calculate a new non reserved char (lowercase and beyond)
        max_char = chr(ord('a') - 1)  # one before 'a' so first char is 'a'
        if len(self.int_2from_char_mapping.values()) > 0:
            max_char = max(max_char, max(self.int_2from_char_mapping.values()))
        new_char = chr(ord(max_char) + 1)
        assert v not in self.int_2from_char_mapping
        if isinstance(v, np.int64):
            self.int_2from_char_mapping[v.item()] = new_char
        else:
            assert isinstance(v, int)
            self.int_2from_char_mapping[v] = new_char

        return new_char

    def _decode_val_to_char(self, v, agent_indication_embedded_value_list):
        # negative values, and uppercase char are reserved.
        # int_2from_char_mapping and int_2from_rgb are first class citizens

        # if v == EMBEDDED_WALL_CODE:
        #     return 'A'
        # if v == UNOBSERVED_BOARD_VALUE:
        #     return '.'

        if v in self.int_2from_char_mapping:
            return self.int_2from_char_mapping[v]

        # ensure the embedded agent values have Char encodings
        for embedded_value in agent_indication_embedded_value_list:
            if embedded_value not in self.int_2from_char_mapping:  # can't be due to above logic
                max_char = 'A'  # A reserved for walls, B-Z reserved for agents
                if len(self.int_2from_char_mapping.values()) > 0:
                    max_char = max(max_char,
                                   max([ch for ch in self.int_2from_char_mapping.inverse.keys() if ch <= 'Z']))
                if max_char == 'Z':
                    # run out of B-Z for agent, must now use general range
                    pass
                else:
                    new_char = chr(ord(max_char) + 1)
                    self.int_2from_char_mapping[embedded_value] = new_char

        # value may have been added in the last block, check again and return if present
        if v in self.int_2from_char_mapping:
            return self.int_2from_char_mapping[v]

        # calculate a new non reserved char (lowercase and beyond)
        new_char = self._get_new_non_reserved_char(v)

        return new_char

    def _convert_bytes_to_rgb_ndarray(self, rgb_bytes):

        assert self.raw_nptype is not None
        deserialized_bytes = np.frombuffer(rgb_bytes, dtype=self.raw_nptype)
        newshape = (self.raw_cell_shape[0], self.raw_cell_shape[1], self.raw_cell_shape[2])
        rgb = np.reshape(deserialized_bytes, newshape=newshape)
        return rgb

    def get_val_for_char(self, c):
        if c in self.int_2from_char_mapping.inverse:
            return self.int_2from_char_mapping.inverse[c]
        raise Exception("Mapping not found for chr '" + str(c) + "'")

    def get_val_to_char_mappings(self, list_of_extra_values=[]):
        # this routine could be simplified, too much looping.
        # return the mappings as of now (they can be updated of course)
        char_set = set([ch for ch in self.debug_board])
        result = {}
        for ch in char_set:
            if ch != '\n':
                val = self.get_val_for_char(ch)
                result[val] = ch
        for val in list_of_extra_values:
            if val in self.int_2from_char_mapping:
                ch = self.int_2from_char_mapping[val]
                result[val] = ch
            else:
                # this is probably caused by not knowing whether the code (and image) in question is an agent or
                # not, and we do not know how to encode it.
                # calculate a new non reserved char (lowercase and beyond)
                new_char = self._get_new_non_reserved_char(val)
                print("WARN can not convert "+str(val)+" to char for debugging purposes. Created a new non reserved char. ", new_char)
                result[val] = new_char

        for val in self.int_2from_char_mapping:
            result[val] = self.int_2from_char_mapping[val]

        return result

    def get_val_for_rgb_cell(self, rgb_cell: np.ndarray):
        # generates an embedded int value for a rgb cell and stores it in self.int_2from_rgb_mapping
        # for fast lookup later

        if self.raw_cell_shape is None:
            self.raw_cell_shape = rgb_cell.shape
        if self.raw_nptype is None:
            self.raw_nptype = type(rgb_cell[0][0][0])

        for dim in [0, 1, 2]:
            if rgb_cell.shape[dim] != self.raw_cell_shape[dim]:
                print("DEBUG rgb_cell.shape", rgb_cell.shape)
                print("DEBUG self.raw_cell_shape", self.raw_cell_shape)

            assert rgb_cell.shape[dim] == self.raw_cell_shape[dim]
        assert isinstance(rgb_cell[0][0][0], self.raw_nptype)

        rgb_bytes = rgb_cell.data.tobytes()
        if rgb_bytes in self.int_2from_rgb_mapping.values():  # return previous values (alows us to overide hashcode for special values
            return self.int_2from_rgb_mapping.inverse[rgb_bytes]

        hc = xxhash.xxh32(rgb_bytes).intdigest()  # should be repeatable between restarts.
        # this is to fix the issue that the hash code are not deterministic, between restarts
        # they can change, this means we can not serialize a knowledge base of rules.
        hci = int(hc)
        # hci = hci % 2147483647 # np int limit. wrap values (more chance of collision, but can be stored in int)

        if self.raw_cell_shape is None:
            self.raw_cell_shape = (rgb_cell.shape[0], rgb_cell.shape[1], rgb_cell.shape[2])
            if len(self.raw_cell_shape) >= 3:
                assert self.raw_cell_shape[2] == 3
        else:
            assert (self.raw_cell_shape[0] == rgb_cell.shape[0] and
                    self.raw_cell_shape[1] == rgb_cell.shape[1] and
                    self.raw_cell_shape[2] == rgb_cell.shape[2])

        return hci

    # ======= END of Value / rgb array / Char Mapping Calculations ========== #

    def get_unobserved_code(self):
        return UNOBSERVED_BOARD_VALUE

    def get_char_at_rc(self, row, col, agent_indication_embedded_value_list):
        " We store integers in each cell, this decodes to 'nice' char values"
        return self._decode_val_to_char(self.board[row, col], agent_indication_embedded_value_list)

    def set_embedded_val_rc(self, row: int, col: int, val: int):
        self.board[row, col] = val

    def get_embedded_val_rc(self, row: int, col: int):
        return self.board[row, col].item()

    def get_time_at_rc(self, row, col):
        return self.times[row, col]

    def get_newest_time(self):
        """
        @return: the must recent, up-to-date time stored in the world.
        """
        if self.with_observed_time:
            if self.times.shape[0] > 0:
                return max(0, self.times.max())
        return 0

    def get_locations_updated_tminus(self, time_delta=1):
        newest_time = self.get_newest_time()
        search_time = newest_time - time_delta
        locations = [(r.item(), c.item()) for (r, c) in zip(*np.where(self.times == search_time))]
        return locations

    def get_board_line(self, row_number, color, agent_indication_embedded_value_list, no_color_on_oldest=False):
        if self.with_observed_time and self.times.size > 0:
            oldest_time = self.times.min().item()
        else:
            oldest_time = float('-inf')
        line = ""
        color_count = 0
        if row_number < self.board.shape[0]:
            for col in range(self.board.shape[1]):
                if self.with_observed_time and self.times[row_number][col] == oldest_time and no_color_on_oldest:
                    line += nace.color_codes.color_code_black_on_white
                    color_count += 1
                line += self.get_char_at_rc(row_number, col, agent_indication_embedded_value_list)

                if self.with_observed_time and self.times[row_number][col] == oldest_time:
                    if color != None:
                        line += color
        return line, self.board.shape[1]

    def get_in_nace_board_format(self):
        board = []
        for row in range(self.board.shape[0]):
            line = []
            for col in range(self.board.shape[1]):
                line.append(self.get_char_at_rc(row, col))
            board.append(line)
        return board

    def _reset_non_board(self):
        # set the times and other values to the default
        if self.with_observed_time:
            self.times = np.zeros(self.board.shape, dtype=np.float16)  # this seems expensive in space. hmmm
            self.times[:] = float('-inf')

    def _set_board_size(self, height, width):
        prior_board_shape = self.board.shape
        size_changed = False
        if prior_board_shape == (0, 0):
            # we need to reset all other values
            self.board = np.zeros((height, width), dtype=np.int64)
            self.board[:] = self.initial_value
            self._reset_non_board()
            size_changed = True

        return prior_board_shape, size_changed

    def _get_windowed_rc_locations(self, rc_locations, whole_screen_raw_width, whole_screen_raw_height, cell_width=1,
                                   cell_height=1):
        """
        Return a list of points within view distance of the agents(s) rc_locations
        """
        if rc_locations == []:
            return []  # speed optimisation
        rc_points_to_copy = []
        rows = list(range(self.view_dist_y * 2 + 1))
        columns = list(range(self.view_dist_x * 2 + 1))

        for r_delta in rows:
            for c_delta in columns:
                for rc_loc in rc_locations:
                    if len(rc_loc) < 2:
                        raise Exception("Type logic Error")
                    if isinstance(rc_loc[1], tuple) or isinstance(r_delta, tuple) or isinstance(self.view_dist_y,
                                                                                                tuple):
                        print("breakpoint")
                    r = rc_loc[0] + r_delta - self.view_dist_y
                    c = rc_loc[1] + c_delta - self.view_dist_x
                    if r >= 0 and r * cell_height < whole_screen_raw_height and \
                            c >= 0 and c * cell_width < whole_screen_raw_width:
                        rc_points_to_copy.append((r, c))
        rc_points_to_copy = list(set(rc_points_to_copy))  # ensure unique
        return rc_points_to_copy

    @staticmethod
    def extract_cell(r: int, c: int, observed_ndarray: np.ndarray, cell_shape_rc=(1, 1)):
        assert (r + 1) * cell_shape_rc[0] <= observed_ndarray.shape[0] + 1
        assert (c + 1) * cell_shape_rc[1] <= observed_ndarray.shape[1] + 1
        cell = observed_ndarray[r * cell_shape_rc[0]:(r + 1) * cell_shape_rc[0],
               c * cell_shape_rc[1]:(c + 1) * cell_shape_rc[1]
               ]
        return cell

    def _convert_raw_to_embedded_values(self, agent_indication_raw_value_list):
        agent_indication_embedded_value_list = [self.get_val_for_rgb_cell(cell) for cell in
                                                agent_indication_raw_value_list]
        return agent_indication_embedded_value_list

    def _copy_mappings_from_source_to_self(self, v: int, source_world):
        if self.raw_cell_shape is not None and source_world.raw_cell_shape is not None:
            if self.raw_cell_shape != source_world.raw_cell_shape:
                raise Exception("Cell shape already set, and can not be changed")

        if self.raw_cell_shape is None and source_world.raw_cell_shape is not None:
            self.raw_cell_shape = source_world.raw_cell_shape

        if v not in self.int_2from_rgb_mapping:
            if v in source_world.int_2from_rgb_mapping:
                rgb_bytes = source_world.int_2from_rgb_mapping[v]

                self.int_2from_rgb_mapping[v.item()] = rgb_bytes
                self.int_2from_char_mapping[v.item()] = source_world.int_2from_char_mapping[v]

    def _copy_from_source_world_to_self(self, rc_points_to_copy: list, source_world, time_counter: int):
        modified_count = 0
        for (r, c) in rc_points_to_copy:
            if source_world.board[r][c] != UNOBSERVED_BOARD_VALUE:
                v = source_world.board[r][c]
                if self.board[r][c] != v:
                    self.board[r][c] = v
                    self._copy_mappings_from_source_to_self(v, source_world)
                    modified_count += 1
                if self.with_observed_time:
                    self.times[r][c] = time_counter
        return modified_count

    def update_world_from_ground_truth(
            self,
            time_counter: int,
            external_ground_truth_world_model,  # type:NPWorld
            rc_locations,  # list of locations, around which data is copied from external to internal world.
            # (Usually just where the agent is)
            agent_indication_raw_value_list: list):

        rc_locations = copy.deepcopy(rc_locations)
        height = external_ground_truth_world_model.board.shape[0]
        width = external_ground_truth_world_model.board.shape[1]

        previous_size, size_changed = self._set_board_size(
            height=height,
            width=width)
        if size_changed:
            if previous_size != (0, 0):
                print("ERROR: should not change in size. ")
                raise Exception("Changing board size once initialised not supported.")

        pre_action_internal_world = copy.deepcopy(self)

        # add the last known place of the agents to the list of update locations, as the agent may have 'jumped'
        agent_last_rc_location = self.extract_agent_location_raw(agent_indication_raw_value_list)
        if len(agent_last_rc_location) > 0:
            assert isinstance(agent_last_rc_location, tuple)
            if agent_last_rc_location != (-1, -1):
                rc_locations.append(agent_last_rc_location)
            else:
                print("ERROR no know last location. Maybe there is no agent. Check last screen shot. And that all images of agent are in agents dir (along with matching .npy file). rc_locations=",str(rc_locations))

        if len(agent_last_rc_location) == 0:
            print("ERROR - logic error? will the next line now fail?")

        # Filter out negative (illegal) values (which indicate location is unknown)
        rc_locations = [t for t in rc_locations if t is not None]
        rc_locations = [(r, c) for (r, c) in rc_locations if r >= 0 and c >= 0]

        # uses view distance, and only returns points in that distance
        rc_points_to_copy = self._get_windowed_rc_locations(rc_locations, width, height)
        modified_count = self._copy_from_source_world_to_self(rc_points_to_copy, external_ground_truth_world_model,
                                                              time_counter)

        if modified_count == 0:
            pass

        agent_indication_embedded_value_list = self._convert_raw_to_embedded_values(agent_indication_raw_value_list)
        self.debug_board = self.board_as_string(agent_indication_embedded_value_list)

        # self.multiworld_print([{"World": self, "Caption":self.name, "Color":nace.color_codes.color_code_white_on_red}])

        return modified_count, pre_action_internal_world

    def _save_new_cells(self, observed_ndarray: np.ndarray, cell_shape_rc: tuple,
                        agent_indication_raw_value_list: list):

        if len(agent_indication_raw_value_list) > 0 and type(agent_indication_raw_value_list[0]) == str:
            # we are using char input rather than rgb, do not save to disk.
            return

        """ Save cell images to disk for ease of debugging"""
        agent_indication_embedded_value_list = list(set([
            self.get_val_for_rgb_cell(cell) for cell in agent_indication_raw_value_list if
            cell.shape == self.raw_cell_shape
        ]))
        for embedded_r in range(int(observed_ndarray.shape[0] / cell_shape_rc[0])):
            for embedded_c in range(int(observed_ndarray.shape[1] / cell_shape_rc[1])):
                # embedded_r, embedded_c are in input space units, i.e. no walls, and in cells
                cell = NPWorld.extract_cell(embedded_r, embedded_c, observed_ndarray, cell_shape_rc=cell_shape_rc)
                cell_embedded_value = self.get_val_for_rgb_cell(cell)
                if self.store_raw_cell_data:
                    if cell_embedded_value not in agent_indication_embedded_value_list:
                        # don't store the images of the known agents, so it is easy to see if new agent values exisit ( ma nually)
                        fn = os.path.join(self.raw_cell_data_location, str(cell_embedded_value) + '.png')
                        if os.path.exists(self.raw_cell_data_location):
                            if not os.path.isfile(fn):
                                if is_cv2_installed:
                                    cv2.imwrite(fn, cell)
                                else:
                                    print("WARN: not saving image as cv2 not installed.")

                            fn = os.path.join(self.raw_cell_data_location, str(cell_embedded_value) + '.npy')
                            if not os.path.isfile(fn):
                                np.save(fn, cell)  # .npy extension is added if not given
        if self.store_raw_cell_data:
            fn = os.path.join(self.raw_cell_data_location, 'screen' + '.png')
            if is_cv2_installed:
                cv2.imwrite(fn, observed_ndarray)
            else:
                print("WARN: not saving image as cv2 not installed.")

    def update_world_from_ground_truth_NPArray(
            self,
            observed_ndarray: np.ndarray,
            update_mode: str,  # 'ALL' or 'VIEW'
            cell_shape_rc: tuple,  # shape of each cell
            add_surrounding_walls: bool = True,
            wall_code: int = EMBEDDED_WALL_CODE,  # int for ansi
            agent_indication_raw_value_list=['B'],
            observed_at: float = float('-inf')):
        """

        Notes:
        - observed_world may be of a larger size than the board, i.e. each 60x60x3 cell may map to a single board
            cell/value.
        - observed_world may not have a 'wall' around it, which can be added if configured to make later logic
             simplier.

        @param observed_ndarray:
                if rgb_shape is None then ndarray shape (1,n,m)
                else (n,m,3)
        @param add_surrounding_walls: bool
        @param wall_code: call value of optional surrounding wall
        @param raw_agent_indication_value: value indication current cell contains an agent
        @param observed_at: the time of the observation
        @return:
        """

        assert update_mode in ['ALL', 'VIEW'], ("update mode must be one of ALL (updates the whole board), or 'VIEW' "
                                                "(updates cells close to agents only)")

        pre_update_world = copy.deepcopy(self)
        modified_count = 0
        modified_locations_embedded_rc = []
        if self.store_raw_cell_data: # dv added 5 feb 2024
            self._save_new_cells(observed_ndarray, cell_shape_rc, agent_indication_raw_value_list)

        if add_surrounding_walls:
            double_wall_size = 2
            wall_thickness = 1
        else:
            double_wall_size = 0
            wall_thickness = 0

        if self.raw_cell_shape is None:
            self.raw_cell_shape = cell_shape_rc
        else:
            if self.raw_cell_shape != cell_shape_rc:
                raise Exception("changing board shape not supported.")

        # a group of elements in observed maps to 1 in the internal
        prior_board_shape, size_changed = self._set_board_size(
            height=int(observed_ndarray.shape[0] / self.raw_cell_shape[0]) + double_wall_size,
            width=int(observed_ndarray.shape[1] / self.raw_cell_shape[1]) + double_wall_size)

        if prior_board_shape != (0, 0):
            if prior_board_shape != self.board.shape:
                raise Exception("Changing board size/shape in flight not yet supported.")

        if add_surrounding_walls:
            if self.board[0][0] != wall_code:
                for r in range(self.board.shape[0]):
                    self.board[r][0] = wall_code
                    self.board[r][-1] = wall_code
                for c in range(self.board.shape[1]):
                    self.board[0][c] = wall_code
                    self.board[-1][c] = wall_code

        agent_indication_embedded_value_list = [self.get_val_for_rgb_cell(cell) for cell in
                                                agent_indication_raw_value_list if cell.shape == self.raw_cell_shape]
        # line below: 3pm 10/Dec was correct. 3:33 below incorrect mixed pre and post
        agent_current_rc_locations_in_embedded_space = self.extract_agent_locations_raw(observed_ndarray,
                                                                                        agent_indication_embedded_value_list,
                                                                                        wall_thickness)

        # check the not yet updated board for the last location
        # block below 3pm 10/Dec was correct. 3:33 below incorrect mixed pre and post
        agent_previous_rc_locations_in_embedded_space = []
        for r in range(self.board.shape[0]):
            for c in range(self.board.shape[1]):
                for raw_agent_indication_value in agent_indication_raw_value_list:
                    if raw_agent_indication_value.shape == self.raw_cell_shape:
                        embedded_agent_indication_value = self.get_val_for_rgb_cell(raw_agent_indication_value)
                        if self.board[r, c] == embedded_agent_indication_value:
                            if (r, c) not in agent_previous_rc_locations_in_embedded_space:
                                agent_previous_rc_locations_in_embedded_space.append((r, c))
        #

        # testing the below block to find agent
        # 3pm 10/Dec next line was **incorrect**
        ____post_update_agent_location_list = self.extract_agent_locations_embedded(
            agent_indication_embedded_value_list)

        # find the agents location in new observed world
        # check the passed in observed array to get the current location
        # 3pm 10/Dec was correct, but matches code above
        # agent_current_rc_locations_in_embedded_space = []
        # for raw_agent_indication_value in agent_indication_raw_value_list:
        #     if raw_agent_indication_value.shape == self.raw_cell_shape:
        #         embedded_agent_indication_value = self.get_val_for_rgb_cell(raw_agent_indication_value)
        #         for r_without_wall in range(int(observed_ndarray.shape[0] / self.raw_cell_shape[0])):
        #             for c_without_wall in range(int(observed_ndarray.shape[1] / self.raw_cell_shape[1])):
        #                 cell = NPWorld.extract_cell(r_without_wall, c_without_wall, observed_ndarray, cell_shape_rc)
        #                 v = self.get_val_for_rgb_cell(cell)
        #                 if embedded_agent_indication_value == v:
        #                     if (r_without_wall + wall_thickness,
        #                         c_without_wall + wall_thickness) not in agent_current_rc_locations_in_embedded_space:
        #                         agent_current_rc_locations_in_embedded_space.append(
        #                             (r_without_wall + wall_thickness, c_without_wall + wall_thickness))

        agent_current_and_previous_rc_locations_embedded_space = []
        agent_current_and_previous_rc_locations_embedded_space.extend(agent_current_rc_locations_in_embedded_space)
        agent_current_and_previous_rc_locations_embedded_space.extend(agent_previous_rc_locations_in_embedded_space)
        if len(agent_current_and_previous_rc_locations_embedded_space) == 0:
            # we have no agent. perhaps their appearance changed. get the location(s)
            # of cells that changed.
            # THIS CODE BLOCK may not be needed.
            # NOTE: this violates the view dist, we should only check cells around the last known agent, but if we have no idea where agent is ....
            possible_agent_locations = []
            for r in range(int(observed_ndarray.shape[0] / self.raw_cell_shape[0])):
                for c in range(int(observed_ndarray.shape[1] / self.raw_cell_shape[1])):
                    observed_cell = NPWorld.extract_cell(r, c, observed_ndarray, cell_shape_rc)
                    observed_cell_embedded_value = self.get_val_for_rgb_cell(observed_cell)
                    if observed_cell_embedded_value in agent_indication_embedded_value_list:
                        possible_agent_locations.append((r + wall_thickness, c + wall_thickness))
            if 0 < len(possible_agent_locations) <= 2:  # NOTE: limitation allows at most 2 agents
                agent_current_and_previous_rc_locations_embedded_space.extend(possible_agent_locations)
        if len(agent_current_and_previous_rc_locations_embedded_space) == 0:
            print("Could not find agent, or agent changed embedded value, i.e. looks different")

        if update_mode == 'VIEW':
            # find points to copy from external view to internal view (only that around the agent)
            # embedded_space means with walls
            rc_points_to_copy_in_embedded_space = self._get_windowed_rc_locations(
                agent_current_and_previous_rc_locations_embedded_space,
                whole_screen_raw_width=observed_ndarray.shape[1] + (2 * wall_thickness * self.raw_cell_shape[1]),
                whole_screen_raw_height=observed_ndarray.shape[0] + (2 * wall_thickness * self.raw_cell_shape[0]),
                cell_width=self.raw_cell_shape[1],
                cell_height=self.raw_cell_shape[0]
            )

        if update_mode == 'ALL':
            # find points to copy from external view to internal view (all)
            rc_points_to_copy_in_embedded_space = []
            r_limit = int(observed_ndarray.shape[0] / cell_shape_rc[0])
            c_limit = int(observed_ndarray.shape[1] / cell_shape_rc[1])
            for r in range(r_limit):
                for c in range(c_limit):
                    rc_points_to_copy_in_embedded_space.append((r + wall_thickness, c + wall_thickness))

        for dim in [0, 1]:
            assert int(observed_ndarray.shape[dim] / cell_shape_rc[dim]) == self.board.shape[dim] - (2 * wall_thickness)

        for (embedded_r,
             embedded_c) in rc_points_to_copy_in_embedded_space:  # in embedded space, with walls in units of cells
            if wall_thickness == 0 or (
                    int(observed_ndarray.shape[0] / cell_shape_rc[0]) >= embedded_r >= wall_thickness and
                    int(observed_ndarray.shape[1] / cell_shape_rc[1]) >= embedded_c >= wall_thickness):
                observed_cell = NPWorld.extract_cell(embedded_r - wall_thickness, embedded_c - wall_thickness,
                                                     observed_ndarray, cell_shape_rc=cell_shape_rc)
                embedded_value_of_observed_cell = self.get_val_for_rgb_cell(observed_cell)
                if embedded_value_of_observed_cell != self.initial_value:
                    r = embedded_r
                    c = embedded_c
                    if self.board[r][c] != embedded_value_of_observed_cell:
                        self.board[r][c] = embedded_value_of_observed_cell
                        modified_count += 1
                        modified_locations_embedded_rc.append((r, c))
                    if self.with_observed_time:
                        self.times[r][c] = float(observed_at)
                else:  # unobserved
                    pass  # leave the observed time, and board value as they are.

        self.debug_board = self.board_as_string(agent_indication_embedded_value_list)
        # self.multiworld_print([{"World": self, "Caption":self.name, "Color":nace.color_codes.color_code_white_on_red}])

        return agent_previous_rc_locations_in_embedded_space, agent_current_rc_locations_in_embedded_space, modified_count, pre_update_world

    def extract_agent_location_raw(
            self,
            agent_indication_raw_value_list):  # note there may be more than 1 agent at some stage.
        """
        return in row colum format (r,c)
        This is used by agents that need to store their location in their internal state.
        """
        agent_indication_embedded_value_list = [self.get_val_for_rgb_cell(cell) for cell in
                                                agent_indication_raw_value_list if cell.shape == self.raw_cell_shape]
        agent_locations_list = self.extract_agent_locations_embedded(agent_indication_embedded_value_list)
        if len(agent_locations_list) > 0:
            return (agent_locations_list[0][0], agent_locations_list[0][1])
        else:
            return (-1, -1)

    def extract_agent_locations_raw(self, observed_ndarray, agent_indication_embedded_value_list, wall_thickness):
        agent_locations = []
        for r in range(int(observed_ndarray.shape[0] / self.raw_cell_shape[0])):
            for c in range(int(observed_ndarray.shape[1] / self.raw_cell_shape[1])):
                observed_cell = NPWorld.extract_cell(r, c, observed_ndarray, self.raw_cell_shape)
                observed_cell_embedded_value = self.get_val_for_rgb_cell(observed_cell)
                if observed_cell_embedded_value in agent_indication_embedded_value_list:
                    agent_locations.append((r + wall_thickness, c + wall_thickness))
        return agent_locations

    def extract_agent_locations_embedded(self, agent_indication_embedded_value_list):
        agent_last_rc_locations = []
        agent_indication_embedded_value_list = list(set(agent_indication_embedded_value_list))
        for agent_value in agent_indication_embedded_value_list:
            locations = [(r.item(), c.item()) for (r, c) in zip(*np.where(self.board == agent_value))]
            if len(locations) > 0 and isinstance(locations[0], int):
                print("place breakpoint here")
            agent_last_rc_locations.extend(locations)
        return agent_last_rc_locations

    def get_list_of_differences(self, world2):
        differences = self.board != world2.board
        (row_indexes, column_indexes) = np.nonzero(
            differences)  # return 2 vectors, with all the y values in one, and x in the other
        return row_indexes, column_indexes

    def get_difference_count(self, world2):
        if world2 is None:
            return 0
        differences = self.board != world2.board
        (row_indexes, column_indexes) = np.nonzero(
            differences)  # return 2 vectors, with all the y values in one, and x in the other
        return len(row_indexes)


    def get_board_hashcode(self):
        """
        @return:
        """
        hc = xxhash.xxh32(bytes(self.board.data)).intdigest()  # should be repeatable between restarts.
        return hc

    def get_height_width(self):
        return self.board.shape[0], self.board.shape[1]

    def get_board_char_counts(self, agent_indication_embedded_value_list):
        result = {}
        unique_values = np.unique(self.board)
        for v in unique_values:
            s = np.sum(self.board == v)
            ch = self._decode_val_to_char(v, agent_indication_embedded_value_list)
            result[ch] = s.item()
        return result

    def multiworld_print(self, list_of_records, pad_length=30, agent_indication_raw_value_list=[]):
        """
        Print a number of worlds in coloured text, left to right across the screen
        @param list_of_worlds: dict e.g. [{"World":list[list[char]], "Caption":str, "Color":color code}]
        @return:
        """
        heights = [record["World"].get_height_width()[0] for record in list_of_records]
        max_lines = max(heights)
        agent_indication_embedded_value_list = [self.get_val_for_rgb_cell(cell) for cell in
                                                agent_indication_raw_value_list if cell.shape == self.raw_cell_shape]

        num_caption_lines = 1
        for world_index in range(len(list_of_records)):
            if "Caption" in list_of_records[world_index]:
                caption_list = list_of_records[world_index]["Caption"].split("\n")
                if len(caption_list) > num_caption_lines:
                    num_caption_lines = len(caption_list)

        for caption_line in range(num_caption_lines):
            line = ""
            for world_index in range(len(list_of_records)):
                caption = ""
                if "Caption" in list_of_records[world_index]:
                    caption_list = list_of_records[world_index]["Caption"].split("\n")
                    caption_list.extend(["", "", ""])
                    caption = caption_list[caption_line]
                line += caption.ljust(pad_length, " ")
            print(line)

        for line_num in range(max_lines):
            line = ""
            for world_index in range(len(list_of_records)):
                pass
                # Set the color
                color = None
                if "Color" in list_of_records[world_index]:
                    color = list_of_records[world_index]["Color"]
                    line += color
                map_line, row_length = list_of_records[world_index]["World"].get_board_line(line_num, color,
                                                                                            agent_indication_embedded_value_list)
                line += map_line
                line += nace.color_codes.color_code_black_on_white

                padding = "".join([" "] * (pad_length - row_length))
                line += padding
                # line += map_line.ljust(pad_length, " ")[len(map_line):]
            print(line)
        print()  # blank line at end

    def board_as_string(self, agent_indication_embedded_value_list):
        result = ""
        for row_number in range(self.board.shape[0]):
            for col_number in range(self.board.shape[1]):
                result += self.get_char_at_rc(row_number, col_number, agent_indication_embedded_value_list)
            result += "\n"
        return result.strip()

    def to_string_list(self):
        board_lines = []
        time_lines = []
        for row_number in range(self.board.shape[0]):
            board_line = ""
            time_line = ""
            for col_number in range(self.board.shape[1]):
                c = self.get_char_at_rc(row_number, col_number)
                board_line += c
                t = self.times[row_number][col_number]
                if t == float("-inf"):
                    time_line += "-inf,"
                else:
                    time_line += str(t) + ","
            board_lines.append(board_line)
            time_lines.append(time_line)
        return ([board_lines, (), time_lines])

    @staticmethod
    def from_string(
            board_list_of_str,
            cell_shape_rc=(45, 180, 3),
            view_dist_x=12,
            view_dist_y=5,
            agent_char_code_list=['B'],
            observed_times_str_list=None,
            numpy_seed=123,
            update_mode='ALL',
            int_2from_char_mapping=[]):
        """
        @param board_list_of_str: list[str] - each string represent 1 row.
        @return:
        """

        for line in board_list_of_str:
            if len(line.strip()) == 0:
                raise ("board lines must all be non empty and not contain space (' ')")

        add_surrounding_walls = False
        wall_thickness = 0

        char_to_rgb_mapping, rgb_to_char_mapping, raw_rgb_array = nace.numpy_utils.convert_string_list_to_cells(
            board_list_of_str,
            cell_shape_rc=cell_shape_rc,
            numpy_seed=numpy_seed)

        # lookup the rgb ndarray value of the agent
        agent_indication_raw_value_list = [char_to_rgb_mapping[agent_char_code] for agent_char_code in
                                           agent_char_code_list]

        # a map can be created with no board
        world = NPWorld(with_observed_time=True, name="from_string()",
                        initial_value=nace.world_module_numpy.UNOBSERVED_BOARD_VALUE,
                        view_dist_x=view_dist_x,
                        view_dist_y=view_dist_y,
                        rgb_to_char_mapping=rgb_to_char_mapping,
                        raw_nptype=type(list(char_to_rgb_mapping.values())[0][0][0][0]),
                        raw_cell_shape=cell_shape_rc,
                        user_set_int_2from_char_mapping=int_2from_char_mapping,
                        )

        world.multiworld_print([
            {"Caption": f"Blank Expected (no board):",
             "World": world,
             "Color": nace.color_codes.color_code_white_on_black},
        ], agent_indication_raw_value_list=agent_indication_raw_value_list)

        world.update_world_from_ground_truth_NPArray(
            raw_rgb_array,
            update_mode=update_mode,
            wall_code=nace.world_module_numpy.EMBEDDED_WALL_CODE,
            observed_at=float('-inf'),  # -inf == never seen
            agent_indication_raw_value_list=agent_indication_raw_value_list,
            cell_shape_rc=cell_shape_rc,
            add_surrounding_walls=add_surrounding_walls
        )

        if observed_times_str_list is not None:
            for row, line in enumerate(observed_times_str_list):
                time_list = line.split(",")
                for col, t_str in enumerate(time_list):
                    if t_str != '':
                        observed_time = float(t_str)
                        if row < world.times.shape[0]:
                            if col < world.times.shape[1]:
                                world.times[row + wall_thickness][col + wall_thickness] = observed_time

        world.multiworld_print([
            {"Caption": f"Should have a board:",
             "World": world,
             "Color": nace.color_codes.color_code_white_on_black},
        ], agent_indication_raw_value_list=agent_indication_raw_value_list)

        return world, agent_indication_raw_value_list

    def from_gymnasium_rgb(gym_np_world: np.ndarray,
                           agent_indication_raw_value_list=['B'],
                           add_surrounding_walls=True,
                           embedded_wall_code: int = ord('A'),
                           observed_at=float('-inf'),
                           cell_shape_rc=(60, 60),
                           store_raw_cell_data=False,
                           ):
        """

        @param gym_world: str , each \n indicates a new row, white space is stripped. agent location indicated by  agent_location_indicator_char
        @param strip_blanks:
        @param agent_location_indicator_char:  char representing the agent
        @param last_world: if not none, state and times seen copied from this world
        @param add_walls_right_and_bottom:
        @param embedded_wall_code: internal embedded value (int)
        @return:
        """

        world = NPWorld(with_observed_time=True,
                        name="from_rgb()",
                        initial_value=UNOBSERVED_BOARD_VALUE,
                        view_dist_x=3,
                        view_dist_y=2,
                        store_raw_cell_data=store_raw_cell_data)

        pre_update_agent_location_embedded_space_list, post_update_agent_location_embedded_space_list, _, _ = world.update_world_from_ground_truth_NPArray(
            gym_np_world,
            update_mode='VIEW',
            observed_at=observed_at,  # -inf == never seen
            agent_indication_raw_value_list=agent_indication_raw_value_list,
            cell_shape_rc=cell_shape_rc,
            add_surrounding_walls=add_surrounding_walls,
            wall_code=embedded_wall_code
        )
        return world, post_update_agent_location_embedded_space_list

    def get_internal_state(self):
        # do we need to store the board as well?
        int_2from_rgb_list = []
        for k in self.int_2from_rgb_mapping.keys():
            int_2from_rgb_list.append((k, self.int_2from_rgb_mapping[k]))

        int_2from_char_list = []
        for k in self.int_2from_char_mapping.keys():
            int_2from_char_list.append((k, self.int_2from_char_mapping[k]))

        result = {"int_2from_rgb_list": int_2from_rgb_list,
                  "int_2from_char_list": int_2from_char_list,
                  "raw_cell_shape": self.raw_cell_shape,
                  "raw_nptype": str(self.raw_nptype)
                  }
        # check it can be json serialised
        s = json.dumps(result)

        return result
