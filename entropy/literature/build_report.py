"""Build the critical literature review PDF, Markdown, evidence ledger and BibTeX.
Requires reportlab and pypdf. No network calls; source evidence was reviewed separately.
"""
from pathlib import Path
import json, re, math
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATE = '27 September 2026'
PAPERS = []
def paper(id, authors, year, title, venue, doi, access, url, support, counter, implication):
    PAPERS.append(dict(id=id, authors=authors, year=year, title=title, venue=venue, doi=doi,
                       access=access, primary_url=url, support=support, counter=counter,
                       implication=implication, publication_type='journal' if id.startswith('J') else 'conference'))

paper('J01','Gneiting, T.; Raftery, A. E.',2007,'Strictly Proper Scoring Rules, Prediction, and Estimation',
 'Journal of the American Statistical Association 102(477), 359-378','10.1198/016214506000001437','Abstract and metadata',
 'https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf',
 'Proper scoring rules provide an established way to evaluate probability forecasts.',
 'Low entropy is not a score for predictive correctness; a concentrated belief can be wrong.',
 'Evaluate interpretation probabilities using held-out outcomes and proper scores, alongside calibration plots. Do not validate probabilities by showing that entropy decreases.')
paper('J02','Bauer, A.; Leucker, M.; Schallhart, C.',2011,'Runtime verification for LTL and TLTL',
 'ACM Transactions on Software Engineering and Methodology 20(4), Article 14','10.1145/2000799.2000800','Abstract and metadata',
 'https://research.uni-luebeck.de/de/publications/runtime-verification-for-ltl-and-tltl/',
 'Runtime verification makes the treatment of finite observations explicit, including inconclusive observations.',
 'A finite prefix with an unfinished obligation need not provide the same evidence as a completed satisfying execution.',
 'State whether traces are complete finite executions or prefixes. Compare the existing weak-boundary acceptance with a separately specified monitoring interpretation; do not call the existing FRET semantics incorrect.')
paper('J03','Grenn, M. W.; Sarkani, S.; Mazzuchi, T. A.',2014,'The Requirements Entropy Framework in Systems Engineering',
 'Systems Engineering 17(4), 462-478','10.1111/sys.21283','Abstract and metadata',
 'https://incose.onlinelibrary.wiley.com/doi/abs/10.1111/sys.21283',
 'Entropy has already been applied to requirements populations and their quality-state evolution in systems engineering.',
 'The broad claim that requirements entropy is new is untenable. Its random variable differs from a distribution over formal meanings.',
 'Position this study as a specific formal-semantics and clarification investigation. Explain why its entropy cannot be compared numerically with a requirements-quality-state entropy.')
paper('J04','Kuhn, T.',2014,'A Survey and Classification of Controlled Natural Languages',
 'Computational Linguistics 40(1), 121-170','10.1162/COLI_a_00168','Abstract and metadata',
 'https://aclanthology.org/J14-1005/',
 'Controlled languages offer a mature foundation for balancing natural-language accessibility and formal precision.',
 'Restricted syntax and formal precision do not establish that the selected sentence captures a stakeholder intention.',
 'Separate grammatical well-formedness, semantic interpretation and validated intent in the user interface and study outcomes.')
paper('J05','Autili, M.; Grunske, L.; Lumpe, M.; Pelliccione, P.; Tang, A.',2015,
 'Aligning Qualitative, Real-Time, and Probabilistic Property Specification Patterns Using a Structured English Grammar',
 'IEEE Transactions on Software Engineering 41(7), 620-638','10.1109/TSE.2015.2398877','Author project description and institutional metadata',
 'https://ps-patterns.wikidot.com/',
 'A structured English grammar can connect qualitative, timed and probabilistic specification patterns.',
 'Pattern-based formalization is established; probability inside a system property is different from uncertainty about which property a person intends.',
 'Keep operational probabilities and analyst interpretation probabilities separate. Use a varied pattern benchmark rather than only two response examples.')
paper('J06','Ferrari, A.; Esuli, A.',2019,'An NLP approach for cross-domain ambiguity detection in requirements engineering',
 'Automated Software Engineering 26(3), 559-598','10.1007/s10515-019-00261-7','Abstract and metadata',
 'https://link.springer.com/article/10.1007/s10515-019-00261-7',
 'Domain-dependent language models support detecting terms whose interpretations may differ across stakeholder domains.',
 'Formal candidate enumeration alone does not capture all contextual or terminological ambiguity.',
 'Include domain experts and an NLP ambiguity baseline. Record omitted interpretations instead of treating a small generated candidate set as proof of low ambiguity.')
