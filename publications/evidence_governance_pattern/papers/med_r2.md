Med-R2: Crafting Trustworthy LLM Physicians via Retrieval and
Reasoning of Evidence-Based Medicine
Zheng Liang
Da Pan
Shusen Zhang
Guosheng Dong
Baichuan Inc.
Beijing, China

Keer Lu
Wentao Zhang∗
wentao.zhang@pku.edu.cn
Center for Data Science, AAIS
Peking University
Beijing, China

Huang Leng
Zhonghai Wu
Bin Cui
School of Computer Science
Peking University
Beijing, China

5
2
0
2

t
c
O
9

]
L
C
.
s
c
[

5
v
5
8
8
1
1
.
1
0
5
2
:
v
i
X
r
a

Abstract
Large Language Models (LLMs) have exhibited remarkable capabili-
ties in clinical scenarios. Despite their potential, existing works face
challenges when applying LLMs to medical settings. Strategies rely-
ing on training with medical datasets are highly cost-intensive and
may suffer from outdated training data. Leveraging external knowl-
edge bases is a suitable alternative, yet it faces obstacles such as
limited retrieval precision and poor effectiveness in answer extrac-
tion. These issues collectively prevent LLMs from demonstrating
the expected level of proficiency in mastering medical expertise. To
address these challenges, we introduce Med-R2, a novel LLM physi-
cian framework that adheres to the Evidence-Based Medicine (EBM)
process, efficiently integrating retrieval mechanisms as well as the
selection and reasoning processes of evidence, thereby enhancing
the problem-solving capabilities of LLMs in healthcare scenarios
and fostering a trustworthy LLM physician. Our comprehensive
experiments indicate that Med-R2 achieves an improvement of
13.27% over vanilla RAG methods and even a 4.55% enhancement
compared to fine-tuning strategies, without incurring additional
training costs. Furthermore, we find that our LLaMA3.1-70B + Med-
R2 surpasses frontier models, including GPT-4o, Claude3.5-Sonnet
and DeepSeek-V3 by 1.05%, 6.14% and 1.91%. Med-R2 effectively
enhances the capabilities of LLMs in the medical domain.

Keywords
Evidence-Based Medicine, Retrieval Augmented Generation, Large
Language Models

ACM Reference Format:
Keer Lu, Wentao Zhang, Zheng Liang, Da Pan, Shusen Zhang, Guosheng
Dong, Huang Leng, Zhonghai Wu, and Bin Cui. 2026. Med-R2: Crafting
Trustworthy LLM Physicians via Retrieval and Reasoning of Evidence-
Based Medicine. In Proceedings of the ACM Web Conference 2026 (WWW
’26), April 13–17, 2026, Dubai, UAE.. ACM, New York, NY, USA, 18 pages.
https://doi.org/XXXXXXX.XXXXXXX

∗Corresponding Author.

Permission to make digital or hard copies of all or part of this work for personal or
classroom use is granted without fee provided that copies are not made or distributed
for profit or commercial advantage and that copies bear this notice and the full citation
on the first page. Copyrights for components of this work owned by others than the
author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
republish, to post on servers or to redistribute to lists, requires prior specific permission
and/or a fee. Request permissions from permissions@acm.org.
WWW ’26, Dubai, UAE.
© 2026 Copyright held by the owner/author(s). Publication rights licensed to ACM.
ACM ISBN 978-1-4503-XXXX-X/2026/06
https://doi.org/XXXXXXX.XXXXXXX

Figure 1: Comparison of Med-R2 with existing strategies for
medical problem-solving.

1 Introduction
Large Language Models (LLMs) have emerged as pivotal tools in
the medical domain, redefining the contours of healthcare prac-
tice [1, 38, 48]. Their ability to process and understand vast amounts
of unstructured medical data positions them at the forefront of med-
ical research [7, 32], clinical decision-making [12, 26], and patient
care [4, 41]. Despite their remarkable capabilities, LLMs encounter
several challenges when applied specifically to healthcare settings:
C1: Inefficiency in Knowledge Acquisition. Existing approaches
predominantly rely on training LLMs with datasets from the medi-
cal domain, the process of which is inherently compute-intensive
and resource-demanding, especially as model sizes increase [31, 37].
Moreover, training with outdated datasets can result in a lack of
highly specialized expertise, which can lead to suboptimal clinical
recommendations or misinform healthcare professionals [14, 24].
C2: Limited Precision for Medical Retrieval. Compared to
domain-specific training, Retrieval-Augmented Generation (RAG)
systems provide a cost-efficient solution, leveraging the external
knowledge base to enhance content generation [27]. The retrieval
quality is critical in RAG systems, where inaccuracy or misinforma-
tion can heavily influence the effectiveness of LLMs’ augmentation.
While efforts [18, 30, 42] have been made to improve the retrieval
precision, they neglect the specific and highly professional nature
of medical knowledge, where tailored retrieval enhancement for
distinct medical scenarios remains insufficiently explored.

Patient: “How can I determine if I have contracted the Marburg virus disease?”Knowledge
CorpusA few hours later...TrainingHigh-Resource ConsumptionOutdated Training DataLLM PhysicianEvidence
AppraisingMed-R2Evidence SearchingEvidence ApplyingEffect AssessmentQuestion FormulatingWhat are the diagnostic criteria for Marburg virus disease, and what clinical symptoms and lab results indicate this diagnosis?EBMLLM PhysicianVanilla RAGLimited Retrieval PrecisionInefficient Content Extraction

WWW ’26, April 13–17, 2026, Dubai, UAE.

Keer Lu et al.

C3: Low Effectiveness in Answer Extraction. Considering the
constraints imposed by the models’ context window length, it is
essential to critically appraise the retrieved medical evidence for its
validity, impact, as well as applicability, and integrate the most perti-
nent ones with existing clinical expertise for problem-solving [5, 10].
Nonetheless, current studies fail to develop targeted answer extrac-
tion methods tailored for healthcare scenarios, where the nuanced
evaluation of evidence hierarchies is required [35].

To address these challenges, we introduce Med-R2, a noval med-
ical LLM framework designed in accordance with the principles of
Evidence-Based Medicine (EBM), conducting outstanding Retrieval
and Reasoning aligned with distinct phases of EBM. 1) For C1, we
have established a comprehensive external knowledge base to en-
hance models’ medical performances, offering a more cost-effective
and flexible alternative to domain-specific training. 2) For C2, we
improve the retrieval precision by refining the original queries
according to their respective medical scenarios, while iteratively
incorporating chain-of-thought sequences generated from the re-
trieved content. 3) For C3, we adopt a coarse-to-fine strategy for
document appraising and filtering, and select the most pertinent
ones supplemented with chain-of-thought demonstrations to assist
medical queries addressing. Our contributions are as follows:
• Challenges in Medical Scenarios. Through conducting a quantita-
tive analysis of strategies aimed at enhancing models’ medical
capabilities, we underscore the challenges prevalent in healthcare
scenarios, including high computational consumption as well as
poor efficiency in knowledge retrieval and extraction.

• LLM Physician Framework. We present Med-R2, a novel LLM physi-
cian framework that integrates the principles of evidence-based
medicine (EBM) for clinical problem-solving with outstanding
retrieval and reasoning capabilities within medical contexts.
• Performance and Effectiveness. Extensive experiments indicate that
Med-R2 achieves a 14.74% improvement over the vanilla RAG
methods, and even a 3.32% enhancement compared to the fine-
tuning strategies without additional training expenses. Moreover,
LLaMA3.1-70B + Med-R2 surpasses frontier models for medical
problem-solving, achieving average improvements over GPT-4o,
Claude3.5-Sonnet and DeepSeek-V3 by 1.22%, 5.33% and 2.80%.

2 Related Work and Discussions
EBM refers to the application
Evidence-Based Medicine (EBM)
of the best available research to healthcare, which requires evidence
integration with clinical expertise and patient values [10, 34, 35].
Clinical questions can be categorized into several types, including
diagnosis, therapy, prognosis, etiology, prevention, cost, etc. [5]. Each
category intersects with EBM principles by emphasizing the collec-
tion, evaluation, and application of the best retrieved evidence to
inform medical decision-making [11], as detailed in Section A.

LLMs for Medical Domain As the application of LLMs ex-
pands, their deployment in the medical domain has become a widely
discussed topic [7, 50]. Recent studies have concentrated on the
direct use of medical data for the pretraining or fine-tuning of
LLMs [36, 38]. Prominent open-source milestones include ChatDoc-
tor [28] which integrates real-world doctor-patient communica-
tion data for training, PMC-LLaMA [43] pretrained on 4.9 million
medical literature records, and MEDITRON [6], a scaling series of

medical pretrained models. However, such extensive training can
be computationally intensive. In contrast, Retrieval-Augmented
Generation (RAG) systems offer a more efficient alternative, achiev-
ing comparable results with reduced training costs and enhancing
the model’s precision in locating and leveraging knowledge.

Retrieval-Augmented Generation (RAG)

The concept of
RAG [27] was introduced as a powerful framework for integrating
external knowledge into natural language generation tasks, enhanc-
ing the accuracy and relevance of generated outputs across various
domains [9, 17, 51]. In the medical field, RAG has been widely used
to improve LLMs’ analytical performances by utilizing external
medical knowledge from sources such as medical papers, textbooks,
guidelines, and entries [22, 45, 46, 49]. However, while there have
been efforts dedicated to optimizing the individual components of
RAG pipelines [3, 18, 19, 42], research that integrates the unique
characteristics and requirements of the medical domain remains in
its infancy. In this study, we incorporate the principles of Evidence-
Based Medicine (EBM) into medical RAG systems to better address
the special demands of healthcare.

3 Med-R2
In this section, we discuss our Med-R2 framework, illustrated in
Figure 2. Med-R2 is designed around the Evidence-Based Medicine
(EBM) workflow, encompassing the stages of clinical question for-
mulation (Section 3.1), evidence retrieval and appraisal (Section 3.2),
evidence application (Section 3.3), and effect assessment (Section 3.4).

3.1 Question Formulation
In the medical domain, the efficacy of information retrieval is closely
tied to the professionalism of the query. A well-crafted, professional
query that includes precise descriptions of medical symptoms can
markedly enhance the accuracy and relevance of the documents
retrieved from knowledge bases. Conversely, non-standard terms
and isolated numerical values frequently hinder effective informa-
tion retrieval. Moreover, the focus of the desired response varies
depending on the type of clinical consultation. For instance, in
queries pertaining to etiology, users seek insights into potential
causes of a condition, including risk factors, pathogens, or genetic
predispositions. In contrast, for prognosis-related queries, users
are interested in understanding the long-term outcomes or patient
prognoses, such as survival rates or recurrence probabilities.

The clinical question formulation stage consists of two compo-
nents: query classifier and query reformulator. The query clas-
sification encompasses two dimensions: Evidence-Based Medicine
(EBM) categories and general natural language question types. Specif-
ically, we have delineated six distinct EBM categories and twelve
general question categories, as illustrated in Figure 2. The applica-
tion of this classification scheme to the MedMCQA dataset yielded
the categorized results presented in Figure 3. For the classifica-
tion task, we have manually annotated 100 samples to fine-tune
Qwen2.5-72B-Instruct1, and employed the trained model as our
classifier. We perform domain-specific reformulations of the origi-
nal queries based on their respective classes of the EBM categories
to align with the professional context. Meanwhile, the general ques-
tion categories are utilized as one of the criteria to rerank retrieved

1https://huggingface.co/Qwen/Qwen2.5-72B-Instruct

2

Med-R

: Crafting Trustworthy LLM Physicians via Retrieval and Reasoning of Evidence-Based Medicine

WWW ’26, April 13–17, 2026, Dubai, UAE.

Figure 2: An illustration of Med-R2’s process, adhering to the Evidence-Based Medicine (EBM) workflow. We first categorize
the query by EBM and general question types. Queries are then reformulated according to established EBM classification
templates to ensure precision and relevance. In the evidence searching and appraising stages, we employ a coarse-to-fine
strategy to retrieve, filter, and re-rank the evidence documents within the knowledge base. CoT sequences are then generated
from processed evidence to refine retrieval space, iterating to ensure the robustness.

