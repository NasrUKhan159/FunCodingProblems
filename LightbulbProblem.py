# Problem description: There are 100 lightbulbs - you start by switching all of them on in the first pass. In the next
# pass, you press every second switch. In the third pass, you press every third switch and so on until you reach the
# 100th pass. On the 100th pass, how many switches are on?

import numpy as np

def update_list(list_pass, pass_no):
    for i, element in enumerate(list_pass):
        if ((i+1) % pass_no) == 0:
            if element == 1:
                list_pass[i] = 0
            else:
                list_pass[i] = 1
    return list_pass

def run(list_pass):
    passes = np.arange(2,101,1)
    for pass_no in passes:
        list_pass = update_list(list_pass, pass_no)
    return list_pass

def find_number_lightbulbs_on_by_end(list_pass):
    for i, element in enumerate(list_pass):
        if i % 2:
            if element == 1:
                element = 0
            else:
                element = 1
    for i, element in enumerate(list_pass):
        if i % 3:
            if element == 1:
                element = 0
            else:
                element = 1

if __name__ == "__main__":
    list_pass = np.ones(100)
    list_pass = run(list_pass)
    print(2)