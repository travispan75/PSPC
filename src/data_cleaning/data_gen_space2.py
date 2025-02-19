import numpy as np
import pandas as pd

# building_occupancy = [500, 1500, 200, 200, 100, 150, 800]
building_occupancy = [5, 4, 3, 2]

output = pd.DataFrame(columns=[i for i in range(len(building_occupancy))])

stack = [0] * len(building_occupancy)
index = 0
curr_sum = 0

while index < len(stack):
    if curr_sum >= 5:
        output.loc[len(output)] = stack
    if stack[index] < building_occupancy[index]:
        curr_sum -= stack[index]
        stack[index] += 1
        curr_sum += stack[index]
        index = 0
    else:
        curr_sum -= building_occupancy[index]
        stack[index] = 0
        index += 1

print(output)
    