3.2 Evidence Searching && Appraising
The retrieval and appraisal of evidence constitute one of the most
critical stages in EBM. The professional reformulating of queries in
the preceding stages (Section 3.1) aims to enhance the precision of
retrieving relevant evidence documents. This stage comprises two
key components: evidence retriever and evidence reranker.

3.2.1 Evidence Retriever. To construct a more comprehensive med-
ical knowledge base adaptable to diverse healthcare scenarios, we
have amassed a collection of medical data to build our knowledge
corpus. The final medical knowledge base employed for retrieval
comprises four distinct types of resources: academic papers, entries,
books, and guidelines, with details of the data sources and statistics
depicted in Table 1. For resources with extensive content such as
academic papers, books, and guidelines, we first perform content
segmentation with a threshold set at 10,000 tokens. We prioritize
dividing the content based on natural chapters. If natural chapters
cannot be identified or exceed the threshold, we resort to truncation
according to the predefined limit.

We integrate multiple types of retrievers to optimize our retrieval
performance, incluing BGE-Large-EN-v1.52 for dense retrieval and
SPLADE-v33 for sparse retrieval. We then consolidate the docu-
ments retrieved through both methods into a unified collection that

Figure 3: Query category of MedMCQA. We employ a loga-
rithmic scale (base 10) on the z-axis, ranging from 1 to 40000,
to represent the wide range of values.

documents, thereby prioritizing those that best match the current
query’s intent and document type preferences described in Figure 5.
Further details can be found in Section B.1.

2https://huggingface.co/BAAI/bge-large-en-v1.5
3https://huggingface.co/naver/splade-v3

Med-R2Evidence-Based Medicine
(EBM)Raw QueryQuery ReformulatorGeneral Question CategoryDescriptiveFactualComparativeDirectiveReferentialEvaluativeOpinionDefinitionVerificationProceduralExplanatoryHypotheticalCostTherapyEtiologyPrognosisDiagnosisPreventionEBM CategoryQuery ClassifierQuestion
FormulatingCoarse
GrainedDoc kUsefulnessInitial StateLoss+ Doc kStrategyGeneral Document CategoryEvaluationInstructionNarrationCommandProcessDefinitionClassificationComparisonDescriptionArgumentationExplanationCause and EffectPredictionConditionProblem-SolvingPurposeEvidence RerankerHierarchy of EvidenceDoc nDoc 5Doc 6Doc 4Doc 3Doc 2Doc n-1Doc 1Knowledge Conflict!IIIIIIIVVFine-GrainedRetrieved Document nRetrieved Document 2Evidence RetrieverRetrieved Document 1Dense RetrieverSparse RetrieverEvidence
Searching && AppraisingLLM PhysicianCoT GeneratorAnalyze the QuestioReview Provided ContexConsult Retrieved DocumentIdentify Key InformatioConstruct Thought ProcesProvide AnswerEvidence ApplyingCategory ProjectionEffect
AssessingClinical PracticeFew-Shot LearningQuery Categories of MedMCQACostDiagnosisEtiologyPreventionPrognosisTherapyVerificationReferentialProceduralOpinionHypotheticalFactualExplanatoryEvaluativeDirectiveDescriptiveDefinitionalComparative500010000150002000025000300003500040000100100010000200003000040000WWW ’26, April 13–17, 2026, Dubai, UAE.

Keer Lu et al.

Table 1: Overall statistics of medical knowledge resources.

Source Type

#Volume

#Tokens / Doc
Max Min Mean Medium

Academic Papers
Entries
Books
Guidelines

600,000
470,000
10,000
10,000

10,643
6,538
15,384
4,981

279
56
524
74

Total

1,090,000

15,384

56

3,820
1,387
4,083
1,100

2,748

3,097
1,962
4,319
1,778

2,219

contains 𝑛 documents, D = {𝑑𝑖 }𝑛
𝑖=1 = D𝐷 ∪ D𝑆 , where D𝐷 com-
prises documents obtained by dense retrieval, and D𝑆 represents
those acquired via sparse retrieval.

3.2.2 Evidence Reranker. For the document collections retrieved
in Section 3.2.1, we employ a coarse-to-fine strategy for rerank-
ing. we initially utilize the BGE-Reranker-v2-M34 to rerank D =
{𝑑𝑖 }𝑛
𝑖=1 based on their semantic relevance to the current query at
a coarse granularity, returning the top 𝑘 documents5, denoted as
S𝑐 = {𝑑𝑖 }𝑘
𝑖=1. At this stage, the total length of these 𝑘 documents
significantly exceeds the context limit of the model. Then we con-
duct a fine-grained reranking that integrates three distinct criteria
for the current 𝑘 documents to get S 𝑓 = {𝑑𝑖 }𝑘′
𝑖=1, enabling the model
to provide answers based on the most effective retrieved documents
within the limited length of the context window. The fine-grained
reranking score can be formulated as:

F (𝑥) = 𝑓ℎ (𝑥) · 𝑓𝑔 (𝑥) (1 + 𝛼 · 𝑓𝑢 (𝑥))
where 𝑓ℎ (𝑥), 𝑓𝑢 (𝑥) and 𝑓𝑔 (𝑥) refer to scores of each refined eval-
uation criteria, while 𝛼 is the non-negative hyper-parameter for
weight controlling. The detailed implementation and explanation
for the derivation of Equation (1) can be found in Section B.3.

(1)

Hierarchy of Evidence Medical knowledge encompasses
facts and theories that are not always consistent, and sometimes
even contradictory. This criterion serves dual purposes: scoring
and conflict filtering. The recalled documents that have undergone
coarse-grained reranking are first categorized according to their
evidence levels. Subsequently, contents of these documents are
analyzed for conflicting facts, where the documents that contain
conflicting facts and have lower evidence ratings are filtered out.
Formally, each retrieved document 𝑑𝑖 ∈ S𝑐 is associated with an
integer evidence level 𝑒, where 𝑒 ∈ {𝑥 ∈ Z | 1 ≤ 𝑥 ≤ 9}, with 1
indicating the highest level of credibility, as depicted in Figure 4:

(2)

𝑓ℎ (𝑥) = 9 − (𝑒𝑥 − 1)
By applying the evidence assessment criteria, the retrieved doc-
uments are categorized into multiple evidence levels, and profes-
sional analysis of evidence at different levels of authority is per-
formed, preventing misjudgments caused by information clutter.
The usefulness ranker is employed to assess the
contribution of retrieved documents to the answering process.
Specifically, we quantify the usefulness of a document by mea-
suring the difference in loss before and after using the retrieved

Usefulness

4https://huggingface.co/BAAI/bge-reranker-v2-m3
5During the previous retrieval phase, documents of all retrieval types are subjected to a
unified ranking, within which the top-𝑘 documents are selected for further processing.

Figure 4: Hierarchy of evidence. The base of the pyramid repre-
sents the lowest quality, while the apex denotes the highest.

Figure 5: Query Document Projection.

document to answer the question. This is achieved with a light-
weight proxy model that evaluates the impact of the document on
the answer’s quality, which can be written as:

𝑓𝑢 (𝑥) = max (cid:8)ℓ𝑖𝑛𝑖𝑡

𝜃 − ℓ𝑥

𝜃 , 0(cid:9)

(3)

where ℓ𝑖𝑛𝑖𝑡
documents, while ℓ𝑥
𝜃

𝜃

indicates the loss without referring to any retrieved

represents that informed by document 𝑥.

General Document Category

It corresponds to the mapping
of general natural language question types discussed in Section 3.1.
Different categories of questions desire distinct answer structures.
For instance, questions regarding procedural steps are ideally an-
swered by documents that describe processes rather than those
that define concepts. To address this, we categorize the retrieved
documents into 16 document types, denoted as 𝐶, as outlined in
Table 6, and score them based on their alignment with the response
type preferred by the original query, as depicted in Figure 5. The
scoring function is defined as:

𝑓𝑔 (𝑥) =

|𝐶𝑒 |
∑︁

𝑗=1

𝑝 (𝑥 |𝑐 𝑗 )

(4)

where 𝐶𝑒 = (cid:8)𝑐 𝑗 (cid:9) |𝐶𝑒 |
stands for the list of expected document types
𝑗=1
(𝐶𝑒 ⊂ 𝐶), and 𝑝 (𝑥 |𝑐 𝑗 ) represents the probability that the docu-
ment 𝑥 belongs to the current expected type 𝑐 𝑗 from 𝐶𝑒 . Details of
computational procedures are provided in Algorithm 1.

Meta-AnalysesSystematic ReviewsCritically Appraised Literature
Evidence-Based Practice GuidelinesRandomized Controlled TrialsNon-Randomized Controlled TrialsCohort StudiesCase Series or StudiesIndividual Case ReportsBackground Information, Expert Opinion, Non-EBM GuidelinesQuality of EvidenceHighLowCritical
AppraisalExperimental
StudiesObservational
StudiesGeneral Question CategoryDescriptiveFactualComparativeDirectiveReferentialEvaluativeOpinionDefinitionVerificationProceduralExplanatoryHypotheticalGeneral Document CategoryEvaluationInstructionNarrationCommandProcessDefinitionClassificationComparisonDescriptionArgumentationExplanationCause and EffectPredictionConditionProblem-SolvingPurpose2

Med-R

: Crafting Trustworthy LLM Physicians via Retrieval and Reasoning of Evidence-Based Medicine

WWW ’26, April 13–17, 2026, Dubai, UAE.

Algorithm 1 Scoring Based on General Document Category Clas-
sification
Input: Coarsely reranked documents S𝑐 , Query-document mapping A
based on Figure 5, classifier 𝑀𝑃 , List of general document categories 𝐶
Parameter: List of current expected document categories 𝐶𝑒 , 𝐶𝑒 ⊂ 𝐶
Output: Scores based on document category 𝑓𝑔 (𝑆𝑐 )
Define 𝑞𝑐 : category of the query used for retrieving
Define (cid:174)𝑝: category probability distribution of document 𝑑
1: for each document 𝑑𝑖 in S𝑐 do
2:
3:
4:
5:

/* Step 1: Expected Category Mapping */
Obtain expected categories 𝐶𝑒 = A (𝑞𝑐
/* Step 2: Document Category Probability Inference */
Provide category probability distribution of 𝑑𝑖 referring to 𝑀𝑃 :

𝑑𝑖 ), where 𝐶𝑒 ⊂ 𝐶

(cid:174)𝑝𝑖 = {𝑝 (𝑑𝑖 |𝑐 𝑗 ) } |𝐶 |

𝑗 =1 ← 𝑀𝑃 (𝑑𝑖 )

6:
7:

/* Step 3: Statistics Aggregation */
Calculate the sum of probabilities across all expected categories:

𝑓𝑔 (𝑑𝑖 ) = (cid:205)|𝐶𝑒 |

𝑗 =1 𝑝 (𝑑𝑖 |𝑐 𝑗 ), where 𝑐 𝑗 ∈ 𝐶𝑒

8: end for
9: Return 𝑓𝑔 (𝑆𝑐 ) = (cid:8)𝑓𝑔 (𝑑𝑖 )(cid:9) |𝑆𝑐 |

𝑖=1

CoT Generator

3.3 Evidence Applying
Through the comprehensive evaluation and reranking of retrieved
documentary evidence in Section 3.2.2, we aim to ensure the appli-
cation of the highest-quality available evidence to decision-making
in the medical field. This process extends beyond merely applying
research findings, where integrating the professional reasoning and
judgment is essential. Therefore, it is imperative to make profes-
sional and reasoned inferences based on the retrieved documents.
This module constructs a chain-of-thought
reasoning process based on the original medical query and the
retrieved evidence documents6. It serves dual functions: (1) Com-
ponent of Query Reformulation: It contributes to the subsequent
query reformulation process, facilitating the retrieval of evidence
documents relevant to the question. In Section 5, we also clar-
ify the rationale behind not incorporating models’ generated CoT
sequences into the query reformulator for medical knowledge re-
trieval at the initial iteration. (2) Few-Shot Learning Instance: It pro-
vides few-shot examples for the LLM physician (target model) in-
tended for downstream task evaluating, demonstrating how to
analyze the retrieved evidence, identify the key information, and
address medical queries effectively.

