__author__ = 'will'
import abc

class Robot(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def load_legs(self):
        """
        Start the legs, init code
        """

    @abc.abstractmethod
    def read_feet(self):
        """
        return array of feet sensor values
        :return:
        """

    @abc.abstractmethod
    def read_imu(self):
        """
        returns orientation array
        :return:
        """

    @abc.abstractmethod
    def move_leg_to_point(self, leg, x, y, z):
        """
        move legs to absolute point
        :param leg: leg name
        :param x: body relative x pos
        :param y: body relative y pos
        :param z: body relative z pos
        :return:
        """

    def start(self):
        pass


