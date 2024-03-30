# DeepRacer
Deep Chasers repository for AWS DeepRacer

## Reward Modifiers

Let's start an inventory of different **reward modifier** functions that we can then piece together into a **reward function**.

A reward modifier is simply a function that takes in inputs including the current reward and deep racer props and returns a new reward value.

### Types:

* Absolute - Sets a absolute value, for example if off course set reward to 0
* Fixed - Adds a fixed value, for example if still on track add 1 to the reward
* Multiplier - Multiplies the reward by some multiple
* Exponential - Exponentially increases the reward 

### Inventory

| # | Modifier                | Type  | Description                                                                                                                                                                                   |
|---|-------------------------|-------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | calculate_speed_reward  | Fixed | Simple reward for speed, adds a multiple of the current speed. Ideally would replace this by something more dynamic that rewards based on proximity of actual speed to an input target speed. |

