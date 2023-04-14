function y = pskmod(x,M,varargin)
    %PSKMOD Phase shift keying modulation
    %
    %   Y = PSKMOD(X,M) outputs the complex envelope of the modulation of
    %   the message signal X, using the phase shift keying (PSK)
    %   modulation. M is the alphabet size and must be an integer greater
    %   than 1. The message signal X must consist of integers between 0 and
    %   M-1. X can be a scalar, a vector, or a matrix. For two-dimensional
    %   signals, the function treats each column as 1 channel.
    %
    %   Y = PSKMOD(X,M,PHASEOFFSET) specifies the desired phase offset of
    %   the PSK constellation in PHASEOFFSET. The default value of
    %   PHASEOFFSET is 0.
    %
    %   Y = PSKMOD(X,M,PHASEOFFSET,SYMBOLORDER) specifies how the function
    %   assigns binary words to corresponding integers. If SYMBOLORDER is
    %   set to 'bin', then the function uses a natural binary-coded
    %   ordering. If SYMBOLORDER is set to 'gray', then the function uses a
    %   Gray-coded ordering. If SYMBOLORDER is an integer-valued vector
    %   with M elements, the function uses the ordering specified by this
    %   vector. This vector must have unique elements in the range [0,
    %   M-1]. The first element of this vector corresponds to the
    %   constellation point with the smallest positive angle, with
    %   subsequent elements running counter-clockwise. The default value of
    %   SYMBOLORDER is 'gray'.
    %
    %   Y = PSKMOD(X,M,...,Name,Value) specifies additional name-value pair
    %   arguments described below:
    %
    %   'InputType'          One of the strings: 'integer', or 'bit'.
    %                        'integer' indicates that the message signal is
    %                        integer valued between 0 and M-1. 'bit'
    %                        indicates that the message signal is binary (0
    %                        or 1). In this case, the number of rows
    %                        (dimension 1) must be an integer multiple of
    %                        log2(M). A group of log2(M) bits are mapped
    %                        onto a symbol, with the first bit representing
    %                        the MSB and the last bit representing the LSB.
    %                        The default value is 'integer'.
    %
    %   'OutputDataType'     One of the strings: 'double', or 'single'.
    %                        OutputDataType determines the data type of the
    %                        output modulated symbols and the data type
    %                        used for intermediate computations. The
    %                        default value is 'double'.
    %
    %   'PlotConstellation'  A logical scalar value. If true, the reference
    %                        PSK constellation is plotted. The default
    %                        value is false. 
    %
    %    Example 1:
    %    % BPSK modulation
    %    x = randi([0, 1], 10, 1);
    %    y = pskmod(x, 2);
    %
    %    Example 2:
    %    % QPSK modulation, with pi/4 phase offset
    %    % Gray coding
    %    x = (0:3)';
    %    y = pskmod(x, 4, pi/4);
    %
    %    Example 3:
    %    % 8-PSK modulation, with pi/8 phase offset, custom symbol
    %    % mapping and bit input. Visualize the reference constellation.
    %    x = randi([0, 1], 30, 2);
    %    customMap = [0 2 6 7 3 1 5 4];
    %    y = pskmod(x, 8, pi/8, customMap, 'InputType', 'bit', ...
    %               'PlotConstellation', true);
    %
    %    Example 4:
    %    % 16-PSK modulation, with single output data type
    %    x = randi([0, 15], 10, 3);
    %    y = pskmod(x, 16, 'OutputDataType', 'single');
    %
    %   See also PSKDEMOD, QAMMOD, APSKMOD, DVBSAPSKMOD, MIL188QAMMOD.
    
    %    Copyright 1996-2022 The MathWorks, Inc.
    
    %#codegen
    
    narginchk(2, 10);
    
    [phaseOffset, symbolOrder, symbolOrderVector, IOType, plotConstellation, outputDataType] = ...
        comm.internal.psk.parseAndValidateInputArgs(true, M, 'double', varargin{:});
    bitInput = strncmp(IOType, 'b', 1);
    
    % Validate X
    if bitInput
        validateattributes(x, {'double','single','int8','uint8','int16','uint16',...
            'int32','uint32','logical'}, {'real','binary'}, mfilename, 'X', 1);
        nBits = log2(M);
        coder.internal.errorIf(mod(size(x,1), nBits) ~= 0, 'comm:shared:xSizeBit');
        xSymbol = bit2int(cast(x, outputDataType), nBits);
    else
        validateattributes(x, {'double','single','int8','uint8','int16','uint16',...
            'int32','uint32',}, {'real','integer','>=',0,'<',M}, mfilename, 'X', 1);
        xSymbol = cast(x, outputDataType);
    end    
    
    % Handle symbol order
    if strncmpi(symbolOrder, 'gray', 4)
        [~, gray_map] = comm.internal.utilities.bin2gray(xSymbol, 'psk', M);
        [~, index] = ismember(xSymbol, gray_map);
        xNew = cast(index-1, outputDataType);
        
    elseif strncmpi(symbolOrder, 'custom', 6)
        symbolOrderMap = coder.nullcopy(zeros(M, 1, outputDataType));
        symbolOrderMap(symbolOrderVector + 1) = 0:M-1;
        if isrow(x)
            newSymbolOrderMap = symbolOrderMap';
        else
            newSymbolOrderMap = symbolOrderMap;
        end
        xNew = newSymbolOrderMap(xSymbol+1);
    else
        % bin symbol order
        xNew = xSymbol;
    end
    
    const = comm.internal.psk.getConstellation(M, phaseOffset, outputDataType);
    
    % If input is a vector, ensure that const has same orientation as
    % input. Note that, const is a column vector.
    if isrow(xNew)
        newConst = const.';
    else
        newConst = const;
    end

    % Compute output Y
    y = complex(newConst(xNew + 1));
    
    if plotConstellation && comm.internal.utilities.isSim()
        comm.internal.utilities.plotConstellation('PSK', double(M), const, symbolOrder, ...
            symbolOrderVector, bitInput);
    end        
end
