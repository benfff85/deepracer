

def calculate_speed_reward(params, initial_reward, weight):
    """Calculates a reward based on speed. Ususally used as the first reward modifier, instead of multiplying the reward
     by a multiple it adds an absolute value to the reward.

    Args:
        params (dict): A dictionary containing parameters. It must have a key 'speed' representing the speed value.
        initial_reward (float): The initial reward value.
        weight (float): The weight to be applied to the speed for reward calculation.

    Returns:
        float: The updated reward value after applying the speed reward.

    Example:
        >>> params = {'speed': 10}
        >>> initial_reward = 0
        >>> weight = 1.0
        >>> calculate_speed_reward(params, initial_reward, weight)
        10.0

    """
    speed = params['speed']

    new_reward = initial_reward + (weight * speed)

    print(f'Reward: {initial_reward} -> {new_reward}, Speed: {speed}, Weight: {weight}')
    return new_reward
