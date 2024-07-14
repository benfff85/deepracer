def reward_function(params):

    # Check Terminal Conditions
    try:
        terminal_off_track_check(params)
        # terminal_wheel_off_track_check(params)
        terminal_reversed_check(params)
        terminal_max_steps_check(params)
    except TerminalConditionException:
        return float(Settings.terminal_reward)

    # Initialize reward
    reward = 1

    # Speed
    reward = calculate_speed_reward(params, reward, WaypointHelper.generate_waypoints("0:155"), 5, 5, 10)

    # Turning Left Areas
    # reward = calculate_steering_angle_reward(params, reward, WaypointHelper.generate_waypoints("6:20,40:52,94:106,130:138"), 15, 15, 2)
    reward = calculate_steering_direction_reward(params, reward, WaypointHelper.generate_waypoints("6:20,40:52,94:106,130:138"), 'left', 1.2)

    # Turning Right Areas
    # reward = calculate_steering_angle_reward(params, reward, WaypointHelper.generate_waypoints("66:78"), -15, 15, 2)
    reward = calculate_steering_direction_reward(params, reward, WaypointHelper.generate_waypoints("66:78"), 'right', 1.2)

    # Left Third Of Track Areas
    reward = calculate_side_of_track_reward(params, reward, WaypointHelper.generate_waypoints("10:18,32:52,94:106,130:140"), 'left', 1.5)

    # Middle Third Of Track Areas
    reward = calculate_side_of_track_reward(params, reward, WaypointHelper.generate_waypoints("0:4,114:122,142:154"), 'middle', 1.5)

    # Right Third Of Track Areas
    reward = calculate_side_of_track_reward(params, reward, WaypointHelper.generate_waypoints("64:78"), 'right', 1.5)

    # Progress Reward
    reward = calculate_progress_reward(params, reward, WaypointHelper.generate_waypoints("0:155"), 225, 25, 10)

    return float(reward)


def calculate_speed_reward(params, initial_reward, waypoints, target_speed, rewardable_speed_range, max_reward_multiplier):

    if params['closest_waypoints'][0] not in waypoints:
        print("calculate_speed_reward :: Excluded for waypoint")
        return initial_reward

    if max_reward_multiplier < 1:
        raise InvalidInputException('Max reward multiplier must be greater than 1')

    speed = params['speed']
    speed_diff = abs(speed - target_speed)

    if speed_diff >= rewardable_speed_range:
        return initial_reward

    percent_of_max_multiplier = (rewardable_speed_range - speed_diff) / rewardable_speed_range
    new_reward = initial_reward * (1 + (max_reward_multiplier - 1) * percent_of_max_multiplier)
    print(f'calculate_speed_reward :: Reward: {initial_reward:.2f} -> {new_reward:.2f}, Speed: {speed}, Target Speed: {target_speed}, Rewardable Speed Range: {rewardable_speed_range}, Max Reward Multiplier: {max_reward_multiplier}')

    return new_reward


def calculate_steering_angle_reward(params, initial_reward, waypoints, target_angle, rewardable_angle_range, max_reward_multiplier):

    if params['closest_waypoints'][0] not in waypoints:
        print("calculate_steering_angle_reward :: Excluded for waypoint")
        return initial_reward

    if max_reward_multiplier < 1:
        raise InvalidInputException('Max reward multiplier must be greater than 1')

    steering_angle = params['steering_angle']
    angle_diff = abs(steering_angle - target_angle)

    if angle_diff >= rewardable_angle_range:
        return initial_reward

    percent_of_max_multiplier = (rewardable_angle_range - angle_diff) / rewardable_angle_range
    new_reward = initial_reward * (1 + (max_reward_multiplier - 1) * percent_of_max_multiplier)
    print(f'calculate_steering_angle_reward :: Reward: {initial_reward:.2f} -> {new_reward:.2f}, Angle: {steering_angle}, Target Angle: {target_angle}, Rewardable Angle Range: {rewardable_angle_range}, Max Reward Multiplier: {max_reward_multiplier}')

    return new_reward


def calculate_steering_direction_reward(params, initial_reward, waypoints, target_direction, reward_multiplier):

    if params['closest_waypoints'][0] not in waypoints:
        print("calculate_steering_direction_reward :: Excluded for waypoint")
        return initial_reward

    if reward_multiplier < 1:
        raise InvalidInputException('Reward multiplier must be greater than 1')

    steering_angle = params['steering_angle']

    new_reward = initial_reward
    if (steering_angle > 0 and target_direction == 'left') or (steering_angle < 0 and target_direction == 'right'):
        new_reward *= reward_multiplier

    print(f'calculate_steering_direction_reward :: Reward: {initial_reward:.2f} -> {new_reward:.2f}, Angle: {steering_angle}, Target Direction: {target_direction}, Reward Multiplier: {reward_multiplier}')

    return float(new_reward)


def calculate_progress_reward(params, initial_reward, waypoints, target_total_steps, rewardable_step_range, max_reward_multiplier):

    if params['closest_waypoints'][0] not in waypoints:
        print("calculate_progress_reward :: Excluded for waypoint")
        return initial_reward

    if max_reward_multiplier < 1:
        raise InvalidInputException('Reward multiplier must be greater than 1')

    steps = params['steps']
    progress = params['progress']

    target_step = target_total_steps * (progress / 100)

    new_reward = initial_reward
    # If beating the target give full reward
    if steps < target_step:
        new_reward *= max_reward_multiplier
    # Otherwise if within the range give a partial reward
    else:
        step_delta = steps - target_step
        if step_delta <= rewardable_step_range:
            percent_of_max_multiplier = (rewardable_step_range - step_delta) / rewardable_step_range
            new_reward = initial_reward * (1 + (max_reward_multiplier - 1) * percent_of_max_multiplier)

    print(f'calculate_progress_reward :: Reward: {initial_reward:.2f} -> {new_reward:.2f}, Target Step: {target_step}, Actual Step: {steps}, Range: {rewardable_step_range}, Max Reward Multiplier: {max_reward_multiplier}')

    return float(new_reward)


def calculate_side_of_track_reward(params, initial_reward, waypoints, target_third_of_track, reward_multiplier):

    if params['closest_waypoints'][0] not in waypoints:
        print("calculate_side_of_track_reward :: Excluded for waypoint")
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

    print(f'calculate_side_of_track_reward :: Reward: {initial_reward:.2f} -> {new_reward:.2f}, Target Third of Track: {target_third_of_track}, Actual Third of Track: {actual_third_of_track}, Reward Multiplier: {reward_multiplier}')

    return float(new_reward)


def terminal_off_track_check(params):
    if params['is_offtrack']:
        print('terminal_off_track_check :: Off track!')
        raise TerminalConditionException


def terminal_wheel_off_track_check(params):
    if not params['all_wheels_on_track']:
        print('terminal_wheel_off_track_check :: Wheels off track!')
        raise TerminalConditionException


def terminal_reversed_check(params):
    if params['is_reversed']:
        print('terminal_reversed_check :: Reversed!')
        raise TerminalConditionException


def terminal_max_steps_check(params):
    if params['steps'] >= Settings.max_steps:
        print('terminal_max_steps_check :: Max steps reached!')
        raise TerminalConditionException


class InvalidInputException(Exception):
    pass


class TerminalConditionException(Exception):
    pass


class Settings:
    terminal_reward = 1e-3
    max_steps = 250


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
