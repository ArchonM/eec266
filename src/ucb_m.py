import matplotlib.pyplot as plt
import math
import random

import dataset as dt

m = 1

class UCB_M():
    def __init__(self, mean_rewards, p01_transition, p10_transition):
        self.arms = []
        self.sorted_indices = []
        self.num_arms = len(mean_rewards)
        self.total_reward = 0;
        self.best_reward = 0;
        self.play_counter = 0;
        for i in range(len(mean_rewards)):
            arm_tmp = dt.ucb_arm(mean_rewards[i], p01_transition[i], p10_transition[i])
            self.arms.append(arm_tmp)
            self.sorted_indices.append(i)

        return
    
    def update_sorted_indices(self):
        for i in range(1, self.num_arms):
            for j in range(0, self.num_arms - 1):
                if self.arms[self.sorted_indices[j]].index < self.arms[self.sorted_indices[j+1]].index:
                    self.sorted_indices[j], self.sorted_indices[j+1] = self.sorted_indices[j+1], self.sorted_indices[j]
            
        return

    def find_m_max(self):
        result = []
        for i in range(m):
            result.append(self.sorted_indices[i])
        return result

    def play(self, i):
        x = random.randint(0, 100)
        if self.arms[i].cur_state == 0:
            if x < self.arms[i].p01:
                self.total_reward += 1
                self.best_reward += self.arms[i].mean_reward
                self.arms[i].cur_state = 1
                self.arms[i].counter += 1
                self.arms[i].sub_counter += 1
                self.arms[i].total_reward += 1
            else:
                self.total_reward += 0.1
                self.best_reward += self.arms[i].mean_reward
                self.arms[i].cur_state = 0
                self.arms[i].counter += 1
                self.arms[i].sub_counter += 1
                self.arms[i].total_reward += 0.1
        else:
            if x > self.arms[i].p10:
                self.total_reward += 1
                self.best_reward += self.arms[i].mean_reward
                self.arms[i].cur_state = 1
                self.arms[i].counter += 1
                self.arms[i].sub_counter += 1
                self.arms[i].total_reward += 1
            else:
                self.total_reward += 0.1
                self.best_reward += self.arms[i].mean_reward
                self.arms[i].cur_state = 0
                self.arms[i].counter += 1
                self.arms[i].sub_counter += 1
                self.arms[i].total_reward += 0.1

    def initialize(self):
        for x in range(m):
            for i in range(self.num_arms):
                self.play(i)

def run_ucb(mean_rewards, p01_transistion, p10_transistion):
    mab = UCB_M(mean_rewards, p01_transistion, p10_transistion)
    mab.initialize()
    i = 1
    plot_x = [0]
    plot_y = [0]
    while i <= 100000:
        for arm in mab.arms:
            try:
                arm.index = (arm.total_reward/arm.counter) + math.sqrt((1 * math.log(i))/arm.counter)
            except:
                print(arm.total_reward)
                print(arm.counter)
                print(i)
                print(arm.counter)
        
        mab.update_sorted_indices()
        for m in mab.find_m_max():
            mab.play(m)
            i += 1
        if i % 100 == 0:
            plot_x.append(i)
            plot_y.append((mab.best_reward-mab.total_reward)/math.log(i))
    
    print(mab.best_reward)
    print(mab.total_reward)

    return plot_x, plot_y


def main():
    fig, ax = plt.subplots()
    plot_x, plot_y = run_ucb(dt.s1_mean_rewards, dt.s1_p01_transistion, dt.s1_p10_transistion)
    ax.plot(plot_x, plot_y, label='s1, L=1')
    plot_x, plot_y = run_ucb(dt.s2_mean_rewards, dt.s2_p01_transistion, dt.s2_p10_transistion)
    ax.plot(plot_x, plot_y, label='s2, L=1')
    plot_x, plot_y = run_ucb(dt.s3_mean_rewards, dt.s3_p01_transistion, dt.s3_p10_transistion)
    ax.plot(plot_x, plot_y, label='s3, L=1')
    plot_x, plot_y = run_ucb(dt.s4_mean_rewards, dt.s4_p01_transistion, dt.s4_p10_transistion)
    ax.plot(plot_x, plot_y, label='s4, L=1')
    
    ax.set_xlabel('n')
    ax.set_ylabel('R(n)/(ln(n))')
    ax.set_title('Regret of UCB, M = 1')
    ax.legend()
    plt.savefig('UCB.png')

        


if __name__ == "__main__":
    main();