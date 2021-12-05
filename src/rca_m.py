import matplotlib.pyplot as plt
import math
import random

from numpy import zeros

import dataset as dt

s1_top_5 = [0.85, 0.82, 0.74, 0.70, 0.37]


class RCA_M():
    def __init__(self, mean_rewards, p01_transition, p10_transition):
        self.sb1 = []
        self.sb2 = []
        self.sb3 = []
        self.arms = []
        self.sorted_indices = []
        self.num_arms = len(mean_rewards)
        self.total_reward = 0;
        self.best_reward = 0;
        self.real_counter = 0;
        self.play_counter = 0;
        for i in range(len(mean_rewards)):
            arm_tmp = dt.arm(mean_rewards[i], p01_transition[i], p10_transition[i])
            self.arms.append(arm_tmp)
            self.sorted_indices.append(i)

        return

    def update_sorted_indices(self):
        for i in range(1, self.num_arms):
            for j in range(0, self.num_arms - 1):
                if self.arms[self.sorted_indices[j]].index < self.arms[self.sorted_indices[j+1]].index:
                    self.sorted_indices[j], self.sorted_indices[j+1] = self.sorted_indices[j+1], self.sorted_indices[j]
        return
    
    def find_m_max(self, m):
        result = []
        for i in range(m):
            result.append(self.sorted_indices[i])
        return result
    
    def update_best_reward(self, L, M, value):
        if L == dt.L_argument[0]:
            for i in range(len(dt.M_argument)):
                if M == dt.M_argument[i]:
                    return value/dt.corrected_coef1[i]
        elif L == dt.L_argument[1]:
            for i in range(len(dt.M_argument)):
                if M == dt.M_argument[i]:
                    return value/dt.corrected_coef2[i]
        
        return value


    def play(self, i):
        x = random.randint(0, 100)
        if self.arms[i].cur_state == 0:
            if x < self.arms[i].p01:
                self.arms[i].cur_state = 1
                self.arms[i].counter += 1
                self.arms[i].sub_counter += 1
                self.arms[i].total_reward += 1
            else:
                self.arms[i].cur_state = 0
                self.arms[i].counter += 1
                self.arms[i].sub_counter += 1
                self.arms[i].total_reward += 0.1
        else:
            if x > self.arms[i].p10:
                self.arms[i].cur_state = 1
                self.arms[i].counter += 1
                self.arms[i].sub_counter += 1
                self.arms[i].total_reward += 1
            else:
                self.arms[i].cur_state = 0
                self.arms[i].counter += 1
                self.arms[i].sub_counter += 1
                self.arms[i].total_reward += 0.1
        return self.arms[i].cur_state

def run_rca(mean_rewards, p01_transistion, p10_transistion, L, M):
    mab = RCA_M(mean_rewards, p01_transistion, p10_transistion)

    cur_arms = [];
    plot_x = [0]
    plot_y = [0]
    while mab.play_counter < 100100:
        for i in range(10):
            if len(cur_arms) < M and mab.arms[i].never_played:
                cur_arms.append(i)
        
        if len(cur_arms) < M:
            for i in mab.find_m_max(M-len(cur_arms)):
                cur_arms.append(i)

        for i in cur_arms:
            cur_state = mab.play(i)
            if mab.arms[i].never_played:
                mab.arms[i].prespecified_state = cur_state
                mab.play_counter += 1
                mab.arms[i].never_played = False
                mab.arms[i].block_indicator = 2
                if cur_state == 1:
                    mab.total_reward += 1
                else:
                    mab.total_reward += 0.1
            elif cur_state != mab.arms[i].prespecified_state and mab.arms[i].block_indicator == 2:
                mab.play_counter += 1
                if cur_state == 1:
                    mab.total_reward += 1
                else:
                    mab.total_reward += 0.1
            elif cur_state == mab.arms[i].prespecified_state and mab.arms[i].block_indicator != 2:
                mab.play_counter += 1
                if cur_state == 1:
                    mab.total_reward += 1
                else:
                    mab.total_reward += 0.1
                mab.arms[i].block_indicator = 2;
            elif cur_state == mab.arms[i].prespecified_state and mab.arms[i].block_indicator == 2:
                if cur_state == 1:
                    mab.total_reward += 1
                else:
                    mab.total_reward += 0.1
                mab.arms[i].block_indicator = 0;
                cur_arms.remove(i)

        mab.real_counter += 1
        if len(cur_arms) > 0:
            mab.play_counter += 1

        for arm in mab.arms:
            try:
                arm.index = (arm.total_reward/arm.counter) + math.sqrt(L * math.log(mab.play_counter)/arm.counter)
            except:
                pass
        
        if mab.play_counter%10000 < M + 10:
            plot_x.append(mab.play_counter)
            best_sum = 0.0
            for i in range(M):
                best_sum += s1_top_5[i]
            best_reward = (mab.play_counter/M)*best_sum
            plot_y.append(mab.update_best_reward(L, M, (best_reward-mab.total_reward)/math.log(mab.play_counter)))

    return plot_x, plot_y





