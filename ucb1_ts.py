import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from collections import deque

def sample_arm(rewardProbabilities, arm):
    return int(float(rewardProbabilities[arm]) > np.random.rand())


def ts(alpha,beta,armToChoose, rewardProbabilities, avgReward, numSelections, gainedReward):
    sampled_means = np.random.beta(alpha, beta)
    selected_arms = np.argsort(sampled_means)[-armToChoose:]
    numSelections[selected_arms] = numSelections[selected_arms] + 1
    for j in selected_arms:
        reward = sample_arm(rewardProbabilities, j)
        alpha[j] = alpha[j] + reward
        beta[j] = beta[j] + 1 - reward
        avgReward[j] = avgReward[j] + (reward)/numSelections[j]
        gainedReward = gainedReward + reward
    return alpha, beta, avgReward, numSelections, gainedReward

def ts_delayed(alphad, betad, numSelections, avgReward, numOfArms, armToChoose, roundNum, gainedReward, rewardProbabilities, fifo, fifoSize, delays, delayTime):
    if((np.size(np.argwhere(numSelections < delayTime))) > 0):
        #selections  = np.random.choice(numOfArms, armToChoose, replace=False)
        selections  = (np.arange(armToChoose) + roundNum % numOfArms) % numOfArms -1
        numSelections[selections] = numSelections[selections] + 1
        for j in selections:    
            loc = np.argwhere(delays[j] == -1)
            loc = loc[0][0]
            delays[j, loc] = delayTime

    else:
        sampled_means = np.random.beta(alphad, betad)
        selections = np.argsort(sampled_means)[-armToChoose:]
        for j in selections:
            tmpIdx = np.random.randint(0, fifoSize)
            reward = fifo[j, tmpIdx]
            alphad[j] = alphad[j] + reward
            betad[j] = betad[j] + 1 - reward
            loc = np.argwhere(delays[j] == -1)
            loc = loc[0][0]
            delays[j, loc] = delayTime
            avgReward[j] = avgReward[j] + (reward)/numSelections[j]
            
    if ((np.size(np.argwhere(delays == 0))) > 0):
        for m in np.argwhere(delays==0):
            
            tmp_queue = deque(fifo[m[0],:].ravel(), maxlen=fifoSize)
            reward = sample_arm(rewardProbabilities, m[0])
            tmp_queue.appendleft(reward)
            fifo[m[0],:] = np.array(tmp_queue)
            delays[tuple(m)] = -1
            gainedReward = gainedReward + reward
            

    return alphad, betad, numSelections, avgReward, gainedReward, fifo, delays


def ucb(numSelections, avgReward, numOfArms, armToChoose, roundNum, gainedReward, rewardProbilities):

    if((np.size(np.argwhere(numSelections == 0))) > 0):
        #selections  = np.random.choice(numOfArms, armToChoose, replace=False)
        selections  = (np.arange(armToChoose) + roundNum % numOfArms) % numOfArms -1
    else:
        UCB = avgReward + np.sqrt(2*np.log(roundNum)/numSelections)
        selections = np.argpartition(UCB, -armToChoose)[-armToChoose:]
    
    for j in selections:
        reward = sample_arm(rewardProbilities, j)
        numSelections[j] = numSelections[j] + 1
        avgReward[j] = avgReward[j] + (reward)/numSelections[j]
        gainedReward = gainedReward + reward

    return numSelections, avgReward, gainedReward

def ucb_delayed_pure(numSelections, avgReward, numOfArms, armToChoose, roundNum, gainedReward, rewardProbabilities, fifo, fifoSize, delays, delayTime):

    if((np.size(np.argwhere(numSelections < delayTime))) > 0):
        #selections  = np.random.choice(numOfArms, armToChoose, replace=False)
        selections  = (np.arange(armToChoose) + roundNum % numOfArms) % numOfArms -1
        numSelections[selections] = numSelections[selections] + 1
        for j in selections:    
            loc = np.argwhere(delays[j] == -1)
            loc = loc[0][0]
            delays[j, loc] = delayTime
    else:
        UCB = avgReward + np.sqrt(2*np.log(roundNum)/numSelections)
        selections = np.argpartition(UCB, -armToChoose)[-armToChoose:]
        numSelections[selections] = numSelections[selections] + 1
        
        for j in selections:
            tmpIdx = np.random.randint(0, fifoSize)
            reward = fifo[j, tmpIdx]
            loc = np.argwhere(delays[j] == -1)
            loc = loc[0][0]
            delays[j, loc] = delayTime
            
    if ((np.size(np.argwhere(delays == 0))) > 0):
        for m in np.argwhere(delays==0):
            reward = sample_arm(rewardProbabilities, m[0])
            delays[tuple(m)] = -1
            gainedReward = gainedReward + reward
            avgReward[j] = avgReward[j] + (reward)/numSelections[j]
            

    return numSelections, avgReward, gainedReward, delays, fifo

