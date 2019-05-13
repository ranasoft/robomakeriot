# Robomaker connected to IoT Core using AWS IoT Device SDK

With the growing usage of Robomaker and also IoT, I want to provide this resources as a demo to how to connect a robot to IoT Core using the python AWS IoT Device SDK.

This demo is based on the RoboMaker HelloWorld example described [here](https://github.com/aws-robotics/aws-robomaker-sample-application-helloworld)

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
* Create and IoT thing for the Robot and donwload the certificates.
* Create a policy that have permisions to Publish to robot/location and Subscribe to robot/move/+, and attach it to the certificate of the Robot (thing).  (Do not forget to enable the certificate).
* VPC, Subnet and Security Group with outbound access to Internet.
* Create a RoboMaker Application based on the [HelloWorld example](https://docs.aws.amazon.com/robomaker/latest/dg/gs-build-rundemo.html).

### 1. Create RoboMaker development environment and upload this code
* Go to the AWS RoboMaker console and create a new development environment, selection a VPC and subnet that has acces to Internet resources.
* When the environment is ready create folder in the root (in my case robomakeriot), and upload the source of this github repo.

### 2. Upload the certificates of the device
* Upload the certificate and private key of the Robot (thing) to the folder robomakeriot/robot_ws/src/hello_world_robot/certs.

### 3. Modify the IoT endpoint and other parameters.
* Open and edit the file robomakeriot/robot_ws/src/hello_world_robot/launch/rotate.launch, and update the attributes like iot endpoint and certificates.

### 4. Build, Bundle and Run the simulation
* Create a Build and Bundle configuration for the Robot and the Simulation.
* Launch the Simulation, to do this you can 1)Create a Simulation Configuration, using the IAM role, bucket from the RoboMaker Simulation Job was generated in your pre-required Robot Application.  Additionally set the name of the Security Group and Subnet mentioned in the pre-requisites; or 2) Clone the HelloWorld Simulation Job, connect and restart the simulation with the new bundles; or 3) Copy & paste the bundle packages to the S3 bucket used in the Simulation Job and clone it.

### 5. Test the different movemenets of the robot
* Go to the Simulation Job and open Gazebo, and check that the robot is not moving.
* Go to IoT Core and using the Test console publish the following message to test 3 different interactions:
1. Linear Move Forward or Back
```
Topic: robot/move/linear
Message:
{
    "direction": "forward",
    "speed": 1,
    "x": 1
}
```
2. Rotate to the Right or Left
```
Topic: robot/move/rotate
{
    "direction": "left",
    "speed": 90
}
```
3. Free movemement based on distance, rotation and time:
```
Topic: robot/move/time
{
    "x": 0.1,
    "z": 0.5,
    "sec": 7
}
```
You can see on Gazebo that the Robot is moving based on the IoT Messages definition.
