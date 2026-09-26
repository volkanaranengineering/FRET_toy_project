function results = run_requirement_demo(outputDir)
%RUN_REQUIREMENT_DEMO Generate Wolfram-style requirement pictures in MATLAB.
% Compatible with MATLAB R2018b; no add-on toolboxes, no random sampling.
if nargin<1, outputDir=fullfile(fileparts(mfilename('fullpath')),'outputs'); end
if ~exist(outputDir,'dir'), mkdir(outputDir); end
test_requirement_ca;
% Illustrative annotation of nine phrases, NOT recovered from omitted image.
seed=[0 0 1 0 1 1 0 0 1]; steps=80;
rules=[90 30 110 204]; results=cell(1,numel(rules));
f=newFigure('Ayni gereksinim farkli algilayicilar',1300,850);
for j=1:numel(rules)
    results{j}=expand_requirement(seed,rules(j),steps);
    subplot(2,2,j); drawCA(results{j});
    title(sprintf('Algilayici kurali %d | ayni 9 bit',rules(j)));
    M=measure_expansion(results{j});
    writetable(M,fullfile(outputDir,sprintf('metrics_rule_%d.csv',rules(j))));
    imwrite(caRGB(results{j}.bits,results{j}.domain),...
        fullfile(outputDir,sprintf('raw_rule_%d.png',rules(j))));
end
savePlot(f,outputDir,'01_observers');

f=newFigure('Kural 90 klasik ve gereksinim tohumu',1200,650);
subplot(1,2,1); drawCA(expand_requirement(1,90,steps)); title('Tek siyah hucre | Kural 90');
subplot(1,2,2); drawCA(results{1}); title('Dokuz parcali gereksinim | Kural 90');
savePlot(f,outputDir,'02_rule90');

f=newFigure('Satir desen entropisi',1250,800);
for j=1:4
    M=measure_expansion(results{j}); subplot(2,2,j);
    plot(M.Step,M.H1_bits,'LineWidth',1.3); hold on;
    plot(M.Step,M.H2_bits_per_pair/2,'LineWidth',1.2);
    plot(M.Step,M.FixedH1_bits,'--','LineWidth',1.2);
    ylim([0 1.05]); grid on; xlabel('Isleme adimi'); ylabel('Desen istatistigi (bit/hucre)');
    title(sprintf('Kural %d | pencere etkisi',rules(j)));
    legend('H1 buyuyen pencere','H2 / 2 buyuyen pencere','H1 sabit 9 hucre','Location','best');
end
savePlot(f,outputDir,'03_entropy');

f=newFigure('Ayni evrim farkli gozlem cozunurlugu',1250,650);
for j=1:3
    b=[1 3 9]; [img,mask]=observe_expansion(results{2},b(j));
    subplot(1,3,j); image(caRGB(img,mask)); axis tight; set(gca,'YDir','reverse');
    xlabel('Gozlenen blok'); ylabel('Isleme adimi + 1');
    title(sprintf('Kural 30 | blok genisligi %d',b(j)));
end
savePlot(f,outputDir,'04_observation');

projected=expand_requirement(seed,90,steps,'DecisionStep',28,'DecisionHalfWidth',32);
f=newFigure('Tasarim karari acik bir mudahaledir',1300,750);
subplot(2,2,1); drawCA(results{1}); title('Serbest Kural 90 evrimi');
subplot(2,2,2); drawCA(projected); title('28. adimdan sonra daralan izinli bolge');
hold on; plot([projected.x(1) projected.x(end)],[28 28],'r--','LineWidth',1.2);
subplot(2,2,[3 4]); A=measure_expansion(results{1}); B=measure_expansion(projected);
plot(A.Step,A.H1_bits,'LineWidth',1.4); hold on;
plot(B.Step,B.H1_bits,'LineWidth',1.4); grid on; ylim([0 1.05]);
xlabel('Isleme adimi'); ylabel('H1 (bit/hucre)');
legend('Serbest','Disaridan sifira sabitleme','Location','best');
title('Ayni buyuyen pencerede olcum | daralma mekanizmasi varsayimdir');
savePlot(f,outputDir,'05_design_intervention');
writetable(B,fullfile(outputDir,'metrics_projection.csv'));

schedule=[repmat(90,1,25) repmat(30,1,25) repmat(110,1,30)];
handoff=expand_requirement(seed,schedule,steps);
f=newFigure('Gereksinimin kisiden kisiye aktarimi',900,650);
drawCA(handoff); hold on;
plot([handoff.x(1) handoff.x(end)],[25 25],'r--');
plot([handoff.x(1) handoff.x(end)],[50 50],'r--');
title('Ayni satirin devri: 90 -> 30 -> 110 | kurallar deney parametresi');
savePlot(f,outputDir,'06_handoffs');

% Hypotheses are explicit rule identities, not black cells or semantic designs.
candidates=[18 22 30 54 90 110 150 204]; ensemble=cell(size(candidates));
for j=1:numel(candidates), ensemble{j}=expand_requirement(seed,candidates(j),steps); end
truth=expand_requirement(seed,90,steps); alive=true(size(candidates));
probeSteps=[0 1 2 4 8 16 32]; remaining=zeros(size(probeSteps));
for k=1:numel(probeSteps)
    t=probeSteps(k); cols=abs(truth.x)<=1;
    for j=find(alive)
        alive(j)=isequal(ensemble{j}.bits(t+1,cols),truth.bits(t+1,cols));
    end
    remaining(k)=sum(alive);
end
T=table(probeSteps',remaining',log2(remaining'),...
    'VariableNames',{'ObservationStep','CompatibleRules','RuleHypothesisEntropy_bits'});
writetable(T,fullfile(outputDir,'rule_hypotheses.csv'));
f=newFigure('Acik alternatif kumesinin elenmesi',900,500);
stairs(probeSteps,log2(remaining),'-o','LineWidth',1.8); grid on;
xlabel('Gozlem adimi (uc merkez hucre)'); ylabel('Kural hipotezi entropisi (bit)');
title('8 es olasilikli kural hipotezi | piksel entropisinden farkli');
savePlot(f,outputDir,'07_hypothesis_selection');
assert(remaining(end)>=1 && all(diff(remaining)<=0));
save(fullfile(outputDir,'simulation_data.mat'),'seed','steps','rules','results',...
    'projected','handoff','candidates','T');
fprintf('DONE: images, figures, metrics and MAT data in %s\n',outputDir);
end

function f=newFigure(name,w,h)
f=figure('Name',name,'Color','w','Visible','off','Position',[50 50 w h]);
end
function drawCA(r)
image(r.x,[0 r.steps],caRGB(r.bits,r.domain));
axis tight; set(gca,'YDir','reverse'); xlabel('Hucre konumu'); ylabel('Isleme adimi');
end
function rgb=caRGB(bits,mask)
gray=ones(size(bits)); gray(bits)=0; gray(~mask)=.88;
rgb=repmat(gray,[1 1 3]);
end
function savePlot(f,folder,name)
set(f,'PaperPositionMode','auto');
print(f,fullfile(folder,[name '.png']),'-dpng','-r140');
savefig(f,fullfile(folder,[name '.fig'])); close(f);
end
