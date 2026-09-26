function verify_matlab
% Independent implementation of the restricted record contract (R2018b).
root=fileparts(mfilename('fullpath'));
data=jsondecode(fileread(fullfile(root,'fixtures.json')));
maxerr=0;
for j=1:numel(data)
    actual=check_record(data(j).record); expected=data(j).expected;
    assert(strcmp(actual.decision,expected.decision));
    assert(strcmp(actual.acceptance,expected.acceptance));
    assert(actual.closed==expected.closed);
    if ~strcmp(actual.decision,'invalid')
        assert(actual.support==expected.support);
        maxerr=max([maxerr abs(actual.label_entropy-expected.label_entropy) abs(actual.class_entropy-expected.class_entropy)]);
    end
end
assert(maxerr<1e-12);
report=struct('fixtures',numel(data),'max_entropy_difference',maxerr,'status','passed');
f=fopen(fullfile(root,'matlab_validation.json'),'w');fprintf(f,'%s',jsonencode(report));fclose(f);
disp(report);

outdir=fullfile(root,'..','assets');if ~exist(outdir,'dir'),mkdir(outdir);end
fig=figure('Visible','off','Color','w','Position',[50 50 1100 420]);
subplot(1,2,1);
q=[1 2 4 8 16];
plot(q,1+log2(q),'o-','LineWidth',1.4);hold on;plot(q,ones(size(q)),'s--','LineWidth',1.4);
set(gca,'XScale','log','XTick',q,'FontName','Times New Roman','FontSize',14);grid on;
xlabel(char([72 101 114 32 115 305 110 305 102 32 105 231 105 110 32 101 116 105 107 101 116 32 115 97 121 305 115 305]));ylabel('Entropi (bit)');
legend('Etiket entropisi',char([83 305 110 305 102 32 101 110 116 114 111 112 105 115 105]),'Location','northwest');
title(char([304 107 105 32 115 305 110 305 102 59 32 100 101 287 105 351 109 101 121 101 110 32 107 97 98 117 108]));
subplot(1,2,2);ks=35:52;h=zeros(size(ks));
for i=1:numel(ks),h(i)=ent([2^ks(i)-1 1]);end
semilogy(ks,h,'o-','LineWidth',1.4);hold on;plot([35 52],[1e-12 1e-12],'r--','LineWidth',1.4);
set(gca,'FontName','Times New Roman','FontSize',14);grid on;
xlabel(char([107 58 32 97 287 305 114 108 305 107 108 97 114 32 40 50 94 107 32 45 32 49 44 32 49 41]));ylabel(char([83 305 110 305 102 32 101 110 116 114 111 112 105 115 105 32 40 98 105 116 41]));
legend(char([304 107 105 32 115 305 110 305 102 32 104 226 108 226 32 97 231 305 107]),char([69 115 107 105 32 115 305 102 305 114 32 101 351 105 287 105]),'Location','southwest');
title(char([75 252 231 252 107 32 101 110 116 114 111 112 105 59 32 97 231 305 107 32 107 97 114 97 114]));
set(fig,'PaperPositionMode','auto');
print(fig,fullfile(outdir,'ayrimlar.png'),'-dpng','-r300');
savefig(fig,fullfile(outdir,'ayrimlar.fig'));close(fig);
end

function out=check_record(r)
out=struct('decision','invalid','acceptance','invalid','closed',false,'support',0,'label_entropy',NaN,'class_entropy',NaN);
keys={'requirement','version','implementation'};
for k=1:numel(keys),if ~isfield(r,keys{k})||~idok(r.(keys{k})),return,end,end
if ~islogical(r.reviewed)||~isscalar(r.reviewed)||~islogical(r.conflict)||~isscalar(r.conflict),return,end
c=r.criteria;e=r.evidence;a=r.alternatives;
if isempty(c)||~iscell(c)||~all(cellfun(@idok,c))||numel(unique(c))~=numel(c)||isempty(a),return,end
ids=cell(numel(a),1);cl=ids;m=zeros(numel(a),1);
for k=1:numel(a)
    if ~idok(a(k).id)||~idok(a(k).class),return,end
    v=a(k).mass;
    if ~isnumeric(v)||~isscalar(v)||~isfinite(v)||v<0||v~=fix(v),return,end
    ids{k}=a(k).id;cl{k}=a(k).class;m(k)=v;
end
if numel(unique(ids))~=numel(ids)||sum(m)<1||sum(m)>2^52,return,end
ek={'id','criterion','requirement','version','implementation','source','reviewer'};
ei=cell(numel(e),1);ec=ei;
for k=1:numel(e)
    for z=1:numel(ek),if ~idok(e(k).(ek{z})),return,end,end
    if ~islogical(e(k).approved)||~isscalar(e(k).approved)||~any(strcmp(e(k).result,{'pass','fail'})),return,end
    ei{k}=e(k).id;ec{k}=e(k).criterion;
end
if numel(unique(ei))~=numel(e)||numel(unique(ec))~=numel(e)||~all(ismember(ec,c)),return,end
classes=unique(cl);mclass=zeros(numel(classes),1);
for k=1:numel(classes),mclass(k)=sum(m(strcmp(cl,classes{k})));end
out.support=sum(mclass>0);out.closed=(out.support==1)&&~r.conflict;
out.decision='open';if r.conflict,out.decision='inconsistent';elseif out.closed,out.decision='committed';end
out.acceptance='pending';bound=numel(e)==numel(c);
for k=1:numel(e)
    bound=bound&&e(k).approved;
    for z=1:numel(keys),bound=bound&&strcmp(e(k).(keys{z}),r.(keys{z}));end
end
if r.reviewed&&~r.conflict&&bound
    out.acceptance='accepted';
    for k=1:numel(e),if strcmp(e(k).result,'fail'),out.acceptance='failed';end,end
end
out.label_entropy=ent(m);out.class_entropy=ent(mclass);
end

function ok=idok(s)
ok=ischar(s)&&isrow(s)&&~isempty(strtrim(s))&&strcmp(s,strtrim(s));
end

function h=ent(m)
p=m(m>0)/sum(m);h=-sum(p.*log2(p));
end
