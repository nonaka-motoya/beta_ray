from betaDecay import betaDecay

bd = betaDecay(dirName='2022_4_18', numFile=9999)

# bd.plotRawData('texio/wfm_0.txt')
# bd.calcAreaDistribution()
bd.plotDistribution(isLog=True)
# bd.calibration()
# bd.plotEnergyDistribution(500, 0, 3)