#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 cylee.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


# from math import comb, floor, log2, pi, sqrt
# from matplotlib import image
# import numpy as np
# from gnuradio import gr
# import random

############### System Parameters ###############
# M = 4  # M-ary modulation size
# N = 4 # Number of sub-carriers
# K = 1 # number of active sub-carriers

############### imperfect CSI setting ###############
# var = 0.05; # fixed imperfect CSI variance, see [1], [2]
# mmse = 1; # variable CSI
# CSI=1; # 1 perfect CSI, 2 fixed CSI error variance, 3 MMSE variable CSI error variance

# Detect_method =1; # to select 1 ML, 2 LLR, 3 Greedy GD detector
# LLR = 1; # select one of two types of LLR detector

# ro=0
# Mary=1; # 1 PSK, 2 QAM
# if(M==8) :
#     QAM = (5*M-4)/6; # QAM power scale factor #Modified ./ -> /
# else :
#     QAM = (2/3)*(M-1)

############### Misc Parameters ###############
# iter = 4 # Iterations
# nSymPerFrame = 1e4 # Number of Symbol per frame (1 OFDM Symbol)
# EbN0dB = range(0, 40, 5)
# EsN0 = 10.^(EbN0dB/10)
# sigma = sqrt(1./EsN0); # additive noise variance

# PwrSC = N/K; # Average Tx power per active sub-carrier
# bps = log2(M); # bits per M-ary symbol
# c = 2^floor(log2(comb(N,K))); # Effective Carrier Combinations
# p1 = floor(log2(comb(N,K)));  # index bit length per cluster
# p2 = K*bps; # information bit length per cluster
# p=p1+p2; # total number of bits

############### Reference M-ary and index symbols used for detection ###############
# index_all = comb(N,K) #Modified
# if(K==2 & N==4) :
#     # index_all = [1 0;2 0;3 1;3 2] # optimal combination for this case
#     index_all = comb(N,K)
# #else if :
# else : 
#     index_allz = index_all + 1

# sym_test = np.zeros(M,1)
# for qq in range(M,1):
#     if (Mary == 1):
#         sym_test.qq = pskmod(qq-1, M, ro*pi/M,'gray') #Modified qq and ./ -> /
#     else:
#         sym_test.qq=qammod(qq-1,M,0,'gray') #Modified

# ref_sym = sym_test
# if(Mary==1):
#     ref_symmm = ref_sym@(1./abs(ref_sym)) # PSK #Modified .* -> @
# else:
#     ref_symmm = ref_sym@(1/sqrt(QAM)) # QAM #Modified .* -> @


############### Loop for SNR ###############
# PEP = np.zeros(1,np.ndarray.shape(sigma,2)) # index symbol error IEP
# OFDM_SER = np.zeros(1,np.ndarray.shape(sigma,2)) # M-ary symbol error
# Total_SER = np.zeros(1,np.ndarray.shape(sigma,2)) # SEP overall
# BER=np.zeros(1,np.ndarray.shape(sigma,2))
# BER1=np.zeros(1,np.ndarray.shape(sigma,2)) # index bit error rate
# BER2=np.zeros(1,np.ndarray.shape(sigma,2)) # M-ary bit error rate

# for s1 in range(1,np.ndarray.shape(sigma,3)): #Modified _ range (sigma,2->3) 수정
#     print('== EbN0(dB) is %g == \n',EbN0dB(s1))
#     ############### Loop for iteration ###############
#     symerr_mcik = np.zeros(1,iter)
#     symerr_ofdm = np.zeros(1,iter)
#     symerr_iter= np.zeros(1,iter)
#     BER_iter= np.zeros(1,iter)
#     BER_iter_1= np.zeros(1,iter)
#     BER_iter_2= np.zeros(1,iter)
#     for s2 in range(1,iter):
#         print('== EbN0(dB) is %g and iteration is %g == \n',EbN0dB(s1),s2)
#         ############### Bit generator ###############
#         ## bit = (index bit + M-ary bps) * symbols in OFDM frame
#         bit = random.randint(range(0,2),1,(p1+p2)*nSymPerFrame) #Modified_[0,1]
#         ## bit split - reshape bit stream (p1+p2)
#         ## bit2 = np.ndarray.reshape(bit.',p1+p2,nSymPerFrame.') #TODO_reshape 소괄호 두개씀, 수정
#         bit2 = np.ndarray.reshape((bit),(p1+p2, nSymPerFrame))