def ucb_delayed(numSelections, avgReward, numOfArms, armToChoose, roundNum, gainedReward, rewardProbabilities, fifo, fifoSize, delays, delayTime):

    if((np.size(np.argwhere(numSelections < delayTime))) > 0):
        #selections  = np.random.choice(numOfArms, armToChoose, replace=False)
        selections  = (np.arange(armToChoose) + roundNum % numOfArms) % numOfArms -1
        numSelections[selections] = numSelections[selections] + 1
        for j in selections:    
            loc = np.argwhere(delays[j] == -1)
            loc = loc[0][0]
            delays[j, loc] = delayTime
    else:
        UCB = avgReward + np.sqrt(2*np.log(roundNum)/numSelections)
        selections = np.argpartition(UCB, -armToChoose)[-armToChoose:]
        numSelections[selections] = numSelections[selections] + 1
        
        for j in selections:
            tmpIdx = np.random.randint(0, fifoSize)
            reward = fifo[j, tmpIdx]
            loc = np.argwhere(delays[j] == -1)
            loc = loc[0][0]
            delays[j, loc] = delayTime
            avgReward[j] = avgReward[j] + (reward)/numSelections[j]
            
    if ((np.size(np.argwhere(delays == 0))) > 0):
        for m in np.argwhere(delays==0):
            
            tmp_queue = deque(fifo[m[0],:].ravel(), maxlen=fifoSize)
            reward = sample_arm(rewardProbabilities, m[0])
            tmp_queue.appendleft(reward)
            fifo[m[0],:] = np.array(tmp_queue)
            delays[tuple(m)] = -1
            gainedReward = gainedReward + reward
            

    return numSelections, avgReward, gainedReward, delays, fifo

def optimal(armToChoose, rewardProbabilities, gainedReward, avgReward, numSelections):
    selections  = np.argsort(rewardProbabilities)[-armToChoose:]
    for j in selections:
        reward = sample_arm(rewardProbabilities, j)
        gainedReward = gainedReward + reward
        avgReward[j] = avgReward[j] + (reward)/numSelections[j]
        numSelections[j] = numSelections[j] + 1
    return gainedReward, avgReward, numSelections

def roundRobin(armToChoose, numOfArms, rewardProbabilities, gainedReward, avgReward, numSelections, roundNum):
    selections  = (np.arange(armToChoose) + roundNum % numOfArms) % numOfArms
    for j in selections:
        reward = sample_arm(rewardProbabilities, j)
        gainedReward = gainedReward + reward
        avgReward[j] = avgReward[j] + (reward)/numSelections[j]
        numSelections[j] = numSelections[j] + 1
    return gainedReward, avgReward, numSelections

def roundRobin_delayed(armToChoose, numOfArms, rewardProbabilities, gainedReward, avgReward, numSelections, roundNum, delays, delayTime):
    selections  = (np.arange(armToChoose) + roundNum % numOfArms) % numOfArms
    for j in selections:
        
        loc = np.argwhere(delays[j] == -1)
        loc = loc[0][0]
        delays[j, loc] = delayTime  
        numSelections[j] = numSelections[j] + 1
    
    
    if ((np.size(np.argwhere(delays == 0))) > 0):
        for m in np.argwhere(delays==0):
            reward = sample_arm(rewardProbabilities, m[0])
            delays[tuple(m)] = -1
            gainedReward = gainedReward + reward
            avgReward[j] = avgReward[j] + (reward)/numSelections[j]

    return gainedReward, avgReward, numSelections, delays

