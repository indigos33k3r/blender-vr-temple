"""
Input/Output
************

Takes the three different inputs, process the data and call the corresponding event.
It also handles head transformation/navigation.
"""

from bge import (
        logic,
        )

from mathutils import Vector
from . import base

TODO = True

class Base(base.Base):
    __slots__ = (
            "_camera",
            "_direction_object",
            "_flashlight_power",
            "_matrix"
            "_sonar_power",
            "_use_headtrack",
            )

    def __init__(self, parent):
        base.Base.__init__(self, parent)

        scene = logic.getCurrentScene()
        objects = scene.objects

        # Flashlight
        self._flashlight_power = False

        # Sonar
        self._sonar_power = False

        # Head Tracking
        self._use_headtrack = False
        self._setupHeadTrack()

        # Flashlight and Rock thrower
        self._direction_object = objects.get('Spot')

        if not self._direction_object:
            raise Exception('"Spot" object not found in the scene')

        self._camera = objects.get('Camera', scene.active_camera)

        # Matrix is set once per frame
        self._resetMatrix()

    def loop(self):
        self._resetMatrix()
        self._updateDirection()

    @property
    def is_sonar(self):
        return self._sonar_power

    @property
    def is_flashlight(self):
        return self._flashlight_power

    @property
    def head_direction(self):
        """
        Get the direction of the player's head

        :rtype: mathutils.Quaternion
        """
        matrix = self._getHeadMatrix()
        return matrix.to_quaternion()

    @property
    def head_position(self):
        """
        Get the direction of the player's head

        :rtype: mathutils.Vector
        """
        matrix = self._getHeadMatrix()
        return matrix.translation

    def _resetMatrix(self):
        self._matrix = None

    def _setupHeadTrack(self):
        """
        If BlenderVR has headtracking setup we use it
        """
        is_debug = self._parent.is_debug

        if is_debug or not hasattr(logic, 'BlenderVR'):
            return

        vrpn = logic.BlenderVR.getPlugin('vrpn')
        oculus_dk2 = logic.BlenderVR.getPlugin('oculus_dk2')

        """
        * get user
        * see if this user is in any vrpn > tracker > user
        * see if this user is in any oculus_dk2 > user
        """
    def _getHeadMatrix(self):
        """
        :rtype: mathutils.Matrix
        """
        if self._matrix:
            return self._matrix

        if self._use_headtrack:
            TODO
        else:
            self._matrix = self._camera.worldTransform

        return self._matrix

    def _updateDirection(self):
        """
        Rotate the flashlight and the rock thrower according to the
        current head orientation
        """
        position = self.head_position
        direction = self.head_direction

        self._direction_object.worldOrientation = direction
        self._direction_object.worldPosition = position

    def flashlightButton(self):
        """
        Flashlight button was pressed
        """
        if self._sonar_power and not self._flashlight_power:
            # we can do only one action at time
            return

        self._flashlight_power = not self._flashlight_power
        self._parent.events.setFlashlightMode(power=self._flashlight_power)

        """
        * also should make the ghost react, and if it stays long in the same ghost, kills the ghost
        """

    def sonarButton(self):
        """
        Sonar button was pressed
        """
        if self._flashlight_power and not self._sonar_power:
            # we can do only one action at time
            return

        self._sonar_power = not self._sonar_power
        self._parent.events.setSonarMode(power=self._sonar_power)

    def rockButton(self):
        """
        Rock button was pressed
        """
        self._parent.events.throwRock()

        """
        * if it hits a bat, make it faster
        """
