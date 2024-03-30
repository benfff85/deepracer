

def calculate_speed_reward(params, initial_reward, weight):
    speed = params['speed']
    new_reward = initial_reward + (weight * speed)
    print(f'Reward: {initial_reward} -> {new_reward}, Speed: {speed}, Weight: {weight}')
    return new_reward
