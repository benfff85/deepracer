def reward_function(params):

    # Check Terminal Conditions
    try:
        terminal_off_track_check(params)
        terminal_reversed_check(params)
        terminal_max_steps_check(params)
    except TerminalConditionException:
        return float(Settings.terminal_reward)

    # Initialize reward
    reward = 1

    # Speed
    reward = calculate_speed_reward(params, reward, WaypointHelper.generate_waypoints("0:155"), 5, 5, 10)

    # Turning Left Areas
    reward = calculate_steering_angle_reward(params, reward, WaypointHelper.generate_waypoints("6:20,40:52,94:106,130:138"), 15, 15, 2)

    # Turning Right Areas
    reward = calculate_steering_angle_reward(params, reward, WaypointHelper.generate_waypoints("66:78"), -15, 15, 2)

    # Left Third Of Track Areas
    reward = calculate_side_of_track_reward(params, reward, WaypointHelper.generate_waypoints("10:18,32:52,94:106,130:140"), 'left', 2)

    # Middle Third Of Track Areas
    reward = calculate_side_of_track_reward(params, reward, WaypointHelper.generate_waypoints("0:4,114:122,142:154"), 'middle', 2)

    # Right Third Of Track Areas
    reward = calculate_side_of_track_reward(params, reward, WaypointHelper.generate_waypoints("64:78"), 'right', 2)

    return float(reward)

def calculate_speed_reward(params, initial_reward, waypoints, target_speed, rewardable_speed_range, max_reward_multiplier):

    if params['closest_waypoints'][0] not in waypoints:
        return initial_reward

    if max_reward_multiplier < 1:
        raise InvalidInputException('Max reward multiplier must be greater than 1')

    speed = params['speed']
    speed_diff = abs(speed - target_speed)

    if speed_diff >= rewardable_speed_range:
        return initial_reward

    percent_of_max_multiplier = (rewardable_speed_range - speed_diff) / rewardable_speed_range
    new_reward = initial_reward * (1 + (max_reward_multiplier - 1) * percent_of_max_multiplier)
    print(f'Reward: {initial_reward} -> {new_reward}, Speed: {speed}, Target Speed: {target_speed}, Rewardable Speed Range: {rewardable_speed_range}, Max Reward Multiplier: {max_reward_multiplier}')

    return new_reward


def calculate_steering_angle_reward(params, initial_reward, waypoints, target_angle, rewardable_angle_range, max_reward_multiplier):

    if params['closest_waypoints'][0] not in waypoints:
        return initial_reward

    if max_reward_multiplier < 1:
        raise InvalidInputException('Max reward multiplier must be greater than 1')

    steeringAngle = params['steering_angle']
    angle_diff = abs(steeringAngle - target_angle)

    if angle_diff >= rewardable_angle_range:
        return initial_reward

    percent_of_max_multiplier = (rewardable_angle_range - angle_diff) / rewardable_angle_range
    new_reward = initial_reward * (1 + (max_reward_multiplier - 1) * percent_of_max_multiplier)
    print(f'Reward: {initial_reward} -> {new_reward}, Angle: {steeringAngle}, Target Angle: {target_angle}, Rewardable Angle Range: {rewardable_angle_range}, Max Reward Multiplier: {max_reward_multiplier}')

    return new_reward


def calculate_side_of_track_reward(params, initial_reward, waypoints, target_third_of_track, reward_multiplier):

    if params['closest_waypoints'][0] not in waypoints:
        return initial_reward

    if reward_multiplier < 1:
        raise InvalidInputException('Reward multiplier must be greater than 1')

    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    is_left_of_center = params['is_left_of_center']

    if distance_from_center < (track_width / 6):
        actual_third_of_track = 'middle'
    else:
        if is_left_of_center:
            actual_third_of_track = 'left'
        else:
            actual_third_of_track = 'right'

    new_reward = initial_reward
    if actual_third_of_track == target_third_of_track:
        new_reward *= reward_multiplier

    print(f'Reward: {initial_reward} -> {new_reward}, Target Third of Track: {target_third_of_track}, Actual Third of Track: {actual_third_of_track}, Reward Multiplier: {reward_multiplier}')

    return float(new_reward)


def terminal_off_track_check(params):
    if params['is_offtrack']:
        print('Off track!')
        raise TerminalConditionException


def terminal_reversed_check(params):
    if params['is_reversed']:
        print('Reversed!')
        raise TerminalConditionException


def terminal_max_steps_check(params):
    if params['steps'] >= Settings.max_steps:
        print('Max steps reached!')
        raise TerminalConditionException


class InvalidInputException(Exception):
    pass


class TerminalConditionException(Exception):
    pass


class Settings:
    terminal_reward = 1e-3
    max_steps = 1000


class WaypointHelper:

    @staticmethod
    def generate_waypoints(waypoint_str):
        waypoints = []
        ranges = waypoint_str.split(',')
        for r in ranges:
            if ':' in r:
                start, end = map(int, r.split(':'))
                waypoints.extend(range(start, end + 1))
            else:
                waypoints.append(int(r))
        return waypoints
