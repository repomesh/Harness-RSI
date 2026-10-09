<div align="center">

# Awesome Harness RSI [![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)

关于 agent 指令、memory、workflows、tools 与 runtime 如何根据执行反馈持续更新的阅读清单。

[项目主页](https://zgcagi.github.io/Harness-RSI/) · [实证证据](docs/reported-evidence.md) · [English](README.md)

</div>

配套论文：**Harness Self-Evolution: Theory, Algorithms, Evaluation, Applications, and Impact**。作者：Chuyang Wei、Haoxiang Guan、Minghang Zhu、Kexin Zhou、Jiyan He、Yifei Shen。

清单依照论文顺序组织：更新对象、Theory、Evaluation 与实证证据。项目主页提供精简的图文概览。

## 目录

- [相关综述](#related-surveys)
- [定义](#definition)
- [分类](#taxonomy)
- [阅读路径](#reading-roadmap)
- [前置工作](#precursors)
- [1. Interpreted Update Targets](#interpreted)
- [2. Executable Update Targets](#executable)
- [3. Theory](#theory)
- [4. Evaluation 与 Benchmarks](#evaluation)
- [5. 实证证据](#evidence)
- [贡献与维护](#contributing)
- [引用](#citation)

<a id="related-surveys"></a>

## 相关综述

已有综述按组件、反馈来源、外部状态或更新过程组织 self-evolving agents。本论文将更新对象与 evolutionary search、continual PAC learning 联系起来，再分析已有研究为四项 Evaluation Claims 提供了哪些证据。

- **A Survey of Self-Evolving Agents** `TMLR'26`：按演化什么、何时演化、如何演化、在哪里演化来组织。 [[paper]](https://arxiv.org/abs/2507.21046)
- **A Comprehensive Survey of Self-Evolving AI Agents** `arXiv'25`：按优化器反馈组织方法。 [[paper]](https://arxiv.org/abs/2508.07407) [[list]](https://github.com/EvoAgentX/Awesome-Self-Evolving-Agents)
- **Externalization in LLM Agents** `arXiv'26`：统一回顾记忆、技能、协议与 harness 工程。 [[paper]](https://arxiv.org/abs/2604.08224)
- **Code as Agent Harness** `arXiv'26`：按代码在 agent 循环中的角色组织。 [[paper]](https://arxiv.org/abs/2605.18747) [[list]](https://github.com/YennNing/Awesome-Code-as-Agent-Harness-Papers)
- **Recursive Self-Improvement in AI** `arXiv'26`：按更新过程的完整程度，组织从局部 self-refinement 到自主研究的方法。 [[paper]](https://arxiv.org/abs/2607.07663)
- **Self-Improvements in Modern Agentic Systems** `arXiv'26`：在显式的参数冻结假设下区分模型更新与 scaffold 更新，讨论独立评测与组件对照，未单独处理 Activation。 [[paper]](https://arxiv.org/abs/2607.13104) [[list]](https://github.com/selfimproving-agent/awesome-Self-Improving-Agents)
- **Self-Evolving Coding Agents** `arXiv'26`：区分模型侧更新与记忆、技能、工作流更新，并把自适应选择下的基准过拟合列为开放问题。 [[paper]](https://arxiv.org/abs/2608.03392)

<a id="definition"></a>

## 定义

**Harness** `H` 是模型 `M` 周围的软件与配置，包括执行控制、tools、上下文构建、memory、调度和基础设施。一次 rollout 表示为 `τ ~ Run(M, H, E)`，由候选不可修改的 evaluator `J` 评分。

Harness self-evolution 根据执行反馈，修订后续运行使用的状态：

```
B_k = {τ_k,i ~ Run(M, H_k, E_k,i)}
H_{k+1} = Update(H_k, B_k)
```

定义包含两个要求：**反馈驱动且可继续更新**，以及**跨运行保留状态**。算法根据执行经验生成或选择修订，后续运行仍可触发更新；采纳后的状态被保存，并由后续运行实际加载。候选被拒绝时，`H_{k+1} = H_k`。

理论分析固定 `M`，以分离 harness 变化。包含 model–harness co-evolution 的系统按其 harness 更新部分纳入；若比较中 weights 也发生变化，Attribution 需要相应对照。离线 prompt 或程序优化器作为前置方法保留，并说明其更新何时终止。仅训练 weights、固定组件或只修改当前任务输出，都不足以构成持续的 harness 更新过程。

**Self-evolution 指更新过程；self-improvement 需要收益证据。** 保存并加载修订说明状态得到保留；是否实际生效、是否带来收益，由 Evaluation 检验。

<a id="taxonomy"></a>

## 分类

按修改对象对方法分类。Interpreted payloads 由固定 host 读取；Executable updates 改变 host 调用的实现。Evaluation 协议单列；Theory 讨论这些方法共用的搜索结构与保证条件。

| 清单章节 | 内容 | 论文对应 |
|---|---|---|
| 1. Interpreted targets | Prompts、memory、workflow 规格 | §3 |
| 2. Executable targets | Tools、源代码、控制程序、plugins | §4 |
| 3. Theory | Evolutionary search、泛化、能力保留与准入 | §5 |
| 4. Evaluation | 评测协议与证据对照 | §6 |
| 5. 实证证据 | 每个方法的主结果所支持的 claims | §6 |

每项工作只设一个主要归类；Theory 可以再次引用方法来说明对应关系。[分类数据](data/taxonomy.json)记录论文 citation keys 与归类。

<a id="reading-roadmap"></a>

## 阅读路径

1. **[Reflexion](http://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)**：把反馈保存到后续尝试。
2. **[Voyager](https://openreview.net/forum?id=ehfRiF0R3a)**：积累可复用的可执行 skills。
3. **[DSPy](https://openreview.net/forum?id=PFS4ffN9Yx)**：固定 pipeline 内的优化。
4. **[DGM](https://openreview.net/forum?id=pUpzQZTvGY)**：保留候选档案的仓库修订。
5. **[Harness Updating ≠ Harness Benefit](https://arxiv.org/abs/2605.30621)**：区分加载与实际使用。
6. **[HarnessBank](https://arxiv.org/abs/2607.13683)**：区分提案、筛选与报告证据。

<a id="precursors"></a>

## 前置工作

- **Speculations Concerning the First Ultraintelligent Machine** `Adv. Computers'65`：把递归改进表述为机器设计出比自己更好的后继者。 [[paper]](https://doi.org/10.1016/S0065-2458%2808%2960418-0)
- **EURISKO** `Artif. Intell.'83`：学到的启发式规则会影响后续搜索，其中包含修改其他启发式规则的规则。 [[paper]](https://doi.org/10.1016/S0004-3702%2883%2980005-8)
- **Gödel Machines** `arXiv'03`：只有在系统证明某次自我重写能提高期望效用之后，这次重写才被执行。 [[paper]](https://arxiv.org/abs/cs/0309048)

<a id="interpreted"></a>

## 1. Interpreted Update Targets

这类方法修改固定组件读取的文本或协调状态。保存后的指令或 skill 是否被遵循，需要实际测量。条目中注明离线优化与单任务适应的情形。

### 1.1 Prompts 与指令

#### 基于分数的搜索

*根据候选分数提出并选择 prompt 修订。*

- **APE** `ICLR'23`：从输入输出样例里采样候选指令，保留分数最高的那个。 [[paper]](https://openreview.net/forum?id=92gvk82DE-) [[project]](https://sites.google.com/view/automatic-prompt-engineer)
- **OPRO** `ICLR'24`：将历史指令及其分数提供给 optimizer model，由它提出下一条候选。 [[paper]](https://openreview.net/forum?id=Bb4VGOWELI) [[code]](https://github.com/google-deepmind/opro)

#### Textual-gradient 优化

*将错误、反馈或执行轨迹转成文本参数的修改建议。*

- **ProTeGi** `EMNLP'23`：把任务错误转成自然语言"梯度"，再对编辑后的提示做 beam search。 [[paper]](https://aclanthology.org/2023.emnlp-main.494/)
- **TextGrad** `Nature'25`：在由模型调用组成的计算图上反向传播文本批评，可以改图中任意文本变量。 [[paper]](https://doi.org/10.1038/s41586-025-08661-4)
- **GEPA** `ICLR'26 Oral`：根据执行轨迹反思修订 prompts，并通过 Pareto selection 保留候选。 [[paper]](https://openreview.net/forum?id=RQm2KQTM5r)
- **Trace** `NeurIPS'24`：把执行轨迹当成计算图，由生成式优化器根据丰富反馈产出编辑。 [[paper]](https://arxiv.org/abs/2406.16218) [[project]](https://microsoft.github.io/Trace/)
- **metaTextGrad** `arXiv'25`：优化的是优化器自己的提示，只有验证集改善时才接受一次更新。 [[paper]](https://arxiv.org/abs/2505.18524)
- **EGO-Prompt** `arXiv'25`：面向领域部署，联合调整提示与一张语义因果图。 [[paper]](https://arxiv.org/abs/2510.21148)
- **SePO** `arXiv'26`：根据累积任务反馈，修订后续运行继续使用的 system prompts。 [[paper]](https://arxiv.org/abs/2606.04465) [[code]](https://github.com/taowangcheng/SePO)

#### 更新变异规则

*搜索用于生成后续变异的指令。*

- **Promptbreeder** `ICML'24`：任务提示与产生它的变异提示一起进化。 [[paper]](https://proceedings.mlr.press/v235/fernando24a.html)
- **DelvePO** `arXiv'25`：解耦提示的各个成分，沿识别出的方向引导变异。 [[paper]](https://arxiv.org/abs/2510.18257)
- **DEEVO** `arXiv'25`：通过结构化辩论产生指令，用 Elo 锦标赛给候选排序。 [[paper]](https://arxiv.org/abs/2506.00178)

### 1.2 Memory 与可复用流程

#### 经验提取

*将执行轨迹提炼为后续运行可检索的知识。*

- **Reflexion** `NeurIPS'23`：失败后存下自然语言反思，在同一任务的下一次尝试中载入。 [[paper]](http://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)
- **ExpeL** `AAAI'24`：从训练轨迹池里抽取跨任务经验规则，并用增删与投票机制维护这些经验规则。 [[paper]](https://doi.org/10.1609/aaai.v38i17.29936)
- **AWM** `ICML'25`：从轨迹中归纳反复出现的子目标工作流，可离线用训练划分做，也可在线从任务流做。 [[paper]](https://proceedings.mlr.press/v267/wang25bx.html)
- **Agent KB** `arXiv'25`：构造跨领域经验库，把检索到的前 k 条注入后续运行。 [[paper]](https://arxiv.org/abs/2507.06229)
- **ReasoningBank** `ICLR'26`：从成功与失败轨迹中提炼推理策略，汇总进一个注入系统指令的库。 [[paper]](https://openreview.net/forum?id=jL7fwchScm)
- **EvoRepair** `arXiv'26`：在长周期修复中累积、打分并复用漏洞修复经验。 [[paper]](https://arxiv.org/abs/2605.30105)
- **SWE-Exp** `arXiv'25`：把历史搜索轨迹中的 issue 解决经验蒸馏进一个库，新 issue 到来时查询。 [[paper]](https://arxiv.org/abs/2507.23361) [[code]](https://github.com/YerbaPage/SWE-Exp)
- **MemCoder** `arXiv'26`：随代码库一起生长的结构化记忆，内容是仓库知识与修复结果。 [[paper]](https://arxiv.org/abs/2603.13258)
- **Behavioral Rules** `arXiv'26`：把部署会话中经工程师评审的行为规则累积成一个纳入版本控制的文件，作为会话上下文载入。 [[paper]](https://arxiv.org/abs/2607.13091)
- **Memory Transfer** `arXiv'26`：在四种记忆格式下测量一个领域形成的记忆迁到另一个领域的效果。 [[paper]](https://arxiv.org/abs/2604.14004)

#### 可复用 Skillbooks

*保存能指导后续任务的明确操作流程。*

- **Trace2Skill** `arXiv'26`：把轨迹局部的经验教训蒸馏成可迁移的技能文档，在演化集的一个验证子集上排序。 [[paper]](https://arxiv.org/abs/2603.25158)
- **SkillClaw** `arXiv'26`：agent 式演化器，验证器只在候选技能于验证任务上超过活跃技能池时才接受它。 [[paper]](https://arxiv.org/abs/2604.08377)
- **CodeSkill** `arXiv'26`：通过部署前的预备遍历构建技能库，学习可自演化的编码技能。 [[paper]](https://arxiv.org/abs/2605.25430)
- **GSkill** `ACM AIAS'26`：从历史运行中自动学出编码 agent 的 `SKILL.md` 文件。 [[paper]](https://doi.org/10.1145/3786335.3813196)
- **GSE** `arXiv'26`：在"留出一个项目"的划分下，用本地验证与回放验证把关，学习全局可复用的技能。 [[paper]](https://arxiv.org/abs/2608.06153)
- **MUSE-Autoskill** `arXiv'26`：把技能创建、记忆与管理耦合起来，只有通过自己生成的测试，技能才被注册。 [[paper]](https://arxiv.org/abs/2605.27366)
- **MemP** `ACL'26 Findings`：从轨迹中蒸馏流程性记忆，并比较不同的更新策略与抽象粒度。 [[paper]](https://doi.org/10.18653/v1/2026.findings-acl.866)
- **Skill Consumption** `arXiv'26`：检验生成的 skills 如何影响后续行为，包括默认策略变化与显式调用。 [[paper]](https://arxiv.org/abs/2605.23899)
- **SkillForge** `SIGIR'26 Industry`：从执行经验中学习可复用的 skill 文档，并将后续时间段单独留作报告评测。 [[paper]](https://doi.org/10.1145/3805712.3808466)

#### 验证与整合

*通过验证或维护规则修订、压缩或替换存储内容。*

- **Dynamic Cheatsheet** `EACL'26`：维护一份测试时持续整理的策略备忘。 [[paper]](https://aclanthology.org/2026.eacl-long.333/)
- **ACE** `ICLR'26`：用增量式的 delta 更新扩展并巩固一份演化中的上下文手册，避免整体重写。 [[paper]](https://openreview.net/forum?id=eC4ygDs02R)
- **SkillOpt** `arXiv'26`：修订后的技能集先在验证集上评估，再替换活跃库。 [[paper]](https://arxiv.org/abs/2605.23904)
- **SkillOpt-Lite** `arXiv'26`：结合带容忍区间的验证规则、编译与 smoke tests，以较低成本决定是否采纳 skill 修改。 [[paper]](https://arxiv.org/abs/2607.03451) [[code]](https://github.com/EvolvingLMMs-Lab/SkillOpt-Lite)
- **Janus** `arXiv'26`：在候选偏离近期更新方向时，用覆盖任务、边界任务与新任务比较旧 memory 和候选 memory，再决定是否替换。 [[paper]](https://arxiv.org/abs/2606.31121)
- **VALVE** `arXiv'26`：在验证任务上进行配对比较后采纳 skill 修订，并跟踪长任务序列中的性能回落。 [[paper]](https://arxiv.org/abs/2609.32990)
- **TACO** `arXiv'26`：为 terminal agents 压缩观测内容，并使用写回准入规则与无需奖励信号的保留停止规则。 [[paper]](https://arxiv.org/abs/2604.19572) [[code]](https://github.com/multimodal-art-projection/TACO)
- **SkillMOO** `arXiv'26`：通过 NSGA-II 排序，在多个目标下选择 skill 组合。 [[paper]](https://arxiv.org/abs/2604.09297)
- **EffiSkill** `arXiv'26`：从验证过的代码对中挖掘效率技能，候选在公开划分上排序，报告用私有划分。 [[paper]](https://arxiv.org/abs/2603.27850)
- **VASO** `arXiv'26`：可形式验证的技能，每个计划在运行前先对技能的规格做模型检查。 [[paper]](https://arxiv.org/abs/2606.05395)
- **Memory Management** `ACL'26`：实证研究保留、删除与检索规则如何改变任务结果，并给出一个基于相似度的遵循度度量。 [[paper]](https://aclanthology.org/2026.acl-long.27/)
- **MCE** `ICML'26`：对 skills 采用 history-informed (1+1) 演化策略，结合 agentic crossover 与验证档案。 [[paper]](https://icml.cc/virtual/2026/poster/64296)
- **Living-Harness** `arXiv'26`：交互式 agent 演化器，跨周期把检索到的记忆巩固成一张可复用的图。 [[paper]](https://arxiv.org/abs/2607.26598) [[code]](https://github.com/anotherbricki/Living-Harness)

### 1.3 Workflows 与拓扑

#### 固定 Pipeline 编译

*在固定 pipeline 结构内优化 prompts 与 demonstrations。*

- **DSPy** `ICLR'24`：编译声明式的模型程序，优化提示与示例，控制流保持固定。 [[paper]](https://openreview.net/forum?id=PFS4ffN9Yx) [[code]](https://github.com/stanfordnlp/dspy)
- **MIPRO** `EMNLP'24`：在多阶段模型程序的各个阶段上，联合优化指令与示例。 [[paper]](https://aclanthology.org/2024.emnlp-main.525/) [[project]](https://dspy.ai)

#### 图与拓扑搜索

*搜索固定算子之间的连接与协作方式。*

- **GPTSwarm** `ICML'24`：把固定算子之间的边变成可学习的，优化由此得到的通信图。 [[paper]](https://proceedings.mlr.press/v235/zhuge24a.html) [[code]](https://github.com/metauto-ai/gptswarm)
- **Mass** `ICLR'26`：在预定义的多 agent 模块上，联合搜索 agent 提示与通信拓扑。 [[paper]](https://proceedings.iclr.cc/paper_files/paper/2026/hash/1ab4e0e8f35078109bc78d7b465d306f-Abstract-Conference.html)
- **MaAS** `ICML'25`：从一个由预定义算子构成的 agent 超网中，采样与查询相关的架构。 [[paper]](https://proceedings.mlr.press/v267/zhang25bi.html)
- **AFlow** `ICLR'25`：把工作流序列化成组合可复用算子的代码，再在其上搜索结构与提示，算子实现本身不动。 [[paper]](https://openreview.net/forum?id=z5uVAKwmjf) [[code]](https://github.com/FoundationAgents/AFlow)
- **AgentSquare** `ICLR'25`：在模块化设计空间中搜索模块组合，同时也生成新的模块实现。 [[paper]](https://openreview.net/forum?id=mPdmDYIQ7f) [[code]](https://github.com/tsinghua-fib-lab/AgentSquare)

#### 反馈驱动的 Workflow 修订

*根据执行反馈修订 workflow 规格。*

- **SEW** `arXiv'25`：同时变异提示与拓扑，并比较不同的工作流表示方式。 [[paper]](https://arxiv.org/abs/2505.18646)
- **JudgeFlow** `arXiv'26`：用块级别的裁判诊断来修订顺序块、循环块与条件块。 [[paper]](https://arxiv.org/abs/2601.07477)
- **RHI** `arXiv'26`：在单个任务回合内，把成对反馈作用于角色、指令、通信契约与交互跳数。 [[paper]](https://arxiv.org/abs/2607.15524)
- **Meta-Team** `arXiv'26`：跨任务携带经验，更新一套可复用脚手架，内容包括 agent 提示、队友画像、协作笔记与共享协调规则。 [[paper]](https://arxiv.org/abs/2605.29790)
- **Symbolic Learning** `AI Open'25`：通过反向传播的语言损失，联合修订流水线结构、提示与工具。 [[paper]](https://doi.org/10.1016/j.aiopen.2025.11.004)

离线 prompt 优化器与固定 pipeline 编译器提供候选生成机制。只有更新机制持续留在部署后的运行周期内，才构成 operational self-evolution。

<a id="executable"></a>

## 2. Executable Update Targets

这类方法修改可执行实现，边界可以是 tool、组件、控制程序或 plugin 接口。代码可执行，并不直接说明修改后的路径在评测中被调用。

### 2.1 Tools 与代码补丁

#### 可调用工具合成

*生成通过工具接口调用的可复用程序。*

- **Voyager** `TMLR'24`：把自验证通过的程序变成不断生长的技能库，后续任务可检索并组合。 [[paper]](https://openreview.net/forum?id=ehfRiF0R3a) [[project]](https://voyager.minedojo.org/)
- **PolySkill** `arXiv'25`：归纳多态的技能抽象，让学到的技能能用在产生它的场景之外。 [[paper]](https://arxiv.org/abs/2510.15863) [[code]](https://github.com/simonucl/PolySkill)
- **FlowEvo** `arXiv'26`：把一条成功的工作流编译成经验证的可调用产物存入持久技能库，之后既可直接执行，也可把它的结构描述交给工作流生成。 [[paper]](https://arxiv.org/abs/2607.21596) [[code]](https://github.com/DEFENSE-SEU/FlowEvo)
- **Live-SWE-agent** `arXiv'25`：运行时临时生成 Bash 与 Python 工具，这些工具随任务容器一起销毁，因此它展示了工具合成，但没有持久的 harness 演化。 [[paper]](https://arxiv.org/abs/2511.13646)
- **RoboPhD** `arXiv'26`：让一个确定性的 Python 分析工具与模型可读的 SQL 指令共同演化，交付时这对产物不再依赖演化基础设施。 [[paper]](https://arxiv.org/abs/2601.01126)

#### 基于执行证据的组件修改

*在固定外围 executor 下，修改指定的可执行组件。*

- **Self-Harness** `arXiv'26`：从 incumbent 提出修改，要求两个评测划分均不退化，且至少一个划分有收益，才采纳候选。 [[paper]](https://arxiv.org/abs/2606.09498) [[code]](https://github.com/qzzqzzb/Self-Harness)
- **HarnessCompass** `arXiv'26`：分别优化 harness 组件，再将它们组合成候选配置。 [[paper]](https://arxiv.org/abs/2608.01918)
- **AHE** `arXiv'26`：利用 submit-guard 与 shell 轨迹诊断组件修改，并支持按文件回滚。 [[paper]](https://arxiv.org/abs/2604.25850)
- **HarnessFix** `arXiv'26`：从失败轨迹诊断 harness 故障，修复只能经由验证集评估才被接受。 [[paper]](https://arxiv.org/abs/2606.06324)
- **ReCreate** `ACL'26`：在一个小规模开发集上，于文本与代码两个层面编辑角色、流程、工具与记忆组件，明确排除执行环境与系统基础设施的适配。 [[paper]](https://aclanthology.org/2026.acl-long.1432/)
- **AutoSaddler** `arXiv'26`：保留在 minibatch 上改善的补丁，在开发集上选择候选，再在按组隔离的测试集上报告结果。 [[paper]](https://arxiv.org/abs/2608.23041)
- **CHASE** `arXiv'26`：用可能消除表面收益的协议变换检验候选补丁，要求补丁通过已确认的变换。 [[paper]](https://arxiv.org/abs/2609.18366)
- **Evo-Harness** `arXiv'26`：沿在线任务流把累积的上下文编译成 harness 层面的技能，并把失败转成功的轨迹与技能内容对应起来。 [[paper]](https://arxiv.org/abs/2608.15071) [[code]](https://github.com/A-EVO-Lab/a-evolve)
- **HarnessBank** `arXiv'26`：按语义描述符存档组件补丁，在 screening 阶段检查 activation beacons，并将评测代码置于候选不可修改的内核。 [[paper]](https://arxiv.org/abs/2607.13683)
- **Ecdysis** `arXiv'26`：训练运行时 harness，晋升只看训练目标，冻结后的 harness 在留出划分上评分。 [[paper]](https://arxiv.org/abs/2609.11677)
- **MemEvolve** `arXiv'25`：重写固定 memory-provider 接口背后的编码、存储、检索与管理实现。 [[paper]](https://arxiv.org/abs/2512.18746)
- **GUI-HARVEST** `arXiv'26`：从重复 GUI 执行中识别反复出现的失败，为限定范围的代码修改记录预期行为。 [[paper]](https://arxiv.org/abs/2610.00948)
- **Harness Ceiling** `arXiv'26`：通过长程规划任务上的 harness 修改，分析仍需 weight training 处理的失败。 [[paper]](https://arxiv.org/abs/2610.11655)

### 2.2 仓库与 Runtime 逻辑

#### 完整控制程序搜索

*搜索控制程序；VERSE 还修订负责提出候选的 optimizer。*

- **ADAS** `ICLR'25`：固定的元 agent 写出新的 agent `forward` 实现，评估过的候选存入档案。 [[paper]](https://openreview.net/forum?id=t9U3LW7JVX) [[project]](https://shengranhu.com/ADAS)
- **Meta-Harness** `COLM'26`：把历史候选的源码、分数与轨迹交给一个外部编码 agent，要求它合成完整的任务专用 harness 程序。 [[paper]](https://arxiv.org/abs/2603.28052)
- **RRSI** `arXiv'26`：通过编辑预算、泄漏检查与按噪声调整的准入阈值，对程序搜索施加约束。 [[paper]](https://arxiv.org/abs/2609.24972) [[code]](https://github.com/google-research/rrsi)
- **VERSE** `arXiv'26`：在执行检查下，同时修订 executor harness 与 optimizer 的 prompts、tools、hooks 和 notes。 [[paper]](https://arxiv.org/abs/2610.02616)

#### 仓库修订

*编辑纳入版本管理的 harness 实现，并保留后续演化可使用的候选。*

- **SICA** `arXiv'25`：把自己的多文件 Python 代码库，包括工具、子 agent 与控制流，交给档案中表现最好的 agent 修改。 [[paper]](https://arxiv.org/abs/2504.15228)
- **DGM** `ICLR'26`：把仓库变体分叉进一个开放式档案，父代选择兼顾性能与新颖性。 [[paper]](https://openreview.net/forum?id=pUpzQZTvGY)
- **DarwinX** `arXiv'26`：通过选择、变异与重组，演化仓库层面的 harness 候选。 [[paper]](https://arxiv.org/abs/2608.07545)
- **HGM** `arXiv'25`：估计谱系层面的产出能力，用 Thompson 采样分配谱系扩展与候选评估的预算。 [[paper]](https://arxiv.org/abs/2510.21614) [[code]](https://github.com/metauto-ai/HGM)
- **Group-Evolving Agents** `arXiv'26`：让被选中的父代先共享代码补丁、工具与执行经验，再产出框架层面的补丁。 [[paper]](https://arxiv.org/abs/2602.04837)
- **MOSS** `arXiv'26`：重写路由、钩子、状态管理与分发代码，再在健康检查加人工授权之后替换容器。 [[paper]](https://arxiv.org/abs/2605.22794) [[code]](https://github.com/hkgai-official/Moss)
- **Ouroboros** `arXiv'26`：通过经评审的提交演化自己的核心，配有运行清单、种子证明与公开的逐任务轨迹。 [[paper]](https://arxiv.org/abs/2608.08311)
- **AgentDevel** `arXiv'26`：把自演化重构为发布工程，包括版本化 diff、候选版本回归测试、逐轮的失败转成功与成功转失败记录。 [[paper]](https://arxiv.org/abs/2601.04620)
- **EvolveNet** `arXiv'26`：合并不同客户端的 harness 修改，验证合并补丁后再同步共享状态。 [[paper]](https://arxiv.org/abs/2608.04968)

#### 进程内修改

*将修改应用到运行中的进程；能否持续生效取决于保存与重新加载机制。*

- **Gödel Agent** `ACL'25`：用 monkey patching 替换活 Python 内存中的决策方法、动作空间与自我修改例程，修改随进程结束而消失。 [[paper]](https://aclanthology.org/2025.acl-long.1354/)
- **TTHE** `arXiv'26`：测试时从执行轨迹演化出可执行的 harness 程序，并把选中的程序带入后续输入。 [[paper]](https://arxiv.org/abs/2607.08124)
- **Life-Harness** `arXiv'26`：同时适配环境契约、动作实现与轨迹调控，随后冻结运行时接口做评测。 [[paper]](https://arxiv.org/abs/2605.22166) [[code]](https://github.com/Tianshi-Xu/Life-Harness)

### 2.3 Plugin 架构

#### 接口约束下的 Hooks

*通过明确接口与准入检查，将更新绑定到 hooks。*

- **HarnessX** `arXiv'26`：提交一份候选配置前先检查钩子类型、单例约束与冒烟测试，并要求每个编辑声明它生效时必然出现的轨迹特征。 [[paper]](https://arxiv.org/abs/2606.14249)
- **Argus** `arXiv'26`：通过通用 agent runtime 提供 skills，并沿长任务流持续修订。 [[paper]](https://arxiv.org/abs/2608.05144)

#### Microkernel 平台

*固定精简的 host，通过 plugin 接口提供可替换组件。*

- **DeepSeek Harness** `产品'26`：Cordis 内核通过声明依赖连接运行时组件，追加式记录支持检查点与回放。它展示的是执行载体，不是一个有报告的自演化闭环。 [[page]](https://www.deepseek.com/harness/en/)
- **Autogenesis** `arXiv'26`：自演化 agent 协议，带显式的提出、评估、提交周期，以及谱系与版本记录。 [[paper]](https://arxiv.org/abs/2604.15034) [[code]](https://github.com/DVampire/Autogenesis)
- **ModularRSI** `arXiv'26`：在固定 composer 后演化模块，通过不读取奖励的准入检查筛选更新，任务由外部整理。 [[paper]](https://arxiv.org/abs/2609.14857)
- **Cordis / Spatiotemporal Composability** `arXiv'26`：该内核背后的形式演算，自演化 harness 被列为未来工作。 [[paper]](https://arxiv.org/abs/2608.25512)

Live-SWE-agent 的工具限于当前任务，Gödel Agent 的修改限于进程生命周期。这些条目展示可执行修订机制，同时具有持久性限制。Plugin 接口约束可以限制调用与权限，任务正确性仍需评测。

<a id="theory"></a>

## 3. Theory

Harness search 根据任务分数与执行反馈提出修改，不对程序本身求导。EA 对应关系描述表示、变异、选择与资源分配，并不表示每个系统都实现了标准 EA。

### 3.1 Evolutionary Algorithms 对应

| EA 范式 | 对应范围 | 系统 |
|---|---|---|
| 精英 (1+1) 与演化策略 | 单个候选与当前版本比较；MCE 明确采用 history-informed (1+1)-ES，其余系统共享候选选择结构 | SICA · MCE · SkillOpt · SkillOpt-Lite · SkillClaw |
| 精英 (1+λ) 风格 | 从同一当前版本提出多个编辑，接受前先评估；把兼容的编辑合并与标准 (1+λ)-ES 的存活者选择不同 | Self-Harness |
| 档案式程序搜索 | 程序充当个体，搜索由父代选择、代码修改与谱系保留组织；这是程序层面的 EA 对应，不是经典树状 GP 算子 | DGM · DarwinX · HGM |
| 重组与交叉 | 跨候选组合互补内容；Trace2Skill 只提供补丁合并层面的类比，没有完整的演化选择过程 | DarwinX · HarnessCompass · Self-Harness · MCE · Trace2Skill |
| Quality-diversity与 MAP-Elites | 语义描述符把档案划分成格子，每格保留精英；HarnessBank 改动了父代选择并加了验证检查 | HarnessBank |
| 协同共演化 | 先按组件优化再组合，对应关系有限，因为没有显式维护独立演化的子种群 | HarnessCompass |
| 多目标 EA 的 Pareto Selection | 性能与成本的前沿，或多准则准入规则，类似 Pareto Selection；这是候选选择层面的对应，不是 NSGA-II 的实现 | Meta-Harness · Self-Harness · SkillMOO |
| bandit 引导的演化 | Thompson 采样分配谱系扩展与候选评估的预算 | HGM |

### 3.2 PAC 学习与稳定性

Continual PAC 分析区分**样本稳定性**、**历史能力保留**与**候选准入**，假设 task loss 有界、任务来自外生独立抽样，且模型与 evaluator 固定。代码改动很小不能直接说明稳定性；每轮允许的小幅退化也可能累积。

每轮至多比较 `K` 个候选，共 `T` 轮；每轮使用与候选生成独立的 `m` 个新任务，配对准入条件为：

```
Δ̂_k(H′) + sqrt(2 ln(KT/δ) / m) < 0
```

`Δ̂` 表示候选 loss 减去 incumbent loss。在这些假设下，以联合置信度 `1−δ` 保证被实际评测的候选在该轮任务混合分布上有收益。结论不覆盖未经测试的合并版本，或查看验证结果后再修改的候选。重复 rollout 能降低执行噪声，但不会增加独立任务数。

#### 稳定性与保留

- **Learnability, Stability and Uniform Convergence** `JMLR'10`：把算法对单个样本的敏感度与它的泛化差距联系起来。[[paper]](https://www.jmlr.org/papers/v11/shalev-shwartz10a.html)
- **Memory Bounds for Continual Learning** `FOCS'22`：给出持续学习所需记忆的下界，说明泛化与保留应当合在一起处理。[[paper]](https://arxiv.org/abs/2204.10830)

#### 基于置信界的准入

- **Hoeffding Bounds** `JASA'63`：为有界经验 loss 的偏差提供上界，用于构造配对准入条件。 [[paper]](https://doi.org/10.1080/01621459.1963.10500830)
- **Selection Overfitting** `JMLR'10`：分析模型选择中的过拟合及其对报告性能带来的偏差。 [[paper]](https://jmlr.org/papers/v11/cawley10a.html)
- **The Reusable Holdout** `Science'15`：在反复依赖数据的决策中保持留出集的有效性。[[paper]](https://doi.org/10.1126/science.aaa9375) · [[companion]](https://arxiv.org/abs/1506.02629)
- **SkillForge** `SIGIR'26 Industry`：从执行经验中学习可复用的 skill 文档，并将后续时间段单独留作报告评测。 [[paper]](https://doi.org/10.1145/3805712.3808466)

#### 自改进的上界

- **Harness Evolution as Learning** `arXiv'26`：自改进个人 agent 的逼近、泛化与优化上界。[[paper]](https://arxiv.org/abs/2609.36892)
- **A Theory of Reliable Self-Evolution** `arXiv'26`：推导采纳条件，其上限由验证与评测成本决定。[[paper]](https://arxiv.org/abs/2609.08175)

### 3.3 背景统计与优化工具

- **The Ladder** `ICML'15`：在反复自适应提交之下仍然可靠的排行榜机制。[[paper]](https://proceedings.mlr.press/v37/blum15.html)
- **Train Faster, Generalize Better** `ICML'16`：以 SGD 的稳定性推导泛化界。[[paper]](https://proceedings.mlr.press/v48/hardt16.html)
- **PAC-Bayes for Prompts** `arXiv'23`：提示工程也许不需要重新思考泛化。[[paper]](https://arxiv.org/abs/2310.03957)
- **ZOPO** `arXiv'24`：局部化的零阶提示优化。[[paper]](https://arxiv.org/abs/2403.02993)
- **Statistical Limits** `TMLR'26`：自改进 agent 的统计上限。[[paper]](https://arxiv.org/abs/2510.04399)
- **AdaEvolve** `arXiv'26`：自适应的、由大模型驱动的零阶优化。[[paper]](https://arxiv.org/abs/2602.20133)
- **GAMBLe** `arXiv'26`：AI 驱动研究系统的分析框架。[[paper]](https://arxiv.org/abs/2606.02863)
- **Mutation Without Variation** `GECCO'26`：大模型驱动程序演化中的收敛动力学。[[paper]](https://arxiv.org/abs/2606.05408) [[code]](https://github.com/can-gurkan/lmca)
- **What Fits Doesn't Overfit** `arXiv'26`：机器学习研究 agent 中的压缩与泛化。[[paper]](https://arxiv.org/abs/2606.11045)
- **IMABO** `arXiv'26`：推理时的 bandit 超参优化。[[paper]](https://arxiv.org/abs/2609.01335) [[code]](https://github.com/Tiime-Software/IMABO)

<a id="evaluation"></a>

## 4. Evaluation 与 Benchmarks

一项报告收益涉及四个不同问题。Selection 检查分数如何得到；Activation、Attribution 与 Improvement 检查它能支持什么结论。

| Claim | 所需证据 |
|---|---|
| **Selection** | 用于报告结果的任务反馈没有参与候选生成、排序、准入，以及报告轮次或配置的选择。 |
| **Activation** | 直接执行记录能把某项已采纳更新对应到报告结果的运行；注明 available、reached 或 carried，以及证据覆盖范围。 |
| **Attribution** | 对照隔离更新本身，控制 inference envelope，并表明收益超过实际测得的执行波动。 |
| **Improvement** | 记录评测任务与生成更新所用任务的距离、比较基线，以及测量收益的轮次。 |

![四项 Evaluation Claims 与纵向对照](assets/claims.png)

Activation 分三个层次：**available**，产物进入运行；**reached**，修改的路径被执行；**carried**，输出进入模型输入，或轨迹遵循了该产物。加载日志只说明 available；搜索或筛选阶段的轨迹不能证明更新在报告的测试运行中生效。

Attribution 用重复执行、配对检验或已报告的原始数据衡量波动。分数差距很大，或仅根据样本数估算出的 binomial bound，都不能替代实测波动。报告运行中的 model calls、生成 tokens、轮数、尝试次数与 effort setting，并将这些开销与搜索成本分开。

连续更新还需保留任务划分、产物版本与激活记录、模型与评测器版本、推理预算和重复测量。改变任务顺序、复测历史分布可用于检验能力保留。基准变化时，在同一协议下让两个 harness 状态分别运行两个快照；结论仍受快照内容及其此前用途限制。

### 4.1 各项 Claim 的评测

#### Selection 与评测器完整性

*将报告结果的证据与更新过程分开，并保护 scorer 不被候选修改。*

- **RSEA** `arXiv'26`：将不同数据分别用于候选生成、准入和结果报告。 [[paper]](https://arxiv.org/abs/2606.28374)
- **Anytime Certificates** `arXiv'26`：为反复依赖数据的准入决策提供 anytime-valid 证书。 [[paper]](https://arxiv.org/abs/2607.00871)
- **HarnessOpt-Bench** `arXiv'26`：整个搜索过程中测试划分都不可触及，这条边界由运行时强制执行，同时计量目标 agent 消耗的资源。 [[paper]](https://arxiv.org/abs/2608.06301)
- **Phantom Guardrails** `arXiv'26`：记录自改进 harness 修复了从未发生过的故障，补丁没有任何观测到的执行作为依据。 [[paper]](https://arxiv.org/abs/2607.13083)
- **Harness Tampering** `arXiv'26`：检查那些修改验证逻辑而不是修改被测行为的候选。 [[paper]](https://arxiv.org/abs/2609.00069)
- **Self-Authored Verification** `arXiv'26`：发现在启发式自改进 agent 中，自己写的检查不足以作为准入证据。 [[paper]](https://arxiv.org/abs/2607.24300)
- **SWE-bench+** `arXiv'24`：记录了解法泄漏与弱断言，它们同时污染晋升与报告。 [[paper]](https://arxiv.org/abs/2410.06992)

#### Runtime Activation

*记录被采纳的产物是否在生成报告结果的运行中实际生效。*

- **SkillsBench** `arXiv'26`：在多样任务上记录任务提供的技能是否被读取或引用。 [[paper]](https://arxiv.org/abs/2602.12670)
- **Harness Updating ≠ Harness Benefit** `arXiv'26`：分别测量 skill 加载率与轨迹遵循率，识别已加载但未被遵循的更新。 [[paper]](https://arxiv.org/abs/2605.30621) [[code]](https://github.com/A-EVO-Lab/a-evolve)
- **Skill Revisions** `arXiv'26`：检验按需加载 skill 时，其修订是否改变 coding agent 的实际行为。 [[paper]](https://arxiv.org/abs/2610.04832)

#### Attribution 对照

*通过对照区分更新效果、执行波动、推理计算量与评测器变化。*

- **Agents That Matter** `TMLR'25`：指出 agent 比较把能力与成本混在一起，要求做成本受控的评测。 [[paper]](https://arxiv.org/abs/2407.01502)
- **Token Cost** `arXiv'26`：分析并预测 agent 的 token 消耗，给资源开销一个可测的单位。 [[paper]](https://arxiv.org/abs/2604.22750)
- **MLE-bench** `ICLR'25`：机器学习工程任务，带重复运行与显式的算力开销。 [[paper]](https://arxiv.org/abs/2410.07095)
- **HAL** `ICLR'26`：把标准化的运行记录、模型快照与成本记账做成共享评测基础设施。 [[paper]](https://proceedings.iclr.cc/paper_files/paper/2026/file/a0928f924a344aaebbb7f6cd8d56e34c-Paper-Conference.pdf)
- **Claw-Eval** `arXiv'26`：给轨迹打分而不是只给最终状态打分，并重复试验，把能力和运气分开。 [[paper]](https://arxiv.org/abs/2604.06132)
- **AgentRewardBench** `COLM'25`：用专家标注对网页 agent 轨迹的自动裁判做元评测。 [[paper]](https://arxiv.org/abs/2504.08942) [[project]](https://agent-reward-bench.github.io)
- **Judge Inflation** `arXiv'24`：记录迭代自我精修中自发出现的 reward hacking。 [[paper]](https://arxiv.org/abs/2407.04549)
- **Memory Reward Inflation** `arXiv'26`：说明存下来的记忆可以抬高报告出的奖励，而行为并未变好。 [[paper]](https://arxiv.org/abs/2608.00017)
- **Who Grades the Grader** `arXiv'26`：分析 metrics 与 skills 共同演化时的 evaluator drift。 [[paper]](https://arxiv.org/abs/2607.12790) [[code]](https://github.com/amazon-science/Self-Evolving-Agents-Double-Ratchet)
- **Don't Blame the LLM** `arXiv'26`：把测到的编码 agent 差异归到 harness 演化上，而不是模型上。 [[paper]](https://arxiv.org/abs/2607.03691)
- **Scaffold Effect** `arXiv'26`：把 harness 选择当作编码 agent 比较中的一个隐藏变量。 [[paper]](https://arxiv.org/abs/2607.22585)
- **Rethinking Harness Evaluation** `arXiv'26`：分析报告 harness 演化收益时的评测协议混杂因素。 [[paper]](https://arxiv.org/abs/2607.12227)
- **Model–Harness Fit** `arXiv'26`：跨 agent 任务比较 model–harness 组合，分析二者的交互效应。 [[paper]](https://arxiv.org/abs/2610.00917)

#### 泛化与能力保留

*在 held-out 任务、新设置或历史分布上检验收益。*

- **HarnessDev** `arXiv'26`：把 harness 的*创建*与迭代*演化*分开，报告能力、成本与留出迁移。 [[paper]](https://arxiv.org/abs/2609.01437)
- **GDPevo** `arXiv'26`：在真实业务任务上给演化后的 harness 打分，留出任务由训练任务里分散的业务规则重新组合而成，因此测试时的增益可以追溯到训练经验。 [[paper]](https://arxiv.org/abs/2608.03764) [[code]](https://github.com/Prism-Shadow/GDPevo)
- **EvoHarnessBench** `arXiv'26`：逐步扩充提供给 agent 的 harness，测量能力增加时早先的能力是否保留。 [[paper]](https://arxiv.org/abs/2609.04280)
- **PATH-Bench** `arXiv'26`：路径相关的评测，刻意变动任务顺序并保留冻结的参照历史。 [[paper]](https://arxiv.org/abs/2608.01149)
- **Agent Plasticity** `arXiv'26`：衡量执行经验能否转化为 held-out 任务上的收益，并分析已有产物未被复用的原因。 [[paper]](https://arxiv.org/abs/2610.08902)
- **Skill Generalization** `arXiv'26`：比较演化后的 skills 在训练任务与 held-out 任务上的表现，检验收益能保留多少。 [[paper]](https://arxiv.org/abs/2609.39148)

### 4.2 纵向与动态评测

#### 活跃产物集合的完整性

*跟踪后续更新后哪些产物仍可访问并实际使用。*

- **Ratchet** `arXiv'26`：追问一个 LLM 裁判要多可靠，才够资格让一项技能退役。 [[paper]](https://arxiv.org/abs/2605.22148) [[code]](https://github.com/amazon-science/Self-Evolving-Agents-Ratchet)
- **SkillsVote** `arXiv'26`：对技能做全生命周期治理，涵盖收集、推荐与基于投票的整理。 [[paper]](https://arxiv.org/abs/2605.18401)
- **Library Drift** `arXiv'26`：诊断并修复不断变大的自演化技能库中的无声漂移。 [[paper]](https://arxiv.org/abs/2605.19576) [[code]](https://github.com/amazon-science/Self-Evolving-Agents-Ratchet)
- **Pre-Commit Gating** `arXiv'26`：在提交前检查 skill 修改，以阻止污染进入技能库。 [[paper]](https://arxiv.org/abs/2608.05810)
- **EVOMAL** `arXiv'26`：记录自演化编码 agent 的自我投毒现象。 [[paper]](https://arxiv.org/abs/2608.25776)

#### 合成边界任务

*构造新任务，并记录它们与生成更新所用反馈的重叠。*

- **Benchmark Self-Evolving** `arXiv'24`：多 agent 框架，从已有实例派生新实例做动态评测。 [[paper]](https://arxiv.org/abs/2402.11443) [[code]](https://github.com/NanshineLoong/Self-Evolving-Benchmark)
- **StressEval** `arXiv'26`：失败驱动的动态基准，从诊断出的失败生成实例。 [[paper]](https://arxiv.org/abs/2605.01939)

#### 时间任务流

*使用截止日期后发布的任务，并记录难度与内容的变化。*

- **LiveBench** `ICLR'25 Spotlight`：污染受限的基准，从截止日期之后的来源刷新，带客观答案。 [[paper]](https://arxiv.org/abs/2406.19314)
- **LiveCodeBench** `arXiv'24`：截止日期之后收集的带时间戳竞赛编程题。 [[paper]](https://arxiv.org/abs/2403.07974) [[project]](https://livecodebench.github.io/)
- **LiveMedBench** `arXiv'26`：带自动刷新的无污染医学基准。 [[paper]](https://arxiv.org/abs/2602.10367)
- **SWE-rebench** `arXiv'25`：自动化的任务收集与去污染评测流水线。 [[paper]](https://arxiv.org/abs/2505.20411) [[project]](https://swe-rebench.com)
- **SWE-bench Live** `arXiv'25`：由新合并的 issue 持续刷新的 SWE-bench。 [[paper]](https://arxiv.org/abs/2505.23419) [[project]](https://swe-bench-live.github.io/)

#### 对抗式交互

*分别报告 agent、任务生成器与评测器的变化。*

- **MathDuels** `COLM'26`：随参与者池一起增长的自博弈基准。 [[paper]](https://arxiv.org/abs/2604.21916)
- **Red Queen Gödel Machine** `arXiv'26`：在同一个闭环里共同演化 agent 与它们的评测器。 [[paper]](https://arxiv.org/abs/2606.26294)

#### 持续学习评测环境

*同时评测连续任务与任务之间传递的状态。*

- **LifelongAgentBench** `arXiv'25`：在技能相互依赖的任务序列上，把 agent 当作终身学习者评测。 [[paper]](https://arxiv.org/abs/2505.11942) [[project]](https://caixd-220529.github.io/LifelongAgentBench/)
- **PAST-Bench** `arXiv'26`：评测个人 agent 的 RSI 基础，对比开启与关闭持久化两种条件。 [[paper]](https://arxiv.org/abs/2608.04003) [[code]](https://github.com/Gen-Verse/PAST-Bench)
- **SEA-Eval** `arXiv'26`：评测 self-evolving agents 跨多个 episode 的表现。 [[paper]](https://arxiv.org/abs/2604.08988)
- **FinEvo-Bench** `arXiv'26`：金融专业场景的纵向基准，带匹配的持久化开关条件。 [[paper]](https://arxiv.org/abs/2608.06144)
- **ContinualSkillBench** `arXiv'26`：测量连续任务流中的 skill 学习与演化。 [[paper]](https://arxiv.org/abs/2608.03874)
- **SkillFlow** `arXiv'26`：评测终身的技能发现与演化。 [[paper]](https://arxiv.org/abs/2604.17308)
- **SkillLearnBench** `arXiv'26`：评测用于 agent 技能生成的持续学习方法。 [[paper]](https://arxiv.org/abs/2604.20087) [[code]](https://github.com/cxcscmu/SkillLearnBench)
- **MemoryArena** `arXiv'26`：相互依赖的多会话任务，早先的写入会影响后续工作。 [[paper]](https://arxiv.org/abs/2602.16313)
- **Evo-Memory** `arXiv'25`：评测带自演化记忆的测试时学习。 [[paper]](https://arxiv.org/abs/2511.20857)
- **Tool-Genesis** `arXiv'26`：面向自演化 agent 的任务驱动工具创建基准。 [[paper]](https://arxiv.org/abs/2603.05578)
- **SWE-EVO** `arXiv'25`：编码 agent 的长周期软件演化场景。 [[paper]](https://arxiv.org/abs/2512.18470)
- **CL-Bench** `arXiv'26`：真实有状态持续学习场景下的前沿系统评测。 [[paper]](https://arxiv.org/abs/2606.05661)
- **SEABench** `arXiv'26`：评测 self-evolving agents 在更新过程中产生的目标偏离。 [[paper]](https://arxiv.org/abs/2609.35596)
- **ServeLearnBench** `arXiv'26`：通过隐藏规则随时间变化的环境，评测 agent 从服务经验中持续学习的效果。 [[paper]](https://arxiv.org/abs/2610.07792)

<a id="evidence"></a>

## 5. 实证证据

<!-- evidence-summary:start -->

我们按四项 claims 整理论文两个更新对象分支中的 **96 个方法**，其中 2 个没有实证评测，94 份报告计入评分。每行以该方法主结果对应的同一项比较为依据，判定四项 claims 的证据是否充分。

| Claim | ✅ 充分 | ◐ 部分 | — 不支持 |
|---|---:|---:|---:|
| Selection | 43 | 17 | 34 |
| Activation | 8 | 86 | 0 |
| Attribution | 12 | 80 | 2 |
| Improvement | 53 | 19 | 22 |

判定描述报告提供了什么证据。各列标准不同，不能把充分证据的数量直接当作方法质量排名。Activation 的充分证据可能只覆盖一个已确认实例，覆盖范围记录在逐方法依据中。

同一份报告达到充分证据的 claim 数量：

| 0 | 1 | 2 | 3 | 4 |
|---:|---:|---:|---:|---:|
| 27 | 26 | 33 | 8 | 0 |

最常见的组合是 Selection 与 Improvement 充分、Activation 与 Attribution 部分。Activation 充分的报告有 8 份，Attribution 充分的有 12 份；详细判定需结合各自主结果与覆盖范围阅读。

各方法的判定、主结果与来源见[完整结果](docs/reported-evidence.md)，具体标准见[判定标准](docs/evidence-criteria.md)。

<!-- evidence-summary:end -->

<a id="contributing"></a>

## 贡献与维护

新增条目需说明更新对象、反馈来源、准入规则与保留的状态，提供原论文链接，并同步中英文。修正证据判定时，需指明主结果对应的比较，以及每个改动判定的具体依据。见 [CONTRIBUTING.md](CONTRIBUTING.md)。

2026-10-09 按[论文来源快照](data/source-snapshot.json)更新。证据表与网页数据可通过以下命令重新生成：

```bash
python3 scripts/build_evidence.py
python3 scripts/build_site_data.py
python3 scripts/check_consistency.py
```

<a id="citation"></a>

## 引用

```bibtex
@misc{wei2026harnessrsi,
  title  = {Harness Self-Evolution: Theory, Algorithms, Evaluation,
            Applications, and Impact},
  author = {Wei, Chuyang and Guan, Haoxiang and Zhu, Minghang and
            Zhou, Kexin and He, Jiyan and Shen, Yifei},
  year   = {2026},
  note   = {Working draft. arXiv identifier to be added on release.},
  url    = {https://github.com/zgcagi/Harness-RSI}
}
```

---

<sub>以 [CC BY 4.0](LICENSE) 发布。所列工作各自遵循其原有许可，本仓库只包含文献元数据、一句话机制总结与证据判定。图片由论文作者从配套论文中转载。</sub>
