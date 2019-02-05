#!/usr/bin/env python
# license removed for brevity

"""
//======================================================================//
//  This software is free: you can redistribute it and/or modify        //
//  it under the terms of the GNU General Public License Version 3,     //
//  as published by the Free Software Foundation.                       //
//  This software is distributed in the hope that it will be useful,    //
//  but WITHOUT ANY WARRANTY; without even the implied warranty of      //
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE..  See the      //
//  GNU General Public License for more details.                        //
//  You should have received a copy of the GNU General Public License   //
//  Version 3 in the file COPYING that came with this distribution.     //
//  If not, see <http://www.gnu.org/licenses/>                          //
//======================================================================//
//                                                                      //
//      Copyright (c) 2019 SinfonIA Pepper RoboCup Team                 //
//      Sinfonia - Colombia                                             //
//      https://sinfoniateam.github.io/sinfonia/index.html              //
//                                                                      //
//======================================================================//
"""

import time
import utils
import rospy
from PIL import Image
from std_msgs.msg import String
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Quaternion
from sinfonia_pepper_robot_toolkit.srv import TakePicture


TESTTOPIC = "sIA_camera"


def robotToolkitTestNode():
    rospy.init_node('robot_toolkit_test_node', anonymous=True)
    rate = rospy.Rate(10)

    if TESTTOPIC == "sIA_moveToward":
        testMoveToward(rate)
    elif TESTTOPIC == "sIA_moveTo":
        testMoveTo(rate)
    elif TESTTOPIC == "sIA_laser":
        testLaser(rate)
    elif TESTTOPIC == "sIA_camera":
        testCamera()


def testMoveToward(rate):
    pub = rospy.Publisher("sIA_moveToward", Vector3, queue_size=10)
    while pub.get_num_connections() == 0:
        rate.sleep()
    pub2 = rospy.Publisher("sIA_stopMove", String, queue_size=10)
    while pub2.get_num_connections() == 0:
        rate.sleep()

    # Functionality test
    square = [[1.0, 0.0, 0.0],
              [0.0, 1.0, 0.0],
              [-1.0, 0.0, 0.0],
              [0.0, -1.0, 0.0]]

    for vertex in square:
        msg = utils.fillVector(vertex, "v3")
        pub.publish(msg)
        time.sleep(3)

    stopStr = "Stop"
    pub2.publish(stopStr)
    time.sleep(3)
    # Error test
    msg = utils.fillVector([0.0, -2.0, 0.0], "v3")
    pub.publish(msg)
    time.sleep(3)
    stopStr = "Stap"
    pub2.publish(stopStr)


def testMoveTo(rate):
    pub = rospy.Publisher("sIA_moveTo", Quaternion, queue_size=10)
    while pub.get_num_connections() == 0:
        rate.sleep()

    # Functionality test
    square = [[1.0, 0.0, 0.0, 6.0],
              [0.0, 1.0, 0.0, 6.0],
              [-1.0, 0.0, 0.0, 6.0],
              [0.0, -1.0, 0.0, 6.0]]

    for vertex in square:
        msg = utils.fillVector(vertex, 'q')
        pub.publish(msg)
        time.sleep(8)

    # Error test
    msg = utils.fillVector([0.0, -1.0, 4.0, 6.0], 'q')
    pub.publish(msg)


def testLaser(rate):
    pub = rospy.Publisher("sIA_stream_from", String, queue_size=10)
    while pub.get_num_connections() == 0:
        rate.sleep()
    pub.publish("sIA_laser_gl.laserScan.ON")
    time.sleep(5)
    pub.publish("sIA_laser_gr.laserScan.ON")
    time.sleep(5)
    pub.publish("sIA_laser_gl.laserScan.OFF")
    time.sleep(5)
    pub.publish("sIA_laser_gr.laserScan.OFF")
    time.sleep(5)


def testCamera():
    rospy.wait_for_service("sIA_takePicture")
    takePicture = rospy.ServiceProxy("sIA_takePicture", TakePicture)
    response = takePicture("Take Picture", [0, 2, 11, 30]).response
    image = Image.frombytes("RGB", (response.width, response.height), str(bytearray(response.data)))
    image.show()

    try:
        takePicture("Takepicture", [0, 2, 11, 30])
    except rospy.service.ServiceException:
        pass
    time.sleep(5)

    try:
        takePicture("Take Picture", [0, 2, 18, 30])
    except rospy.service.ServiceException:
        pass


if __name__ == '__main__':
    try:
        robotToolkitTestNode()
    except rospy.ROSInterruptException:
        pass
