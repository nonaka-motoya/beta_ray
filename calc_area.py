import numpy as np
import matplotlib.pyplot as plt

def main():
    num_file = 2502 # ファイルの数
    f = open('output/area.txt', 'w') # 出力結果を書き込むファイル
    
    
    for i in range(num_file):
        filename = 'texio/wfm_' + str(i+1) + '.txt' # ファイル名
        t, V = load_data(filename) # テキストファイルを読み込んでtとVを抽出
        area = calc_area(t, V) # 波形の面積を計算
        print(type(area))
        # 計算した面積をテキストファイルに出力
        f.write(str(area))
        f.write('\n')
        
    # 面積の分布を出力
    plot_data()
    return
    
    

def load_data(filename):
    """
    オシロスコープの波形データを読み込む．
    
    parameters
    ----------
    filename: str
        読み込むファイルの名前
        
    returns
    ----------
    t: ndarray
        時間
    V: ndarray
        電圧
    """
    data = np.loadtxt(filename) # テキストファイルの読み込み

    # tとVの出力
    # print(t, V)

    t = data[:, 0] # データの１列目を抽出
    V = data[:, 1] # データの２列目を抽出
    return t, V
    
def calc_area(t, V):
    """
    面積を計算する．
    
    parameters
    ----------
    t: ndarray
        時間
    V: ndarray
        電圧
    
    returns
    ----------
    -total_area: numpy.float64
        面積にマイナスをかけたものを出力
        
        
    notes
    ----------
    電圧が-50を下回った領域のみの面積を計算している
    """
    data_length = t.size # データの長さ
    delta_t = (t.max() - t.min()) / data_length # Δtの計算
    
    total_area = 0 # 面積
    for i in range(data_length):
        if V[i] < -50: # Vが-50より小さい時だけ計算
            total_area += V[i] * delta_t # ΔS = V * Δt
            
    return -total_area

def plot_data():
    """
    面積のデータをテキストファイルから読み込みヒストグラムを作成する．
    """
    area = np.loadtxt('output/area.txt')

    plt.figure()
    plt.hist(area, bins=500)
    plt.xlim(area.min(), area.max())
    plt.xlabel('area')
    plt.ylabel('count')
    plt.show()
    
    
if __name__ == '__main__':
    main()