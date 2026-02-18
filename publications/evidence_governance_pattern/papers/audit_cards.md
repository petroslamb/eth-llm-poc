Audit Cards: Contextualizing AI Evaluations

Leon Staufer1,2*, Mick Yang1,3*, Anka Reuel4, Stephen Casper5,1
1ML Alignment & Theory Scholars
2Technical University of Munich
3University of Pennsylvania
4Stanford University
5Massachusetts Institute of Technology
leon@staufer.me, mickyang@seas.upenn.edu

5
2
0
2

g
u
A
4
1

]

Y
C
.
s
c
[

2
v
9
3
8
3
1
.
4
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

AI governance frameworks increasingly rely on audits, yet
the results of their underlying evaluations require interpreta-
tion and context to be meaningfully informative. Even techni-
cally rigorous evaluations can offer little useful insight if re-
ported selectively or obscurely. Current literature focuses pri-
marily on technical best practices, but evaluations are an in-
herently sociotechnical process, and there is little guidance on
reporting procedures and context. Through literature review,
stakeholder interviews, and analysis of governance frame-
works, we propose “audit cards” to make this context explicit.
We identify six key types of contextual features to report
and justify in audit cards: auditor identity, evaluation scope,
methodology, resource access, process integrity, and review
mechanisms. Through analysis of existing evaluation reports,
we find significant variation in reporting practices, with most
reports omitting crucial contextual information such as audi-
tors’ backgrounds, conflicts of interest, and the level and type
of access to models. We also find that most existing regula-
tions and frameworks lack guidance on rigorous reporting. In
response to these shortcomings, we argue that audit cards can
provide a structured format for reporting key claims along-
side their justifications, enhancing transparency, facilitating
proper interpretation, and establishing trust in reporting.

1

Introduction

AI governance frameworks1 are being designed to increas-
ingly rely on audits.2 Within these frameworks, audits are
meant to (1) identify potential risks, (2) incentivize more re-
sponsive development practices, and (3) involve more stake-
holders in the system deployment process. However, audits
can only fulfill this role effectively if the underlying eval-
uations are both technically rigorous and effectively inte-
grated into decision-making (Hardy et al. 2024). However,

*These authors contributed equally.

Under review for AAAI-26. Updated August 2025.

1This includes frontier AI safety policies from AI companies
(e.g. OpenAI Preparedness Framework), regulations (e.g. US AI
Action Plan, EU AI Act), and other norms (e.g. NIST AI Risk Man-
agement Framework). See Appendix D for a complete list.

2We understand audits as formalized evaluation processes of AI
models. We refer to the specific evaluation procedure (e.g. bench-
marking, red-teaming, uplift studies) underlying the audit as eval-
uations. See Appendix A for an overview of key terms.

not all evaluations are equally rigorous (e.g., Raji et al. 2022;
Birhane et al. 2024; M¨okander 2023; Anderljung et al. 2023;
Kolt et al. 2024; Casper et al. 2024; Reuel et al. 2024b; Li
and Goel 2024).

To date, much prior literature has focused on the tech-
nical side of audits (see Section 2). However, evaluations
are never conducted in a vacuum (Wallach et al. 2025).
Their results are intimately shaped, not only by the technical
methods employed, but by numerous non-technical details
of their context and design (see Section 3). For example,
while the research field has long understood the importance
of conflict of interest disclosures for academic integrity (e.g.,
Knerr and D’Amelia 2020), auditor independence remains a
consistent concern in the AI ecosystem (Costanza-Chock,
Raji, and Buolamwini 2022; Evans et al. 2023).

Even technically rigorous evaluations can be uninforma-
tive or actively misleading if reported on selectively or ob-
scurely (Ananny and Crawford 2018). This risk is magnified
given the vested interest of AI developers in obtaining fa-
vorable audit results. In AI and other fields, companies un-
dergoing evaluations have strong incentives to game audits
and influence reporting in potentially misleading ways (e.g.,
Krawiec 2003; Lu 2006; Marquis, Toffel, and Zhou 2016).

Thus, for AI audits to play a meaningful role in gov-
ernance, evaluation reporting must be done in a way that
minimizes the chance of omitting key contextual informa-
tion. To address this challenge, we propose “audit cards”:
a structured reporting framework to document the context
of an AI audit rather than the evaluated system itself (Fig-
ure 1). Unlike model and system cards (Mitchell et al. 2019),
which document system characteristics and capabilities, au-
dit cards address the distinct transparency requirements of
evaluation processes-specifically the contextual factors that
shape how evaluations are conducted and reported. They are
designed to offer a standardized approach to reporting that
enhances transparency and facilitates informed interpreta-
tions of results. This need not necessarily be reported in a
separate audit card document, rather the relevant context can
be added as sections in existing model and system cards.

Overall, we make four key contributions:

1. Audit cards framework addressing evaluation trans-
parency gaps: Based on a survey of 28 prior works on AI
evaluations (Section 3), we synthesise existing literature

General principles of
reporting on audits

Justification

Limitations

Assumptions

Specific contextual features to report on in audits

Who are the auditors?
• Expertise
• Background

Review & Communication
• Review mechanism
• Feedback channel
• Executive summary
• Defintions of key terms
• Access to results

What is evaluated?
• Scope and goal
• Type of evaluation
• Continuous evaluations
• Obsolescence criteria

Integrity
• Selection process
• Conflicts of interest
• Compensation and
incentive structures

How is it evaluated?
• Desc. of evaluation setup
• Justification of

capability-to-goal
translation

• Interpretation of scores

Access and Resources
• Level of access
• Compute, time, financial

resources available

Figure 1: Our audit card template requires reporting on three principles and six features. (Left) The three cross-cutting principles
(justification, limitations, and assumptions) further transparency about the process behind an audit. (Right) The six features offer
key methodological and contextual information. See Section 3 and Appendix C for details.

to propose a template and checklist (Appendix C) for AI
audit cards that addresses transparency needs not covered
by existing tools, including three cross-cutting principles
(justification, limitations, and assumptions) and six key
types of contextual information (auditor identity, evalu-
ation scope, methodology, resource access, process in-
tegrity, and review mechanisms).

2. Survey of frontier AI evaluation reports: We analyze
the thoroughness of 24 existing evaluation reports for
frontier systems (Section 4).

3. Survey of governance frameworks: We analyze gaps
between best reporting practices and 21 existing AI gov-
ernance frameworks (Section 5).

4. Stakeholder insights: We interview and present perspec-
tives from 10 expert stakeholders on AI evaluation report-
ing practices (Section 6).

2 Related work
Transparency and reporting: In the past decade, fron-
tier AI research and development have largely shifted
from being predominantly academia-driven to predomi-
nantly industry-driven (Maslej et al. 2024). This shift has
been accompanied by a decrease in transparency around pro-
prietary state-of-the-art systems. As such, increasing trans-
parency and awareness has emerged as a key goal of AI gov-
ernance (e.g., Felzmann et al. 2020; Haresamudram, Lars-
son, and Heintz 2023; Winecoff and Bogen 2024; Chan et al.
2024; Bommasani et al. 2024; Kolt et al. 2024). One barrier
to meaningful transparency is a lack of standards for report-
ing (Maslej et al. 2024). In response to this challenge, pre-
vious works have proposed data, model, system, agent, and
usage “cards” (Pushkarna, Zaldivar, and Kjartansson 2022;
Mitchell et al. 2019; Gursoy and Kakadiaris 2022; Casper
et al. 2025; Wahle et al. 2023) for documenting key infor-
mation within the AI ecosystem. In this paper, we build on
past work by introducing the notion of an “audit card,” sur-
veying what prior literature suggests they should contain,
and analyzing the current state of reporting around audits.

AI audits: Formal evaluations, also known as “audits,”
of AI systems have been proposed as a key objective to
facilitate transparency and scrutiny (Raji et al. 2022; An-
derljung et al. 2023; M¨okander 2023; Li and Goel 2024;
Reuel et al. 2024a). Meanwhile, audits are increasingly in-
corporated into frameworks for AI governance (e.g., EU AI
Act 2024). However, as we will show in Section 5, current
governance frameworks often lack substantial guidance for
how to report on audits.

Technically rigorous evaluations: AI systems are au-
dited using a variety of approaches including case studies,
benchmarks, red-teaming, and mechanistic analysis (Ben-
gio et al. 2024). However, the science of evaluating AI sys-
tems is still nascent (Apollo Research 2024). Not all eval-
uations are equally technically rigorous, and their appar-
ent outcomes can be highly sensitive to framing and design
(e.g., Schaeffer, Miranda, and Koyejo 2023; Burnell et al.
2023; Khan, Casper, and Hadfield-Menell 2025). Toward
improved technical practices, Reuel et al. (2024b) outline
a set of 46 best practices for rigorous AI benchmark design.
Meanwhile, METR (2024) work toward a portable standard
for framing and conducting capability evaluations. However,
unlike prior work, here we focus on rigor in reporting both
key technical details and context behind AI audits.

On the inherent sociotechnical nature of evaluations:
AI evaluations depend on technical tools to assess system
properties and risks. However, they are never conducted in a
vacuum; they are always embedded in a broader sociotech-
nical and political context. Meanwhile, the standards that
systems are evaluated against are inherently based on sub-
jective human values. Thus, AI evaluations represent a so-
cial science measurement challenge (Wallach et al. 2025).
Aside from lacking technical soundness, evaluations can fail
to be rigorous and serve the public’s interest for a vari-
ety of nontechnical reasons. Prior works have emphasized
the role of evaluation integrity and integration in ensuring
meaningful oversight (Ojewale et al. 2024; Raji et al. 2022;
Sharkey et al. 2024). By surveying prior literature on evalu-
ation procedures (Section 3), analyzing current evaluation

reports (Section 4), and analyzing evaluation frameworks
(Section 5), we make progress toward a more contextual and
critical understanding of AI audits.

3 What information do audit cards need for

rigorous reporting?

Methodology: We identify key components of audit cards
through an initial literature review of work on AI audits and
evaluations, transparency, technical evaluation design, and
sociotechnical approaches.3 We selected 28 total papers and
manually annotated them, scoring the extent to which the pa-
per recommends that aspect of reporting: is it a major argu-
ment of the paper (2), a minor argument of the paper (1), or
not mentioned in the paper (0). See Appendix B for further
details on the methodology. In Table 1, we summarize the
perspectives from all 28 papers on the three principles and
six features. It’s aim is to be a comprehensive and exhaustive
overview of audit features based on the relevant literature.
Next, we expand on these principles and features. See Fig-
ure 1 for an overview of an audit card and Appendix C for an
actionable audit card checklist that discusses the relative im-
portance of principles and features for different stakeholders
and auditing types.

Overarching principles for transparent reporting
The following three overarching principles behind auditing
are key for transparency and methodological clarity. These
apply across the entire auditing process and the six specific
features. We design audit cards to make it easier to adopt
these principles throughout the auditing process. This, in re-
turn, enables accurate interpretation, facilitates constructive
critique, and builds trust in the evaluation process.

Justifications as explicit arguments to support method-
ological choices, metric selection, and interpretative
frameworks. Explicit reporting on justifications enables
process transparency. This justification can be through el-
ements of a rigorous scientific process, such as explain-
ing proxies and experimental coverage (Apollo Research
2024), or through standardized auditing procedures, such
as detailed standards identification (Birhane et al. 2024;
Costanza-Chock, Raji, and Buolamwini 2022).

Assumptions to articulate the premises underlying the
evaluation design and analysis.4 Reporting on assump-
tions clarifies the relationship (or lack thereof) between tests
and real-world outcomes, presumptions about what consti-
tutes “good” performance, and details about the threat mod-
els considered (Reuel et al. 2024b; Barnett and Thiergart
2024a,b; Raji et al. 2020).

Limitations to explicitly acknowledge the constraints
that affect the validity, reliability, or generalizability of
findings. Reporting limitations clarifies constraints in data
sampling, potential artifacts in the evaluation process, and
boundaries of what auditors can reasonably claim based on

3We also refined our audit card template based on structured

interviews with expert stakeholders. See Section 6.

4This differs from justifications insofar that they answer “Why
did we choose this approach?” whereas assumptions answer “What
are we taking as given?”

the evaluation evidence (M¨okander et al. 2024; Barnett and
Thiergart 2024b; Reuel et al. 2024b).

Specific features for contextual information
Aside from overarching principles, reporting on more spe-
cific contextual features of audits helps stakeholders assess
trustworthiness. We compile recommendations from past lit-
erature into six features for reporting evaluation context in
audit cards. For a more granular analysis, see Appendix C,
where we further divide these six features into constituent
aspects.

• Who are the auditors: Reporting details of auditor iden-
tity facilitates trust and clarifies what potential biases
might affect their work. It includes reporting the expertise
(relevant domain knowledge, accreditations) (Anderljung
et al. 2023; METR b; Reuel et al. 2024b) and back-
ground (track record of conducting evaluations, position-
ality) of auditors (Costanza-Chock, Raji, and Buolamwini
2022; Gebru et al. 2021). Given worries about the pri-
vacy of auditors, information about the background can
be anonymized and aggregated.

• What is evaluated: Reporting on evaluation goals en-
ables clear interpretation of findings. This includes the
scope (e.g., model vs. scaffolding) and goal (context of
use) (Raji et al. 2020; Birhane et al. 2024; Shevlane et al.
2023), type of evaluation (e.g., capability vs. propensity),
as the scope of the evaluation influences what the rele-
vant level of access is (METR 2024; Liang et al. 2023), as
well as reporting on the evaluation obsolescence criteria
(Joaquin et al. 2025).5 It also includes reporting whether
the evaluation will be repeated, and if so, at what time
or after which conditions are met (Barnett and Thiergart
2024b; Anderljung et al. 2023).

• How is it evaluated: Explaining the underlying proce-
dures for the evaluation, such as descriptions of the eval-
uation setup with justifications of how a capability trans-
lates to evaluation goal (Apollo Research 2024; Raji et al.
2020; Reuel et al. 2024b) and provide interpretation of
scores (Dobbe, Krendl Gilbert, and Mintz 2021; Selbst
et al. 2019). The specific relevant aspects to report for this
feature may change depending on the underlying evalu-
ation. We therefore refer to the appropriate literature for
the underlying evaluation for a complete list of relevant
aspects to report and details on how to report on them, e.g.
for benchmarks (Reuel et al. 2024b).

• Access and resources: Report

the constraints under
which the evaluation was conducted to allow readers
to critically assess the audit’s limitations. This includes,
what access auditors have to a system (black/white box,
with/without safeguards) and which resources available
are available (compute, time, funding) as this can have
a large impact on the rigor of evaluations (Barnett and
Thiergart 2024b; Ojewale et al. 2024; Casper et al. 2024).

5Examples of obsolescence criteria could include substantial
amounts of model fine-tuning, changes in system components, or
changes in deployment context. This helps stakeholders understand
the shelf life of the findings.

Paper

Anderljung et al. 2023
Apollo Research 2024
Barnett and Thiergart 2024a
Barnett and Thiergart 2024b
Birhane et al. 2024
Bucknall and Trager 2023
Burnell et al. 2023
Casper et al. 2024
Chang et al. 2023
Costanza-Chock, Raji, and Buolamwini 2022
Dobbe, Krendl Gilbert, and Mintz 2021
Dow et al. 2024
Eriksson et al. 2025
Gallifant et al. 2025
Gebru et al. 2021
Hendrycks and Woodside 2024
Kolt et al. 2024
Liang et al. 2023
METR b
M¨okander et al. 2024
Mukobi 2024
Ojewale et al. 2024
Raji et al. 2020
Reuel et al. 2024b
Selbst et al. 2019
Shevlane et al. 2023
Weidinger et al. 2025
Zhan et al. 2024

Principles

Justif. Assum.

Features
Limit. Who What How Access

Integrity Review

1
2
2
1
2
0
2
1
0
2
2
0
2
2
1
0
1
1
0
0
0
1
0
0
0
0
2
2

2
2
2
2
2
2
2
2
2
2
2
2
2
2
2
0
1
2
0
2
2
2
2
2
2
2
2
2

2
0
0
2
2
2
0
0
0
0
2
0
1
2
2
1
0
0
0
2
0
0
2
2
2
2
2
2

2
0
1
0
2
0
0
1
2
2
2
1
1
2
2
0
2
0
2
1
2
2
2
2
2
2
0
1

2
2
0
2
2
2
1
0
0
1
1
2
2
2
1
0
1
2
2
2
2
1
2
2
0
2
2
2

2
2
0
2
0
0
2
0
2
0
2
2
2
2
2
2
0
0
2
1
2
1
2
2
2
2
2
2

2
0
0
2
1
2
0
2
0
2
0
0
0
1
2
0
0
0
0
2
2
2
1
0
0
2
0
0

2
0
0
2
2
2
0
0
0
1
0
0
1
2
2
0
2
0
0
2
2
1
0
0
0
2
0
0

2
0
0
0
2
2
2
1
0
2
2
0
0
2
2
1
2
0
2
2
1
1
1
2
0
2
1
2

Table 1: What contextual details do prior works say are key for audit reporting? We divide reporting into three overarching
principles (justifications, assumptions, limitations) and six key features (who, what, how, access, integrity, review). We score
each paper’s extent of recommendation of each these as 2 (major argument), 1 (minor argument), and 0 (no mention). Refer to
Table 4 for our complete, more granular analysis of papers.

• Integrity: Accountability for the auditing process estab-
lishes trust in auditors and rules out potential conflicts of
interest. This includes reporting transparently about the
selection process (how auditors were chosen) and com-
pensation (funding sources, incentive structures). These
dynamics can significantly affect the evaluation process
and are therefore crucial context (Birhane et al. 2024;
Costanza-Chock, Raji, and Buolamwini 2022; Gebru et al.
2021).

• Review and communication: Reports on if and what in-
dependent reviews of audit methods facilitate accountabil-
ity6 (Reuel et al. 2024b; Anderljung et al. 2023). This fur-
ther includes contact information and avenues for correc-
tions, executive summaries (covering the evaluation pro-
cess and result for non-technical audiences), and clear
definitions of key terms (Gebru et al. 2021; Bucknall and
Trager 2023; METR 2024; Reuel et al. 2024b).

Some of the above features may be considered confi-

6We discuss issues of intellectual property and non-disclosure
agreements (NDAs) standing in the way of internal review in Sec-
tion 6 and Section 7. This review can be performed by experts at
the organization by cross-checking the final report, insofar as they
were not involved in the evaluation beforehand.

dential in certain contexts, with academic researchers po-
tentially sharing different details than commercial entities
(Mitchell et al. 2019). Recommendations about how and
with whom audit cards should be shared are beyond the
scope of this report. However, redactions offer a simple,
well-precedented approach for protecting sensitive informa-
tion (Boone, Floros, and Johnson 2015).

4 What do existing evaluation reports

include?

Methodology: To study the thoroughness of existing eval-
uation reports, we examined 24 reports produced between
2023 and 2025. We selected these 24 due to their focus on
frontier systems, ensuring to include reports from both de-
velopers and third party organizations. We manually anno-
tated each report using the 3 principles and 6 features from
our audit card template (Section 3). For each audit card
component, we scored reports on a 0-2 scale for compre-
hensively reporting that component (2), minimally reporting
that component (1), not reporting on this component at all
(0). We assessed reporting thoroughness only, not execution
quality, making no judgments about how well evaluations
were executed. This means, for example, transparently re-

porting that there was a lack of any review/feedback process
and justifying this would receive a full score of 2. We sum-
marize the findings in Table 2.

While all evaluation reports provide at least a gen-
eral overview of procedures, the level of detail differs.
We find that audit reports consistently offer information on
evaluation scope (average score 1.38) and procedures (1.29)
used. However, contextual details are much less consistently
reported (average 0.94, σ = 0.68) both across organiza-
tions and sometimes within the same organization. For ex-
ample, Google DeepMind released four documents with sig-
nificantly varying levels of contextual detail (average scores
of 1.00, 0.67, 0.56, 1.44, and 1.44 in chronological order).
Only some reports (e.g., Meinke et al. (2025); Gemma Team
et al. (2024); ¨Ust¨un et al. (2024)) offered detailed informa-
tion on the scaffolding used to evaluate the system.

Reports inconsistently address assumptions, limita-
tions, and auditor information. While justifications and
limitations are more commonly acknowledged (22 of 24)
than assumptions (16 of 24), they are typically discussed
at a high level rather than relating to specific methodologi-
cal choices. Ten reports discuss limitations minimally, while
twelce do so comprehensively. However, there are notable
qualitative differences even among more comprehensive dis-
cussions. For example, ¨Ust¨un et al. (2024) discuss limita-
tions in prompting techniques, language transferability, eval-
uation tool chaining, and reproducibility in significant detail,
whereas the OpenAI system card (OpenAI 2024) only con-
sider limitations of what was being evaluated (e.g. classified
information or restricted data) rather than substantial lim-
itations of the procedures. Regarding auditor information,
15 of 24 reports include auditor expertise details, but rarely
their background (3 of 24), making an assessment of poten-
tial biases in the audit harder.

Reports rarely disclose information about evaluation
integrity, resources, review processes, and obsolescence
criteria. Only 4 of 24 reports detail organization and auditor
selection, conflicts of interest, or contractual arrangements
governing the evaluation process. Even in these cases, the
report tended to be about the contractual details of human
baselines that are part of the evaluation rather than the core
auditing team itself. Only 11 of 24 reports specify which
resources auditors had access to, including model access
level, computational resources, and time constraints. Simi-
larly, only eight reported on some form of review and ten
on feedback mechanisms (Meinke et al. 2025; METR 2024;
OpenAI 2024; UK AISI and US AISI 2024a). Seven report
whether they underwent any form of peer review or qual-
ity assurance process before publication (e.g. Gemini Team
et al. 2024b; UK AISI and US AISI 2024b). Five specified
an option for public feedback and corrections. Zero reports
explicitly present obsolescence criteria.

5 What guidance do current governance

frameworks offer?

Methodology: We analyzed key governance frameworks is-
sued by institutions that are considered influential regarding
technical evaluations for risks from state-of-the-art models.

We selected these frameworks based on jurisdiction, institu-
tional authority, and direct influence on model evaluations
(see Appendix D for details). This included official regula-
tions and policies (EU AI Act, US AI Action Plan), volun-
tary industry standards (NIST AI Risk Management Frame-
work), and policies from major AI developers. We scored
each framework on whether it either explicitly required or
recommended reporting of each feature in our audit card
template, as shown in Table 3.

Existing frameworks offer limited guidance on audit
reporting. We find existing frameworks consistently require
that models are evaluated (treated synonymously with be-
ing assessed or tested) but are not at the level of detail to
specifically require or even recommend evaluation reports
state the features of the evaluation we have listed. This is
especially true for these features: assumptions, limitations,
process integrity matters, resources and access given to au-
ditors involved. This is somewhat expected, as governance
frameworks for emerging technologies crystallize gradually
(Linkov et al. 2018), and the supplementary lower-level de-
tails around evaluations in the form of soft law are still
emerging.

6 Challenges with auditing according to

expert stakeholders

Methodology: To more thoroughly understand audit report-
ing and perceived gaps between current and best practices,
we interviewed 10 experts. We reached out to these experts
based on their expertise and familiarity across the evalua-
tion ecosystem. The 10 experts come from a diverse range
of private companies, non-profit organizations, and gov-
ernment bodies. Interviewees include: evaluation designers
(P1), evaluation developers (P3, P4, P5), evaluation report
writers (P1, P3, P5), evaluation-related policy researchers
(P6, P7), and those supporting evaluation delivery and stan-
dards development (P8, P9). Interview findings reveal in-
sights that extend beyond that documented in existing lit-
erature. To allow for candid discussions, we committed to
working with the level of anonymity that was comfortable
for experts. See Appendix E for methodological details, in-
terviewees’ backgrounds, interview questions and consent
forms.

The quality of audits depends greatly on the auditor.
Reporting on auditor details may become more critical
as the evaluation market grows. Currently, the quality and
trustworthiness of evaluators are primarily assessed infor-
mally (P1, P6, P7) through impressions of auditors’ work
and reputation. Many evaluation reports currently lack de-
tailed information about evaluator selection, training, and
reporting methods for various reasons, including time con-
straints or the belief that technical details about the evalua-
tion sufficiently indicate evaluation quality (P3). However,
because third-party auditors’ access to proprietary models is
voluntary (P1, P6), regulatory gaps and market failures must
be addressed to enable more reporting about auditor selec-
tion and engagement terms. Standardized evaluation report-
ing may become increasingly important as the market ex-
pands. Auditing regimes from other industries, such as fi-

Report

Average

Release date

Justif. Assum.

Limit. Who What How Access

Integrity Review Average

1.17

0.67

1.42

0.75

1.38

1.29

0.50

0.17

1.13

Mistral 7B
Apollo
Cohere Aya
UK AISI evals
Gemini paper
Llama 3 paper
Llama 3 card
METR o1
Claude 3 card
METR Claude 3.5
Gemma 2 paper
AISI Sonnet 3.5
OpenAI o1 card
Gemma 2 card
Gemini 1.5 paper
AISI o1
METR update
DeepSeek R1
o3 mini card
DeepSeek V3
METR o3 and o4-mini
Claude 4 card
Gemini 2.5 paper
IJTE agent report

10/23
01/24
02/24
05/24
06/24
07/24
07/24
09/24
10/24
10/24
10/24
11/24
12/24
12/24
12/24
12/24
01/25
01/25
01/25
02/25
04/25
05/25
06/25
07/25

0
2
2
1
1
1
1
1
1
1
1
2
1
1
1
2
1
0
1
1
2
2
1
1

0
1
1
0
1
1
1
0
1
0
0
1
1
0
1
1
1
0
1
0
1
1
1
1

0
2
2
1
1
2
1
1
1
2
1
2
1
1
2
2
2
0
1
1
2
2
2
2

0
0
2
0
1
2
1
1
1
1
0
1
1
0
2
1
0
0
1
0
1
1
1
0

1
2
2
1
1
1
1
1
1
1
2
2
1
1
1
2
1
1
1
1
2
2
2
2

1
2
1
1
1
2
1
1
1
1
1
1
1
1
2
1
1
1
1
1
2
2
2
2

0
0
0
0
1
0
0
1
0
0
0
1
1
0
1
1
0
0
1
0
2
1
1
1

0
0
1
0
1
0
0
0
0
0
0
0
0
0
1
0
0
0
0
0
0
0
1
0

0
2
1
2
1
1
1
1
1
1
1
1
1
1
2
1
2
0
1
1
1
1
2
1

0.94

0.22
1.22
1.33
0.67
1.00
1.11
0.78
0.78
0.78
0.78
0.67
1.22
0.89
0.56
1.44
1.22
0.89
0.22
0.89
0.56
1.44
1.33
1.44
1.11

Table 2: What contextual details do existing audit reports provide? We score reports as providing comprehensive (2),
minimal (1), or no information (0) for each component of an audit card. Table ordered by release date of the report.

nance, energy, and medicine, may offer guidance moving
forward (P9; see also Anderson-Samways (2024)).

Reporting about the evaluation timeline can help with
industry’s standardization efforts. The amount of time
spent on designing and executing an evaluation can have
a direct effect on the quality and thoroughness of the
evaluation. When audits begin and end, and the correspond-
ing versions of model access at each checkpoint, can of-
ten be in tension with commercial pressures in companies
to develop and deploy quickly (P1, P4, P6). Evaluation re-
sources, including time, are often difficult to measure in a
chaotic situation (P3). Standardization and guidance before-
hand around auditing timeframes may be greatly appreci-
ated by evaluators (P1, P4, P5, P6). In lieu of laws explicitly
specifying timeframes for different stages of evaluation, re-
porting the time taken by auditors will be crucial to facilitate
standardization and coordination.

Evaluation reports are currently used more by audi-
tors than policymakers. Currently, evaluation reports by
both internal and external evaluators assume a primarily
technical audience. Policymakers are constrained by time,
technical understanding, regulatory state of affairs, and of-
ten read them at a high level (P6, P9). Thus, it seems that
evaluation reports more directly inform the science of eval-
uations than policy, as they assist with reproducibility and
elicitation. In the future, it will likely be useful for govern-
ment authorities to check compliance with standards. Ex-
perts have also said that adapting features to a prioritization
for each user group would be valuable (P1, P5, P6, P8). This

may be the subject of future research.

7 Discussion and recommendations
There are currently no established standards on how to
report the context of audits. The lack of standards leads
to inconsistency in audit reporting practices. Certain contex-
tual features, such as reporting on the integrity of auditing
processes, are particularly neglected. Lacking transparency
around audit methodology and context impedes accountabil-
ity in the AI ecosystem, where trust in evaluations is essen-
tial for informed decision-making by regulators, users, and
the public.

Audit cards address AI evaluation reporting gaps to
aid methodological rigor and public transparency. Cur-
rent inconsistent reporting practices undermine evaluations’
governance role, creating trust gaps between developers, au-
ditors, regulators, and the public. By structuring the essen-
tial contextual information to be reported, audit cards en-
able meaningful interpretation of evaluation results. Coun-
tries vary in how they see evaluations—emphasizing sci-
entific rigor or compliance verification, public transparency
or government oversight. While this paper does not com-
ment on which regulatory approach is superior, it does take
the premise that evaluations are scientific exercises requiring
public transparency for effective governance.

Audit cards are one approach among several to
increase transparency between developers, users, and
other stakeholders. Audit cards are designed to offer a
structured checklist applicable to all types of assessment

Document

Regulations
Brazil
China
EU
Singapore
South Korea
USA
New York

Other norms
Bletchley
Int’l Report
Japan AISI
METR
NIST AI RMF
Paris
Seoul
UK AISI

Company policies
Anthropic
Google DeepMind
Meta
Microsoft
OpenAI
xAI

Principles

Justif. Assum.

Features
Limit. Who What How Access

Integrity Review

0
0
1
0
0
0
0

0
1
0
1
1
0
0
0

1
1
1
1
1
1

0
0
1
0
0
0
0

0
1
0
1
1
0
0
0

1
0
0
1
0
0

0
0
1
0
0
0
0

0
1
0
1
1
0
0
1

0
1
1
1
0
1

0
0
1
1
0
0
0

0
1
0
1
1
0
0
1

0
1
1
1
0
0

0
1
1
1
0
1
0

0
1
1
1
1
0
1
1

1
1
1
1
1
1

0
1
1
1
0
0
1

1
1
0
1
1
0
0
1

1
1
1
1
1
1

0
0
1
0
0
0
0

0
1
0
0
0
0
0
0

0
0
0
0
0
0

0
0
1
0
0
0
0

0
1
0
1
1
0
0
0

1
1
1
0
0
0

0
1
1
1
0
0
0

1
1
0
1
1
0
0
1

1
1
1
1
1
1

Table 3: What guidance do existing governance frameworks provide for reporting? We give binary scores of 1 (requires
or recommends explicit reporting of this feature) or 0 (may mention issue’s importance to the ecosystem but not specifically
require or recommend its disclosure or reporting). For company policies we score disclosure of it. Citations and details for the
specific documents are in Appendix D.

(see Appendix C), but should be viewed as an instrument
in a larger AI accountability toolkit. The context they offer
can be helpful to other mechanisms, including model and
system cards, datasheets, and benchmark details (Mitchell
et al. 2019; Gebru et al. 2021; Reuel et al. 2024b).

the accuracy of disclosed information. However, fraud is
not unique to AI. Other fields handle these challenges
through formal scrutiny mechanisms and occasional legal
action. Through explicit disclosure, audit cards can be a
first step toward a more accountable governance regime.

Limitations and concerns:

• Limited sample size and reporting details. To enable
consistent high-level analysis of the current ecosystem,
we used simple 2 or 3 point scoring methods. However,
this comes at the expense of granular details and nuance,
differentiating between reports only to a limited degree.
This is particularly pronounced for our analysis of gover-
nance frameworks, where we use binary scores. Further-
more, our analysis, while extensive (28 academic papers,
20 evaluation reports, and 21 governance frameworks), is
not exhaustive.

• Trade-offs between reporting quality and audit qual-
ity: Implementing thorough reporting through audit cards
requires additional time and effort from auditors who of-
ten already operate under significant resource constraints.
The additional burden of comprehensive reporting may be
challenging, particularly for smaller organizations or time-
sensitive evaluations.

• Verification challenges: Even with comprehensive re-
porting guidelines, there remain challenges in verifying

Key near-term challenges with AI audit reporting in-
clude providing rigorous and standardized guidance. In
the absence of external, authoritative standards for report-
ing, stakeholders across the AI ecosystem will struggle to
effectively compare and interpret audit results. The EU AI
Act (including its Code of Practice) and various contribu-
tions from AISIs and NIST, international consortia, labs, and
third-party evaluators have offered progress toward a shared
understanding of rigor. However, future initiatives may ben-
efit from a higher degree of specificity (e.g., templates) for
reporting on the principles and features highlighted in this
paper.

Standardized reporting frameworks are key for trust-
worthy AI audits. The path toward effective AI governance
requires both technical innovation and procedural standard-
ization. By establishing shared expectations for auditing
transparency through structured reporting mechanisms like
audit cards, policymakers can build a more accountable AI
governance landscape. Such frameworks ensure evaluations
are rigorous, not only in execution, but also in reporting.
Ultimately, this enables stakeholders to make informed de-

cisions based on transparent, comparable, and contextually
rich information that serves the public interest.

Acknowledgments
This research was supported by the ML Alignment & The-
ory Scholars (MATS) Program, which provided funding for
Leon Staufer and Mick Yang through research stipends. We
also thank MATS and our research managers Juan Gil and
Keivan Navaie for their organizational assistance and re-
search support.

We express our gratitude to Michael Aird, Lily Stelling,
as well as other members of the MATS cohort, participants
in the FAR Labs discussion group, and others for their valu-
able feedback and suggestions throughout the development
of this paper.

We are grateful

to all participants who contributed
through interviews. Their perspectives were instrumental in
developing the frameworks presented.

References
AI Safety Institute. 2024. Advanced AI Evaluations at
AISI: May Update. https://www.aisi.gov.uk/work/advanced-
ai-evaluations-may-update.
Ananny, M.; and Crawford, K. 2018. Seeing without know-
ing: Limitations of the transparency ideal and its application
to algorithmic accountability. new media & society, 20(3):
973–989.
Anderljung, M.; Smith, E. T.; O’Brien, J.; Soder, L.; Buck-
nall, B.; Bluemke, E.; Schuett, J.; Trager, R.; Strahm, L.; and
Chowdhury, R. 2023. Towards Publicly Accountable Fron-
tier LLMs: Building an External Scrutiny Ecosystem under
the ASPIRE Framework. arXiv:2311.14711.
AI-relevant Regulatory
Anderson-Samways, B. 2024.
Precedents: A Systematic Search across All Federal Agen-
cies. Institute for AI Policy and Strategy.
Anthropic. 2024. The Claude 3 Model Family: Opus, Son-
net, Haiku.
Anthropic. 2025a. Responsible Scaling Policy.
Anthropic. 2025b. System Card: Claude Opus 4 & Claude
Sonnet 4.
Apollo Research. 2024. We Need a Science of Evals.
Barnett, P.; and Thiergart, L. 2024a. Declare and Justify:
Explicit Assumptions in AI Evaluations Are Necessary for
Effective Regulation. arXiv:2411.12820.
Barnett, P.; and Thiergart, L. 2024b. What AI Evalua-
tions for Preventing Catastrophic Risks Can and Cannot Do.
arXiv:2412.08653.
Bengio, Y.; Mindermann, S.; Privitera, D.; Besiroglu, T.;
Bommasani, R.; Casper, S.; Choi, Y.; Goldfarb, D.; Heidari,
H.; Khalatbari, L.; et al. 2024. International Scientific Re-
port on the Safety of Advanced AI (Interim Report). arXiv
preprint arXiv:2412.05282.
Bianzino, N. M.; Delarue, M.-L.; Maher, S.; Koene, A.;
Kummer, K.; and Hassan-Szlamka, F. 2023. The Artificial
Intelligence (AI) Global Regulatory Landscape. Technical
report, EY.

Birhane, A.; Steed, R.; Ojewale, V.; Vecchione, B.; and Raji,
I. D. 2024. AI Auditing: The Broken Bus on the Road to AI
Accountability. arXiv:2401.14462.
Bommasani, R.; Klyman, K.; Longpre, S.; Xiong, B.;
Kapoor, S.; Maslej, N.; Narayanan, A.; and Liang, P. 2024.
Foundation model transparency reports. In Proceedings of
the AAAI/ACM Conference on AI, Ethics, and Society, vol-
ume 7, 181–195.
Boone, A. L.; Floros, I. V.; and Johnson, S. A. 2015. Redact-
ing Proprietary Information at the Initial Public Offering.
Social Science Research Network:2348184.
Brazilian Federal Senate. 2023. Bill No. 2338/2023: Pro-
vides for the use of Artificial Intelligence.
Bucknall, B. S.; and Trager, R. F. 2023. Structured Access
for Third-Party Research on Frontier AI Models: Investigat-
ing Researchers’ Model Access Requirements.
Burnell, R.; Schellaert, W.; Burden, J.; Ullman, T. D.;
Martinez-Plumed, F.; Tenenbaum, J. B.; Rutar, D.; Cheke,
L. G.; Sohl-Dickstein, J.; Mitchell, M.; Kiela, D.; Shana-
han, M.; Voorhees, E. M.; Cohn, A. G.; Leibo, J. Z.; and
Hernandez-Orallo, J. 2023. Rethink Reporting of Evalua-
tion Results in AI. Science, 380(6641): 136–138.
Casper, S.; Bailey, L.; Hunter, R.; Ezell, C.; Cabal´e, E.;
Gerovitch, M.; Slocum, S.; Wei, K.; Jurkovic, N.; Khan,
arXiv preprint
A.; et al. 2025. The AI Agent Index.
arXiv:2502.01635.
Casper, S.; Ezell, C.; Siegmann, C.; Kolt, N.; Curtis, T. L.;
Bucknall, B.; Haupt, A.; Wei, K.; Scheurer, J.; Hobbhahn,
M.; Sharkey, L.; Krishna, S.; Von Hagen, M.; Alberti, S.;
Chan, A.; Sun, Q.; Gerovitch, M.; Bau, D.; Tegmark, M.;
Krueger, D.; et al. 2024. Black-Box Access Is Insufficient
for Rigorous AI Audits. In Proceedings of the 2024 ACM
Conference on Fairness, Accountability, and Transparency,
FAccT ’24, 2254–2272. New York, NY, USA: Association
for Computing Machinery. ISBN 979-8-4007-0450-5.
Chan, A.; Ezell, C.; Kaufmann, M.; Wei, K.; Hammond, L.;
Bradley, H.; Bluemke, E.; Rajkumar, N.; Krueger, D.; Kolt,
N.; et al. 2024. Visibility into AI agents. In Proceedings of
the 2024 ACM Conference on Fairness, Accountability, and
Transparency, 958–973.
Chang, Y.; Wang, X.; Wang, J.; Wu, Y.; Yang, L.; Zhu,
K.; Chen, H.; Yi, X.; Wang, C.; Wang, Y.; Ye, W.;
Zhang, Y.; Chang, Y.; Yu, P. S.; Yang, Q.; and Xie, X.
2023. A Survey on Evaluation of Large Language Models.
arXiv:2307.03109.
Costanza-Chock, S.; Raji, I. D.; and Buolamwini, J. 2022.
Who Audits the Auditors? Recommendations from a Field
Scan of the Algorithmic Auditing Ecosystem. In Proceed-
ings of the 2022 ACM Conference on Fairness, Accountabil-
ity, and Transparency, FAccT ’22, 1571–1583. New York,
ISBN
NY, USA: Association for Computing Machinery.
978-1-4503-9352-2.
Creemers, R.; Webster, G.; and Helen Toner. 2022. Transla-
tion: Internet Information Service Algorithmic Recommen-
dation Management Provisions.
DeepSeek-AI; Guo, D.; Yang, D.; Zhang, H.; Song, J.;
Zhang, R.; Xu, R.; Zhu, Q.; Ma, S.; Wang, P.; Bi, X.; Zhang,

X.; Yu, X.; Wu, Y.; Wu, Z. F.; Gou, Z.; Shao, Z.; Li, Z.;
Gao, Z.; Liu, A.; et al. 2025. DeepSeek-R1: Incentivizing
Reasoning Capability in LLMs via Reinforcement Learning.
arXiv:2501.12948.
DeepSeek-AI; Liu, A.; Feng, B.; Xue, B.; Wang, B.; Wu,
B.; Lu, C.; Zhao, C.; Deng, C.; Zhang, C.; Ruan, C.; Dai,
D.; Guo, D.; Yang, D.; Chen, D.; Ji, D.; Li, E.; Lin, F.; Dai,
F.; Luo, F.; et al. 2024. DeepSeek-V3 Technical Report.
arXiv:2412.19437.
Dobbe, R.; Krendl Gilbert, T.; and Mintz, Y. 2021. Hard
Choices in Artificial Intelligence. Artificial Intelligence,
300: 103555.
Dow, P. A.; Vaughan, J. W.; Barocas, S.; Atalla, C.; Choulde-
chova, A.; and Wallach, H. 2024. Dimensions of Generative
AI Evaluation Design. arXiv:2411.12709.
Drafting Expert Group. 2025. Artificial Intelligence Law of
the People’s Republic of China.
Eriksson, M.; Purificato, E.; Noroozian, A.; Vinagre, J.;
Chaslot, G.; Gomez, E.; and Fernandez-Llorca, D. 2025.
Can We Trust AI Benchmarks? An Interdisciplinary Review
of Current Issues in AI Evaluation. arXiv:2502.06559.
EU AI Act. 2024. Regulation (EU) 2024/1689 of the
European Parliament and of
the Council of 13 June
2024 Laying down Harmonised Rules on Artificial Intelli-
gence and Amending Regulations (EC) No 300/2008, (EU)
No 167/2013, (EU) No 168/2013, (EU) 2018/858, (EU)
2018/1139 and (EU) 2019/2144 and Directives 2014/90/EU,
(EU) 2016/797 and (EU) 2020/1828 (Artificial Intelligence
Act) (Text with EEA Relevance).
EU monitor. ???? Legal Instruments.
European Commission. 2025. General-Purpose AI Code of
Practice.
European Union. ???? Types of Legislation.
Evans, O.; Leung, J.; Shevlane, T.; and Prunkl, C. 2023.
Who Should Develop Which AI Evaluations? Oxford Mar-
tin AI Governance Initiative. Accessed: [date of access].
Felzmann, H.; Fosch-Villaronga, E.; Lutz, C.; and Tam`o-
Larrieux, A. 2020. Towards transparency by design for ar-
tificial intelligence. Science and engineering ethics, 26(6):
3333–3361.
Gallifant, J.; Afshar, M.; Ameen, S.; Aphinyanaphongs, Y.;
Chen, S.; Cacciamani, G.; Demner-Fushman, D.; Dligach,
D.; Daneshjou, R.; Fernandes, C.; Hansen, L. H.; Landman,
A.; Lehmann, L.; McCoy, L. G.; Miller, T.; Moreno, A.;
Munch, N.; Restrepo, D.; Savova, G.; Umeton, R.; et al.
2025. The TRIPOD-LLM Reporting Guideline for Stud-
ies Using Large Language Models. Nature Medicine, 31(1):
60–69.
Gebru, T.; Morgenstern, J.; Vecchione, B.; Vaughan, J. W.;
Wallach, H.; Iii, H. D.; and Crawford, K. 2021. Datasheets
for Datasets. arXiv:1803.09010.
Gemini Team. 2024. Gemini 1.5: Unlocking Multimodal
Understanding across Millions of Tokens of Context.
Gemini Team; Anil, R.; Borgeaud, S.; Alayrac, J.-B.; Yu, J.;
Soricut, R.; Schalkwyk, J.; Dai, A. M.; Hauth, A.; Millican,
K.; Silver, D.; Johnson, M.; Antonoglou, I.; Schrittwieser, J.;

Glaese, A.; Chen, J.; Pitler, E.; Lillicrap, T.; Lazaridou, A.;
Firat, O.; et al. 2024a. Gemini: A Family of Highly Capable
Multimodal Models. arXiv:2312.11805.

Gemini Team; Georgiev, P.; Lei, V. I.; Burnell, R.; Bai, L.;
Gulati, A.; and et. al. 2024b. Gemini 1.5: Unlocking Multi-
modal Understanding across Millions of Tokens of Context.
arXiv:2403.05530.

Gemini Team; and Google. 2025. Gemini 2.5: Pushing
the Frontier with Advanced Reasoning, Multimodality, Long
Context, and Next Generation Agentic Capabilities.

Gemma Team; Riviere, M.; Pathak, S.; Sessa, P. G.; Hardin,
C.; Bhupatiraju, S.; Hussenot, L.; Mesnard, T.; Shahriari,
B.; Ram´e, A.; and Others. 2024. Gemma 2: Improving
Open Language Models at a Practical Size. Arxiv Preprint
Arxiv:2408.00118.

Google.
https://ai.google.dev/gemma/docs/core/model card 2.

2 Model

Gemma

????

Card.

Google. 2025. Frontier Safety Framework 2.0.

Grattafiori, A.; Dubey, A.; Jauhri, A.; Pandey, A.; Kadian,
A.; Al-Dahle, A.; Letman, A.; Mathur, A.; Schelten, A.;
Vaughan, A.; and Others. 2024. The Llama 3 Herd of Mod-
els. Arxiv Preprint Arxiv:2407.21783.

Gu, A. 2023. China Released New Ethics Rules Requiring
Company’s Internal EC.

Gursoy, F.; and Kakadiaris, I. A. 2022. System cards for
AI-based decision-making for public policy. arXiv preprint
arXiv:2203.04754.

Hardy, A.; Reuel, A.; Meimandi, K. J.; Soder, L.; Griffith,
A.; Asmar, D. M.; Koyejo, S.; Bernstein, M. S.; and Kochen-
derfer, M. J. 2024. More than Marketing? On the Infor-
mation Value of AI Benchmarks for Practitioners. arXiv
preprint arXiv:2412.05520.

Haresamudram, K.; Larsson, S.; and Heintz, F. 2023. Three
levels of AI transparency. Computer, 56(2): 93–100.

Hendrycks, D.; and Woodside, T. 2024. Devising ML Met-
rics.

Huang, S.; Toner, H.; Haluza, Z.; Creemers, R.; and Web-
ster, G. 2023. Translation: Measures for the Management of
Generative Artificial Intelligence Services (Draft for Com-
ment).

International Network of AISIs. 2025.
Testing Exercise: Agentic Testing Evaluation Report.

International Joint

Japan AI Safety Institute. 2024. Guide to Evaluation Per-
spectives. Technical report, Japan AI Safety Institute. Ver-
sion 1.00.

Jiang, A. Q.; Sablayrolles, A.; Mensch, A.; Bamford, C.;
Chaplot, D. S.; de las Casas, D.; Bressand, F.; Lengyel, G.;
Lample, G.; Saulnier, L.; Lavaud, L. R.; Lachaux, M.-A.;
Stock, P.; Scao, T. L.; Lavril, T.; Wang, T.; Lacroix, T.; and
Sayed, W. E. 2023. Mistral 7B. arXiv:2310.06825.

Joaquin, A. S.; Gipiˇskis, R.; Staufer, L.; and Gil, A. 2025.
Deprecating Benchmarks: Criteria and Framework. In ICML
Workshop on Technical AI Governance (TAIG).

in LLMs.

Khan, A.; Casper, S.; and Hadfield-Menell, D. 2025. Ran-
domness, Not Representation: The Unreliability of Eval-
arXiv preprint
uating Cultural Alignment
arXiv:2503.08688.
Knerr, P.; and D’Amelia, R. P. 2020.
Introduction to the
Ethics of Scientific Conflict of Interest (COI). Committee
on Ethics, American Chemical Society. Ethics Committee
Monograph.
Kolt, N.; Anderljung, M.; Barnhart, J.; Brass, A.; Esvelt, K.;
Hadfield, G. K.; Heim, L.; Rodriguez, M.; Sandbrink, J. B.;
and Woodside, T. 2024. Responsible reporting for frontier
AI development. In Proceedings of the AAAI/ACM Confer-
ence on AI, Ethics, and Society, volume 7, 768–783.
Krawiec, K. D. 2003. Cosmetic compliance and the failure
of negotiated governance. Wash. ULQ, 81: 487.
Li, Y.; and Goel, S. 2024. Making it possible for the auditing
of ai: A systematic review of ai audits and ai auditability.
Information Systems Frontiers, 1–31.
Liang, P.; Bommasani, R.; Lee, T.; Tsipras, D.; Soylu, D.;
Yasunaga, M.; Zhang, Y.; Narayanan, D.; Wu, Y.; Kumar,
A.; Newman, B.; Yuan, B.; Yan, B.; Zhang, C.; Cosgrove, C.;
Manning, C. D.; R´e, C.; Acosta-Navas, D.; Hudson, D. A.;
Zelikman, E.; et al. 2023. Holistic Evaluation of Language
Models. arXiv:2211.09110.
Linkov, I.; Trump, B. D.; Anklam, E.; Berube, D.; Bois-
seasu, P.; Cummings, C.; Ferson, S.; Florin, M.-V.; Gold-
stein, B.; Hristozov, D.; et al. 2018. Comparative, collabora-
tive, and integrative risk governance for emerging technolo-
gies. Environment Systems and Decisions, 38: 170–176.
Lu, T. 2006. Does opinion shopping impair auditor indepen-
dence and audit quality? Journal of Accounting Research,
44(3): 561–583.
Marquis, C.; Toffel, M. W.; and Zhou, Y. 2016. Scrutiny,
norms, and selective disclosure: A global study of green-
washing. Organization science, 27(2): 483–504.
Maslej, N.; Fattorini, L.; Perrault, R.; Parli, V.; Reuel, A.;
Brynjolfsson, E.; Etchemendy, J.; Ligett, K.; Lyons, T.;
Manyika, J.; Niebles, J. C.; Shoham, Y.; Wald, R.; and
Clark, J. 2024. Artificial Intelligence Index Report 2024.
arXiv:2405.19522.
Meinke, A.; Schoen, B.; Scheurer, J.; Balesni, M.; Shah, R.;
and Hobbhahn, M. 2025. Frontier Models Are Capable of
In-context Scheming.
Meta. 2025. Frontier AI Framework.
meta-llama. 2024.
https://github.com/meta-llama/llama3/blob/a0940f9cf7
065d45bb6675660f80d305c041a754/MODEL CARD.md.
METR. ????a. Frontier AI Safety Policies.
METR. ????b. Task Development Guide.
METR. 2024. Details about METR’s Preliminary Eval-
uation of Claude 3.5 Sonnet | METR’s Autonomy Eval-
uation Resources.
https://metr.github.io/autonomy-evals-
guide/claude-3-5-sonnet-report/.
Details
METR.
of
liminary

about METR’s
OpenAI

Llama 3 MODEL CARD.md.

Pre-
O1-Preview.

Evaluation

2024.

2025.

Details

of OpenAI’s O3

about METR’s Prelimi-
and O4-Mini.

An Update on Our Preliminary Eval-
and O1 - METR.

https://metr.github.io/autonomy-evals-guide/openai-o1-
preview-report/.
METR. 2024. Key Components of an RSP.
METR. 2024. Portable Evaluation Tasks via the METR Task
Standard. Accessed: 2025-03-14.
METR.
nary Evaluation
https://metr.github.io/autonomy-evals-guide/openai-o3-
report/.
METR. 2025.
uations of Claude 3.5 Sonnet
https://metr.org/blog/2025-01-31-update-sonnet-o1-evals/.
Microsoft. 2025. Frontier Governance Framework.
Mitchell, M.; Wu, S.; Zaldivar, A.; Barnes, P.; Vasserman,
L.; Hutchinson, B.; Spitzer, E.; Raji, I. D.; and Gebru, T.
2019. Model Cards for Model Reporting. In Proceedings
of the Conference on Fairness, Accountability, and Trans-
parency, FAT* ’19, 220–229. New York, NY, USA: Associ-
ation for Computing Machinery. ISBN 978-1-4503-6125-5.
M¨okander, J. 2023. Auditing of AI: Legal, ethical and tech-
nical approaches. Digital Society, 2(3): 49.
M¨okander, J.; Schuett, J.; Kirk, H. R.; and Floridi, L. 2024.
Auditing Large Language Models: A Three-Layered Ap-
proach. AI and Ethics, 4(4): 1085–1115.
Mukobi, G. 2024. Reasons to Doubt the Impact of AI Risk
Evaluations. arXiv:2408.02565.
National Assembly of the Republic of Korea. 2024. Ba-
sic Act on the Development of Artificial Intelligence and
Creation of a Trust Base. Technical Report 2206772, Na-
tional Assembly of the Republic of Korea, 1 Uisadang-
daero, Yeongdeungpo-gu, Seoul, 07233, Republic of Korea.
National Institute of Standards and Technology. 2024. AI
Risk Management Framework. Technical Report NIST AI
600-1, U.S. Department of Commerce.
New York State. 2025. Responsible AI Safety and Education
Act (RAISE Act). Assembly Bill A6453A.
Ojewale, V.; Steed, R.; Vecchione, B.; Birhane, A.; and
Raji, I. D. 2024. Towards AI accountability infrastructure:
Gaps and opportunities in AI audit tooling. arXiv preprint
arXiv:2402.17861.
OpenAI. 2024. OpenAI O1 System Card.
OpenAI. 2025a. OpenAI O3-Mini System Card.
OpenAI. 2025b. Preparedness Framework.
Pushkarna, M.; Zaldivar, A.; and Kjartansson, O. 2022. Data
cards: Purposeful and transparent dataset documentation for
responsible ai. In Proceedings of the 2022 ACM Conference
on Fairness, Accountability, and Transparency, 1776–1826.
Raji, I. D.; Smart, A.; White, R. N.; Mitchell, M.; Gebru, T.;
Hutchinson, B.; Smith-Loud, J.; Theron, D.; and Barnes, P.
2020. Closing the AI Accountability Gap: Defining an End-
to-End Framework for Internal Algorithmic Auditing.
In
Proceedings of the 2020 Conference on Fairness, Account-
ability, and Transparency, 33–44. Barcelona Spain: ACM.
ISBN 978-1-4503-6936-7.

Fadaee, M.; Kreutzer, J.; and Hooker, S. 2024. Aya Model:
An Instruction Finetuned Open-Access Multilingual Lan-
guage Model. arXiv:2402.07827.
Wahle, J. P.; Ruas, T.; Mohammad, S. M.; Meuschke, N.;
and Gipp, B. 2023. Ai usage cards: Responsibly reporting
ai-generated content. In 2023 ACM/IEEE Joint Conference
on Digital Libraries (JCDL), 282–284. IEEE, IEEE.
Wallach, H.; Desai, M.; Cooper, A. F.; Wang, A.; Atalla, C.;
Barocas, S.; Blodgett, S. L.; Chouldechova, A.; Corvi, E.;
Dow, P. A.; et al. 2025. Position: Evaluating Generative AI
Systems is a Social Science Measurement Challenge. arXiv
preprint arXiv:2502.00561.
Weidinger, L.; Raji, I. D.; Wallach, H.; Mitchell, M.; Wang,
A.; Salaudeen, O.; Bommasani, R.; Ganguli, D.; Koyejo, S.;
and Isaac, W. 2025. Toward an Evaluation Science for Gen-
erative AI Systems. arXiv:2503.05336.
Winecoff, A. A.; and Bogen, M. 2024.
Improving gover-
nance outcomes through AI documentation: Bridging theory
and practice. arXiv preprint arXiv:2409.08960.
xAI. 2025. xAI Risk Management Framework (2.10.2025
Draft).
Zhan, J.; Wang, L.; Gao, W.; Li, H.; Wang, C.; Huang, Y.;
Li, Y.; Yang, Z.; Kang, G.; Luo, C.; Ye, H.; Dai, S.; and
Zhang, Z. 2024. Evaluatology: The Science and Engineering
of Evaluation. BenchCouncil Transactions on Benchmarks,
Standards and Evaluations, 4(1): 100162.
´Elys´ee Palace. 2025. Statement on Inclusive and Sustainable
Artificial Intelligence for People and the Planet. Paris AI
Action Summit.

Raji, I. D.; Xu, P.; Honigsberg, C.; and Ho, D. 2022. Out-
sider oversight: Designing a third party audit ecosystem for
ai governance. In Proceedings of the 2022 AAAI/ACM Con-
ference on AI, Ethics, and Society, 557–571.
Reuel, A.; Bucknall, B.; Casper, S.; Fist, T.; Soder, L.;
Aarne, O.; Hammond, L.; Ibrahim, L.; Chan, A.; Wills, P.;
et al. 2024a. Open problems in technical ai governance.
arXiv preprint arXiv:2407.14981.
Reuel, A.; Hardy, A.; Smith, C.; Lamparth, M.; Hardy, M.;
and Kochenderfer, M. J. 2024b. BetterBench: Assessing
AI Benchmarks, Uncovering Issues, and Establishing Best
Practices. arXiv:2411.12990.
Schaeffer, R.; Miranda, B.; and Koyejo, S. 2023. Are emer-
gent abilities of large language models a mirage? Advances
in Neural Information Processing Systems, 36: 55565–
55581.
Selbst, A. D.; Boyd, D.; Friedler, S. A.; Venkatasubrama-
nian, S.; and Vertesi, J. 2019. Fairness and Abstraction in
Sociotechnical Systems. In Proceedings of the Conference
on Fairness, Accountability, and Transparency, FAT* ’19,
59–68. New York, NY, USA: Association for Computing
Machinery. ISBN 978-1-4503-6125-5.
Sharkey, L.; N´ı Ghuidhir, C.; Braun, D.; Scheurer, J.;
Balesni, M.; Bushnaq, L.; Stix, C.; and Hobbhahn, M. 2024.
A Causal Framework for AI Regulation and Auditing.
Shevlane, T.; Farquhar, S.; Garfinkel, B.; Phuong, M.; Whit-
tlestone, J.; Leung, J.; Kokotajlo, D.; Marchal, N.; An-
derljung, M.; Kolt, N.; Ho, L.; Siddarth, D.; Avin, S.;
Hawkins, W.; Kim, B.; Gabriel, I.; Bolina, V.; Clark, J.; Ben-
gio, Y.; Christiano, P.; et al. 2023. Model Evaluation for
Extreme Risks. arXiv:2305.15324.
Singapore. 2024. Model AI Governance Framework for
Generative AI.
Stanford HAI staff. 2024. Global AI Power Rankings: Stan-
ford HAI Tool Ranks 36 Countries in AI.
State Administration for Market Regulation; and Standard-
ization Administration of China. 2025. Security Specifica-
tion for Generative Artificial Intelligence Pre-training and
Fine-tuning Data.
The White House. 2025. America’s AI Action Plan.
UK AI Safety Institute. 2024. AI Safety Institute Approach
to Evaluations. Technical report, UK Government.
UK AI Safety Institute. 2025. International AI Safety Re-
port. Technical report, UK Government.
UK AISI; and US AISI. 2024a. Pre-Deployment Evaluation
of Anthropic’s Upgraded Claude 3.5 Sonnet.
UK AISI; and US AISI. 2024b. Pre-Deployment Evaluation
of OpenAI’s O1 Model.
UK Government. 2023. The Bletchley Declaration by Coun-
tries Attending the AI Safety Summit, 1-2 November 2023.
UK Government. 2024. Seoul Declaration for Safe, Innova-
tive and Inclusive AI. AI Seoul Summit, 21-22 May 2024.
¨Ust¨un, A.; Aryabumi, V.; Yong, Z.-X.; Ko, W.-Y.; D’souza,
D.; Onilude, G.; Bhandari, N.; Singh, S.; Ooi, H.-L.; Kayid,
A.; Vargus, F.; Blunsom, P.; Longpre, S.; Muennighoff, N.;

Appendix A Disambiguating auditing and

the evaluations process

AI audits, for the purpose of our analysis, refer to formal-
ized evaluation processes of AI models or systems. By for-
malized, we mean that it is performed systematically and by
an organization, i.e., not just being performed ad hoc by indi-
viduals. This kind of evaluation is a model audit, as opposed
to a governance audit or an application audit (M¨okander
et al. 2024).

The evaluation is the underlying assessment run on the
model during the audit. We account for the fact that evalu-
ations can occur internally or externally, and pre- or post-
deployment. Evaluations can assess capabilities, propensi-
ties, or risks. Evaluations can be in many forms, such as
benchmarks, red-teaming, human uplift studies, and user
studies. Our approach considers all these variants, as the
contextual features we have identified are relevant to all. It is
possible, that in some of these contexts certain features will
be more important and should therefore be reported in more
detail. We explore the importance of certain features further
in Section 7 and Appendix C.

We conceptualize the evaluation process as comprising
three main stages: (1) designing the underlying evaluation
methodology to achieve its aims (this could be a benchmark,
an evaluation suite, or a red-teaming exercise); (2) execut-
ing the evaluation and getting results; (3) publishing these
results in some form. Our focus is to elaborate on stage (3),
that is, what is to be included in these evaluation reports.

When speaking of evaluation reports, we refer to inter-
nal or external documents including evaluation results (e.g.,
a model’s results on a benchmark). Examples of evaluation
reports include: (OpenAI 2024; Meinke et al. 2025) as well
as private evaluation reports produced by third-parties for
AI companies and internal reports created by AI companies
themselves.

Appendix B Literature review

Methodology Details

We reviewed past work on “AI auditing”, “AI evaluations”,
“best practices”, “science of evaluations”, “evaluation con-
text” and “reporting”. We then assessed each paper for rele-
vance based off the titles. This only yielded eight papers. We
thus expanded to adjacent fields such as transparency and
AI auditing, technical evaluation design, and sociotechni-
cal approaches. These fields integrate technical performance
metrics with societal assessments and considerations of how
technical performance interacts with real-world social, cul-
tural, and institutional factors.

We scored recommendations within each paper as ma-
jor arguments (2), minor arguments (1), and no mention
(0). Scoring of (2) represents that the paper actively dis-
cussed and/or advocates for a feature, rather than mention-
ing the feature’s importance in passing (1). We chose our
three-point scale to balance reliability and granularity. For
all three annotations (papers, reports, and regulations), we
deliberated on the appropriate scoring system to ensure it is
objective, whilst not giving a false sense of detail.

Through four iterations, we refined which aspects were
most salient, focusing particularly on aspects that were ac-
tionable for auditors. Our methodology included: (1) two
annotators discussing discrepancies before establishing the
scoring system, (2) iterating on granularity. We found fine-
grained scoring unreliable at higher levels, opting instead for
our three-tiered system, and (3) developing detailed scoring
rubrics with concrete examples for each category.

Finally, we categorized and prioritized these aspects based
on input from experts. The mapping of aspects to features is
shown in Appendix B. The final audit card is depicted in
Figure 1 and Appendix C.

The guidelines for annotation of audit reports in Section 4

were as follows:

Focus is how well the features are reported not how
well they are argued/performed.
(0) no information / not mentioned.
(1) some (even minimal)
information. Example:
“based on conversations with global experts. [...] ex-
pert consultants” regarding expertise for biological
evaluations in Claude 3 model card (Anthropic 2024,
25).
(2) rich information, meaning you don’t have any im-
portant open questions after reading. Example: “red
team consists of experts in cybersecurity, [...], in ad-
dition to multilingual content specialists with back-
grounds in integrity issues for specific geographic
markets” regarding the expertise feature in Llama 3
research paper (Grattafiori et al. 2024, 48).
This granularity is commensurate with our aim: show
from a bird’s-eye view that current aspects of audit cards
are inconsistently reported on, not provide a definitive as-
sessment of individual audit reports. We find that awarding
one point for a minimal amount of information is not an is-
sue, as we want to be charitable in our assessment of reports
while still illustrating a frequent lack of thorough reporting.

List of papers
1. Towards Publicly Accountable Frontier LLMs (An-

derljung et al. 2023)

2. Science of Evals (Apollo Research 2024)
3. Declare and Justify: Explicit assumptions in AI evalua-
tions are necessary for effective regulation (Barnett and
Thiergart 2024a)

4. What AI evaluations for preventing catastrophic risks can

and cannot do (Barnett and Thiergart 2024b)

5. AI auditing: The Broken Bus on the Road to AI Account-

ability (Birhane et al. 2024)

6. Structured Access for Third-Party Research (Bucknall

and Trager 2023)

7. Rethink reporting of evaluation results in AI (Burnell

et al. 2023)

8. Black-Box Access is Insufficient for Rigorous AI Audits

(Casper et al. 2024)

9. A Survey on Evaluation of Large Language Models

(Chang et al. 2023)

10. Who Audits the Auditors? Recommendations from
a field scan of the algorithmic auditing ecosystem
(Costanza-Chock, Raji, and Buolamwini 2022)

9. What human input was used / who were they → How is

it evaluated

10. Peer review process / QA testing → Review and commu-

11. Hard

choices

in

artificial

intelligence

(Dobbe,

nication

Krendl Gilbert, and Mintz 2021)

11. How does capability or concept translate to benchmark

12. Dimensions of Generative AI Evaluation Design (Dow

task → How is it evaluated

et al. 2024)

13. Can We Trust AI Benchmarks? (Eriksson et al. 2025)
14. The TRIPOD-LLM Reporting Guideline for Studies Us-
ing Large Language Models (Gallifant et al. 2025)

15. Datasheets for Datasets (Gebru et al. 2021)
16. Devising ML Metrics (Hendrycks and Woodside 2024)
17. Responsible Reporting for Frontier AI Development

(Kolt et al. 2024)

18. Holistic Evaluation of Language Models (Liang et al.

2023)

19. Task Development Guide (METR b)
20. Auditing Large Language Models: A Three-Layered Ap-

proach (M¨okander et al. 2024)

21. Reasons to Doubt the Impact of AI Risk Evaluations

(Mukobi 2024)

22. Towards AI Accountability Infrastructure (Ojewale et al.

2024)

23. Closing the AI Accountability Gap: Defining an End-to-
End Framework for Internal Algorithmic Auditing (Raji
et al. 2020)

24. BetterBench (Reuel et al. 2024b)
25. Fairness and Abstraction in Sociotechnical Systems

(Selbst et al. 2019)

26. Model evaluation for extreme risks (Shevlane et al. 2023)
27. Toward an evaluation science for generative AI systems

(Weidinger et al. 2025)

28. Evaluatology: The Science and Engineering of Evalua-

tion (Zhan et al. 2024)

Mapping of initial aspects
Our initial literature review yielded 24 aspects listed below
that were mapped (→ ) to the principles and features:
1. Level of access auditors had → Access and Resources
2. How did they work with the model developers → In-

tegrity

3. Were they trained by the developers to evaluate the model

→ Who are the auditors

4. How much compute given to auditors, which manufac-

turers/chip model → Access and Resources

5. Expertise / background of people involved → Who are

the auditors

6. What was their initial goal for the evaluation → What is

evaluated

7. What were their documentation requirements → Review

and communication

8. What was the contract structure / How were they

paid/rewarded → Integrity

12. Involvement of domain experts during design → Who are

the auditors

13. Feedback channel (openness + how to contact) → Re-

view and communication

14. How should scores be interpreted or used → How is it

evaluated

15. Assumptions of normative properties are documented →

Assumptions

16. Non-normative assumptions justified → Assumptions
17. Evals as a process should consider eval’s limitations (not

that evals are limited) → Limitations

18. Interdisciplinary teams / including multiple perspectives

→ Who are the auditors

19. What is the technical goal of the model being evaluated

→ What is evaluated

20. What are the principles behind the development of the

model → What is evaluated

21. Consider context in which the AI system will be used
(e.g. value hierarchies, diverse populations) → Assump-
tions

22. Justification of evaluation methods used / using qualita-

tive evaluations as well → Justification

23. Timely, continuous evals → What is evaluated
24. Interpretable, easy to read, accessible to a wide audience

→ Review and communication

Appendix C Audit cards

Details and justifications of features
This section provides an overview of audit card features, in-
cluding a concise summary of what to report and why this
contextual information matters. A detailed list of aspects for
each feature can be found in the checklist in Appendix C.

Who are the auditors?
Summary: Documents auditor qualifications through do-
main expertise, experience, technical familiarity, formal cre-
dentials, stakeholder perspectives, and social positionality.

Why it matters: Transparency about qualifications es-
tablishes credibility while revealing potential biases. Ex-
pertise levels directly affect the ability to assess specific
systems, while diverse backgrounds help identify evalua-
tion blind spots. Without this information, readers cannot
judge whether auditors possessed the necessary skills to
thoroughly evaluate the system or what perspectives might
be underrepresented in the analysis.

Relevance across contexts: Basic expertise documenta-
tion is essential for all evaluation types. Red-teaming specif-
ically requires specialized adversarial thinking skills and se-
curity expertise. In user studies, auditor social positional-
ity becomes particularly important as it may influence how
human-AI interactions are interpreted.

Paper

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24

2 0 0 2 2 2 2 2 2
Anderljung et al. 2023
0 0 0 0 0 2 0 0 0
Apollo Research 2024
0 0 0 0 1 0 0 0 0
Barnett and Thiergart 2024a
Barnett and Thiergart 2024b
2 2 0 1 0 0 0 0 0
1 2 0 0 1 2 0 0 0
Birhane et al. 2024
2 2 0 2 0 2 2 0 0
Bucknall and Trager 2023
0 0 0 0 0 1 2 0 0
Burnell et al. 2023
2 0 1 0 0 0 0 0 0
Casper et al. 2024
Chang et al. 2023
0 0 0 0 1 0 0 0 2
Costanza-Chock, Raji, and Buolamwini 2022 2 1 0 0 2 1 0 1 0
0 0 0 0 0 0 0 0 0
Dobbe, Krendl Gilbert, and Mintz 2021
Dow et al. 2024
0 0 1 0 1 2 0 0 2
0 1 0 0 1 2 0 0 1
Eriksson et al. 2025
0 0 0 1 2 2 2 2 1
Gallifant et al. 2025
2 1 1 0 1 1 2 2 2
Gebru et al. 2021
0 0 0 0 0 0 0 0 1
Hendrycks and Woodside 2024
Kolt et al. 2024
0 2 0 0 2 0 2 0 0
0 0 0 0 0 0 0 0 0
Liang et al. 2023
0 0 0 0 2 2 2 0 1
METR b
M¨okander et al. 2024
2 2 0 0 1 2 2 0 0
2 2 2 2 0 2 0 2 0
Mukobi 2024
2 1 1 0 1 1 1 0 1
Ojewale et al. 2024
1 0 0 0 0 2 0 0 2
Raji et al. 2020
0 0 0 0 2 0 2 0 0
Reuel et al. 2024b
0 0 0 0 0 0 0 0 2
Selbst et al. 2019
2 2 0 0 2 2 0 0 0
Shevlane et al. 2023
Weidinger et al. 2025
0 0 0 0 0 2 1 0 0
0 0 0 0 1 2 2 0 0
Zhan et al. 2024

2
0
0
0
0
0
1
0
0
0
0
0
0
0
1
1
0
0
2
0
0
1
0
2
0
0
0
0

2
2
0
2
0
0
2
0
0
0
2
1
2
2
0
2
0
0
2
1
2
1
2
2
2
2
2
2

2
0
1
0
2
0
0
0
2
1
0
1
1
1
1
0
0
0
2
1
0
1
1
2
1
0
0
0

0
0
0
0
0
2
0
0
0
0
0
0
0
0
2
0
0
0
2
0
0
0
0
2
0
0
0
0

2
0
0
0
0
0
2
0
0
0
2
0
1
2
2
0
0
0
0
0
1
0
0
2
2
0
2
2

0
0
2
0
2
0
2
0
2
0
2
0
2
1
2
0
0
0
0
0
0
0
2
2
2
0
0
2

0
0
0
2
0
0
2
0
0
0
0
0
2
1
2
0
0
0
0
0
0
0
0
0
0
1
0
2

2
0
0
2
2
2
0
0
0
0
2
0
1
2
2
1
0
0
0
2
0
0
2
2
2
2
2
2

2
0
0
0
2
0
0
0
0
2
2
1
0
0
2
0
0
0
0
1
0
2
2
0
2
0
0
0

0
0
0
0
0
0
1
0
0
0
1
0
2
1
0
0
1
2
0
2
1
1
2
0
0
0
2
0

0
0
0
0
0
0
0
0
0
0
2
0
2
0
0
0
0
0
0
0
0
0
2
0
2
0
1
0

2
2
1
2
2
2
2
2
1
2
2
2
2
2
1
0
1
2
0
2
2
2
2
1
2
2
2
2

1
2
2
1
2
0
2
1
0
2
2
0
2
2
1
0
1
1
0
0
0
1
0
0
0
0
2
2

2
0
0
2
2
2
0
0
0
0
1
2
0
2
0
0
1
0
0
2
2
0
0
2
0
2
1
0

2
0
0
0
2
2
1
1
0
2
2
0
0
2
2
1
2
0
0
2
1
1
1
2
0
2
0
0

Table 4: Annotations for all 28 papers across the 24 initial contextual aspects (see Appendix B). We score each paper’s discus-
sion of these as 2 (major argument), 1 (minor argument), and 0 (no mention).

What is evaluated?
Summary: Defines evaluation scope, goals, and approach
by specifying system version, components, scaffolding used,
threat models addressed, and whether capabilities or propen-
sities were evaluated. Includes continuous monitoring plans
and obsolescence criteria.

Why it matters: Clear boundaries prevent misinterpreta-
tion of results. Understanding threats, contexts, and capabil-
ity vs. propensity assessment helps readers gauge relevance
to their specific concerns. Without specific scope informa-
tion, readers might incorrectly assume the evaluation covers
more than it does, while obsolescence criteria help prevent
outdated evaluations from being applied to newer system
versions.

Relevance across contexts: Evaluation scope and goal
specification are critical across all evaluation types. Bench-
marks particularly require clear documentation of obsoles-
cence criteria as AI capabilities rapidly evolve. Safety as-
sessments benefit from explicit threat models tailored to de-
ployment context. Human-centered evaluations need clear
articulation of intended user groups and use cases, while de-
ployed systems require specified intervals and conditions for
re-evaluation.

How is it evaluated?
Summary: Describes methodology, implementation de-
tails, and result interpretation guidance. Explains connec-
tions between evaluation methods and capabilities, justifies

capability-to-goal translations, and outlines finding limita-
tions. Reporting on this feature can be very extensive, as the
specific details for reporting depend on the exact evaluation
procedure used. We refer to existing literature on best prac-
tices for reporting on evaluation procedures, such as Reuel
et al. (2024b); Apollo Research (2024).

Why it matters: Methodology directly impacts result
validity and reliability. Understanding how capabilities be-
come measurable criteria and how scores translate to real-
world performance prevents misapplication of evaluation
outcomes. Without methodological
transparency, readers
cannot assess whether the evaluation approach actually mea-
sures what it claims to measure or understand the confidence
level appropriate for various findings.

Relevance across contexts: A description of methodol-
ogy is essential for all evaluation types. Benchmarks specif-
ically require detailed score interpretation guidance to pre-
vent misapplication of numerical results. Propensity evalua-
tions need robust justification for capability-to-goal transla-
tions since they often use proxy measurements. Novel sys-
tem types need clearer justification for how evaluation ap-
proaches measure intended capabilities.

Access and resources
Summary: Details

level
pro-
(black/gray/white-box, with/without
vided documentation, and available computational, time,
and financial resources.

system access
safeguards),

auditor

Why it matters: Resource constraints and access lim-
itations impact evaluation thoroughness and depth. Lim-
ited system access or insufficient resources may prevent
auditors from discovering certain vulnerabilities or testing
edge cases. Transparency about these constraints helps read-
ers understand which areas received less scrutiny and what
types of issues the evaluation might have missed due to prac-
tical limitations.

Relevance across contexts: Basic access level informa-
tion is relevant to all evaluations. Red-teaming findings can
differ dramatically between black-box and white-box condi-
tions. Large-scale benchmarks particularly require computa-
tional resource documentation.

Integrity
Summary: Addresses auditor selection process, poten-
tial “opinion shopping,” conflicts of interest, compensation
structures, contract terms, and NDAs. Documents measures
ensuring diverse perspectives.

Why it matters: Selection processes and incentive struc-
tures reveal potential influences on outcomes. Auditors with
financial ties to the evaluated organization may face pressure
to produce favorable results, while restrictive NDAs might
limit disclosure of critical findings. Transparent disclosure
of relationships and contractual limitations builds trust in
findings and allows readers to identify potential sources of
bias.

Relevance across contexts: Integrity documentation and
conflict of interest disclosure is universally important across
all evaluation contexts. Selection process transparency be-
for high-stakes evaluations where find-
comes critical
ings may significantly impact deployment decisions. Non-
disclosure agreement details matter most when evaluations
involve proprietary information that might limit the disclo-
sure of certain findings. Disclosure of prior relationships
between auditors and developers matters more for external
evaluations to establish credibility and independence.

Review and communication
Summary: Outlines evaluation review process, feedback
channels, executive summary quality, key term definitions,
and result distribution. Focuses on unambiguous key find-
ings and consistent terminology.

Why it matters: Robust review strengthens findings’ re-
liability by catching errors and biases. Clear feedback chan-
nels enable continuous improvement when new information
emerges or vulnerabilities are discovered after publication.
Well-defined terminology ensures consistent understanding
across different stakeholders, preventing miscommunication
about technical concepts and evaluation outcomes that could
lead to inappropriate system deployment decisions.

Relevance across contexts: Robust review processes are
essential across all evaluation types to ensure reliability and
catch potential errors or biases. Interdisciplinary evalua-
tions require clear definitions of domain-specific terminol-
ogy. Security-sensitive applications need explicit documen-
tation of which findings are shared with which audiences.

Checklist for audit card
This checklist provides a framework for documenting con-
textual information about AI system audits. Questions are

prioritized with the most important appearing first in each
section, though not all questions in a section will be relevant
to every evaluation. The checklist serves as a flexible guide
rather than a rigid requirement. More comprehensive infor-
mation generally enhances transparency. Through use of the
audit card checklist, it is easier to document evaluation con-
texts, limitations, and strengths to facilitate informed discus-
sions about AI system capabilities and risks.
□ Who are the auditors

□ Expertise:

• What specific domain expertise (e.g. cybersecurity
knowledge) do the auditors possess that is relevant to
this evaluation?

• What relevant experience do the auditors have in eval-

uating similar systems?

• What is the auditors’ familiarity with the specific tech-

nology being evaluated?

• Do the auditors hold official accreditations or certifi-

cations relevant to this evaluation?

• Have the auditors undergone any training specific to

this evaluation (internal or external)?

□ Background:

• What stakeholder perspectives do the auditors repre-

sent or have experience with?

• What is the social positionality of the auditors (ag-
gregated demographic information, cultural back-
ground)?
□ What is evaluated

□ Scope:

• Which specific version or iteration of the system is be-

ing evaluated?

• What specific components of the system are included

in the evaluation?

• What aspects of the system were explicitly excluded

from the evaluation scope?

• Does the evaluation cover the full system or only spe-

cific functionalities?

• What scaffolding (e.g. chain-of-thought prompting,
few-shot demonstrations) or additional tools (e.g. web
or command line access) were used during the evalua-
tion?
□ Goal:

• What threat models or risk scenarios is the evaluation

addressing?

• What specific harms or misuses is the evaluation at-

tempting to identify?

• What are the specific contexts (e.g. user groups and
use cases) in which the AI system will be deployed?
• What are the performance expectations in the intended

contexts?

□ Type of evaluation:

• Is the evaluation assessing capabilities, propensities,

or risks?

• What form of evaluation methodology is being used
(benchmark, red-teaming, human uplift studies, or
user studies, etc.)?

□ Continuous evaluations:

• Will the system be subject to ongoing monitoring after

this evaluation?

• At what intervals will follow-up evaluations occur?

□ Obsolescence criteria:

• What changes (system updates, deployment context,
discoveries about similar systems, or technological ad-
vances) would render this evaluation obsolete?

• How long is this evaluation expected to remain rele-

vant without updates?

□ How is it evaluated

□ Description of evaluation setup:

• What general evaluation methodology was employed?
• What were the key components of the evaluation de-

sign?

• What evaluation framework or established protocol

was followed (if applicable)?

□ Justification of capability-to-goal translation:

• How does the evaluation approach align with the ca-

pabilities or risks being assessed?

• How do the evaluation procedures relate to the sys-

tem’s intended use contexts?

• What is the rationale for how the chosen methods mea-

sure the targeted capabilities?

□ Interpretation of scores:

• How should the evaluation results be interpreted?
• What limitations should be considered when interpret-

ing the findings?

• What do different performance levels indicate about

the system?
□ Access and resources
□ Level of access:

• Did the auditor have black-box, gray-box, or white-

box access?

• What specific system documentation was provided to
auditors, including access to system code, architec-
ture, design documents, training data, or previous eval-
uation results?

• Were any aspects of the system explicitly restricted

from auditor access?
□ Resources available:

• What computational resources were allocated to the

evaluation?

• How much time was allocated for the full evaluation

cycle?

• Was the evaluation timeline sufficient for comprehen-

sive testing?

• How many auditors were involved and what was their

time commitment?

• What specialized tools or software were available to

the auditors?

• Were resources sufficient to conduct all planned eval-

uation activities?

• What resource constraints limited the scope or depth

of the evaluation?

□ Integrity

□ Selection process:

• How were auditors identified and recruited for this

evaluation?

• What criteria were used to select auditors?
• What measures were taken to ensure diversity of per-

spectives among auditors?

• Was there an open call or nomination process for au-

ditors?

• Were independent third parties involved in the selec-

tion process?
□ Conflicts of interest:

• What relationships exist between auditors and the or-

ganization being evaluated?

• Have auditors previously received compensation from

the evaluated organization?

• Do auditors have financial interests or competing in-

terests related to the evaluated system?

• What measures were taken to mitigate potential con-

flicts of interest?

• Were potential conflicts of interest publicly disclosed?

□ Compensation and incentive structures:

• What was the compensation structure for auditors

(fixed fee, hourly, etc.)?

• What contractual limitations were placed on auditors

(non-disclosure agreements, etc.)?

• Were there incentives for identifying system flaws or

vulnerabilities?

• Were auditors employed internally or contracted exter-

nally?

• Were there any performance-based incentives that

might bias results?
□ Review and communication

□ Review:

• What aspects of the evaluation (e.g. methodology, re-

port, findings) were subjected to review?

• Who reviewed these aspects, and what was their rela-

tionship to the auditors and system developers?

• What expertise did the reviewers bring to the process?
• How were reviewer disagreements resolved and what

changes resulted from the review process?

□ Feedback channels:

• What specific mechanisms exist for providing feed-

back on the audit?

• How can new information be submitted for considera-

tion after publication?

• Who should be contacted with questions or concerns

about the evaluation?

• Is there a plan for addressing follow-up questions

about the results?
□ Executive summary:

• Does the summary clearly explain what was evaluated,

how, and what was found?

• Are limitations of the evaluation explicitly stated?
• Is the summary accessible to non-technical audiences?

□ Definitions of key terms:

• Are technical terms and evaluation metrics clearly de-

fined?

• Is terminology consistent with industry standards?

□ Access to results:

• Who will receive which parts of the evaluation find-

ings?

• How and when will results be published or distributed?
• What information, if any, will be redacted from public

versions?

Appendix D Selection of governance

documents

We chose the relevant governance documents to include in
the analysis by considering the following three factors:

1. Major jurisdiction: broadly selected by geopolitical and
economic centrality, especially in the AI industry (Stan-
ford HAI staff 2024; Bianzino et al. 2023).

2. Authority of the institution: within each jurisdiction,
we chose government and non-government institutions.
METR was the exception because their evaluation reports
have been highly influential in the field, and often involve
co-authorship from researchers in scaling labs and AISIs.
3. Direct influence on model evaluations. For model devel-
opers, these tended to be their Responsible Scaling Poli-
cies or Frontier Safety Frameworks (see METR a). For
government bodies, we selected documents that tracked
with more scale and influence (i.e. more national/federal
than local, or more binding than not). The EU Code of
Practice is a unique outlier in not being strictly binding
but in effect being as influential as it enables presumption
of conformity with the Act (see European Union and EU
monitor).

To enable the governance documents to fit Table 3, we
abbreviated the names of the documents. Here, we present
their official names.

• Official regulations

– Brazil: We analyzed the Federal Senate Bill No.
2338/2023 (Brazilian Federal Senate 2023). It was ap-
proved by Senate in 2024, but still pending approval by
the House of Representatives and President to become
law.

– China: Governance of AI models and systems is de-
tailed across various documents. This analysis ac-
counts for: Security Specification for Generative AI
Pre-training and Fine-tuning Data (State Administra-
tion for Market Regulation and Standardization Ad-
ministration of China 2025), Draft AI Law, trans-
lated with scholars comments (Drafting Expert Group
2025); Internet Information Service Algorithmic Rec-
ommendation Management Provisions with effect
from 2022 (Creemers, Webster, and Helen Toner
2022); Measures for the Management of Generative
Artificial Intelligence Services (Draft for Comment)
2023 (Huang et al. 2023); China 2022 rules for deep

synthesis (Gu 2023); and China (Draft Measure on
Ethical Review).

– EU: We included the keystone AI Act (EU AI
Act 2024); with its accompanying Code of Practice
(“CoP”) (European Commission 2025). The EU AI
Act needs to be read in conjunction with the Code
of Practice. The Code of Practice is a unique type of
document which, while technically not legally bind-
ing, enables presumption of conformity with the EU
AI Act. In effect, due to the legal uncertainty of not
knowing what alternatives would comply, it is likely
to be followed by those wishing to be compliant with
the EU AI Act, resulting in effectively a binding effect
until “harmonized standards” are published.

– Singapore: We analyzed the Model AI Governance
Framework, which is not technically binding but au-
thoritative guidance. Model AI Governance Frame-
work for Generative AI (Singapore 2024).

– South Korea: We analyzed the “Basic Act on the De-
velopment of Artificial Intelligence and Establishment
of Foundation for Trust”, which comes into force Jan
2026. Governance of AI models and systems appears
to be done by a keystone AI Act with effect from 2026
(National Assembly of the Republic of Korea 2024).
– US: Given the lack of a US federal-wide AI regulation,
we examined the Trump Administration’s AI Action
Plan issued in July 2025. This does not have the status
of binding law but is the most authoritative signal at
the federal level as to how the US government might
think about governing model evaluations and risk as-
sessments (The White House 2025).

• Other norms

– Bletchley: The Bletchley Declaration by Countries At-
tending the AI Safety Summit, 1-2 November 2023
(UK Government 2023)

– Int’l Report: International AI Safety Report (UK AI

Safety Institute 2025)

– Japan AISI: Guide to Evaluation Perspectives (Japan

AI Safety Institute 2024)

– METR: Key Components of an RSP (METR 2024)
– NIST AI RMF: AI Risk Management Framework (Na-
tional Institute of Standards and Technology 2024)
– Paris: Statement on Inclusive and Sustainable Arti-
ficial Intelligence for People and the Planet ( ´Elys´ee
Palace 2025)

– Seoul: Seoul Declaration for Safe, Innovative and In-

clusive AI (UK Government 2024)

– UK AISI: AI Safety Institute Approach to Evaluations

(UK AI Safety Institute 2024)

• AI company policies

– Anthropic: Responsible Scaling Policy (Anthropic

2025a)

– Google DeepMind: Frontier Safety Framework v2

(Google 2025)

– Meta: Frontier AI Framework v1.1 (Meta 2025)

– Microsoft: Frontier Governance Framework (Mi-

crosoft 2025)

– OpenAI: Preparedness Framework Beta (OpenAI

2025b)

– xAI: Draft Risk Management Framework (xAI 2025)

Appendix E Stakeholder interviews

Detailed Methodology

We engaged with stakeholders through interviews in two
stages. During literature review and feature selection (see
Section 3), we engaged in a dozen off-the-record discus-
sions with academics, evaluation report writers, and policy
researchers. After completing the audit card framework, we
engaged in the ten semi-structured interviews with stake-
holder experts (see Section 6). Our protocol focused on cur-
rent practices, perceived gaps, and contextual needs.

During both stakeholder engagement stages, the feed-
back shaped our audit card design. For instance, we
distinguished compensation from conflicts of interest (“In-
tegrity”), or condensed features within “Review and feed-
back”. Interviewees also generally agreed with the high-
level value of this audit card proposal, but some expressed
doubts about implementation, resulting in the addition of
Appendix C.

The interview process was fully based on informed
consent. We implemented a comprehensive consent process,
obtaining explicit agreement on recording, attribution levels,
and data usage. Participants chose their preferred anonymity
level, and all quotes were verified before inclusion. Partic-
ipants were not compensated for the 30-minute voluntary
interviews.

Our procedure for reaching out to interviewees was as fol-

lows:

As part of the [anonymized for review], we are work-
ing on a research project on reporting contextual as-
pects of the AI evaluations process. The goal is to im-
prove the quality of evaluations through clearer norms
on responsible reporting. Here is a more detailed
project summary, and below you find the types of in-
formation an extensive literature survey has shown to
be relevant to evaluations reporting.
As part of this project, we are now looking to get the
input from diverse stakeholders in the evaluations pro-
cess. This could either be in writing or during a short
30-minute call. We would be grateful if you could an-
swer a few questions, which, depending on your ex-
act responsibilities as [role of interviewee], would be
some subset of the following:
[Questions as shown in Appendix E.]
Any contribution of yours will be appropriately cited
following academic standards. Please let me know if
you have any preferences regarding direct quotation
or paraphrasing. We are happy to adjust attribution to
reflect your preferred level of visibility, whether by
name, role at [interviewee organisation], or role more
generally. We are happy to share any citations or at-

tributions with you before publication to ensure accu-
racy and alignment with your preferences.
Finally, we followed up with interviewees to confirm the

level of attribution:

We’d be very grateful if you could let us know by
Wednesday EOD if you are alright with how this in-
formation is being presented. If it’s not acceptable to
you, we’d be grateful to understand why and how we
can better frame it for better accuracy or anonymity.
Any changes to the final draft will be in the direction
of less detail/identifiability.
This is how your identity is described: [description of
interviewee as per Table 5.]
This is how your interview is being attributed (you are
[Px], highlighted is where you’re cited alone, Py −
Pz indicate other interviews being referenced together
with yours):
[Selection from Section 6 that references the intervie-
wee.]

Interviewee details
See Table 5 for details on the background of interviewees.

Interview guide
The following is our interview guide and set of questions we
used for the 30-minute semi-structured interview with each
interviewee.
Introductions [3 mins]
• Introduce our project: We defined what audit cards are,

what we did and did not include in that scope
– Audit cards are a way to standardize reporting of AI
evaluation process, with the goal of contextualizing
what evaluations can do and transparency about the
process

– We state examples of what we include: why these met-
rics, who are the auditors, resources available (com-
pute, time) during eval, how they’re selected and po-
tential COI

– We disambiguate them from examples we don’t in-
clude: specific metrics, technical implications, elicita-
tion techniques;

• Outline process for interview: We walked interviewees

through what to expect of the interview
– Contribution: Used to color in details about evalua-

tions process from stakeholders.

– Privacy and permissions: We checked beforehand
what level of recording, attribution, and other process
checks they would be comfortable with. We confirmed
nothing they said to us will be shared to others without
it being run past them and them confirming in writing.

General questions to ask everyone [10 mins max]
1. Describe the work you do in relation to evaluations, try to
be specific about your responsibilities, identities of peo-
ple/orgs you relate to, your role in the evaluations field

Participant Organization
P1
P2
P3
P4
P5
P6
P7
P8
P9
P10

Third-party evaluator
[anonymized]
Scaling lab
Third-party evaluator
Third-party evaluator
[anonymized]
Third-party
Government
Third-party evaluator
[anonymized]

Role
Evaluation designer, developer & writer
[anonymized]
Evaluation developer
Evaluation developer
Evaluation developer & writer
Evaluation policy researcher
Evaluation policy researcher
Evaluation policymaker & writer
Evaluation development operations support
[anonymized]

Table 5: Overview of the stakeholders interviewed for the semi-structured interviews. The organization and role has been
reported up to the level of detail interviewees were comfortable with. Note: Participants P2 and P10 were excluded from the
final analysis as their interviews were conducted off the record and attributions could not be confirmed in time for publication.

2. Who is the evaluation report you [build/analyze/use] for?
Who is the target audience? E.g. developers (internal, ex-
ternal), research, governance, or also the general public.
3. What part of the evaluation process which, if not done
well/reported well, would make you doubt the quality of
the eval?

4. How do imagine evaluation best practices best becom-
ing reality? Do you see codification—whether in law or
Industry norm—as a good/valid way to quality control?
5. In your view, what are the biggest challenge preventing
evaluations from being better? More useful for improv-
ing safety, or whatever their key goal is?

Questions to ask specific categories of people [12 mins]
Evaluation developer

6. Do you consider the limitations and assumptions of your
evaluations process? Where does that thinking get cap-
tured (if it does)?

7. What is the background/expertise of auditors—does it
depend on the type of evaluation or something else, and
who makes that decision?

8. Can you give us examples of evaluations where the evalu-
ations process differed and whether it affected the quality
of eval?

9. Do you follow any internal best practices?
10. What is the current training process both internally (with
evaluation developers, human baseliners) and with your
engagement partner?

Evaluation report writer

11. What is the most important information to share in the

evaluation report? How do you decide that?

(a) Can you walk through two situations in which you de-
cided differently (i.e. type of info/detail level to pub-
lish and why)?

(b) What’s the right balance of transparency in reporting
evaluations, and what risks surround the achieving of
that?

12. From our skim of evaluation reports, we found these tend
to be underspecified/not specified—why do you think

that might be? e.g. assumptions, auditors’ background,
integrity and resources of process, peer review, commit-
ments to take action based on evaluation results, and state
criteria that make evaluation obsolete

Evaluation development overseer/manager & translate it
to policy people

13. Do you consider the limitations and assumptions of your
evaluations? Where does that thinking get captured (if it
does)?

(a) e.g. specific downstream application context on which

the benchmark is contingent;

14. How do you select the right auditors (external / internal)?

Walk through a recent eval’s selection?

15. How much autonomy does your organization get in de-
ciding access/resources (e.g. time/compute) for evalua-
tions [of a lab’s models]? What does this depend on?

(a) Do you include different stakeholders in the evalua-
tions process—who are they, and how are they en-
gaged?

16. What is the current training process both internally (with
evaluation developers, human baseliners) and with your
engagement partner?

17. What is the right balance of flexibility and specificity in
regulation? E.g. what makes an auditor ’qualified’ (back-
ground/training), conflict of interest, funding/contract
structures

18. If you wanted to, how easy would it be for you to be mis-

leading when communicating evaluation results? Why?
Evaluation operations support (decisions getting access to
resources that evaluation developers need)

19. What resources do you usually require for an eval, and
what influences that? Do you document resource require-
ments, and where do you share this?

20. What are the conditions of you being able to access
them? E.g. Recent Cyber CBRN Agent evaluations re-
port used blue/red anonymized models at UK AISI
21. Could you describe the different engagement processes,

and why some have been easier than others?

Evaluation used for recommendations - policy re-
searcher/think tank, funders, lobbying, advocacy

22. If you have had to use an evaluation report (could be your
org or another org.) to make a recommendation, what fea-
tures of the report have helped you to do so?

23. Do you have examples of/from evaluation reports you

found good and/or bad, and why?

24. How much do you trust evaluation results depending on
the funding source (e.g. internal different labs OpenAI,
external: Apollo, AISI)
AI safety communicators

25. How do you understand evaluations

(as distinct
type of evaluation report-

from audits) and what
ing/communication are you aware of?

26. What insights are people most often seeking from evalu-
ations, and how are evaluations (not) meeting that need?
27. Re target audience question: Why do you think [previ-
ous answer] is the relevant audience? Other relevant au-
dience segments, how does the messaging change? How
can evaluations most strongly communicate their goal?