def main():
    fig, ax = plt.subplots()
    plot_x, plot_y = run_rca(dt.s1_mean_rewards, dt.s1_p01_transistion, dt.s1_p10_transistion, 7200, 1)
    ax.plot(plot_x, plot_y, label='M=1')
    plot_x, plot_y = run_rca(dt.s1_mean_rewards, dt.s1_p01_transistion, dt.s1_p10_transistion, 7200, 2)
    ax.plot(plot_x, plot_y, label='M=2')
    plot_x, plot_y = run_rca(dt.s1_mean_rewards, dt.s1_p01_transistion, dt.s1_p10_transistion, 7200, 3)
    ax.plot(plot_x, plot_y, label='M=3')
    plot_x, plot_y = run_rca(dt.s1_mean_rewards, dt.s1_p01_transistion, dt.s1_p10_transistion, 7200, 4)
    ax.plot(plot_x, plot_y, label='M=4')
    plot_x, plot_y = run_rca(dt.s1_mean_rewards, dt.s1_p01_transistion, dt.s1_p10_transistion, 7200, 5)
    ax.plot(plot_x, plot_y, label='M=5')
    ax.set_xlabel('n')
    ax.set_ylabel('R(n)/(ln(n))')
    ax.set_title('Regret of RCA-M: S1, L = 7200')
    ax.legend()
    plt.grid()
    plt.savefig('../graphs/RCA_M_7200.png')

    fig, ax = plt.subplots()
    plot_x, plot_y = run_rca(dt.s3_mean_rewards, dt.s3_p01_transistion, dt.s3_p10_transistion, 3600, 1)
    ax.plot(plot_x, plot_y, label='M=1')
    plot_x, plot_y = run_rca(dt.s3_mean_rewards, dt.s3_p01_transistion, dt.s3_p10_transistion, 3600, 2)
    ax.plot(plot_x, plot_y, label='M=2')
    plot_x, plot_y = run_rca(dt.s3_mean_rewards, dt.s3_p01_transistion, dt.s3_p10_transistion, 3600, 3)
    ax.plot(plot_x, plot_y, label='M=3')
    plot_x, plot_y = run_rca(dt.s3_mean_rewards, dt.s3_p01_transistion, dt.s3_p10_transistion, 3600, 4)
    ax.plot(plot_x, plot_y, label='M=4')
    plot_x, plot_y = run_rca(dt.s3_mean_rewards, dt.s3_p01_transistion, dt.s3_p10_transistion, 3600, 5)
    ax.plot(plot_x, plot_y, label='M=5')
    ax.set_xlabel('n')
    ax.set_ylabel('R(n)/(ln(n))')
    ax.set_title('Regret of RCA-M: S3, L = 3600')
    ax.legend()
    plt.grid()
    plt.savefig('../graphs/RCA_M_3600.png')

if __name__ == "__main__":
    main();