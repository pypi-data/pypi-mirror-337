# YggSimLib

## Introduction
YggSimLib is a wrapper library that simplifies working with K-Spice for the Yggdrasil Engineering Simulator.  
It consists of two main functionalities
-   Wrapping object operations
-   Setting up sequences/scenarios that can be programmed to execute in a pre-set order

## Object Wrapping
The Yggdrasil Engineering Simulator makes use of several object types to represent for instance on/off valves. Each object type can have different parameters that needs to be set in order to i.e. open the valve.  The YggSimLib.On_Off_Valve object simplifies operations on valves, exposing a single open() method that behind the scenes sets the correct parameter on the K-Spice object.  
The following types are implemented:
-   On_Off_Valve
    -   Wraps MotorOperatedValve, BlockValve and LedaValve
-   Motor_Heater
    -   Wraps ControlledAsynchronousMachine and ControlledElectricHeater 
-   PID
    -   Wraps PidController
-   Choke
    -   Wraps ControlValve and LedaValve (acting as a choke)
-   Transmitter
    -   Wraps AlarmTransmitter

## Sequencing
Sequencing / Scenario building are supported through the classes Step, Sequence and Admin. 
The Step class lets the user define a set of actions to be performed.  When the actions has been initiated, a set of transition conditions can be configured that will allow the step to complete within a maximum time limit (simulation clock). Each step is configured so it contains the name of the next step.
A set of Steps can be collected in Sequence object.  The Sequence object will execute the steps in the order configured by the steps themselves, and also allows a set of inhibit conditions to be set that will disalow the sequence from starting. 
Finally, a set of Sequence objects can be collected in an Admin object.  Together with the Sequences, this class requires a set of relations between the sequences that dictates execution order, allowing for both parallell and serial execution of the sequences.  These relations are configured as a set of edges connecting the sequence names.