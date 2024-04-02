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

| #   | Modifier                        | Type       | Waypoint Filtering | Description                                                                                                                                                                                                                                                                                                  |
|-----|---------------------------------|------------|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1   | calculate_speed_reward          | Multiplier | Yes                | Rewards based on speed. The function is provided a target speed and rewardable speed range. If the current speed is within target speed +/- range, the reward will have a multiplier applied linearly proportional to the proximity to the target speed. ([Diagram](docs/diagrams/Speed_Reward_Diagram.png)) |
| 2   | calculate_steering_angle_reward |            |                    | TODO Steering Angle relative to predefined target angle                                                                                                                                                                                                                                                      |
| 3   | calculate_car_angle_reward      |            |                    | TODO Car heading relative to track                                                                                                                                                                                                                                                                           |
| 4   | calculate progress_reward       |            |                    | TODO Track progress                                                                                                                                                                                                                                                                                          |
| 5   | calculate_side_of_track_reward  |            |                    | TODO Which third of the track the car is on                                                                                                                                                                                                                                                                  |
| 100 | terminal_off_track_reward       | Absolute   | NA                 | Set reward to low value if the car has driven off track                                                                                                                                                                                                                                                      |
| 101 | terminal_reversed_reward        | Absolute   | NA                 | Set reward to low value if the car is in a reversed orientation                                                                                                                                                                                                                                              |
| 102 | terminal_max_steps_check        | Absolute   | NA                 | Set reward to low value if the number of steps has exceeded a pre-defined maximum                                                                                                                                                                                                                            |