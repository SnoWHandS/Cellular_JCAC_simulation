#The following python 3 code is used to simulate the blocking and dropping states of a 2 RAT heterogeneous network
#The states are determined for each new call and handover call arrival rate and the relevant probabilities are calculated.
#Author: Dillon Heald
#Date: 30 May 2020

import math

#This is the main function which takes in a network configuration and call rate value and determines the dropping and blocking probabilities
def calc_probs(t1,t2,c1,c2,bbu,callRate,departRate):
    #Create and instantiate call variables
    n1 = 0  #New calls for RAT1
    n2 = 0  #New calls for RAT2
    h1 = 0  #Handover calls for RAT1
    h2 = 0  #Handover calls for RAT2

    #Create and instantiate states counters
    blocked_1 = 0   #Count for blocked calls of RAT1
    dropped_1 = 0   #Count for dropped calls of RAT1
    blocked_2 = 0   #Count for blocked calls of RAT2
    dropped_2 = 0   #Count for dropped calls of RAT2

    #Create probability variables
    blocking_prob_1 = 0
    dropping_prob_1 = 0
    blocking_prob_2 = 0
    dropping_prob_2 = 0

    normalization_factor = 0     #G
    total_prob = 0              #P(s)

    #Split call rate into new calls and handover calls
    new_split = 0.4                         #40% new
    handovr_split = 1-new_split             #60% handover
    new_calls = (callRate/departRate)*new_split
    handovr_calls = (callRate/departRate)*handovr_split

    #New calls incremented until reached threshhold for RAT1
    for n1 in range(0,t1):       #might need to be t1+1
        #Handover calls incremeted until reached capacity for RAT1
        for h1 in range(0,c1):
            #New calls incremented until reached threshhold for RAT2
            for n2 in range(0,t2):       #might need to be t2+1
                #Handover calls incremeted until reached capacity for RAT2
                for h2 in range(0,c2):
                    #Define the admissible states
                    adm_states = (((n1+h1)*bbu <= c1) and (n1*bbu <= t1)   and   ((n2+h2)*bbu <= c2) and (n2*bbu <= t2))
                    #Define the dropping state
                    drop_state_1 = ((bbu+bbu*(n1+h1) > c1))
                    drop_state_2 = ((bbu+bbu*(n1+h1) > c1) and (bbu+bbu*(n2+h2) > c2))        #could be done with bbu(1+(n1+h1)...)
                    #Define the blocking state
                    block_state_1 = ((bbu+bbu*(n1+h1) > t1))
                    block_state_2 = ((bbu+bbu*(n1+h1) > t1) and (bbu+bbu*(n2+h2) > t2))        #could be done with bbu(1+(n1+h1)...)

                    #Check if the admissible states is valid
                    if(adm_states):
                        PhPn = (new_calls**(n1+n2))*(handovr_calls**(h1+h2))    #calculate numberator (Pn^n * Ph^h)
                        #Create the denomenator
                        h_fac_n_fac = (math.factorial(n1))*(math.factorial(n2))*(math.factorial(h1))*(math.factorial(h2))
                        total_prob = PhPn/h_fac_n_fac       #calculate total probability

                        normalization_factor = normalization_factor + total_prob    #calcualte G

                        #Check for blocking state on RAT1
                        if(block_state_1):
                            blocked_1 += 1
                            blocking_prob_1 += total_prob
                        #Check for blocking state on RAT2
                        if(block_state_2):
                            blocked_2 += 1
                            blocking_prob_2 += total_prob

                        #Check for dropping state on RAT1
                        if(drop_state_1):
                            dropped_1 += 1
                            dropping_prob_1 += total_prob
                        #Check for dropping state on RAT2
                        if(drop_state_2):
                            dropped_2 += 1
                            dropping_prob_2 += total_prob
    
    #End of all for loops
    #normalize probabilities
    blocking_prob_1 = blocking_prob_1/normalization_factor
    blocking_prob_2 = blocking_prob_2/normalization_factor
    dropping_prob_1 = dropping_prob_1/normalization_factor
    dropping_prob_2 = dropping_prob_2/normalization_factor

    return blocking_prob_1, blocking_prob_2, dropping_prob_1, dropping_prob_2