3.4 Effect Assessment
Our assessment of evidence is centered on the following aspect:
the stability of evidence document retrieval across different stages.
Algorithm 2 delineates the evidence evaluation process and the
iterative retrieval loop for the query corpus within the pipeline,
where we determine the number of iterations for optimization
termination based on our assessment of such factor. This ensures
that when evaluating the LLM physician (target model) on medical
tasks, the retrieved documents provided are effective and robust.

6When ablating the integration of CoT sequences at the onset in Section 5, the CoT
sequences are curated solely from the original medical query during the initial iteration,
excluding the retrieved evidence documents.

Algorithm 2 Evidence Assessment and Iterative Retrieval Loop
for Query Corpus

𝑓
Q−𝑡𝑜𝑝

Input: Query corpus Q, CoT generator 𝑀𝐶𝑜𝑇 , Context window length 𝑤,
Hyperparameters: alteration threshold 𝛿, maximum iterations 𝑇
Params: Coarsely reranked documents S𝑐 , finely reranked documents S 𝑓
and CoT sequences Q𝐶𝑜𝑇
Output: Selected evidence documents S
Define 𝑞𝐶𝑜𝑇 : chain-of-thought sequence generated based on query and
associated evidence documents
Define 𝐸 (𝑑 ): embedding of document 𝑑
, Q𝐶𝑜𝑇 ← [ ], [ ]
1: S
2: for each query 𝑞𝑖 in Q do
for 𝑡 = 1, 2, . . . ,𝑇 do
3:
4:

Reformulate query 𝑞𝑖 (Section 3.1), search and appraise the re-
trieved evidence (Section 3.2)
/* Step 1: CoT Generation */
𝑓 (𝑡 )
Select top 𝑘 documents from S
𝑖

referring to 𝑤:

𝑓
Q−𝑡𝑜𝑝

𝑓 (𝑡 )
𝑓 (𝑡 )
𝑖 −𝑡𝑜𝑝 ← SelectTopK( S
S
𝑖

, 𝑘, 𝑤 )

Generate chain-of-thought sequence based on 𝑞𝑖 and S

𝑓 (𝑡 )
𝑖 −𝑡𝑜𝑝 :

𝑞𝐶𝑜𝑇 (𝑡 )
𝑖

← 𝑀𝐶𝑜𝑇 (𝑞𝑖, S

𝑓 (𝑡 )
𝑖 −𝑡𝑜𝑝 )

/* Step 2: Evidence Assessment */
Compute semantic stability of docs in consecutive iterations:

(cid:174)𝜇 (𝑡 )
𝑖 ← | |

1
| S𝑐 (𝑡 )
𝑖

|

∑︁

𝐸 (𝑑𝑖 ) −

𝑑𝑖 ∈S𝑐 (𝑡 )
𝑖

1
| S𝑐 (𝑡 −1)
𝑖

|

∑︁

𝐸 (𝑑𝑖 ) | |

𝑑𝑖 ∈S𝑐 (𝑡 −1)
𝑖

/* Step 3: Termination Condition Evaluation */
if (cid:174)𝜇 (𝑡 )
𝑖 < 𝛿 then
𝑓
S
Q−𝑡𝑜𝑝
Break

.𝑎𝑝𝑝𝑒𝑛𝑑 ( S

𝑓 (𝑡 )
𝑖 −𝑡𝑜𝑝 ), Q𝐶𝑜𝑇 .𝑎𝑝𝑝𝑒𝑛𝑑 (𝑞𝐶𝑜𝑇 (𝑡 )

𝑖

)

end if
end for
S

𝑓
Q−𝑡𝑜𝑝

.𝑎𝑝𝑝𝑒𝑛𝑑 ( S

16:
17: end for
18: Return Selected documents S

𝑓 (𝑇 )
𝑖 −𝑡𝑜𝑝 ), Q𝐶𝑜𝑇 .𝑎𝑝𝑝𝑒𝑛𝑑 (𝑞𝐶𝑜𝑇 (𝑇 )

𝑖

)

𝑓
Q−𝑡𝑜𝑝

and CoT sequences Q𝐶𝑜𝑇

5:

6:

7:

8:
9:

10:

11:

12:

13:
14:
15:

4 Experiments and Results
4.1 Experimental Setup
Model Details. We employ the open-sourced LLMs from LLaMA [8,
40] and Qwen [47] series as our target models for evaluation. We
assessed models including LLaMA3.1-8B, Qwen2.5-14B, Qwen2.5-
32B and LLaMA3.1-70B, scaling from 8B to 70B. The default setting
of context window for our main experiments is 4K, with an in-depth
scaling analysis presented in Section 5.

Datasets. We have selected eight medical datasets including
PubMedQA [21], MedQA-USMLE, MedQA-MCMLE [20], MedM-
CQA [33], MMLU-Med [15], NEJMQA [25], MedXpertQA [52], and
RareArena [39], covering both standard and real-world clinical sce-
narios. We use accuracy as evaluation metrics. More details about
the datasets can be found in Section C.1.

Implementation. We constructed the medical knowledge cor-
pus by establishing FAISS vector library [23]. Experiments related to
model training were conducted based on full-parameter fine-tuning,

WWW ’26, April 13–17, 2026, Dubai, UAE.

Keer Lu et al.

Table 2: Comparison of Med-R2 with baselines. The best and second best are in bold and underlined.

Model

Method

MedQA-USMLE MedQA-MCMLE MedMCQA PubMedQA MMLU-Med NEJMQA MedXpertQA RareArena-RDC RareArena-RDS

Within-Dataset Fine-Tuning

Cross-Dataset Fine-Tuning

GPT-4o
Claude3.5-Sonnet
DeepSeek-V3

PMC-LLaMA-7B
MEDITRON-7B
PMC-LLaMA-13B
MEDITRON-70B

–
–
–

–
–
–
–

LLaMA3.1-8B

Qwen2.5-14B

Qwen2.5-32B

LLaMA3.1-70B

Direct Response
Vanilla RAG
Fine-Tuning
LLM-AMT
Med-R2

Direct Response
Vanilla RAG
Fine-Tuning
LLM-AMT
Med-R2

Direct Response
Vanilla RAG
Fine-Tuning
LLM-AMT
Med-R2

Direct Response
Vanilla RAG
Fine-Tuning
LLM-AMT
Med-R2

84.95
83.20
80.93

38.65
46.76
40.38
55.05

31.16
55.80
76.53
52.91
77.01
50.01
54.88
55.87
51.48
54.34

16.23
19.33
25.57
19.38
24.43

46.43
62.66
87.17
79.18
86.37

79.28
72.54
77.82

35.30
42.78
33.07
52.21

41.45
59.38
85.24
66.63
84.16

65.23
75.60
85.52
77.11
80.19

87.07
89.30
89.97
88.08
90.01
58.36
77.91
86.21
68.59
84.58

Frontier Models

74.60
68.80
74.30

77.20
76.40
73.60

84.44
83.90
87.67

Open-Sourced Medical Models
26.87
43.60
46.85
71.45

52.26
58.32
54.63
72.84

32.40
36.83
37.55
53.50

Open-Sourced Base Models

30.02
35.91
47.38
45.08
52.33
42.85
42.06
47.64
43.09
48.36
66.44
67.63
66.17
68.33
69.09
62.33
66.63
71.65
70.12
73.36

36.17
47.10
42.78
44.60
52.75
56.93
60.38
54.29
62.42
68.32

68.66
67.06
66.69
68.61
68.36

66.81
68.78
74.72
79.05
78.24

37.12
43.54
42.92
45.39
45.19

71.60
79.46
80.41
78.78
84.03
80.19
83.85
82.40
82.06
84.95
71.33
76.95
79.46
80.74
82.82

72.20
68.52
74.23

35.63
38.80
40.60
66.97

50.41
52.01
52.48
53.07
55.69
45.63
45.69
46.67
47.44
48.03
43.59
46.63
52.58
46.82
50.40

65.43
66.40
68.11
68.90
70.18

30.37
21.31
24.16

11.02
11.74
11.44
18.05

14.90
15.50
15.54
16.22
17.79
11.06
12.28
12.30
13.73
14.45
15.06
17.49
15.71
17.90
18.54
23.43
25.95
24.18
26.53
26.84

73.76
68.46
75.09

28.96
35.68
39.86
74.81

41.85
56.23
55.38
60.20
62.90
43.17
54.00
66.32
60.03
72.80
59.67
66.10
70.20
66.75
72.51
72.59
77.70
76.41
77.00
78.60

47.50
50.78
45.72

21.67
26.50
28.98
46.58

22.16
35.06
38.37
40.29
44.82
26.58
28.05
43.66
38.81
46.30
31.33
40.59
45.08
45.40
55.36
43.54
44.88
47.23
45.87
49.42

Avg.

69.31
65.99
68.73

31.42
37.89
37.04
56.83

33.91
44.51
50.73
47.16
54.74
45.89
50.27
54.75
52.54
57.43
52.03
55.33
57.15
55.93
59.29
56.69
63.10
68.35
66.22
70.04

during which we utilized a learning rate scheduler featuring lin-
ear warm-up and cosine decay, peaking at a learning rate of 2e-5,
alongside a warmup ratio of 0.03, a weight decay of 0.0 and a batch
size of 128 for 3 epochs. We conducted all training and evaluation
experiments on NVIDIA RTX H800 GPUs with 80G memory.

4.2 Baselines
We compare Med-R2 with the following baselines: (1) Frontier
Models contain GPT-4o [16], Claude3.5-Sonnet [2] and DeepSeek-
V3 [29]. (2) Open-Sourced Medical Models include PMC-LLaMA-
7B, PMC-LLaMA-13B [43], MEDITRON-7B and MEDITRON-70B [6].
(3) The simplest baseline is Direct Response, where the model an-
swer medical questions directly without the aid of external knowl-
edge bases or dataset fine-tuning. (4) Vanilla RAG [27] utilizes raw
queries for evidence searching, and the retrieved documents are
then directly integrated into the generation process without any
further manipulation. (5) Fine-Tuning leverages medical datasets
to further train the model under supervised conditions. Here we em-
ploy two strategies: within-dataset fine-tuning, where the datasets
for training and evaluation are derived from different parts of the
same data corpus, and cross-dataset fine-tuning, where the model is
fine-tuned on one medical dataset (e.g., MedMCQA) and then eval-
uated on different datasets (e.g., PubMedQA). (6) LLM-AMT [42]
is a dedicated process tailored for biomedical question answering,

which includes typical modules such as query augmenter, hybrid re-
triever, knowledge refiner, etc. Details are discussed in Section C.2.

4.3 Main Results
We have performed evaluations to validate the efficiency of our
Med-R2 on open-sourced models across different parameter scales.
The main results of baselines and Med-R2 are demonstrated in
Table 2, and we summarize the observations below.

Med-R2 is effective across different models. Table 2 shows
that the incorporation of external knowledge bases significantly
enhances the model’s ability to address medical queries, where even
the most basic vanilla RAG method depicts an average enhance-
ment of 13.10% over direct responses. Furthermore, Med-R2 provides
an added layer of the enhancement by adhering to the EBM process,
which outperforms all baselines across benchmarks, achieving an
average improvement of 28.10% over the direct response strategy.
Notably, for lightweight models such as LLaMA3.1-8B, Med-R2
demonstrates increases of 61.43%. We surmise that this is due to the
fact that while lightweight models inherently lack comprehensive
domain-specific medical knowledge, they possess the capability
to efficiently read and identify information from external medical
documents. Consequently, effective augmentation from external
knowledge substantially bolsters the models’ capacity to tackle
medical-domain questions. Compared with medical-specific models

2

Med-R

: Crafting Trustworthy LLM Physicians via Retrieval and Reasoning of Evidence-Based Medicine

WWW ’26, April 13–17, 2026, Dubai, UAE.

of the same parameter scale, models equipped with Med-R2 demon-
strate superior performance in medical tasks. Moreover, LLaMA3.1-
70B + Med-R2 has the potential to surpass frontier models under
medical scenarios, achieving average improvements over GPT-4o,
Claude3.5-Sonnet and DeepSeek-V3 by 1.05%, 6.14% and 1.91%.

