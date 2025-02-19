import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

output = pd.DataFrame(columns=["Usable Space", "$ per Usable Sqr Ft", "Occupancy"])

for i in range(1000):
    usable_space = np.random.normal(loc=70, scale=10)
    usable_space = np.clip(usable_space, 50, 90)

    cost_per_sqr_ft = 100 - (usable_space * 1.2) + np.random.normal(0, 10)
    cost_per_sqr_ft = np.clip(cost_per_sqr_ft, 10, 50)

    occupancy = (120 - cost_per_sqr_ft) * (usable_space / 100) * np.random.uniform(5, 15)
    occupancy += np.random.normal(0, 200)
    occupancy = np.clip(occupancy, 100, 8000)

    output.loc[i] = [usable_space, cost_per_sqr_ft, occupancy]

print(output)

x = output["Occupancy"]
y = output["Usable Space"]
z = output["$ per Usable Sqr Ft"]

grid_x, grid_y = np.meshgrid(
    np.linspace(x.min(), x.max(), 50),
    np.linspace(y.min(), y.max(), 50)
)

grid_z = griddata((x, y), z, (grid_x, grid_y), method='linear')

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

ax.set_box_aspect([2, 2, 1])

ax.set_xlim(x.min(), x.max())
ax.set_ylim(y.min(), y.max())
ax.set_zlim(z.min(), z.max())

ax.plot_surface(grid_x, grid_y, grid_z, cmap='viridis', edgecolor='k', alpha=0.8)

ax.set_xlabel("Occupancy")  
ax.set_ylabel("Usable Space")  
ax.set_zlabel("$ per Usable Sqr Ft")  
ax.set_title("3D Surface Plot of Space, Cost, and Occupancy")

plt.show()