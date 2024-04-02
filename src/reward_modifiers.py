

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


def terminal_off_track_check(params):
    if params['is_offtrack']:
        raise TerminalConditionException


def terminal_reversed_check(params):
    if params['is_reversed']:
        raise TerminalConditionException


def terminal_max_steps_check(params):
    if params['steps'] >= Settings.max_steps:
        raise TerminalConditionException


class InvalidInputException(Exception):
    pass


class TerminalConditionException(Exception):
    pass


class Settings:
    terminal_reward = .001
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
