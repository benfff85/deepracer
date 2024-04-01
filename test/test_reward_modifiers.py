import unittest

from reward_modifiers import calculate_speed_reward, InvalidInput


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
        with self.assertRaises(InvalidInput):
            calculate_speed_reward(params={'speed': 5, 'closest_waypoints': [0]}, initial_reward=1, waypoints={0}, target_speed=5, rewardable_speed_range=10, max_reward_multiplier=0.9)


if __name__ == '__main__':
    unittest.main()
