From Fluent to Verifiable: Claim-Level Auditability for
Deep Research Agents

Razeen A Rasheed
Indian Institute of Science

Animesh Mukherjee
IIT Kharagpur

Somnath Banerjee
IIT Kharagpur, Cisco Systems

Rima Hazra
TCG CREST

6
2
0
2

b
e
F
4
1

]
I

A
.
s
c
[

1
v
5
5
8
3
1
.
2
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
A deep research agent produces a fluent scientific report in minutes;
a careful reader then tries to verify the main claims and discovers
the real cost is not reading, but tracing: which sentence is supported
by which passage, what was ignored, and where evidence conflicts.
We argue that as research generation becomes cheap, auditability
becomes the bottleneck, and the dominant risk shifts from isolated
factual errors to scientifically styled outputs whose claim–evidence
links are weak, missing, or misleading. This perspective proposes
claim-level auditability as a first-class design and evaluation tar-
get for deep research agents, distills recurring long-horizon failure
modes (objective drift, transient constraints, and unverifiable in-
ference), and introduces the Auditable Autonomous Research
(AAR) standard, a compact measurement framework that makes
auditability testable via provenance coverage, provenance sound-
ness, contradiction transparency, and audit effort. We then argue
for semantic provenance with protocolized validation: persistent,
queryable provenance graphs that encode claim–evidence relations
(including conflicts) and integrate continuous validation during syn-
thesis rather than after publication, with practical instrumentation
patterns to support deployment at scale.

1 Introduction
Deep research agents are emerging as autonomous investigators,
they search the literature, plan multi-step work, use tools, and write
scientific reports. Recent benchmarks reflect this shift by defining
long-horizon research tasks that require sustained planning and
evidence use, not short one-turn answers [23]. Yet empirical studies
of multi-agent systems show that these workflows often fail due to
unclear task specifications, lost context, poor coordination across
roles, and weak verification [19].

The most dangerous failures are increasingly plausible. A report
may read like legitimate scholarship - coherent narrative, confident
tone, familiar venues, while a reader still cannot answer a basic
question: what exact evidence supports this key claim? When that
link is weak, the risk is not only incorrect facts, but scientific pol-
lution: outputs that look credible while the underlying evidence
trails are fragile or missing. As agents generate thousands of draft
papers cheaply, generation stops being the bottleneck; trust and
auditability become the bottleneck. In practice, the breakdown
often appears as citation–claim mismatch or fabricated or incor-
rect references, making verification slow or infeasible [20]. The
risk compounds when large volumes of agent outputs flow back
into training and evaluation pipelines, reducing reliability through
feedback effects [58].

Deep research agents should be designed and evaluated for
claim-level auditability, where every key claim links to spe-
cific supporting evidence in a clear, semantic way, not just a
log of actions or fluent text. Current provenance and reporting
practices may record what an agent did, but often fail to encode
which sources substantiate each claim and how they support it. The
W3C PROV [9] model provides a standard way to represent entities,
activities, and agents, but deep research agents need more: claim-
level links that preserve the meaning of the claim–evidence relation,
surface contradictions rather than smoothing them away, and keep
verification cost low enough to scale. In short, deep research re-
quires semantic provenance that preserves evidential structure, not
merely action traces.

Building on this position, we propose auditability as a first-class
systems constraint for deep research agents. We advocate evalua-
tion criteria that measure traceability and evidential support, and
argue for semantic provenance that preserves claim–evidence struc-
ture to enable systematic auditing. This perspective aligns with
emerging efforts that directly audit citation integrity in deep re-
search settings, reinforcing that credibility requires explicit, check-
able evidence links rather than narrative coherence alone [56].

The urgency is driven by a widening capability–credibility
gap. Autonomous research agents can compress weeks-long cycles
into hours, yet their most consequential steps—hypothesis forma-
tion, evidence selection, and causal attribution—often remain non-
auditable after the fact [29]. This is already visible in the ecosystem:
AI-fabricated “junk science” is contaminating discovery layers such
as Google Scholar, enabling downstream “evidence manipulation”
where non-existent results are ingested, summarized, and even-
tually cited as record [28]. Even in well-intentioned deployments,
failures can survive the “looks scientific” filter: an independent
evaluation of Sakana’s The AI Scientist found that 42% of proposed
experiments failed to execute due to coding errors, yet the system
still produced manuscripts that mischaracterized established con-
cepts as novel and relied on weak or flawed evidence chains [8].
Critically, the failure mode is shifting from wrong answers to wrong
citations: analyses have surfaced hallucinated references in tech-
nical writing pipelines [2] and even in the published record of
elite venues, showing how attribution—central to reproducibility
and credit assignment—can silently break under AI-mediated draft-
ing [27]. Meanwhile, the broader integrity ecosystem is under strain
from industrial-scale fraud: Wiley’s Hindawi paper-mill investiga-
tions alone drove 11,300+ retractions by 2024 [1, 18]. The result is a
looming reproducibility crisis of a new type: a deluge of technically
fluent papers whose inferential lineage cannot be reconstructed,
audited, or falsified because the reasoning and tool actions that

, ,

Razeen A Rasheed, Somnath Banerjee, Animesh Mukherjee, and Rima Hazra

generated them are opaque. Auditability, therefore, is not merely a
debugging aid; it is a governance primitive for scientific trust when
discovery becomes autonomous.

Our contribution. We (i) formalise operational require-
ments for auditable deep research agents (what must be
captured and what “auditability” means at claim granu-
larity), (ii) propose a concrete provenance encoding that
represents claim–evidence relations as first-class structure
(beyond action logs), and (iii) demonstrate practical in-
strumentation that captures complete decision lineage at
scale. This targets the core systems question: how do we
architect agents whose outputs are both capable and
certifiable under real-world constraints?

2 Background
2.1 The anatomy of autonomous discovery
Deep research agents share a common pipeline, even when imple-
mentations differ across The AI Scientist [41], Coscientist [14], and
ChemCrow [17]. Most systems run a plan, execute, synthesize loop,
where an LLM acts as the controller that assigns sub-tasks and
routes tool calls [19, 55]. We divide the system into two phases, a
‘doing zone’ and a ‘thinking zone’ (see Figure 1). The doing zone
produces evidence through planning and execution. The thinking
zone turns evidence into a report through synthesis and review.
This structure matters because errors introduced early propagate
forward and shape what the agent searches, runs, and writes.
Planning step (Decomposition). The process begins with a high-
level objective (for example, discover a novel optimizer for neural
networks). A planning agent decomposes this into a directed acyclic
graph (DAG) of sub-tasks [19, 41]. For AI Scientist, this phase in-
volves brainstorming ideas against a literature database to filter
for novelty [41]. However, systematic evaluation reveals that this
produces simplistic keyword searches rather than profound synthe-
sis [32], leading to fundamental errors in hypothesis decomposition.
Previous analysis [19] of multi-agent planning shows that 44.2% of
failures arise from specification errors, task misinterpretation, and
improper decomposition. These failures are consistent with broader
patterns observed in agentic systems, in which errors propagate
across layers from initial task specification to execution, creating
cascading vulnerabilities that compromise downstream outputs [3].
When the planning layer misinterprets objectives, careful execution
or synthesis cannot restore scientific validity.
Execution loop (Action step). The execution loop runs tools to
carry out the plan. The agent generates code or machine-action in-
structions, executes them in a sandbox, reads errors (e.g., stderr),
and debugs iteratively [14, 41, 64]. Tool-rich designs reduce some er-
rors by adding feasibility checks; ChemCrow [17] integrates many
expert tools to validate chemical constraints before acting. How-
ever, execution still fails at high rates when the agent lacks per-
sistent memory, because it repeatedly applies the same ineffec-
tive strategy across iterations [11, 54]. Earlier analysis [19] across
∼1,642 multi-agent system traces demonstrates systematic failure
rates ranging from 41% to 86.7% depending on system architecture
and task complexity. These execution vulnerabilities align with

autonomous-agent threat models; shadow agent emergence arises
when execution consistently diverges from the planned workflow
without detection, and tool squatting enables malicious behavior
via compromised dependencies [3]. Without continuous alignment
verification, an agent can run complex protocols that fail to test the
stated hypothesis.
Synthesis step (Writing). The synthesis step aggregates tool
outputs, logs, plots, and retrieved sources into a structured nar-
rative [41, 55]. This stage does more than summarizing. It links
results to the hypothesis and states what the evidence supports.
When the planning or execution stage deviates from the objec-
tive, the synthesis stage often produce fluent text that obscures
inadequate controls or weak evidential support, as it relies on the
artifacts the system has accumulated.
The reflexion loop (Review). The reflexion loop adds a reviewer
agent that critiques the draft and checks whether claims follow
from the evidence [24, 41]. This step aims to catch gaps, contradic-
tions, and unsupported statements before finalization. In practice,
reviewer agents often share the same evidence trace as the writer,
so they validate internal consistency instead of detecting upstream
errors. When both agents trust the same flawed plan or incomplete
execution, review fails to flag that the system answers the wrong
question or cites weak evidence.

This pipeline explains how agents generate reports, but it does
not guarantee that each claim remains correct, supported, and trace-
able to evidence. This gap motivates a Verification, Provenance, and
Evaluation (VPE) framework that makes reports auditable across ar-
chitectures; as agents move from retrieval to multi-step reasoning, a
single unsupported step can distort the entire investigation. Existing
approaches remain largely platform specific; proprietary systems
add platform-specific checks, OpenAI uses reinforcement learning
with grader models and secondary summarizers (e.g., o3-mini) to
audit reasoning traces [38], and Google introduces DeepSearchQA
to benchmark factuality and report structure [35]. Open-source ef-
forts also advance standardization, including ReportBench [55] for
report-level evaluation and PROV AGENT [62], which adapts W3C
provenance standards [9, 49] to track decision lineage. However, the
field still lacks a unified, interoperable VPE framework that guaran-
tees reliability and traceability across systems, so deployment often
relies on trust rather than auditable proof.

2.2 Why current provenance fails
Current provenance standards help reproduce a workflow. The
W3C PROV standard records entities, activities, and agents to show
how a system produces an output [9, 48]. Tools such as MLflow,
DVC, and FAIR data pipeline use this idea to track data, code, and
artifacts across runs [47]. This record shows what the system runs.
It does not show why a research claim is correct. It also does not
store clear links between each claim and the evidence that supports
it [48]. Agent logs add more detail about tool use and retrieval. They
record queries, retrieved papers, and executed code [61, 62]. These
logs help developers inspect what the agent did, but they still miss
the reasoning traces that turn evidence into conclusions. Structured
memory approaches [11, 75] maintain persistent state across execu-
tion rounds, yet focus on forward continuity (what to search next)
rather than backward traceability (which evidence supports each

From Fluent to Verifiable: Claim-Level Auditability for
Deep Research Agents

, ,

Figure 1: The plan-execute-synthesize architecture of deep research agents. Research agents operate through four interconnected
modules driven by LLM orchestration controllers. The planning module decomposes high-level objectives into task DAGs
(44.2% of failures stem from specification errors [19]). The execution loop generates and runs code in sandboxed environments,
parsing logs to debug autonomously (41-86.7% failure rates without persistent memory [19]). The synthesis layer aggregates
results into manuscripts. The reflexion loop provides automated review.

claim). Rerunning the same steps does not fix this issue because
the model may make different choices during inference and the log
does not capture those choices [62]. This makes it hard to check
if the agent reads sources correctly and uses fair baselines [41]. It
also makes it hard to check if the experiment really tests the target
idea [32]. This gap makes audits harder and can spread weak results
at scale [13, 52, 57].
3 Architectural failures in autonomous

discovery

Deep research agents separate the execution environment (doing
zone) from the reasoning environment (thinking zone) [12, 37]. This
design creates a weak connection between what happens during
tool use and what the agent thinks has happened. Current prove-
nance logs do not build explicit graphs that link execution traces
to reasoning decisions. As a result, these systems do not provide
the verification guarantees needed for autonomous scientific in-
quiry [26]. The following subsections describe three failure modes
observed in recent evaluations.

3.1 Planning failures
A core architectural failure is that agents optimize for task com-
pletion rather than truth preservation [13, 52]. Current objective
functions often reward producing a coherent manuscript (e.g., a
compiled PDF) instead of detecting when empirical outcomes con-
tradict the stated goal [41]. This mismatch typically arises from
three linked steps. The plan simplifies the objective, the evaluation
follows the simplified metric, and the review checks the write-up
rather than the link between the objective and the evidence.
Objective drift: The AI Scientist report includes a task framed as
improving energy efficiency in neural network training [32]. The
stated objective is to reduce computational cost while maintaining
accuracy. The agent implements a new training schedule, runs

benchmarks, and collects accuracy and compute measurements.
The results show higher accuracy but also higher cost [32]. This
directly conflicts with the objective. However, the final manuscript
still presents the outcome as improved training efficiency using
accuracy as the main evidence [19, 32]. This pattern of objective
misalignment appears systematically across autonomous research
systems. Evaluations of language model agents demonstrate goal
drift scores ranging from 0.25 to 0.93 when exposed to competing
objectives [6], while studies of 16 major AI models reveal that
agents consistently bypass stated constraints to pursue alternative
goals [5]. Prior work [59] also shows that in long-horizon tasks,
agent state can drift and remain misaligned even when individual
reasoning steps appear locally coherent, and that increasing context
capacity alone does not prevent this drift.
Metric misalignment: The reviewer module of the deep research
agent checks whether the paper is internally consistent (e.g., meth-
ods match results) but does not verify that the reported metrics test
the stated objective. This requires a provenance chain that links the
objective (reduce compute) to the chosen metrics (accuracy only)
and to the acceptance decision [48, 62]. Without this linkage, debate-
style review cannot surface the error if both agents share the same
metric mismatch [24]. The root cause is that the system has no way
to remember and enforce the compute constraint throughout the
workflow [11, 54]. Worryingly, the authors in [50] find that more
capable agents are more prone to misalignment, and that persona
characteristics can strongly and unpredictably shape this tendency.
Work on scientific integrity and transparency motivates architec-
tures that make these links traceable and accountable [13, 37].
Novelty verification failures: The AI Scientist reports micro-
batching for stochastic gradient descent algorithm as a novel con-
tribution [32]. This technique is standard in model training, but

LLMCentral AI ControllerBreak down big goalsinto tasks lists.1. Planning Step44.2% failure(mistake in setting goals)Doing Zone(Reality Check)Write & run code safely,read logs, fix bugsautomatically.2. Action Step(Execution)41-86.7% failure(no long-term memory)Combine results intofinal report.3. Writing Step(Synthesis)28.6-91.4%made-up informationThinking Zone(Agent's Beliefs)Automatic checking4. Review Step(Reflexion)misses 78% of made upsummariesFinal AgentReportTHE KNOWLEDGE DISCONNECT:Missing link between what happened vs why, ,

Razeen A Rasheed, Somnath Banerjee, Animesh Mukherjee, and Rima Hazra

Objective Drift

The agent confused energy efficiency with model performance, producing more accurate results but using
more computational resources [19, 32].

Metric Misalignment

The reviewer checked if the paper was internally consistent but could not verify whether the measurements
actually tested the original goal [24, 48, 62].

The Baseline Rediscovery
Problem

The agent presented well-known methods as new discoveries even though they were already widely used
[32, 57].

The Cross-Validation
Implementation Bug

The agent planned to test multiple validation settings but accidentally locked in just one during debugging,
then reported results as if all settings were tested [32].

Transient Memory as
Architectural Liability

In long tasks, the agent forgets important constraints given at the beginning by the time it reaches later steps
[11, 40].

High Execution Failure
Rate

Independent reviewers found that many proposed experiments could not run due to unresolved programming
errors [19, 32].

The Architectural Root
Cause

Citations become disconnected from actual content because of how the system processes information, leading
to high rates of false information in biomedical writing [21].

The Unverifiable Inference
Chain

The agent’s reasoning happens through internal neural network processes that leave no clear path from evidence
to conclusions [12, 62].

Why Unverifiable Inference
Chains Prevent Scientific
Falsification

The mathematical representations used cannot capture how evidence supports claims because they treat all
relationships as bidirectional rather than one-way logical connections [16, 69].

The Parameter Capacity
Paradox

Smaller models struggle to break down complex problems properly, while larger models confidently generate
false information during the writing stage [22, 76].

The Open Weight Verification
Tradeoff

Open-source models allow researchers to inspect and modify internal processes, while proprietary models reason
better but cannot be examined or modified [71].

Module-Specific Failure
Propagation

Different types of failures occur in planning, execution, and writing stages, and each spreads through the system
in different ways [19, 76].

)
3
§
(
y
m
o
n
o
x
a
T
e
r
u
l
i
a
F

l
a
r
u
t
c
e
t
i
h
c
r
A

g
n
i
n
n
a
l

P

.

)
1
3
§
(

s
e
r
u
l
i
a
F

n
o
i
t
u
c
e
x
E

.

)
2
3
§
(

s
e
r
u
l
i
a
F

s
i
s
e
h
t
n
y
S

.

)
3
3
§
(

s
e
r
u
l
i
a
F

t
n
e
d
n
e
p
e
D

-
l
e
d
o
M

.

)
4
3
§
(

s
e
r
u
l
i
a
F

Figure 2: Taxonomy of architectural failures in deep research agents. Planning failures include objective drift and baseline
rediscovery [19, 32]. Execution failures include critical information loss over long tasks with substantial failure rates [19, 40].
Synthesis failures include citations that become disconnected from their sources, leading to high hallucination rates [21, 57].
Model characteristics amplify these failures differently depending on model size and whether the model is open-source or
proprietary [71, 76].

simplistic keyword-driven retrieval fails to map equivalent terminol-
ogy. Without persistent knowledge structures tracking previously
explored hypotheses [11, 75], agents cannot recognize when they
revisit known solutions, contributing to the broader problem of
model collapse where AI-generated content contaminates training
data [57]. Related evidence [67] shows that language-based agents
also struggle to adapt when feedback changes the environment:
they may select the right tool initially, but they often fail to revise
plans, explore alternatives, or execute contingency strategies even
in constrained search spaces.

3.2 Execution failures
The cross-validation implementation bug: Autonomous re-
search requires the initial experimental specification to remain
available and is enforced throughout planning, implementation,
execution, and reporting [40]. In current agent pipelines, these
constraints are stored only as text in the prompt context rather
than in any queryable structures. Long trajectories, limited context
windows and the lost in the middle effect reduce the likelihood
that earlier requirements are attended to during later edits and
decisions [40] (see Figure 3, left). This leads to a recurring failure
where the implementation and the reported evaluation drift from
the original specification, despite the code running correctly. The

From Fluent to Verifiable: Claim-Level Auditability for
Deep Research Agents

Figure 3: Stateless vs. Cumulative Memory Architectures.
Left: Current stateless execution. Critical constraints (e.g.,
“𝑘 ∈ {2, 3, 4, 5}”) specified at Step 1 become inaccessible by
Step 15 when code is revised due to context window limi-
tations [40]. Right: Proposed cumulative memory. A persis-
tent constraint graph [11, 54] maintains the specification as
a structured requirement, enabling automated verification
that implementation satisfies all original constraints [62].

AI Scientist provides an instance where a cross-validation plan spec-
ifies multiple 𝑘 values, but later code revisions effectively test only
one setting while the final write-up still describes the broader eval-
uation [32]. The underlying issue is not only code correctness but
specification–implementation consistency since the system lacks a
persistent representation that binds experimental requirements to
concrete checks in code and results [62]. A very recent work [36]
shows that strong key performance indicators (KPI) performance
can coincide with violating mandated constraints, exposing drift
between what agents optimize and what the specification requires
(e.g., ethical or safety limits). Their benchmark demonstrates that
standard metrics can falsely signal success: an agent can score
highly on outcomes while breaching explicit constraints. Across
12 state-of-the-art LLMs, they measure outcome-driven constraint
violations from 1.3% to 71.4%, with Gemini-3-Pro-Preview showing
the highest violation rate at 71.4% While trajectory compression
methods [75] extend effective context through structured state sum-
maries, they compress for forward continuity rather than backward
verification. The compressed state enables avoiding redundant re-
trieval but does not preserve which evidence supports which claims.
Transient memory as architectural liability: Persistent mem-
ory and trace structures target this gap (Figure 3, right). Work on
knowledge-graph-based memory shows benefits for multi-step rea-
soning and coordination compared to stateless prompting [10, 11].
In contrast, stateless execution makes it difficult to retain which
constraints must be satisfied and which fixes have already failed.
High execution failure rate: Consistent with this, the AI Scientist
evaluation reports that 5 out of 12 proposed experiments fail to ex-
ecute (42%) due to unresolved coding errors [32], and multi-agent
studies report coordination failures that include losing track of
prior attempts [19]. Provenance-style traces can record constraints,
attempted fixes, and outcomes so the agent can detect repeated
failures and escalate earlier when needed [34, 62]. Complementary
evidence [60] shows that many execution failures arise from agent-
environment interaction rather than planning alone. Based on 3,656
interaction traces across benchmarks, the authors define six failure
modes driven by environment feedback.

, ,

3.3 Synthesis failures
Synthesis failures occur when agents generate fluent text with
apparently valid citations, but the cited sources do not actually
support the stated claims.
The architectural root cause: Deep research agents risk produc-
ing black box science [12, 39] unlike human scientists who ground
claims in specific passages that logically support their conclusions.
Agents generate text through opaque vector operations where cita-
tions function as plausibility signals rather than evidential links [68].
This citation decorrelation, i.e., the systematic disconnect between
cited papers and the claims they purport to support, arises from the
architecture of retrieval systems that operate through cosine similar-
ity in embedding space rather than formal logical inference [21, 45].
Retrieval mechanisms surface papers that are topically similar to a
claim based on high cosine similarity without encoding the logical
relationship between evidence and conclusion. Geometrically, a
claim such as “Treatment X reduces symptom Y” retrieves litera-
ture mentioning treatment X and symptom Y regardless of whether
the paper demonstrates efficacy, refutes it, or studies an unrelated
mechanism, because shared entities dominate embedding similarity
while evidential directionality is ignored [16]. DeepTRACE [66]
shows that deep research agents often generate strongly one-sided
and overly confident answers to debate-style questions, while a
substantial proportion of their claims are not actually supported by
the sources they themselves cite. In particular, they exhibit large
fractions of unsupported statements, with citation accuracy rang-
ing from 40-80% across systems. ChemCrow [17, 52] illustrates this
failure mode where agents planned correct chemical syntheses but
attributed reaction conditions to papers that used different catalysts
or substrates, producing citations that appeared relevant but were
evidentially false. Crucially, this failure is systematic rather than
random because it stems from a fundamental architectural mis-
match. Logical support has directional structure: if paper A proves
“catalyst X enables reaction Y,” then A supports the claim but the
claim does not inversely prove A’s methodology. Logical support
also has exclusive states, where evidence either supports, refutes,
or is neutral toward a hypothesis. In contrast, cosine similarity
is symmetric (the distance from A to B equals B to A) and blend-
ing (contradictory evidence vectors average rather than conflict),
making it mathematically incapable of representing entailment or
contradiction [43, 69]. A paper refuting treatment X and a paper
supporting it will be both retrieved if they share entity overlap, with
their opposing conclusions smoothed away in the embedding space.
These errors reflect fundamental mathematical incompatibilities
rather than limitations fixable through scale or better training.
The unverifiable inference chain: In documented evaluations
of The AI Scientist [32], the agent produced a report claiming im-
proved training efficiency despite experimental results showing
increased computational cost (23% more FLOPs, 18% more wall-
clock time). The system cannot answer verification questions such
as “Which evidence justified framing higher accuracy as efficiency?”
or “Why was the cost-accuracy tradeoff resolved in favor of accu-
racy when the objective specified cost reduction?” because the
reasoning occurred through transient neural activations during
LLM forward passes rather than explicit logical operations [12].
The final report contains no record of how the agent reconciled

Step 1 (Planning):Specify constraint k ∈ {2,3,4,5}ConstraintlostStep 15 (Debugging):Code modified...Step 30 (Synthesis) : Final report(False claim: evaluated k ∈ {2,3,4,5}Constraint InaccessibleTransientContextWindowStateless ExecutionStep 1 (Planning):Specify constraint k ∈ {2,3,4,5}Step 15 (Debugging):Code modified...Step 30 (Synthesis) : Final report(False claim: evaluated k ∈ {2,3,4,5}PersistentConstraintGraphCumulative MemoryAutomatedVerificationVerifiedTrace, ,

Razeen A Rasheed, Somnath Banerjee, Animesh Mukherjee, and Rima Hazra

contradictory objectives or weighted competing metrics. This re-
flects a fundamental gap: while execution logs capture what code
ran and what results emerged, they cannot recover why the agent
interpreted those results as supporting the original claim, because
that interpretation happened in vector space rather than through
traceable logical steps [12, 68].

Current research agents provide no reconstructible trace linking
generated claims to supporting evidence through explicit reasoning
steps [62]. The synthesized manuscript cites relevant literature, but
we cannot programmatically reconstruct which specific passages
influenced which claims, how conflicting evidence was weighted,
or whether alternative interpretations were considered. The infer-
ence chain exists only as transient activation patterns in the LLM’s
forward pass that vanish after token generation [39].
Why unverifiable inference chains prevent scientific verifica-
tion: Popper’s criterion [53] for scientific claims requires that one
should be able to systematically test assertions against evidence
and identify contradictions. This demands – (a) Identifying which
specific evidence supports each claim, (b) Verifying that the evidence
actually entails the claim [45], (c) Determining whether contradic-
tory evidence was considered and properly addressed [44], and (d)
Assessing whether alternative interpretations were evaluated [25].

Current architectures make these steps intractable without com-
plete manual re-analysis [26]. When independent evaluators identi-
fied the energy efficiency paradox, they had to manually re-read the
agent’s code, trace through execution logs, and reconstruct what
the agent might have been optimizing for, requiring hours of expert
time comparable to conducting the original research manually [32].
This defeats the purpose of automation. Research on auditability in
AI systems emphasizes that verification effort must be substan-
tially lower than generation effort for autonomous systems to
provide practical value [26, 37].

The architectural deficit is the absence of provenance graphs
linking claims to evidence with explicit reasoning edges [48, 62].
The W3C PROV standard provides a foundation for this through
entities, activities, and agents connected via fundamental prove-
nance relationships [9, 48], enabling structured queries like “which
sources support claim C?” and “how was contradictory evidence
from source S resolved?” Yet current research agents, including the
AI Scientist, do not implement these standards [62]. Without such
infrastructure, generated research remains scientifically unfalsifi-
able: we can test final claims experimentally, but cannot audit the
reasoning that produced them. An initial step toward this is dis-
cussed in [63], where the authors introduce VeriLA, a systematic
framework for evaluating agent failures that reduces human effort
while improving interpretability. VeriLA uses a human-aligned
verifier module, trained on gold-standard human annotations, to
assess each agent output, enabling fine-grained analysis, surfacing
failures relative to human standards, providing actionable feedback,
and lowering the cognitive burden on evaluators.

3.4 Model dependent failures
The choice of foundation model including the scale and the weight
accessibility also heavily determine the architectural failure modes
introduced in the previous sections. Identical plan-execute-synthesize
architectures exhibit qualitatively different failure patterns when

instantiated using small open weight models vis-à-vis large propri-
etary systems [74, 76]. Existing research agents treat the underlying
language model as a black box and assume that increased scale suf-
fices for autonomous research [41]. However empirical evaluations
show that model choice shifts failure location rather than reducing
failure incidence. Smaller models fail during planning due to in-
sufficient decomposition while larger models fail during synthesis
through confident hallucination. While increased scale alters, it
does not eliminate these architectural limitations [22, 76].
The parameter capacity paradox: Open-source LLMs in the
7B–13B range generally lag behind commercial models on agent-
style tasks, with prior benchmarks reporting substantially higher
hallucination on factual question answering and weaker reliabil-
ity in multi-step settings [22, 74]. Prior work attributes much of
this gap to capacity limits; smaller models have weaker reasoning
and working memory, which makes it harder to sustain consistent
beliefs across long agent dialogues and increases the chance of fab-
ricated intermediate steps [74]. Model scaling reduces these errors,
but size alone is not decisive. Across benchmarks, improvements
within a model family from scaling can be large, yet cross-family
comparisons suggest that architecture, data, and instruction tun-
ing can matter as much as raw parameter count [22]. Moreover,
end-to-end evaluations that require reproducing machine learning
papers from scratch show that even strong proprietary models and
research-agent systems frequently fail to deliver complete, correct
results, with common breakdowns in experimental design, method-
ological rigor, and execution reliability [76]. Smaller models often
fail in the planning module because they cannot keep many con-
straints in mind, so they break a complex goal into overly simple
sub-tasks and miss key requirements [42, 74]. Larger models make
fewer planning mistakes, but they can still produce a clean and
confident plan that is wrong and looks correct at first glance [42].
In the execution module, research agents run for a long time (about
46,000 seconds per task vs. 250 seconds for reasoning-only agents),
so early constraints get lost during coding and debugging [76]. This
leads to “constraint drop” bugs, such as forgetting the intended
cross-validation setup, and smaller models degrade more under
long runs due to limited context [40, 74]. In the synthesis module,
scale does not prevent hallucinations: reviewers can accept plausi-
ble but wrong abstracts, and even frontier models still hallucinate
on technical QA, especially on multi-hop or conflicting evidence
[22, 46, 73].
The open weight verification tradeoff: Closed-weight propri-
etary models (e.g., GPT-4, Claude 3.5 Sonnet) often outperform
open-weight models but their closed design prevents inspection
or modification of the reasoning process, which makes auditing,
verification, and reproducibility difficult for autonomous research.
In contrast, open-weight models can be fine-tuned to become com-
petitive in low-data, low-resource, domain-specific settings, while
remaining easier to adapt and control. They support stronger safety
and governance hooks such as privacy-preserving training, mecha-
nistic interpretability and better abstention behavior [71].
Module-specific failure propagation: Systematic evaluations of
research agents report high failure rates across the full pipeline.
In an analysis of 1,642 multi-agent traces, 44.2% of failures were
specification errors introduced during planning, and execution fail-
ures ranged from 41% to 86.7% depending on the architecture and

From Fluent to Verifiable: Claim-Level Auditability for
Deep Research Agents

whether constraints were persistently stored [19]. Independent
evaluation of The AI Scientist further found that 42% of proposed
experiments failed to run [32]. Most notably, PaperBench reports
that 100% of agent-generated papers contained experimental or
methodological weaknesses, and Claude 3.5 Sonnet achieved only
1.8% task completion despite being a frontier model [76].

The following sections formalize these requirements through
the auditable autonomous research AAR standard (section 4) quan-
tifying when research agents achieve the verifiability necessary for
autonomous scientific inquiry [26, 62], and semantic provenance
graphs (section 5) providing the architectural substrate making
auditable autonomous research tractable [11, 48].

4 The AAR standard: A measurement
framework for auditable research

In section 3, we discussed three systematic failure modes in au-
tonomous research agents: objective drift (experiments contradict
their goals), transient constraints (specifications lost during ex-
ecution), and unverifiable inference (citations decorrelated from
claims). These failures share a common architectural deficit, i.e.,
the absence of persistent, queryable representations of reasoning
that enable systematic verification. Current agents optimize for
generation fluency while treating verification as an afterthought,
producing systems that are impressively capable yet fundamentally
untrustworthy for scientific work [32, 41]. This section establishes
the AAR standard - a measurement framework defining what prop-
erties must be quantified to assess research agent trustworthiness.
We argue that auditability must be measurable to be enforceable,
and that current benchmarks’ exclusive focus on task completion
creates perverse incentives that reward unverifiable generation.

4.1 The auditability invariant
We begin with a foundational principle that any research-grade
agent must satisfy:

Definition 1 (Research-grade auditability). A research agent
is auditable if independent reviewers can verify claim correctness
with effort 𝐸verify ≪ 𝐸generate, where verification accesses only:
(1) agent outputs, (2) structured provenance graphs, and (3) cited
sources. Systems requiring re-execution of experiments or manual
reconstruction of reasoning from logs fail this criterion.

This definition immediately reveals why current systems fail.
When independent evaluators identified the AI Scientist’s energy
efficiency paradox (section 3.1), they spent hours manually trac-
ing through code and logs to reconstruct what the agent actually
optimized for [32]. This effort approached that of conducting the
original research, defeating the purpose of automation.

4.2 Four properties of auditable research
Each documented failure mode implies a measurable property that,
if monitored, would expose problems before outputs propagate to
downstream use. We propose four complementary metrics:

, ,

sources through reasoning steps to outputs [48, 62]. High 𝑃𝐶𝑜𝑣 in-
dicates comprehensive traceability; low 𝑃𝐶𝑜𝑣 indicates prevalence
of orphaned claims lacking verifiable foundations.

Definition 3 (Provenance soundness: Do citations actually sup-
port claims?). Semantic validity 𝑃𝑆𝑛𝑑 measuring whether cited
sources actually entail attributed claims, not merely whether cita-
tions resolve to real papers [21]. 𝑃𝐶𝑜𝑣 is necessary but insufficient,
i.e., citations may resolve to real papers yet not support the specific
relationships asserted, creating scientific pollution: authoritative-
looking text with real DOIs but severed logical links between evi-
dence and claim.

Definition 4 (Contradiction transparency: Are evidence con-
flicts surfaced or suppressed?). The proportion (𝐶𝑇𝑟𝑎𝑛) of ac-
tual evidence conflicts that are detected and reported rather than
suppressed through aggregation [43, 69]. Vector-based retrieval
systems average contradictory embeddings, producing hedged sum-
maries that obscure which specific sources disagree.

4.3 Formal metric definitions
Semantic provenance graph construction. Given a user query
𝑞, a deep research agent constructs a directed provenance graph
𝐺𝑞 = (𝑉 , 𝐸) that traces how 𝑞 is answered through retrieved evi-
dence and reasoning. For each query 𝑞, the agent executes a pipeline
that retrieves a set of sources (S𝑞), performs a sequence of rea-
soning steps (R𝑞) that synthesize evidence from those sources,
and generates a set of final claims (C𝑞) that directly respond to
the query 𝑞. The resulting provenance graph is then defined as
(𝐺𝑞 = (𝑉 , 𝐸)), where the vertex set is the union of these compo-
nents, i.e., (𝑉 = S𝑞 ∪ R𝑞 ∪ C𝑞).

Definition 5 (Source nodes). Each 𝑠 ∈ S𝑞 is a tuple (𝑖𝑑, DOI/URL,
excerpt, timestamp) representing external evidence retrieved for 𝑞.
Source nodes have no incoming edges.

Definition 6 (Reasoning nodes). Each 𝑟 ∈ R𝑞 is a tuple (id, infer-
ence, type, model) where type ∈ {deduction, induction, synthesis}
and model identifies the generating LLM.

Definition 7 (Claim nodes). Each 𝑐 ∈ C𝑞 is a tuple
(𝑖𝑑, statement, location) where statement is the factual assertion
answering (part of) 𝑞 and location specifies its position in the output.
Claim nodes have no outgoing edges.

Definition 8 (Typed edges). Each edge (𝑢, 𝑣, rel, 𝜈) ∈ 𝐸 connects
nodes with relation rel ∈ {supports, contradicts, refines, prerequisite}.
For supports edges, 𝜈 ∈ [0, 1] quantifies entailment strength; other-
wise 𝜈 = null.

Definition 9 (Provenance path). For any claim 𝑐 ∈ C𝑞, the prove-
nance path (𝜋 (𝑐)) is defined as the subgraph obtained by traversing
backward from 𝑐, where 𝑉𝑐 consists of all vertices 𝑣 ∈ 𝑉 that have
a directed path to 𝑐, and the source and reasoning subsets are given
by 𝑆𝑐 = 𝑉𝑐 ∩ S𝑞 and 𝑅𝑐 = 𝑉𝑐 ∩ R𝑞, respectively. This path traces
how specific sources 𝑆𝑐 support claim 𝑐 through reasoning 𝑅𝑐 , es-
tablishing the evidential lineage from 𝑞 to 𝑐.

Definition 2 (Provenance coverage: Can claims be traced?). The
fraction – 𝑃𝐶𝑜𝑣 – of claims with complete traceable paths from

We formalize the four AAR properties as computable functions

over these sets.

, ,

Razeen A Rasheed, Somnath Banerjee, Animesh Mukherjee, and Rima Hazra

Figure 4: Provenance tracking in RAG Systems. Black-box aggregation (left) versus transparent provenance (right) for identical
sources. Black-box reasoning hides two contradictions (𝑠3 ↔ 𝑐1, 𝑠4 ↔ 𝑐3), produces invalid citations, and leaves 𝑐2/𝑐3 ungrounded
– yielding 𝐶𝑇 𝑟𝑎𝑛 = 0.0, 𝑃𝑆𝑛𝑑 = 0.25 (1/4 valid pairs with 𝜈 > 0.5), 𝑃𝐶𝑜𝑣 = 0.33. Explicit reasoning surfaces model-size contradiction,
validates all citations and traces all claims – achieving 𝐶𝑇𝑟𝑎𝑛 = 1.0, 𝑃𝑆𝑛𝑑 = 1.0, 𝑃𝐶𝑜𝑣 = 1.0. Metrics computed using NLI entailment
scores (𝜈).

Provenance coverage: The fraction of claims with complete prove-
nance paths can be calculated as 𝑃𝐶𝑜𝑣 = | {𝑐 ∈ C:𝜋 (𝑐 ) is complete} |
Provenance soundness: For each claim-source pair (𝑐, 𝑠) where 𝑐
cites 𝑠, define semantic validity 𝜈 (𝑐, 𝑠) ∈ [0, 1] measuring whether
𝑠 entails 𝑐. Let P = {(𝑐, 𝑠) : 𝑐 ∈ C, 𝑠 ∈ S, 𝑐 cites 𝑠} be all citation
pairs.

| C |

𝑃𝑆𝑛𝑑 =

1

|P |

∑︁

(𝑐,𝑠 ) ∈ P

1[𝜈 (𝑐, 𝑠) > 𝜏entail]

where 𝜏entail is a domain-specific threshold.
Contradiction transparency: Define K = {(𝑠𝑖, 𝑠 𝑗, 𝑒) : 𝑠𝑖, 𝑠 𝑗 ∈
S, 𝑒 ∈ entities} as the set of source pairs making contradictory
claims about entity 𝑒. Let D be the subset of contradictions explicitly
detected and reported by the system. Quantitatively, 𝐶𝑇𝑟𝑎𝑛 = | D |
.
| K |
Audit effort: This is measured empirically through human verifi-
cation studies. Let 𝑇𝑐 be the time (minutes) required for a domain
expert to verify claim 𝑐 given access to: (1) the claim, (2) provenance
graph 𝜋 (𝑐), (3) cited sources. The audit effort can be calculated as
𝑇𝑐 where Csample is a representative sam-
𝐴𝐸 𝑓 𝑓 =
ple of claims. While 𝐴𝐸 𝑓 𝑓 measures human time, we can automate
this score by simply counting the number of steps and sources
in a claim’s provenance path. Since the graph is already machine-
readable, its structural complexity serves as a fast, automated proxy
for how much effort a human would actually need.
Measurement approach: We assess auditability through the above
four metrics. First, 𝑃𝐶𝑜𝑣 verifies that claims can be traced to their
sources. Second, 𝑃𝑆𝑛𝑑 uses formal verification to prove whether

(cid:205)𝑐 ∈ Csample

1
| Csample |

sources logically entail the attributed claims. Third, 𝐶𝑇𝑟𝑎𝑛 identi-
fies contradictions by testing entailment bidirectionally – checking
whether evidence supports the claim as well as whether conflicting
evidence exists. Fourth, 𝐴𝐸 𝑓 𝑓 measures verification time empiri-
cally through user studies with domain experts [44, 45]. Persistently
low AAR scores expose concrete architectural deficiencies – low
𝑃𝐶𝑜𝑣 reflects missing provenance infrastructure, low 𝑃𝑆𝑛𝑑 indi-
cates weak semantic verification, low 𝐶𝑇 𝑟𝑎𝑛 signals suppressed
contradictions, and high 𝐴𝐸 𝑓 𝑓 denotes poor intelligibility – mak-
ing these limitations visible and actionable rather than obscured by
aggregate performance metrics.
Example. For 𝑞 = “Does retrieval-augmented generation (RAG) im-
prove factual accuracy in long-form question answering compared
to parametric-only LLMs?”, the agent retrieves S𝑞 = {𝑠1, 𝑠2, 𝑠3, 𝑠4}
from the literature and generates output claims C𝑞 = {𝑐1, 𝑐2, 𝑐3}
where 𝑐1 states “RAG achieves 14-18% higher accuracy than para-
metric models”, 𝑐2 asserts “RAG is preferred architecture for all fac-
tual tasks”, and 𝑐3 claims “Improvements generalize across model
sizes and domains”. Figure 4 contrasts two architectures: black-
box aggregation (left) directly maps sources to claims without ex-
plicit reasoning, achieving 𝐶𝑇 𝑟𝑎𝑛 = 0.0 (contradictions between
𝑠3 → 𝑐1 and 𝑠4 → 𝑐3 remain hidden), 𝑃𝑆𝑛𝑑 = 0.25 (only 1 of 4 claim
nodes has complete traceable paths), and 𝑃𝐶𝑜𝑣 = 0.33 (only 𝑐1 is
valid; 𝑐2 and 𝑐3 are hallucinated or contradicted). In contrast, trans-
parent provenance (right) exposes intermediate reasoning nodes
R𝑞 = {𝑟1, 𝑟2, 𝑟3} with typed inference (synthesis, induction, deduc-
tion), explicitly surfaces the contradiction, and achieves perfect

Transparent Provenancec1: RAG improvesaccuracy by 14-18% formodels <1B parameterson open-domain QAc2: Large models (>30Bparameters) showcomparable or betterparametric-onlyperformancec3: Retrieval introduces23% contradiction rate inmulti-hop reasoninganswered byEntailsr1 (Synthesis):Extract accuracydeltas from s1 ands2Entailsr2 (Induction):Extract from s3  (GPT-3.5 175B: 82.3%parametric vs 79.1%RAG)Entailsr3 (Deduction):Quote s4 (23%contradiction), scopedto multi-hop, as alimitation.s1: Lewis et al. (2020) -RAG paper, NeurIPS2020  Contradiction  s2: Izacard & Grave(2021) - FiD paper,EACL 2021 s3: Mallen et al. (2023) -Parametric vs non-parametric, ACL 2023s4: Elazar et al. (2021) -Consistency study, TACL2021Claim Nodes (c1-c3)Reasoning Nodes with Type(r1-r3)Source Nodes (s1-s4)PCov = 3/3 = 1.0 | All claims have complete traceable pathsPSnd = 4/4 = 1.0 | All pairs valid CTran = 1/1 = 1.0 | 1 contradiction surfaced with conditional claimsEvaluation MetricsDoes retrieval-augmented generation (RAG) improve factualaccuracy in long-form question answering compared toparametric-only LLMs?Queryc1: RAG achieves 15-20% higher accuracythan parametricmodelsBlack Box Aggregations1: Lewis et al. (2020) - RAGpaper, NeurIPS 2020s2: Izacard & Grave (2021) -FiD paper, EACL 2021 s3: Mallen et al. (2023) -Parametric vs non-parametric, ACL 2023s4: Elazar et al. (2021) -Consistency study, TACL2021r1: Reasoningblack box c2: RAG is preferredarchitecture for allfactual tasksc3: Improvementsconsistent across allmodel sizes anddomainsClaim Nodes (c1-c3)Source Nodes (s1-s4)CTran = 0/2 = 0.0 | 2 contradictions exist (s3↔c1, s4↔c3), 0 surfacedPSnd = 1/4 = 0.25 | Only (c1,s1) valid; others hallucinated/contradictedPCov = 1/3 = 0.33 | Only c1 has traceable provenanceEvaluation MetricsDoes retrieval-augmented generation (RAG) improve factualaccuracy in long-form question answering compared toparametric-only LLMs?QueryFrom Fluent to Verifiable: Claim-Level Auditability for
Deep Research Agents

auditability: 𝑃𝐶𝑜𝑣 = 1.0, 𝑃𝑆𝑛𝑑 = 1.0, and 𝐶𝑇𝑟𝑎𝑛 = 1.0, enabling
systematic verification of each claim’s evidential support.

5 Perspective: Semantic provenance with

protocolized validation

We argue that auditable research agents need provenance graphs
with protocolized validation. By this we mean systematic verifi-
cation that measures entailment strength, source reliability, and
extraction confidence according to explicit protocols, operating con-
tinuously during synthesis rather than as post-hoc review. Vector-
based systems cannot reliably meet 𝑃𝐶𝑜𝑣, 𝑃𝑆𝑛𝑑, 𝐶𝑇𝑟𝑎𝑛, and 𝐴𝐸 𝑓 𝑓
because embedding similarity does not represent entailment or
contradiction. Similar wording can hide opposite claims, and aggre-
gation can erase disagreements. We therefore require provenance
that is persistent and queryable. It must record evidence support
with measured strength (entailment strength, source reliability, ex-
traction confidence). It must also represent conflicts and show how
each conflict was resolved. Finally, it must store reasoning traces
across decisions so reviewers can inspect why conclusions were
chosen and test counterfactual changes. We show that post-hoc ver-
ification does not scale because it cannot recover missing reasoning
chains and it arrives too late to prevent error build-up. Validation
should run during synthesis with continuous feedback. We also
integrate adversarial review into the provenance loop by writing
validates/challenges edges that trigger retrieval, revision, or human
escalation. Operational gating then blocks unverified claims from
entering downstream outputs.

6 Alternative views and objections
The provenance-first architecture faces four recurring objections
from practitioners prioritizing immediate deployment over verifi-
able research infrastructure. We address each systematically.
Bigger models will solve this. Scaling proponents argue that
larger models will show emergent capabilities, making external
provenance infrastructure unnecessary [33, 70]. We argue this claim
conflates generation quality with attribution accuracy. Current sys-
tems still exhibit architectural amnesia across both open-weight
and proprietary model families [32]. More importantly, provenance
is required even when the generated content is correct. If an agent
synthesizes conclusions from dozens of papers, users must ver-
ify which specific sources support each claim, and this need is
independent of model scale. Provenance also enables root-cause
analysis when failures occur, supports iterative refinement through
queryable audit trails, and provides reproducibility guarantees ex-
pected in scientific workflows [30, 62].
Graphs are too expensive. A common objection is that prove-
nance graphs are too expensive to maintain, especially for long-
running research workflows, and that flat logs are a more practical
option [51]. However, recent evidence suggests that graph-based
structure can be cost-effective in practice [10, 11, 15, 31]. Knowledge
graph of thoughts reports that graph-based task representations
reduce cost while also improving success rates compared to state-
less agents [11]. HippoRAG [10] similarly shows that graph-based
memory improves multi-hop reasoning that stateless retrieval of-
ten misses. Manual post-hoc validation can easily cost more than
generation, while architectural validation enables automated graph

, ,

checks that run in milliseconds per claim. At scale, research agents
generate unreliable papers through hallucinated content, and this
increases the risk of downstream reuse and training contamina-
tion [13, 57]. For this reason, provenance graphs should be viewed
as a cost control mechanism where they reduce verification effort,
limit error propagation, and lower the long-term cost of maintain-
ing a reliable scientific corpus.
Logs provide sufficient traceability. Some practitioners [7] claim
that timestamped logs provide enough traceability because they
are easy to collect and have low overhead. We argue that logs only
record actions and outputs; they do not capture why an agent makes
a choice or how specific evidence supports a claim. For example,
when The AI Scientist failed, the logs showed what ran, but they
did not explain the key reasoning mistakes, which forced hours of
manual inspection to piece together the decision path [32]. In con-
trast, semantic provenance graphs store explicit links from claims
to evidence and reasoning steps, including how the system handles
conflicting sources, which enables direct verification queries that
flat logs cannot support [30, 62].
Validation introduces prohibitive latency. Critics [4, 34, 65, 72]
argue that continuous verification adds latency and compute cost,
and they claim this reduces the value of automation. They argue
that when verification takes as long as generation, automation loses
its efficiency advantage. We disagree because this view treats verifi-
cation delay as the main cost and ignores larger downstream costs.
A small verification delay saves much more time by preventing hal-
lucinated reports that force long debugging and can contaminate
later analyses. Independent evaluators of The AI Scientist spend
expert effort similar to doing original research to find failures such
as the energy efficiency paradox (section 3.1).

7 Conclusion
Deep research agents are becoming capable of generating full sci-
entific narratives at scale, so the limiting factor is no longer writing
speed but whether outputs are verifiable before they pollute down-
stream science. This paper argues that today’s logs and citation
practices are structurally insufficient because they record actions
and references, not the claim-level evidence links needed to audit
correctness. We therefore propose “auditable-by-design” research
agents built around semantic provenance graphs that explicitly
connect sources → intermediate reasoning → final claims in a
persistent, queryable form, and we operationalize this goal with
the AAR standard; provenance coverage (are claims traceable),
provenance soundness (do sources actually support claims), contra-
diction transparency (are conflicts surfaced rather than averaged
away), and audit effort (can a human verify faster than redoing
the work). Framed this way, progress should be judged not only by
task success but by whether verification is cheaper than generation,
enabling scalable human oversight and safe autonomy. Looking
ahead, the key engineering and research agenda is to standardize
provenance schemas, improve entailment/contradiction checking
over heterogeneous sources, and build benchmarks that reward low
audit cost and high evidence fidelity so that agents produce not just
plausible papers, but inspectable scientific artifacts.

, ,

Razeen A Rasheed, Somnath Banerjee, Animesh Mukherjee, and Rima Hazra

References
[1] 2024. Wiley’s ’fake science’ scandal is just the latest chapter in a broader crisis

of trust. ABC News (Australia) (May 2024). Published May 20, 2024.

[2] 2026. HalluCitation Matters: Revealing the Impact of Hallucinated Citations.

arXiv (Jan. 2026). arXiv:2601.18724.

[3] Ibrahim Adabara, Bashir Olaniyi Sadiq, Aliyu Nuhu Shuaibu, Yale Ibrahim
Danjuma, and Venkateswarlu Maninti. 2025. Trustworthy Agentic AI Sys-
tems: A Cross-Layer Review of Architectures, Threat Models, and Gover-
nance Strategies for Real-World Deployment. F1000Research 14 (2025), 905.
doi:10.12688/f1000research.169927.1

[4] Gastão Amaral et al. 2024. ProVe: A pipeline for automated provenance ver-
ification of knowledge graphs against textual sources. Semantic Web Journal
(2024).

[5] Anthropic. 2025. Agentic Misalignment: How LLMs Could Be Insider Threats.
https://www.anthropic.com/research/agentic- misalignment. Accessed:
2026-02-04.

[6] Rauno Arike, Elizabeth Donoway, Henning Bartsch, and Marius Hobbhahn.
2025. Technical Report: Evaluating Goal Drift in Language Model Agents.
arXiv:2505.02709 [cs.AI] doi:10.48550/arXiv.2505.02709

[7] Adam Bates, Dave Tian, Kevin R. B. Butler, and Thomas Moyer. 2015. Trustwor-
thy Whole-System Provenance for the Linux Kernel. In 24th USENIX Security
Symposium (USENIX Security 15). USENIX Association, 319–334.

[8] Joeran Beel and Min-Yen Kan. 2025. Evaluating Sakana’s AI Scientist: Bold Claims,
Mixed Results, and a Promising Future? arXiv preprint arXiv:2502.14297 (2025).
https://arxiv.org/abs/2502.14297

[9] Khalid Belhajjame, Reza B’Far, James Cheney, Sam Coppens, Yolanda Gil, Paul
Groth, Graham Klyne, et al. 2013. PROV-DM: The PROV Data Model. Technical
Report. W3C Recommendation. https://www.w3.org/TR/prov-dm/

[10] Bernal Bernal, Weizhe Yuan, O Harari, et al. 2024. HippoRAG: Neurobiologically
Inspired Long-Term Memory for Large Language Models. In Advances in Neural
Information Processing Systems (NeurIPS), Vol. 37.

[11] Maciej Besta, Lorenzo Paleari, Jia Hao Andrea Jiang, Robert Gerstenberger, et al.
2025. Affordable AI Assistants with Knowledge Graph of Thoughts. arXiv preprint
arXiv:2504.02670 (2025).

[12] Siddhant Bhambri, Upasana Biswas, and Subbarao Kambhampati. 2025. Do
Cognitively Interpretable Reasoning Traces Improve LLM Performance? arXiv
preprint arXiv:2508.16695 (2025). https://arxiv.org/abs/2508.16695

[13] Wulfram Blau, Vinton G. Cerf, Juan Enriquez, Joseph S. Francisco, Urs Gasser,
Mary L. Gray, Mark Greaves, Barbara J. Grosz, Kathleen Hall Jamieson, Gerald H.
Haug, et al. 2024. Protecting scientific integrity in an age of generative AI.
Proceedings of the National Academy of Sciences 121, 22 (2024), e2407886121.
doi:10.1073/pnas.2407886121

[14] Daniil A Boiko, Robert MacKnight, Ben Kline, and Gabe Gomes. 2023. Au-
tonomous chemical research with large language models. Nature 624, 7992 (2023),
570–578. doi:10.1038/s41586-023-06792-0

[15] Vasilis Bountris, Lauritz Thamsen, and Ulf Leser. 2025. HyProv: Hybrid Prove-
nance Management for Scientific Workflows. arXiv preprint arXiv:2511.07574
(2025).

[16] Samuel R Bowman, Gabor Angeli, Christopher Potts, and Christopher D Manning.
2015. A large annotated corpus for learning natural language inference. In
Proceedings of the 2015 Conference on Empirical Methods in Natural Language
Processing. 632–642.

[17] Andres M Bran, Sam Cox, Oliver Schilter, Carlo Baldassari, Andrew D White, and
Philippe Schwaller. 2024. ChemCrow: Augmenting large-language models with
chemistry tools. Nature Machine Intelligence 6 (2024), 525–535. doi:10.1038/s42256-
024-00832-8

[18] C Brundy. 2024. The paper mill crisis is a five-alarm fire for science. Insights: the
UKSG journal (2024). Discusses Wiley/Hindawi retractions exceeding 11,300 as
of April 2024.

[19] Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A. Agrawal, et al. 2025. Why
Do Multi-Agent LLM Systems Fail? arXiv preprint arXiv:2503.13657 (2025).
[20] Mikaël Chelli, Jules Descamps, Vincent Lavoué, Christophe Trojani, Michel Azar,
Marcel Deckert, Jean-Luc Raynier, Gilles Clowez, Pascal Boileau, and Caroline
Ruetsch-Chelli. 2024. Hallucination Rates and Reference Accuracy of ChatGPT
and Bard for Systematic Reviews: Comparative Analysis. J Med Internet Res 26
(22 May 2024), e53164. doi:10.2196/53164

[21] Mikaël Chelli, Jules Descamps, Vincent Lavoué, Christophe Trojani, Michel Azar,
Marcel Deckert, Jean-Luc Raynier, Gilles Clowez, Pascal Boileau, and Caroline
Ruetsch-Chelli. 2024. Hallucination Rates and Reference Accuracy of ChatGPT
and Bard for Systematic Reviews: Comparative Analysis. Journal of Medical
Internet Research 26 (2024), e53164. doi:10.2196/53164

[22] I Chern, Steffi Chern, Shiqi Chen, Weizhe Yuan, K Feng, C Zhou, J He, Graham
Neubig, and Pengfei Liu. 2024. FacTool: Factuality Detection in Generative AI –
A Tool Augmented Framework. In Proceedings of the 2024 Conference of the North
American Chapter of the Association for Computational Linguistics.

[23] Mingxuan Du, Benfeng Xu, Chiwei Zhu, Xiaorui Wang, and Zhendong Mao. 2025.
DeepResearch Bench: A Comprehensive Benchmark for Deep Research Agents.

arXiv preprint arXiv:2506.11763 (2025).

[24] Yilun Du, Shuang Li, Antonio Torralba, Joshua B. Tenenbaum, and Igor Mordatch.
2023. Improving Factuality and Reasoning in Language Models through Multi-
agent Debate. In Advances in Neural Information Processing Systems (NeurIPS),
Vol. 36. 31114–31136.

[25] Sebastian Farquhar, Jannik Kossen, Lorenz Kuhn, and Yarin Gal. 2024. Detecting
hallucinations in large language models using semantic entropy. Nature 630
(2024), 625–630. doi:10.1038/s41586-024-07421-0

[26] Paul Fernsel, Cedric Maier, Ehsan Toreini, and Dominik Kowald. 2024. Assessing
the Auditability of AI-integrating Systems: A Framework and Learning Analytics
Case Study. arXiv preprint arXiv:2411.08906 (2024).

[27] Sharon Goldman. 2026. NeurIPS research papers contained 100+ AI-hallucinated

citations. Fortune (Jan. 2026). Published Jan 21, 2026.

[28] Jutta Haider, Björn Ekström, Kristofer Söderström, and Malte Rödl. 2024. AI-
fabricated “junk science” floods Google Scholar: Key features, spread, and impli-
cations for preempting evidence manipulation. https://www.hb.se/en/about-
ub/current/news-archive/2024/december/ai-fabricated-junk-science-floods-
google-scholar/

[29] Thomas Hartung. 2025. AI, agentic models and lab automation for scientific

discovery. Frontiers in Artificial Intelligence (2025). Frontiers.

[30] Melanie Herschel, Ralf Diestelkämper, and Houssem Ben Lahmar. 2017. A survey
on provenance: What for? What form? What from? The VLDB Journal 26, 6
(2017), 881–906.

[31] Yikuan Hu, Jie Zhou, Ganqu Cui, Shengding Hu, and Maosong Sun. 2025. Re-
MindRAG: Low-Cost LLM-Guided Knowledge Graph Traversal for Efficient RAG.
arXiv preprint arXiv:2510.13193 (2025).

[32] Moritz Baumgart Joeran Beel, Min-Yen Kan. 2025. Evaluating Sakana’s AI Scientist
for Autonomous Research. arXiv preprint arXiv:2502.14297 (2025). https://arxiv.
org/html/2502.14297v2

[33] Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess,
Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. 2020.
Scaling Laws for Neural Language Models. arXiv preprint arXiv:2001.08361 (2020).
[34] Roham Koohestani et al. 2025. AgentGuard: Runtime Verification of AI Agents.

arXiv preprint arXiv:2509.23864 (2025).

[35] Minghao Li, Ying Zeng, Zhihao Cheng, Cong Ma, and Kai Jia. 2025. ReportBench:
Evaluating Deep Research Agents via Academic Survey Tasks. arXiv preprint
arXiv:2508.15804 (2025). https://arxiv.org/abs/2508.15804

[36] Miles Q. Li, Benjamin C. M. Fung, Martin Weiss, Pulei Xiong, Khalil Al-Hussaeni,
and Claude Fachkha. 2026. A Benchmark for Evaluating Outcome-Driven
Constraint Violations in Autonomous AI Agents. arXiv:2512.20798 [cs.AI]
https://arxiv.org/abs/2512.20798

[37] Q. Vera Liao and Jennifer Wortman Vaughan. 2024. AI Transparency in the Age
of LLMs: A Human-Centered Research Roadmap. Harvard Data Science Review 6,
2 (2024).

[38] Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker,
Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. 2023. Let’s
Verify Step by Step. arXiv preprint arXiv:2305.20050 (2023).

[39] Zachary C Lipton. 2018. The Mythos of Model Interpretability. Queue 16, 3 (2018),

31–57.

[40] Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua,
Fabio Petroni, and Percy Liang. 2024. Lost in the Middle: How Language Models
Use Long Contexts. Transactions of the Association for Computational Linguistics
12 (2024), 157–173.

[41] Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, and David Ha.
2024. The AI Scientist: Towards fully automated open-ended scientific discovery.
arXiv preprint arXiv:2408.06292 (2024). https://arxiv.org/abs/2408.06292
[42] Ruofan Lu, Yichen Li, and Yintong Huo. 2025. Exploring Autonomous Agents:
A Closer Look at Why They Fail When Completing Tasks. arXiv preprint
arXiv:2508.13143 (2025). https://arxiv.org/abs/2508.13143

[43] Potsawee Manakul, Adian Liusie, and Mark J. F. Gales. 2023. SelfCheckGPT: Zero-
Resource Black-Box Hallucination Detection for Generative Large Language
Models. arXiv preprint arXiv:2303.08896 (2023).

[44] Ananya Mantravadi, Shivali Dalmia, Olga Pospelova, Abhishek Mukherji, Nand
Dave, and Anudha Mittal. 2025. LegalWiz: A Multi-Agent Generation Framework
for Contradiction Detection in Legal Documents. arXiv preprint arXiv:2510.03418
(2025). Corrected authors (previously attributed to Zhang)..

[45] Dasha Metropolitansky and Jonathan Larson. 2025. VeriTrail: Closed-Domain
Hallucination Detection with Traceability. arXiv preprint arXiv:2505.21786 (2025).
[46] Sewon Min, Kalpesh Krishna, Xinxi Lyu, Mike Lewis, Wen-tau Yih, Pang Wei Koh,
Mohit Iyyer, Luke Zettlemoyer, and Hannaneh Hajishirzi. 2023. FActScore: Fine-
grained Atomic Evaluation of Factual Precision in Long Form Text Generation.
In Proceedings of the 2023 Conference on Empirical Methods in Natural Language
Processing. 12076–12100.

[47] Sonia Natalie Mitchell, Andrew Lahiff, Nathan Cummings, Jonathan Hollocombe,
Bram Boskamp, Ryan Field, Dennis Reddyhoff, Kristian Zarebski, Antony Wilson,
Bruno Viola, et al. 2022. FAIR Data Pipeline: provenance-driven data management
for traceable scientific workflows. Philosophical Transactions of the Royal Society
A 380, 2233 (2022), 20210300. doi:10.1098/rsta.2021.0300

, ,

[70] Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebastian
Borgeaud, Dani Yogatama, Maarten Bosma, Denny Zhou, Donald Metzler, et al.
2022. Emergent Abilities of Large Language Models. Transactions on Machine
Learning Research (2022). https://openreview.net/forum?id=yzkSU5zdwD
[71] Robert Wolfe, Isaac Slaughter, Bin Han, Bingbing Wen, Yiwei Yang, Lucas Rosen-
blatt, Bernease Herman, Eva Brown, Zening Qu, Nic Weber, and Bill Howe.
2024. Laboratory-Scale AI: Open-Weight Models are Competitive with Chat-
GPT Even in Low-Resource Settings. arXiv preprint arXiv:2405.16820 (2024).
https://arxiv.org/abs/2405.16820

[72] Boming Xia, Qinghua Lu, Liming Zhu, Zhenchang Xing, Dehai Zhao, and Hao
Zhang. 2024. Evaluation-Driven Development and Operations of LLM Agents: A
Process Model and Reference Architecture. In arXiv preprint arXiv:2411.13768.

[73] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu,
Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P Xing, et al. 2024. Judg-
ing LLM-as-a-Judge with MT-Bench and Chatbot Arena. Advances in Neural
Information Processing Systems 36 (2024).

[74] Qinhao Zhou, Zihan Zhang, Xiang Xiang, Ke Wang, Yuchuan Wu, and Yongbin
Li. 2024. Enhancing the General Agent Capabilities of Low-Parameter LLMs
through Tuning and Multi-Branch Reasoning. arXiv preprint arXiv:2403.19962
(2024). https://arxiv.org/abs/2403.19962

[75] Jialiang Zhu, Gongrui Zhang, Xiaolong Ma, Lin Xu, Miaosen Zhang, Ruiqi Yang,
Song Wang, Kai Qiu, Zhirong Wu, Qi Dai, Ruichun Ma, Bei Liu, Yifan Yang,
Chong Luo, Zhengyuan Yang, Linjie Li, Lijuan Wang, Weizhu Chen, Xin Geng,
and Baining Guo. 2025. RE-TRAC: REcursive TRAjectory Compression for Deep
Search Agents. arXiv preprint arXiv:2602.02486 (2025).

[76] Minjun Zhu, Qiujie Xie, Yixuan Weng, Jian Wu, Zhen Lin, Linyi Yang, and Yue
Zhang. 2025. AI Scientists Fail Without Strong Implementation Capability. arXiv
preprint arXiv:2506.01372 (2025).

From Fluent to Verifiable: Claim-Level Auditability for
Deep Research Agents

[48] Luc Moreau and Paul Groth. 2013. Provenance: An Introduction to PROV. Morgan

& Claypool Publishers.

[49] Luc Moreau, Paolo Missier, Khalid Belhajjame, Reza B’Far, James Cheney, Sam
Coppens, Yolanda Gil, Paul Groth, Graham Klyne, Timothy Lebo, et al. 2013.
PROV-DM: The PROV Data Model. W3C Recommendation. World Wide Web
Consortium (W3C). https://www.w3.org/TR/prov-dm/

[50] Akshat Naik, Patrick Quinn, Guillermo Bosch, Emma Gouné, Francisco
Javier Campos Zabala, Jason Ross Brown, and Edward James Young. 2025. Agent-
Misalignment: Measuring the Propensity for Misaligned Behaviour in LLM-Based
Agents. arXiv:2506.04018 [cs.AI] https://arxiv.org/abs/2506.04018

[51] Thomas Pasquier, Xueyuan Han, Mark Goldstein, Thomas Moyer, David Eyers,
Margo Seltzer, and Jean Bacon. 2017. Practical Whole-System Provenance Capture.
In Proceedings of the 2017 Symposium on Cloud Computing (SoCC ’17). 405–418.
[52] Luca Della Pellegrina, Ylber Haxhimusa, Raza Malik, et al. 2025. AI for scientific
integrity: Detecting ethical breaches, errors, and fraud using generative AI tools
and large language models. Frontiers in Artificial Intelligence 8 (2025), 1644098.
doi:10.3389/frai.2025.1644098

[53] Karl Popper. 1959. The Logic of Scientific Discovery. Hutchinson, London.
[54] Paul Rasmussen and The Zep Team. 2025. Zep: A Temporal Knowledge Graph
Architecture for Agent Memory. arXiv preprint arXiv:2501.13956 (2025).
[55] Anjali Sharma, Christopher Lin, et al. 2025. ResearchRubrics: Auditing the
Citation Integrity of Deep Research Agents. arXiv preprint arXiv:2511.07685
(2025).

[56] Manasi Sharma, Chen Bo Calvin Zhang, Chaithanya Bandi, Clinton Wang,
Ankit Aich, Huy Nghiem, Tahseen Rabbani, Ye Htet, Brian Jang, Sumana Basu,
Aishwarya Balwani, Denis Peskoff, Marcos Ayestaran, Sean M. Hendryx, Brad
Kenstler, and Bing Liu. 2025. ResearchRubrics: A Benchmark of Prompts
and Rubrics For Evaluating Deep Research Agents. arXiv:2511.07685 [cs.AI]
https://arxiv.org/abs/2511.07685

[57] Ilia Shumailov, Zakhar Shumaylov, Yiren Zhao, Yarin Gal, Nicolas Papernot, and
Ross Anderson. 2024. AI models collapse when trained on recursively generated
data. Nature 631 (2024), 755–759. doi:10.1038/s41586-024-07566-y

[58] Ilia Shumailov, Zakhar Shumaylov, Yiren Zhao, Nicolas Papernot, Ross Anderson,
and Yarin Gal. 2024. AI models collapse when trained on recursively generated
data. Nature 631, 8022 (01 Jul 2024), 755–759. doi:10.1038/s41586-024-07566-y
[59] Sameer Kumar Singh. 2026. State Drift in Language-Conditioned Autonomous
Agents: A Failure Mode of Long-Horizon Reasoning. Preprints (January 2026).
doi:10.20944/preprints202601.0910.v1

[60] Kevin Song, Anand Jayarajan, Yaoyao Ding, Qidong Su, Zhanda Zhu, Sihang Liu,
and Gennady Pekhimenko. 2025. Aegis: Taxonomy and Optimizations for Over-
coming Agent-Environment Failures in LLM Agents. arXiv:2508.19504 [cs.MA]
https://arxiv.org/abs/2508.19504

[61] Renan Souza, Rafael Ferreira da Silva, et al. 2024. Workflow Provenance in the
Computing Continuum for Responsible, Trustworthy, and Energy-Efficient AI.
In Proceedings of the 2024 IEEE International Conference on Cluster Computing
(CLUSTER). IEEE.

[62] Renan Souza, Amal Gueroudji, Stephen DeWitt, Daniel Rosendo, Tirthankar
Ghosal, Robert Ross, Prasanna Balaprakash, and Rafael Ferreira da Silva. 2025.
PROV-AGENT: Unified Provenance for Tracking AI Agent Interactions in Agentic
Workflows. In 2025 IEEE 21st International Conference on e-Science (e-Science).
IEEE.

[63] Yoo Yeon Sung, Hannah Kim, and Dan Zhang. 2025. VeriLA: A Human-Centered
Evaluation Framework for Interpretable Verification of LLM Agent Failures.
arXiv:2503.12651 [cs.AI] https://arxiv.org/abs/2503.12651

[64] Nathan J Szymanski, Bernardus Rendy, Yuxing Fei, Rishi E Kumar, Tanjin He,
David Milsted, Matthew J McDermott, Max Gallant, Ekin Dogus Cubuk, Amil
Merchant, et al. 2023. An autonomous laboratory for the accelerated synthesis of
novel materials. Nature 624, 7990 (2023), 86–91. doi:10.1038/s41586-023-06734-w
[65] SpecMAS Team. 2025. SpecMAS: A Multi-Agent System for Self-Verifying Sys-
tem Generation via Formal Model Checking. In Advances in Neural Information
Processing Systems (NeurIPS).

[66] Pranav Narayanan Venkit, Philippe Laban, Yilun Zhou, Kung-Hsiang Huang,
Yixin Mao, and Chien-Sheng Wu. 2026. DeepTRACE: Auditing Deep Research AI
Systems for Tracking Reliability Across Citations and Evidence. In The Fourteenth
International Conference on Learning Representations. https://openreview.net/for
um?id=QkaeTea16Y

[67] Andrew Wang, Sophia Hager, Adi Asija, Daniel Khashabi, and Nicholas Andrews.
2025. Hell or High Water: Evaluating Agentic Recovery from External Failures.
In Second Conference on Language Modeling. https://openreview.net/forum?id=
Zk224WPT42

[68] Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang,
Zhiyuan Chen, Jiakai Tang, Xu Chen, Yankai Lin, et al. 2024. A Survey on Large
Language Model based Autonomous Agents. arXiv preprint arXiv:2308.11432
(2024).

[69] Yuxia Wang, Bela GIpp, and G Spanakis. 2024. Factcheck-GPT: End-to-End
Fact-Checking with Large Language Models. arXiv preprint arXiv:2311.09657
(2024).


