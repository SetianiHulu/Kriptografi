import matplotlib.pyplot as plt
import numpy as np

# Generate random data
x = np.random.randint(1, 11, 20)
y = np.random.randint(1, 11, 20)

# Create scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(x, y)
plt.title('Random Data Scatter Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid(True)
plt.show()
