import unittest

from reward_modifiers import calculate_speed_reward


class TestRewardModifiers(unittest.TestCase):

    def test_speed_reward_calculation(self):

        self.assertEqual(calculate_speed_reward(params={'speed': 10}, initial_reward=0, weight=1), 10)
        self.assertEqual(calculate_speed_reward(params={'speed': 10}, initial_reward=0, weight=2), 20)
        self.assertEqual(calculate_speed_reward(params={'speed': 10}, initial_reward=5, weight=1), 15)
        self.assertEqual(calculate_speed_reward(params={'speed': 10}, initial_reward=-5, weight=1), 5)
        self.assertEqual(calculate_speed_reward(params={'speed': 0}, initial_reward=0, weight=1), 0)


if __name__ == '__main__':
    unittest.main()