#         ############### Index selector ###############
#         # information bits (p2)
#         # info_bit = bit2(:,p1+1:end)
#         info_bit = bit2([],[p1+1,]) #Modified 위에걸 이렇게 바꾸는게 맞나..?
#         # M-ary data symbol
#         sym=[] #배열 생성
#         x=1
#         for i in range(1,K+1):
#             y = bps * i
#             # info_bit_i= info_bit(:,x:y)
#             info_bit_i= info_bit[[],[x,y]] #Modified 위에걸 이렇게 바꾸는게 맞나..?
#             x = y + 1
#             # info_dec_i = bi2de(info_bit_i) # from binary to decimal
#             binary_info_bit_i = info_bit_i #Modified
#             decimal_info_bit_i = int(binary_info_bit_i) #Modified
#             # sym_i = sym_test(info_dec_i+1);
#             if(Mary==1) :
#                 sym_i = pskmod(decimal_info_bit_i,M,ro*pi/M,'gray') #Modified 
#             elif (Mary!=1) :  #Modified 임시로 조건 걸어놈 ㅠ.ㅠ 저거 수정해야함 흑
#                 sym_i = qammod(decimal_info_bit_i,M,0,'gray') #Modified 
#             else :
#                 # sym(:,i)=sym_i 
#                 sym [[],i] = sym_i #Modified

#             # index bits (p1)
#             # index_bit = bit2(:,1:p1)
#             index_bit = bit2[[],[1,p1]] #Modified
#             # index symbol ( bit to decimal ), select indices from combinatorial method
#             index_sym = BitoDe(index_bit)
#             # Set average symbol power to 1
#             sym_norm = sym*(1./abs(sym)) #Modified .* -> *
#             # Power reallocation
#             sym_tx = sym_norm*sqrt(PwrSC) #Modified .* -> *
#             # transmitted OFDM symbols
#             tx_sym = np.zeros(N,nSymPerFrame)
#             for kk in range(1,nSymPerFrame+1):
#                 kk_index = index_sym(kk)+1
#                 indices = index_all([kk_index,])+1  #Modified
#                 tx_sym[indices,kk] = sym_tx[kk,] #Modified

#             ############### CSI error variance ###############
#             if(CSI==1) :
#                 eps=0       #perfect CSI
#             elif (CSI==2) :
#                 eps=var     #fixed CSI
#             else :
#                 eps=1/(1+mmse*EsN0(s1))     #variable CSI

#             ############### Transmission over Rayleigh fading channel and AWGN noise ###############
#             #noise = 1/sqrt(2)*(randn(size(tx_sym))+1i*randn(size(tx_sym)))
#             #h = 1/sqrt(2)*(randn(size(tx_sym))+1i*randn(size(tx_sym)))*sqrt(1-eps)
#             #e=sqrt(eps)./sqrt(2)*(randn(size(tx_sym))+1i*randn(size(tx_sym)))
            
#             noise = 1/sqrt(2)*random.randint((tx_sym.size)) + np.imag(1)*random.randint(tx_sym.size) #Modified
#             h = 1/sqrt(2)*random.randint(tx_sym.size) + np.imag(1) * random.randint(tx_sym.size) * sqrt(1-eps) #Modified
#             e=sqrt(eps)/sqrt(2)*random.randint(tx_sym.size) + np.imag(1) * random.randint(tx_sym.size) #Modified
#             h1=h+e
#             y = sqrt(EsN0(s1))*h1*tx_sym+noise #Modified *
#             avSNR=sqrt(EsN0(s1))

            ############### ML / LLR / Greedy detectors ###############
            #Not yet, maybe unnecessary

            ############### error rate computation ###############
            #ofdm symbol error
            #index symbol error
            #index symbol to bit, index bit error
            #QAM symbol to bit

            ############### symbol & bit error rate  1 iteration ###############
            #Not yet

            ############### average bit error rate ###############
            #Not yet
            










############### Basic Function ###############
class indexModulation(gr.basic_block):
    """
    docstring for block indexModulation
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="indexModulation",
            in_sig=[np.float32],
            out_sig=[np.float32])

#    def forecast(self, noutput_items, ninputs):
        # ninputs is the number of input connections
        # setup size of input_items[i] for work call
        # the required number of input items is returned
        #   in a list where each element represents the
        #   number of required items for each input
 #       ninput_items_required = [noutput_items] * ninputs
  #      return ninput_items_required

    def general_work(self, input_items, output_items):
        # For this sample code, the general block is made to behave like a sync block
        ninput_items = min([len(items) for items in input_items])
        noutput_items = min(len(output_items[0]), ninput_items)
        output_items[0][:noutput_items] = input_items[0][:noutput_items]
        self.consume_each(noutput_items)
        return noutput_items
    
    # def pskmod(self, x,M,varargin):
    #     return 
    
    # def qammod(self):
    #     return  

