import pandas as pd
import os, joblib
from sklearn.metrics import confusion_matrix

# Load a model to identify baseline results

tor = r''
nor = r''
modelpath = r''

select_features = ['B_dstPortClassN', 'A_dstPortClassN', 'B_tcpMSS', 'A_ipMinTTL', 'A_ipMaxTTL', 'B_tcpBtm', 'A_tcpBtm', 'A_tcpTmS', 'A_tcpTmER', 'B_tcpTmER', 'A_tcpInitWinSz', 'B_tcpTmS', 'A_tcpRTTAckTripMin', 'B_ipMinTTL', 'A_tcpMaxWinSz', 'B_connDip', 'A_tcpAveWinSz', 'B_numBytesRcvd', 'A_tcpOptCnt', 'A_tcpRTTSseqAA', 'B_ipMaxTTL', 'A_dsMaxPl', 'B_connSip', 'A_ipMaxdIPID', 'A_numPktsRcvd', 'A_dsRangePl', 'A_tcpOptPktCnt', 'A_dsSkewPl', 'A_tcpSeqSntBytes', 'A_stdPktSize', 'A_tcpMinWinSz', 'B_tcpAveWinSz', 'B_tcpPSeqCnt', 'B_tcpInitWinSz', 'A_connSip', 'A_numBytesSnt', 'A_bytAsm', 'B_tcpFlwLssAckRcvdBytes', 'A_tcpMSS', 'A_dsMedianPl', 'B_tcpOptPktCnt', 'A_connDip', 'A_numPktsSnt', 'B_bytAsm', 'A_tcpPSeqCnt', 'A_avePktSize', 'B_tcpMaxWinSz', 'A_dsExcPl', 'A_tcpWS', 'B_dsMeanPl', 'B_tcpSSASAATrip', 'B_tcpMinWinSz', 'A_maxPktSz', 'A_tcpPAckCnt', 'A_tcpWinSzDwnCnt', 'A_dsRobStdIat', 'A_tcpFlwLssAckRcvdBytes', 'B_numPktsRcvd', 'B_tcpRTTAckTripMin', 'B_dsIqdIat']

pl_iat = ['0A_PL', '0A_IAT', '1A_PL', '1A_IAT', '2A_PL', '2A_IAT', '3A_PL', '3A_IAT', '4A_PL', '4A_IAT', '5A_PL', '5A_IAT', '6A_PL', '6A_IAT', '7A_PL', '7A_IAT', '8A_PL', '8A_IAT', '9A_PL', '9A_IAT', '10A_PL', '10A_IAT', '11A_PL', '11A_IAT', '12A_PL', '12A_IAT', '13A_PL', '13A_IAT', '14A_PL', '14A_IAT', '15A_PL', '15A_IAT', '16A_PL', '16A_IAT', '17A_PL', '17A_IAT', '18A_PL', '18A_IAT', '19A_PL', '19A_IAT', '0B_PL', '0B_IAT', '1B_PL', '1B_IAT', '2B_PL', '2B_IAT', '3B_PL', '3B_IAT', '4B_PL', '4B_IAT', '5B_PL', '5B_IAT', '6B_PL', '6B_IAT', '7B_PL', '7B_IAT', '8B_PL', '8B_IAT', '9B_PL', '9B_IAT', '10B_PL', '10B_IAT', '11B_PL', '11B_IAT', '12B_PL', '12B_IAT', '13B_PL', '13B_IAT', '14B_PL', '14B_IAT', '15B_PL', '15B_IAT', '16B_PL', '16B_IAT', '17B_PL', '17B_IAT', '18B_PL', '18B_IAT', '19B_PL', '19B_IAT']

if __name__ == '__main__':
    tor_data = pd.read_csv(tor ,low_memory=False, delimiter=',')
    tor_label = tor_data['class1']
    tor_data = tor_data[select_features]
    tor_data = tor_data.replace(' ', 0)

    nor_data = pd.read_csv(nor ,low_memory=False, delimiter=',')
    nor_label = nor_data['class1']
    nor_data = nor_data[select_features]
    nor_data = nor_data.replace(' ', 0)

    data = pd.concat([tor_data, nor_data])
    label = pd.concat([tor_label, nor_label])    

    modelnames = os.listdir(modelpath)
    n=1
    sheet = []
    for model in modelnames:
        clf = joblib.load(modelpath +'/' + model)
        predict = clf.predict(data)
        cfs_mtrx = confusion_matrix(label, predict, labels=['audio','mail','p2p','message','vedio','browser','voip','normal'])
        tmp = [n, model, cfs_mtrx[0][0], cfs_mtrx[0][1], cfs_mtrx[0][2], cfs_mtrx[0][3], cfs_mtrx[0][4], cfs_mtrx[0][5], cfs_mtrx[0][6], cfs_mtrx[0][7]]
        sheet.append(tmp)
        for i in range(1, 8):
            tmp = ['','',cfs_mtrx[i][0],cfs_mtrx[i][1],cfs_mtrx[i][2],cfs_mtrx[i][3],cfs_mtrx[i][4],cfs_mtrx[i][5],cfs_mtrx[i][6],cfs_mtrx[i][7]]
            sheet.append(tmp)
    
    writer = pd.ExcelWriter('data.xlsx')
    df = pd.DataFrame(sheet, columns=['num', 'model', 'audio','browser','vedio','p2p','message','mail','voip','normal'])
    df.to_excel(writer, index=False)
    writer.save()