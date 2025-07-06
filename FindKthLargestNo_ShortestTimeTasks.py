# https://daily.dev/blog/fun-coding-problems-from-easy-to-hard
# 1. Find Kth largest element: imagine you have a list of numbers all mixed up, and you need to find the kth biggest no
# number in it.
# 2. Shortest remaining time first scheduling: Suppose you have info on when each task arrives and how long each task
# needs to be done. Keep tasks in order of how much time they need to finish. Pick task with least time left when
# computer is free. If more important task comes in, switch to it. Make wait time and total time for tasks as short as
# possible

import numpy as np
from random import randrange
import datetime
import pandas as pd


def find_kth_biggest(k: int, M: int, N: int):
    """
    :param k: kth largest no
    :param M: (M-1) = largest posible number in list
    :param N: Number of elements in list
    :return:
    """
    rng = np.random.default_rng(23456)
    arbitrary_list = np.random.randint(M, size=N).tolist()
    max = sorted(set(arbitrary_list))[-k]
    print(f"Problem 1 solution: {max} for k = {k} with a list having {N} numbers where largest possible number is {M-1}")

def random_date(start,l):
    current = start
    while l >= 0:
        curr = current + datetime.timedelta(minutes=randrange(60))
        yield curr
        l-=1

def run_shortest_time(date_list: np.ndarray):
    data = {}
    data['Start_time_task'] = date_list
    # Importance of tasks can range from 0 to 10 where importance measured as integer.
    # For first implementation, assume that importance of task = time it takes to do task. so importance = 0 means it
    # takes less than a minute to do task. importance = 10 means it takes more than 9 minutes and less than or equal to
    # 10 minutes to do task. Simple implementation.
    data['Importance_Task'] = np.random.randint(10, size=len(date_list)).tolist()
    df = pd.DataFrame.from_dict(data)
    df = df.sort_values(by=['Start_time_task'])
    df = df.reset_index(drop=True)
    df['End_time_task'] = pd.to_datetime(df['Start_time_task']) + pd.to_timedelta(df['Importance_Task'], unit="m")
    df_updated = df.copy()
    for i, row in df_updated.iterrows():
        if i != len(df_updated) - 1:
            # cannot change start time of first task because that is the first task!
            # update start time based on end of the previous task because we can only do one task at a time!
            # we will also need to update the end time of the next task in this case too. this works!
            if df.loc[i, 'End_time_task'] > df.loc[i+1, 'Start_time_task']:
                df_updated.loc[i+1, 'Start_time_task'] = df_updated.loc[i, 'End_time_task']
                df_updated.loc[i+1, 'End_time_task'] = pd.to_datetime(df_updated.loc[i+1, 'Start_time_task']) + \
                                                     pd.to_timedelta(df_updated.loc[i+1, 'Importance_Task'], unit="m")
    return df


if __name__ == "__main__":
    # Problem 1 solution
    k = 3
    N = 50
    M = 50
    find_kth_biggest(k, M, N)
    # Problem 2 solution
    N_TASKS = 10
    start_date = datetime.datetime(2025, 7, 6, 13, 0)
    date_list = np.array(list(random_date(start_date, N_TASKS)))
    ordered_set_of_tasks_w_exptime = run_shortest_time(date_list)
    print(f"Problem 2: Tasks came in at {date_list[0]}, we finished at {ordered_set_of_tasks_w_exptime.iloc[-1]['End_time_task']}"
          f" and completed {len(ordered_set_of_tasks_w_exptime)} tasks!")