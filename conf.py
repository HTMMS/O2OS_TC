# Feature Importance Ranking
featuresort = ['B_dstPortClassN', 'A_dstPortClassN', 'B_tcpMSS', 'A_ipMinTTL', 'A_ipMaxTTL', 'B_tcpBtm', 'A_tcpBtm', 'A_tcpTmS', 'duration', 'A_tcpTmER', 'B_duration', 'B_tcpTmER', 'A_tcpInitWinSz', 'B_tcpTmS', 'A_tcpRTTAckTripMin', 'B_ipMinTTL', 'A_tcpMaxWinSz', 'B_connDip', 'A_tcpAveWinSz', 'A_duration', 'B_numBytesRcvd', 'A_tcpOptCnt', 'A_tcpRTTSseqAA', 'B_ipMaxTTL', 'A_dsMaxPl', 'B_connSip', 'A_ipMaxdIPID', 'A_numPktsRcvd', 'A_dsRangePl', 'A_tcpOptPktCnt', 'A_dsSkewPl', 'A_tcpSeqSntBytes', 'A_stdPktSize', 'A_tcpMinWinSz', 'B_tcpAveWinSz', 'B_tcpPSeqCnt', 'B_tcpInitWinSz', 'A_connSip', 'A_numBytesSnt', 'A_bytAsm', 'B_tcpFlwLssAckRcvdBytes', 'A_tcpMSS', 'A_dsMedianPl', 'B_tcpOptPktCnt', 'A_connDip', 'A_numPktsSnt', 'B_bytAsm', 'A_tcpPSeqCnt', 'A_avePktSize', 'B_tcpMaxWinSz', 'A_dsExcPl', 'A_tcpWS', 'B_dsMeanPl', 'B_tcpSSASAATrip', 'B_tcpMinWinSz', 'A_maxPktSz', 'A_tcpPAckCnt', 'A_tcpWinSzDwnCnt', 'A_dsRobStdIat', 'A_tcpFlwLssAckRcvdBytes', 'B_numPktsRcvd', 'B_tcpRTTAckTripMin', 'B_dsIqdIat', 'B_maxPktSz', 'B_numBytesSnt', 'B_connSipDprt', 'A_connSipDprt', 'A_dsMeanPl', 'B_connF', 'A_pktAsm', 'B_dsLowQuartileIat', 'A_dsStdPl', 'B_tcpSeqSntBytes', 'A_dsRobStdPl', 'B_ipMaxdIPID', 'B_nFpCnt', 'A_numBytesRcvd', 'A_connSipDip', 'B_numPktsSnt', 'B_tcpOptCnt', 'B_dsMedianIat', 'A_dsLowQuartilePl', 'B_dsUppQuartileIat', 'A_tcpRTTAckTripMax', 'B_tcpRTTAckJitAve', 'A_dsExcIat', 'A_connF', 'B_pktps', 'B_tcpWinSzUpCnt', 'A_tcpRTTAckTripAve', 'B_avePktSize', 'B_tcpRTTAckTripMax', 'A_stdIAT', 'A_tcpRTTAckTripJitAve', 'B_tcpPAckCnt', 'A_aveIAT', 'B_tcpRTTAckTripJitAve', 'B_connSipDip', 'A_dsModePl', 'B_tcpRTTAckTripAve', 'B_dsIqdPl', 'B_dsRangePl', 'B_dsLowQuartilePl', 'A_dsModeIat', 'B_tcpWinSzChgDirCnt', 'A_dsUppQuartilePl', 'B_dsUppQuartilePl', 'B_dsStdPl', 'B_dsRobStdIat', 'A_dsStdIat', 'B_maxIAT', 'A_dsUppQuartileIat', 'B_dsMaxPl', 'B_pktAsm', 'B_aveIAT', 'B_bytps', 'A_tcpWinSzUpCnt', 'B_tcpWinSzDwnCnt', 'A_bytps', 'A_dsMedianIat', 'B_dsRobStdPl', 'A_dsIqdPl', 'A_dsLowQuartileIat', 'B_dsSkewPl', 'A_dsMeanIat', 'B_tcpWS', 'A_maxIAT', 'B_stdPktSize', 'B_dsMedianPl', 'A_dsIqdIat', 'B_tcpRTTSseqAA', 'B_dsExcPl', 'B_dsExcIat', 'A_tcpWinSzChgDirCnt', 'B_dsMeanIat', 'B_stdIAT', 'A_nFpCnt', 'A_pktps', 'A_dsSkewIat', 'B_dsSkewIat', 'B_tcpAckFaultCnt', 'B_dsStdIat', 'A_tcpSeqFaultCnt', 'B_dsMaxIat', 'B_dsModePl', 'B_dsRangeIat', 'A_dsRangeIat', 'B_ipMindIPID', 'A_dsMaxIat', 'B_dsModeIat', 'B_dsMinIat', 'A_tcpAckFaultCnt', 'A_ipMindIPID', 'A_dsMinIat', 'B_tcpWinSzThRt', 'A_tcpWinSzThRt', 'B_tcpSeqFaultCnt', 'A_dsMinPl', 'B_dsMinPl', 'A_ipTTLChg', 'A_minPktSz', 'B_minPktSz', 'B_ipTTLChg', 'A_tcpRTTAckJitAve', 'A_tcpSSASAATrip']

