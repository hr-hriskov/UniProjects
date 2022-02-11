import matplotlib.pyplot as plt
import numpy as np
from module1 import to_evenrows_list

# Leckrate R
R = 3.06304 * 10 ** -4
# R = 3.9596 * 10 ** -4

# End value
ev = 1*10**-2

# Second end value
ev5 = 5*10**-2

# Third end value
ev3 = 5*10**-3

def plot_function(
    x,
    y1,
    y2,
    null_point,
    g2_null_point_value,
    start_lim,
    end_lim,
    diff,
    m_pos,
    T
    ):
    
    # Calculates new x-axis
    x = x - null_point
    
    # Calculates Gauge 2 corrected
    y2_c = y2 - g2_null_point_value - x*R
    [y2, y2_c] = to_evenrows_list(y2, y2_c)
    
    # Finds where 'Gauge 2 corrected' crosses 1^10-2 Pa
    t = np.argmax((y2_c.astype(float) > ev) & (x >= 0))
    
    # Finds where 'Gauge 2 corrected' crosses 5^10-2 Pa
    t5 = np.argmax((y2_c.astype(float) > ev5) & (x >= 0))
    
    # Finds where 'Gauge 2 corrected' crosses 5^10-3 Pa
    t3 = np.argmax((y2_c.astype(float) > ev3) & (x >= 0))
    
    # plt.clf()
    plt.figure(figsize = (8,5))
    plt.scatter(x, y1, s=50, color='red', alpha=0.5, label="Gauge 1")
    plt.scatter(x, y2, s=50, color='blue', alpha=0.5, label="Gauge 2")
    plt.scatter(x, y2_c, s=50, color='green', alpha=0.5, label="Gauge 2 corrected")
    plt.scatter(x.iloc[t3], y2_c.iloc[t3], s=50, color='brown', alpha=1, label="Point 1 (%is)" %x.iloc[t3])
    plt.scatter(x.iloc[t], y2_c.iloc[t], s=50, color='yellow', alpha=1, label="Point 2 (%is)" %x.iloc[t])
    plt.scatter(x.iloc[t5], y2_c.iloc[t5], s=50, color='orange', alpha=1, label="Point 3 (%is)" %x.iloc[t5])
    
#     plt.plot([], [], color = 'purple', label="Differenz = %.6f" %diff)

    plt.title('[%i] Messung bei %i°C' % (m_pos, T), size=15)
    plt.xlabel("Zeit [s]", size=15)
    plt.ylabel("Druck [Pa]", size=15)
    plt.xlim(start_lim, end_lim)
    plt.ylim(1*10**-4, 10)
    plt.yscale("log")
    plt.legend()
    plt.grid(True)

    return int(x.iloc[t3]), int(x.iloc[t]), int(x.iloc[t5])