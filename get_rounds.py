from get_longest_clips import get_longest_clips
from get_clips_x_y import read_clips_x_y
import argparse
import numpy as np
import pandas as pd
import os 

def get_rounds_1(x_ys):
    """
    Parameters: 
    ignore the 0 vlaue 
    x_ys(dict): dict contain df for longest clips
    """
    frame = 2
    min_diff = 40
    max_diff = 300

    for clip_name, x_y in x_ys.items():

        y_values = x_y['Y'].tolist()

        y_not_zero_values = [y for y in y_values if y != 0.0]
        print(y_not_zero_values)
        valid_y = []


        for index in range(len(y_not_zero_values)-frame-1):
            diffs = []
            for i in range(frame):
                diffs.append(abs(y_not_zero_values[index + i + 1] - y_not_zero_values[index + i]))
                
            valid = True
            for diff in diffs:
                if (diff > max_diff):
                    valid = False
                    break

            if valid == True:
                valid_y.append(y_not_zero_values[index])


        count = 0
        i = 1
        n = len(valid_y)

        print(valid_y)

        # Loop through the array to find increasing then decreasing sequences
        while i < n - 1:
            # Find the increasing sequence
            while i < n and valid_y[i] > valid_y[i - 1]:
                i += 1
            count += 1

            # Check for a peak (increasing then decreasing)
            while i < n and valid_y[i] < valid_y[i - 1]:
                i += 1
            count += 1
     
        print(clip_name)
        print(count)


def get_rounds(x_ys):
    """
    Parameters: 
    x_ys(dict): dict contain df for longest clips
    """
    frame = 3
    min_diff = 5
    max_diff = 150

    rounds = []

    for clip_name, x_y in x_ys.items():

        y_values = x_y['Y'].tolist()

        #print(y_values)
        valid_y = []


        for index in range(len(y_values)-frame-1):
            diffs = []
            for i in range(frame):
                diffs.append(abs(y_values[index + i + 1] - y_values[index + i]))
                
            valid = True
            for diff in diffs:
                if (diff < min_diff or diff > max_diff):
                    valid = False
                    break

            if valid == True:
                valid_y.append(y_values[index])


        count = 0
        i = 1
        n = len(valid_y)

        #print(valid_y)

        # Loop through the array to find increasing then decreasing sequences
        while i < n - 1:
            # Find the increasing sequence
            while i < n and valid_y[i] > valid_y[i - 1]:
                i += 1
            # Check for a peak (increasing then decreasing)
            if i < n and valid_y[i] < valid_y[i - 1]:
                count += 1
                # Find the decreasing sequence
                while i < n and valid_y[i] < valid_y[i - 1]:
                    i += 1
            else:
                i += 1
        print(clip_name)
        if count == 0:
            count += 1 
        print(count)
        rounds.append(count)

    return rounds


def get_rounds_of_longest_clips(path, longest_coefficent=0.2, time_file_postfix = ".txt", x_y_file_posfix = "_tracknet.txt"):
    """
    handler all the problem of paths. when call other help function,need to pass in entire pass
    Parameters:
    path (float): path to the game folder which contain the x_y datas and start,end time of clips.
    longest_coefficent(float): the most coefficent of clips want to get.
    time_file_postfix(string):
    """

    # generate the path to x_y file and start,end files
    # the file name prefix : 2024-05-21_21-27-54_the_43_court_2877
    _, last_folder_name = os.path.split(path)
    time_file = path + '/' + last_folder_name + time_file_postfix
    x_y_file = path + '/' + last_folder_name +  x_y_file_posfix

    longest_clips = get_longest_clips(time_file,longest_coefficent)
    x_ys = read_clips_x_y(longest_clips,x_y_file)



    rounds = get_rounds(x_ys)
   

    scores = []
    for index,clip in enumerate(longest_clips):
        scores.append(clip[3]/rounds[index])
        clip.append(scores[index])

    for longest_clip in longest_clips:
        print(longest_clip)
    



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="calculate the rounds number of every clips inside a game")
    parser.add_argument("path", type=str, help="path to where the video and relative data are stored")
    parser.add_argument("longest_coefficent", type=float, help="proportion of longests clips will be used to calculate rounds")
    parser.add_argument("time_file_postfix", type=str, help = "postfix")
    parser.add_argument("x_y_file_posfix", type=str, help = "postfix")
    args = parser.parse_args()
   
    path = args.path
    longest_coefficent = args.longest_coefficent
    time_file_postfix = args.time_file_postfix
    x_y_file_posfix = args.x_y_file_posfix

    get_rounds_of_longest_clips(path, longest_coefficent, time_file_postfix, x_y_file_posfix)









