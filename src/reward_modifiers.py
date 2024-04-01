

def calculate_speed_reward(params, initial_reward, waypoints, target_speed, rewardable_speed_range, max_reward_multiplier):

    if params['closest_waypoints'][0] not in waypoints:
        return initial_reward

    speed = params['speed']
    speed_diff = abs(speed - target_speed)

    if speed_diff >= rewardable_speed_range:
        return initial_reward

    percent_of_max_multiplier = (rewardable_speed_range - speed_diff) / rewardable_speed_range
    new_reward = initial_reward * max_reward_multiplier * percent_of_max_multiplier
    print(f'Reward: {initial_reward} -> {new_reward}, Speed: {speed}, Target Speed: {target_speed}, Rewardable Speed Range: {rewardable_speed_range}, Max Reward Multiplier: {max_reward_multiplier}')

    return new_reward
