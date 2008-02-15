#!/usr/bin/env python

from j5.Basic import Timer
import threading
import time

class TimerDriver:
    def __init__(self, expecteddiff=1, expectarg=False):
        self.lasttime = None
        self.expecteddiff = expecteddiff
        self.expectarg = expectarg
        self.ticks = 0

    def timefunc(self, testarg=None):
        tm = time.time()
        self.ticks += 1
        assert not self.expectarg or testarg is not None
        if self.lasttime != None:
            actual_diff = tm - self.lasttime
            assert abs(actual_diff - self.expecteddiff) <= (float(self.expecteddiff) / 10)
        self.lasttime = tm

    def sleepfunc(self, testarg=None):
        """takes an iterable and sleeps for item seconds for each item"""
        next_sleep = testarg.next()
        tm = time.time()
        self.lasttime = tm
        self.ticks += 1
        print tm, next_sleep, self.ticks
        if next_sleep:
            time.sleep(next_sleep)

class TestTimer:
    def test_onesec(self):
        """Test the one second resolution"""
        tm = TimerDriver()
        timer = Timer.Timer(tm.timefunc)
        thread = threading.Thread(target=timer.start)
        thread.start()
        time.sleep(3)
        timer.stop = True
        assert tm.lasttime is not None
        assert 2 <= tm.ticks <= 3

    def test_twosec(self):
        """Test a non one second resolution"""
        tm = TimerDriver(2)
        timer = Timer.Timer(tm.timefunc, resolution=2)
        thread = threading.Thread(target=timer.start)
        thread.start()
        time.sleep(5)
        timer.stop = True
        assert tm.lasttime is not None
        assert 2 <= tm.ticks <= 3

    def test_args(self):
        """Test passing args"""
        tm = TimerDriver(expectarg=True)
        timer = Timer.Timer(tm.timefunc, args=(True,))
        thread = threading.Thread(target=timer.start)
        thread.start()
        time.sleep(3)
        timer.stop = True
        assert tm.lasttime is not None

    def test_missed(self):
        """Test missing time events by sleeping in the target function"""
        tm = TimerDriver(1)
        timer = Timer.Timer(tm.sleepfunc, args=(iter([0,2,3,0,6]),))
        import logging
        logging.getLogger().setLevel(logging.INFO)
        thread = threading.Thread(target=timer.start)
        thread.start()
        # make sure our sleep happens within the last 6-second pause
        time.sleep(12)
        print time.time(), tm.lasttime
        timer.stop = True
        assert tm.lasttime is not None
        assert 4 <= tm.ticks <= 5

    def test_kwargs(self):
        """Test passing kwargs"""
        tm = TimerDriver(expectarg=True)
        timer = Timer.Timer(tm.timefunc, kwargs={"testarg":True})
        thread = threading.Thread(target=timer.start)
        thread.start()
        time.sleep(3)
        timer.stop = True
        assert tm.lasttime is not None

