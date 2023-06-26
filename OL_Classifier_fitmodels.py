import pandas as pd
import joblib
import copy
import numpy as np
from collections import Counter
import Models_Classifier as models
from imblearn import over_sampling

select_features = ['B_dstPortClassN', 'A_dstPortClassN', 'B_tcpMSS', 'A_ipMinTTL', 'A_ipMaxTTL', 'B_tcpBtm', 'A_tcpBtm', 'A_tcpTmS', 'A_tcpTmER', 'B_tcpTmER', 'A_tcpInitWinSz', 'B_tcpTmS', 'A_tcpRTTAckTripMin', 'B_ipMinTTL', 'A_tcpMaxWinSz', 'B_connDip', 'A_tcpAveWinSz', 'B_numBytesRcvd', 'A_tcpOptCnt', 'A_tcpRTTSseqAA', 'B_ipMaxTTL', 'A_dsMaxPl', 'B_connSip', 'A_ipMaxdIPID', 'A_numPktsRcvd', 'A_dsRangePl', 'A_tcpOptPktCnt', 'A_dsSkewPl', 'A_tcpSeqSntBytes', 'A_stdPktSize', 'A_tcpMinWinSz', 'B_tcpAveWinSz', 'B_tcpPSeqCnt', 'B_tcpInitWinSz', 'A_connSip', 'A_numBytesSnt', 'A_bytAsm', 'B_tcpFlwLssAckRcvdBytes', 'A_tcpMSS', 'A_dsMedianPl', 'B_tcpOptPktCnt', 'A_connDip', 'A_numPktsSnt', 'B_bytAsm', 'A_tcpPSeqCnt', 'A_avePktSize', 'B_tcpMaxWinSz', 'A_dsExcPl', 'A_tcpWS', 'B_dsMeanPl', 'B_tcpSSASAATrip', 'B_tcpMinWinSz', 'A_maxPktSz', 'A_tcpPAckCnt', 'A_tcpWinSzDwnCnt', 'A_dsRobStdIat', 'A_tcpFlwLssAckRcvdBytes', 'B_numPktsRcvd', 'B_tcpRTTAckTripMin', 'B_dsIqdIat']

pl_iat = ['0A_PL', '0A_IAT', '1A_PL', '1A_IAT', '2A_PL', '2A_IAT', '3A_PL', '3A_IAT', '4A_PL', '4A_IAT', '5A_PL', '5A_IAT', '6A_PL', '6A_IAT', '7A_PL', '7A_IAT', '8A_PL', '8A_IAT', '9A_PL', '9A_IAT', '10A_PL', '10A_IAT', '11A_PL', '11A_IAT', '12A_PL', '12A_IAT', '13A_PL', '13A_IAT', '14A_PL', '14A_IAT', '15A_PL', '15A_IAT', '16A_PL', '16A_IAT', '17A_PL', '17A_IAT', '18A_PL', '18A_IAT', '19A_PL', '19A_IAT', '0B_PL', '0B_IAT', '1B_PL', '1B_IAT', '2B_PL', '2B_IAT', '3B_PL', '3B_IAT', '4B_PL', '4B_IAT', '5B_PL', '5B_IAT', '6B_PL', '6B_IAT', '7B_PL', '7B_IAT', '8B_PL', '8B_IAT', '9B_PL', '9B_IAT', '10B_PL', '10B_IAT', '11B_PL', '11B_IAT', '12B_PL', '12B_IAT', '13B_PL', '13B_IAT', '14B_PL', '14B_IAT', '15B_PL', '15B_IAT', '16B_PL', '16B_IAT', '17B_PL', '17B_IAT', '18B_PL', '18B_IAT', '19B_PL', '19B_IAT']

normal_class = 1 # Whether the normal class is treated as a separate class

torpath = r''
norpath = r''
modelpath = r''

Online_model = {'c45':models.c45,'knn':models.knn,'rf30':models.rf30,'gbdt':models.gbdt}
Offline_model = {'c45':models.c45,'knn':models.knn,'rf30':models.rf30,'gbdt':models.gbdt}

# tor_train 27985 samles
nor_num_1 = 30000 #how many normal sampels in online
nor_num_2 = 5000 #how many normal sampels in offline

# generate bordlerline samples
borderline = 0

# output adaboost samples
adaboostout = 0
adaboostpath = r''

