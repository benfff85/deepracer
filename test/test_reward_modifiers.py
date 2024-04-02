import unittest

from reward_modifiers import calculate_speed_reward, InvalidInputException, terminal_off_track_check, Settings, \
    TerminalConditionException, terminal_reversed_check, terminal_max_steps_check


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

    def test_terminal_off_track_check(self):
        # Check exception raised when off track
        with self.assertRaises(TerminalConditionException):
            terminal_off_track_check(params={'is_offtrack': True})
        # Check no exception raised when on track
        terminal_off_track_check(params={'is_offtrack': False})

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


if __name__ == '__main__':
    unittest.main()
