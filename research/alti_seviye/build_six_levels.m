function build_six_levels(outputDir)
% Six requirement levels, five periods of exactly ten CA thinking steps.
% Decision rendering is explicit entropy-controlled recoding, not new evidence.
if nargin<1,outputDir=fullfile(fileparts(mfilename('fullpath')),'six_level_report','assets');end
if ~exist(outputDir,'dir'),mkdir(outputDir);end
seed=[0 1 1 1 0 1 0 0 0];T=55;W=119;rules=[90 150 30 110 90];
bits=dec2bin(0:15,4)-'0';target=[1 0 1 1];rank=[11 10 3 15 9 7 2 14 1 13 8 6 5 0 12 4];
summary=zeros(5,7);
for m=1:5
 X=false(56,W);domain=false(56,W);X(1,56:64)=seed;domain(1,56:64)=true;
 values=zeros(56,15);probs=zeros(56,16);allrows=cell(56,1);
 levelH=pattern_entropy(seed,1);
 for t=0:T
  g=floor(t/11);[p,open]=distribution(m,g,bits,target,rank);U=-sum(p(p>0).*log2(p(p>0)));
  probs(t+1,:)=p';width=9+2*t;isgate=t>0 && mod(t,11)==0;pre=NaN;targetH=NaN;removed=0;rule=-1;
  if t>0
   domain(t+1,56-t:64+t)=true;old=X(t,:);
   if isgate
    % Decision row grows by two white boundary cells; no extra CA step.
    raw=old;current=raw(domain(t+1,:));pre=pattern_entropy(current,1);
    prevH=values(t,5);prevU=values(t,8);
    targetH=min([pre prevH levelH])*(U/prevU);
    nBlack=sum(current);
    if g==5,k=0;
    else
     counts=1:min(nBlack,floor(width/2));h=arrayfun(@(b)binaryH(b/width),counts);
     allowed=counts(h<min([pre prevH levelH])-1e-12);
     assert(~isempty(allowed),'No nonzero entropy-decreasing representation exists.');
     below=allowed(arrayfun(@(b)binaryH(b/width),allowed)<=targetH+1e-12);
     if isempty(below),k=min(allowed);else,k=max(below);end
    end
    positions=find(raw);X(t+1,:)=false;
    if k>0
     pick=floor(((1:k)-.5)*numel(positions)/k)+1;
     X(t+1,positions(pick))=true;
    end
    removed=nBlack-k;levelH=pattern_entropy(X(t+1,domain(t+1,:)),1);
   else
    rule=rules(g+1);left=[false old(1:end-1)];right=[old(2:end) false];idx=4*double(left)+2*double(old)+double(right);
    X(t+1,:)=logical(bitget(uint16(rule),idx+1));
   end
  end
  row=X(t+1,domain(t+1,:));mask=domain(1:t+1,:);im=X(1:t+1,:);
  values(t+1,:)=[t g+1 rule sum(row) pattern_entropy(row,1) pattern_entropy(row,2) pattern_entropy(im(mask)',1) U sum(p>0) open 4*(t==55) pre targetH removed isgate];
  allrows{t+1}=sprintf('%d',row);
 end
 gates=12:11:56;
 assert(all(diff(values([1 gates],5))<0) && all(diff(values([1 gates],8))<0));
 assert(all(values(gates,5)<values(gates-1,5)) && all(values(gates,5)<values(gates,12)));
 assert(all(values(end,[4 5 6 8 10])==0) && values(end,9)==1 && values(end,11)==4);
 stats=array2table(values,'VariableNames',{'Step','Level','Rule','Ones','H1','H2','HistoryH1','ProjectU','Candidates','OpenTopics','Verified','PreDecisionH1','TargetH1','RemovedMarks','IsGate'});
 stats.RowBits=allrows;writetable(stats,fullfile(outputDir,sprintf('method_%d.csv',m)));
 writetable(array2table(probs,'VariableNames',arrayfun(@(j)sprintf('C%d',j),0:15,'UniformOutput',false)),fullfile(outputDir,sprintf('posterior_%d.csv',m)));
 % Wide margin carries requirement and thinking-period labels explicitly.
 f=figure('Visible','off','Color','w','Position',[20 20 1350 880]);
 axes('Position',[.075 .085 .53 .85]);gray=ones(size(X));gray(X)=0;gray(~domain)=.90;
 image(-59:59,[0 T],repmat(gray,[1 1 3]));set(gca,'YDir','reverse');xlim([-60 60]);ylim([-.8 55.8]);hold on;
 set(gca,'YTick',0:11:55,'FontSize',11);xlabel('Hucre konumu i');ylabel('Adim t');title(sprintf('Yontem %d: alti gereksinim seviyesi',m));
 for level=1:6
  t=(level-1)*11;plot([-60 60],[t t],':','Color',[.12 .35 .65]);
  text(64,t,sprintf('%d. seviye gereksinim  |  t=%d',level,t),'FontWeight','bold','FontSize',12,'Color',[.1 .25 .45],'Clipping','off');
  if level<6
   text(64,t+5.5,sprintf('Dusunme ve inceleme %d\n%d-%d. adimlar (10 adim)',level,t+1,t+10),'FontSize',11,'Clipping','off');
  end
 end
 saveplot(f,outputDir,sprintf('image_%d',m));
 f=figure('Visible','off','Color','w','Position',[20 20 1200 470]);
 subplot(1,2,1);stairs(0:T,values(:,8),'LineWidth',1.6);hold on;plot(0:11:T,values(1:11:end,8),'o','MarkerFaceColor',[.1 .4 .7]);
 xticks(0:11:T);grid on;ylim([0 4.2]);xlabel('Adim t');ylabel('Proje U (bit)');title('Kararlarda azalan secenek entropisi');
 subplot(1,2,2);plot(0:T,values(:,5),'LineWidth',1.3);hold on;plot(0:T,values(:,7),'LineWidth',1.3);
 plot(0:11:T,values(1:11:end,5),'ko','MarkerFaceColor','w');xticks(0:11:T);ylim([0 1.05]);grid on;
 xlabel('Adim t');ylabel('bit/hucre');title('Satir ve korunmus tarihce');legend('Satir H1','Tarihce H1','Gereksinim seviyesi','Location','best');
 saveplot(f,outputDir,sprintf('entropy_%d',m));
 summary(m,:)=[m values(1:11:end,8)'];
end
writetable(array2table(summary,'VariableNames',{'Method','L1','L2','L3','L4','L5','L6'}),fullfile(outputDir,'level_summary.csv'));
fprintf('SIX LEVELS COMPLETE: 5 methods, 280 rows, 25 decision gates.\n');
end
function [p,open]=distribution(m,g,bits,target,rank)
match=bsxfun(@eq,bits,target);p=ones(16,1);
if m==1
 if g==1,p=.8.^match(:,1).*.2.^(1-match(:,1));
 elseif g>=2,p=double(all(match(:,1:g-1),2));end
elseif m==2
 if g==1,p=.8.^sum(match(:,1:2),2).*.2.^(2-sum(match(:,1:2),2));
 elseif g>=2
  p=double(all(match(:,1:2),2));
  if g==3,p=p.*(.8.^match(:,3).*.2.^(1-match(:,3)));end
  if g>=4,p=p.*double(match(:,3));end
  if g==5,p=p.*double(match(:,4));end
 end
elseif m==3
 if g>=1,p=.8.^match(:,1).*.2.^(1-match(:,1));end
 if g>=2,p=p.*double(bits(:,2)==1-bits(:,1));end
 if g>=3,p=p.*double(bits(:,3)==bits(:,1));end
 if g>=4,p=p.*double(match(:,1));end
 if g==5,p=p.*double(match(:,4));end
elseif m==4
 if g<5,q=4^g/(1+4^g);s=sum(match,2);p=q.^s.*(1-q).^(4-s);
 else,p=double(all(match,2));end
else
 sizes=[16 12 8 4 2 1];p=double(ismember((0:15)',rank(1:sizes(g+1))));
end
assert(sum(p)>0);p=p/sum(p);active=any(bsxfun(@ne,bits(p>0,:),bits(find(p>0,1),:)),1);open=sum(active);
end
function h=binaryH(q)
if q==0 || q==1,h=0;else,h=-q*log2(q)-(1-q)*log2(1-q);end
end
function saveplot(f,folder,name)
set(f,'PaperPositionMode','auto');print(f,fullfile(folder,[name '.png']),'-dpng','-r180');savefig(f,fullfile(folder,[name '.fig']));close(f);
end
