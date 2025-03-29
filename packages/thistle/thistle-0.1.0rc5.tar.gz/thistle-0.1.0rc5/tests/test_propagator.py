import datetime

import numpy as np
from hypothesis import given
from sgp4.api import Satrec
from sgp4.conveniences import sat_epoch_datetime
from sgp4.exporter import export_tle

from thistle.propagator import Propagator, _slices_by_transitions
from thistle.utils import datetime_to_dt64, jday_datetime64, trange

from . import strategies as cst
from .conftest import ISS_TLES


@given(cst.transitions(), cst.times())
def test_slices(
    transitions: np.ndarray[np.datetime64], times: np.ndarray[np.datetime64]
):
    slices = _slices_by_transitions(transitions, times)
    for idx, slc_ in slices:
        assert (transitions[idx] <= times[slc_]).all()
        assert (times[slc_] < transitions[idx + 1]).all()


class PropagatorBaseClass:
    method: str

    def setup_class(self):
        self.tles = ISS_TLES
        self.propagator = Propagator(ISS_TLES, method=self.method)


class TestPropagatorEpoch(PropagatorBaseClass):
    method: str = "epoch"

    def test_find_satrec_by_epoch(self):
        line1 = "1 25544U 98067A   98325.45376114  .01829530  18113-2  41610-2 0  9996"
        line2 = "2 25544 051.5938 162.0926 0074012 097.3081 262.5015 15.92299093   191"

        exp_sat = Satrec.twoline2rv(line1, line2)
        dt = sat_epoch_datetime(exp_sat)
        sat = self.propagator.find_satrec(datetime_to_dt64(dt))
        assert export_tle(sat) == export_tle(exp_sat)

    def test_propagator(self):
        line1 = "1 25544U 98067A   98325.45376114  .01829530  18113-2  41610-2 0  9996"
        line2 = "2 25544 051.5938 162.0926 0074012 097.3081 262.5015 15.92299093   191"

        exp_sat = Satrec.twoline2rv(line1, line2)
        dt = sat_epoch_datetime(exp_sat)
        times = trange(dt, dt + datetime.timedelta(seconds=60), 10)

        jd, fr = jday_datetime64(times)
        exp_e, exp_r, exp_v = exp_sat.sgp4_array(jd, fr)

        e, r, v = self.propagator.propagate(times)

        assert e.tolist() == exp_e.flatten().tolist()
        assert r.tolist() == exp_r.flatten().tolist()
        assert v.tolist() == exp_v.flatten().tolist()


class TestPropagatorMidpoint(PropagatorBaseClass):
    method: str = "midpoint"

    def test_propagator(self):
        a1 = "1 25544U 98067A   98325.45376114  .01829530  18113-2  41610-2 0  9996"
        a2 = "2 25544 051.5938 162.0926 0074012 097.3081 262.5015 15.92299093   191"
        b1 = "1 25544U 98067A   98325.51671211  .01832406  18178-2  41610-2 0  9996"
        b2 = "2 25544 051.5928 161.7497 0074408 097.6565 263.2450 15.92278419   200"

        sat_a = Satrec.twoline2rv(a1, a2)
        sat_b = Satrec.twoline2rv(b1, b2)

        epoch_a, epoch_b = sat_epoch_datetime(sat_a), sat_epoch_datetime(sat_b)
        delta = epoch_b - epoch_a
        midpoint = epoch_a + delta / 2
        step = delta.total_seconds() / 100

        # Check first half of range
        times = trange(epoch_a, midpoint, step)
        jd, fr = jday_datetime64(times)
        e, r, v = self.propagator.propagate(times)
        exp_e, exp_r, exp_v = sat_a.sgp4_array(jd, fr)
        assert export_tle(self.propagator.find_satrec(times[-1])) == export_tle(sat_a)
        assert e.tolist() == exp_e.flatten().tolist()
        assert r.tolist() == exp_r.flatten().tolist()
        assert v.tolist() == exp_v.flatten().tolist()

        # Check second half of range
        times = trange(midpoint, epoch_b, step)
        jd, fr = jday_datetime64(times)
        e, r, v = self.propagator.propagate(times)
        exp_e, exp_r, exp_v = sat_b.sgp4_array(jd, fr)
        assert export_tle(self.propagator.find_satrec(times[-1])) == export_tle(sat_b)
        assert e.tolist() == exp_e.flatten().tolist()
        assert r.tolist() == exp_r.flatten().tolist()
        assert v.tolist() == exp_v.flatten().tolist()