Med-R2 shows superiority compared to fine-tuning. From
Table 2, we find that Med-R2 stands out as the only approach among
those leveraging external knowledge that surpasses the average
performance of fine-tuning methods. Specifically, Med-R2 exhibits
nearly equivalent performance to fine-tuning strategies in within-
dataset training, yet it significantly outperforms in cross-dataset
training, achieving an enhancement of 7.61% and an overall capa-
bility improvement of 4.55%. One contributing factor is that during
within-dataset fine-tuning, the training and testing datasets are
of the same origin, thus a model trained on homogeneous data
could achieve substantial performance gains on the test set. Con-
versely, in cross-dataset fine-tuning, the heterogeneity between the
training and testing datasets more rigorously assesses the model’s
ability of generalization. Under these circumstances, the utilization
of a comprehensive external medical knowledge base and the ef-
fective retrieval and extraction of pertinent information becomes
particularly crucial. Additionally, considering that fine-tuning ne-
cessitates additional training time and computational resources,
Med-R2 emerges as a more efficient approach for enhancing the
model’s performance on medical domain-related issues.

5 Ablations and Analysis Across Scales
We further analyze the impact of model scale and context window
length on Med-R2 , and provide rationale for incorporating the CoT
sequences of models into the retrieval process starting from the
second iteration. Additionally, we have also ablate the components
of Med-R2 in Table 3 to identify the contribution of each module.
Integrating CoT at the onset may bring adverse effects.
We ablate the components of query reformulator 𝑞𝐸𝐵𝑀 [+𝑞𝐶𝑜𝑇 ]
through integrating the chain-of-thought (CoT) sequences gener-
ated by models into the initial evidence retrieval phase, which is
denoted as Med-R2-CoT . Figure 6 presents the medical task per-
formance of Med-R2-CoT and all baselines included in our main
experiments. It is observed that Med-R2-CoT exhibits a decline in
performance compared to Med-R2, with the disparity increasing as
the model parameter scale decreases. Notably, at the 8 billion pa-
rameter level (e.g., LLaMA3.1-8B), the performance of Med-R2-CoT
is even inferior to that of the vanilla RAG strategy. We hypothesize
that one contributing factor is that the lightweight models’ less
solid grasp of medical knowledge. As a result, in the absence of
external medical knowledge, models of these scales may struggle
to align the direction of their thinking with the original query, and
thus, the generated CoT sequences may even negatively impact
the retrieval effectiveness. However, this phenomenon is somewhat
mitigated as the model parameter scale increases.

Effect of context window scale on model’s performance. We
compared the performance of Med-R2 across models with varying
parameter scales and different context window lengths on medical
tasks, and then plotted heatmaps illustrating the percentage im-
provement of Med-R2 over direct responses, as depicted in Figure 7.
It reveals that Med-R2 exhibits an optimal context window length

Figure 6: Average evaluation results of baselines from Table 2
and Med-R2-CoT. Compared to Med-R2, Med-R2-CoT involves
the immediate incorporation of models’ CoT sequence into
the query reformulator for retrieval during the initial round.

Figure 7: The percentage increase of performance achieved by
Med-R2 over direct responses across various context window
sizes and model scales.

for enhancing the model’s medical performance, which increases
with the growth of model parameter size. Concurrently, the en-
hancement of Med-R2 follows a trend of initial decline followed by
an increase with the escalation of model scale. Specifically:
• For models of 8B parameters, the most pronounced enhancement
was observed at a 4K context window, but this benefit diminished
sharply as the context length increased.

• For 14B models, the 8K length stands out, where a measurable
decrease in performances is observed as the context window
expanded. Moreover, the improvement provided by Med-R2 at
this scale is the most modest compared to others.

• Models with 32B and 70B parameters achieved optimal perfor-
mance at a 16K context length, demonstrating relatively stable
improvement across various context window lengths.
We hypothesize that as the context length increases, the role
of Med-R2’s reranker diminishes since most retrieved documents
are fed into the same context window of the model. At this point,
lightweight models, particularly those around 8B, which may not
have a solid grasp of medical knowledge, and overly long sequences

020406080100LLaMA3.1-8BQwen2.5-14BQwen2.5-32BLLaMA3.1-70B22Direct ResponseVanilla RAGFine-TuningLLM-AMTMed-RMed-R -CoTMed-R -CoT2Med-R -CoT2Med-R -CoT2Med-R -CoT233.91Direct Response45.89Direct Response52.03Direct Response56.69Direct Response44.51Vanilla RAG50.27Vanilla RAG55.33Vanilla RAG63.10Vanilla RAG50.73Fine-Tuning54.75  Fine-Tuning57.15Fine-Tuning68.35
Fine-Tuning47.16LLM-AMT52.54LLM-AMT55.93LLM-AMT66.22LLM-AMT54.74Med-R257.43Med-R259.29Med-R270.04Med-R240.8353.6257.9669.574K8K16K32K64K128K70B32B14B8B32.7916.975.7377.0635.658.0937.6435.0634.3532.568.518.238.397.3424.5820.3816.5815.7711.8574.7968.9854.3749.9436.32Context Window ScaleModel ScaleWWW ’26, April 13–17, 2026, Dubai, UAE.

Keer Lu et al.

Table 3: Module analysis of Med-R2 . We sequentially integrate various modules onto the vanilla RAG systems to conduct
comparative analyses. We highlight the optimal performance values for models with single and dual component additions.

Model

Method

MedQA-USMLE MedQA-MCMLE MedMCQA PubMedQA MMLU-Med Average

LLaMA3.1-8B

Qwen2.5-14B

Qwen2.5-32B

LLaMA3.1-70B

Direct Response
Vanilla RAG
+ Query Reformulator
+ Evidence Reranker
+ CoT Generator
+ Query Reformulator, Evidence Reranker
+ Query Reformulator, CoT Generator
+ Evidence Reranker, CoT Generator
Med-R2 (ours)

Direct Response
Vanilla RAG
+ Query Reformulator
+ Evidence Reranker
+ CoT Generator
+ Query Reformulator, Evidence Reranker
+ Query Reformulator, CoT Generator
+ Evidence Reranker, CoT Generator
Med-R2 (ours)

Direct Response
Vanilla RAG
+ Query Reformulator
+ Evidence Reranker
+ CoT Generator
+ Query Reformulator, Evidence Reranker
+ Query Reformulator, CoT Generator
+ Evidence Reranker, CoT Generator
Med-R2 (ours)

Direct Response
Vanilla RAG
+ Query Reformulator
+ Evidence Reranker
+ CoT Generator
+ Query Reformulator, Evidence Reranker
+ Query Reformulator, CoT Generator
+ Evidence Reranker, CoT Generator
Med-R2 (ours)

31.16
55.80
62.47
68.62
59.87
74.41
70.86
72.69
77.01

50.01
54.88
54.93
55.03
54.62
55.38
54.77
54.81
54.34

16.23
19.33
20.14
20.83
19.78
23.04
21.97
23.01
24.43

46.43
62.66
70.82
73.96
68.08
80.41
78.62
81.93
86.37

41.45
59.38
72.85
75.74
65.63
81.68
77.43
79.84
84.16

65.23
75.60
78.96
78.83
76.72
82.04
80.58
81.79
80.19

87.07
89.30
89.42
89.88
88.69
89.25
89.56
89.75
90.01

58.36
77.91
80.64
80.78
78.65
84.09
82.56
82.97
84.58

30.02
35.91
41.66
43.84
39.45
47.71
44.83
45.12
52.33

42.85
42.06
45.43
45.97
43.86
48.29
47.61
47.87
48.36

66.44
67.63
68.72
68.88
67.94
70.35
69.06
69.75
69.09

62.33
66.63
69.72
70.87
68.85
73.01
72.71
72.88
73.36

36.17
47.10
48.72
49.97
47.71
53.96
51.75
52.25
52.75

56.93
60.38
64.85
65.08
62.13
67.02
66.98
67.48
68.32

68.66
67.06
68.41
68.47
67.72
68.89
68.56
69.00
68.36

66.81
68.78
71.82
74.64
70.09
77.80
76.06
76.52
78.24

37.12
43.54
43.98
43.76
43.61
44.23
44.02
44.00
45.19

71.60
79.46
81.73
81.56
80.02
83.17
82.21
82.95
84.03

80.19
83.85
83.97
83.99
83.92
84.46
84.08
84.39
84.95

71.33
76.95
73.56
75.28
73.72
80.68
78.56
81.62
82.82

35.18
48.35
53.94
56.34
51.25
60.40
57.78
58.78
62.29

57.32
62.48
65.18
65.29
63.47
67.18
66.43
66.98
67.05

63.72
65.43
66.13
66.41
65.61
67.20
66.65
67.18
67.37

61.05
70.59
73.31
75.11
71.88
79.20
77.70
79.18
81.07

could reduce the model’s efficiency in extracting key information,
potentially leading to the generation of hallucinations and adversely
affecting the model’s medical performance. However, the addition of
other modules, such as the query reformulator, can help improve the
precision of knowledge retrieval, thereby mitigating this negative
impact to some extent. In contrast, models with 32B and higher
scales exhibit greater robustness, and the impact of increasing the
window length on Med-R2’s effectiveness is less pronounced.

Module Impact Analysis. We have analyzed the contributions
of various modules in Med-R2 to the model’s performance in the
medical domain using a default context window size of 4K, sequen-
tially incorporating components into the vanilla RAG framework.
As shown in Table 3, we decompose the modules into three compo-
nents: query reformulator, evidence reranker, and CoT gener-
ator. Overall, the evidence reranker contributed the most to models’
performances among the individual components. When combined
with the query reformulator, the performance gains were even more

pronounced, showing a synergistic effect. The addition of the CoT
generator further enhanced the model’s ability to effectively utilize
retrieved medical documents, providing substantial added value.

6 Discussion
In this study, we follow the Evidence-Based Medicine (EBM) process
to design a novel LLM physician framework, which effectively lever-
ages the retrieval, filtering, and reasoning processes inherent to
EBM. Experiments demonstrate that Med-R2 holds superior advan-
tages over existing strategies, while also reducing the substantial
computational costs associated with model training. Furthermore,
our analysis of model scale and context window size also highlights
the scaling capabilities of Med-R2. By scaling the model parame-
ters and adjusting the context window length, we demonstrate the
robustness of Med-R2 in achieving optimal performance across a
broad spectrum of medical tasks.

2

Med-R

: Crafting Trustworthy LLM Physicians via Retrieval and Reasoning of Evidence-Based Medicine

WWW ’26, April 13–17, 2026, Dubai, UAE.

References
[1] Alaa Abd-Alrazaq, Rawan AlSaad, Dari Alhuwail, Arfan Ahmed, Padraig Mark
Healy, Syed Latifi, Sarah Aziz, Rafat Damseh, Sadam Alabed Alrazak, Javaid
Sheikh, et al. 2023. Large language models in medical education: opportunities,
challenges, and future directions. JMIR Medical Education 9, 1 (2023), e48291.
[2] Anthropic. 2024. Claude. https://www.anthropic.com/ Accessed: 2024-06-27.
[3] Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi. 2023.
Self-rag: Learning to retrieve, generate, and critique through self-reflection. In
The Twelfth International Conference on Learning Representations.

[4] Felix Busch, Lena Hoffmann, Christopher Rueger, Elon HC van Dijk, Rawen
Kader, Esteban Ortiz-Prado, Marcus R Makowski, Luca Saba, Martin Hadamitzky,
Jakob Nikolas Kather, et al. 2024. Systematic Review of Large Language Models
for Patient Care: Current Applications and Challenges. medRxiv (2024), 2024–03.
[5] Susan M Case and David B Swanson. 1998. Constructing written test questions for
the basic and clinical sciences. National Board of Medical Examiners Philadelphia.
[6] Zeming Chen, Alejandro Hernández Cano, Angelika Romanou, Antoine Bonnet,
Kyle Matoba, Francesco Salvi, Matteo Pagliardini, Simin Fan, Andreas Köpf,
Amirkeivan Mohtashami, et al. 2023. Meditron-70b: Scaling medical pretraining
for large language models. arXiv preprint arXiv:2311.16079 (2023).

