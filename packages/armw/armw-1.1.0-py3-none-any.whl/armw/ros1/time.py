import types

import rospy
import armw.globals


def get_time():
    if armw.globals.NODE is not None:
        return armw.Time().now().to_sec()
    else:
        raise Exception("time is not initialized. Have you created a node?")


class Duration(rospy.Duration):
    def __init__(self, secs=0, nsecs=0):
        super().__init__(nanoseconds=secs * 1000000000 + nsecs)
        self.to_nsec = types.MethodType(lambda self: self.nanoseconds, self)
        self.to_sec = types.MethodType(lambda self: self.nanoseconds / 1e9, self)
        self.is_zero = types.MethodType(lambda self: self.nanoseconds == 0, self)
        self.secs = secs
        self.nsecs = nsecs

    def __add__(self, other):
        if isinstance(other, Time):
            return armw.Time().from_sec(self.to_sec() + other.to_sec())
        else:
            Duration.__add__(self, other)

    @classmethod
    def from_sec(cls, secs):
        return Duration(int(secs), nsecs=int((secs - int(secs)) * 1000000000))

    @classmethod
    def from_seconds(cls, secs):
        return Duration(int(secs), nsecs=int((secs - int(secs)) * 1000000000))


class Time(rospy.Time):
    def __init__(self, secs=0, nsecs=0):
        super().__init__(secs=secs, nsecs=nsecs)

    def __add__(self, other):
        if isinstance(other, rospy.Duration):
            return armw.Time().from_sec(self.to_sec() + other.to_sec())
        else:
            Time.__add__(self, other)

    def __sub__(self, other):
        if isinstance(other, rospy.Duration):
            return armw.Time().from_sec(self.to_sec() - other.to_sec())
        else:
            Time.__add__(self, other)

    def __gt__(self, other):
        return self.to_sec() > other.to_sec()

    def __lt__(self, other):
        return self.to_sec() < other.to_sec()

    def __ge__(self, other):
        return self.to_sec() >= other.to_sec()

    def __le__(self, other):
        return self.to_sec() <= other.to_sec()

    def __eq__(self, other):
        return self.to_sec() == other.to_sec()

    def __ne__(self, other):
        return self.to_sec() != other.to_sec()

    def to_sec(self):
        return self.sec + float(self.nsecs) / 1000000000

    @classmethod
    def from_sec(cls, secs: float):
        return Time(secs=int(secs), nsecs=int((secs - int(secs)) * 1000000000))

    @classmethod
    def from_seconds(cls, secs: float):
        return Time().from_sec(secs=secs)

    @classmethod
    def now(cls):
        s = rospy.Time.now()
        return Time(secs=s[0], nsecs=s[1])


if __name__ == '__main__':
    a = Time(3, 5)
    b = Duration(5, 6)

    print(a)
    print(b)

    print(a + b)
    print(b + a)
