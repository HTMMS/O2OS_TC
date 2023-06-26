import pandas as pd
import sys,time, copy, os
import joblib
import numpy as np
from prettytable import PrettyTable
from sklearn import ensemble
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix
from imblearn import over_sampling, under_sampling
import math
from collections import Counter
import warnings

warnings.filterwarnings("ignore")

tor = r''
nor = r''
modelpath = r''
adaboostpath = r''

lowbound = 1
uppbound = 1000
increaseratio = 10

# output misclassification sampels# dont use!已失效，这里是测试集中的错误分类样本放入训练集，这样不对。
adaboostout = 0

# output classifcaition labels, for ensemble
ensembleout = 0

featuresort = ['B_dstPortClassN', 'A_dstPortClassN', 'B_tcpMSS', 'A_ipMinTTL', 'A_ipMaxTTL', 'B_tcpBtm', 'A_tcpBtm', 'A_tcpTmS', 'duration', 'A_tcpTmER', 'B_duration', 'B_tcpTmER', 'A_tcpInitWinSz', 'B_tcpTmS', 'A_tcpRTTAckTripMin', 'B_ipMinTTL', 'A_tcpMaxWinSz', 'B_connDip', 'A_tcpAveWinSz', 'A_duration', 'B_numBytesRcvd', 'A_tcpOptCnt', 'A_tcpRTTSseqAA', 'B_ipMaxTTL', 'A_dsMaxPl', 'B_connSip', 'A_ipMaxdIPID', 'A_numPktsRcvd', 'A_dsRangePl', 'A_tcpOptPktCnt', 'A_dsSkewPl', 'A_tcpSeqSntBytes', 'A_stdPktSize', 'A_tcpMinWinSz', 'B_tcpAveWinSz', 'B_tcpPSeqCnt', 'B_tcpInitWinSz', 'A_connSip', 'A_numBytesSnt', 'A_bytAsm', 'B_tcpFlwLssAckRcvdBytes', 'A_tcpMSS', 'A_dsMedianPl', 'B_tcpOptPktCnt', 'A_connDip', 'A_numPktsSnt', 'B_bytAsm', 'A_tcpPSeqCnt', 'A_avePktSize', 'B_tcpMaxWinSz', 'A_dsExcPl', 'A_tcpWS', 'B_dsMeanPl', 'B_tcpSSASAATrip', 'B_tcpMinWinSz', 'A_maxPktSz', 'A_tcpPAckCnt', 'A_tcpWinSzDwnCnt', 'A_dsRobStdIat', 'A_tcpFlwLssAckRcvdBytes', 'B_numPktsRcvd', 'B_tcpRTTAckTripMin', 'B_dsIqdIat', 'B_maxPktSz', 'B_numBytesSnt', 'B_connSipDprt', 'A_connSipDprt', 'A_dsMeanPl', 'B_connF', 'A_pktAsm', 'B_dsLowQuartileIat', 'A_dsStdPl', 'B_tcpSeqSntBytes', 'A_dsRobStdPl', 'B_ipMaxdIPID', 'B_nFpCnt', 'A_numBytesRcvd', 'A_connSipDip', 'B_numPktsSnt', 'B_tcpOptCnt', 'B_dsMedianIat', 'A_dsLowQuartilePl', 'B_dsUppQuartileIat', 'A_tcpRTTAckTripMax', 'B_tcpRTTAckJitAve', 'A_dsExcIat', 'A_connF', 'B_pktps', 'B_tcpWinSzUpCnt', 'A_tcpRTTAckTripAve', 'B_avePktSize', 'B_tcpRTTAckTripMax', 'A_stdIAT', 'A_tcpRTTAckTripJitAve', 'B_tcpPAckCnt', 'A_aveIAT', 'B_tcpRTTAckTripJitAve', 'B_connSipDip', 'A_dsModePl', 'B_tcpRTTAckTripAve', 'B_dsIqdPl', 'B_dsRangePl', 'B_dsLowQuartilePl', 'A_dsModeIat', 'B_tcpWinSzChgDirCnt', 'A_dsUppQuartilePl', 'B_dsUppQuartilePl', 'B_dsStdPl', 'B_dsRobStdIat', 'A_dsStdIat', 'B_maxIAT', 'A_dsUppQuartileIat', 'B_dsMaxPl', 'B_pktAsm', 'B_aveIAT', 'B_bytps', 'A_tcpWinSzUpCnt', 'B_tcpWinSzDwnCnt', 'A_bytps', 'A_dsMedianIat', 'B_dsRobStdPl', 'A_dsIqdPl', 'A_dsLowQuartileIat', 'B_dsSkewPl', 'A_dsMeanIat', 'B_tcpWS', 'A_maxIAT', 'B_stdPktSize', 'B_dsMedianPl', 'A_dsIqdIat', 'B_tcpRTTSseqAA', 'B_dsExcPl', 'B_dsExcIat', 'A_tcpWinSzChgDirCnt', 'B_dsMeanIat', 'B_stdIAT', 'A_nFpCnt', 'A_pktps', 'A_dsSkewIat', 'B_dsSkewIat', 'B_tcpAckFaultCnt', 'B_dsStdIat', 'A_tcpSeqFaultCnt', 'B_dsMaxIat', 'B_dsModePl', 'B_dsRangeIat', 'A_dsRangeIat', 'B_ipMindIPID', 'A_dsMaxIat', 'B_dsModeIat', 'B_dsMinIat', 'A_tcpAckFaultCnt', 'A_ipMindIPID', 'A_dsMinIat', 'B_tcpWinSzThRt', 'A_tcpWinSzThRt', 'B_tcpSeqFaultCnt', 'A_dsMinPl', 'B_dsMinPl', 'A_ipTTLChg', 'A_minPktSz', 'B_minPktSz', 'B_ipTTLChg', 'A_tcpRTTAckJitAve', 'A_tcpSSASAATrip']

