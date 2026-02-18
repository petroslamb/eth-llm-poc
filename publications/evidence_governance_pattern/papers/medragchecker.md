MedRAGChecker: Claim-Level Verification for Biomedical
Retrieval-Augmented Generation

Yuelyu Ji Min Gu Kwak Hang Zhang Xizhi Wu Chenyu Li Yanshan Wang
University of Pittsburgh, Pittsburgh, PA, USA
yueluji@gmail.com

6
2
0
2

n
a
J

0
1

]
L
C
.
s
c
[

1
v
9
1
5
6
0
.
1
0
6
2
:
v
i
X
r
a

Abstract

Biomedical retrieval-augmented generation
(RAG) can ground LLM answers in med-
ical literature, yet long-form outputs often
contain isolated unsupported or contradictory
claims with safety implications. We introduce
MEDRAGCHECKER, a claim-level verification
and diagnostic framework for biomedical RAG.
Given a question, retrieved evidence, and a gen-
erated answer, MEDRAGCHECKER decom-
poses the answer into atomic claims and esti-
mates claim support by combining evidence-
grounded natural language inference (NLI)
with biomedical knowledge-graph (KG) con-
sistency signals. Aggregating claim decisions
yields answer-level diagnostics that help disen-
tangle retrieval and generation failures, includ-
ing faithfulness, under-evidence, contradiction,
and safety-critical error rates. To enable scal-
able evaluation, we distill the pipeline into com-
pact biomedical models and use an ensemble
verifier with class-specific reliability weighting.
Experiments on four biomedical QA bench-
marks show that MEDRAGCHECKER reliably
flags unsupported and contradicted claims and
reveals distinct risk profiles across generators,
particularly on safety-critical biomedical rela-
tions.

1

Introduction

Large language models (LLMs) have shown re-
markable ability in biomedical question answering,
but ungrounded generations can be dangerously
wrong. Hallucination—producing plausible but
factually incorrect statements—is a major concern
in clinical settings (Yu et al., 2025; Singhal et al.,
2025; Vladika et al., 2024; Pandit et al., 2025; Liu
and Yu, 2025). Even powerful systems such as
GPT-4.1 or Med-PaLM2 can provide unsupported
medical advice. Retrieval-augmented generation

1

Figure 1: Example of claim-level verification in biomed-
ical RAG. We decompose both the model response and
the reference answer into atomic claims. Each model
claim is labeled as ENTAIL (supported) or CONTRA-
DICT given retrieved evidence, and reference claims not
covered by the model are marked as Missing.

(RAG) partly addresses this by conditioning an-
swers on up-to-date medical literature (Achiam
et al., 2023; Tu et al., 2024; Lewis et al., 2020).
However, noisy retrieval and weak grounding still
lead to errors: when irrelevant or contradictory doc-
uments are retrieved, the model may latch onto mis-
leading snippets and hallucinate. MedTrust-RAG
(Ning et al., 2025) even shows that adding retrieved
text can flip a correct answer into an incorrect one.
Therefore, factual reliability has become a central
concern in recent LLM factuality studies (Wang
et al., 2023, 2024).

Long-form biomedical answers contain many
distinct factual claims, and whole-answer scoring
can hide isolated but clinically important mistakes.

Ground Truth ClaimsG1 (✓ Covered) "Propranolol", "is a", "non-selective beta-blocker"G2 (✓ Covered) "Non-selective beta-blockers", "can exacerbate", "bronchoconstriction in patients with asthma"G3 (✗ Contradicted) "Propranolol", "is not recommended for", "patients with asthma due to bronchospasm risk"G4 (△ Missing) "If a beta-blocker is necessary", "consider", "a cardioselective beta-1 blocker with monitoring"Claims flagged as ContradictClaims flagged as EntailMissing ClaimsClaim 1:  Propranolol is a non-selective beta-blocker.[1]Ground Truth Answer Model ResponseClaim 3:Propranolol is safe for patients with asthma when used at low doses. [3]Claim 2:Non-selective beta-blockers can exacerbate bronchoconstrictionin patients with asthma. [2]Question: Can patients with asthma safely use propranolol?Model Response Claims C1 (✓ Match GT) Propranolol is a  non-selective beta-blockerC2 (✓ Match GT) Non-selective beta-blockers", "can exacerbate", "bronchoconstriction in patients with asthma"C3 (✗ Contradict GT) "Propranolol", "is generally considered safe for", "patients with asthma when used at low doses"

Recent work argues for atomic, claim-level evalu-
ation: Med-PaLM’s verifier decomposes answers
into statements and searches evidence for each,
while FActScore measures factual precision over
atomic claims (Singhal et al., 2025; Min et al.,
2023). Figure 1 illustrates claim-level verification
outcomes in biomedical RAG, including supported
(Entail), contradicted (Contradict), and missing ref-
erence claims.

RagChecker further uses claims to diagnose be-
haviors such as hallucination and self-knowledge
(Ru et al., 2024). However, in medical settings,
retrieved passages may contain correlational state-
ments that look supportive but do not justify
causal/treatment claims; claims can be linguisti-
cally supported yet violate known drug–disease
contraindication relations. This motivates augment-
ing claim verification with structured biomedical
knowledge graphs (KGs).

We introduce MEDRAGCHECKER, a claim-
level verification framework for biomedical RAG
(Figure 2). Given a question, retrieved evidence,
and a long-form answer, MEDRAGCHECKER de-
composes the answer into atomic claims and as-
signs each claim a calibrated support confidence by
combining (i) textual natural language inference
(NLI) verification supervised by LLM supervision
(GPT-4.1 or GPT-4o) and (ii) KG-based support
computed by linking entities to a Drug Repurposing
Knowledge Graph (DRKG)-style biomedical graph
(Ioannidis et al., 2020). To make the pipeline prac-
tical, we distill teacher supervision into compact
biomedical student models (Li et al., 2025c,b,a;
Ma et al., 2025b,a) and validate the resulting di-
agnostics with human judgments, complementing
LLM-as-judge approaches (Wang et al., 2023; Li
et al., 2024; Min et al., 2023).

In summary, our contributions are: (1) A claim-
level diagnostic framework for biomedical RAG.
We extract atomic claims from long-form answers
and verify each claim to produce per-claim confi-
dence scores and answer-level hallucination diag-
nostics. (2) KG-enhanced biomedical verifica-
tion. We augment text-only claim verification by
anchoring claims to a DRKG-style biomedical KG
and computing a soft KG support signal (Ioanni-
dis et al., 2020). (3) Teacher-distilled, efficient
checking. We distill GPT-4.1 supervision into com-
pact biomedical student models for claim extrac-
tion and verification (Li et al., 2025c,b,a; Ma et al.,
2025b,a). (4) Human-aligned evaluation. We
evaluate on multiple biomedical QA benchmarks

and calibrate MedRAGChecker diagnostics against
human judgments, complementing prior factual-
ity evaluation work (Wang et al., 2023; Li et al.,
2024; Min et al., 2023). Our code is available at
https://anonymous.4open.science/r/Medica
lRagChecker-752E/.

2 Related Work

Biomedical QA. Biomedical QA benchmarks
(e.g., MedQA, MedMCQA, PubMedQA) drove
domain-specific LMs, and systems such as Med-
PaLM2 achieved strong performance on standard-
ized medical exams (Jin et al., 2020; Pal et al.,
long-form
2022; Jin et al., 2019). However,
biomedical answers remained prone to hallucina-
tions (Asgari et al., 2025; Huang et al., 2025), mak-
ing safety-critical validation necessary.

RAG Evaluation and Fact-Checking. RAG fac-
tuality checking was often formulated as an NLI-
style claim-evidence problem, where systems split
generations into statements and verified them by
retrieving supporting evidence (Lewis et al., 2020;
Fu et al., 2024; Xin et al., 2025a,b). Related works,
such as RAGAS (Es et al., 2024) and RAGChecker
(Ru et al., 2024), evaluated the quality of re-
trieval and grounding at the answer-level scores.
In contrast, MEDRAGCHECKER operated at the
claim level and then aggregated verified claims
into answer-level diagnostics, integrating an ad-
ditional structured KG signal to assess claim ve-
racity and evidence sufficiency. Domain-specific
fact-checkers like HealthFC (Vladika et al., 2024)
offered strong baselines for clinical validation, but
typically assumed short, well-formed statements.
Our work, targeting multi-sentence RAG answers,
provides a more fine-grained approach.

Knowledge Graphs for QA. Biomedical KGs
were applied in QA to support reasoning and
decision-making, such as in diagnostic KGs for
disease-centric applications (Himmelstein et al.,
2017). We built on this by using a biomedical KG
as an external verifier, mapping claims to KG en-
tities and relations to complement text-based NLI,
improving robustness. Because biomedical KGs
were incomplete (Chen et al., 2022), fusing KG evi-
dence with textual entailment enhanced consistency
in answering safety-critical biomedical questions.

2

Figure 2: Overview of MEDRAGCHECKER. For each atomic claim, textual NLI checking (purple) and KG-based
verification (orange) provide complementary signals—semantic entailment from retrieved context versus structured
biomedical constraints—which are fused and distilled into a student verifier (grey).

3 MedRAGChecker

3.2 Claim Extraction (Teacher → Student)

Figure 2 overviews the pipeline. MedRAGChecker
combines a textual NLI signal from teacher-
distilled student checkers with a KG-based con-
sistency signal from DRKG, and fuses them into
a single calibrated support score used by all down-
stream diagnostics.

3.1 Task Definition and Outputs

the

We cast biomedical RAG evaluation as claim-
centric verification. Given a RAG instance
(q, D, a), where q
the question, a is
is
the generated answer, and D = {dj}k
j=1
top-k retrieved evidence pas-
denotes
sages/documents, MEDRAGCHECKER decom-
poses a into atomic claims C = {c1, . . . , cn}
and assigns each claim (1) a discrete verdict
ˆyi ∈ {ENTAIL, NEUTRAL, CONTRADICT} and
(2) a calibrated support score s(ci) ∈ [0, 1]
indicating how likely the claim is supported under
the available evidence.

In our implementation, the textual checker pro-
vides pNLI(ci) ≜ P (ENTAIL | ci, D) from the
ensemble distribution. When KG evidence is avail-
able, we further fuse this textual signal with KG
support to obtain the final support score (Sec-
tion 3.5).

3.2.1 Teacher supervision

We use GPT-4.1 as a teacher to generate pseudo-
labels for both claim extraction and claim verifi-
cation. For each (q, D, a) triple, we first prompt
teacher model
to extract atomic claims (Sec-
tion 3.2.1). We then obtain NLI-style verifica-
tion labels and entailment probabilities for each
extracted claim using teacher model (Section 3.3).
Claim extraction: teacher model decomposes
the answer into a list of short, atomic statements
c1, . . . , cn that are intended to capture the factual
content of a, following the spirit of FActScore-style
atomic evaluation.(Min et al., 2023)

These teacher outputs give us supervision sig-
nal for training both the claim extractor and the
checker. We treat teacher labels as noisy but strong
teacher claim and labels compared to automatic
heuristics, and use them on the training and devel-
opment splits rather than as definitive human labels.
Combined with a small human study (Section 4.5),
this allows us to approximate claim-level supervi-
sion at scale while acknowledging that conclusions
are conditional on the choice of teacher model.

3.2.2 Student claim extractor

To avoid calling teacher model at inference time
due to its costs and time, we distill a student claim

3

QuestionRetrieved Context LLM Generate AnswerClaim Extractor C 1C 2C n…Ground Truth AnswerClaim Extractor C 1C 2C m…Textural NLI CheckerTextual entailment under retrieved evidenceAtomic Claim  CRetrieved Context Teacher NLI  Verifier NLI Score & Label(Entail/Neutral/Contradict)Multi-signal Claim JudgementEntity LinkingKG Lookup & Path Biomedical KGKG Support ScoreKG-Based VerificationGraph-based factual grounding Student Model Training  Student Models SFT trainingFinal Claim Teacher Claim for Training["subject", "relation", "object"]Teacher Label for Training  (NLI: Entail, Contradict Neutral)extractor. The student is a biomedical LLM (e.g.,
Meditron3-8B or Med42-Llama3-8B) fine-tuned to
map the question-answer pair (q, a) to a list of tex-
tual spans that closely match the teacher’s claims.
Training data consists of teacher claim lists, lin-
earized as a sequence of numbered bullet points.
We fine-tune the student with a standard sequence-
to-sequence SFT objective on (q, a) → c1, . . . , cn.
At evaluation time, we compare the extracted
claims with the output of the teacher model us-
ing precision, recall, and F1 at the span-level, and
we also ask human annotators to rate the overall
quality of the claim set on a 1–5 Likert scale (Sec-
tion G). Empirically, the distilled extractor recovers
most atomic facts while introducing few halluci-
nated claims; this makes it suitable as the front-end
for MedRAGChecker when the teacher model is
not available.

3.3 Textual Verification via NLI (Student

Checkers + Ensemble)

∈

For each extracted claim ci,
the teacher
is prompted with the retrieved ev-
model
idence D and asked to assign a
label
yi
{ENTAIL, NEUTRAL, CONTRADICT}
together with an entailment probability pNLI(ci),
language inference task
framed as a natural
(evidence as premise, claim as hypothesis). These
teacher outputs provide teacher label supervision
for distilling student claim checkers.

3.3.1 Student claim checkers

We similarly distill the claim verifier into com-
pact student checkers. Each training example con-
sists of an extracted claim ci, the associated re-
trieved context D, and the teacher model verdict
yi ∈ {Entail, Neutral, Contradict}.

We consider several biomedical LLMs as stu-
dents, including Meditron3-8B (Sallinen et al.,
2025), PMC-LLaMA-13B (Wu et al., 2024), Med-
Qwen2-7B (Bai et al., 2023), and Med42-Llama3-
8B (Christophe et al., 2024) using a standard cross-
entropy loss over the three NLI labels.This super-
vised fine-tuning already brings all students close
to the teacher model in overall accuracy (Table 1),
and we use these SFT checkers throughout the main
experiments. We also experimented with GRPO-
based refinement of the SFT checkpoints; how-
ever, the improvements were not consistent across
models and often came with drops in overall ac-
curacy. We therefore report GRPO results only in
Appendix F and keep SFT-only checkers as our

default.

3.3.2 F1-weighted ensemble
Because different student checkers specialize in
different classes, we build a lightweight ensemble
that combines their predictions using per-class F1
scores as reliability weights.

Let pm(y | ci, D) be the predicted probability
that the student checker m assigns the label y ∈
{Entail, Neutral, Contradict} to claim ci. From the
dev set, we compute per-class F1 scores F 1(y)
m for
each checker. We then define class-specific weights

w(y)

m =

F 1(y)
m
m′ F 1(y)
m′

.

(cid:80)

(1)

At inference time, the ensemble score for label y is

s(y | ci, D) =

(cid:88)

m

w(y)

m pm(y | ci, D),

(2)

and the final discrete verdict

is ˆyi =

arg maxy s(y | ci, D).

Intuitively, the ensemble allows models that are
strong on Neutral to dominate that class, while
models that are better at spotting contradictions
(e.g., Med-Qwen2-7B or Med42-Llama3-8B) con-
tribute more to CONTRADICT} decisions.