paper('J07','Cavezza, D. G.; Alrajeh, D.; Gyorgy, A.',2021,'A Weakness Measure for GR(1) Formulae',
 'Formal Aspects of Computing 33, 27-63; online 2020','10.1007/s00165-020-00519-y','Abstract and metadata',
 'https://link.springer.com/article/10.1007/s00165-020-00519-y',
 'Quantitative logical weakness has a formal literature connecting entropy, language properties and specification refinement.',
 'Entropy alone can be insufficient for distinctions involving fairness; this work uses additional structure including Hausdorff dimension. Its infinite-language setting differs from this prototype.',
 'Do not rename a bounded log model count as a general logical-weakness measure. Test implication, horizon sensitivity and fairness-related limitations separately.')
paper('J08','Giannakopoulou, D.; Pressburger, T.; Mavridou, A.; Schumann, J.',2021,
 'Automated formalization of structured natural language requirements',
 'Information and Software Technology 137, 106590','10.1016/j.infsof.2021.106590','Abstract and selected introductory material',
 'https://www.sciencedirect.com/science/article/pii/S0950584921000707',
 'FRET supplies the structured-language formalization foundation and compositional temporal semantics used by the prototype.',
 'Correct translation is a different claim from correct elicitation of intent. The compiler and formalization are prior work.',
 'Attribute FRET explicitly, retain compiler provenance and describe entropy analysis as a companion extension rather than a replacement formalization method.')
paper('J09','Zhao, L., et al.',2021,'Natural Language Processing for Requirements Engineering: A Systematic Mapping Study',
 'ACM Computing Surveys 54(3), 1-41; online 2021, issue 2022','10.1145/3444689','Publisher metadata and selected record material',
 'https://doi.org/10.1145/3444689',
 'The mapping study locates requirements-language processing within a substantial prior research landscape.',
 'A toy demonstration cannot establish an advantage over the wider NLP-for-requirements literature.',
 'Use this survey for backward and forward citation expansion before a submission. This review does not extract numerical effectiveness conclusions from the limited publisher material inspected.')
paper('J10','Hullermeier, E.; Waegeman, W.',2021,'Aleatoric and epistemic uncertainty in machine learning: an introduction to concepts and methods',
 'Machine Learning 110, 457-506','10.1007/s10994-021-05946-3','Abstract and selected conceptual sections',
 'https://link.springer.com/article/10.1007/s10994-021-05946-3',
 'The distinction between variability and lack of knowledge helps define what a reported uncertainty number represents.',
 'A single entropy value does not automatically isolate epistemic uncertainty or capture model-set incompleteness.',
 'Document the uncertain object, probability source and omitted possibilities. Application to requirements elicitation is an inference from this conceptual literature, not an evaluated result of that paper.')
paper('J11','Montgomery, L.; Fucci, D.; Bouraffa, A.; Scholz, L.; Maalej, W.',2022,
 'Empirical research on requirements quality: a systematic mapping study',
 'Requirements Engineering 27(2), 183-209','10.1007/s00766-021-00367-z','Abstract and selected full-text sections',
 'https://link.springer.com/article/10.1007/s00766-021-00367-z',
 'The mapping study motivates explicit definitions and empirical evaluation of requirements-quality constructs.',
 'Ambiguity, consistency, completeness and correctness are distinct. An easily computed scalar is not automatically a validated quality measure.',
 'Define an independently judged outcome for each claim. Evaluate whether the entropy measures add information beyond existing defect and quality assessments.')
paper('J12','Nguyen, V.-L.; Shaker, M. H.; Hullermeier, E.',2022,
 'How to measure uncertainty in uncertainty sampling for active learning',
 'Machine Learning 111(1), 89-122; online 2021','10.1007/s10994-021-06003-9','Abstract and institutional metadata',
 'https://epub.ub.uni-muenchen.de/91888/',
 'Active-learning research studies the consequences of different uncertainty measures for selecting informative observations.',
 'Uncertainty sampling and expected information gain are not interchangeable; the best measure depends on assumptions and the task.',
 'Compare candidate-selection strategies under answer noise. Do not cite this paper as direct evidence that entropy-ranked FRET questions outperform simpler questions.')
paper('J13','Farquhar, S.; Kossen, J.; Kuhn, L.; Gal, Y.',2024,
 'Detecting hallucinations in large language models using semantic entropy',
 'Nature 630, 625-630','10.1038/s41586-024-07421-0','Abstract and selected methods material',
 'https://www.nature.com/articles/s41586-024-07421-0',
 'Grouping outputs by meaning before measuring uncertainty is established in semantic-entropy research.',
 'The original setting concerns LLM outputs and particular errors, not stakeholder intention. Semantic entropy itself is not a new contribution here.',
 'Study exact bounded formal equivalence, alias-mass conservation and probability calibration as requirements-specific questions. Do not interpret LLM frequency as an automatically valid intent prior.')