class Algos(Enum):
    UCB = 0
    UCB_DELAYED_5 = 1
    UCB_DELAYED_10 = 2
    UCB_DELAYED_20 = 3
    UCB_DELAYED_50 = 4
    TS = 5
    TS_DELAYED_5 = 6
    TS_DELAYED_10 = 7
    OPTIMAL = 8
    ROUND_ROBIN = 9
    ROUND_ROBIN_DELAYED_5 = 10
    UCB_DELAYED_PURE_5 = 11


MAX_DELAY = 10

numOfArms = 100
armToChoose = 3
numOfRounds = 15000

algoNum = len(Algos)
fifoSize = 10
fifo = np.zeros((algoNum, numOfArms, fifoSize))

rewardProbabilities = np.random.uniform(0,0.1,(numOfArms))
rewardProbabilities[0] = 0.9
rewardProbabilities[1] = 0.9
rewardProbabilities[2] = 0.9

avgRewardArray = np.zeros((algoNum, numOfRounds))
numSelections = np.zeros((algoNum, numOfArms))
avgReward = np.zeros((algoNum, numOfArms))
delays = np.zeros((algoNum, numOfArms, MAX_DELAY+60)) -1

gainedReward = np.zeros(algoNum)

alpha = np.ones(numOfArms)
alphad = np.ones(numOfArms)

beta = np.ones(numOfArms)
betad = np.ones(numOfArms)

alphad2 = np.ones(numOfArms)
betad2 = np.ones(numOfArms)

