from typing import List
from collections import defaultdict

def get_input() -> defaultdict[int]:
    """
    Generates a defaultdict where the key is the day in the lanternfish's life, 
    and the value is the number of lanternfish in that stage. All lanternfish in stage 0 
    gives birth to a new lanternfish (in stage 8) and returns to stage 6. All other lanternfish 
    continue to progress through stages in decreasing order.

    Returns:
        defaultdict[int]: A dictionary containing the number of lanternfish in each stage of its life
    """
    stage_dict = defaultdict(int)

    # Pre-populate all the stages with an initial value of 0
    stage_dict[8] = 0

    for num in open("Day_06_input.txt").readline().split(","):
        stage_dict[int(num)] += 1

    return stage_dict

def progress_variable_days(stage_dict: defaultdict[int], days: int) -> int:
    """
    Given a dictionary representing the state of the lanternfish population, 
    predicts the population of lanternfish in the given number of days

    Args:
        stage_dict (defaultdict[int]): 
            The state of the current lanternfish population, with the keys being stages 
            in its life and the values being the number of lanternfish in that stage currently
        days (int): The number of days to simulate for

    Returns:
        int: The final number of lanternfish
    """

    # Establish the max stage. All lanternfish are birthed into the max stage and live through the remaining stages in decreasing order
    max_stage = max(stage_dict.keys())
    
    for day in range (0, days):
        # Take the number of new fish into a temporary variable
        new_fish = stage_dict[0]
        for stage in range(0, max_stage):
            stage_dict[stage] = stage_dict[stage + 1]
        
        # All new fish are birthed into the max stage (which is 8). The fish that are in stage 0 and have already given birth are added back into stage 6
        stage_dict[max_stage] = new_fish
        stage_dict[max_stage - 2] += new_fish

    return sum(stage_dict.values())

def main():
    stage_dict = get_input()
    print ("Answer to part 1:", progress_variable_days(stage_dict=stage_dict, days=80))

    stage_dict = get_input()
    print ("Answer to part 2:", progress_variable_days(stage_dict=stage_dict, days=256))
    

if (__name__ == "__main__"):
    main()