Default checker. Unless otherwise stated, we use
the F1-weighted ensemble as the default checker to
produce pNLI(ci); when KG fusion is enabled, we
then combine it with the KG signal to obtain the
final support score (Section 3.5).

3.4 KG Support via DRKG

3.4.1 Entity/relation linking
For each claim c, we construct a candidate set of
aligned KG triples A(c) = {(hj, rj, tj)}j. We
first identify a subject mention and an object men-
tion in c using simple heuristics over the extracted
SPO form (Appendix C), and perform string-based
matching against DRKG entity names to obtain can-
didate heads hj and tails tj. We similarly map the
canonical claim relation (e.g., TREATS, CAUSES) to
DRKG edge types to obtain candidate relations rj.
For each candidate triple (hj, rj, tj) we compute
a text alignment score stext(c, j) ∈ [0, 1] by com-
bining normalized string similarity for the subject,
relation, and object (details in Appendix C), and
define the claim-level alignment score as

stext(c) = max

j

stext(c, j).

(3)

4

3.4.2 Soft support with TransE
We score each aligned candidate triple (h, r, t) ∈
A(c) using TransE (Bordes et al., 2013):

dTransE(h, r, t) = ∥eh + rr − et∥2

pKGE(h, r, t) = σ(−dTransE(h, r, t)) .

(4)

(5)

We then aggregate a claim-level embedding plausi-
bility score by

pKGE(c) = max

(h,r,t)∈A(c)

pKGE(h, r, t).

(6)

If A(c) is empty, the claim is treated as KG-
uncovered.

3.5 Signal Fusion and Calibrated Support

Score P ⋆

For claims that can be aligned to DRKG, we com-
pute a KG consistency score as a soft prior, com-
bining embedding-based plausibility and text-level
alignment:

sKG(ci) = (1 − α) pKGE(ci) + α stext(ci),

(7)

where α ∈ [0, 1] is tuned on a development set. We
then fuse the textual NLI probability pNLI(ci) from
the ensemble checker with the KG score using a
logistic mixture:

P ⋆(ci) = σ

(cid:16)

β · logit(cid:0)pNLI(ci)(cid:1)
+ (1 − β) · logit(cid:0)sKG(ci)(cid:1)(cid:17)

,

(8)

where β controls the relative weight of text vs. KG
evidence and σ is the sigmoid function. For claims
that cannot be mapped to DRKG entities, we fall
back to P ⋆(ci) = pNLI(ci). We fuse the two sig-
nals in logit space to avoid one score dominating
the mixture purely due to scale mismatch in proba-
bility space. This fusion treats both components as
support proxies and yields a single support score
used consistently across diagnostics.

All downstream MedRAGChecker diagnos-
tics (claim faithfulness, hallucination rate, con-
text precision, and safety-critical error rate) are
computed from P ⋆(ci) and the predicted En-
tail/Neutral/Contradict labels. In experiments we
focus on safety-critical subsets where DRKG cover-
age is reasonably high, such as drug–disease treat-
ment, drug–side-effect and gene–disease claims. In
all experiments we tune the fusion weights α and

β and the decision threshold τ by grid search on
a held-out development split, maximizing macro-
F1 on claim-level verification. Once selected, the
same (α, β, τ ) configuration is fixed across all test
sets. For ablations comparing NLI-only vs. Fused,
we keep the same dev-tuned support threshold τ
when computing supported/unsupported statistics
(e.g., CLAIMREC and CTXPREC) to ensure com-
parability. SELFKNOW is computed with KG fu-
sion disabled and uses the NLI-only threshold τNLI
(Section 3.6).

3.6 Metrics

Notation. For an example (q, D, a), the extractor
outputs claims C = {ci}n
i=1. The checker predicts
a label ˆyi ∈ {ENTAIL, NEUTRAL, CONTRADICT}
and a fused confidence P ⋆(ci) ∈ [0, 1] (Eq. 8). In
the fused setting, we propagate the fused entail-
ment signal to the 3-way decision: we replace the
textual NLI ENTAIL logit with the fused entail logit
implied by P ⋆(ci) (Eq. 8), while keeping the NEU-
TRAL and CONTRADICT logits from the textual
NLI checker unchanged. We then renormalize with
a softmax to obtain a 3-way distribution and predict
ˆyi = arg maxy p(y | ci, D).

When computing binary supported/unsupported
statistics, we use a threshold τ (tuned on dev) and
define Isup(ci) = I[P ⋆(ci) ≥ τ ].

Claim extraction quality. Against
teacher-
extracted claims (GPT-4.1), we compute soft span-
level precision/recall/F1 by matching each pre-
dicted claim to the most similar teacher claim using
a token-overlap similarity (details in Appendix C).
We also report the average number of extracted
claims per answer.

Verification metrics (claim-level). Given claim-
level teacher labels yi from the teacher model (or
human labels when available), we report accuracy
and Macro-F1 over the three NLI classes.

Diagnostic metrics (answer-level). We aggre-
gate claim outputs to characterize generator and
retrieval behaviors:

Faith(a) =

Halluc(a) =

1
n

1
n

n
(cid:88)

i=1
n
(cid:88)

i=1

I[ˆyi = ENTAIL],

(9)

I[ˆyi = CONTRADICT]. (10)

Retrieval diagnostics. Let Cref be reference
(gold) claims extracted from the dataset reference

5

answer. We define claim recall as the fraction of
reference claims that are supported by the retrieved
evidence:

4 Experiments

4.1 Experimental Setup

ClaimRec =

1
|Cref|

(cid:88)

c∈Cref

Isup(c).

(11)

ClaimRec only reported where references are avail-
able.

