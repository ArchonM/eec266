s1_p01_transistion = [0.01, 0.01, 0.02, 0.02, 0.03, 0.03, 0.04, 0.04, 0.05, 0.05]
s1_p10_transistion = [0.08, 0.07, 0.08, 0.07, 0.08, 0.07, 0.02, 0.02, 0.02, 0.01]
s2_p01_transistion = [0.1, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
s2_p10_transistion = [0.9, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
s3_p01_transistion = [0.01, 0.1, 0.02, 0.3, 0.04, 0.5, 0.06, 0.7, 0.08, 0.9]
s3_p10_transistion = [0.09, 0.9, 0.08, 0.7, 0.06, 0.5, 0.04, 0.3, 0.02, 0.1]
s4_p01_transistion = [0.02, 0.04, 0.04, 0.5, 0.06, 0.05, 0.7, 0.8, 0.9, 0.9]
s4_p10_transistion = [0.03, 0.03, 0.04, 0.4, 0.05, 0.06, 0.6, 0.7, 0.8, 0.9]

s1_mean_rewards = [0.20, 0.21, 0.28, 0.30, 0.35, 0.37, 0.70, 0.82, 0.74, 0.85]
s2_mean_rewards = [0.19, 0.19, 0.28, 0.37, 0.46, 0.55, 0.64, 0.73, 0.82, 0.91]
s3_mean_rewards = [0.19, 0.19, 0.28, 0.37, 0.46, 0.55, 0.64, 0.73, 0.82, 0.91]
s4_mean_rewards = [0.460, 0.641, 0.550, 0.600, 0.591, 0.509, 0.585, 0.580, 0.577, 0.550]

L_argument = [7200, 3600, 360, 1]
M_argument = [1, 2, 3, 4, 5]
corrected_coef1 = [2.1, 2.4, 2.75, 3, 4.4]
corrected_coef2 = [2.1, 2.5, 3, 3.6, 4.4]


class ucb_arm():
    def __init__(self, mean_reward, p01, p10):
        self.index = 0;
        self.mean_reward = mean_reward;
        self.s1_reward = 1;
        self.s0_reward = 0.1;
        self.total_reward = 0;
        self.p01 = p01 * 100;
        self.p10 = p10 * 100;
        self.counter = 0;
        self.sub_counter = 0;
        self.cur_state = 0;

class arm():
    def __init__(self, mean_reward, p01, p10):
        self.index = 0;
        self.mean_reward = mean_reward;
        self.s1_reward = 1;
        self.s0_reward = 0.1;
        self.total_reward = 0;
        self.p01 = p01 * 100;
        self.p10 = p10* 100;
        self.counter = 0;
        self.sub_counter = 0;
        self.cur_state = 0;
        self.never_played = True;
        self.block_indicator = 0;
        self.prespecified_state = 0;
