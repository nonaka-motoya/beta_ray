from betaDecay import betaDecay

dirName = 'data/20220427'

bd = betaDecay(dirName=dirName)

# bd.plotRawData(dirName + '/wfm_2.txt')
# bd.calcAreaDistribution()
bd.plotDistribution(isLog=False,binNum=100)
bd.calibration(Qarea=17500, Qenergy=2.28)
bd.plotEnergyDistribution(isLog=False, binNum=70)
