function test_requirement_ca
% Independent identities and edge cases; no toolbox required.
r=expand_requirement(1,90,3);
assert(isequal(double(r.bits),[0 0 0 1 0 0 0;0 0 1 0 1 0 0;...
    0 1 0 0 0 1 0;1 0 1 0 1 0 1]));
seed=[1 0 1 1 0 0 1];
for code=0:255
    r=expand_requirement(seed,code,1); prev=r.bits(1,:);
    expected=false(size(prev));
    for j=1:numel(prev)
        l=false; rr=false;
        if j>1,l=prev(j-1);end
        if j<numel(prev),rr=prev(j+1);end
        b=4*double(l)+2*double(prev(j))+double(rr);
        expected(j)=mod(floor(code/2^b),2)==1;
    end
    assert(isequal(r.bits(2,:),expected));
end
r=expand_requirement(seed,204,8);
assert(isequal(r.bits,repmat(r.bits(1,:),9,1))); % rule 204 identity
r=expand_requirement(0,1,2); assert(all(r.bits(2,:)) && ~any(r.bits(3,:)));
r=expand_requirement(seed,90,0); assert(isequal(r.bits,logical(seed)));
assert(pattern_entropy([0 0 0],1)==0);
assert(abs(pattern_entropy([0 1 0 1],1)-1)<1e-12);
[h,p,c]=pattern_entropy([0 0 1 1 0],2);
assert(abs(h-2)<1e-12 && all(p==.25) && all(c==1));
assert(isnan(pattern_entropy(1,2)));
r=expand_requirement(seed,90,8,'DecisionStep',3,'DecisionHalfWidth',2);
assert(~any(r.bits(r.removed)));
M=measure_expansion(r); assert(all(M.H1_bits>=0 & M.H1_bits<=1));
[coarse,mask]=observe_expansion(r,3);
assert(isequal(size(coarse),size(mask)) && isequal(r.bits,r.bits));
fprintf('PASS: 256 rule tables, Rule 90 pattern, identity, exterior, entropy and projection.\n');
end