We define context precision as the fraction of
retrieved passages that are used as evidence for at
least one supported claim (teacher provides evi-
dence spans):

CtxPrec =

1
k

k
(cid:88)

j=1

(cid:104)
∃i : dj is cited for ci

I

(12)

∧ P ⋆(ci) ≥ τ

(cid:105)

.

ClaimF1 (answer-level, reference-claim overlap).
Let Cref be reference claims extracted from the
dataset reference answer, and let Cgen be claims
extracted from the generated answer. We compute
Precision/Recall by matching each generated claim
to the most similar reference claim (token-overlap
matching as in Appendix C) and counting a match
as correct if it is supported (P ⋆ ≥ τ ). ClaimF1 is
the harmonic mean of this Precision and Recall.

Self-knowledge (parametric, NLI-only). To es-
timate parametric knowledge usage, we disable
KG fusion and rerun the textual NLI checker with
an empty context ∅. Let pNLI(ci | ∅) denote the
ensemble entailment probability when no retrieved
passages are provided. We compute

SelfKnow =

1
n

i=1

n
(cid:88)

I[pNLI(ci | ∅) ≥ τNLI] ,

(13)
where τNLI is tuned on the dev split using NLI-
only scores. This isolates parametric support from
external structured evidence (KG).

Safety-critical error rate. Let Csafety ⊆ C be
claims mapped to safety-critical biomedical rela-
tions (e.g., drug–disease, drug–side-effect) by our
DRKG linker. We report

Data and RAG setup. We evaluated on four
biomedical QA benchmarks: PubMedQA (Jin
et al., 2019), MedQuAD (Ben Abacha and Demner-
Fushman, 2019), LiveQA (Yang et al., 2017), and
MedRedQA (Nguyen et al., 2023). We used a
PubMed-based RAG pipeline with fixed retrieval
settings across runs and compared four biomed-
ical generators (Meditron3-8B, PMC-LLaMA-
13B, Med-Qwen2-7B, Med42-Llama3-8B) plus a
general-domain baseline (LLaMA-3-8B-Instruct).
Dataset and retrieval details are in Appendix A and
Appendix J.

Checker training and evaluation protocol. We
used GPT-4.1 to provide claims and NLI labels for
claim extraction and NLI verification on train/dev,
and distilled (i) a student claim extractor and (ii)
student NLI checkers; unless stated otherwise, we
used the F1-weighted ensemble (Section 3.3.2)
for downstream diagnostics. We report three
verification settings that differ only in who per-
forms extraction/checking: teacher-checker (GPT-
4.1), single-student, and student-ensemble. We
split the teacher-labeled data into train/dev/test
(80/10/10) and fine-tuned open-source students
with LoRA; training details are in Appendix L.
For KG-enhanced verification, we computed a
DRKG-based support score for aligned claims (Sec-
tion 3.4.1) and fused it with textual NLI via Eq. 8;
(α, β, τ ) were tuned on dev and then fixed for all
test results. GRPO refinements were exploratory
and are reported in Appendix F; unless noted, all
test results use student models only (no GPT-4.1
calls at inference).

We computed a DRKG-based support score for
aligned claims (Section 3.4.1) and fused it with
textual NLI via Eq. 8. Hyperparameters (α, β, τ )
were tuned on dev and then fixed for all test re-
sults. In RQ2, we focused on KG-aligned safety-
critical claim subsets (e.g., drug–disease, drug–
adverse event, gene–disease), where KG coverage
was meaningful.

4.2 Research Questions

SafetyErr =

1
|Csafety|

(cid:88)

c∈Csafety

I[ˆy(c) = CONTRADICT],

(14)
and optionally the same metric under the fused
score threshold τ .

6

Our experiments addressed: RQ1: How well did
distilled extractors/checkers match the teacher?
RQ2: Did DRKG fusion improve verification, es-
pecially for safety-critical claims? RQ3: Did end-
to-end diagnostics meaningfully differentiate gen-

Model

Panel A: Extractor

Panel B: Checker

P ↑ R ↑

F1 ↑ #Claims

Training

Acc (%) Macro-F1 (%) F1-E (%) F1-N (%) F1-C (%)

Med-Qwen2-7B
11.9
Med42-Llama3-8B 21.4
20.5
Meditron3-8B
0.3
PMC-LLaMA-13B

12.5
26.7
25.1
0.2

12.2
23.7
22.6
0.2

3.25
4.70
5.28
1.19

SFT
SFT
SFT
SFT

Ensemble (F1-weighted)

83.7
85.6
81.2
84.5

87.4

55.0
67.3
49.7
43.8

60.5

40.1
50.3
46.3
34.1

52.8

94.9
94.5
92.9
97.2

95.0

42.4
27.3
23.4
53.1

41.3

Table 1: Distilled claim extractor and checker fidelity to the GPT-4.1 teacher. Panel A: Soft span-level P/R/F1 under
token-overlap matching to teacher atomic claims; absolute values are conservative because the teacher produces
highly granular claims and matching requires near-surface overlap. Panel B: Checker accuracy and per-class F1 on
the 3-way NLI task. Unless stated otherwise, we use the F1-weighted ensemble as the default checker in downstream
experiments.

Model

Setting

Faith. ↑ Halluc. ↓ SafetyErr ↓ Faith. ↑ Halluc. ↓ SafetyErr ↓

Teacher-checker (GPT-4.1)

Student-checker (SFT ensemble)

Med-Qwen2-7B

Med42-Llama3-8B

Meditron3-8B

PMC-LLaMA-13B

NLI-only
Fused (ours)

NLI-only
Fused (ours)

NLI-only
Fused (ours)

NLI-only
Fused (ours)

70.1
75.6

70.2
77.0

58.2
66.8

23.2
22.2

21.8
18.6

18.1
23.0

20.6
33.2

38.8
77.8

29.9
24.4

29.8
17.5

41.8
23.7

76.8
67.3

62.3
68.6

67.3
58.4

52.7
59.6

15.3
21.3

20.7
10.4

24.3
25.7

14.6
27.3

57.3
73.4

19.6
12.6

28.9
19.6

29.0
27.2

63.2
54.3

Table 2: The results for the generation models in the overall seting. KG fusion ablation on KG-aligned claims. For
both the teacher-checker and student-checker columns, we evaluate on the same set of atomic claims extracted by
the teacher model and restrict to claims that are aligned to DRKG. Teacher-checker uses the teacher model for NLI
labeling, while student-checker uses the SFT ensemble to label the same claims. All numbers are macro-averaged
over four datasets on the KG-aligned subset.

Model

Claim qual.

Corr.

Compl.

Overall

Generator

Faith. ↑ Halluc. ↓ SafetyErr ↓

4.97±0.18 2.29±0.98 3.06±1.31 2.66±1.05
Med-Qwen2-7B
Med42-Llama3-8B 4.73±0.99 2.35±0.95 4.10±1.12 3.16±0.92
4.62±0.18 2.42±1.04 3.21±1.25 2.77±1.09
Meditron3-8B
PMC-LLaMA-13B 3.12±0.18 1.35±1.03 2.86±1.07 2.13±0.95

Med-Qwen2-7B
Med42-Llama3-8B
Meditron3-8B
PMC-LLaMA-13B

81.4
85.3
71.5
60.1

8.0
6.3
7.6
10.7

7.7
6.8
8.2
11.3

Table 3: RQ3: Human ratings (1–5) averaged over two
annotators on 100 questions. Claim quality measures
whether the extracted claim set faithfully reflects the
answer without introducing new facts.

Table 4: Representative end-to-end MedRAGChecker
diagnostics, macro-averaged across four biomedical
QA datasets. Full per-dataset results are reported in
Appendix B.

erators and align with human ratings?

4.3 RQ1: Distillation Quality

Extractor. Panel A of Table 1 reported span-
level precision/recall/F1 of the distilled extractors
against GPT-4.1 teacher claims, as well as the
average number of claims per answer. Med42-
Llama3-8B and Meditron3-8B obtained the high-
est F1 while producing 4–5 claims per answer,
closely matching the teacher’s atomic decompo-

sition. Because teacher claims were intentionally
highly granular and evaluation used conservative
token-overlap matching, absolute extractor F1 val-
ues were lower-bounded; human ratings in RQ3 fur-
ther validated that extracted claim sets were faithful
to the original answers.

Checker. Panel B of Table 1 showed that SFT
brought all biomedical checkers to strong overall
accuracy on the three-way NLI task, but with clear
class-wise specialization (e.g., stronger CONTRA-

7

Setting

Acc. ↑ Macro-F1 ↑

NLI-only
Fused (NLI+KG)

63.4
69.8

59.2
64.7

Table 5: Human agreement on KG-induced decision
flips (KG-aligned safety claims). Corrected flips: 31%.

DICT F1 for Med42-Llama3-8B). The F1-weighted
ensemble improved overall accuracy and robust-
ness on the minority CONTRADICT class, and was
used as the default checker for all downstream di-
agnostics. GRPO variants were deferred to Ap-
pendix F.

4.4 RQ2: Effect of KG-Enhanced Verification

We isolated the impact of the KG signal (DRKG)
by comparing NLI-only vs. Fused (NLI+KG) un-
der identical teacher and student checkers. Ta-
ble 2 reported results on KG-aligned safety-critical
claims. Overall, fusion changed decisions mainly
within the KG-covered subset, indicating that KG
evidence acted as a complementary support proxy
rather than perturbing unrelated claims. Additional
analyses on fusion sensitivity were provided in
Appendix E. While Table 2 showed that KG fu-
sion systematically altered verification outcomes
on KG-aligned claims, this alone did not establish
that such changes were more reliable. To directly
test whether KG integration improved trustwor-
thiness, we conducted a targeted human study on
KG-aligned claims where the final decision dif-
fered between NLI-only and Fused (NLI+KG)
settings.

Specifically, we focused on decision-flip
cases where KG fusion changed the sup-
ported/unsupported status or the predicted EN-
TAIL/CONTRADICT label. These cases concen-
trated annotation effort on scenarios where the KG
signal actively intervened, providing the most di-
rect test of its benefit. Annotators were asked to
judge claim veracity given the retrieved passages,
and we compared agreement with human labels
between NLI-only and Fused predictions.

As shown in Table 5, KG fusion achieved
higher agreement with human judgments on these
decision-flip claims,
indicating that structured
biomedical constraints helped correct a non-trivial
subset of text-only over-entailment errors, espe-
cially for safety-critical relations such as drug–
disease treatment and drug–adverse effect claims.
Calibration and Sensitivity On the dev split
(KG-aligned claims), P ⋆ is stable over a wide range