[7] Jan Clusmann, Fiona R Kolbinger, Hannah Sophie Muti, Zunamys I Carrero,
Jan-Niklas Eckardt, Narmin Ghaffari Laleh, Chiara Maria Lavinia Löffler, Sophie-
Caroline Schwarzkopf, Michaela Unger, Gregory P Veldhuizen, et al. 2023. The
future landscape of large language models in medicine. Communications medicine
3, 1 (2023), 141.

[8] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad
Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan,
et al. 2024. The llama 3 herd of models. arXiv preprint arXiv:2407.21783 (2024).
[9] Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai,
Jiawei Sun, and Haofen Wang. 2023. Retrieval-augmented generation for large
language models: A survey. arXiv preprint arXiv:2312.10997 (2023).

[10] Gordon Guyatt, John Cairns, David Churchill, Deborah Cook, Brian Haynes,
Jack Hirsh, Jan Irvine, Mark Levine, Mitchell Levine, Jim Nishikawa, et al. 1992.
Evidence-based medicine: a new approach to teaching the practice of medicine.
Jama 268, 17 (1992), 2420–2425.

[11] Gordon H Guyatt, R Brian Haynes, Roman Z Jaeschke, Deborah J Cook, Lee
Green, C David Naylor, Mark C Wilson, W Scott Richardson, Evidence-Based
Medicine Working Group, Evidence-Based Medicine Working Group, et al. 2000.
Users’ guides to the medical literature: XXV. Evidence-based medicine: principles
for applying the users’ guides to patient care. Jama 284, 10 (2000), 1290–1296.

[12] Paul Hager, Friederike Jungmann, Robbie Holland, Kunal Bhagat, Inga Hubrecht,
Manuel Knauer, Jakob Vielhauer, Marcus Makowski, Rickmer Braren, Georgios
Kaissis, et al. 2024. Evaluation and mitigation of the limitations of large language
models in clinical decision-making. Nature medicine 30, 9 (2024), 2613–2622.
[13] Kai Hakala, Suwisa Kaewphan, Tapio Salakoski, and Filip Ginter. 2016. Syntactic
analyses and named entity recognition for PubMed and PubMed Central — up-to-
the-minute. In Proceedings of the 15th Workshop on Biomedical Natural Language
Processing, Kevin Bretonnel Cohen, Dina Demner-Fushman, Sophia Ananiadou,
and Jun-ichi Tsujii (Eds.). Association for Computational Linguistics, Berlin,
Germany, 102–107.

[14] Hangfeng He, Hongming Zhang, and Dan Roth. 2022. Rethinking with retrieval:
Faithful large language model inference. arXiv preprint arXiv:2301.00303 (2022).
[15] Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn
Song, and Jacob Steinhardt. 2021. Measuring Massive Multitask Language Under-
standing. Proceedings of the International Conference on Learning Representations
(ICLR) (2021).

[16] Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh,
Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford, et al. 2024.
Gpt-4o system card. arXiv preprint arXiv:2410.21276 (2024).

[17] Gautier Izacard, Patrick Lewis, Maria Lomeli, Lucas Hosseini, Fabio Petroni,
Timo Schick, Jane Dwivedi-Yu, Armand Joulin, Sebastian Riedel, and Edouard
Grave. 2023. Atlas: Few-shot learning with retrieval augmented language models.
Journal of Machine Learning Research 24, 251 (2023), 1–43.

[18] Minbyul Jeong, Jiwoong Sohn, Mujeen Sung, and Jaewoo Kang. 2024. Improving
medical reasoning through retrieval and self-reflection with retrieval-augmented
large language models. Bioinformatics 40, Supplement_1 (2024), i119–i129.
[19] Soyeong Jeong, Jinheon Baek, Sukmin Cho, Sung Ju Hwang, and Jong C Park.
2024. Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language
Models through Question Complexity. In Proceedings of the 2024 Conference of the
North American Chapter of the Association for Computational Linguistics: Human
Language Technologies (Volume 1: Long Papers). 7029–7043.

[20] Di Jin, Eileen Pan, Nassim Oufattole, Wei-Hung Weng, Hanyi Fang, and Peter
Szolovits. 2020. What Disease does this Patient Have? A Large-scale Open Domain
Question Answering Dataset from Medical Exams. arXiv preprint arXiv:2009.13081
(2020).

[21] Qiao Jin, Bhuwan Dhingra, Zhengping Liu, William Cohen, and Xinghua Lu.
2019. PubMedQA: A Dataset for Biomedical Research Question Answering. In

Proceedings of the 2019 Conference on Empirical Methods in Natural Language Pro-
cessing and the 9th International Joint Conference on Natural Language Processing
(EMNLP-IJCNLP). 2567–2577.

[22] Qiao Jin, Robert Leaman, and Zhiyong Lu. 2023. Retrieve, summarize, and verify:
how will ChatGPT affect information seeking from the medical literature? Journal
of the American Society of Nephrology 34, 8 (2023), 1302–1304.

[23] Jeff Johnson, Matthijs Douze, and Hervé Jégou. 2019. Billion-scale similarity

search with GPUs. IEEE Transactions on Big Data 7, 3 (2019), 535–547.

[24] Nikhil Kandpal, Haikang Deng, Adam Roberts, Eric Wallace, and Colin Raffel.
2023. Large language models struggle to learn long-tail knowledge. In Interna-
tional Conference on Machine Learning. PMLR, 15696–15707.

[25] Uriel Katz, Eran Cohen, Eliya Shachar, Jonathan Somer, Adam Fink, Eli Morse,
Beki Shreiber, and Ido Wolf. 2024. GPT versus resident physicians—a benchmark
based on official board scores. Nejm Ai 1, 5 (2024), AIdbp2300192.

[26] Yubin Kim, Chanwoo Park, Hyewon Jeong, Yik Siu Chan, Xuhai Xu, Daniel
McDuff, Hyeonhoon Lee, Marzyeh Ghassemi, Cynthia Breazeal, and Hae Won
Park. 2024. Mdagents: An adaptive collaboration of llms for medical decision-
making. In The Thirty-eighth Annual Conference on Neural Information Processing
Systems.

[27] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin,
Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel,
et al. 2020. Retrieval-augmented generation for knowledge-intensive nlp tasks.
Advances in Neural Information Processing Systems 33 (2020), 9459–9474.
[28] Yunxiang Li, Zihan Li, Kai Zhang, Ruilong Dan, Steve Jiang, and You Zhang. 2023.
Chatdoctor: A medical chat model fine-tuned on a large language model meta-ai
(llama) using medical domain knowledge. Cureus 15, 6 (2023).

[29] Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Cheng-
gang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al. 2024. Deepseek-v3
technical report. arXiv preprint arXiv:2412.19437 (2024).

[30] Cui Long, Yongbin Liu, Chunping Ouyang, and Ying Yu. 2024. Bailicai: A Domain-
Optimized Retrieval-Augmented Generation Framework for Medical Applications.
arXiv preprint arXiv:2407.21055 (2024).

[31] Renqian Luo, Liai Sun, Yingce Xia, Tao Qin, Sheng Zhang, Hoifung Poon, and
Tie-Yan Liu. 2022. BioGPT: generative pre-trained transformer for biomedical
text generation and mining. Briefings in bioinformatics 23, 6 (2022), bbac409.
[32] Ummara Mumtaz, Awais Ahmed, and Summaya Mumtaz. 2024. LLMs-Healthcare:
Current applications and challenges of large language models in various medical
specialties. Artificial Intelligence in Health 1, 2 (2024), 16–28.

[33] Ankit Pal, Logesh Kumar Umapathi, and Malaikannan Sankarasubbu. 2022.
Medmcqa: A large-scale multi-subject multi-choice dataset for medical domain
question answering. In Conference on health, inference, and learning. PMLR, 248–
260.

[34] David L Sackett. 1997. Evidence-based medicine. In Seminars in perinatology,

Vol. 21. Elsevier, 3–5.

[35] David L Sackett, William MC Rosenberg, JA Muir Gray, R Brian Haynes, and
W Scott Richardson. 1996. Evidence based medicine: what it is and what it isn’t.
71–72 pages.

[36] Karan Singhal, Shekoofeh Azizi, Tao Tu, S Sara Mahdavi, Jason Wei, Hyung Won
Chung, Nathan Scales, Ajay Tanwani, Heather Cole-Lewis, Stephen Pfohl, et al.
2023. Large language models encode clinical knowledge. Nature 620, 7972 (2023),
172–180.

[37] Karan Singhal, Tao Tu, Juraj Gottweis, Rory Sayres, Ellery Wulczyn, Le Hou,
Kevin Clark, Stephen Pfohl, Heather Cole-Lewis, Darlene Neal, et al. 2023. To-
wards expert-level medical question answering with large language models. arXiv
preprint arXiv:2305.09617 (2023).

[38] Arun James Thirunavukarasu, Darren Shu Jeng Ting, Kabilan Elangovan, Laura
Gutierrez, Ting Fang Tan, and Daniel Shu Wei Ting. 2023. Large language models
in medicine. Nature medicine 29, 8 (2023), 1930–1940.

[39] THUMedInfo. 2025. RareArena: A Dataset for Rare Disease Information Retrieval.

https://huggingface.co/datasets/THUMedInfo/RareArena

[40] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yas-
mine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhos-
ale, et al. 2023. Llama 2: Open foundation and fine-tuned chat models. arXiv
preprint arXiv:2307.09288 (2023).

[41] Satvik Tripathi, Rithvik Sukumaran, and Tessa S Cook. 2024. Efficient healthcare
with large language models: optimizing clinical workflow and enhancing patient
care. Journal of the American Medical Informatics Association 31, 6 (2024), 1436–
1440.

[42] Yubo Wang, Xueguang Ma, and Wenhu Chen. 2024. Augmenting Black-box LLMs
with Medical Textbooks for Biomedical Question Answering. In Findings of the
Association for Computational Linguistics: EMNLP 2024. 1754–1770.

[43] Chaoyi Wu, Weixiong Lin, Xiaoman Zhang, Ya Zhang, Weidi Xie, and Yanfeng
Wang. 2024. PMC-LLaMA: toward building open-source language models for
medicine. Journal of the American Medical Informatics Association (2024), ocae045.
[44] Mengzhou Xia, Tianyu Gao, Zhiyuan Zeng, and Danqi Chen. 2023. Sheared llama:
Accelerating language model pre-training via structured pruning. arXiv preprint
arXiv:2310.06694 (2023).

WWW ’26, April 13–17, 2026, Dubai, UAE.

Keer Lu et al.

[45] Guangzhi Xiong, Qiao Jin, Zhiyong Lu, and Aidong Zhang. 2024. Benchmarking
retrieval-augmented generation for medicine. In Findings of the Association for
Computational Linguistics ACL 2024. 6233–6251.

[46] Guangzhi Xiong, Qiao Jin, Xiao Wang, Minjia Zhang, Zhiyong Lu, and Aidong
Zhang. 2024. Improving retrieval-augmented generation in medicine with it-
erative follow-up questions. In Biocomputing 2025: Proceedings of the Pacific
Symposium. World Scientific, 199–214.

[47] An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu,
Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, et al. 2024. Qwen2. 5
Technical Report. arXiv preprint arXiv:2412.15115 (2024).

[48] Rui Yang, Ting Fang Tan, Wei Lu, Arun James Thirunavukarasu, Daniel Shu Wei
Ting, and Nan Liu. 2023. Large language models in health care: Development,
applications, and challenges. Health Care Science 2, 4 (2023), 255–263.

[49] Cyril Zakka, Rohan Shad, Akash Chaurasia, Alex R Dalal, Jennifer L Kim, Michael
Moor, Robyn Fong, Curran Phillips, Kevin Alexander, Euan Ashley, et al. 2024.
Almanac—retrieval-augmented language models for clinical medicine. NEJM AI
1, 2 (2024), AIoa2300068.

[50] Guangtao Zeng, Wenmian Yang, Zeqian Ju, Yue Yang, Sicheng Wang, Ruisi Zhang,
Meng Zhou, Jiaqi Zeng, Xiangyu Dong, Ruoyu Zhang, et al. 2020. MedDialog:
Large-scale medical dialogue datasets. In Proceedings of the 2020 conference on
empirical methods in natural language processing (EMNLP). 9241–9250.