select_features = ['B_tcpMSS', 'B_tcpBtm', 'A_tcpBtm', 'A_tcpTmS', 'duration', 'A_tcpTmER', 'B_duration', 'B_tcpTmER', 'A_tcpInitWinSz', 'B_tcpTmS', 'A_tcpMaxWinSz', 'A_tcpAveWinSz', 'A_duration', 'B_numBytesRcvd', 'A_tcpOptCnt', 'A_tcpRTTSseqAA', 'A_dsMaxPl', 'A_numPktsRcvd', 'A_dsRangePl', 'A_tcpOptPktCnt', 'A_dsSkewPl', 'A_tcpSeqSntBytes', 'A_stdPktSize', 'A_tcpMinWinSz', 'B_tcpAveWinSz', 'B_tcpPSeqCnt', 'B_tcpInitWinSz', 'A_numBytesSnt', 'A_bytAsm', 'B_tcpFlwLssAckRcvdBytes']

pl_iat = ['0A_PL', '0A_IAT', '1A_PL', '1A_IAT', '2A_PL', '2A_IAT', '3A_PL', '3A_IAT', '4A_PL', '4A_IAT', '5A_PL', '5A_IAT', '6A_PL', '6A_IAT', '7A_PL', '7A_IAT', '8A_PL', '8A_IAT', '9A_PL', '9A_IAT', '10A_PL', '10A_IAT', '11A_PL', '11A_IAT', '12A_PL', '12A_IAT', '13A_PL', '13A_IAT', '14A_PL', '14A_IAT', '15A_PL', '15A_IAT', '16A_PL', '16A_IAT', '17A_PL', '17A_IAT', '18A_PL', '18A_IAT', '19A_PL', '19A_IAT', '0B_PL', '0B_IAT', '1B_PL', '1B_IAT', '2B_PL', '2B_IAT', '3B_PL', '3B_IAT', '4B_PL', '4B_IAT', '5B_PL', '5B_IAT', '6B_PL', '6B_IAT', '7B_PL', '7B_IAT', '8B_PL', '8B_IAT', '9B_PL', '9B_IAT', '10B_PL', '10B_IAT', '11B_PL', '11B_IAT', '12B_PL', '12B_IAT', '13B_PL', '13B_IAT', '14B_PL', '14B_IAT', '15B_PL', '15B_IAT', '16B_PL', '16B_IAT', '17B_PL', '17B_IAT', '18B_PL', '18B_IAT', '19B_PL', '19B_IAT']