def test_call_arrival_rate():
    #create heterogeneous network and calculate probabilities for increasing call (arrival) rates
    c1 = c2 = 20
    t1 = t2 = 10
    bbu = 1
    maxCalls = 35
    depart = 1
    file = open("./Output/CallArrivalprobabilites.csv", "w")
    file.write("Call Arrival Rate, Group 1 Calls Blocked,Group 2 Calls Blocked,Group 1 Calls Dropped,Group 2 Calls Dropped\n")

    for calls in range(1,maxCalls):
        #calculate the probabilities
        (probBlock1, probBlock2, probDrop1, probDrop2) = calc_probs(t1,t2,c1,c2,bbu,calls,depart)
        #write to csv file
        file.write(str(calls) + "," + str(probBlock1) + "," + str(probBlock2) + "," + str(probDrop1) + "," + str(probDrop2) + "\n")

def test_call_departure_rate():
    #create heterogeneous network and calculate probabilities for increasing call (depart) rates
    c1 = c2 = 15
    t1 = t2 = 10
    bbu = 1
    callArrivalRate = 35
    maxDepart = 15
    file = open("./Output/CallDepartprobabilites.csv", "w")
    file.write("Call Departure Rate, Group 1 Calls Blocked,Group 2 Calls Blocked,Group 1 Calls Dropped,Group 2 Calls Dropped\n")

    for depart in range(1,maxDepart):
        #calculate the probabilities
        (probBlock1, probBlock2, probDrop1, probDrop2) = calc_probs(t1,t2,c1,c2,bbu,callArrivalRate,depart)
        #write to csv file
        file.write(str(depart) + "," + str(probBlock1) + "," + str(probBlock2) + "," + str(probDrop1) + "," + str(probDrop2) + "\n")


def test_increasing_capacity():
    #same as call arrival rate test but with capacity changing
    maxCapacity = 71
    t1 = t2 = 10
    bbu = 1
    callArrivalRate = 10    #locked this to 10 calls
    depart = 1
    file = open("./Output/Capacityprobabilites.csv", "w")
    file.write("Capacity, Group 1 Calls Blocked,Group 2 Calls Blocked,Group 1 Calls Dropped,Group 2 Calls Dropped\n")

    for c in range(1,maxCapacity):
        #calculate the probabilities
        (probBlock1, probBlock2, probDrop1, probDrop2) = calc_probs(t1,t2,c,c,bbu,callArrivalRate,depart)
        #write to csv file
        file.write(str(c) + "," + str(probBlock1) + "," + str(probBlock2) + "," + str(probDrop1) + "," + str(probDrop2) + "\n")

def test_increasing_threshold():
    #same as call arrival rate test but with threshold changing
    c1 = c2 = 20
    maxThreshold = c1       #set the threshold as sa % of the maximum capacity
    bbu = 1
    callArrivalRate = 10    #locked this to 10 calls - made most interesting calls blocked curve
    depart = 1
    file = open("./Output/Thresholdprobabilites.csv", "w")
    file.write("Threshold, % of Capacity , Group 1 Calls Blocked,Group 2 Calls Blocked,Group 1 Calls Dropped,Group 2 Calls Dropped\n")

    for t in range(1,maxThreshold+1):
        #calculate the probabilities
        (probBlock1, probBlock2, probDrop1, probDrop2) = calc_probs(t,t,c1,c2,bbu,callArrivalRate,depart)
        #write to csv file
        file.write(str(t) + "," + str((float(t)/float(c1))*100) + "," + str(probBlock1) + "," + str(probBlock2) + "," + str(probDrop1) + "," + str(probDrop2) + "\n")

def test_increasing_baseBandwidth():
    #same as call arrival rate test but with threshold changing
    c1 = c2 = 20
    t1 = t2 = 10       
    maxBbu = 80                 #set max bandwidth
    callArrivalRate = 10    #locked this to 10 calls
    depart = 1
    file = open("./Output/BBUprobabilites.csv", "w")
    file.write("Base Bandwidth Unit (bbu) , Group 1 Calls Blocked,Group 2 Calls Blocked,Group 1 Calls Dropped,Group 2 Calls Dropped\n")

    for bbu in range(1,maxBbu+1):
        #calculate the probabilities
        halfbbu=float(bbu)/5
        (probBlock1, probBlock2, probDrop1, probDrop2) = calc_probs(t1,t2,c1,c2,halfbbu,callArrivalRate,depart)
        #write to csv file
        file.write(str(halfbbu) + "," + str(probBlock1) + "," + str(probBlock2) + "," + str(probDrop1) + "," + str(probDrop2) + "\n")



#Execute all the tests
test_call_arrival_rate()
test_increasing_capacity()
test_increasing_threshold()
test_call_departure_rate()
test_increasing_baseBandwidth()
