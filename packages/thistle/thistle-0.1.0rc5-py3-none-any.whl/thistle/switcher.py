import abc

import numpy as np
from sgp4.api import Satrec
from sgp4.conveniences import sat_epoch_datetime

from thistle.utils import (
    DATETIME_MAX,
    DATETIME_MIN,
    EPOCH_DTYPE,
    datetime_to_dt64,
)

try:
    from itertools import pairwise
except ImportError:
    from thistle.utils import pairwise


# Transition Examples
# Epoch Switching
# -     A     B     C     D     E     +
# |-----~-----|-----|-----|-----|-----|
# Transitions: n + 1
# Segments: n
#
# MidpointSWitching
# -     A     B     C     D     E     +
# |-----~--|--~--|--~--|--~--|--~-----|
# Transitions: n + 1
# Segments: n
#
# TCA Switching
# -     A     B     C     D     E     +
# |-----~--|--~--|--~--|--~--|--~-----|
# Transitions: n + 1
# Segments: n


class SwitchingStrategy(abc.ABC):
    satrecs: list[Satrec]
    transitions: np.ndarray

    def __init__(
        self,
        satrecs: list[Satrec],
    ) -> None:
        self.satrecs = sorted(satrecs, key=lambda sat: sat_epoch_datetime(sat))
        self.transitions = None

    @abc.abstractmethod
    def compute_transitions(self) -> None:
        raise NotImplementedError()


class EpochSwitcher(SwitchingStrategy):
    """Switching based on the TLE epoch.

    This TLE switching strategy selects the TLE generated with an epoch
    closest to the time without being "in the future".
    """

    def compute_transitions(self) -> None:
        transitions = [
            sat_epoch_datetime(sat).replace(tzinfo=None) for sat in self.satrecs
        ]
        transitions = [DATETIME_MIN] + transitions[1:] + [DATETIME_MAX]
        self.transitions = np.array(
            [datetime_to_dt64(dt) for dt in transitions],
            dtype=EPOCH_DTYPE,
        )


class MidpointSwitcher(SwitchingStrategy):
    """Switching based on the midpoint between neighboring TLE epoch times.

    This TLE switching strategy selects the TLE nearest to the desired time,
    regardless of whether that TLE is precedes it or is "in the future".
    """

    def compute_transitions(self) -> None:
        transitions = []
        for sat_a, sat_b in pairwise(self.satrecs):
            time_a = sat_epoch_datetime(sat_a).replace(tzinfo=None)
            time_b = sat_epoch_datetime(sat_b).replace(tzinfo=None)

            delta = time_b - time_a
            midpoint = time_a + delta / 2
            midpoint = datetime_to_dt64(midpoint)
            transitions.append(midpoint)

        transitions = [DATETIME_MIN] + transitions + [DATETIME_MAX]
        self.transitions = np.array(transitions, dtype=EPOCH_DTYPE)


class TCASwitcher(SwitchingStrategy):
    """Switching based on the time of closest approach for neighboring TLEs.

    This TLE switching method attempts to determine the time of closest approach
    for each pair of neighboring TLEs and use those times as the transitions.
    """