paper('J14','Rainforth, T.; Foster, A.; Ivanova, D. R.; Bickford Smith, F.',2024,
 'Modern Bayesian Experimental Design',
 'Statistical Science 39(1), 100-114','10.1214/23-STS915','Abstract and metadata',
 'https://doi.org/10.1214/23-STS915',
 'Expected information gain is a standard objective for selecting experiments that reduce uncertainty.',
 'Applying this objective to questions is not, by itself, a new information-theoretic method.',
 'Specify priors, answer likelihoods, question costs and decision objectives. A defensible contribution must show a useful requirements-specific method or evaluated benefit beyond this established foundation.')
paper('J15','Abualhaija, S.; Aydemir, F. B.; Dalpiaz, F.; Dell\'Anna, D.; Ferrari, A.; Franch, X.; Fucci, D.',2024,
 'Replication in Requirements Engineering: The NLP for RE Case',
 'ACM Transactions on Software Engineering and Methodology 33(6), Article 151, 1-33','10.1145/3658669','Abstract and selected publisher material',
 'https://doi.org/10.1145/3658669',
 'Replication and verifiability require sufficient information about data, annotation and tool reconstruction.',
 'A runnable script is useful but does not make an empirical result independently reproducible without the associated protocol and evidence.',
 'Release candidate-generation settings, priors, annotation guidance, anonymized answer records where permitted, exclusions and analysis scripts; retain compiler and dataset versions.')
paper('J16','Henkel, E.; Hauff, N.; Langenfeld, V.; Funk, L.; Podelski, A.',2025,
 'Is it vacuous to check redundancy, or is it redundant to check vacuity?',
 'Requirements Engineering 30, 173-194','10.1007/s00766-025-00438-5','Abstract and selected full-text sections',
 'https://link.springer.com/article/10.1007/s00766-025-00438-5',
 'Formal analysis of real-time requirements already addresses redundancy and its relationship with vacuity.',
 'A zero marginal trace-count restriction can rediscover bounded redundancy. It does not establish every form of vacuity or unbounded redundancy.',
 'Compare quantitative marginal restriction with established logical checks, and label each result by horizon and environment assumptions.')
paper('J17','Darif, I.; El Boussaidi, G.; Kpodjedo, S.; Politowski, C.',2026,
 'Controlled Natural Language for Requirements Specification: A Systematic Literature Review',
 'ACM Computing Surveys 58(7), Article 175, 36 pages; published January 2026','10.1145/3778169','Institutional abstract and metadata',
 'https://pure.etsmtl.ca/en/publications/controlled-natural-language-for-requirements-specification-a-syst/',
 'A recent review identifies continuing limitations in controlled-language tooling and case-study validation.',
 'CNL-based requirements support is an established field; a new interface alone does not resolve its adoption or validation problems.',
 'Prioritize evaluation with real users, domain vocabulary and realistic workflows. Avoid interpreting limitations reported in a review as a claim that no successful tools or studies exist.')
paper('J18','Luckcuck, M.; Sheridan, O.; Farrell, M.; Monahan, R.',2026,
 'Mu-FRET: a catalogue and tool for requirement refactoring',
 'Software and Systems Modeling; online 18 May 2026','10.1007/s10270-025-01355-5','Abstract and selected full-text sections',
 'https://link.springer.com/article/10.1007/s10270-025-01355-5',
 'Mu-FRET demonstrates semantics-preserving refactoring and formal equivalence in a FRET-related workflow.',
 'Formal comparison of FRET requirements and meaningful tool extensions already exist. Bounded equivalence grouping is not the first semantics-aware FRET extension.',
 'Separate changes of wording that preserve meaning from genuinely different candidate meanings; compare grouping against a suitable equivalence baseline.')
paper('S01','Mendoza, D.; Mavridou, A.; Katis, A.; Trippel, C.',2026,
 'Automating Requirements Formalization: Using LLMs and Low-Complexity Distinguishing Traces for Semantic Validation',
 'ICSE 2026, 13 pages (conference; outside journal corpus)','10.1145/3744916.3787815','Abstract, method and evaluation section 7.3',
 'https://cs.stanford.edu/people/trippel/pubs/mendoza_ICSE26.pdf',
 'ARTEMIS combines structured-language candidates, including FRETish, with low-complexity and balanced distinguishing traces.',
 'It directly challenges novelty claims for trace-based FRET clarification. Section 7.3 uses an expert specification to answer traces and ensures a plausible candidate is present; effort includes trace-complexity proxies.',
 'Use it as a mandatory comparator. Measure actual human accuracy and time, candidate omissions and noisy answers. Do not present the current EIG implementation as the first balanced-trace FRET method.')

PAGES = []
def page(title, subtitle, blocks):
    PAGES.append((title, subtitle, blocks))

