from src.DataReader.VODataSet import VODataSetManager_CNN
from src.Models.Model_CNN_0 import Model_CNN_0
from src.Models.ModelContainer_CNN import ModelContainer_CNN
import numpy as np
import time
from src.git_branch_param import *
from src.Params import getNoiseLevel

def train(dsName, subType, seq):
    wName = '../Weights/' + branchName() + '_' + dsName + '_' + subType
    dm = VODataSetManager_CNN(dsName=dsName, subType=subType, seq=seq, isTrain=True, split=0.2)
    train, val = dm.trainSet, dm.valSet
    mc = ModelContainer_CNN(Model_CNN_0(dsName))
    #mc.load_weights(wName, train=True)
    mc.fit(train, val, batch_size=64, epochs=20, wName=wName, checkPointFreq=1)

def test(dsName, subType, seqRange):
    wName = '../Weights/' + branchName() + '_' + dsName + '_' + subType
    resName = '../Results/Data/' + branchName() + '_' + dsName + '_'
    for seq in range(seqRange[0], seqRange[1]):
        commName = resName + subType + str(seq)  #if dsName == 'airsim' else resName + str(seq)
        dm = VODataSetManager_CNN(dsName=dsName, subType=subType, seq=[seq], isTrain=False)
        dataset = dm.testSet

        mc = ModelContainer_CNN(Model_CNN_0(dsName))
        mc.load_weights(wName +'_best', train=False)

        pr_du, du_cov, \
        pr_dw, dw_cov, \
        pr_dtr, dtr_cov, \
        pr_dtr_gnd, \
        mae = mc.predict(dataset)

        noise = getNoiseLevel()

        np.savetxt(commName + '_du' + str(noise) + '.txt', pr_du)
        np.savetxt(commName + '_du_cov' + str(noise) + '.txt', du_cov)
        np.savetxt(commName + '_dw' + str(noise) + '.txt', pr_dw)
        np.savetxt(commName + '_dw_cov' + str(noise) + '.txt', dw_cov)
        np.savetxt(commName + '_dtr' + str(noise) + '.txt', pr_dtr)
        np.savetxt(commName + '_dtr_cov' + str(noise) + '.txt', dtr_cov)
        np.savetxt(commName + '_dtr_gnd' + str(noise) + '.txt', pr_dtr_gnd)

def runTrainTest(dsName, subType, seq, seqRange):
    runTrain(dsName, subType, seq, seqRange)
    runTest(dsName, subType, seqRange)

def runTrain(dsName, subType, seq, seqRange=None):
    s = time.time()
    train(dsName, subType, seq)
    print(time.time() - s)

def runTest(dsName, subType, seqRange):
    test(dsName, subType, seqRange)

if __name__ == '__main__':
    dsName = 'airsim'
    seq = [0]
    seqRange = [0, 3]
    #test
    #runTrainTest(dsName, 'mr', seq, seqRange)
    #runTrainTest(dsName, 'mrseg', seq, seqRange)

    runTrainTest('kitti', 'none', seq=[0, 2, 4, 6], seqRange=[0, 11])
    #runTest('kitti', 'none', seqRange=[0, 1])
    #runTrainTest('kitti', 'edge', seq=[0, 2, 4, 6], seqRange=[0, 11])
    #runTrainTest('mycar', 'none', seq=[0, 2], seqRange=[0,3])