of (β, τ ). A β sweep shows that uncalibrated KG
scores make Eq. 8 overly β-sensitive and increase
decision flips, while min–max calibration (rescal-
ing KG scores to [0, 1] on dev) substantially flat-
tens both supported-rate and flip-rate curves (Ap-
pendix E, Fig. 4; Appendix E.1).

4.5 RQ3: End-to-End Diagnostics and

Human Alignment

Human study. We conducted a small-scale hu-
man evaluation on 100 questions sampled from
the four datasets, covering long-form answers pro-
duced by four biomedical generators. Two anno-
tators with biomedical/NLP background indepen-
dently rated, for each (question, model) pair, (1) the
quality of the extracted claim set, (2) answer cor-
rectness, (3) completeness, and (4) overall quality
on a 1–5 Likert scale.

Table 3 summarized the results. All systems
obtained near-ceiling claim-set quality scores, in-
dicating that the distilled extractor generally pro-
duced faithful and non-hallucinated atomic claims.
Across models, answer correctness was modest,
with Med42-Llama3-8B achieving higher com-
pleteness and overall quality than the others. We
reported agreement statistics and KG-alignment
validation in Appendix H. We also reported inter-
annotator agreement (quadratic-weighted κ) and
correlations between MedRAGChecker diagnos-
tics and human ratings in Appendix H.6.

End-to-end diagnostics. We applied the full
MedRAGChecker pipeline (distilled extractor,
student-ensemble checker, and KG fusion) to gener-
ator outputs to obtain answer-level diagnostics (e.g.,
faithfulness/NotSupported rate, context precision,
self-knowledge, safety-critical error rate). Repre-
sentative end-to-end diagnostics, macro-averaged
across datasets, were summarized in Table 4; the
full per-dataset breakdown was reported in Ap-
pendix B.

5 Conclusion

We introduced MEDRAGCHECKER, a claim-
level diagnostic framework for biomedical RAG.
MedRAGChecker decomposes long-form answers
into atomic claims, verifies each claim with a dis-
tilled textual NLI checker and a DRKG-based con-
sistency signal, and fuses them into a calibrated sup-
port score P ⋆. Across four biomedical QA bench-
marks, MedRAGChecker reveals distinct error pro-
files across generators (e.g., under-evidenced vs.

8

contradicted claims) and supports actionable diag-
nosis via retrieval- and safety-oriented metrics.

Limitations

Teacher supervision as pseudo-ground truth.
Our distillation and evaluation rely on teacher la-
bels for claim decomposition and NLI judgments,
which may contain biases or systematic errors, es-
pecially for rare biomedical conditions or ambigu-
ous questions. As shown by our teacher-sensitivity
analysis (Appendix Table 10), agreement between
GPT-4.1 and GPT-4o is high on research-style
datasets but substantially lower on consumer-health
questions (MedRedQA), so conclusions on those
datasets should be interpreted with caution and as
conditional on the chosen teacher.

Checker calibration and class imbalance.
Contradiction is typically a minority class; even
with ensembling, performance can vary across
datasets and may under-detect subtle contradic-
tions. MedRedQA exhibits low inter-teacher agree-
ment (Appendix Table 10), so we interpret absolute
Faith/Halluc values on MedRedQA with caution
and primarily focus on within-teacher relative com-
parisons and trends. KG coverage and linker
errors. DRKG does not cover all biomedical en-
tities/relations, and our entity/relation linking re-
lies on surface-form matching without ontology-
level normalization. This can fail for paraphrases,
negations, or multi-hop statements, and KG-based
signals may therefore be sparse or noisy outside
covered subsets. We use DRKG because it is a
large, public biomedical KG with broad coverage
of the safety-critical relation families we analyze,
enabling scalable and reproducible KG-based con-
sistency scoring.

General-purpose LLM-based evaluators may be
less reliable in high-stakes medical settings with-
out domain calibration, and standardized evalua-
tion remains an open challenge for medical LLM
applications.

Ethics Statement

MedRAGChecker is designed to detect unsup-
ported or contradictory claims in biomedical RAG
outputs and to surface safety-critical error patterns.
Nevertheless, automatic verification can be wrong;
false negatives may miss harmful claims and false
positives may over-warn. We recommend using
MedRAGChecker as a screening and debugging
aid, with human oversight for high-stakes settings.

Our experiments use publicly available datasets
and retrieved biomedical literature. If human an-
notation is used, annotators are informed of the
study purpose, compensated appropriately, and in-
structed not to provide medical advice. We do
not process private patient data. We will release
prompts, model checkpoints (where licenses allow),
and evaluation code to support transparency and
reproducibility.

References

Josh Achiam, Steven Adler, Sandhini Agarwal, Lama
Ahmad, Ilge Akkaya, Florencia Leoni Aleman,
Diogo Almeida, Janko Altenschmidt, Sam Altman,
Shyamal Anadkat, and 1 others. 2023. Gpt-4 techni-
cal report. arXiv preprint arXiv:2303.08774.

Elham Asgari, Nina Montaña-Brown, Magda Dubois,
Saleh Khalil, Jasmine Balloch, Joshua Au Yeung, and
Dominic Pimenta. 2025. A framework to assess clin-
ical safety and hallucination rates of llms for medical
text summarisation. npj Digital Medicine, 8(1):274.

Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang,
Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei
Huang, and 1 others. 2023. Qwen technical report.
arXiv preprint arXiv:2309.16609.

Asma Ben Abacha and Dina Demner-Fushman. 2019. A
question-entailment approach to question answering.
BMC Bioinform., 20(1):511:1–511:23.

Antoine Bordes, Nicolas Usunier, Alberto Garcia-
Duran, Jason Weston, and Oksana Yakhnenko.
2013. Translating embeddings for modeling multi-
relational data. Advances in neural information pro-
cessing systems, 26.

Weijian Chen, Yixin Cao, Fuli Feng, Xiangnan He, and
Yongdong Zhang. 2022. Explainable sparse knowl-
edge graph completion via high-order graph reason-
ing network. arXiv preprint arXiv:2207.07503.

Clément Christophe, Praveen K Kanithi, Tathagata
Raha, Shadab Khan, and Marco AF Pimentel. 2024.
Med42-v2: A suite of clinical llms.

Gordon V Cormack, Charles LA Clarke, and Stefan
Buettcher. 2009. Reciprocal rank fusion outperforms
condorcet and individual rank learning methods. In
Proceedings of the 32nd international ACM SIGIR
conference on Research and development in informa-
tion retrieval, pages 758–759.

Shahul Es, Jithin James, Luis Espinosa Anke, and
Steven Schockaert. 2024. RAGAs: Automated evalu-
ation of retrieval augmented generation. In Proceed-
ings of the 18th Conference of the European Chap-
ter of the Association for Computational Linguistics:
System Demonstrations, pages 150–158, St. Julians,
Malta. Association for Computational Linguistics.

9

Jinlan Fu, See Kiong Ng, Zhengbao Jiang, and Pengfei
Liu. 2024. Gptscore: Evaluate as you desire.
In
Proceedings of the 2024 Conference of the North
American Chapter of the Association for Computa-
tional Linguistics: Human Language Technologies
(Volume 1: Long Papers), pages 6556–6576.

Daniel Scott Himmelstein, Antoine Lizee, Christine
Hessler, Leo Brueggeman, Sabrina L Chen, Dexter
Hadley, Ari Green, Pouya Khankhanian, and Sergio E
Baranzini. 2017. Systematic integration of biomedi-
cal knowledge prioritizes drugs for repurposing. elife,
6:e26726.

Bolin Huang, Yuanzhou Wei, Jun Xiao, Yuanhao
Tian, Yeyubei Zhang, and Changyang Zheng. 2025.
Proactive reliability governance in complex systems:
Leveraging pattern mining for scalable solutions. In
2025 10th International Conference on Information
and Network Technologies (ICINT), pages 180–185.
IEEE.

Vassilis N. Ioannidis, Xiang Song, Saurav Manchanda,
Mufei Li, Xiaoqin Pan, Da Zheng, Xia Ning, Xi-
angxiang Zeng, and George Karypis. 2020. Drkg
- drug repurposing knowledge graph for covid-19.
https://github.com/gnn4dr/DRKG/.

Di Jin, Eileen Pan, Nassim Oufattole, Wei-Hung Weng,
Hanyi Fang, and Peter Szolovits. 2020. What dis-
ease does this patient have? a large-scale open do-
main question answering dataset from medical exams.
arXiv preprint arXiv:2009.13081.

Qiao Jin, Bhuwan Dhingra, Zhengping Liu, William
Cohen, and Xinghua Lu. 2019. PubMedQA: A
dataset for biomedical research question answering.
In Proceedings of the 2019 Conference on Empirical
Methods in Natural Language Processing and the
9th International Joint Conference on Natural Lan-
guage Processing (EMNLP-IJCNLP), pages 2567–
2577, Hong Kong, China. Association for Computa-
tional Linguistics.

Jeff Johnson, Matthijs Douze, and Hervé Jégou. 2019.
IEEE

Billion-scale similarity search with gpus.
Transactions on Big Data, 7(3):535–547.

Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio
Petroni, Vladimir Karpukhin, Naman Goyal, Hein-
rich Küttler, Mike Lewis, Wen-tau Yih, Tim Rock-
täschel, and 1 others. 2020. Retrieval-augmented gen-
eration for knowledge-intensive nlp tasks. Advances
in neural information processing systems, 33:9459–
9474.

Haitao Li, Qian Dong, Junjie Chen, Huixue Su, Yu-
jia Zhou, Qingyao Ai, Ziyi Ye, and Yiqun Liu.
2024. Llms-as-judges: a comprehensive survey
on llm-based evaluation methods. arXiv preprint
arXiv:2412.05579.

Yuqi Li, Junhao Dong, Chuanguang Yang, Shiping
Wen, Piotr Koniusz, Tingwen Huang, Yingli Tian,
and Yew-Soon Ong. 2025a. Mmt-ard: Multimodal
multi-teacher adversarial distillation for robust vision-
language models. arXiv preprint arXiv:2511.17448.

Yuqi Li, Kai Li, Xin Yin, Zhifei Yang, Junhao Dong,
Zeyu Dong, Chuanguang Yang, Yingli Tian, and
Yao Lu. 2025b. Sepprune: Structured pruning for
efficient deep speech separation. arXiv preprint
arXiv:2505.12079.