page('FRET requirement entropy', 'Critical literature survey and research-gap report | '+DATE, [
 ('Lead finding', 'The three implemented ideas are mathematically useful demonstrations, but their underlying concepts are established. A journal contribution should investigate reliable intent elicitation under imperfect candidate coverage, uncertain answers and explicit finite-trace assumptions, with independently measured human outcomes.'),
 ('Scope', 'This structured critical review covers journal publications within 27 September 2006 to 27 September 2026. The selected corpus contains 18 journal papers, published from 2007 to 2026, plus one separately labelled 2026 conference paper because it directly affects novelty. It is a scoped survey, not an exhaustive systematic review or meta-analysis.'),
 ('Most consequential counter-evidence', 'ARTEMIS [S01] already overlaps directly with the clarification direction. Treating information gain as a replacement name for balanced splitting would not establish novelty. The proposed extension must justify its additional assumptions and demonstrate an advantage against this prior method.'),
 ('Deliverables and evidence', 'The report includes an annotated evidence matrix, separate supporting and challenging interpretations, research questions, falsifiable hypotheses, a comparison protocol and a staged research plan. DOI links and access-depth notes are provided for every paper. Supporting means methodological relevance, not proof that this prototype works; counter means a challenge to novelty, assumptions or validity, not a direct refutation of this implementation.'),
 ('Project baseline', 'Repository: volkanaranengineering/FRET_toy_project. Implementation baseline: 6443ce8; tutorial baseline: 16a78ad. The survey assesses the three separate entropy modules applied to the two setup request-response examples. No human experiment was conducted for this report.')])

page('1. Review method and boundaries','What was searched, selected and actually inspected',[
 ('Search procedure', 'Targeted web searches combined FRET, FRETish, requirements entropy, semantic entropy, logical weakness, temporal-logic model counting, ambiguity, active clarification, Bayesian experimental design, controlled natural language, requirements quality and replication. Publisher, author and institutional records were preferred; relevant references and the FRET publication landscape guided follow-up searches. The accompanying search_log.md records representative queries, not an invented exhaustive database export.'),
 ('Eligibility', 'Include journal work in the stated time window when it informs at least one implemented measure, the validity of its assumptions, or a plausible evaluation baseline. Include methodological papers outside requirements engineering only when the transfer is explained. Keep conference proceedings, preprints and older foundational work outside the journal count. S01 is an explicit exception in a supplementary comparison, not a nineteenth journal article.'),
 ('Extraction', 'For each item record title, authors as available, year, venue, DOI, primary source, access depth, supporting contribution, challenge and study implication. Dates follow the journal publication record, distinguishing online and issue dates where relevant; a DOI containing an earlier year is not treated as the publication year. J09 uses an abbreviated author list rather than an unverified expansion.'),
 ('Evidence strength', 'Access depth ranges from abstract/metadata to selected full-text sections. The annotations state this openly; they do not imply every paper was read end-to-end. Abstract-level evidence supports conceptual positioning but is insufficient for detailed claims about effect sizes or experimental quality. No pooled effect sizes, study-quality score or inter-reviewer agreement is reported.'),
 ('Limitations', 'Selection was performed in one assisted review workflow without independent duplicate screening, subscription-database exports or a PRISMA flow. Search-engine coverage, access restrictions and relevance judgement may omit important papers, including very recent publications. The gap is therefore a gap in the reviewed corpus, not proof of worldwide absence. Before journal submission, expand through Scopus/Web of Science/IEEE/ACM where available and perform independent screening and full-text appraisal.')])

page('2. What the current implementation measures','Three different random objects; three different interpretations',[
 ('The two starting requirements', 'REQ-001: when request the ResponseSystem shall within 3 ticks satisfy response. REQ-002: whenever request the ResponseSystem shall within 3 ticks satisfy response. These are already precise FRETish sentences. Added deadline and trigger alternatives are analyst-constructed hypotheses; they are not observed stakeholder misunderstandings.'),
 ('Idea 1 - uncertainty over meanings', 'Each example has four equally weighted candidate spellings: the original, a punctuation alias, a shorter deadline and the alternative trigger. Grouping equivalent spellings at the analysed bound gives meaning masses (0.50, 0.25, 0.25). H(M) = -sum p(m) log2 p(m) = 1.5 bits, versus 2 bits over spelling labels. Keeping only the original gives zero. All priors are illustrative; bounded agreement is not unrestricted temporal equivalence.'),
 ('Idea 2 - permitted behavioral freedom', 'With two Boolean signals and six ticks, there are 2^12 = 4096 equally weighted traces. The original when requirement admits 3848; whenever admits 3784. H_B = log2 |S| gives 11.909893 and 11.885696 bits. Restriction relative to the unrestricted universe is log2(4096/|S|): 0.090107 and 0.114304 bits. This is uniform conditional trace entropy, not operational risk or a probability that a requirement is correct.'),
 ('Idea 3 - expected clarification gain', 'For a candidate-discriminating trace q, IG(q) = H(M) - sum_a P(a|q) H(M|a,q). Under deterministic reliable binary answers, the best gains are 1.000000 bit for REQ-001 and 0.811278 bit for REQ-002. Different available partitions explain the difference. These are expected model-based reductions, not measured reductions in human effort.'),
 ('What validation establishes', 'The saved validation records eight test methods and 43,680 formula-versus-independent-obligation comparisons over horizons 1 to 6. They support bounded implementation correctness. They are not 43,680 independent requirements, stakeholder observations or an external model-checking study. The prototype remains a browser companion, not a native FRET feature.')])

