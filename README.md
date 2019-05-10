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
* Create and IoT thing for the Robot and donwload the certificates.
* Create a policy that have permisions to Publish to robot/location and Subscribe to robot/move/+, and attach it to the certificate of the Robot (thing).  (Do not forget to enable the certificate).

### 1. Create RoboMaker development environment and upload this code
* Go to the AWS RoboMaker console and create a new development environment, selection a VPC and subnet that has acces to Internet resources.
* When the environment is ready create folder in the root (in my case robomakeriot), and upload the source of this github repo.

### 2. Upload the certificates of the device
* Upload the certificate and private key of the Robot (thing) to the folder robomakeriot/robot_ws/src/hello_world_robot/certs.

### 3. Modify the IoT endpoint and other parameters.
* Open and edit the file robomakeriot/robot_ws/src/hello_world_robot/launch/rotate.launch
* Update the parameter iot/endpoint/host with the appropiate endpoint of your IoT Core.
* Update the parameter iot/certs/certificate with the file name of the certificate of the Robot.
* Update the parameter iot/certs/private with the file name of the private key of the Robot.
* Optional: Update any other parameter like the thing_name if you want.

### 4. Deploy and run the simulation
* Create the Build and Bundle operations, going to the menu Run (besides RoboMaker menu) and select the Add or Edit Configurations...
* In the "Create New Configuration" window, select "Colcon build", then set the name to something like "robomakeriot Robot", and set the Working directory to "./robomakeriot/robot_ws" (or the root folder name you choose), and click Save.
* Repeat the operation for the build simulation: In the "Create New Configuration" window, select "Colcon build", then set the name to something like "robomakeriot Simulation", and set the Working directory to "./robomakeriot/simulation_ws" (or the root folder name you choose), and click Save.
* Repeat the operation for the bundle robot: In the "Create New Configuration" window, select "Colcon bundle", then set the name to something like "robomakeriot Robot", and set the Working directory to "./robomakeriot/robot_ws" (or the root folder name you choose), and click Save.
* Repeat the operation for the bundle robot: In the "Create New Configuration" window, select "Colcon bundle", then set the name to something like "robomakeriot Simulation", and set the Working directory to "./robomakeriot/simulation_ws" (or the root folder name you choose), and click Save.

### 5. Test the different movemenets of the robot