for i in range(1,numOfRounds):
    # UCB
    numSelections[Algos.UCB.value,:],  avgReward[Algos.UCB.value,:], gainedReward[Algos.UCB.value]= ucb(numSelections[Algos.UCB.value, :], avgReward[Algos.UCB.value, :], numOfArms, armToChoose, i, gainedReward[Algos.UCB.value], rewardProbabilities)
    avgRewardArray[Algos.UCB.value,i] = gainedReward[Algos.UCB.value] / i
    # UCB Delayed PURE 5
    numSelections[Algos.UCB_DELAYED_PURE_5.value,:],  avgReward[Algos.UCB_DELAYED_PURE_5.value,:], gainedReward[Algos.UCB_DELAYED_PURE_5.value], delays[Algos.UCB_DELAYED_PURE_5.value,:], fifo[Algos.UCB_DELAYED_PURE_5.value, :, :] = ucb_delayed_pure(numSelections[Algos.UCB_DELAYED_PURE_5.value, :], avgReward[Algos.UCB_DELAYED_PURE_5.value, :], numOfArms, armToChoose, i, gainedReward[Algos.UCB_DELAYED_PURE_5.value], rewardProbabilities, fifo[Algos.UCB_DELAYED_PURE_5.value,:,:], fifoSize, delays[Algos.UCB_DELAYED_PURE_5.value,:], 5)
    avgRewardArray[Algos.UCB_DELAYED_PURE_5.value,i] = gainedReward[Algos.UCB_DELAYED_PURE_5.value] / i
    # UCB Delayed 5
    numSelections[Algos.UCB_DELAYED_5.value,:],  avgReward[Algos.UCB_DELAYED_5.value,:], gainedReward[Algos.UCB_DELAYED_5.value], delays[Algos.UCB_DELAYED_5.value,:], fifo[Algos.UCB_DELAYED_5.value, :, :] = ucb_delayed(numSelections[Algos.UCB_DELAYED_5.value, :], avgReward[Algos.UCB_DELAYED_5.value, :], numOfArms, armToChoose, i, gainedReward[Algos.UCB_DELAYED_5.value], rewardProbabilities, fifo[Algos.UCB_DELAYED_5.value,:,:], fifoSize, delays[Algos.UCB_DELAYED_5.value,:], 5)
    avgRewardArray[Algos.UCB_DELAYED_5.value,i] = gainedReward[Algos.UCB_DELAYED_5.value] / i
    # UCB Delayed 10
    numSelections[Algos.UCB_DELAYED_10.value,:],  avgReward[Algos.UCB_DELAYED_10.value,:], gainedReward[Algos.UCB_DELAYED_10.value], delays[Algos.UCB_DELAYED_10.value,:], fifo[Algos.UCB_DELAYED_10.value, :, :] = ucb_delayed(numSelections[Algos.UCB_DELAYED_10.value, :], avgReward[Algos.UCB_DELAYED_10.value, :], numOfArms, armToChoose, i, gainedReward[Algos.UCB_DELAYED_10.value], rewardProbabilities, fifo[Algos.UCB_DELAYED_10.value,:,:], fifoSize, delays[Algos.UCB_DELAYED_10.value,:], 10)
    avgRewardArray[Algos.UCB_DELAYED_10.value,i] = gainedReward[Algos.UCB_DELAYED_10.value] / i
    # UCB Delayed 20
    numSelections[Algos.UCB_DELAYED_20.value,:],  avgReward[Algos.UCB_DELAYED_20.value,:], gainedReward[Algos.UCB_DELAYED_20.value], delays[Algos.UCB_DELAYED_20.value,:], fifo[Algos.UCB_DELAYED_20.value, :, :] = ucb_delayed(numSelections[Algos.UCB_DELAYED_20.value, :], avgReward[Algos.UCB_DELAYED_20.value, :], numOfArms, armToChoose, i, gainedReward[Algos.UCB_DELAYED_20.value], rewardProbabilities, fifo[Algos.UCB_DELAYED_20.value,:,:], fifoSize, delays[Algos.UCB_DELAYED_20.value,:], 20)
    avgRewardArray[Algos.UCB_DELAYED_20.value,i] = gainedReward[Algos.UCB_DELAYED_20.value] / i
    # UCB Delayed 20
    numSelections[Algos.UCB_DELAYED_50.value,:],  avgReward[Algos.UCB_DELAYED_50.value,:], gainedReward[Algos.UCB_DELAYED_50.value], delays[Algos.UCB_DELAYED_50.value,:], fifo[Algos.UCB_DELAYED_50.value, :, :] = ucb_delayed(numSelections[Algos.UCB_DELAYED_50.value, :], avgReward[Algos.UCB_DELAYED_50.value, :], numOfArms, armToChoose, i, gainedReward[Algos.UCB_DELAYED_50.value], rewardProbabilities, fifo[Algos.UCB_DELAYED_50.value,:,:], fifoSize, delays[Algos.UCB_DELAYED_50.value,:], 50)
    avgRewardArray[Algos.UCB_DELAYED_50.value,i] = gainedReward[Algos.UCB_DELAYED_50.value] / i
    # TS
    alpha, beta, avgReward[Algos.TS.value,:], numSelections[Algos.TS.value,:], gainedReward[Algos.TS.value] = ts(alpha, beta, armToChoose, rewardProbabilities, avgReward[Algos.TS.value,:], numSelections[Algos.TS.value,:], gainedReward[Algos.TS.value])
    avgRewardArray[Algos.TS.value,i] = gainedReward[Algos.TS.value] / i
    # TS Delayed 5
    alphad, betad, numSelections[Algos.TS_DELAYED_5.value,:], avgReward[Algos.TS_DELAYED_5.value,:], gainedReward[Algos.TS_DELAYED_5.value], fifo[Algos.TS_DELAYED_5.value, :, :], delays[Algos.TS_DELAYED_5.value,:] = ts_delayed(alphad, betad, numSelections[Algos.TS_DELAYED_5.value,:], avgReward[Algos.TS_DELAYED_5.value,:], numOfArms, armToChoose, i, gainedReward[Algos.TS_DELAYED_5.value], rewardProbabilities, fifo[Algos.TS_DELAYED_5.value,:,:], fifoSize, delays[Algos.TS_DELAYED_5.value,:], 5)
    avgRewardArray[Algos.TS_DELAYED_5.value,i] = gainedReward[Algos.TS_DELAYED_5.value] / i
    # TS Delayed 10
    alphad2, betad2, numSelections[Algos.TS_DELAYED_10.value,:], avgReward[Algos.TS_DELAYED_10.value,:], gainedReward[Algos.TS_DELAYED_10.value], fifo[Algos.TS_DELAYED_10.value, :, :], delays[Algos.TS_DELAYED_10.value,:] = ts_delayed(alphad2, betad2, numSelections[Algos.TS_DELAYED_10.value,:], avgReward[Algos.TS_DELAYED_10.value,:], numOfArms, armToChoose, i, gainedReward[Algos.TS_DELAYED_10.value], rewardProbabilities, fifo[Algos.TS_DELAYED_10.value,:,:], fifoSize, delays[Algos.TS_DELAYED_10.value,:], 10)
    avgRewardArray[Algos.TS_DELAYED_10.value,i] = gainedReward[Algos.TS_DELAYED_10.value] / i
    # Optimal
    gainedReward[Algos.OPTIMAL.value], avgReward[Algos.OPTIMAL.value,:], numSelections[Algos.OPTIMAL.value,:] = optimal(armToChoose, rewardProbabilities, gainedReward[Algos.OPTIMAL.value], avgReward[Algos.OPTIMAL.value,:], numSelections[Algos.OPTIMAL.value,:])
    avgRewardArray[Algos.OPTIMAL.value,i] = gainedReward[Algos.OPTIMAL.value] / i
    # Round Robin
    gainedReward[Algos.ROUND_ROBIN.value], avgReward[Algos.ROUND_ROBIN.value,:], numSelections[Algos.ROUND_ROBIN.value,:] = roundRobin(armToChoose, numOfArms, rewardProbabilities, gainedReward[Algos.ROUND_ROBIN.value], avgReward[Algos.ROUND_ROBIN.value,:], numSelections[Algos.ROUND_ROBIN.value,:], i)
    avgRewardArray[Algos.ROUND_ROBIN.value,i] = gainedReward[Algos.ROUND_ROBIN.value] / i
    # Round Robin Delayed 5
    gainedReward[Algos.ROUND_ROBIN_DELAYED_5.value], avgReward[Algos.ROUND_ROBIN_DELAYED_5.value,:], numSelections[Algos.ROUND_ROBIN_DELAYED_5.value,:], delays[Algos.ROUND_ROBIN_DELAYED_5.value,:] = roundRobin_delayed(armToChoose, numOfArms, rewardProbabilities, gainedReward[Algos.ROUND_ROBIN_DELAYED_5.value], avgReward[Algos.ROUND_ROBIN_DELAYED_5.value,:], numSelections[Algos.ROUND_ROBIN_DELAYED_5.value,:], i, delays[Algos.ROUND_ROBIN_DELAYED_5.value,:], 10)
    avgRewardArray[Algos.ROUND_ROBIN_DELAYED_5.value,i] = gainedReward[Algos.ROUND_ROBIN_DELAYED_5.value] / i

    idxs = np.argwhere(delays > 0)
    for idx in idxs:
        delays[tuple(idx)] = delays[tuple(idx)] - 1


