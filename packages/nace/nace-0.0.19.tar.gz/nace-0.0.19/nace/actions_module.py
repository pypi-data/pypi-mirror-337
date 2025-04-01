"""

Used to hold a master list of current valid actions, and convert to/from gym actions

"""
import gymnasium
import numpy as np
from gymnasium.spaces import Space

import nace.prettyprint


class NaceGymActionMapper():
    """
    Maintains mappings of actions between the 2 representations,
    - Gymnasium Actions (int.64) that may not be in sequence
        and
    - 'Nice' names that can be of any type, but being human-readable is useful.

    """

    def __init__(self,
                 gym_action_space: Space,
                 extend_beyond_configured_actions: bool,
                 gym_to_nace_name_mapping):
        """

        @param gym_action_space:
        @param extend_beyond_configured_actions: if True, if the gym environment says there are 20 actions, we will use all.
        """
        self.nace2gym = {}
        self.gym2nace = {}

        if isinstance(gym_action_space, gymnasium.spaces.box.Box):
            # Box (-2, 2, (7,), float32) - meaning 7 actions each with a value between -2 and 2 of type float 32
            pass # TBC
        elif isinstance(gym_action_space, Space):
            for gym_value, nace_value in gym_to_nace_name_mapping.items():
                self.nace2gym[nace_value] = gym_value
                self.gym2nace[gym_value] = nace_value

            if extend_beyond_configured_actions:
                # part of the action space is hard coded, the rest have to be learnt.
                for i in range(gym_action_space.n.item()):
                    gym_value = np.int64(i)
                    if gym_value not in self.gym2nace:
                        nace_action = int(i)
                        self.gym2nace[gym_value] = nace_action
                        self.nace2gym[nace_action] = gym_value

    def convertToGymAction(self, nace_action):
        nace_action_name = nace.prettyprint.get_pretty_action(nace_action)
        return np.int64(self.nace2gym[nace_action]), nace_action_name

    def get_full_action_list(self):
        # create a copy, and use a type that can be pickled.
        result = []
        result.extend(self.nace2gym.keys())
        return result
