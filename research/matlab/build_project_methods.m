function build_project_methods(outputDir)
% Five illustrative project decision processes; not measured project data.
if nargin<1,outputDir=fullfile(fileparts(mfilename('fullpath')),'project_report','assets');end
if ~exist(outputDir,'dir'),mkdir(outputDir);end
seed=[0 1 1 1 0 1 0 0 0]; T=24; W=57; target=[1 0 1 1];
ruleSets=[90 150 232 204;30 90 184 232;150 232 204 204;30 110 90 204;110 30 184 204];
bits=dec2bin(0:15,4)-'0'; ranking=[11 10 3 15 9 7 2 14 1 13 8 6 5 0 12 4];
summary=zeros(5,5);
for method=1:5
 X=false(25,W);tags=zeros(25,W,'uint8');domain=false(25,W);
 X(1,25:33)=seed;domain(1,25:33)=true; tags(1,24+find(seed))=uint8([1 2 4 8]);
 values=zeros(25,12);states=zeros(25,16); previousOpen=15;
 for t=0:T
  [p,open]=posterior(method,t,bits,target,ranking); states(t+1,:)=p';
  active=find(any(bsxfun(@ne,bits(p>0,:),bits(find(p>0,1),:)),1));
  assert(numel(active)==sum(bitget(uint8(open),1:4)));
  if t>0
   rule=ruleSets(method,min(4,ceil(t/6)));old=X(t,:);ot=tags(t,:);
   left=[false old(1:end-1)];right=[old(2:end) false];idx=4*double(left)+2*double(old)+double(right);
   raw=logical(bitget(uint16(rule),idx+1));
   propagated=bitor(bitor([uint8(0) ot(1:end-1)],ot),[ot(2:end) uint8(0)]);
   newTags=bitand(propagated,uint8(open));
   X(t+1,:)=raw & newTags>0; tags(t+1,:)=newTags;tags(t+1,~X(t+1,:))=0;
   domain(t+1,25-t:33+t)=true;
   removed=sum(raw(domain(t+1,:)) & ~X(t+1,domain(t+1,:)));
  else,rule=0;removed=0;end
  row=X(t+1,domain(t+1,:));mask=domain(1:t+1,:);im=X(1:t+1,:);
  U=-sum(p(p>0).*log2(p(p>0)));verified=4*(t==24);
  values(t+1,:)=[t rule numel(row) sum(row) pattern_entropy(row,1) pattern_entropy(row,2) ...
   pattern_entropy(im(mask)',1) U sum(p>0) sum(bitget(uint8(open),1:4)) verified removed];
  previousOpen=open;
 end
 assert(values(end,4)==0 && values(end,8)==0 && values(end,9)==1 && values(end,10)==0 && values(end,11)==4);
 stats=array2table(values,'VariableNames',{'Step','Rule','Width','Ones','H1','H2','HistoryH1','ProjectU','Candidates','OpenTopics','Verified','ProjectedCells'});
 stats.RowBits=cell(25,1);for k=1:25,stats.RowBits{k}=sprintf('%d',X(k,domain(k,:)));end
 writetable(stats,fullfile(outputDir,sprintf('method_%d.csv',method)));
 writetable(array2table(states,'VariableNames',arrayfun(@(j)sprintf('C%d',j),0:15,'UniformOutput',false)),fullfile(outputDir,sprintf('posterior_%d.csv',method)));
 f=figure('Visible','off','Color','w','Position',[30 30 1250 600]);
 subplot(1,3,1);gray=ones(size(X));gray(X)=0;gray(~domain)=.88;
 image(-28:28,[0 T],repmat(gray,[1 1 3]));axis tight;set(gca,'YDir','reverse');hold on;
 for gate=[6 12 18 24],plot([-28 28],[gate gate],'Color',[.8 .25 .1],'LineStyle',':');end
 xlabel('Hucre konumu');ylabel('Proje adimi');title('Kararlarla guncellenen resim');
 subplot(1,3,2);plot(0:T,values(:,8),'-o','LineWidth',1.5,'MarkerSize',3);hold on;
 plot(0:T,values(:,10),'--','LineWidth',1.4);ylim([0 4.2]);grid on;
 xlabel('Proje adimi');ylabel('bit / acik konu sayisi');legend('Proje U (bit)','Acik konu (adet)','Location','best');title('Karar kaydindan hesap');
 subplot(1,3,3);plot(0:T,values(:,5),'LineWidth',1.4);hold on;
 plot(0:T,values(:,7),'LineWidth',1.4);ylim([0 1.05]);grid on;
 xlabel('Proje adimi');ylabel('bit/hucre');legend('Guncel satir H1','Tarihce H1','Location','best');title('Guncel durum ve tarihce');
 set(f,'PaperPositionMode','auto');print(f,fullfile(outputDir,sprintf('method_%d.png',method)),'-dpng','-r180');savefig(f,fullfile(outputDir,sprintf('method_%d.fig',method)));close(f);
 summary(method,:)=[method values(end,[8 10 5 7])];
end
writematrix_compat(summary,fullfile(outputDir,'summary.csv'));
fprintf('FIVE PROJECT METHODS COMPLETE: %s\n',outputDir);
end
function [p,open]=posterior(m,t,bits,target,ranking)
 keep=true(16,1);p=ones(16,1)/16;
 if m==1
  n=floor(t/6);if n>0,keep=all(bsxfun(@eq,bits(:,1:n),target(1:n)),2);end
 elseif m==2
  n=2*(t>=12)+2*(t>=24);if n>0,keep=all(bsxfun(@eq,bits(:,1:n),target(1:n)),2);end
 elseif m==3
  if t>=6,keep=keep & bits(:,1)==1;end
  if t>=12,keep=keep & bits(:,2)==1-bits(:,1) & bits(:,3)==bits(:,1);end
  if t>=24,keep=keep & bits(:,4)==1;end
 elseif m==4
  n=min(3,floor(t/6));q=4^n/(1+4^n);match=sum(bsxfun(@eq,bits,target),2);
  p=q.^match.*(1-q).^(4-match);
  if t<24,open=15;return;end
  keep=all(bsxfun(@eq,bits,target),2);
 else
  n=16/2^floor(t/6);keep=ismember((0:15)',ranking(1:n));
 end
 p=double(keep)/sum(keep);active=any(bsxfun(@ne,bits(keep,:),bits(find(keep,1),:)),1);
 open=sum(2.^(find(active)-1));
end
function writematrix_compat(x,path)
writetable(array2table(x,'VariableNames',{'Method','FinalU','FinalOpen','FinalH1','HistoryH1'}),path);
end