def fitmodel(online_dict, offline_dict):
    tor = pd.read_csv(torpath, low_memory=False)
    norl = pd.read_csv(norpath, low_memory=False)
    norl = norl.replace(' ', 0)
    nor = norl.sample(nor_num_1)

    data = pd.concat([tor, nor])
    data = data.replace(' ', 0)

    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # generate borderline samples during online stage
    if(borderline > 0):
        {'browser': 5000, 'mail': 5000, 'p2p': 5000, 'voip': 5000, 'message': 3797, 'vedio': 2514, 'audio': 1674}

        x = data.iloc[::, 0:-1]
        y = data.iloc[::, -1]
        # improve recall
        #Blsmo = over_sampling.BorderlineSMOTE(kind='borderline-1',sampling_strategy={'browser': 5000, 'mail': 5000, 'p2p': 5000, 'voip': 5000, 'message': 3797, 'vedio': 2514, 'audio': 1674, 'normal': 10000},random_state=42)
        # improve precision
        Blsmo = over_sampling.BorderlineSMOTE(kind='borderline-1',sampling_strategy=online_dict,random_state=42)

        m, n = Blsmo.fit_resample(x, y)
        columns = data.columns.values
        data = pd.concat([m,n], axis=1)
        data.columns = columns
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    features_1 = data[pl_iat]

    label2 = data['class1']

    label1 = copy.deepcopy(label2)
    label1[label1!='normal']='tor'

    print("1阶段：",Counter(label1))
    for model1 in Online_model:
        # fit online model
        print(model1)
        clf_1 = Online_model[model1]()
        clf_1.fit(features_1,label1)
        # save online model
        joblib.dump(clf_1, modelpath+'/1_'+model1+'.m')
        if(adaboostout > 0):
            # 本分类器中分类错误的
            predict_1 = clf_1.predict(features_1)
            arr_label1 = np.array(label1)
            index1 = np.where(arr_label1!=predict_1)
            data1 = data.iloc[index1]
            # 训练集其他normal类中分类错误的
            predict_1 = clf_1.predict(norl[pl_iat])
            index1 = np.where(norl['class1']!=predict_1)
            data2 = norl.iloc[index1]
            data1 = pd.concat([data1, data2])
            data1.to_csv(adaboostpath+'\\1_'+model1+'.csv', index=False)

    nor = nor.sample(nor_num_2)
    data = pd.concat([tor, nor])
    data = data.replace(' ', 0)

    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # 基于borderline的样本生成
    if(borderline > 0):
        {'browser': 5000, 'mail': 5000, 'p2p': 5000, 'voip': 5000, 'message': 3797, 'vedio': 2514, 'audio': 1674}

        x = data.iloc[::, 0:-1]
        y = data.iloc[::, -1]
        # 提升tor样本以提高recall
        #Blsmo = over_sampling.BorderlineSMOTE(kind='borderline-1',sampling_strategy={'browser': 5000, 'mail': 5000, 'p2p': 5000, 'voip': 5000, 'message': 3797, 'vedio': 2514, 'audio': 1674, 'normal': 10000},random_state=42)
        # 提升normal样本提升precision
        Blsmo = over_sampling.BorderlineSMOTE(kind='borderline-1',sampling_strategy=offline_dict,random_state=42)

        m, n = Blsmo.fit_resample(x, y)
        columns = data.columns.values
        data = pd.concat([m,n], axis=1)
        data.columns = columns
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    features_2 = data[select_features]
    label2 = data['class1']

    print("2阶段：",Counter(label2))
    for model2 in Offline_model:
        #离线识别模型训练
        print(model2)
        clf_2 = Offline_model[model2]()
        clf_2.fit(features_2, label2)
        # 保存模型
        joblib.dump(clf_2, modelpath+'/2_'+model2+'.m')
        if(adaboostout > 0):
            # 本分类器中分类错误的
            predict_2 = clf_2.predict(features_2)
            arr_label2 = np.array(label2)
            index2 = np.where(arr_label2!=predict_2)
            data1 = data.iloc[index2]
            # 训练集其他normal类中分类错误的
            predict_2 = clf_2.predict(norl[select_features])
            index2 = np.where(norl['class1']!=predict_2)
            data2 = norl.iloc[index2]
            data1 = pd.concat([data1, data2])
            data1.to_csv(adaboostpath+'\\2_'+model2+'.csv', index=False)

def cirfitmodel():
    onlinedict = {'browser': 5000, 'mail': 5000, 'p2p': 5000, 'voip': 5000, 'message': 3797, 'vedio': 2514, 'audio': 1674, 'normal':nor_num_1}
    offlinedict = {'browser': 5000, 'mail': 5000, 'p2p': 5000, 'voip': 5000, 'message': 3797, 'vedio': 2514, 'audio': 1674, 'normal':nor_num_2}
    for i in range(0,10):
        for j in range(0,10):
            offlinedict['normal']+=(j*0.1*nor_num_2)
        onlinedict['browser']+=500
        onlinedict['mail']+=500
        onlinedict
            
    fitmodel(onlinedict, offlinedict)

cirfitmodel()