# 生成一个数据集迭代器,按照normal流量与Tor流量比例生成数据集
# a是比例下限，b是比例上限，nor_tor_ratio是比例递增数
def get_dataset(data, a=1, b=2, nor_tor_ratio=1):
    while(a<b):
        tor_num = len(data[data['class1']!='normal'])
        nor_num = math.ceil(tor_num*a)
        nor = len(data)-tor_num
        print('a: ', a, ' normal_num: ', nor_num)

        type_dict = Counter(data['class1'])
        type_dict['normal']=nor_num
        print(nor_num)

        if(nor<nor_num):
            # 上采样
            sampling = over_sampling.BorderlineSMOTE(kind='borderline-1',sampling_strategy=type_dict,random_state=42)
        else:
            # 下采样
            sampling = under_sampling.RandomUnderSampler(sampling_strategy=type_dict,random_state=42)
        
        features = data.iloc[:, :-1]
        label = data.iloc[:, -1]

        x, y = sampling.fit_resample(features, label)
        data = pd.concat([x, y], axis=1)
        yield a, data
        a += nor_tor_ratio

def get_tor_normal(tor,normal, a=1, b=2, ratio=1):
    while(a<=b):
        tor_num = len(tor)
        nor_num = math.ceil(tor_num*a)
        print('a: ', a, ' normal_num: ', nor_num)

        # 下采样
        nor = normal.sample(nor_num)
        data = pd.concat([tor, nor])
        yield a, data
        a += ratio

def classify(x_test, y_test, modeldict1, modeldict2):
    print('start')
    z_test = copy.deepcopy(y_test)
    z_test[z_test!='normal']='tor'
    table = PrettyTable(['num','time','all-accuracy','all-precision','all-recall','model-1','acc-1','pre-1','rec-1','model-2','acc-2','pre-2','rec-2'])
    online = []
    offline = []

    if(ensembleout> 0):
        esmb = pd.DataFrame(y_test.values)
        esmb.columns = ['label']
    n = 1
    # 在线识别
    for model1 in modeldict1:
        print(model1)
        clf_1 = joblib.load(modelpath +'/' + model1)
        start_1 = time.time()
        predict_1 = clf_1.predict(x_test[pl_iat])
        end_1 = time.time()

        # 模型评估
        acc_1 = accuracy_score(z_test, predict_1)
        rec_1 = recall_score(z_test, predict_1, pos_label='tor')
        pre_1 = precision_score(z_test, predict_1, pos_label='tor')
        cfs_mtrx_1 = confusion_matrix(z_test, predict_1, labels=['tor', 'normal'])
        tmp1 = [n, model1, cfs_mtrx_1[0][0],cfs_mtrx_1[0][1], acc_1, pre_1,rec_1]
        online.append(tmp1)
        tmp1 = ['', '', cfs_mtrx_1[1][0],cfs_mtrx_1[1][1], '', '','']
        online.append(tmp1)

        print(model1, " ", pre_1)
        
        # --------------------------------------------------------------------------------------------
        # 输出第一次分类错的结果
        if(adaboostout > 0):
            z_ar = np.array(z_test)
            Findex1 = np.where(z_ar!=predict_1)
            orgdata = pd.concat([x_test, y_test], axis=1)
            Fdata1 = orgdata.iloc[Findex1]
            Fdata1.to_csv(adaboostpath+'\\'+model1+'.csv', index=False)
        # --------------------------------------------------------------------------------------------

        m_test = x_test.iloc[np.where(predict_1=='tor')]
        n_test = y_test.iloc[np.where(predict_1=='tor')]

        # 离线识别
        for model2 in modeldict2:
            clf_2 = joblib.load(modelpath +'/' +model2)
            start_2 = time.time()
            predict_2 = clf_2.predict(m_test[select_features])
            end_2 = time.time()

            # 模型评估
            acc_2 = accuracy_score(n_test, predict_2)
            rec_2 = recall_score(n_test, predict_2, average='weighted')
            pre_2 = precision_score(n_test, predict_2, average='weighted')
            cfs_mtrx_2 = confusion_matrix(n_test, predict_2, labels=['audio','mail','p2p','message','vedio','browser','voip','normal'])
            tmp2 = [n,model1,model2,cfs_mtrx_2[0][0],cfs_mtrx_2[0][1],cfs_mtrx_2[0][2],cfs_mtrx_2[0][3],cfs_mtrx_2[0][4],cfs_mtrx_2[0][5],cfs_mtrx_2[0][6],cfs_mtrx_2[0][7]]
            offline.append(tmp2)
            for i in range(1, 8):
                tmp2 = ['','','',cfs_mtrx_2[i][0],cfs_mtrx_2[i][1],cfs_mtrx_2[i][2],cfs_mtrx_2[i][3],cfs_mtrx_2[i][4],cfs_mtrx_2[i][5],cfs_mtrx_2[i][6],cfs_mtrx_2[i][7]]
                offline.append(tmp2)
            
            # ----------------------------------------------------------------------------------------------------------------
            # 输出第二次分类错的结果
            if(adaboostout > 0):
                n_ar = np.array(n_test)
                Findex2 = np.where(n_ar!=predict_2)
                Fdata2 = orgdata.iloc[Findex2]
                Fdata2.to_csv(adaboostpath+'\\'+model2+'.csv', index=False)
            # ----------------------------------------------------------------------------------------------------------------
           
           # ----------------------------------------------------------------------------------------------------------------
            if(ensembleout > 0):
                p = pd.DataFrame(predict_1, columns=['p'])
                q = pd.DataFrame(predict_2, columns=['q'])
                idx = p[p['p']=='tor'].index
                qq = q.values
                q = pd.DataFrame(qq, index=idx, columns=[model1+model2])
                esmb = esmb.join(q[model1+model2])

           # ----------------------------------------------------------------------------------------------------------------

            table.add_row([n, end_1-start_1+end_2-start_2, 'all-accuracy',pre_2,rec_1*rec_2,model1,acc_1,pre_1,rec_1,model2,acc_2,pre_2,rec_2])
            n += 1
    if(ensembleout > 0):
        esmb.to_csv('ensemble.csv', index=False)
    return table, online, offline


