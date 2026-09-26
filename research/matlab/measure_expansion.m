function M = measure_expansion(result, halfWidth)
%MEASURE_EXPANSION Separate growing-window statistics from a fixed aperture.
if nargin<2, halfWidth=4; end
validateattributes(halfWidth,{'numeric'},{'scalar','integer','nonnegative'});
n=size(result.bits,1); H1=zeros(n,1); H2=H1; H4=H1;
fixedH1=H1; fixedH2=H1; density=H1; width=H1;
aperture=abs(result.x)<=halfWidth;
assert(any(aperture),'Fixed aperture contains no cells.');
for k=1:n
    row=result.bits(k,result.domain(k,:));
    H1(k)=pattern_entropy(row,1); H2(k)=pattern_entropy(row,2);
    H4(k)=pattern_entropy(row,4); density(k)=mean(row); width(k)=numel(row);
    observed=result.bits(k,aperture);
    fixedH1(k)=pattern_entropy(observed,1); fixedH2(k)=pattern_entropy(observed,2);
end
M=table((0:n-1)',width,density,H1,H2,H4,fixedH1,fixedH2,...
    'VariableNames',{'Step','WindowWidth','BlackFraction','H1_bits',...
    'H2_bits_per_pair','H4_bits_per_word','FixedH1_bits','FixedH2_bits_per_pair'});
end
