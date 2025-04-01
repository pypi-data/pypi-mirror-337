import copy


class Agent():
    """
    Holds the state of the agent, including location, and 'internal' arbitrary values (num keys held)
    """

    INDEX_SCORE = 0
    INDEX_TERMINATED = 1
    PREFIX_LENGTH = max(INDEX_SCORE, INDEX_TERMINATED) + 1

    def __init__(self, rc_loc, score, terminated=0, values_excluding_prefix=()):
        """

        @param rc_loc: row column location of the agent. Ideally should not be used in learning.
        @param score: Cumulative reward for the current episode. Can/is reset at termination
        @param terminated: True if the episode was terminated i.e. dead or reset
        @param values_excluding_prefix: Env specific values, i.e. keys held
        """
        # location is stored, but not part of agent state for purpose of learning, as ground truth is from the world.
        self.rc_loc = rc_loc
        # ideally the terminated flag would be optimised out, the agent would learn the pattern resets, but it
        # is needed to learn to avoid a reset where one is not needed.
        prefix = [score] + [int(terminated)]
        self.values = prefix + list(values_excluding_prefix)

    def __eq__(self, other):
        if not isinstance(other, Agent):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return (
                self.rc_loc == other.rc_loc and
                self.values == other.values
        )

    @staticmethod
    def new_default_instance(rc_loc):
        return Agent(rc_loc, 0, 0, [])

    @staticmethod
    def get_prefix_length():
        return Agent.PREFIX_LENGTH

    def set_rc_loc(self, rc_loc):
        self.rc_loc = rc_loc

    def get_rc_loc(self):
        return copy.deepcopy(self.rc_loc)

    def set_score(self, score):
        self.values[Agent.INDEX_SCORE] = score

    def get_score(self):
        return self.values[Agent.INDEX_SCORE]

    def get_terminated(self):
        return self.values[Agent.INDEX_TERMINATED]

    def get_values_for_precondition(self):
        # Return all values EXCLUDING score, which matches a rule's PRE-CONDITION,
        # but note the effect includes the score.

        # Contains all the values that are needed to be included to see if agent state is the same for the
        # purposes of planning, i.e. includes terminated, but not score, as being in the same place with the same
        # things but with a greater score should be the same. This is used in the rule preconditions.

        # NOTE: adding anything into the agents values that has a large number of
        # discrete values explodes the size of the stored rules.
        return copy.deepcopy(self.values[1:])

    def get_values_exc_prefix(self):
        # this is used to generate code for the purposes of unit tests, and matches a param in the constructor.

        # NOTE: adding anything into the agents values that has a large number of
        # discrete values explodes the size of the stored rules.
        return copy.deepcopy(self.values[2:])

    def get_values_inc_prefix(self):
        # NOTE: extending the length of the values may explode the size of the planning space.
        return copy.deepcopy(self.values)

    def set_values_inc_prefix(self, values):
        self.values = list(copy.deepcopy(values))

    def accumulate_values_incl_prefix(self, values):
        for i in range(len(values)):
            if i < len(self.values):
                self.values[i] += values[i]
