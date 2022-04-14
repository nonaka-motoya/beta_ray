import numpy as np
import matplotlib.pyplot as plt

def main():
    num_file = 2502
    f = open('output/area.txt', 'w')
    
    
    for i in range(num_file):
        filename = 'texio/wfm_' + str(i+1) + '.txt'
        t, V = load_data(filename)
        area = calc_area(t, V)
        f.write(str(area))
        f.write('\n')
        
    
    
    
    
def load_data(filename):
    data = np.loadtxt(filename)
    t = data[:, 0]
    V = data[:, 1]
    return t, V

def plot_data():
    t, V = load_data('texio/wfm_0.txt')

    plt.figure()
    plt.scatter(t, V, s=1)
    plt.show()
    
def calc_area(t, V):
    # t, V = load_data('texio/wfm_0.txt')
    data_length = t.size
    delta_t = (t.max() - t.min()) / data_length
    
    total_area = 0
    for i in range(data_length):
        if V[i] < -50:
            total_area += V[i] * delta_t
            
    return -total_area
    
    
if __name__ == '__main__':
    main()