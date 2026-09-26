function build_ten_rules(outputDir)
% Ten rules, identical seed/window; MATLAB R2018b, no toolbox.
if nargin<1, outputDir=fullfile(fileparts(mfilename('fullpath')),'report','assets10'); end
if ~exist(outputDir,'dir'), mkdir(outputDir); end
seed=[0 1 1 1 0 1 0 0 0]; T=24;
rules=[0 4 204 170 232 184 90 150 30 110];
for rule=rules
    r=expand_requirement(seed,rule,T); values=zeros(T+1,13); rowBits=cell(T+1,1);
    for k=1:T+1
        row=r.bits(k,r.domain(k,:)); n=numel(row); b=sum(row);
        [h2,~,c]=pattern_entropy(row,2);
        mask=r.domain(1:k,:); img=r.bits(1:k,:);
        fixed=r.bits(k,abs(r.x)<=4);
        values(k,:)=[k-1 n b pattern_entropy(row,1) h2 sum(mask(:)) ...
            sum(img(mask)) pattern_entropy(img(mask)',1) pattern_entropy(fixed,1) c];
        rowBits{k}=sprintf('%d',row);
    end
    stats=array2table(values,'VariableNames',{'Step','Width','Ones','H1','H2',...
        'Area','TotalOnes','ImageH1','FixedH1','C00','C01','C10','C11'});
    stats.RowBits=rowBits;
    writetable(stats,fullfile(outputDir,sprintf('rule_%03d.csv',rule)));
    f=figure('Visible','off','Color','w','Position',[30 30 1250 470]);
    subplot(1,3,1); gray=ones(size(r.bits));gray(r.bits)=0;gray(~r.domain)=.88;
    image(r.x,[0 T],repmat(gray,[1 1 3])); axis tight;set(gca,'YDir','reverse');
    xlabel('Hucre konumu');ylabel('Adim t');title(sprintf('Kural %d: buyuyen resim',rule));
    subplot(1,3,2);plot(values(:,1),values(:,4),'LineWidth',1.5);hold on;
    plot(values(:,1),values(:,8),'LineWidth',1.5);plot(values(:,1),values(:,9),'--','LineWidth',1.3);
    ylim([0 1.05]);grid on;xlabel('Adim t');ylabel('bit/hucre');title('Tekli desen entropileri');
    legend('Satir','Birikmis resim','Sabit 9 hucre','Location','best');
    subplot(1,3,3);plot(values(:,1),values(:,5),'-o','LineWidth',1.4,'MarkerSize',3);
    ylim([0 2.05]);grid on;xlabel('Adim t');ylabel('bit/cift');title('Satir H2');
    set(f,'PaperPositionMode','auto');
    print(f,fullfile(outputDir,sprintf('rule_%03d.png',rule)),'-dpng','-r180');
    savefig(f,fullfile(outputDir,sprintf('rule_%03d.fig',rule)));close(f);
end
fprintf('TEN RULES COMPLETE: %s\n',outputDir);
end
