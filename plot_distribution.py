from betaDecay import betaDecay

dirName = '20220421'

bd = betaDecay(dirName=dirName)

bd.plotRawData(dirName + '/wfm_2.txt')
bd.calcAreaDistribution()
bd.plotDistribution(isLog=False,binNum=70)
bd.calibration(Qarea=17500, Qenergy=2.28)
bd.plotEnergyDistribution(isLog=False, binNum=70, binMin=0, binMax=3)