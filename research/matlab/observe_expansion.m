function [image, mask] = observe_expansion(result, blockWidth)
%OBSERVE_EXPANSION Observation-only majority coarse graining, no feedback.
% Fixed spatial bins; ties -> white. Only entirely in-domain blocks shown.
% This lossy view is not a more/less capable human without empirical evidence.
validateattributes(blockWidth,{'numeric'},{'scalar','integer','positive'});
[h,w]=size(result.bits); count=floor(w/blockWidth);
assert(count>=1,'Block width exceeds image width.');
image=false(h,count); mask=false(h,count);
for j=1:count
    cols=(j-1)*blockWidth+(1:blockWidth);
    image(:,j)=sum(result.bits(:,cols),2)>blockWidth/2;
    mask(:,j)=all(result.domain(:,cols),2);
end
end
