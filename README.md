# DeepRacer
Deep Chasers repository for AWS DeepRacer

## Reward Modifiers

Let's start an inventory of different **reward modifier** functions that we can then piece together into a **reward function**.

A reward modifier is simply a function that takes in inputs including the current reward and deep racer props and returns a new reward value.

### Types

* `Absolute` - Sets a absolute value, for example if off course set reward to 0
* `Fixed` - Adds a fixed value, for example if still on track add 1 to the reward
* `Multiplier` - Multiplies the reward by some multiple
* `Exponential` - Exponentially increases the reward 

### Inventory

| #   | Modifier                        | Type       | Waypoint Filtering | Description                                                                                                                                                                                                                                              |
|-----|---------------------------------|------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1   | calculate_speed_reward          | Multiplier | Yes                | Rewards based on speed. The function is provided a target speed and rewardable speed range. If the current speed is within target speed +/- range, the reward will have a multiplier applied linearly proportional to the proximity to the target speed. |
| 2   | calculate_steering_angle_reward |            |                    |                                                                                                                                                                                                                                                          |
| 3   | calculate_car_angle_reward      |            |                    |                                                                                                                                                                                                                                                          |
| 4   | calculate progress_reward       |            |                    |                                                                                                                                                                                                                                                          |
| 5   | calculate_side_of_track_reward  |            |                    |                                                                                                                                                                                                                                                          |
| 100 | terminal_off_track_reward       | Absolute   | NA                 | Set reward to low value if the car has driven off track                                                                                                                                                                                                  |