[51] Penghao Zhao, Hailin Zhang, Qinhan Yu, Zhengren Wang, Yunteng Geng,
Fangcheng Fu, Ling Yang, Wentao Zhang, and Bin Cui. 2024. Retrieval-augmented
generation for ai-generated content: A survey. arXiv preprint arXiv:2402.19473
(2024).

[52] Yuxin Zuo, Shang Qu, Yifei Li, Zhangren Chen, Xuekai Zhu, Ermo Hua, Kaiyan
Zhang, Ning Ding, and Bowen Zhou. 2025. MedXpertQA: Benchmarking Expert-
Level Medical Reasoning and Understanding. arXiv preprint arXiv:2501.18362
(2025).

Appendix

Evidence-Based Medicine (EBM)
Method Details

Question Formulation Details
Knowledge Corpus Details
Evidence Reranking Details
Evidence Assessment Details

Experiments Details

Details of Medical Datasets
Details of Baselines
Hyper-Parameters Setting

Scaling Analysis and Ablation Details
Case Studies
Prompts

A
B
B.1
B.2
B.3
B.4
C
C.1
C.2
C.3
D
E
F

10
10
10
11
11
11
11
11
13
13
13
14
18

A Evidence-Based Medicine (EBM)
Evidence-Based Medicine (EBM) is defined as the conscientious,
explicit, and judicious application of the best current evidence in
making decisions regarding the care of individual patients. This
practice entails the integration of individual clinical expertise with
the most reliable external clinical evidence derived from systematic
research [35]. The EBM process typically includes five stages, ques-
tion formulating, evidence searching, evidence appraising, evidence
applying and effect assessing, which aims to make the best possible
health care decision through iterative improvements. To utilize
“best evidence”, researchers assess the quality of trials by determin-
ing the grading system based on the likelihood that the methods
used and the results obtained are less prone to bias and more reliable.
The hierarchy of evidence guides the clinical decision-making,
since not all evidence is created equal, as described in Figure 4.

The evidence hierarchy establishes the priority of references, par-
ticularly when conflicting facts are present within the retrieved
evidence. The construction and rationale behind the hierarchical
structure of evidence grading is outlined from the highest to the
lowest levels:
• Systematic Reviews/Meta-Analyses (SR/MA) represent the
highest tier of evidence. These assessments evaluate the consis-
tency and risk of bias across all research findings within the
medical domain, demonstrating the overall effect of exposures.
• Randomized Controlled Trials (RCTs) constitute the second-
highest level of evidence. These trials aim to minimize confound-
ing biases and examine the causal relationships between inter-
vention measures and outcomes across groups.

• Cohort Studies fall into the third-highest category of evidence.
Both retrospective and prospective cohort studies are prone to
various biases. Prospective cohort studies are considered more
reliable, less susceptible to information biases (selection, mis-
classification, recall), and can establish temporal associations
(outcomes following exposure). However, these cohort studies
may suffer from confounding biases, which is a major concern
that can undermine the validity of their findings.

• Case-Control Studies are a form of observational research and
rank as the fourth-highest level of evidence. These studies attempt
to identify associations between outcomes and exposure to risk
factors after the outcomes have occurred. Case-control studies
are susceptible to selection, information, and confounding biases,
reducing their credibility compared to cohort studies.

• Individual Case Reports are of the second-lowest evidence level,
essentially uncontrolled cohort studies lacking a comparison
group. The absence of a control group affects the correlation
between study variables, interventions factors and outcomes.
• Expert Opinion is considered the lowest level of evidence due
to its high susceptibility to bias. Compared to other levels, ex-
perts tend to choose evidence that confirms their preconceived
hypotheses, potentially leading to conflicts of interest and a focus
on a specific domain while overlooking broader contexts, thereby
introducing bias into their perspectives.

B Method Details
B.1 Question Formulation Details
B.1.1 Details of Query Classification. We categorize the medical
queries along two orthogonal dimensions: Evidence-Based Medicine
(EBM) categories and general natural language question types.

Evidence-Based Medicine (EBM) Categories Nonprofes-
sional queries may fail to clearly articulate the current medical
symptoms, thereby hindering the effective retrieval of the necessary
evidence. We classify medical queries into several types according
to the categories of Evidence-Based Medicine (EBM) questions, in-
cluding diagnosis, therapy, prognosis, etiology, prevention, cost, etc.,
and then conduct professional medical query reformulations based
on their EBM categorization to emphasize specialized retrieval. In-
structions for targeted augmentation of clinical queries are outlined
in Table 4, where we employ Qwen2.5-72B-Instruct7 fine-tuned on
our 100 manually annotated samples as our question reformulator.

7https://huggingface.co/Qwen/Qwen2.5-72B-Instruct

2

Med-R

: Crafting Trustworthy LLM Physicians via Retrieval and Reasoning of Evidence-Based Medicine

WWW ’26, April 13–17, 2026, Dubai, UAE.

General Natural Language Question Types

It serves as a
crucial reference for filtering and reranking the documents retrieved
in response to a query, since the emphasis of the expected answer
varies with different question types. We categorize queries into 12
natural language classes, as illustrated in Table 5, establishing a
mapping between the types of questions and that of evidence to
form a question-answer typology (depicted in Figure 5).

B.1.2 Details of Query Reformulator. Following the instructions
outlined in Table 4, we have manually annotated 120 samples (20
samples for each EBM category) to fine-tune the Qwen2.5-72B-
Instruct model, and employed the trained model to professionally
reformulate the queries within the medical datasets to enhance the
subsequent retrieval of relevant evidence pertaining to the current
query from the knowledge corpus.

B.2 Knowledge Corpus Details
We organized the medical knowledge corpus from four data sources:
academic papers, entries, books, and guidelines, as listed below:
• Academic Papers Academic literature provide valuable in-
sights derived from the latest scientific investigations, offering
a robust theoretical foundation for guiding clinical practice and
informing public health decisions. We obtained the publicly avail-
able literature from PubMed Central (PMC)8, and exracted valid
contents following the processing pipeline of Hakala et al. [13].
• Entries Medical entries provide valuable information across
multiple dimensions of healthcare, from direct patient care to
cutting-edge research. We extracted and curated medical-related
data from the Wikipedia dataset9 to build the entries. In the end,
we got approximately 470k documents.

• Books Medical textbooks are vital resources for medical knowl-
edge retrieval, which can be consulted when faced with complex
cases or when seeking updated knowledge about specific condi-
tions. We gathered books from NCBI Bookshelf10, and collected
10k documents following the process of Hakala et al. [13].

• Guidelines Clinical practice guidelines serve as essential tools
in Evidence-Based Medicine (EBM), aiding healthcare providers
in making informed decisions for diagnosis and treatment. We
utilized the guideline data when training MEDITRON series
from Chen et al. [6], and gained approximately 10k documents.

B.3 Evidence Reranking Details
B.3.1 Components of Fine-Grained Reranker. We detail the scoring
clarification and implementation for the fine-grained reranking
phase of retrieved documents from Equation (1).
• Hierarchy of Evidence 𝑓ℎ (𝑥): It should be clarified that for the
guideline-sourced data retrieved from the knowledge corpus, we
assign the 𝑓ℎ score directly to 7 (𝑒 = 3) based on the evidence level
depicted in Figure 4. It is because the grading system of evidence
hierarchy explicitly designates a specific level for guideline data.
• Usefulness 𝑓𝑢 (𝑥): 1) Regarding the lightweight proxy models we
employed for scoring usefulness 𝑓𝑢 of the retrieved documents,
for the LLaMA series, we used the Sheared-LLaMA-1.3B [44] as

8https://pmc.ncbi.nlm.nih.gov/
9https://huggingface.co/datasets/wikimedia/wikipedia
10https://www.ncbi.nlm.nih.gov/books/

a lightweight reference model; for the Qwen series, we utilized
Qwen-2.5-1.5B [47]. 2) Moreover, to avoid potential label leakage
when computing 𝑓𝑢 in Equation (3), we have implemented strate-
gies to ensure that the entire framework does not have access
to ground truth answers (labels) during the deployment phase,
where we employed frontier models’ responses to serve as the
“reference answers” for consultation throughout the framework’s
operation. Specifically, we utilized the training subsets from
MedQA-USMLE, MedQA-MCMLE [20], and MedMCQA [33] to
fine-tune the Qwen2.5-72B-Instruct11 model, resulting in model
𝑀𝐹 . We replaced the labels with responses generated by model
𝑀𝐹 for the current medical question.

• General Document Category 𝑓𝑔 (𝑥): The calculation is based on
the categorization and mapping to general document categories,
as depicted in Algorithm 1. For this categorization, advanced lan-
guage models provide probabilities. In addition, the relationship
between the general question category and the general document
category is multifaceted (illustrated in Figure 5), which further
enhances the robustness of category assignment.

B.3.2 Explanation for Equation Derivation. We have chosen Equa-
tion (1) in the form of multiplication instead of additive scoring
primarily for the following two reasons:
• Multi-Variable Synergy: The multiplicative structure empha-
sizes the synergistic effect, preventing any single variable from
dominating. It is necessary for all variables to reach a certain
value simultaneously to achieve the expected outcomes. For in-
stance, if 𝑓ℎ (𝑥) or 𝑓𝑔 (𝑥) approaches a lower bound (e.g., 𝑓𝑔 (𝑥) →
0), even if the usefulness score 𝑓𝑢 (𝑥) is extremely high, the final
outcome F (𝑥) will still tend towards 0.

• Metric Self-Adaptation: The value ranges of the variables differ
significantly (e.g., 𝑓ℎ (𝑥) ∈ [1, 9], 𝑓𝑔 (𝑥) ∈ (0, 1), 𝑓𝑢 (𝑥) ∈ [0, +∞)).
Equation (1) built upon the multiplicative formula naturally bal-
ances the scales of these variables. In contrast, the weighted
summation approach requires manual normalization of variables.

B.4 Evidence Assessment Details
Here, we provide the details of the iterative multi-document re-
trieval process, as illustrated in Algorithm 2.

• Integration of CoT Sequences

It is important to note that
during the initial retrieval phase, we did not incorporate the
generated CoT sequences as part of the query reformulation
𝑞𝐸𝐵𝑀 [+𝑞𝐶𝑜𝑇 ]. Instead, this component was integrated in the
second iteration, where we have shown the rationale in Section 5.

C Experiments Details
C.1 Details of Medical Datasets
For MedQA-USMLE and MedQA-MCMLE, the original data is di-
vided into three parts: train, dev, and test. We utilize the training
part directly for model fine-tuning. The dev and test subsets are
merged for evaluation, from which we selected 10 (or 11) instances
as Chain-of-Thought (CoT) demonstration examples. Since the test
portion of MedMCQA does not provide ground truth answers, we
use the development set for evaluation. We employ MedQA-USMLE,

11https://huggingface.co/Qwen/Qwen2.5-72B-Instruct

WWW ’26, April 13–17, 2026, Dubai, UAE.

Keer Lu et al.

(a) Query category of MedQA-USMLE.

(b) Query category of MedQA-MCMLE.

(c) Query category of PubMedQA.

(d) Query category of MMLU-Med.

Figure 8: Query categories of different medical datasets. We employ a 3D bar chart to represent the number of instances in
each category within the two distinct classification systems of the current dataset. A logarithmic scale (base 10) on the z-axis,
ranging from 1 to 𝑧 (𝑧 = 100, 140, 4000), is utilized to represent the wide range of values.

Table 4: Prompts for query reformulation of each category within the Evidence-Based Medicine (EBM) categories.

Category

Diagnosis

Therapy

Prognosis

Etiology

Prevention

Cost

Instructions for Query Reformulation

Specify the condition you need to diagnose and ask about the accuracy, sensitivity, or specificity of specific diagnostic tests.

Specify the disease or symptom along with the therapy being considered, and inquire about its effectiveness, safety, or comparison with other therapies.

Specify the disease or condition and ask about long-term outcomes such as survival rates, recovery chances, or disease progression.