Yuqi Li, Chuanguang Yang, Hansheng Zeng, Zeyu
Dong, Zhulin An, Yongjun Xu, Yingli Tian, and Hao
Wu. 2025c. Frequency-aligned knowledge distilla-
tion for lightweight spatiotemporal forecasting. In
Proceedings of the IEEE/CVF International Confer-
ence on Computer Vision, pages 7262–7272.

Jimmy Lin, Xueguang Ma, Sheng-Chieh Lin, Jheng-
Hong Yang, Ronak Pradeep, and Rodrigo Nogueira.
2021. Pyserini: A Python toolkit for reproducible
information retrieval research with sparse and dense
representations. In Proceedings of the 44th Annual
International ACM SIGIR Conference on Research
and Development in Information Retrieval (SIGIR
2021), pages 2356–2362.

Dong Liu and Yanxuan Yu. 2025. Cxl-speckv: A dis-
aggregated fpga speculative kv-cache for datacenter
llm serving. Preprint, arXiv:2512.11920.

Zhichao Ma, Yutong Luo, Zheyu Zhang, Aijia Sun,
Yinuo Yang, and Hao Liu. 2025a. Reinforcement
learning approach for highway lane-changing: Ppo-
based strategy design. In 2025 10th International
Conference on Electronic Technology and Informa-
tion Science (ICETIS), pages 298–301.

Zhichao Ma, Aijia Sun, Zheyu Zhang, Yinuo Yang, Zi-
jun Gao, and Hao Liu. 2025b. Energy-constrained
motion planning and scheduling for autonomous
In 2025 5th In-
robots in complex environments.
ternational Conference on Advanced Algorithms and
Neural Networks (AANN), pages 591–594.

Sewon Min, Kalpesh Krishna, Xinxi Lyu, Mike Lewis,
Wen-tau Yih, Pang Koh, Mohit Iyyer, Luke Zettle-
moyer, and Hannaneh Hajishirzi. 2023. Factscore:
Fine-grained atomic evaluation of factual precision
in long form text generation. In Proceedings of the
2023 Conference on Empirical Methods in Natural
Language Processing, pages 12076–12100.

Vincent Nguyen, Sarvnaz Karimi, Maciej Rybinski, and
Zhenchang Xing. 2023. MedRedQA for medical con-
sumer question answering: Dataset, tasks, and neural
baselines. In Proceedings of the 13th International
Joint Conference on Natural Language Processing
and the 3rd Conference of the Asia-Pacific Chapter of
the Association for Computational Linguistics (Vol-
ume 1: Long Papers), pages 629–648, Nusa Dua,
Bali. Association for Computational Linguistics.

Yingpeng Ning, Yuanyuan Sun, Ling Luo, Yanhua
Wang, Yuchen Pan, and Hongfei Lin. 2025. Medtrust-
rag: Evidence verification and trust alignment for
arXiv preprint
biomedical question answering.
arXiv:2510.14400.

Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida,
Carroll Wainwright, Pamela Mishkin, Chong Zhang,

10

Sandhini Agarwal, Katarina Slama, Alex Ray, and 1
others. 2022. Training language models to follow in-
structions with human feedback. Advances in neural
information processing systems, 35:27730–27744.

Ankit Pal, Logesh Kumar Umapathi, and Malaikannan
Sankarasubbu. 2022. Medmcqa: A large-scale multi-
subject multi-choice dataset for medical domain ques-
tion answering. In Proceedings of the Conference
on Health, Inference, and Learning, volume 174 of
Proceedings of Machine Learning Research, pages
248–260. PMLR.

Shrey Pandit, Jiawei Xu, Junyuan Hong, Zhangyang
Wang, Tianlong Chen, Kaidi Xu, and Ying Ding.
2025. Medhallu: A comprehensive benchmark for
detecting medical hallucinations in large language
models. arXiv preprint arXiv:2502.14302.

Rafael Rafailov, Archit Sharma, Eric Mitchell, Christo-
pher D Manning, Stefano Ermon, and Chelsea Finn.
2023. Direct preference optimization: Your language
model is secretly a reward model. Advances in neural
information processing systems, 36:53728–53741.

Stephen Robertson, Hugo Zaragoza, and 1 others. 2009.
The probabilistic relevance framework: Bm25 and
beyond. Foundations and Trends® in Information
Retrieval, 3(4):333–389.

Dongyu Ru, Lin Qiu, Xiangkun Hu, Tianhang Zhang,
Peng Shi, Shuaichen Chang, Cheng Jiayang, Cunx-
iang Wang, Shichao Sun, Huanyu Li, and 1 others.
2024. Ragchecker: A fine-grained framework for di-
agnosing retrieval-augmented generation. Advances
in Neural Information Processing Systems, 37:21999–
22027.

Alexandre Sallinen, Antoni-Joan Solergibert, Michael
Zhang, Guillaume Boyé, Maud Dupont-Roc, Xavier
Theimer-Lienhard, Etienne Boisson, Bastien Bernath,
Hichem Hadhri, Antoine Tran, and 1 others. 2025.
Llama-3-meditron: An open-weight suite of medical
llms based on llama-3.1. In Workshop on Large Lan-
guage Models and Generative AI for Health at AAAI
2025.

Archit Sharma, Sedrick Scott Keh, Eric Mitchell,
Chelsea Finn, Kushal Arora, and Thomas Kollar.
2024. A critical evaluation of ai feedback for aligning
large language models. Advances in Neural Informa-
tion Processing Systems, 37:29166–29190.

Karan Singhal, Tao Tu, Juraj Gottweis, Rory Sayres,
Ellery Wulczyn, Mohamed Amin, Le Hou, Kevin
Clark, Stephen R Pfohl, Heather Cole-Lewis, and
1 others. 2025. Toward expert-level medical ques-
tion answering with large language models. Nature
Medicine, 31(3):943–950.

Tao Tu, Shekoofeh Azizi, Danny Driess, Mike Schaek-
ermann, Mohamed Amin, Pi-Chuan Chang, Andrew
Carroll, Charles Lau, Ryutaro Tanno, Ira Ktena, and
1 others. 2024. Towards generalist biomedical ai.
Nejm Ai, 1(3):AIoa2300138.

Juraj Vladika, Phillip Schneider, and Florian Matthes.
2024. Healthfc: Verifying health claims with
evidence-based medical fact-checking. In Proceed-
ings of the 2024 Joint International Conference
on Computational Linguistics, Language Resources
and Evaluation (LREC-COLING 2024), pages 8095–
8107.

Cunxiang Wang, Xiaoze Liu, Yuanhao Yue, Xiangru
Tang, Tianhang Zhang, Cheng Jiayang, Yunzhi Yao,
Wenyang Gao, Xuming Hu, Zehan Qi, and 1 others.
2023. Survey on factuality in large language models:
Knowledge, retrieval and domain-specificity. arXiv
preprint arXiv:2310.07521.

Yuxia Wang, Minghan Wang, Muhammad Arslan Man-
zoor, Fei Liu, Georgi Nenkov Georgiev, Rocktim Jy-
oti Das, and Preslav Nakov. 2024. Factuality of large
language models: A survey. In Proceedings of the
2024 Conference on Empirical Methods in Natural
Language Processing, pages 19519–19529, Miami,
Florida, USA. Association for Computational Lin-
guistics.

Chaoyi Wu, Weixiong Lin, Xiaoman Zhang, Ya Zhang,
Weidi Xie, and Yanfeng Wang. 2024. Pmc-llama:
toward building open-source language models for
medicine. Journal of the American Medical Infor-
matics Association, 31(9):1833–1843.

Wangjiaxuan Xin, Kanlun Wang, Zhe Fu, and Lina
Zhou. 2025a. Let community rules be reflected in
online content moderation. In The 18th China Sum-
mer Workshop on Information Management (CSWIM)
2025.

Wangjiaxuan Xin, Shuhua Yin, Shi Chen, and Yaorong
Ge. 2025b. Improving topic modeling of social me-
dia short texts with rephrasing: A case study of covid-
19 related tweets. arXiv preprint arXiv:2510.18908.

Yuan Yang, Jingcheng Yu, Ye Hu, Xiaoyao Xu, and Eric
Nyberg. 2017. Cmu livemedqa at trec 2017 liveqa: A
consumer health question answering system. arXiv
preprint arXiv:1711.05789.

Erlan Yu, Xuehong Chu, Wanwan Zhang, Xiangbin
Meng, Yaodong Yang, Xunming Ji, and Chuanjie Wu.
2025. Large language models in medicine: Applica-
tions, challenges, and future directions. International
Journal of Medical Sciences, 22(11):2792.

Daniel M Ziegler, Nisan Stiennon, Jeffrey Wu, Tom B
Brown, Alec Radford, Dario Amodei, Paul Chris-
tiano, and Geoffrey Irving. 2019. Fine-tuning lan-
arXiv
guage models from human preferences.
preprint arXiv:1909.08593.

A Dataset

This section summarizes the four biomedical QA
benchmarks used in our experiments. Table 6 re-
ports length and retrieval-context statistics, and
Table 7 provides a qualitative overview of question
style and evidence source.

11

Dataset
MedRedQA (CSIRO)
TREC LiveQA Medical
MedQuAD
PubMedQA

#Q Median |q| Max |q| Median |a| Max |a| Median #Doc Max #Doc Median/Max |d|
123 / 187
799
205 / 972
104
123 / 203
1000
239 / 735
1000

3732
66
18
43

1187
486
731
263

167
12
9
15

8
8
10
8

56
88
86
35

8
8
10
8

Table 6: Dataset statistics for MedRAGChecker RAG inputs. |q| and |a| denote tokenized question and (ground-
truth) answer lengths (whitespace tokens). |d| denotes retrieved document length; median/max refer to median and
maximum values across all retrieved contexts.

Dataset
MedRedQA
(CSIRO)

Domain
Consumer health (Red-
dit r/AskDocs)

Answer type
Free-text answers by
verified clinicians

TREC
Medical

LiveQA

Consumer health ques-
tions to NLM

Free-text answers with
quality judgments

MedQuAD

PubMedQA

NIH consumer health
websites

Free-text factoid / defi-
nition QA

Biomedical
(PubMed abstracts)

research

Yes/No/Maybe + long-
answer rationale