page('3. Supporting literature and its limits','Established foundations that make the study plausible',[
 ('Formal grounding', 'Controlled-language and pattern research supplies a rationale for a structured intermediate representation [J04, J05, J17]. FRET formalization supplies the actual semantic foundation [J08]. This supports making candidate differences inspectable and reproducible; it does not establish that the chosen candidate matches intent.'),
 ('Semantic uncertainty', 'Meaning-level grouping is supported by semantic-entropy research [J13], while the distinction between knowledge uncertainty and variability helps specify the construct [J10]. Proper scoring rules provide an evaluation foundation for probabilities [J01]. The proposed requirements-specific question is whether formally grouped, empirically estimated beliefs predict intended meanings, rather than whether Shannon entropy can be computed.'),
 ('Behavioral restriction', 'Formal weakness measures show that quantifying permitted behavior is a legitimate line of investigation [J07]. Redundancy analysis supplies a comparator for marginal contribution [J16]. The useful extension would explain when bounded trace volume provides extra diagnostic value beyond logical implication, consistency and vacuity checks.'),
 ('Clarification as experiment selection', 'Bayesian experimental design supplies the information-gain foundation [J14]; active-learning uncertainty research motivates alternative acquisition strategies and sensitivity analysis [J12]. Inference for this study: trace questions can be treated as experiments only after specifying an answer model and the object being learned. A mathematical gain does not establish that users can understand the question.'),
 ('Empirical discipline', 'Requirements-quality research and replication work motivate explicit constructs, independent outcomes and complete artifacts [J11, J15]. Domain-sensitive ambiguity detection suggests contextual candidate omissions [J06]. These connections justify a multi-domain study and a reproducible answer ledger, not a claim of effectiveness from two toy examples.')])

page('4. Counter-evidence and the novelty boundary','Why three entropy displays are not yet three journal contributions',[
 ('Existing concepts', 'Requirements entropy predates this work [J03]; semantic entropy is established [J13]; EIG is standard [J14]. Mu-FRET already demonstrates semantics-aware changes in the FRET ecosystem [J18]. The current contribution is an implementation and explanatory artifact. A stronger publication claim needs a new, validated method or empirical finding.'),
 ('Closest overlap: ARTEMIS', 'The supplementary ICSE paper [S01] is a necessary comparator even in a journal-focused review. Its existing FRETish/trace workflow substantially narrows the clarification claim. The new study should investigate candidate coverage, probability calibration and actual human outcomes rather than claim the first trace-based clarification approach. See the annotated S01 record for the inspected evaluation assumptions.'),
 ('Derived equivalence of two selection criteria', 'Let n meanings be equally likely and let q deterministically divide them into m accepting and n-m rejecting meanings. Then P(yes|q)=m/n. Because the answer is determined by the meaning, H(A|M,q)=0. Thus IG(q)=I(M;A|q)=H(A|q)=h2(m/n), where h2(x)=-x log2 x-(1-x) log2(1-x). This is maximized by the most balanced feasible partition. Under these conditions, maximizing EIG and balancing candidate counts select the same partition criterion. This derivation concerns the objective; it does not assert algorithmic equivalence or identical complexity.'),
 ('What changes with nonuniform beliefs', 'For unequal meaning masses, replace m/n by the total accepting mass. With noisy answers, IG(q)=H(A|q)-sum_m p(m)H(A|m,q), so a balanced answer distribution alone is insufficient. These standard identities identify testable modifications; neither identity is a new theorem of this project.'),
 ('What must not be claimed', 'Do not claim that zero entropy proves correct intent, that stricter requirements are better, that bounded equality proves unrestricted equivalence, or that the two default examples establish industrial usefulness. Do not describe supporting conceptual papers as direct evaluations of this prototype.')])

