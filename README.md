<div align="center">
    <h1>DeepRacer</h1>
    <p>Deep Chasers repository for AWS DeepRacer</p>
    <img src="https://d1.awsstatic.com/deepracer/DRL%20Logo%20web%20500px.2b6ea0add11b4cf83314b39d3d7d6ab63d7fdff9.png" alt="AWS DeepRacer League Logo" width="250">
</div>

## Reward Modifiers

Let's start an inventory of different **reward modifier** functions that we can then piece together into a **reward function**.

A reward modifier is simply a function that takes in inputs including the current reward and deep racer props and returns a new reward value.

### Types

* `Absolute` - Sets a absolute value, for example if off course set reward to 0
* `Fixed` - Adds a fixed value, for example if still on track add 1 to the reward
* `Multiplier` - Multiplies the reward by some multiple
* `Exponential` - Exponentially increases the reward 

### Inventory

| #   | Modifier                        | Type       | Waypoint Filtering | Description                                                                                                                                                                                                                                                                                                    |
|-----|---------------------------------|------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1   | calculate_speed_reward          | Multiplier | Yes                | Rewards based on speed. The function is provided a target speed and rewardable speed range. If the current speed is within target speed +/- range, the reward will have a multiplier applied linearly proportional to the proximity to the target speed. ([Diagram](docs/diagrams/Speed_Reward_Diagram.png))   |
| 2   | calculate_steering_angle_reward | Multiplier | Yes                | Rewards based on steering angle. The function is provided a target steering angle and rewardable steering angle range. If the current steering angle is within target steering angle +/- range, the reward will have a multiplier applied linearly proportional to the proximity to the target steering angle. |
| 3   | calculate_car_angle_reward      |            |                    | TODO Car heading relative to track                                                                                                                                                                                                                                                                             |
| 4   | calculate progress_reward       |            |                    | TODO Track progress                                                                                                                                                                                                                                                                                            |
| 5   | calculate_side_of_track_reward  |            |                    | TODO Which third of the track the car is on                                                                                                                                                                                                                                                                    |
| 100 | terminal_off_track_reward       | Absolute   | NA                 | Set reward to low value if the car has driven off track                                                                                                                                                                                                                                                        |
| 101 | terminal_reversed_reward        | Absolute   | NA                 | Set reward to low value if the car is in a reversed orientation                                                                                                                                                                                                                                                |
| 102 | terminal_max_steps_check        | Absolute   | NA                 | Set reward to low value if the number of steps has exceeded a pre-defined maximum                                                                                                                                                                                                                              |

## Waypoint Helper

A class designed to make generating collections of waypoints cleaner. All functions that deal with waypoints expect a list of individual waypoints. 

This class exposes a `generate_waypoints(str)` method that will take string representing the waypoints and return the list of waypoints.

Examples

| String    | Waypoints            |
|-----------|----------------------|
| 1:10      | 1,2,3,4,5,6,7,8,9,10 |
| 2:4,6:8   | 2,3,4,6,7,8          |
| 1:4,7,9   | 1,2,3,4,7,9          |

## Input Parameter Reference

A writeup on the available input params can be found [here](https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-reward-function-input.html).

```
{
    "all_wheels_on_track": Boolean,        # flag to indicate if the agent is on the track
    "x": float,                            # agent's x-coordinate in meters
    "y": float,                            # agent's y-coordinate in meters
    "closest_objects": [int, int],         # zero-based indices of the two closest objects to the agent's current position of (x, y).
    "closest_waypoints": [int, int],       # indices of the two nearest waypoints.
    "distance_from_center": float,         # distance in meters from the track center 
    "is_crashed": Boolean,                 # Boolean flag to indicate whether the agent has crashed.
    "is_left_of_center": Boolean,          # Flag to indicate if the agent is on the left side to the track center or not. 
    "is_offtrack": Boolean,                # Boolean flag to indicate whether the agent has gone off track.
    "is_reversed": Boolean,                # flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
    "heading": float,                      # agent's yaw in degrees
    "objects_distance": [float, ],         # list of the objects' distances in meters between 0 and track_length in relation to the starting line.
    "objects_heading": [float, ],          # list of the objects' headings in degrees between -180 and 180.
    "objects_left_of_center": [Boolean, ], # list of Boolean flags indicating whether elements' objects are left of the center (True) or not (False).
    "objects_location": [(float, float),], # list of object locations [(x,y), ...].
    "objects_speed": [float, ],            # list of the objects' speeds in meters per second.
    "progress": float,                     # percentage of track completed
    "speed": float,                        # agent's speed in meters per second (m/s)
    "steering_angle": float,               # agent's steering angle in degrees
    "steps": int,                          # number steps completed
    "track_length": float,                 # track length in meters.
    "track_width": float,                  # width of the track
    "waypoints": [(float, float), ]        # list of (x,y) as milestones along the track center
}
```