Question style / evidence
Medium–long layperson questions covering di-
verse symptoms and concerns; thread content
and PubMed-style references.
Long, noisy real-world user questions; reference
answers plus retrieved passages with human rel-
evance labels.
Short–medium consumer questions about dis-
eases, drugs, and procedures; long snippets from
NIH pages with source URLs.
Short research questions derived from article
titles; abstract body used as context, conclusion
paragraph as gold answer.

Table 7: Qualitative overview of the biomedical QA datasets used with MedRAGChecker, including domain, answer
type, and typical question/evidence style.

B Full Diagnostic Tables

12

Dataset

Generator

Faith. ↑ Halluc. ↓ CtxPrec ↑ SelfKnow. ↑ SafetyErr ↓

PubMedQA

MedQuAD

LiveQA

MedRedQA

Med-Qwen2-7B
Med42-Llama3-8B
Meditron3-8B
PMC-LLaMA-13B

Med-Qwen2-7B
Med42-Llama3-8B
Meditron3-8B
PMC-LLaMA-13B

Med-Qwen2-7B
Med42-Llama3-8B
Meditron3-8B
PMC-LLaMA-13B

Med-Qwen2-7B
Med42-Llama3-8B
Meditron3-8B
PMC-LLaMA-13B

83.6
88.9
69.2
57.9

85.3
87.6
73.1
63.2

72.4
82.5
72.3
55.7

84.2
82.4
71.2
63.4

7.4
4.7
3.3
11.7

6.0
5.5
7.6
8.7

11.3
8.6
11.3
12.8

7.3
6.4
8.3
9.5

41.8
41.4
53.2
35.6

42.4
46.3
49.4
44.6

43.2
42.7
48.6
38.1

41.7
42.7
44.3
41.3

28.2
32.7
30.4
21.6

32.4
31.2
24.0
20.0

23.1
28.6
31.4
22.6

26.4
27.2
28.0
22.5

7.0
6.5
5.9
12.4

8.5
7.8
8.2
9.7

7.6
6.2
9.5
10.4

7.6
6.7
9.3
12.7

Table 8: RQ3: Full end-to-end MedRAGChecker diagnostics across all datasets and generators (teacher = GPT-4.1 ).

Teacher = GPT-4.1

Teacher = GPT-4o

Dataset

Generator

ClaimF1 ClaimRec CtxPrec Faith. Halluc. ClaimF1 ClaimRec CtxPrec Faith. Halluc.

PubMedQA

MedQuAD

LiveQA

MedRedQA

Med-Qwen2-7B
Med42-Llama3-8B
Meditron3-8B
PMC-LLaMA-13B

Med-Qwen2-7B
Med42-Llama3-8B
Meditron3-8B
PMC-LLaMA-13B

Med-Qwen2-7B
Med42-Llama3-8B
Meditron3-8B
PMC-LLaMA-13B

Med-Qwen2-7B
Med42-Llama3-8B
Meditron3-8B
PMC-LLaMA-13B

26.7
27.6
23.5
14.6

39.3
43.4
31.8
0.0

6.3
10.8
5.7
0.0

10.7
11.5
7.4
9.8

97.6
97.9
97.2
98.3

65.7
61.5
63.3
63.5

26.8
27.5
26.4
30.1

16.2
14.6
14.5
14.4

49.9
49.8
32.9
50.0

51.4
51.4
52.8
51.9

43.1
42.2
41.1
45.6

12.3
11.2
11.3
10.5

88.6
92.4
69.2
58.0

88.1
86.1
83.1
0.0

72.4
70.3
53.9
27.3

31.4
32.0
26.7
7.4

7.4
5.2
3.3
29.6

9.4
6.4
4.9
5.2

18.3
12.6
22.9
45.2

52.1
48.0
51.4
75.0

23.2
21.1
21.0
14.7

30.1
39.5
30.1
0.0

5.3
8.8
4.6
0.0

1.5
2.0
1.2
0.0

96.9
99.0
97.5
97.4

62.3
62.8
63.9
61.3

23.8
24.8
26.3
15.6

13.9
13.2
13.5
9.2

41.8
41.4
41.9
50.7

47.0
46.0
49.4
47.2

37.6
38.1
41.9
27.5

9.5
9.8
10.1
7.5

83.6
88.9
63.7
60.5

82.9
80.2
73.1
4.0

65.9
63.7
29.6
0.0

12.7
14.0
9.7
3.7

7.4
4.7
1.0
29.5

6.2
8.5
7.6
6.0

22.4
7.5
13.5
0.0

5.6
4.5
6.0
5.3

Table 9: Teacher-checker results (teacher = GPT-4.1 vs GPT-4o).

C Prompt Templates

C.1 Teacher claim extraction prompt

You are a claim extraction assistant.

Task: Given an answer, extract a list of
ATOMIC factual claims as SPO triples.