Describe the health issue and ask about potential causes, including risk factors, pathogens, or genetic background.

Specify the disease or health issue and ask about the effectiveness of preventive measures or recommendations.

Specify the medical intervention or service and ask about cost-effectiveness analyses, including direct and indirect costs and cost-effectiveness ratios.

CostDiagnosisEtiologyPreventionPrognosisTherapyVerificationReferentialProceduralOpinionHypotheticalFactualExplanatoryEvaluativeDirectiveDescriptiveDefinitionalComparative101001000200030004000Query Categories of MedQA-USMLE5001000150020002500300035004000Query Categories of MedQA-MCMLE5001000150020002500300035004000CostDiagnosisEtiologyPreventionPrognosisTherapyVerificationReferentialProceduralOpinionHypotheticalFactualExplanatoryEvaluativeDirectiveDescriptiveDefinitionalComparative101001000200030004000CostDiagnosisEtiologyPreventionPrognosisTherapyVerificationReferentialProceduralOpinionHypotheticalFactualExplanatoryEvaluativeDirectiveDescriptiveDefinitionalComparativeQuery Categories of PubMedQA101100203040506070809020406080100Query Categories of MMLU-MedCostDiagnosisEtiologyPreventionPrognosisTherapyVerificationReferentialProceduralOpinionHypotheticalFactualExplanatoryEvaluativeDirectiveDescriptiveDefinitionalComparative2040608010012014011030504060701402080901002

Med-R

: Crafting Trustworthy LLM Physicians via Retrieval and Reasoning of Evidence-Based Medicine

WWW ’26, April 13–17, 2026, Dubai, UAE.

Table 5: Explanations and descriptions for each category
within the general question classification.

Category

Factual

Referential

Definition

Explanatory

Descriptive

Directive

Opinion

Procedural

Comparative

Evaluative

Verification

Hypothetical

Details of Description

Inquiring into specific and objective facts or data.

Seeking answers by referencing specific documents, resources, or other information.

Inquiring about the definition or explanation of a concept or entity.

Seeking explanations for the causes of phenomena, processes, or events.

Requesting a description of the characteristics, properties, and features of an entity.

Seeking guidance or recommendations.

Pertaining to individual feelings, attitudes, or preferences.

Inquiring about the specific steps to complete a particular task or activity.

Inquiring comparison of the differences between two or more entities.

Assessing the validity or quality of a statement or viewpoint.

Confirming or verifying the authenticity or accuracy of certain information.

Presenting a hypothetical scenario and requesting predictions of outcomes.

Table 6: Explanations and descriptions for each category
within the general document classification.

Category

Argumentation

Definition

Description

Explanation

Purpose

Narration

Process

Instruction

Command

Problem-Solving

Comparison

Evaluation

Classification

Condition

Prediction

Cause and Effect

Presenting a viewpoint or argument, potentially accompanied by supporting evidence.

Details of Description

Providing a clear definition of a term or concept.

Describing the characteristics or attributes of an object or event.

Explaining a concept, process, or cause.

Elucidating the purpose or intent behind a particular action or event.

Providing a narrative account of an event, experience, or story.

Describing a process or a sequence of steps.

Providing steps or guidance for executing a task or operation.

Conveying a request that requires the listener to take action.

Proposing methods or strategies for addressing specific issues.

Comparing the similarities or differences between two or more entities.

Articulating a judgment on a particular subject or behavior.

Categorizing objects or concepts into specific categories systems.

Describing the assumptions under which a particular event occurs.

Forecasting future events or trends.

Describing the causal relationships between events.

MedQA-MCMLE, and MedMCQA datasets for within-dataset fine-
tuning. For instance, we train with the training subset of MedQA-
USMLE and subsequently evaluate with its corresponding test parti-
tions. We utilize the remaining datasets for cross-dataset fine-tuning
setting to test the model’s generalizability on disparate data sources.

Table 7: Overall statistics of datasets. We utilize MedQA-
USMLE, MedQA-MCMLE and MedMCQA for within-dataset
fine-tuning, while others for cross-dataset fine-tuning.

Dataset

# Training Instance

# Testing Instance

# N-Shot for CoT # Total Instance

MedQA-USMLE [20]
MedQA-MCMLE [20]
MedMCQA [33]
PubMedQA [21]
MMLU-Med [15]
NEJMQA [25]
MedXpertQA [52]
RareArena [39]

10178
27400
182822
-
-
-
-
-

2535
6840
4170
990
1080
655
2455
72,661

10
11
13
10
9
10
10
10

12723
34251
187005
1000
1089
655
2455
72,661

C.2 Details of Baselines
• Frontier Models: Frontier models are considered to represent
the pinnacle of performance across various dimensions of LLMs,

serving as the strongest baselines. Here, we have selected sev-
eral state-of-the-art LLMs to establish the maximum potential of
model performance on several medical benchmarks, including
GPT-4o [16], Claude3.5-Sonnet [2], and DeepSeek-V3 [29].
• Open-Sourced Medical Models: These models stand for the
domain-specific models that were specifically trained on medical
data. We have selected PMC-LLaMA-7B, PMC-LLaMA-13B [43],
MEDITRON-7B and MEDITRON-70B [6] to represent the open-
sourced medical models for comparison to assess Med-R2’s rela-
tive advantage compared to specialized medical AI systems.
• Direct Response: We employ the base model to directly respond
to medical queries without aid of additional training on any
dataset or augmentation from external knowledge bases.

• Vanilla RAG [27]: It represents the most traditional and funda-
mental strategy for utilizing external knowledge bases to assist
models in answering questions. In this study, we employ the same
medical knowledge base as Med-R2 , but directly utilizing the
raw text retrieved by FAISS and combining it with the original
query to test the model’s performance on medical tasks.

• Within-Dataset Fine-Tuning: The training and test sets origi-
nate from the same distribution, and models exhibit strong per-
formance gains due to the homogeneity of the datasets.

• Cross-Dataset Fine-Tuning: It poses a greater challenge by
testing the model’s ability to generalize across different distribu-
tions, demanding robust transfer learning capabilities, which are
bolstered by the integration of rich external medical knowledge.
• LLM-AMT [42]: LLM-AMT is a RAG system specifically de-
signed for clinical question answering. It incorporates common
RAG components such as a query augmentor, textbook retriever,
knowledge refiner, and an LLM reader. LLM-AMT leverages a
collection of medical textbooks as an external indexable medical
knowledge base. However, in this comparison, we aim to assess
the RAG’s capability to retrieve, filter, and apply evidence from
the same external knowledge base. To control variables, we em-
ploy the LLM-AMT’s process but replace the medical knowledge
base with our own constructed medical retrieval corpus.

C.3 Hyper-Parameters Setting
In the fine-grained reranking phase, we treat each factor as hav-
ing equal importance, hence we set the weight controlling hyper-
parameter 𝛼 in Equation (1) to 1. For retrieval iteration settings, we
performed iterative retrieval on each query within the datasets in
Table 7. Our analysis revealed that after approximately 5 iterations,
the distribution of the retrieved document vectors stabilizes. Conse-
quently, we set the maximum iterations 𝑇 to 5 in Algorithm 2. After
performing iterative retrieval for all samples in the dataset and cal-
culating the average of the minimum distances in the retrieval space
during iterations, we obtained a value of 6.85, which we adopted as
our termination alteration threshold 𝛿 in Algorithm 2.

D Scaling Analysis and Ablation Details
In this section, we conduct a more detailed analysis of the impact
of context window size and model parameter scale on our Med-R2.
Scaling for Context Window The training context windows
length for the LLaMA3.1 series models are explicitly designed to
extend up to a context length of 128K. The Qwen2.5 series, trained

WWW ’26, April 13–17, 2026, Dubai, UAE.

Keer Lu et al.

Figure 9: A case of the t-SNE visualization for retrieved documents. We visualized the projections of document embeddings
onto a 2-D plane across different iterations. It is evident that aside from the significant variation in the retrieval document
vector space at 𝑡 = 2, the semantics of the retrieved documents tend to stabilize in subsequent iterations. It occurs because we
did not incorporate the model’s CoT sequence for the initial retrieval round (𝑡 = 1). Instead, we began to include it starting from
the second iteration onwards (𝑡 = 2) to avoid the generation of sequences that are not only unrealistic but also detrimental to
the precision of evidence document retrieval.

at a 32K context length, can also be extended to 128K by modifying
the max_position_embedding in the config.json file through
Yarn. Consequently, we have chosen two models each from the
LLaMA3.1 series and the Qwen2.5 series to conduct inference tests
on context window length expansion. Experimental results are
outlined in Table 8 and Figure 7.

E Case Studies
Here, we provide concrete examples of query reformulation and CoT
generation to demonstrate the critical importance of these compo-
nents. (1) Query Reformulation: As depicted in Figure 10, the
example utilizes the standard medical term “acute liver failure” with
the specification “pediatric” to focus on the child population, which
facilitates retrieval precision. It is more suitable for scenarios that

require rapid positioning of medical concepts. Moreover, the term
“core” is more professional and precise than “the most important”,
offering a distinct advantage in evidence retrieval. (2) CoT Gen-
eration: As illustrated in Figure 11, its advantage lies in further
optimizing the precision of retrieval based on the content from the
previous round of the CoT process. During the CoT process, the
addition of keywords such as “infections”, “autoimmune diseases”,
“malignancies”, and “rheumatologic diseases” improved the recall
accuracy for potential causes in the next iteration.

-40-200204060-60-40-2002040t = 1-120-90-60-3003060-100-80-60-40-2002040t = 2-120-90-60-3003060-100-80-60-40-2002040t = 3-120-90-60-3003060-90-60-3003060t = 4-120-90-60-3003060-90-60-3003060t = 5-120-90-60-3003060-90-60-3003060t = 6Iter 1Iter 2Iter 4Iter 3Iter 5Iter 6T-SNE Visualization of Retrieved Documents2

Med-R

: Crafting Trustworthy LLM Physicians via Retrieval and Reasoning of Evidence-Based Medicine

WWW ’26, April 13–17, 2026, Dubai, UAE.

Table 8: Scaling analysis of context window and model size for Med-R2 .

Model

Method

MedQA-USMLE MedQA-MCMLE MedMCQA PubMedQA MMLU-Med Average

LLaMA3.1-8B

Qwen2.5-14B

Qwen2.5-32B

LLaMA3.1-70B

LLaMA3.1-8B

Qwen2.5-14B

Qwen2.5-32B

LLaMA3.1-70B

LLaMA3.1-8B

Qwen2.5-14B

Qwen2.5-32B

LLaMA3.1-70B

LLaMA3.1-8B

Qwen2.5-14B

Qwen2.5-32B

LLaMA3.1-70B

LLaMA3.1-8B

Qwen2.5-14B

Qwen2.5-32B

LLaMA3.1-70B

LLaMA3.1-8B

Qwen2.5-14B

Qwen2.5-32B

LLaMA3.1-70B

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

Direct Response
Med-R2

31.16
77.01

50.01
54.34

16.23
24.43

46.43
86.37

31.34
73.16

50.21
58.50

15.75
25.28

47.99
85.72

31.39
72.54

49.69
55.46

15.46
28.02

47.46
86.43

31.25
62.86

50.40
54.78

15.61
27.05

46.31
83.36

31.92
62.57

49.88
54.84

15.89
27.87

47.17
83.55

31.14
56.06

51.38
52.79

16.11
27.09

47.26
83.84

4K
41.45
84.16

65.23
80.19

87.07
90.01

58.36
84.58

8K
41.64
82.61

64.21
86.86

86.82
89.36

57.78
86.80

16K
41.43
77.22

66.44
83.01

86.83
89.32

57.61
88.15

32K
40.51
68.67

66.31
78.41

86.85
89.29

57.89
85.58

64K
39.85
62.51

64.76
78.75

86.81
88.75

57.43
84.86

128K
39.97
59.58

65.04
75.53

85.77
88.21

57.37
84.07

30.02
52.33

42.85
48.36

66.44
69.09

62.33
73.36

29.54
47.72

41.34
53.40

66.39
75.55

61.69
78.21

29.72
45.13

41.84
52.67

66.52
70.79

61.62
74.64

30.58
41.65

