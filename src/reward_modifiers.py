

def calculate_speed_reward(params, initial_reward, waypoints, target_speed, rewardable_speed_range, max_reward_multiplier):

    if params['closest_waypoints'][0] not in waypoints:
        return initial_reward

    if max_reward_multiplier < 1:
        raise InvalidInput('Max reward multiplier must be greater than 1')

    speed = params['speed']
    speed_diff = abs(speed - target_speed)

    if speed_diff >= rewardable_speed_range:
        return initial_reward

    percent_of_max_multiplier = (rewardable_speed_range - speed_diff) / rewardable_speed_range
    new_reward = initial_reward * (1 + (max_reward_multiplier - 1) * percent_of_max_multiplier)
    print(f'Reward: {initial_reward} -> {new_reward}, Speed: {speed}, Target Speed: {target_speed}, Rewardable Speed Range: {rewardable_speed_range}, Max Reward Multiplier: {max_reward_multiplier}')

    return new_reward


def terminal_off_track_reward(params, initial_reward):
    if params['is_offtrack']:
        return float(Settings.terminal_reward)
    return initial_reward


class InvalidInput(Exception):
    pass


class Settings:
    terminal_reward = .001
