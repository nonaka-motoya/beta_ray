# 必要なライブラリをインストール

```shell
$ pip install -r requirements.txt
```

# 使い方

## 面積の分布を表示する

betaDecay.pyからbetaDecayクラスをインポートする。
```python:
from betaDecay import betaDecay
```
インスタンスを作成する際に，引数としてdirNameにデータのあるディレクトリ，numFileにデータの数を渡す。
```python
bd = betaDecay(dirName='texio')
```

波形のグラフを出力したい場合はplotRawDataを使う。その際にファイルのパスを渡す。
```python
bd.plotRawData('texio/wfm_0.txt')
```

面積を計算するためにcalcAreaDistributionを呼び出す。その後plotDistributionを呼べばグラフが表示される。
```python
bd.calcAreaDistribution()
bd.plotDistribution()
```

plotDistributionに引数を与えればグラフのビン，描画範囲，y軸のログスケールを変更できる。

```python
bd.plotDistribution(isLog=True, binNum=500, binMin=0, binMax=300)
```

## キャリブレーションをしてエネルギー分布を出す
Q値における面積とエネルギーを指定してキャリブレーションをする。結果はテキストファイルに出力される。

```python
bd.calibration(Qarea=17500, Qenergy=2.28)
```

その後，エネルギー分布をプロットできる。

```python
bd.plotEnergyDistribution(isLog=False, binNum=70, binMin=0, binMax=3)
```