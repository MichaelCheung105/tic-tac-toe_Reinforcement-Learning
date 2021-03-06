# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 20:11:01 2018
@author: lupus
"""

"""define winning function"""
def win(matrix):
    
    won = False
    
    if \
    abs(matrix[0] + matrix[1] + matrix[2]) == 3 or \
    abs(matrix[3] + matrix[4] + matrix[5]) == 3 or \
    abs(matrix[6] + matrix[7] + matrix[8]) == 3 or \
    abs(matrix[0] + matrix[3] + matrix[6]) == 3 or \
    abs(matrix[1] + matrix[4] + matrix[7]) == 3 or \
    abs(matrix[2] + matrix[5] + matrix[8]) == 3 or \
    abs(matrix[0] + matrix[4] + matrix[8]) == 3 or \
    abs(matrix[2] + matrix[4] + matrix[6]) == 3:
        
        won = True
    
    return won
"""define winning function"""

import random
import numpy as np
import matplotlib.pyplot as plt

max_episode = 100000
episode = 1
epsilon = 0.3
seen_states = {}
winning_list = []
number_of_seen_states = []

while episode <= max_episode:
    matrix = [0]*9
    episode_states = []
    
    while 0 in matrix:
        #black move
        possible_action_list = [i for i, v in enumerate(matrix) if v == 0]
        number_of_options = len(possible_action_list)
        expected_reward_list = [0]*number_of_options
        selection_prob_list = [0]*number_of_options
        
        for index, possible_action in enumerate(possible_action_list):
            possible_state = matrix.copy()
            possible_state[possible_action] = 1
            
            if str(possible_state) not in seen_states:
                seen_states[str(possible_state)] = {}
                seen_states[str(possible_state)]["expected_reward"] = 0
                seen_states[str(possible_state)]["counter"] = 0
            
            expected_reward_list[index] = seen_states[str(possible_state)]["expected_reward"]
            if number_of_options != 1:
                selection_prob_list[index] = 1/number_of_options - epsilon/(number_of_options - 1)
            else:
                selection_prob_list[index] = 1/number_of_options
                
        best_option_index = expected_reward_list.index(max(expected_reward_list))
        if number_of_options != 1:
            selection_prob_list[best_option_index] = 1/number_of_options + epsilon

        final_decision = np.random.choice(possible_action_list, p=selection_prob_list)
        matrix[final_decision] = 1
        episode_states.append(str(matrix))
        
        if win(matrix):
            winner = "black"
            break
        
        if 0 not in matrix:
            winner = "draw"
            break
            
        else:
            #white move
            possible_action_list = [i for i, v in enumerate(matrix) if v == 0]
            number_of_options = len(possible_action_list)
            expected_reward_list = [0]*number_of_options
            selection_prob_list = [0]*number_of_options
            
            for index, possible_action in enumerate(possible_action_list):
                possible_state = matrix.copy()
                possible_state[possible_action] = -1
                
                if str(possible_state) not in seen_states:
                    seen_states[str(possible_state)] = {}
                    seen_states[str(possible_state)]["expected_reward"] = 0
                    seen_states[str(possible_state)]["counter"] = 0
                
                expected_reward_list[index] = seen_states[str(possible_state)]["expected_reward"]
                if number_of_options != 1:
                    selection_prob_list[index] = 1/number_of_options - epsilon/(number_of_options - 1)
                else:
                    selection_prob_list[index] = 1/number_of_options
                
            best_option_index = expected_reward_list.index(min(expected_reward_list))
            if number_of_options != 1:
                selection_prob_list[best_option_index] = 1/number_of_options + epsilon
            
            final_decision = np.random.choice(possible_action_list, p=selection_prob_list)
            matrix[final_decision] = -1
            episode_states.append(str(matrix))
                
            if win(matrix):
                winner = "white"
                break
            
            if 0 not in matrix:
                winner = "draw"
                break

    #calculate reward for each state observed in this episode
    for state in episode_states:
        
        seen_states[state]["counter"] += 1
        
        if winner == "black":
            seen_states[state]["expected_reward"] += (1 - seen_states[state]["expected_reward"])/seen_states[state]["counter"]
        
        if winner == "white":
            seen_states[state]["expected_reward"] += (-1 - seen_states[state]["expected_reward"])/seen_states[state]["counter"]
            
        if winner == "draw":
            seen_states[state]["expected_reward"] += (0 - seen_states[state]["expected_reward"])/seen_states[state]["counter"]
    
    print(np.array(matrix).reshape((3,3)))
    print(winner)
    winning_list.append(winner)
    number_of_seen_states.append(len(seen_states))
    episode +=1

#plot a graph indicating probability for black to win
x = list(range(1,max_episode+1))
winning_ratio = [int(winning_list[0] == "black")]
for k in range(2, max_episode+1):
    winning_ratio.append(winning_ratio[-1] + (int(winning_list[k-1] == "black") - winning_ratio[-1])/k)
plt.plot(x,winning_ratio)
plt.show()
plt.clf()

#plot a graph indicating # of seen states
x = list(range(1,max_episode+1))
plt.plot(x,number_of_seen_states)
plt.show()
plt.clf()

#hist
plt.hist([seen_states[state]["expected_reward"] for state in seen_states.keys()])

#play with trained tic-tac-toe
def init_matrix():
    mat = [0]*9
    return mat

def commove(mat, seen_states):
    #com move
    possible_action_list = [i for i, v in enumerate(mat) if v == 0]
    if sum(mat) == 0:
        possible_action_expected_reward = [-2]*9
    else:
        possible_action_expected_reward = [2]*9
                
    for possible_action in possible_action_list:
        possible_state = mat.copy()
        
        if sum(mat) == 0:
            possible_state[possible_action] = 1
        else:
            possible_state[possible_action] = -1
        
        if str(possible_state) not in seen_states:
            seen_states[str(possible_state)] = {}
            seen_states[str(possible_state)]["expected_reward"] = 0
            seen_states[str(possible_state)]["counter"] = 0
        
        possible_action_expected_reward[possible_action] = seen_states[str(possible_state)]["expected_reward"]
    
    if sum(mat) == 0:
        final_decision = possible_action_expected_reward.index(max(possible_action_expected_reward))
        mat[final_decision] = 1
    else:
        final_decision = possible_action_expected_reward.index(min(possible_action_expected_reward))
        mat[final_decision] = -1
    
    if win(mat):
        print("Com won")
        return np.array(mat).reshape((3,3))
    elif 0 not in mat:
        print("draw")
        return np.array(mat).reshape((3,3))
    else:
        return np.array(mat).reshape((3,3))

def mymove(mat, location):
    if mat[location] !=0:
        print("occupied")
    else:
        if sum(mat) == 0:
            mat[location] = 1
        else:
            mat[location] = -1
        if win(mat):
            print("I win")
            return np.array(mat).reshape((3,3))
        elif 0 not in mat:
            print("draw")
            return np.array(mat).reshape((3,3))
        else:
            return np.array(mat).reshape((3,3))
