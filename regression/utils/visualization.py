import matplotlib.pyplot as plt
import numpy as np
import math

def weight_histogram(coefficient, name, mode='normal', title='Feature'):
    coefficient = coefficient.copy()
    name = name.copy()

    if mode == 'cleanup': # remove zero coefficients
        new_coeff = []
        new_name = []
        for idx in range(len(coefficient)):
            if math.fabs(coefficient[idx]) > 1e-3:
                new_coeff.append(coefficient[idx])
                new_name.append(name[idx])

        coefficient = new_coeff
        name = new_name
    N = len(name)
    index = np.arange(N)
    width = 0.3
    plt.bar(index, coefficient, width, label="value", color="#87CEFA")
    plt.xlabel('Features')
    plt.ylabel('Weight')
    plt.title(title)
    plt.xticks(index, name)
    plt.legend(loc="upper right")
    #If average length of xtick label is greater than 3, rotate 45 degree
    if np.mean([len(str) for str in name]) > 3:
        plt.xticks(rotation=90)
    #decrease xtick label font size
    plt.tick_params(axis='x', which='major', labelsize=6)
    
    plt.tight_layout() 
    plt.show()
    return coefficient, name
