import unittest

from reward_modifiers import calculate_speed_reward, InvalidInputException, terminal_off_track_check, Settings, \
    TerminalConditionException, terminal_reversed_check, terminal_max_steps_check, WaypointHelper, \
    calculate_steering_angle_reward, calculate_side_of_track_reward, calculate_steering_direction_reward, \
    terminal_wheel_off_track_check, calculate_progress_reward


class TestRewardModifiers(unittest.TestCase):

    def test_calculate_speed_reward(self):

        # If outside targeted waypoints just return initial reward
        self.assertEqual(1, calculate_speed_reward(params={'speed': 5, 'closest_waypoints': [0]}, initial_reward=1, waypoints={1}, target_speed=5, rewardable_speed_range=10, max_reward_multiplier=10))

        # If in targeted waypoint and perfectly matching target speed, multiply reward by max multiplier
        self.assertEqual(10, calculate_speed_reward(params={'speed': 5, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_speed=5, rewardable_speed_range=10, max_reward_multiplier=10))
        self.assertEqual(20, calculate_speed_reward(params={'speed': 5, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_speed=5, rewardable_speed_range=10, max_reward_multiplier=20))

        # If in target waypoints and within speed range, give reward multiple equal to proximity to the target speed
        self.assertAlmostEqual(1, calculate_speed_reward(params={'speed': 3, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_speed=5, rewardable_speed_range=2, max_reward_multiplier=2))
        self.assertAlmostEqual(1.05, calculate_speed_reward(params={'speed': 3.1, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_speed=5, rewardable_speed_range=2, max_reward_multiplier=2))
        self.assertAlmostEqual(1.5, calculate_speed_reward(params={'speed': 4, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_speed=5, rewardable_speed_range=2, max_reward_multiplier=2))
        self.assertAlmostEqual(1.95, calculate_speed_reward(params={'speed': 4.9, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_speed=5, rewardable_speed_range=2, max_reward_multiplier=2))
        self.assertAlmostEqual(2, calculate_speed_reward(params={'speed': 5, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_speed=5, rewardable_speed_range=2, max_reward_multiplier=2))
        self.assertAlmostEqual(1.95, calculate_speed_reward(params={'speed': 5.1, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_speed=5, rewardable_speed_range=2, max_reward_multiplier=2))
        self.assertAlmostEqual(1.5, calculate_speed_reward(params={'speed': 6, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_speed=5, rewardable_speed_range=2, max_reward_multiplier=2))
        self.assertAlmostEqual(1.05, calculate_speed_reward(params={'speed': 6.9, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_speed=5, rewardable_speed_range=2, max_reward_multiplier=2))
        self.assertAlmostEqual(1, calculate_speed_reward(params={'speed': 7, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_speed=5, rewardable_speed_range=2, max_reward_multiplier=2))

        # If outside the rewardable range the initial reward value should be returned
        self.assertEqual(1, calculate_speed_reward(params={'speed': 5, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_speed=10, rewardable_speed_range=2, max_reward_multiplier=10))

        # If max reward multiplier is < 1 InvalidInput should be raised
        with self.assertRaises(InvalidInputException):
            calculate_speed_reward(params={'speed': 5, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_speed=5, rewardable_speed_range=10, max_reward_multiplier=0.9)


    def test_calculate_steering_angle_reward(self):

        # If outside targeted waypoints just return initial reward
        self.assertEqual(1, calculate_steering_angle_reward(params={'steering_angle': 5, 'closest_waypoints': [0]}, initial_reward=1, waypoints={1}, target_angle=20, rewardable_angle_range=10, max_reward_multiplier=10))

        # If in targeted waypoint and perfectly matching target angle, multiply reward by max multiplier
        self.assertEqual(10, calculate_steering_angle_reward(params={'steering_angle': 20, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_angle=20, rewardable_angle_range=10, max_reward_multiplier=10))
        self.assertEqual(20, calculate_steering_angle_reward(params={'steering_angle': 20, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_angle=20, rewardable_angle_range=10, max_reward_multiplier=20))

        # If in targeted waypoint and within angle range, give reward multiple equal to proximity to the target angle
        self.assertEqual(20, calculate_steering_angle_reward(params={'steering_angle': 20, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_angle=20, rewardable_angle_range=10, max_reward_multiplier=20))

        # If outside the rewardable range the initial reward value should be returned
        self.assertEqual(1, calculate_steering_angle_reward(params={'steering_angle': 10, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_angle=20, rewardable_angle_range=10, max_reward_multiplier=10))
        self.assertEqual(1.9, calculate_steering_angle_reward(params={'steering_angle': 11, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_angle=20, rewardable_angle_range=10, max_reward_multiplier=10))
        self.assertEqual(9.1, calculate_steering_angle_reward(params={'steering_angle': 19, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_angle=20, rewardable_angle_range=10, max_reward_multiplier=10))
        self.assertEqual(10, calculate_steering_angle_reward(params={'steering_angle': 20, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_angle=20, rewardable_angle_range=10, max_reward_multiplier=10))
        self.assertEqual(9.1, calculate_steering_angle_reward(params={'steering_angle': 21, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_angle=20, rewardable_angle_range=10, max_reward_multiplier=10))
        self.assertEqual(1.9, calculate_steering_angle_reward(params={'steering_angle': 29, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_angle=20, rewardable_angle_range=10, max_reward_multiplier=10))
        self.assertEqual(1, calculate_steering_angle_reward(params={'steering_angle': 30, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_angle=20, rewardable_angle_range=10, max_reward_multiplier=10))

        # If max reward multiplier is < 1 InvalidInput should be raised
        with self.assertRaises(InvalidInputException):
            calculate_steering_angle_reward(params={'steering_angle': 5, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_angle=5, rewardable_angle_range=10, max_reward_multiplier=0.9)


    def test_calculate_steering_direction_reward(self):

        # If outside targeted waypoints just return initial reward
        self.assertEqual(1, calculate_steering_direction_reward(params={'steering_angle': 5, 'closest_waypoints': [0]}, initial_reward=1, waypoints={1}, target_direction='left', reward_multiplier=20))

        # If turning the desired direction, apply the reward multiplier
        self.assertEqual(20, calculate_steering_direction_reward(params={'steering_angle': 5, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_direction='left', reward_multiplier=20))
        self.assertEqual(20, calculate_steering_direction_reward(params={'steering_angle': -5, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_direction='right', reward_multiplier=20))

        # If not turning the desired direction, do not apply the reward multiplier
        self.assertEqual(1, calculate_steering_direction_reward(params={'steering_angle': 5, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_direction='right', reward_multiplier=20))
        self.assertEqual(1, calculate_steering_direction_reward(params={'steering_angle': -5, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_direction='left', reward_multiplier=20))

        # If max reward multiplier is < 1 InvalidInput should be raised
        with self.assertRaises(InvalidInputException):
            calculate_steering_direction_reward(params={'steering_angle': -5, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_direction='left', reward_multiplier=0.9)


    def test_calculate_progress_reward(self):

        # If outside targeted waypoints just return initial reward
        self.assertEqual(1, calculate_progress_reward(params={'closest_waypoints': [0], 'progress': 80}, initial_reward=1, waypoints={1}, target_total_steps=100, rewardable_step_range=20, max_reward_multiplier=10))

        # If beating target get full reward
        self.assertEqual(10, calculate_progress_reward(params={'closest_waypoints': [0], 'progress': 80, 'steps': 50}, initial_reward=1, waypoints={0}, target_total_steps=100, rewardable_step_range=20, max_reward_multiplier=10))

        # If inside target range get partial reward
        self.assertEqual(10, calculate_progress_reward(params={'closest_waypoints': [0], 'progress': 80, 'steps': 80}, initial_reward=1, waypoints={0}, target_total_steps=100, rewardable_step_range=20, max_reward_multiplier=10))
        self.assertEqual(7.75, calculate_progress_reward(params={'closest_waypoints': [0], 'progress': 80, 'steps': 85}, initial_reward=1, waypoints={0}, target_total_steps=100, rewardable_step_range=20, max_reward_multiplier=10))
        self.assertEqual(5.5, calculate_progress_reward(params={'closest_waypoints': [0], 'progress': 80, 'steps': 90}, initial_reward=1, waypoints={0}, target_total_steps=100, rewardable_step_range=20, max_reward_multiplier=10))
        self.assertEqual(3.25, calculate_progress_reward(params={'closest_waypoints': [0], 'progress': 80, 'steps': 95}, initial_reward=1, waypoints={0}, target_total_steps=100, rewardable_step_range=20, max_reward_multiplier=10))
        self.assertEqual(1, calculate_progress_reward(params={'closest_waypoints': [0], 'progress': 80, 'steps': 100}, initial_reward=1, waypoints={0}, target_total_steps=100, rewardable_step_range=20, max_reward_multiplier=10))

        # If outside range get initial reward only
        self.assertEqual(1, calculate_progress_reward(params={'closest_waypoints': [0], 'progress': 80, 'steps': 120}, initial_reward=1, waypoints={0}, target_total_steps=100, rewardable_step_range=20, max_reward_multiplier=10))

        with self.assertRaises(InvalidInputException):
            self.assertEqual(10, calculate_progress_reward(params={'closest_waypoints': [0], 'progress': 80, 'steps': 50}, initial_reward=1, waypoints={0}, target_total_steps=100, rewardable_step_range=20, max_reward_multiplier=.9))


    def test_calculate_side_of_track_reward(self):

        # If outside targeted waypoints just return initial reward
        self.assertEqual(1, calculate_side_of_track_reward(params={'closest_waypoints': [0]}, initial_reward=1, waypoints={1}, target_third_of_track='left', reward_multiplier=10))

        # If targeting left and in left reward is multiplied
        self.assertEqual(10, calculate_side_of_track_reward(params={'closest_waypoints': [0], 'is_left_of_center': True, 'track_width': 100, 'distance_from_center': 45}, initial_reward=1, waypoints={0}, target_third_of_track='left', reward_multiplier=10))

        # If targeting left and in either middle or right do not reward
        self.assertEqual(1, calculate_side_of_track_reward(params={'closest_waypoints': [0], 'is_left_of_center': False, 'track_width': 100, 'distance_from_center': 45}, initial_reward=1, waypoints={0}, target_third_of_track='left', reward_multiplier=10))
        self.assertEqual(1, calculate_side_of_track_reward(params={'closest_waypoints': [0], 'is_left_of_center': True, 'track_width': 100, 'distance_from_center': 0}, initial_reward=1, waypoints={0}, target_third_of_track='left', reward_multiplier=10))

        # If targeting middle and in middle reward is multiplied
        self.assertEqual(10, calculate_side_of_track_reward(params={'closest_waypoints': [0], 'is_left_of_center': True, 'track_width': 100, 'distance_from_center': 5}, initial_reward=1, waypoints={0}, target_third_of_track='middle', reward_multiplier=10))

        # If targeting middle and in either left or right do not reward
        self.assertEqual(1, calculate_side_of_track_reward(params={'closest_waypoints': [0], 'is_left_of_center': False, 'track_width': 100, 'distance_from_center': 45}, initial_reward=1, waypoints={0}, target_third_of_track='middle', reward_multiplier=10))
        self.assertEqual(1, calculate_side_of_track_reward(params={'closest_waypoints': [0], 'is_left_of_center': True, 'track_width': 100, 'distance_from_center': 45}, initial_reward=1, waypoints={0}, target_third_of_track='middle', reward_multiplier=10))

        # If targeting right and in right reward is multiplied
        self.assertEqual(10, calculate_side_of_track_reward(params={'closest_waypoints': [0], 'is_left_of_center': False, 'track_width': 100, 'distance_from_center': 45}, initial_reward=1, waypoints={0}, target_third_of_track='right', reward_multiplier=10))

        # If targeting right and in either left or middle do not reward
        self.assertEqual(1, calculate_side_of_track_reward(params={'closest_waypoints': [0], 'is_left_of_center': False, 'track_width': 100, 'distance_from_center': 5}, initial_reward=1, waypoints={0}, target_third_of_track='right', reward_multiplier=10))
        self.assertEqual(1, calculate_side_of_track_reward(params={'closest_waypoints': [0], 'is_left_of_center': True, 'track_width': 100, 'distance_from_center': 45}, initial_reward=1, waypoints={0}, target_third_of_track='right', reward_multiplier=10))

        with self.assertRaises(InvalidInputException):
            calculate_side_of_track_reward(params={'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_third_of_track='left', reward_multiplier=0.9)


    def test_terminal_off_track_check(self):
        # Check exception raised when off track
        with self.assertRaises(TerminalConditionException):
            terminal_off_track_check(params={'is_offtrack': True})
        # Check no exception raised when on track
        terminal_off_track_check(params={'is_offtrack': False})


    def test_terminal_wheel_off_track_check(self):
        # Check exception raised when off track
        with self.assertRaises(TerminalConditionException):
            terminal_wheel_off_track_check(params={'all_wheels_on_track': False})
        # Check no exception raised when on track
        terminal_wheel_off_track_check(params={'all_wheels_on_track': True})


    def test_terminal_reversed_check(self):
        # Check exception raised when reversed
        with self.assertRaises(TerminalConditionException):
            terminal_reversed_check(params={'is_reversed': True})
        # Check no exception raised when not reversed
        terminal_reversed_check(params={'is_reversed': False})

    def test_terminal_max_steps_check(self):
        # Check exception raised when max steps reached
        with self.assertRaises(TerminalConditionException):
            terminal_max_steps_check(params={'steps': Settings.max_steps})
        # Check no exception raised when not max steps reached
        terminal_max_steps_check(params={'steps': Settings.max_steps - 1})

    def test_waypoint_helper_generate_waypoints(self):
        test_cases = [
            ("1:10", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            ("2:4,6:8", [2, 3, 4, 6, 7, 8]),
            ("1:4,7,9", [1, 2, 3, 4, 7, 9])
        ]

        for case, expected in test_cases:
            result = WaypointHelper.generate_waypoints(case)
            self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
