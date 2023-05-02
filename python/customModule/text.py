from math import comb, floor, log2, pi, sqrt
from matplotlib import image
import numpy as np
from gnuradio import gr
import random

############### System Parameters ###############
M = 4  # M-ary modulation size
N = 4 # Number of sub-carriers
K = 1 # number of active sub-carriers

ro=0
Mary=1; # 1 PSK, 2 QAM
############### Misc Parameters ###############
iter = 4 # Iterations
nSymPerFrame = 1e4 # Number of Symbol per frame (1 OFDM Symbol)
bps = log2(M); # bits per M-ary symbol
c = 2^floor(log2(comb(N,K))); # Effective Carrier Combinations
p1 = floor(log2(comb(N,K)));  # index bit length per cluster
p2 = K*bps; # information bit length per cluster
p=p1+p2; # total number of bits

index_all = comb(N,K)
############### Bit generator ###############
## bit = (index bit + M-ary bps) * symbols in OFDM frame
bit = np.random.randint(0,2,size=(1,(p1+p2)*nSymPerFrame))
bit2 = bit.T
## bit split - reshape bit stream (p1+p2)
bit2 = np.ndarray.reshape((p1+p2),nSymPerFrame)
bit2 = bit2.T
print(bit2)
############### Index selector ###############
# information bits (p2)
info_bit = bit2[:,p1+1,:]

# M-ary data symbol
sym = []
x=1
for i in range(1,K+1):
    y = bps * i
    info_bit_i = info_bit[:,x:y]
    x = y + 1
    binary_info_bit_i = info_bit_i #from binary to decimal
    decimal_info_bit_i = int(binary_info_bit_i) #from binary to decimal
    # sym_i = sym_test(info_dec_i+1);
    if(Mary==1) :
        sym_i = pskmod(decimal_info_bit_i,M,ro*pi/M,'gray')
    elif (Mary!=1) :  #Modified 임시로 조건 걸어놈 ㅠ.ㅠ 저거 수정해야함 흑
        sym_i = qammod(decimal_info_bit_i,M,0,'gray')
    else :
        sym[:,i] = sym_i

    # index bits (p1)
    index_bit = bit2[:,1:p1]
    # index symbol ( bit to decimal ), select indices from combinatorial method
    index_sym = int(index_bit)
    # transmitted OFDM symbols
    tx_sym = np.zeros(N,nSymPerFrame)
    for kk in range(1, nSymPerFrame+1):
        kk_index = index_sym(kk)+1