Output format (STRICT): Return ONLY
a valid JSON array of triples: [ ["sub-
ject", "relation", "object"], ...
- No
prose, no markdown, no preface, no trail-
ing commas. - Use double quotes for
all strings. - Each triple must contain
exactly 3 strings.

]

Atomicity & faithfulness constraints: -
Each triple must express a single, check-
able fact stated in the answer. - Do NOT
paraphrase the whole sentence; split con-

junctions into separate triples. - Do NOT
introduce any new facts that are not ex-
plicitly stated in the answer. - Keep entity
names as they appear in the answer when
possible.

Negation / uncertainty / condition han-
dling: - If the answer negates a fact, re-
flect negation in the RELATION (pre-
ferred) or OBJECT. Example: ["Drug
A", "is not recommended for", "Con-
dition B"] - If the answer is uncer-
tain/probabilistic (may/can/likely), re-
flect it in RELATION. Example: ["Drug
A", "may cause", "Side effect X"] - If the
claim is conditional (if/when), include
the condition in RELATION. Example:
["Drug A", "reduces X when", "taken

13

with food"]

Now extract triples from the answer be-
low.

ANSWER: answer

C.2 Teacher NLI verification prompt

You are a strict NLI verifier for biomedi-
cal QA.

Goal: Decide whether the CLAIM is sup-
ported by the provided PASSAGES.

Input: - CLAIM: a single atomic claim
(hypothesis).
- PASSAGES: retrieved
text snippets (premises). Each passage
includes a doc_id.

Decision labels: - Entail: at least one
passage explicitly supports the claim. -
Contradict: at least one passage explic-
itly states the opposite of the claim. -
Neutral: the passages do not provide suf-
ficient information to entail or contra-
dict. Neutral includes: (a) insufficient
evidence (relevant but incomplete) (b) ir-
relevant evidence (not about the claim)

Constraints: - Use ONLY the informa-
tion in PASSAGES. Do NOT use exter-
nal knowledge. - If evidence is missing,
choose Neutral (insufficient). - Prefer En-
tail/Contradict only with explicit textual
support.

Output format (STRICT JSON): Re-
turn ONLY: "label": "Entail" | "Neu-
tral" | "Contradict", "prob": "Entail":
<float>, "Neutral": <float>, "Contradict":
<float>, "neutral_type": "insufficient" |
"irrelevant" | null, "rationale": <string>,
"spans": [ "doc_id": <string>, "quote":
- prob values must sum to
<string> ]
1.
- quote should be a short support-
ing/contradicting span (<= 25 words). -
If label is Neutral, spans can be [].

Now verify.

CLAIM: claim

PASSAGES:
topk_passages_with_doc_id

Teacher sensitivity and RAG alignment. Ta-
ble 10 shows that GPT-4.1 and GPT-4o agree
on most claim–evidence labels, suggesting that
our conclusions are not overly sensitive to the

14

Dataset

Label agreement ↑

κ ↑

PubMedQA
MedQuAD
LiveQA
MedRedQA

96.2
91.9
68.9
32.1

0.84
0.74
0.53
0.13

Table 10: Teacher sensitivity: GPT-4o vs GPT-4.1 on
the same claim–evidence pairs.

teacher choice. Recent RAG evaluation tools (e.g.,
RAGAS (Es et al., 2024)) provide answer-level,
reference-free signals such as faithfulness and con-
text quality; we conceptually align with this line
by treating each extracted claim as a minimal eval-
uation unit and scoring its support from retrieved
evidence. We do not report RAGAS as a main quan-
titative baseline because it is a general-purpose
framework rather than a biomedical claim-level
checker, and its behaviour in our setting is highly
sensitive to configuration choices (e.g., claim seg-
mentation and judge prompts).

D KG Case Study

D.1 Rating Scales and Guidelines

This appendix provides the full guidelines given
to annotators when rating model answers and ex-
tracted claims.

D.2 Goal of the Annotation

We evaluate (i) the quality of long-form answers
produced by different LLM/RAG generators to
medical questions, and (ii) the quality of an au-
tomatic claim extraction step applied to those an-
swers. Each row in the annotation sheet corre-
sponds to a single question, and contains:

• The original question.

• Model-generated answers from each student
model (e.g., Meditron3-8B, Med42-Llama3-
8B, Med-Qwen2-7B, PMC-LlaMA-13B).

• Automatically extracted claims for each

model.

For each model, annotators rate both the claim
set and the answer text according to the scales de-
scribed below.

We quantify how often generated claims can be
aligned to DRKG entities and edges. Table 11
reports node/pair coverage and KG-subset faith-
fulness/hallucination behavior under the pair-hit
definition.

Figure 3: Example where KG support corrects an over-confident textual entailment decision.

Dataset

Generator

KG-Covnode (%) KG-Covpair (%) Faith FaithKG HallKG

LiveQA

PubMedQA

MedQuAD

MedRedQA

Med-Qwen2-7B
Med42-Llama3-8B
Meditron3-8B
PMC-LLaMA-13B

Med-Qwen2-7B
Med42-Llama3-8B
Meditron3-8B
PMC-LLaMA-13B

Med-Qwen2-7B
Med42-Llama3-8B
Meditron3-8B
PMC-LLaMA-13B

Med-Qwen2-7B
Med42-Llama3-8B
Meditron3-8B
PMC-LLaMA-13B

84.2
68.5
70.0
65.0

83.0
95.0
88.3
72.0

93.0
94.0
84.0
8.0

90.0
92.0
90.2
92.7

51.3
56.4
52.6
30.0

49.0
83.0
62.7
35.0

69.0
88.0
66.0
4.0

53.4
74.3
46.3
86.6

72.4
63.7
53.9
27.3

88.6
92.4
69.2
60.5

88.1
86.1
83.1
4.0

37.8
31.3
26.7
7.4

86.3
87.8
65.7
25.6

96.1
94.5
85.8
57.1

87.2
89.0
89.5
0.0

32.8
36.7
26.0
6.1

8.8
9.4
26.1
57.7

3.9
5.0
6.2
42.9

11.2
7.2
7.4
92.3

50.3
48.5
55.1
76.2

Table 11: DRKG coverage and KG-subset behavior (pair-hit definition). We report node/pair coverage and KG-
subset faithfulness/hallucination metrics.

Dataset

Generator

Avg. Resp. Claims Avg. GT Claims Ent (%) Neu (%) Con (%)

PubMedQA

MedQuAD

LiveQA

MedRedQA

Med-Qwen2-7B
Med42-Llama3-8B
Meditron3-8B
PMC-LLaMA-13B

Med-Qwen2-7B
Med42-Llama3-8B
Meditron3-8B
PMC-LLaMA-13B

Med-Qwen2-7B
Med42-Llama3-8B
Meditron3-8B
PMC-LLaMA-13B

Med-Qwen2-7B
Med42-Llama3-8B
Meditron3-8B
PMC-LLaMA-13B

2.10
2.00
1.95
6.80

4.80
5.10
4.70
12.50

5.60
6.81
5.20
17.50

3.92
3.82
7.98
21.01

4.90
4.90
4.90
4.90

10.20
10.20
10.20
10.20

14.00
13.06
14.12
14.00

5.81
5.80
7.71
9.23

88.6
92.3
29.1
58.0

88.1
86.1
83.1
4.0

72.4
12.3
10.6
27.3

15.5
19.3
54.6
28.1

4.0
2.4
69.0
12.4

2.4
7.5
12.0
90.0

9.3
86.1
87.9
27.5

82.1
78.2
45.1
71.1

7.4
5.2
1.8
29.6

9.4
6.4
4.9
6.0

18.3
1.7
1.6
45.2

2.3
2.5
0.3
0.8

Table 12: Text-level claim verification summary (Entailment/Neutral/Contradiction histograms) across runs.
Ent/Neu/Con denote the percentage of generated claims assigned to each NLI label.

15

Claim + Evidence SnippetClaim: “Aspirin is recommended to treat fever in children with viral infections.”Retrieved snippet (partial/ambiguous): “Aspirin is effective for reducing fever and pain. … children … viral infections … Reye’s syndrome … (avoid aspirin).”Textual NLI/Checker Entailment score: 0.93 (ENTAIL)Note: Negation/contraindication under-attended → over-confident entailment.KG +FusionKGAspirin —(associated_with/adverse_event)—> Reye syndromeReye syndrome —(risk_group)—> ChildrenReye syndrome —(triggered_by)—> Viral infectionFusiontext_entail = 0.93kg_support = -0.70 (contradiction)fused = down-weighted to 0.20 → label: NOT-ENTAILED (safety-critical)AspirindrugViral infectionReye syndromediseasesymptomsE Calibration Details

E.1 Fusion-weight sensitivity (β-sweep)

We study how the fused support score P ⋆ and down-
stream supported/not-supported decisions change
as we vary the mixing weight β in Eq. 8. Unless
otherwise specified, we fix α to the dev-tuned value
and sweep β ∈ {0, 0.1, . . . , 1.0}.

Metrics. We report (i) the fused supported rate
(fraction of claims with P ⋆ ≥ τ ) and (ii) the deci-
sion flip rate relative to a near-NLI reference setting
(e.g., β = 0.9).

Supported rate and flip rate. For a given mixing
weight β, we compute fused scores P ⋆
β (c) via Eq. 8
and binarize them with the dev-tuned threshold τ :

Isup,β(c) ≜ I(cid:2)P ⋆

β (c) ≥ τ (cid:3) .

We summarize fusion behavior on a claim set C
using

fused_E(β) = 100 ·

1
|C|

(cid:88)

c∈C

Isup,β(c),

16

and the decision flip rate relative to a near-text-only
reference β0 (we use β0=0.9):

flip_rate(β) =

100
|C|

(cid:88)

c∈C

I [Isup,β(c) ̸= Isup,β0(c)] .

(15)

A lower flip_rate means fusion decisions are less
dominated by the KG score scale and thus more
stable across β.

Min–max calibration of KG scores. Raw KG
plausibility scores (e.g., TransE-based pKGE and
the derived sKG) can be poorly scaled and concen-
trated in a narrow range. To reduce scale mismatch
in the logit-mixture fusion (Eq. 8), we optionally
apply min–max calibration to the KG score on the
development split:

˜sKG(c) = clip

(cid:18) sKG(c) − smin
smax − smin

(cid:19)

, ϵ, 1 − ϵ

, (16)

where smin and smax are the minimum and maxi-
mum KG scores observed on the dev set (restricted
to KG-aligned claims), and ϵ is a small constant to
avoid infinite logits. We then replace sKG(c) with
˜sKG(c) when computing Eq. 8.

Why calibrating KG scores matters. Raw KG
plausibility scores can be poorly calibrated and
concentrated in a narrow range, which makes the
logit term logit(sKG) disproportionately large (in
magnitude) and causes fusion decisions to change
sharply with β. Min–max calibration aligns the
KG score scale to the NLI probability range while
preserving ranking, substantially reducing flip rates
and yielding flatter supported-rate curves in Fig. 4.

E.2 Threshold robustness (τ -sweep)

We additionally sweep the support threshold τ
around the dev-tuned value and observe stable
trends in the supported rate and SafetyErr within a
reasonable range.

For completeness, we report teacher-checker re-
sults for all dataset/generator configurations in Ta-
ble 9, complementing the representative results in
the main text.

F GRPO Refinement of Student Checkers

Setup. Beyond supervised fine-tuning (SFT), we
also explored Group Relative Policy Optimization
(GRPO; (Sharma et al., 2024; Rafailov et al., 2023;
Ziegler et al., 2019)) to further align the student

Figure 4: Sensitivity of KG–NLI fusion to the mixing weight β. Top: fused entailment rate (fused_E), i.e., the
fraction of claims classified as supported after fusion and thresholding. Bottom: decision flip rate (flip_rate)
relative to a near-NLI reference setting (β=0.9), measuring how often KG changes the supported/not-supported
decision. We compare SFT and GRPO checkers, with and without KG score calibration (minmax vs. none).

checkers with the GPT-4.1 teacher. Starting from
the SFT checkpoints, GRPO generates multiple ver-
dict candidates per (claim, evidence) pair and nor-
malizes rewards within each group. The reward is
+1 if the candidate label matches the teacher verdict
and 0 otherwise, with a KL penalty to the SFT pol-
icy. We run one additional GRPO epoch for each
biomedical backbone considered in the main text
(Med-Qwen2-7B, Med42-Llama3-8B, Meditron3-
8B, PMC-LLaMA-13B) using a smaller learning
rate than SFT (Ouyang et al., 2022; Sharma et al.,
2024; Rafailov et al., 2023; Ziegler et al., 2019).

Model

Train / Setting

Faith. ↑ Halluc. ↓

SafetyErr ↓

Med-Qwen2-7B

Med42-Llama3-8B

Meditron3-8B

PMC-LLaMA-13B

SFT / NLI-only
SFT / Fused (ours)
GRPO / NLI-only
GRPO / Fused (ours)

SFT / NLI-only
SFT / Fused (ours)
GRPO / NLI-only
GRPO / Fused (ours)

SFT / NLI-only
SFT / Fused (ours)
GRPO / NLI-only
GRPO / Fused (ours)

SFT / NLI-only
SFT / Fused (ours)
GRPO / NLI-only
GRPO / Fused (ours)

62.3
68.6
24.0
20.1

67.3
58.4
75.1
73.8

52.7
59.6
32.6
37.0

15.3
21.3
16.2
24.6

20.7
10.4
76.0
79.9

24.3
25.7
24.9
26.2

14.6
27.3
66.7
63.0

57.3
73.4
73.1
68.7

19.6
12.6
13.2
13.8

28.9
19.6
49.9
50.0

29.0
27.2
20.8
22.0

63.2
54.3
18.9
21.2

Table 13: RQ2: KG fusion ablation by checker back-
bone (SFT vs. GRPO). GRPO variants are deferred to
Appendix F and do not consistently improve over SFT.

Results. Overall, GRPO did not consistently im-
prove checker quality. For some backbones (e.g.,
Med-Qwen2-7B), GRPO increased CONTRADICT
F1 but substantially reduced ENTAIL F1 and overall
accuracy, leading to overly aggressive contradiction
predictions. For other backbones, GRPO produced
only marginal changes relative to the SFT base-
lines. When plugged into MedRAGChecker, these
GRPO-tuned checkers did not yield clear gains on
downstream diagnostics such as answer-level faith-
fulness, hallucination, or safety-critical error rate.
Given the extra complexity and computational cost
of GRPO, and the lack of consistent improvements,
we therefore report SFT-only student checkers in
the main paper and treat GRPO as an exploratory
negative result.

G Human Evaluation: Protocol

We conduct human evaluation to assess (i) answer
quality and (ii) claim extraction quality for model
outputs.

G.1 Setup

Sampling. We sample 100 questions from
MedQuAD, LiveQA, MedRedQA, and Pub-
MedQA. For each question, we evaluate up to
four generators’ answers (Meditron3-8B, PMC-
LLaMA-13B, Med-Qwen2-7B, Med42-Llama3-
8B) and the extracted claim sets.

Annotators. Annotators are graduate students
with training in biomedical or health sciences. Each

17

05101520253035fused_EMed-Qwen2-7B1020304050607080Med42-Llama3-8B010203040Meditron3-8B01020304050PMC-LLaMA-13B0.20.40.60.80.9051015202530flip_rate0.20.40.60.80.9010203040500.20.40.60.80.9051015202530350.20.40.60.80.950510152025Metrics vs  (mean ± SEM)grpo | minmaxgrpo | nonesft | minmaxsft | noneScore Anchor rubric (applies to all four dimen-

H.1 Sampling and annotation unit

5

3

1

sions)

Excellent: correct and reliable; for claims,
covers key factual points without adding un-
supported content.
Mixed: partially correct but with noticeable
omissions or distortions; could mislead with-
out caution.
Poor: largely incorrect/off-topic or unusable;
for claims, fails to represent the answer or
introduces clear hallucinations.

Table 14: Collapsed anchor rubric for 1–5 ratings (2 and
4 are intermediate).

model output is rated independently; annotators do
not rank models.

Unit of annotation. For each (question, model)
pair, annotators score the answer and its extracted
claim set. When reference answers/evidence are
available, annotators rely primarily on them; other-
wise they use domain knowledge.

G.2 Dimensions and scoring

Annotators assign 1–5 Likert scores for four dimen-
sions: Claim extraction quality (claims faithfully
reflect the answer without hallucinations), Answer
correctness, Answer completeness, and Overall
answer quality. Scores 5/3/1 correspond to excel-
lent / mixed / poor, with 2 and 4 as intermediate
levels. Table 16 include the results for the kappa
value for correctness and claim quality

When to comment. Annotators provide a brief
comment if (i) any answer score is 1–2, or (ii) claim
quality is ≤ 3.

G.3 Agreement and reporting

We report mean±std over samples (averaging two
annotators per sample) and compute quadratic-
weighted Cohen’s κ for inter-annotator agreement.

Full guidelines. Detailed examples and interface
schemas are provided in our anonymized reposi-
tory.

H Human Validation of KG Alignment

Goal. We assess whether the KG-alignment mod-
ule yields a semantically faithful structured ren-
dering of a claim. This evaluates alignment cor-
rectness (entity identity and relation meaning), not
biomedical truth.

We perform stratified sampling over evaluation
folders (dataset/model/config), and only sample
from claims where the aligner outputs at least one
DRKG triple after filtering. Each annotated item
is a claim-level instance consisting of: claim text,
optional supporting context, and the top-1 aligned
triple (h, r, t) returned by the aligner (ties broken
deterministically). We annotate n=100 aligned
claims for correctness, and additionally double-
annotate a subset of size nκ for inter-annotator
agreement.

H.2 Annotation fields

Annotators provide four binary labels and optional
notes:

• h_subj_entity_ok: subject entity refers to
the same biomedical concept as the claim sub-
ject;

• h_obj_entity_ok: object entity refers to the
same biomedical concept as the claim object;

• h_relation_map_ok: relation matches the

claim predicate and directionality;

• h_triple_semantic_ok: overall triple ex-

presses the claim semantics.

H.3 Decision criteria

Entities are marked OK if they map to the same con-
cept (synonyms/standard variants allowed); NOT
OK for wrong concept/type or overly broad/narrow
mappings that change meaning. Relations are
marked OK only if predicate meaning and direction
match (e.g., treats vs. associated with; contraindi-
cation vs. adverse event).

Collapsed triple criterion. To avoid ambiguity,
we define:

htriple ≜ hsubj ∧ hobj ∧ hrel,

=

hsubj

h_subj_entity_ok,
where
hobj = h_obj_entity_ok,
and hrel =
h_relation_map_ok. This yields a conservative
estimate of end-to-end alignment correctness.

H.4 Metrics

We report claim-level correctness rates on the an-
Pr[h_subj_entity_ok=1],
notated
subset:
Pr[h_obj_entity_ok=1],
Pr[h_relation_map_ok=1],

18

Metric

Value (%)

Dimension

κ (quadratic)

#Items

Subject entity accuracy
Object entity accuracy
Relation mapping accuracy
Triple plausibility rate

78
76
89.2
82

Claim quality
Correctness
Completeness

0.67
0.32
0.27

100
100
100

Table 15: Human validation results for DRKG align-
ment on a stratified sample, aggregating two annotators.

Table 16: Inter-annotator agreement for the human
study.

Pr[h_triple_semantic_ok=1]. On the double-
annotated subset, we report Cohen’s κ for each
field (or for h_triple_semantic_ok).

H.5 Coverage of KG alignment

We also report claim-level coverage: a claim is
counted as “aligned” if the module outputs at least
one retained DRKG triple (h, r, t) after filtering.
We stratify coverage by coarse relation families
used in our safety analysis (e.g., Drug–Disease,
Drug–Adverse Event, Gene–Disease).

H.6 Human Evaluation: Agreement and

Correlation

Correlations between MedRAGChecker diagnos-
tics and human ratings. See in Table 16.

Metric vs Human

ρ (Spearman)

Faith vs Correctness
Halluc vs Correctness
SafetyErr vs Correctness
CtxPrec vs Overall

0.47
0.23
0.36
0.53

Table 17: Correlation between MedRAGChecker diag-
nostics and human ratings, since we have 100 questions
for annotation and each question at least 4 claims gener-
ated.

I Human Evaluation on KG-Induced

Decision Flips

Sampling. We sample claims from the KG-
aligned subset where the final verification decision
differs between NLI-only and Fused (NLI+KG)
settings. Claims are stratified by relation families
used in the safety analysis (e.g., drug–disease, drug–
adverse effect, gene–disease).

Annotation unit. Each annotation instance con-
sists of a single atomic claim, the retrieved pas-
sages used for verification, and (optionally) the
top-1 aligned KG triple for reference. Annotators
are instructed to judge claim veracity only based
on the retrieved passages, without using external
knowledge.

Labels. Annotators assign one of {ENTAIL, NEU-
TRAL, CONTRADICT} to each claim. We then
compare human labels against NLI-only and Fused
predictions to compute accuracy, Macro-F1, and
corrected flip rates.

J Retrieval settings and indices

retrieval

Overview. We
across
standardize
datasets by using (i) a FAISS index for CSIRO
runs, (ii) a pre-retrieved pickle for MedQuAD, and
(iii) the MedRAG retrieval system for the remain-
ing datasets. Table 18 summarizes the mapping
from dataset to retriever and the corresponding
index artifacts. Table 19 lists the index files and
where they are stored.

19

Dataset

MedRedQA

MedQuAD

Retriever

Index / evidence source

CsiroFaissRetriever / gold FAISS mode (Johnson et al., 2019): FAISS ANN index built over
CSIRO corpus (faiss.index + texts.jsonl + meta.jsonl under
–csiro_index_dir); gold mode: use provided contexts directly
(no external index).
Pre-retrieved contexts loaded from –medquad_pickle (a pickle file
containing query-to-context mappings).

MedQuADRetriever

PubMedQA / LiveQA /
MedRedQA (non-CSIRO) MedRAGRetriever

MedRAG retrieval over a selected corpus (e.g., PubMed / MedCorp)
using BM25 (Robertson et al., 2009) (–retriever bm25), dense
(contriever/specter/medcpt), or hybrid (RRF (Cormack et al.,
2009)). Indices are stored under –medrag_db_dir.

Table 18: Dataset-to-retriever mapping and the evidence source used for retrieval.

Retriever family

Key artifacts

CSIRO FAISS

faiss.index, texts.jsonl, meta.jsonl

MedQuAD pre-retrieval

retrieved_*.pkl

Where it lives / how it is used

All under –csiro_index_dir. Re-
trieved hits are mapped to text via
texts.jsonl (with optional meta-
data in meta.jsonl).
–medquad_pickle. No ANN/BM25
search at runtime; directly loads
cached retrieval results.

MedRAG BM25

Lucene/Pyserini (Lin et al., 2021) BM25 index (directory) Stored under –medrag_db_dir (per
corpus). Used when –retriever
bm25.
MedRAG dense / hybrid faiss.index (+ metadata file such as metadatas.jsonl) Stored

under

–medrag_db_dir
(per corpus and retriever). Used
when –retriever is dense (e.g.,
contriever/specter/medcpt)
or
hybrid (RRF fusion).

Table 19: Index artifacts used by each retriever family.

K Extractor Results

Backbone ablation. Table 13 compares GRPO
checkers under calibrated β fusion. med42-llama3-
8b yields the most stable fused distribution, while
other backbones exhibit degenerate or highly
skewed fused label rates, motivating our choice of
med42-llama3-8b as the default checker backbone.

Fusion form and calibration. We compare
additive-style fusion (alpha) with logit-mixture fu-
sion (beta). Beta fusion benefits from calibrating
KG scores, as raw KGE plausibility often concen-
trates in a narrow low range; calibration preserves
KG ranking while aligning its scale to NLI proba-
bilities, preventing the KG term from dominating
the mixture purely due to scale mismatch. We use
GPU A100 80G for the training.

L Student Configurations

Dataset

Generator

ClaimF1 ↑ Faith ↑ Halluc ↓

PubMedQA

Med42-Llama3-8B
Meditron3-8B (GPT-4o)
Med-Qwen2-7B
PMC-LLaMA-13B

MedQuAD

LiveQA

MedRedQA

Med42-Llama3-8B
Meditron3-8B
Med-Qwen2-7B
PMC-LLaMA-13B

Med42-Llama3-8B
Meditron3-8B
Med-Qwen2-7B
PMC-LLaMA-13B

Med42-Llama3-8B
Meditron3-8B
Med-Qwen2-7B
PMC-LLaMA-13B

21.1
21.0
23.2
19.2

27.2
30.1
34.2
22.8

14.3
10.4
12.6
7.4

11.6
12.4
15.7
8.0

88.9
63.0
83.6
56.3

72.5
73.1
82.4
63.6

77.3
67.4
76.7
43.6

33.2
20.9
37.4
18.3

4.7
1.0
7.4
20.6

4.2
7.6
5.4
12.8

7.9
10.6
21.6
26.4

63.2
57.2
18.9
74.6

Table 20: Teacher-based MedRAGChecker metrics
(placeholder version). ClaimF1 is claim overlap F1;
Faith is entailment rate; Halluc is contradiction rate
(Contradict-only).

20

Stage

Base models

lr

ep bs acc L Gen

LoRA / Extra

Extractor SFT

Checker SFT

Checker GRPO

Med42-Llama3-8B
Meditron3-8B
Med-Qwen2-7B
PMC-LLaMA-13B

Med42-Llama3-8B
Meditron3-8B
Med-Qwen2-7B
PMC-LLaMA-13B

Med42-Llama3-8B
Meditron3-8B
Med-Qwen2-7B
PMC-LLaMA-13B

1e−4 3

2

16

2048 max_new_tokens=256

r=16, α=32, drop=0
targets: q,k,v,o,gate,up,down

5e−5 3

2

16

1024

eval: max_new_tokens=4
eval_subset=1000

r=8, α=16, drop=0
targets: q,k,v,o,gate,up,down

5e−6 1

2

8

1024

sample: max_new_tokens=3, T =0.7, top_p=0.9
eval: max_new_tokens=4
eval_subset=800

r=8, α=16, drop=0
K=4 samples/prompt
grad clip=1.0
targets: q,k,v,o,gate,up,down

Table 21: Training configurations for the distilled extractor and checker models. L denotes tokenizer truncation
length.

21