page('5. A defensible research gap','A scoped gap statement and three separable research questions',[
 ('Proposed gap statement', 'The reviewed literature does not establish whether a calibrated, candidate-coverage-aware and answer-noise-aware FRET clarification process improves independently judged intended-formalization accuracy per unit of human effort over balanced-trace methods, while exposing horizon and environment sensitivity. This is a proposed empirical and methodological gap, conditional on a fuller systematic search; it is not a claim that the entropy formulas are novel.'),
 ('G1 / RQ1 - interpretation validity', 'When does formally grouped entropy predict real disagreement or formalization error, and when does missing candidate coverage cause false confidence? Study alias-mass invariance, priors learned without project leakage, calibration and deliberate omission of the intended candidate. Compare uniform, expert-elicited and learned probabilities. A useful result could be a validated warning policy; a null result would show entropy adds little beyond simpler indicators.'),
 ('G2 / RQ2 - behavioral validity', 'When do bounded behavioral freedom and marginal restriction provide stable, actionable information beyond implication and redundancy checks? Vary horizon, boundary interpretation, environment constraints and trace distribution. Determine whether engineers make better defect or change-impact decisions using these quantities. A contribution would be a characterized domain of validity, including failure cases, rather than a universal requirement-quality number.'),
 ('G3 / RQ3 - clarification effectiveness', 'Does probability-weighted, noise-aware and cost-aware trace selection improve accurate completion compared with balanced trace selection and ordinary FRET review? Evaluate actual answers and elapsed effort, including uncertain and none-of-the-above responses. Count reopening and correction costs. Improvement must survive held-out projects and imperfect candidate generation.'),
 ('How to keep the ideas separate', 'Maintain three experimental modules with shared versioned inputs. RQ1 tests probability and meaning constructs; RQ2 tests behavioral analysis; RQ3 tests interaction outcomes. An integrated journal paper can connect them through a shared protocol, but three standalone papers would each need a distinct contribution and sufficient evidence; splitting the current demonstration alone would not provide that.')])

page('6. Evaluation design that could defend the gap','Proposed future work - no results are asserted here',[
 ('Data and reference interpretation', 'Use multiple independent projects and requirement patterns, including relevant reusable FRET examples where licensing permits. Preserve original natural language, elicitation context and author clarifications. Have independent domain experts specify acceptable interpretations and adjudicate disagreement while blinded to the tested method. Allow several valid meanings; do not force every requirement into a single unquestionable label. Split training and evaluation by project.'),
 ('Controlled candidate conditions', 'Create covered, partially covered and intended-meaning-absent sets. Include aliases without multiplying their prior mass, plausible distractors, deadline changes and trigger changes. Keep candidate generation fixed across selection-policy comparisons; otherwise generation improvements confound question selection. Use a separate experiment to compare generators. Report coverage, omitted-meaning types and the fraction of cases where reference intent is genuinely unresolved.'),
 ('Comparators', 'B0: ordinary FRET review without entropy guidance. B1: random feasible distinguishing questions. B2: balanced candidate-count trace selection, reproducing ARTEMIS as faithfully as possible and labelling any simplified approximation. B3: deterministic weighted EIG. B4: noise-aware EIG with an explicit cost model. Use identical available candidates and query constraints for policy ablations. Include logical redundancy/implication checks for RQ2 and a relevant NLP ambiguity baseline for RQ1.'),
 ('Participants and assignment', 'Use actual requirements engineers or clearly identified proxies; report expertise. Randomize or counterbalance methods and task order while preventing learning from repeated identical requirements. Pilot comprehension and timing before choosing sample size. Base power or precision analysis on the primary outcome, clustering and plausible effect sizes, not an arbitrary participant count. Analyse participant and project/task dependence.'),
 ('Primary and secondary outcomes', 'Pre-register independently judged final correctness and completion time, with a prespecified rule for their tradeoff. Secondary outcomes: question count, comprehension errors, abstention, reopening, false-confidence rate, Brier/log scores for identifiable intent labels, calibration, candidate coverage, runtime and memory. Report confidence intervals and failures. Do not pool individual traces as independent human observations or optimize the primary outcome after viewing results.')])

page('7. Technical safeguards and falsifiable claims','Conditions that make a positive result credible',[
 ('Probability model', 'A prior over meanings must conserve mass when spelling aliases are split or merged. Specify how an outside-the-candidate-set possibility is represented; an unknown bucket without an answer likelihood is not a complete Bayesian model. Learn or elicit answer reliability separately, with regularization and sensitivity analysis. Never eliminate a candidate with certainty merely because a noisy response disagrees.'),
 ('Cost and decision objective', 'A practical acquisition score could be expected information gain divided by predicted answer time, but this is a heuristic, not guaranteed optimal policy. Compare it with expected decision-loss reduction when errors have unequal consequences. Entropy does not encode severity. Record how question length, number of signals and explanation format affect comprehension and cost.'),
 ('Finite-trace semantics', 'Under the present weak-deadline convention, a trigger whose deadline lies beyond the trace may remain accepted without an observed response. This can influence trace rankings and model counts. Report horizon and boundary semantics on every result. Distinguish finite-execution satisfaction from monitoring-prefix inconclusiveness [J02]; compare interpretations explicitly instead of silently changing the compiler semantics.'),
 ('Generalized behavioral measure', 'For a declared operational distribution P(T), permitted-trace entropy would be H(T | T in S), which generally differs from log2|S|. Compute acceptance probability P(T in S) separately. If S is empty, conditional entropy is undefined; inconsistency is not a zero-entropy success. Relative restriction and marginal restriction must use the same universe, assumptions and distribution. Bounded equality of accepted sets does not prove equality for all lengths.'),
 ('Hypotheses with genuine failure conditions', 'H1: grouped, calibrated beliefs improve held-out probability scores over specified simpler baselines; reject the advantage if scores do not improve. H2: behavioral measures improve prespecified engineering decisions and remain useful over the target sensitivity range; report instability if rankings reverse. H3: the extended policy improves the preregistered accuracy-effort objective over B2; a faster but less accurate outcome is not automatically a success. H4: explicit candidate-absence handling reduces false certainty without an unacceptable prespecified cost.')])

