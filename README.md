# Robomaker connected to IoT Core using AWS IoT Device SDK

With the growing usage of Robomaker and also IoT, I want to provide this resources as a demo to how to connect a robot to IoT Core using the python AWS IoT Device SDK.

This demo is based on the RoboMaker HelloWorld example described here https://github.com/aws-robotics/aws-robomaker-sample-application-helloworld

With some modifications that do the following:

* Connect to IoT Core with X.500 certificates
* Wait for messages to move the robot, specifically 3 movement: linear, rotation, free.
* Report any movemenet of the robot publishing a message to IoT Core.

The demostration allow you to see:

* How to connect a robot created in RoboMaker to connect to AWS IoT Core using the AWS IoT Device SDK.
* Send information from the Robot.
* Do actions to the Robot based on MQTT messages.

## Steps to reproduce the demo

### Pre-requisites
* Create and IoT thing and donwload the certificates, incluiding the Ammazon Root CA 1.
* Create a policy that have permisions to Publish to robot/location and Subscribe to robot/move/+

### 1. Create RoboMaker development environment and upload this code

### 2. Upload the certificates of the device

### 3. Modify the IoT endpoint parameter and any other parameter

### 4. Deploy and run the simulation

### 5. Test the different movemenets of the robot
