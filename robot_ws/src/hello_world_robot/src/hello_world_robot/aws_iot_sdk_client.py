"""
 Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.

 Permission is hereby granted, free of charge, to any person obtaining a copy of this
 software and associated documentation files (the "Software"), to deal in the Software
 without restriction, including without limitation the rights to use, copy, modify,
 merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnished to do so.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import ssl
import json
import time

import rospy
from geometry_msgs.msg import Twist

# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


class AWSIoT(object):
    QOS = 1
    HZ = 10
    
    def __init__(self):
        rospy.loginfo("AWSIot#__init__")
        self.is_connected = False
        # Get server parameters
        self.__params = rospy.get_param("~awsiot")
        # For certificate based connection
        self.__myMQTTClient = AWSIoTMQTTClient(self.__params["thingName"])
        rospy.on_shutdown(self._on_shutdown)
        
        
    def run(self):
        rospy.loginfo("AWSIoT#run")
        # Configurations
        # For TLS mutual authentication
        self.__myMQTTClient.configureEndpoint(
            self.__params["endpoint"]["host"], 
            self.__params["endpoint"]["port"])
        self.__myMQTTClient.configureCredentials(
            self.__params["certs"]["rootCA"],
            self.__params["certs"]["private"],
            self.__params["certs"]["certificate"])
        self.__myMQTTClient.configureConnectDisconnectTimeout(
            self.__params["connectionTimeOut"])
        # Connect
        self.__myMQTTClient.connect()
        rospy.loginfo("AWSIoT#Connected using AWSIoTPythonSDK")
        # Subscribe to topic
        self.__myMQTTClient.subscribe(
            self.__params["mqtt"]["topic"]["sub"], 
            AWSIoT.QOS,
            self._on_message)
        self.is_connected = True
        self.__cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        
        
    def _on_message(self, client, userdata, data):
        topic = data.topic
        payload = str(data.payload)
        rospy.loginfo("AWSIoT#_on_message payload={}".format(payload))
        twist = Twist()
        try:
            params = json.loads(payload)
            if "x" in params and "z" in params and "sec" in params:
                start_time = time.time()
                d = float(params["sec"])
                r = rospy.Rate(AWSIoT.HZ)
                while time.time() - start_time < d:
                    twist.linear.x = float(params["x"])
                    twist.angular.z = float(params["z"])
                    self.__cmd_pub.publish(twist)
                    r.sleep()
        except (TypeError, ValueError):
            pass
        
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.__cmd_pub.publish(twist)
    
    def _on_shutdown(self):
        logmsg = "AWSIoT#_on_shutdown is_connected={}".format(self.is_connected)
        rospy.loginfo(logmsg)
        if self.is_connected:
            self.__myMQTTClient.unsubscribe(self.__params["mqtt"]["topic"]["sub"])
            self.__myMQTTClient.disconnect()