page('8. Research plan and publication positioning','Turn the demonstration into a testable study',[
 ('Stage 1 - strengthen the review', 'Retrieve full texts for abstract-only records, expand citation searches, and record independent eligibility decisions. Check for new or adjacent uncertainty-aware FRET and trace-elicitation work. Update the gap if a closer method appears. The accompanying evidence ledger is a starting extraction form, not a finished systematic-review dataset.'),
 ('Stage 2 - freeze and audit the artifact', 'Keep the existing two examples as regression fixtures. Add explicit probability provenance, candidate coverage status, boundary-semantics labels and an immutable answer ledger. Verify unsupported operators fail visibly. Cross-check selected formulas with an external formal tool when feasible. Add scalable counting only after recording its approximation error and performance limits.'),
 ('Stage 3 - run separate ablations', 'First test RQ1 calibration and alias behavior on held-out interpretations. Then test RQ2 sensitivity and redundancy comparisons. Finally pilot RQ3 with understandable traces and a fair balanced-query baseline. Freeze the protocol and analysis before the main participant study. Preserve negative cases and report when an intended meaning was unavailable.'),
 ('Stage 4 - evaluate and release', 'Publish data and anonymized observations where consent and licensing allow, plus exclusion rules, environment assumptions, generators, priors, compiler hashes and analysis scripts. Separate algorithm runtime, simulated oracle experiments and human experiments in tables. State how many independent projects, requirements and participants contributed to each estimate [J15].'),
 ('Possible paper framing', 'Working title: Calibrated and Coverage-Aware Clarification of FRET Requirements under Uncertain Human Answers. Central contribution: a reproducible method and empirical evidence about accurate intent recovery under realistic uncertainty. Supporting contributions: formal treatment of meaning classes and characterization of bounded behavioral measures. These are proposed contributions until implemented and evaluated.'),
 ('Current readiness assessment', 'Ready: reproducible small-scale calculations, separate modules, compiler provenance and explanatory class notes. Missing: representative datasets, empirically justified priors, tested candidate-absence and answer-noise models, a faithful closest-work baseline and human evidence. The present artifact can support a methods demonstration; it cannot yet support a claim of improved engineering effectiveness.')])

for start in range(0,18,3):
    blocks=[]
    for p in PAPERS[start:start+3]:
        blocks.append((p['id']+' | '+p['title'],
          f"{p['authors']} ({p['year']}). {p['venue']}. DOI: {p['doi']}.\n"
          f"SUPPORT: {p['support']}\nCHALLENGE: {p['counter']}\nSTUDY IMPLICATION: {p['implication']}\nEVIDENCE ACCESS: {p['access']}."))
    page('9. Annotated journal evidence',f"Records J{start+1:02d}-J{start+3:02d} | Support and counter-evidence are interpretive roles",blocks)
page('10. Supplementary closest-work record','Conference evidence is excluded from the 18-journal count',[
 (PAPERS[-1]['id']+' | '+PAPERS[-1]['title'],
  f"{PAPERS[-1]['authors']} (2026). {PAPERS[-1]['venue']}. DOI: {PAPERS[-1]['doi']}.\nSUPPORT: {PAPERS[-1]['support']}\nCHALLENGE: {PAPERS[-1]['counter']}\nSTUDY IMPLICATION: {PAPERS[-1]['implication']}\nEVIDENCE ACCESS: {PAPERS[-1]['access']}."),
 ('Claim-to-evidence map', 'Meaning-level uncertainty: J01, J06, J10, J13; formal-language foundations: J04, J05, J08, J17, J18; behavioral semantics and restriction: J02, J07, J16; acquisition and clarification: J12, J14, S01; quality and reproducibility: J03, J09, J11, J15. These are thematic roles, not independent positive or negative votes.'),
 ('Evidence-to-gap reasoning', 'Established components remove broad novelty claims. Differences between model confidence and correctness motivate RQ1. Dependence on semantics and trace assumptions motivates RQ2. The closest workflow overlap and the distinction between oracle simulation and human performance motivate RQ3. This synthesis is the present report\'s research proposal, not a claim made by any one cited paper.'),
 ('Excluded from the core count', 'Foundational Shannon entropy work predates the time window. Conference FRET introductions, workshop papers, unreviewed preprints and conference active-learning papers were not counted as journals. They may be useful in a future comprehensive background section. No excluded-item count is claimed because an exhaustive screening log was not produced.')])