41.27
50.76

64.98
70.80

61.87
75.93

30.24
40.97

42.02
50.64

65.12
70.42

61.79
74.09

30.69
32.48

40.73
49.52

66.29
69.17

63.28
74.97

36.17
52.75

56.93
68.32

68.66
68.36

66.81
78.24

36.71
58.72

57.18
69.74

68.64
68.87

67.20
78.66

36.70
57.45

57.07
67.23

68.48
70.51

67.45
80.94

36.62
57.22

58.24
65.73

69.16
71.07

67.32
78.22

36.68
52.44

57.06
63.06

68.65
70.65

67.18
78.79

36.43
47.64

57.50
63.96

68.12
70.99

68.12
77.87

37.12
45.19

71.60
84.03

80.19
84.95

71.33
82.82

38.65
48.74

70.28
84.29

79.73
84.21

70.69
84.82

37.78
46.75

69.10
83.68

80.07
85.72

69.09
87.24

38.44
43.44

69.31
83.23

80.10
84.56

69.96
86.61

37.52
45.73

69.42
80.51

79.29
84.54

69.37
85.70

38.26
44.82

70.90
77.61

79.84
83.87

70.03
84.93

35.18
62.29

57.32
67.05

63.72
67.37

61.05
81.07

35.58
62.19

56.64
70.56

63.51
68.65

61.07
82.84

35.40
59.82

56.83
68.41

63.47
68.87

60.65
83.48

35.48
54.77

57.11
66.58

63.34
68.55

60.67
81.94

35.24
52.84

56.63
65.56

63.15
68.45

60.59
81.40

35.30
48.12

57.11
63.88

63.23
67.87

61.21
81.14

WWW ’26, April 13–17, 2026, Dubai, UAE.

Keer Lu et al.

Figure 10: A case study of query reformulation. We highlight the sentences within the retrieved documents that exhibit a high
degree of relevance to the keywords in the query and the final answer after the query reformulation process. It is evident that
prior to query reformulation (left), the retrieved evidence contains descriptions of acute liver failure mortality prognoses that
are dispersed, including “hepatic encephalopathy”, “INR”, “serum bilirubin level”, etc., without emphasizing the most critical
prognostic factors. Consequently, the model is unable to extract the correct answers when answering medical questions based
on such documents. In contrast, after the query reformulation process (right), it can be observed that the retrieved documents
consistently identify “INR” as a core prognostic feature, providing effective evidential support for the model’s responses to
medical inquiries.

hepatic encephalopathyAnswer:hepatic encephalopathy? INR? etiology of liver failure?
serum bilirubin level?
...Document 3A study of pediatric patients with active liver failure found that factors such as the degree of hepatic encephalopathy, coagulopathy (INR), and the etiology of liver failure were important prognosis factors. The presence of renal
failure and poor nutritional status also negatively
impacted the prognosis.Document 2In children with active liver failure, multiple factors influence the prognosis. Hepatic encephalopathy is a complication, and its severity often correlates with the liver dysfunction degree. Coagulopathy, assessed by INR, is another critical factor, as it significantly reflects the liver's inability to synthesize clotting factors. Additionally, the etiology of liver failure, presence of renal dysfunction, and the child's nutritional status are also important considerations for predicting outcomes.Document 1The prognosis for children with active liver failure is influenced by various factors. Hepatic encephalopathy grade, coagulopathy (INR), and serum bilirubin levels
are key indicators of disease severity. Early referral to a liver transplantation center and appropriate supportive care are crucial for improving survival chances.                 “In a child with active liver failure, what is the
                 most important prognosis factor for death?”Patient:Document 3Under the scenario of ,  for mortality. Elevated INR reflects the liver's impaired synthetic function. When the INR value exceeds certain thresholds, it indicates a higher risk of mortality, making it a crucial marker for clinicians to monitor
                 and interpret when making decisions regarding liver
                 transplantation and intensive care management.pediatric acute liver failureINR has been identified as a core independent prognostic factorDocument 2Research has shown that in the ,  for mortality. Higher peak INR values were found to be significantly associated with poorer outcomes, emphasizing their importance in predicting the need for liver transplantation and the risk of death.pediatric acute liver failurepeak INR levels are a core independent prognostic factorDocument 2Document 1A recent study analyzed the prognostic factors for mortality in  and found that . INR greater than 2.0 was significantly associated with increased mortality risk. This biochemical marker provides valuable insights into liver function and helps clinicians assess the severity and predict outcomes in affected children.pediatric acute liver failureINR is a core independent prognostic factor                 “What is the  independent prognostic factor
               for mortality in ?”corepediatric acute liver failureReformulated	:INRAnswer:INR !Knowledge
CorpusLLM Physician2

Med-R

: Crafting Trustworthy LLM Physicians via Retrieval and Reasoning of Evidence-Based Medicine

WWW ’26, April 13–17, 2026, Dubai, UAE.

Figure 11: A case study of CoT generation. We highlight the keywords within the generated CoT sequences and retrieved
documents that play a pivotal role in both retrieval recall and answer inference. It is observed that when the model generates
CoT sequences based on the initial set of retrieved documents, it incorporates keywords such as “infections”, “autoimmune
diseases”, “malignancies”, and “rheumatologic diseases”. The inclusion of these keywords enhances the comprehensiveness of
the evidence documents retrieved in subsequent iterations. For instance, the second round of document retrieval encompasses
causes like “systemic lupus erythematosus (SLE)” and “systemic inflammatory response syndrome (SIRS)”. Through such
iterative process, the model progressively accumulates more relevant information, leading to a final answer that is notably
more accurate and comprehensive compared to approaches that do not incorporate the CoT generation module.

Without
CoT Generation“A 65-year-old male with a long history of diabetes has recently experienced fatigue, low-grade fever, and joint pain, along with elevated CRP. What might be the possible causes?”Patient:With
CoT GenerationDocument 4Systemic Inflammatory Response Syndrome (SIRS) can be triggered by both infectious and non-infectious etiologies, including trauma, pancreatitis, and malignancy.Document 3Chronic elevation of CRP in elderly patients, particularly those with comorbidities like diabetes, may indicate an underlying malignancy such as lymphoma or solid tumors. Inflammation associated with cancer can mimic infection or autoimmune disease.Rheumatoid arthritis is more prevalent among diabetic patients, likely due to shared inflammatory pathways involving TNF-α and IL-6. Joint pain and stiffness in diabetic individuals should raise suspicion for underlying autoimmune conditions such as polymyalgia rheumatica or , especially when accompanied by elevated inflammatory markers like CRP.systemic lupus erythematosus (SLE)Document 2Document 1Patients with long-standing diabetes are at increased risk of bacterial infections like urinary tract infections (UTIs), pneumonia, and soft tissue infections because of impaired neutrophil function and hyperglycemia-induced immune suppression. These infections often present with non-specific symptoms such as fatigue and low-grade fever, making early diagnosis challenging.CoT GenerationTo answer the question, I integrated the patient’s clinical presentation (fatigue, low-grade fever, joint pain, elevated CRP) with his history of diabetes and the information from retrieved documents. Elevated CRP suggests inflammation, which could arise from , , or . Diabetes increases the risk of infections, particularly bacterial , but also predisposes to autoimmune and inflammatory conditions. The joint pain specifically raises suspicion for , while the patient’s age and persistent inflammation warrant consideration of malignancy.infectionsautoimmune diseasesmalignanciesrheumatologic diseasesinfectionsbacterial infections;
rheumatoid arthritis;
polymyalgia rheumatica;
systemic lupus erythematosus;
malignancies;
systemic inflammatory response syndromeAnswer:Next Iteration...Document 3Elevated C-reactive protein (CRP) levels are a nonspecific but sensitive marker of systemic inflammation and can be observed in various clinical conditions. In the context of infections, CRP typically rises rapidly in response to bacterial pathogens, making it a useful adjunct in differentiating bacterial from viral etiologies. In autoimmune diseases such as rheumatoid arthritis or vasculitides, chronic immune activation leads to persistent elevation of CRP, reflecting ongoing inflammatory activity.Diabetes mellitus has been recognized as a condition that may coexist with or contribute to the development of various rheumatologic disorders. Among these, rheumatoid arthritis (RA) is notable due to shared immunoinflammatory pathways; both diseases involve chronic systemic inflammation and are associated with elevated levels of pro-inflammatory cytokines such as TNF-α and IL-6. Furthermore, patients with diabetes demonstrate a higher prevalence of polymyalgia rheumatica (PMR), an inflammatory disorder characterized by bilateral shoulder and hip girdle pain, often accompanied by marked elevations in inflammatory markers such as CRP.Document 2Document 1Due to a combination of immunological, physiological, and metabolic impairments associated with diabetes mellitus, diabetic patients are more prone to bacterial infections, including urinary tract infections (UTIs), pneumonia, and soft tissue infections.bacterial infections;
rheumatoid arthritis;
polymyalgia rheumaticaAnswer:LLM PhysicianWWW ’26, April 13–17, 2026, Dubai, UAE.

Keer Lu et al.

F Prompts
We present the prompts employed throughout our pipeline in Med-
R2 . Specially, prompts for query reformulation according to the
Evidence-Based Medicine (EBM) categories can be found in Table 4.

Prompt: Evidence-Based Medicine (EBM) Category
Classification

You are an expert in sentence annotation within the medical
field. There are 6 categories of clinical questions: Prognosis,
Therapy, Etiology, Diagnosis, Prevention, and Cost. Please
classify the following text fragment based on their purpose
and structure by providing only the category name without
additional commentary:

# Question
{question}

Prompt: General Natural Language Question Cate-
gory Classification

You are an expert in natural language question annotation.
Given the following 12 categories of question types: Factual,
Definitional, Explanatory, Descriptive, Directive, Opinion,
Comparative, Evaluative, Hypothetical, Procedural, Refer-
ential, and Verification. Please classify the following text
fragment based on their purpose and structure by providing
only the category name without additional commentary:

# Question
{question}

Prompt: Retrieved Document Category Classification

You are an expert in sentence annotation within the medical
field. There are 16 categories of documents: Argumentation,
Definition, Description, Explanation, Purpose, Narration,
Process, Instruction, Command, Problem-Solving, Com-
parison, Evaluation, Classification, Condition, Prediction,
Cause-and-Effect. Please classify the following text frag-
ment based on their purpose and structure by providing the
probability distribution of its belonging to each category,
where the sum of probabilities across all categories equals
1, without additional commentary:

# Document
{retrieved_document}

Output Format:
```json
{

"Argumentation": "",
"Definition": "",
...

}

'''

Prompt: Hierarchy of Evidence Judgement

You are an expert in evidence quality annotation within the
medical field. There are 9 quality levels of evidence, ranging
from the highest to the lowest as follows: Meta-Analyses,
Systematic Reviews, Evidence-Based Practice Guidelines,
Randomized Controlled Trials, Non-Randomized Con-
trolled Trials, Cohort Studies, Case Series or Studies, Indi-
vidual Case Reports, Expert Opinion. Please classify the
following evidence document based on its structure and
characteristics, providing only the names of the levels, with-
out any additional description:

# Evidence
{retrieved_document}

Prompt: Chain-of-Thought (CoT) Generator

Given the provided [Context], [Question], as well as the
[Retrieved Documents], please provide an answer that
includes your thought process. Specifically:

(1) Analyze the Question: Carefully analyze the
[Question] to understand what information is
being sought.

(2) Review Provided Context:

the
[Context] for any background information
that can help frame the answer.

Examine

(3) Consult Retrieved Documents: Go through the
snippets of [Retrieved Documents] to identify
sections that are directly related to [Question].

(4) Identify Key Information: Highlight

points from the [Retrieved
address the question’s requirements.

the key
Documents] that

(5) Construct Thought Process: Explain how you
used the information from the [Context] and the
retrieved documents to form your understanding
and construct your answer.

(6) Provide Answer: Finally, give a clear and concise
answer to the [Question], supported by the analy-
sis of the [Retrieved Documents].

Please present your response in a way that clearly shows
your reasoning and the sources of information you relied
on.

# Context
{context} [optional]

# Question
{question}

# Retrieved Documents
{retrieved_documents} [optional]


