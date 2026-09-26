function build_report_figures(outputDir)
% Reproducible figures and per-step data for the Turkish TeX report.
if nargin<1, outputDir=fullfile(fileparts(mfilename('fullpath')),'report','assets'); end
if ~exist(outputDir,'dir'),mkdir(outputDir);end
seed=[0 1 1 1 0 1 0 0 0]; T=24;
r=expand_requirement(seed,90,T); n=T+1;
N=zeros(n,1); onesCount=N; H1=N; H2=N; pooled=N; area=N; totalOnes=N;
pairCounts=zeros(n,4); rows=cell(n,1);
for k=1:n
    row=r.bits(k,r.domain(k,:)); N(k)=numel(row); onesCount(k)=sum(row);
    H1(k)=pattern_entropy(row,1);
    [H2(k),~,pairCounts(k,:)]=pattern_entropy(row,2);
    visible=r.bits(1:k,:); mask=r.domain(1:k,:);
    pooled(k)=pattern_entropy(visible(mask)',1);
    area(k)=sum(mask(:)); totalOnes(k)=sum(visible(mask));
    rows{k}=sprintf('%d',row);
end
stats=table((0:T)',N,onesCount,N-onesCount,H1,H2,area,totalOnes,pooled,...
    pairCounts(:,1),pairCounts(:,2),pairCounts(:,3),pairCounts(:,4),rows,...
    'VariableNames',{'Step','Width','Ones','Zeros','H1','H2','Area','TotalOnes',...
    'ImageH1','C00','C01','C10','C11','RowBits'});
writetable(stats,fullfile(outputDir,'step_metrics.csv'));
assert(all(area==((0:T)'+1).*(9+(0:T)')));
imwrite(uint8(255*(1-double(seed))),fullfile(outputDir,'seed.png'));

small=expand_requirement(seed,90,6);
f=makefig(1250,500); draw(small);
set(gca,'XTick',small.x,'YTick',0:6,'FontSize',12);
for k=1:7
    for c=find(small.domain(k,:))
        color='k'; if small.bits(k,c),color='w';end
        text(small.x(c),k-1,num2str(small.bits(k,c)),...
            'HorizontalAlignment','center','Color',color,'FontSize',12);
    end
end
title('Kural 90: ilk 7 satir, hucrelerin icinde ikili degerler');
saveplot(f,outputDir,'first_steps');

f=makefig(1200,850); ts=[0 4 12 24];
for j=1:4
    subplot(2,2,j); k=ts(j)+1;
    img=r.bits; mask=r.domain; mask(k+1:end,:)=false;
    rr=r; rr.bits=img;rr.domain=mask;draw(rr);
    title(sprintf('t = %d | son satir %d hucre | H1 = %.4f',ts(j),N(k),H1(k)));
end
saveplot(f,outputDir,'growth');

f=makefig(1200,560);
subplot(1,2,1);plot(0:T,H1,'-o','LineWidth',1.4,'MarkerSize',4);hold on;
plot(0:T,pooled,'-s','LineWidth',1.4,'MarkerSize',4);ylim([0 1.05]);grid on;
xlabel('Isleme adimi t');ylabel('Tekli desen entropisi (bit/hucre)');
legend('Yeni satir H1','Birikmis resim H1','Location','best');title('Satir ve birikmis resim');
subplot(1,2,2);plot(0:T,H2,'-o','LineWidth',1.4,'MarkerSize',4);
ylim([0 2.05]);grid on;xlabel('Isleme adimi t');ylabel('H2 (bit/ikili desen)');
title('Komsuluk yapisini da sayan olcum');
saveplot(f,outputDir,'entropy_curves');

f=makefig(1200,800); rules=[90 30 204];
for j=1:3
    z=expand_requirement(seed,rules(j),T);m=measure_expansion(z,4);
    subplot(2,3,j);draw(z);title(sprintf('Algilayici kurali %d',rules(j)));
    subplot(2,3,3+j);plot(m.Step,m.H1_bits,'LineWidth',1.4);hold on;
    plot(m.Step,m.FixedH1_bits,'--','LineWidth',1.4);ylim([0 1.05]);grid on;
    xlabel('Adim');ylabel('H1 (bit/hucre)');legend('Buyuyen','Sabit 9 hucre','Location','best');
end
saveplot(f,outputDir,'observer_windows');
save(fullfile(outputDir,'report_data.mat'),'seed','T','r','stats');
fprintf('REPORT FIGURES COMPLETE: %s\n',outputDir);
end
function f=makefig(w,h)
f=figure('Visible','off','Color','w','Position',[30 30 w h]);
end
function draw(r)
gray=ones(size(r.bits));gray(r.bits)=0;gray(~r.domain)=.88;
image(r.x,[0 r.steps],repmat(gray,[1 1 3]));axis tight;
set(gca,'YDir','reverse');xlabel('Hucre konumu i');ylabel('Isleme adimi t');
end
function saveplot(f,folder,name)
set(f,'PaperPositionMode','auto');
print(f,fullfile(folder,[name '.png']),'-dpng','-r180');
savefig(f,fullfile(folder,[name '.fig']));close(f);
end