if __name__ == '__main__':
    tor_data = pd.read_csv(tor ,low_memory=False, delimiter=',')
    tor_data = tor_data.replace(' ', 0)
    nor_data = pd.read_csv(nor ,low_memory=False, delimiter=',')
    nor_data = nor_data.replace(' ', 0)
    
    modelnames = os.listdir(modelpath)
    modeldict1 = [model for model in modelnames if model.find('1_')>=0]
    modeldict2 = [model for model in modelnames if model.find('2_')>=0]

    online_result = []
    offline_result = []

    #data_iter = get_dataset(data, 1, 501, 100)
    data_iter = get_tor_normal(tor_data,nor_data, lowbound, uppbound, increaseratio)
    while True:
        try:
            ratio, data = next(data_iter)
            features = data.iloc[:, :-1]
            label = data.iloc[:, -1]
            result, online, offline = classify(features, label, modeldict1, modeldict2)
            print(online)

            for i in online:
                i.insert(1,'') if i[0]=='' else i.insert(1, ratio)
                online_result.append(i)
            for i in offline:
                i.insert(1,'') if i[0]=='' else i.insert(1, ratio)
                offline_result.append(i)

            with open('result.txt', 'a') as f:
                f.write('\n')
                f.write('--------------------------------------------------------------------------------------\n')
                ratioline = 'a: '+str(ratio)+'------------------------------------------------------------------------\n'
                f.write(ratioline)
                f.write(str(result))
            
        except StopIteration:
            writer = pd.ExcelWriter('data.xlsx')# pylint: disable=abstract-class-instantiated
            df1 = pd.DataFrame(online_result, columns=['num','ratio','model1','tor','normal','accuracy','precision','recall'])
            df2 = pd.DataFrame(offline_result, columns=['num','ratio','model1','model2','audio','browser','vedio','p2p','message','mail','voip','normal'])
            df1.to_excel(writer,sheet_name='online',index=False)
            df2.to_excel(writer,sheet_name='offline',index=False)
            writer.save()
            sys.exit()