# statistical features we used
select_features = ['B_dstPortClassN', 'A_dstPortClassN', 'B_tcpMSS', 'A_ipMinTTL', 'A_ipMaxTTL', 'B_tcpBtm', 'A_tcpBtm', 'A_tcpTmS', 'A_tcpTmER', 'B_tcpTmER', 'A_tcpInitWinSz', 'B_tcpTmS', 'A_tcpRTTAckTripMin', 'B_ipMinTTL', 'A_tcpMaxWinSz', 'A_tcpAveWinSz', 'B_numBytesRcvd', 'A_tcpOptCnt', 'A_tcpRTTSseqAA', 'B_ipMaxTTL', 'A_dsMaxPl', 'A_ipMaxdIPID', 'A_numPktsRcvd', 'A_dsRangePl', 'A_tcpOptPktCnt', 'A_dsSkewPl', 'A_tcpSeqSntBytes', 'A_stdPktSize', 'A_tcpMinWinSz', 'B_tcpAveWinSz', 'B_tcpPSeqCnt', 'B_tcpInitWinSz', 'A_numBytesSnt', 'A_bytAsm', 'B_tcpFlwLssAckRcvdBytes', 'A_tcpMSS', 'A_dsMedianPl', 'B_tcpOptPktCnt', 'A_numPktsSnt', 'B_bytAsm', 'A_tcpPSeqCnt', 'A_avePktSize', 'B_tcpMaxWinSz', 'A_dsExcPl', 'A_tcpWS', 'B_dsMeanPl', 'B_tcpSSASAATrip', 'B_tcpMinWinSz', 'A_maxPktSz', 'A_tcpPAckCnt', 'A_tcpWinSzDwnCnt', 'A_dsRobStdIat', 'A_tcpFlwLssAckRcvdBytes', 'B_numPktsRcvd', 'B_tcpRTTAckTripMin', 'B_dsIqdIat', 'B_maxPktSz', 'B_numBytesSnt', 'A_dsMeanPl','A_pktAsm']

pl_iat = ['0A_PL', '0A_IAT', '1A_PL', '1A_IAT', '2A_PL', '2A_IAT', '3A_PL', '3A_IAT', '4A_PL', '4A_IAT', '5A_PL', '5A_IAT', '6A_PL', '6A_IAT', '7A_PL', '7A_IAT', '8A_PL', '8A_IAT', '9A_PL', '9A_IAT', '10A_PL', '10A_IAT', '11A_PL', '11A_IAT', '12A_PL', '12A_IAT', '13A_PL', '13A_IAT', '14A_PL', '14A_IAT', '15A_PL', '15A_IAT', '16A_PL', '16A_IAT', '17A_PL', '17A_IAT', '18A_PL', '18A_IAT', '19A_PL', '19A_IAT', '0B_PL', '0B_IAT', '1B_PL', '1B_IAT', '2B_PL', '2B_IAT', '3B_PL', '3B_IAT', '4B_PL', '4B_IAT', '5B_PL', '5B_IAT', '6B_PL', '6B_IAT', '7B_PL', '7B_IAT', '8B_PL', '8B_IAT', '9B_PL', '9B_IAT', '10B_PL', '10B_IAT', '11B_PL', '11B_IAT', '12B_PL', '12B_IAT', '13B_PL', '13B_IAT', '14B_PL', '14B_IAT', '15B_PL', '15B_IAT', '16B_PL', '16B_IAT', '17B_PL', '17B_IAT', '18B_PL', '18B_IAT', '19B_PL', '19B_IAT']

# replace these path to your paths
torpath = '/home/O2OS/Documents/tor_train.csv'
norpath = '/home/O2OS/Documents/nor_train.csv'
modelpath = '/home/O2OS/Documents/models'

tor_testpath = '/home/O2OS/Documents/tor_test.csv'
nor_testpath = '/home/O2OS/Documents/nor_test.csv'

adaboostpath = '/home/O2OS/Documents/adaboost'

# output misclassification results
adaboostout = 0

# output prediction labels for ensemble tech.
ensembleout = 0

# 1=naive; 2=slightly; 3=strong
ensemble_strategy = 1