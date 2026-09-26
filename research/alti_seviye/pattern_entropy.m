function [H, probabilities, counts] = pattern_entropy(row, blockLength)
%PATTERN_ENTROPY Empirical entropy of overlapping, non-wrapping binary words.
% H is bits/word, NOT entropy of an uncertain entire image or requirement.
% Order and scale matter. H(2)/2 is not an entropy-rate estimate.
if nargin<2, blockLength=1; end
validateattributes(blockLength,{'numeric'},{'scalar','integer','>=',1,'<=',16});
validateattributes(row,{'numeric','logical'},{'vector','nonempty','real','finite'});
assert(all(row(:)==0|row(:)==1),'Row must be binary.');
row=double(row(:)'); n=numel(row)-blockLength+1;
counts=zeros(1,2^blockLength); probabilities=counts;
if n<=0, H=NaN; return; end
code=zeros(1,n);
for j=1:blockLength, code=2*code+row(j:j+n-1); end
counts=accumarray(code(:)+1,1,[2^blockLength 1])';
probabilities=counts/sum(counts); q=probabilities(probabilities>0);
H=-sum(q.*log2(q));
end