for start in range(0,len(PAPERS),7):
    page('References and primary-source links',f'Records {start+1}-{min(start+7,len(PAPERS))} | DOI links identify publications',[
     (p['id']+' | '+str(p['year']), f"{p['authors']} {p['title']}. {p['venue']}.\nhttps://doi.org/{p['doi']}\nPrimary evidence: {p['primary_url']}") for p in PAPERS[start:start+7]])

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='ReportTitle',fontName='Times-Bold',fontSize=24,leading=28,textColor=colors.HexColor('#16374b'),spaceAfter=10))
styles.add(ParagraphStyle(name='Sub',fontName='Helvetica',fontSize=9,leading=13,textColor=colors.HexColor('#526777'),spaceAfter=19))
styles.add(ParagraphStyle(name='Label',fontName='Helvetica-Bold',fontSize=10,leading=13,textColor=colors.HexColor('#176779'),spaceBefore=11,spaceAfter=5))
styles.add(ParagraphStyle(name='Prose',fontName='Times-Roman',fontSize=10.5,leading=14.4,spaceAfter=6))
styles.add(ParagraphStyle(name='Ref',fontName='Times-Roman',fontSize=9.2,leading=12,spaceAfter=5,splitLongWords=True))

def markup(s):
    s=escape(s)
    return re.sub(r'https://[^\s]+',lambda m:'<link href="'+m.group()+'" color="#176779">'+m.group()+'</link>',s).replace('\n','<br/>')
def footer(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#c4d3dc'));canvas.line(46,43,A4[0]-46,43)
    canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#526777'))
    canvas.drawString(46,29,'FRET entropy | Critical review | 27 September 2026')
    canvas.drawRightString(A4[0]-46,29,str(doc.page))

def main():
    pdf=HERE/'FRET_Entropy_Literature_Survey.pdf'
    story=[];md=['# FRET requirement entropy: critical literature survey\n']
    for i,(title,sub,blocks) in enumerate(PAGES):
        if i:story.append(PageBreak())
        story.extend([Paragraph(markup(title),styles['ReportTitle']),Paragraph(markup(sub),styles['Sub'])])
        md.extend(['\n## '+title+'\n',sub+'\n'])
        for label,body in blocks:
            story.extend([Paragraph(markup(label),styles['Label']),Paragraph(markup(body),styles['Ref' if title.startswith('References') else 'Prose'])])
            md.extend(['\n### '+label+'\n',body+'\n'])
    SimpleDocTemplate(str(pdf),pagesize=A4,rightMargin=46,leftMargin=46,topMargin=43,bottomMargin=58,
        title='FRET requirement entropy: critical literature survey and research gap',author='Research synthesis prepared for FRET_toy_project').build(story,onFirstPage=footer,onLaterPages=footer)
    (HERE/'FRET_Entropy_Literature_Survey.md').write_text('\n'.join(md),encoding='utf-8')
    (HERE/'evidence_ledger.json').write_text(json.dumps({'review_date':'2026-09-27','window_start':'2006-09-27','window_end':'2026-09-27','review_type':'Scoped critical literature review; not exhaustive systematic review','journal_count':18,'supplementary_conference_count':1,'records':PAPERS},indent=2)+'\n',encoding='utf-8')
    bib=[]
    for p in PAPERS:
        kind='article' if p['publication_type']=='journal' else 'inproceedings'
        field='journal' if kind=='article' else 'booktitle'
        authors=p['authors'].replace('; ',' and ')
        if p['id']=='J09':authors='Zhao, Liping and others'
        bib.append('@'+kind+'{'+p['id']+',\n  author = {'+authors+'},\n  title = {{'+p['title']+'}},\n  year = {'+str(p['year'])+'},\n  '+field+' = {'+p['venue']+'},\n  doi = {'+p['doi']+'},\n  url = {https://doi.org/'+p['doi']+'}\n}')
    (HERE/'references.bib').write_text('\n\n'.join(bib)+'\n',encoding='utf-8')
    reader=PdfReader(pdf);texts=[p.extract_text() for p in reader.pages]
    assert len(texts)==len(PAGES),(len(texts),len(PAGES),'Unexpected overflow page')
    assert all(title in text for (title,_,_),text in zip(PAGES,texts))
    assert len(set(p['doi'] for p in PAPERS))==19
    assert all(p['id'] in '\n'.join(texts) for p in PAPERS)
    results={'status':'PASS','pages':len(texts),'journal_records':18,'supplementary_conference_records':1,'unique_dois':19,'checks':['Expected page boundaries and headings','All evidence IDs appear','Distinct DOI records','Journal/conference separation'],'visual_review':'Pending; inspect rendered PDF pages before delivery'}
    (HERE/'report_validation.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results))
if __name__=='__main__':main()
