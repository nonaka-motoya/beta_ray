import numpy as np
import matplotlib.pyplot as plt
    
class betaDecay():
    """
    オシロスコープの波形データからベータ線のエネルギー分布を作成する
    
    Attributes
    ------------
    dirName: str
        データのあるディレクトリ
    
    numFile: int
        読み込むファイルの数
    """
    
    def __init__(self, dirName, numFile):
        self.dirName = dirName
        self.numFile = numFile
        
    
    def load_data(self, filename):
        """
        オシロスコープの波形データを読み込む．
        
        Parameters
        ----------
        filename: str
            読み込むファイルの名前
            
        Returns
        ----------
        t: ndarray
            時間
        V: ndarray
            電圧
        """
        data = np.loadtxt(filename) # テキストファイルの読み込み

        t = data[:, 0] # データの１列目を抽出
        V = data[:, 1] # データの２列目を抽出
        return t, V
    
    
    
    def calcArea(self, t, V):
        """
        面積を計算する．
        
        Parameters
        ----------
        t: ndarray
            時間
        V: ndarray
            電圧
        
        Returns
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
    
    
    
    def calcAreaDistribution(self):
        """
        波形の面積を計算する
        出力は'output/area.txt'にされる
        """
        
        f = open('output/area.txt', 'w') # 出力結果を書き込むファイル
        
        for i in range(self.numFile):
            filename =  self.dirName + '/wfm_' + str(i+1) + '.txt' # ファイル名
            t, V = self.load_data(filename) # テキストファイルを読み込んでtとVを抽出
            area = self.calcArea(t, V) # 波形の面積を計算
            f.write(str(area))
            f.write('\n')
            
        return
    
    
    
    def calibration(self):
        """
        キャリブレーションをする
        作成中
        """
        
        f = open('output/energy.txt', 'w')
        
        area = np.loadtxt('output/area.txt')
        ratio = 2.28 / 200
        energy = area * ratio
        
        for i in range(energy.size):
            f.write(str(energy[i]))
            f.write('\n')
            
        return
    
            
    
    def plotDistribution(self, isLog=False, binNum=500, binMin=None, binMax=None):
        """
        面積のデータをテキストファイルから読み込みヒストグラムを作成する．
        
        Parameters
        ----------
        isLog: bool
            y軸をログスケールで出力したい場合はTrueにする
        binNum: int
            ビンの数
        binMin: double
            最小値
        binMax: double
            最大値
        """
        area = np.loadtxt('output/area.txt')
        
        if not binMin:
            binMin = area.min()
        
        if not binMax:
            binMax = area.max()

        plt.figure()
        plt.hist(area, bins=binNum)
        plt.xlim(binMin, binMax)
        plt.xlabel(r'area (mV $\cdot$  ns)')
        plt.ylabel('count')
        
        if isLog:
            plt.yscale('log')
        
        plt.show()
        
        
        
    def plotEnergyDistribution(self, binNum=500, binMin=None, binMax=None):
        energy = np.loadtxt('output/energy.txt')
        
        if not binMin:
            binMin = energy.min() - 0.5
        
        if not binMax:
            binMax = energy.max() + 0.5

        plt.figure()
        plt.hist(energy, bins=binNum)
        plt.xlim(binMin, binMax)
        plt.xlabel(r'energy (MeV)')
        plt.ylabel('count')
        plt.show()
        
        
        
    def plotRawData(self, filename):
        """
        生データを描画する
        
        Parameters
        ----------
        filename: str
            生データのパス
        """
        t, V = self.load_data(filename)

        plt.figure()
        plt.scatter(t, V, s=1)

        plt.xlabel(r'$t$ (ns)')
        plt.ylabel(r'$V$ (mV)')

        plt.show()