plt.plot(avgRewardArray[Algos.UCB.value,:], label="PURE UCB without delay")
plt.plot(avgRewardArray[Algos.UCB_DELAYED_5.value,:], label="UCB with reward queue delay = 5")
plt.plot(avgRewardArray[Algos.UCB_DELAYED_10.value,:], label="UCB with reward queue delay = 10")
plt.plot(avgRewardArray[Algos.UCB_DELAYED_20.value,:], label="UCB with reward queue delay = 20")
plt.plot(avgRewardArray[Algos.UCB_DELAYED_50.value,:], label="UCB with reward queue delay = 50")
plt.plot(avgRewardArray[Algos.UCB_DELAYED_PURE_5.value,:], label="PURE Delayed UCB delay = 5")
plt.plot(avgRewardArray[Algos.TS.value,:], label="PURE TS without delay")
plt.plot(avgRewardArray[Algos.TS_DELAYED_5.value,:], label="TS with reward queue d = 5")
plt.plot(avgRewardArray[Algos.TS_DELAYED_10.value,:], label="TS with reward queue d = 10")
plt.plot(avgRewardArray[Algos.OPTIMAL.value,:], label="Optimal")
plt.plot(avgRewardArray[Algos.ROUND_ROBIN.value,:], label="Round Robin without delay")
plt.plot(avgRewardArray[Algos.ROUND_ROBIN_DELAYED_5.value,:], label="Delayed Round Robin, d = 5")

plt.title("Average Reward vs Rounds [N = 100, K = 3]")
plt.xlabel("Rounds")
plt.ylabel("Average Reward")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()