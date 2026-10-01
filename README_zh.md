<div align="center">

# Awesome Harness RSI

**按理论框架组织的 harness 递归自改进（harness RSI）阅读清单。模型权重固定，agent 改写自己的指令、记忆、工作流与代码。**

中关村学院 · 中关村人工智能研究院

<p align="center">
  <a href="https://awesome.re"><img src="https://awesome.re/badge-flat2.svg" alt="Awesome"></a>
  <img src="https://img.shields.io/badge/papers-187-2F6B4F" alt="papers">
  <img src="https://img.shields.io/badge/audited%20methods-96-16429A" alt="audited methods">
  <img src="https://img.shields.io/badge/updated-2026--10-5498D0" alt="updated">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey" alt="license"></a>
</p>

<p align="center">
  <a href="#sdef">📘 定义</a>
  &nbsp;·&nbsp;
  <a href="#sorg">🧭 分类框架</a>
  &nbsp;·&nbsp;
  <a href="docs/claim-audit.md">🔬 证据审计（96 个方法）</a>
  &nbsp;·&nbsp;
  <a href="#ssurvey">📚 相关综述</a>
  &nbsp;·&nbsp;
  <a href="CONTRIBUTING.md">🤝 贡献指南</a>
</p>

[English](README.md)

</div>

![harness 自演化的四级路径：指令与提示、记忆与可复用流程、agent 工作流与拓扑、可执行组件与运行时](assets/banner.png)

![harness 更新对象与操作闭环](assets/overview.png)

<p align="center"><sub><b>这份清单依据的更新闭环。</b>左侧是固定宿主读取的解释型对象，右侧是宿主直接调用的可执行实现。闭环顺序为执行反馈、候选提出、准入、持久化与部署、后续复用。仅完成持久化既不能说明更新被激活，也不能说明性能提升。</sub></p>

> 本仓库是论文 **Harness Self-Evolution: Theory, Algorithm, Evaluations, Applications, and Social Impacts** 的配套阅读清单。下面第 1 到第 4 节对应论文分类图的四个分支，[证据审计](docs/claim-audit.md) 公开了论文 Table 5 背后的逐篇判定与依据。

---

## 目录

- [什么是 harness RSI](#sdef)
- [清单的组织方式](#sorg)
- [入门阅读路径](#sroad)
- [前身工作](#spre)
- [1. 解释型更新对象](#s1)
  - [1.1 提示与指令](#s11)
  - [1.2 记忆与可复用流程](#s12)
  - [1.3 工作流与拓扑](#s13)
- [2. 可执行更新对象](#s2)
  - [2.1 工具与代码补丁](#s21)
  - [2.2 仓库与运行时逻辑](#s22)
  - [2.3 一切皆插件](#s23)
- [3. 评测与基准](#s3)
  - [3.1 按 claim 划分的证据](#s31)
  - [3.2 纵向与动态证据](#s32)
- [4. 理论](#s4)
  - [4.1 演化算法对应](#s41)
  - [4.2 PAC 学习与稳定性](#s42)
  - [4.3 背景统计与优化工具](#s43)
- [5. 96 个方法的证据审计](#s5)
- [6. 持久状态带来的风险](#s6)
- [7. 已部署的 harness 与产品接口](#s7)
- [边界情形与排除范围](#sbound)
- [相关综述](#ssurvey)
- [领域增长图](#slandscape)
- [维护说明](#smaint)
- [贡献指南](#scontrib)
- [引用](#scite)
- [许可](#slicense)

---

<a id="sdef"></a>

## 什么是 harness RSI

**harness** `H` 指围绕模型 `M` 的那层软件与配置，它决定 `M` 在环境 `E` 中如何执行：agent 循环、工具与技能编排、上下文构造、记忆、上下文压缩、调度，以及沙箱、权限、日志这类执行基础设施。一次 rollout 写作 `τ ~ Run(M, H, E)`，由评测程序 `J` 打分，而 `J` 不属于 `H`。

**harness 递归自改进**是如下迭代过程：

```
B_t = { τ_t,i ~ Run(M, H_t, E_t,i) }         # 一批执行经验
H_{t+1} = Update(H_t, B_t)                    # 对 harness 的一次持久修改
```

其中骨干模型 `M` 保持不变。一个工作要进入这份清单，需要同时满足三个条件。

| 条件 | 判断标准 |
|---|---|
| **持久性** | 修改写入了后续运行会加载的 harness 状态，因此它会支配并非由它产生的那些 rollout。 |
| **递归性** | 被采纳的修改支配后续执行，而后续执行产生的 rollout 又反过来影响下一轮修改。 |
| **模型固定** | 循环内不更新权重，于是行为变化可以归到一次有名字的状态转移上，而不是模型能力的漂移上。 |

被拒绝的候选让 `H_{t+1} = H_t`。规则不变前提下的常规执行，比如追加一条会话日志、触发一个固定的压缩策略，不算 harness RSI。**一次更新不等于一次改进**，被采纳的修改到底有没有用是经验问题，这正是[第 3 节](#s3)要处理的。

<details>
<summary><b>这份清单排除了什么，以及为什么</b></summary>

- **仅在运行时自我纠错**，例如 Self-Refine、Self-Debug。纠错结果是本次 rollout 内部消费的任务输出，没有任何东西留给后续运行加载。
- **权重侧自改进**，例如 SPIN、TTRL、self-rewarding LM。它违反模型固定的前提，报告出的差异无法归到某次有名字的 harness 修改上。
- **静态 agent 框架**，例如 ReAct、CodeAct、AutoGen。它们提供脚手架，但脚手架本身不依据反馈被修改。
- **没有报告更新闭环的已部署产品**。它们确实跨会话保留状态，但没有报告反馈驱动的修改过程，单列在[第 7 节](#s7)。

有两个系统被收录但标注了限制。**Live-SWE-agent** 合成的工具随任务容器一起销毁，**Gödel Agent** 修补的是活进程内存，进程结束即消失。两者在机制上有参考价值，在持久性上不成立。

</details>

---

<a id="sorg"></a>

## 清单的组织方式

条目按**一次候选修改了什么**来分类，也就是按更新对象分类。在所有可选的分类轴里，只有更新对象是候选本身的属性，反馈来源属于产生它的搜索过程，终端分数属于报告它的那个数字。反馈来源、准入规则、资源开销、安全约束这些因素，作为更新的*属性*进入讨论，影响它的评测能支持什么结论，而不再充当并列的分类轴。

| 分支 | 可变对象 | 强制力 | 小节 |
|---|---|---|---|
| **1. 解释型更新对象** | 固定宿主读取的模型可读内容与协调状态 | 行为层面。一条指令可以改变输出倾向，但无法强制一个运行时不变量 | [1.1](#s11) · [1.2](#s12) · [1.3](#s13) |
| **2. 可执行更新对象** | 宿主直接调用的实现，包括工具、组件文件、控制程序、插件 | 可强制。修改本身会被执行 | [2.1](#s21) · [2.2](#s22) · [2.3](#s23) |
| **3. 评测与基准** | 自身贡献是评测协议或审计的工作 | 不适用 | [3.1](#s31) · [3.2](#s32) |
| **4. 理论** | 自身贡献是分析或对应关系的工作 | 不适用 | [4.1](#s41) · [4.2](#s42) |

**归类规则。**一个工作只列**一次**，放在与它自身贡献相符的节点下。因此第 3 节审计过的那些系统，出现在它们所修改的更新对象下面，而不出现在评测分支里。[第 4 节](#s4)是唯一声明的例外，它的贡献就是这组对应关系本身，所以会重新列出已经出现在第 1、2 节的系统。

三级标题命名的是**机制**，不是主题。两个系统共享一个三级标题，意思是它们实现了同一种"提出候选再准入"的结构，即使它们改的对象不同。

![分类与引用地图](assets/taxonomy.png)

<p align="center"><sub><b>完整分类。</b>四个分支各对应论文一节，第二层是小节，第三层是机制。这份清单是该图的逐项展开。</sub></p>

**条目格式。**机制句说明系统对自己的 harness 做了什么，不说明它跑出了多少分。

```markdown
- **名称** `会议'年份`：一句机制说明。[[paper]](url)
```

---

<a id="sroad"></a>

## 入门阅读路径

按顺序读这八篇，可以定位整个领域。

1. **[Reflexion](http://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)** `NeurIPS'23`，最小的闭环，失败后写一条自然语言反思，下次尝试时重新载入。
2. **[Voyager](https://openreview.net/forum?id=ehfRiF0R3a)** `TMLR'24`，最小的*可执行*闭环，自验证通过的程序累积成可检索的技能库。
3. **[DSPy](https://openreview.net/forum?id=PFS4ffN9Yx)** `ICLR'24`，编译视角，在程序员定义好的流水线内优化提示与示例，控制流不动。
4. **[ADAS](https://openreview.net/forum?id=t9U3LW7JVX)** `ICLR'25`，搜索视角，元 agent 直接写控制程序，候选存入档案。
5. **[DGM](https://openreview.net/forum?id=pUpzQZTvGY)** `ICLR'26`，开放式视角，仓库变体不断分叉，档案本身就是种群。
6. **[Harness Updating Is Not Harness Benefit](https://arxiv.org/abs/2605.30621)** `arXiv'26`，技能载入率与遵循率会严重分离，0.96 对 0.35。
7. **[HarnessBank](https://arxiv.org/abs/2607.13683)** `arXiv'26`，一条完整证据链长什么样：候选不可改的评测内核、每次尝试的激活信标、配对显著性门。
8. **[Agents That Matter](https://arxiv.org/abs/2407.01502)** `TMLR'25`，为什么一个终端分数不构成答案。

---

<a id="spre"></a>

## 前身工作

*大模型之前对"提出候选、评估、保留"这一结构的表述。*

- **Speculations Concerning the First Ultraintelligent Machine** `Adv. Computers'65`：把递归改进表述为机器设计出比自己更好的后继者。[[paper]](https://doi.org/10.1016/S0065-2458%2808%2960418-0)
- **EURISKO** `Artif. Intell.'83`：学到的启发式规则会影响后续搜索，其中包含修改其他启发式规则的规则。[[paper]](https://doi.org/10.1016/S0004-3702%2883%2980005-8)
- **Gödel Machines** `arXiv'03`：只有在系统证明某次自我重写能提高期望效用之后，这次重写才被执行。[[paper]](https://arxiv.org/abs/cs/0309048)

---

<a id="s1"></a>

## 1. 解释型更新对象

*修改落在模型可读内容或协调状态上。原生工具、算子实现、底层执行机制保持不变。可变面较小，候选之间好比较，代价是被采纳的产物依赖固定模型愿不愿意照着做。*

<a id="s11"></a>

### 1.1 提示与指令

包括系统指令、提示模板、few-shot 示例，以及变异提示本身。三代方法的区别在于**反馈携带了什么**。

#### 按分数搜索

*反馈只有每个候选一个数字。*

- **APE** `ICLR'23`：从输入输出样例里采样候选指令，保留分数最高的那个。[[paper]](https://openreview.net/forum?id=92gvk82DE-)
- **OPRO** `ICLR'24`：把历史候选及其分数喂给一个优化器模型，让它提出下一条指令。[[paper]](https://openreview.net/forum?id=Bb4VGOWELI)

#### 文本梯度式批评

*反馈是一个错误、一条批评或一整条轨迹，转成具体的编辑建议。*

- **ProTeGi** `EMNLP'23`：把任务错误转成自然语言"梯度"，再对编辑后的提示做 beam search。[[paper]](https://aclanthology.org/2023.emnlp-main.494/)
- **TextGrad** `Nature'25`：在由模型调用组成的计算图上反向传播文本批评，可以改图中任意文本变量。[[paper]](https://doi.org/10.1038/s41586-025-08661-4)
- **GEPA** `ICLR'26 Oral`：基于执行轨迹的反思式提示进化，候选在与报告测试集分开的 Pareto 划分上择优。[[paper]](https://openreview.net/forum?id=RQm2KQTM5r)
- **Trace** `NeurIPS'24`：把执行轨迹当成计算图，由生成式优化器根据丰富反馈产出编辑。[[paper]](https://arxiv.org/abs/2406.16218)
- **metaTextGrad** `arXiv'25`：优化的是优化器自己的提示，只有验证集改善时才接受一次更新。[[paper]](https://arxiv.org/abs/2505.18524)
- **EGO-Prompt** `arXiv'25`：面向领域部署，联合调整提示与一张语义因果图。[[paper]](https://arxiv.org/abs/2510.21148)
- **SePO** `arXiv'26`：根据累积的任务反馈重写长期存在的系统提示，而不是做一次性搜索。[[paper]](https://arxiv.org/abs/2606.04465)

#### 自指式变异

*变异过程本身也在搜索空间里。*

- **Promptbreeder** `ICML'24`：任务提示与产生它的变异提示一起进化。[[paper]](https://proceedings.mlr.press/v235/fernando24a.html)
- **DelvePO** `arXiv'25`：解耦提示的各个成分，沿识别出的方向引导变异。[[paper]](https://arxiv.org/abs/2510.18257)
- **DEEVO** `arXiv'25`：通过结构化辩论产生指令，用 Elo 锦标赛给候选排序。[[paper]](https://arxiv.org/abs/2506.00178)

> **这一层的终点。**多数提示优化器是*离线前身*，选出一条高分提示后冻结，闭环就结束了。把提示更新延伸到整个运行周期，问题会变成上下文管理，累积的指令占用有限的注意力预算并推高推理成本，这是 [1.2](#s12) 要处理的事情。无论写多少提示文本，它都不会变成可强制的运行时控制。

<a id="s12"></a>

### 1.2 记忆与可复用流程

从过往经验构造、并在后续运行中被检索进上下文的持久化模型可读状态。区分维度是**提取出的经验预期能用多久**，以及**库本身是否被维护**。

#### 经验挖掘

*把轨迹变成可检索的条目。*

- **Reflexion** `NeurIPS'23`：失败后存下自然语言反思，在同一任务的下一次尝试中载入。[[paper]](http://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)
- **ExpeL** `AAAI'24`：从训练轨迹池里抽取跨任务洞见，并用增删与投票机制维护这些洞见。[[paper]](https://doi.org/10.1609/aaai.v38i17.29936)
- **AWM** `ICML'25`：从轨迹中归纳反复出现的子目标工作流，可离线用训练划分做，也可在线从任务流做。[[paper]](https://arxiv.org/abs/2409.07429)
- **Agent KB** `arXiv'25`：构造跨领域经验库，把检索到的前 k 条注入后续运行。[[paper]](https://arxiv.org/abs/2507.06229)
- **ReasoningBank** `ICLR'26`：从成功与失败轨迹中提炼推理策略，汇总进一个注入系统指令的库。[[paper]](https://openreview.net/forum?id=jL7fwchScm)
- **EvoRepair** `arXiv'26`：在长周期修复中累积、打分并复用漏洞修复经验。[[paper]](https://arxiv.org/abs/2605.30105)
- **SWE-Exp** `arXiv'25`：把历史搜索轨迹中的 issue 解决经验蒸馏进一个库，新 issue 到来时查询。[[paper]](https://arxiv.org/abs/2507.23361)
- **MemCoder** `arXiv'26`：随代码库一起生长的结构化记忆，内容是仓库知识与修复结果。[[paper]](https://arxiv.org/abs/2603.13258)
- **Behavioral Rules** `arXiv'26`：把部署会话中经工程师评审的行为规则累积成一个纳入版本控制的文件，作为会话上下文载入。[[paper]](https://arxiv.org/abs/2607.13091)
- **Memory Transfer** `arXiv'26`：在四种记忆格式下测量一个领域形成的记忆迁到另一个领域的效果。[[paper]](https://arxiv.org/abs/2604.14004)

#### 流程化技能手册

*可复用单元是一份显式写下来的流程。*

- **Trace2Skill** `arXiv'26`：把轨迹局部的经验教训蒸馏成可迁移的技能文档，在演化集的一个验证子集上排序。[[paper]](https://arxiv.org/abs/2603.25158)
- **SkillClaw** `arXiv'26`：agent 式演化器，验证器只在候选技能于验证任务上超过现役技能池时才接受它。[[paper]](https://arxiv.org/abs/2604.08377)
- **CodeSkill** `arXiv'26`：通过部署前的预备遍历构建技能库，学习可自演化的编码技能。[[paper]](https://arxiv.org/abs/2605.25430)
- **GSkill** `ACM AIAS'26`：从历史运行中自动学出编码 agent 的 `SKILL.md` 文件。[[paper]](https://doi.org/10.1145/3786335.3813196)
- **Socratic-SWE** `arXiv'26`：用苏格拉底式追问从轨迹中导出技能，由一个留出验证池把关。[[paper]](https://arxiv.org/abs/2606.07412)
- **GSE** `arXiv'26`：在"留出一个项目"的划分下，用本地验证与回放验证把关，学习全局可复用的技能。[[paper]](https://arxiv.org/abs/2608.06153)
- **MUSE-Autoskill** `arXiv'26`：把技能创建、记忆与管理耦合起来，只有通过自己生成的测试，技能才被注册。[[paper]](https://arxiv.org/abs/2605.27366)
- **MemP** `ACL'26 Findings`：从轨迹中蒸馏流程性记忆，并比较不同的更新策略与抽象粒度。[[paper]](https://doi.org/10.18653/v1/2026.findings-acl.866)
- **Skill Consumption** `arXiv'26`：系统检验模型生成的技能下游到底有没有被消费，结论是它更多地重塑了默认策略，而不是触发显式调用。[[paper]](https://arxiv.org/abs/2605.23899)
- **SkillForge** `SIGIR'26 Industry`：为云技术支持锻造领域专用的自演化技能，并留出一个闭环从未见过的时间尾段分区。[[paper]](https://doi.org/10.1145/3805712.3808466)

#### 带门控的巩固

*库的维护本身成为学习问题的一部分：重写、裁剪、验证或替换现役集合。*

- **Dynamic Cheatsheet** `EACL'26`：维护一份测试时持续整理的策略备忘。[[paper]](https://aclanthology.org/2026.eacl-long.333/)
- **ACE** `ICLR'26`：用增量式的 delta 更新扩展并巩固一份演化中的上下文手册，避免整体重写。[[paper]](https://openreview.net/forum?id=eC4ygDs02R)
- **SkillOpt** `arXiv'26`：修订后的技能集先在验证集上评估，再替换现役库。[[paper]](https://arxiv.org/abs/2605.23904)
- **SkillOpt-Lite** `arXiv'26`：同一道门的低成本版本，用一条带死区的验证规则加编译与冒烟测试接受技能编辑。[[paper]](https://arxiv.org/abs/2607.03451)
- **MemEvolve** `arXiv'25`：对记忆系统本身做元演化，每轮保留一个 top-1 Pareto 存活者。[[paper]](https://arxiv.org/abs/2512.18746)
- **Janus** `arXiv'26`：包住已有的更新器，当候选偏离近期更新方向时，在一个由覆盖、边界与新鲜任务组成的紧凑集合上比较旧记忆与候选记忆，再决定部署哪一个。[[paper]](https://arxiv.org/abs/2606.31121)
- **SWE-MeM** `arXiv'26`：为长周期编码 agent 学习自适应的记忆管理策略。[[paper]](https://arxiv.org/abs/2606.28434)
- **SWE-Pruner** `arXiv'26`：按一个调过的保留阈值做自适应上下文裁剪。[[paper]](https://arxiv.org/abs/2601.16746)
- **TACO** `arXiv'26`：面向终端 agent 的观测式上下文压缩，带写回门与一个无需奖励的保留停止条件。[[paper]](https://arxiv.org/abs/2604.19572)
- **SkillMOO** `arXiv'26`：用 NSGA-II 排序，在多个互相冲突的目标下选技能组合，而不是只看一个分数。[[paper]](https://arxiv.org/abs/2604.09297)
- **EffiSkill** `arXiv'26`：从验证过的代码对中挖掘效率技能，候选在公开划分上排序，报告用私有划分。[[paper]](https://arxiv.org/abs/2603.27850)
- **VASO** `arXiv'26`：可形式验证的技能，每个计划在运行前先对技能的规格做模型检查。[[paper]](https://arxiv.org/abs/2606.05395)
- **Memory Management** `ACL'26`：实证研究保留、删除与检索规则如何改变任务结果，并给出一个基于相似度的遵循度度量。[[paper]](https://aclanthology.org/2026.acl-long.27/)
- **Memory as Action** `ACL'26 Findings`：把上下文整理当成 agent 的一个动作来端到端训练，而不是由固定策略规定。[[paper]](https://aclanthology.org/2026.findings-acl.956/)
- **MCE** `ICML'26`：技能层面的 history-informed (1+1) 演化策略，带 agent 式交叉与一个验证档案。[[paper]](https://icml.cc/virtual/2026/poster/64296)
- **Living-Harness** `arXiv'26`：交互式 agent 演化器，跨周期把检索到的记忆巩固成一张可复用的图。[[paper]](https://arxiv.org/abs/2607.26598)

> **这一层的终点。**存下来的经验是数据，由模型按概率解释。一条有用的技能可能检索不到，检索到了也可能被忽略，[Harness Updating](#s31) 那一项里载入率与遵循率从 0.96 掉到 0.35。持久化存储同时把过时策略与注入载荷跨会话带下去，见[第 6 节](#s6)。

<a id="s13"></a>

### 1.3 工作流与拓扑

由**固定**编排框架执行的协调规格，包括角色分配、通信图、条件路由、验证与终止循环。节点实现与工具接口保持不变。

#### 固定流水线编译

*流水线由程序员定义，只搜索其中的文本参数。*

- **DSPy** `ICLR'24`：编译声明式的模型程序，优化提示与示例，控制流保持固定。[[paper]](https://openreview.net/forum?id=PFS4ffN9Yx)
- **MIPRO** `EMNLP'24`：在多阶段模型程序的各个阶段上，联合优化指令与示例。[[paper]](https://aclanthology.org/2024.emnlp-main.525/)

#### 图与拓扑搜索

*连接结构本身就是搜索空间。*

- **GPTSwarm** `ICML'24`：把固定算子之间的边变成可学习的，优化由此得到的通信图。[[paper]](https://arxiv.org/abs/2402.16823)
- **Mass** `ICLR'26`：在预定义的多 agent 模块上，联合搜索 agent 提示与通信拓扑。[[paper]](https://proceedings.iclr.cc/paper_files/paper/2026/hash/1ab4e0e8f35078109bc78d7b465d306f-Abstract-Conference.html)
- **MaAS** `ICML'25`：从一个由预定义算子构成的 agent 超网中，采样与查询相关的架构。[[paper]](https://proceedings.mlr.press/v267/zhang25bi.html)
- **AFlow** `ICLR'25`：把工作流序列化成组合可复用算子的代码，再在其上搜索结构与提示，算子实现本身不动。[[paper]](https://openreview.net/forum?id=z5uVAKwmjf)
- **AgentSquare** `ICLR'25`：在模块化设计空间中搜索模块组合，同时也生成新的模块实现。[[paper]](https://openreview.net/forum?id=mPdmDYIQ7f)

#### 反馈驱动的工作流修订

*决定下一个拓扑的是执行结果，不是搜索预算。*

- **SEW** `arXiv'25`：同时变异提示与拓扑，并比较不同的工作流表示方式。[[paper]](https://arxiv.org/abs/2505.18646)
- **JudgeFlow** `arXiv'26`：用块级别的裁判诊断来修订顺序块、循环块与条件块。[[paper]](https://arxiv.org/abs/2601.07477)
- **RHI** `arXiv'26`：在单个任务回合内，把成对反馈作用于角色、指令、通信契约与交互跳数。[[paper]](https://arxiv.org/abs/2607.15524)
- **Evolve as a Team** `arXiv'26`：跨任务携带经验，更新一套可复用脚手架，内容包括提示、队友画像与共享协调规则。[[paper]](https://arxiv.org/abs/2605.29790)
- **Symbolic Learning** `AI Open'25`：通过反向传播的语言损失，联合修订流水线结构、提示与工具。[[paper]](https://doi.org/10.1016/j.aiopen.2025.11.004)

> **边界说明。**AgentSquare 与 Symbolic Learning 也会生成可执行的模块与工具实现，列在这里是因为它们的主要贡献是模块化搜索与联合符号优化。它们额外带来的可执行可变面在 [2.1](#s21) 讨论。

---

<a id="s2"></a>

## 2. 可执行更新对象

*宿主或运行时直接执行这次修改。分类依据是被改动的对象，不是写它的文件格式。下面三个小节是**并列的软件边界**，不是能力等级，区别在于一次错误编辑能传播多远，以及挂载前必须满足什么契约。*

<a id="s21"></a>

### 2.1 工具与代码补丁

外围执行器固定，修改落在一个声明过的可执行单元上，可以是一个可调用工具、一份技能实现、一个函数或一个指定的组件文件。这条边界让测试与回滚局部化，但它不阻止错误经由该组件的输出或共享状态扩散出去。

#### 可调用工具合成

*把成功的执行变成可独立调用的代码。*

- **Voyager** `TMLR'24`：把自验证通过的程序变成不断生长的技能库，后续任务可检索并组合。[[paper]](https://openreview.net/forum?id=ehfRiF0R3a)
- **PolySkill** `arXiv'25`：归纳多态的技能抽象，让学到的技能能用在产生它的场景之外。[[paper]](https://arxiv.org/abs/2510.15863)
- **FlowEvo** `arXiv'26`：把一条成功的工作流编译成经验证的可调用产物存入持久技能库，之后既可直接执行，也可把它的结构描述交给工作流生成。[[paper]](https://arxiv.org/abs/2607.21596)
- **Live-SWE-agent** `arXiv'25`：运行时临时生成 Bash 与 Python 工具，这些工具随任务容器一起销毁，因此它展示了工具合成，但没有持久的 harness 演化。[[paper]](https://arxiv.org/abs/2511.13646)
- **RoboPhD** `arXiv'26`：让一个确定性的 Python 分析工具与模型可读的 SQL 指令共同演化，交付时这对产物不再依赖演化基础设施。[[paper]](https://arxiv.org/abs/2601.01126)

#### 以证据为依据的组件修补

*执行证据选中一个已声明的组件，外围 agent 循环不对修改开放。这些系统的主要差别在**准入程序**。*

- **Self-Harness** `arXiv'26`：从同一个现役版本提出多个编辑，只有在两个划分上都不下降、且至少一个上升时才晋升。[[paper]](https://arxiv.org/abs/2606.09498)
- **HarnessCompass** `arXiv'26`：分别优化 harness 的各个组件再组合，在 50 个演化任务上排序，另外 450 个留出任务单独报告。[[paper]](https://arxiv.org/abs/2608.01918)
- **AHE** `arXiv'26`：以可观测性驱动演化，每次运行的提交信标与 shell 层记录为每个上线编辑提供依据，有害时按文件粒度回滚。[[paper]](https://arxiv.org/abs/2604.25850)
- **HarnessFix** `arXiv'26`：从失败轨迹诊断 harness 故障，修复只能经由验证集评估才被接受。[[paper]](https://arxiv.org/abs/2606.06324)
- **ReCreate** `ACL'26`：在一个小规模开发集上，于文本与代码两个层面编辑角色、流程、工具与记忆组件，明确排除执行环境与系统基础设施的适配。[[paper]](https://aclanthology.org/2026.acl-long.1432/)
- **AutoSaddler** `arXiv'26`：只在小批量上有增益时保留补丁，在开发集上取最优，并且按组不相交的测试集只评一次。[[paper]](https://arxiv.org/abs/2608.23041)
- **CHASE** `arXiv'26`：反事实引导的 harness 演化，Challenger 提出意图摧毁候选相对父版本增益的协议变换，只有增益在档案中每个已确认变换下都存活，补丁才被接受。[[paper]](https://arxiv.org/abs/2609.18366)
- **Evo-Harness** `arXiv'26`：沿在线任务流把累积的上下文编译成 harness 层面的技能，并把失败转成功的轨迹与技能内容对应起来。[[paper]](https://arxiv.org/abs/2608.15071)
- **HarnessBank** `arXiv'26`：MAP-Elites 风格的基因库，用语义描述符分区，每次尝试记录激活信标，配对显著性门把关，从不触发的精英被淘汰。[[paper]](https://arxiv.org/abs/2607.13683)
- **Ecdysis** `arXiv'26`：训练运行时 harness，晋升只看训练目标，冻结后的 harness 在留出划分上评分。[[paper]](https://arxiv.org/abs/2609.11677)

<a id="s22"></a>

### 2.2 仓库与运行时逻辑

端到端的控制程序变成可变对象。一次修改可以跨越组件边界，改动上下文构造、工具分发、验证与恢复、agent 循环，甚至改动提出后续修改的那段代码。载体可以是单个程序、多文件仓库或活进程内存，定义性质是**若干 harness 功能可以一次性被重新组合**。

#### 整体控制程序搜索

*固定的外层循环合成整个控制程序。三者都是离线优化前身，产物是一个被选出来准备部署的 harness，而部署后的 harness 不再继续更新。*

- **ADAS** `ICLR'25`：固定的元 agent 写出新的 agent `forward` 实现，评估过的候选存入档案。[[paper]](https://openreview.net/forum?id=t9U3LW7JVX)
- **Meta-Harness** `COLM'26`：把历史候选的源码、分数与轨迹交给一个外部编码 agent，要求它合成完整的任务专用 harness 程序。[[paper]](https://arxiv.org/abs/2603.28052)
- **RRSI** `arXiv'26`：对同样的搜索加正则，包括退火的编辑预算、泄漏筛查与按噪声调整的接受下限，用演化集上的增益换分布外迁移。[[paper]](https://arxiv.org/abs/2609.24972)

#### 仓库修订

*编辑一份纳入版本管理的 harness 实现。档案成员身份只标明谁可以参与后续演化，不意味着任何存档版本会成为现役运行时。*

- **SICA** `arXiv'25`：把自己的多文件 Python 代码库，包括工具、子 agent 与控制流，交给档案中表现最好的 agent 修改。[[paper]](https://arxiv.org/abs/2504.15228)
- **DGM** `ICLR'26`：把仓库变体分叉进一个开放式档案，父代选择兼顾性能与新颖性。[[paper]](https://openreview.net/forum?id=pUpzQZTvGY)
- **DarwinX** `arXiv'26`：以自然选择演化 harness，训练划分在留出划分被动用之前就已冻结。[[paper]](https://arxiv.org/abs/2608.07545)
- **HGM** `arXiv'25`：估计谱系层面的产出能力，用 Thompson 采样分配谱系扩展与候选评估的预算。[[paper]](https://arxiv.org/abs/2510.21614)
- **Group-Evolving Agents** `arXiv'26`：让被选中的父代先共享代码补丁、工具与执行经验，再产出框架层面的补丁。[[paper]](https://arxiv.org/abs/2602.04837)
- **MOSS** `arXiv'26`：重写路由、钩子、状态管理与分发代码，再在健康检查加人工授权之后替换容器。[[paper]](https://arxiv.org/abs/2605.22794)
- **Ouroboros** `arXiv'26`：通过经评审的提交演化自己的核心，配有运行清单、种子证明与公开的逐任务轨迹。[[paper]](https://arxiv.org/abs/2608.08311)
- **AgentDevel** `arXiv'26`：把自演化重构为发布工程，包括版本化 diff、候选版本回归测试、逐轮的失败转成功与成功转失败记录。[[paper]](https://arxiv.org/abs/2601.04620)
- **EvolveNet** `arXiv'26`：跨客户端协同演化 harness，经一道不相交验证门后，把合并的补丁作为共享状态广播。[[paper]](https://arxiv.org/abs/2608.04968)

#### 进程内修补

*修改作用于正在运行的进程，不写回仓库。*

- **Gödel Agent** `ACL'25`：用 monkey patching 替换活 Python 内存中的决策方法、动作空间与自我修改例程，修改随进程结束而消失。[[paper]](https://aclanthology.org/2025.acl-long.1354/)
- **TTHE** `arXiv'26`：测试时从执行轨迹演化出可执行的 harness 程序，并把选中的程序带入后续输入。[[paper]](https://arxiv.org/abs/2607.08124)
- **Life-Harness** `arXiv'26`：同时适配环境契约、动作实现与轨迹调控，随后冻结运行时接口做评测。[[paper]](https://arxiv.org/abs/2605.22166)

<a id="s23"></a>

### 2.3 一切皆插件

可执行组件放在一个固定微内核、一组声明接口与生命周期钩子之后。可变对象是插件实现，或是把工具、记忆、模型提供方、agent 循环与验证器绑定进运行时的那份组合。**这一类的贡献不是更大的可变半径，而是围绕替换与激活的更明确契约**，由内核决定存在哪些钩子、哪些依赖合法、一个组件可以如何被挂载。

#### 契约驱动的钩子

- **HarnessX** `arXiv'26`：提交一份候选配置前先检查钩子类型、单例约束与冒烟测试，并要求每个编辑声明它生效时必然出现的轨迹特征。[[paper]](https://arxiv.org/abs/2606.14249)
- **Argus** `arXiv'26`：通用的 agent 推理运行时，技能被暴露而非注入，沿长周期任务流演化。[[paper]](https://arxiv.org/abs/2608.05144)

#### 微内核平台

- **DeepSeek Harness** `产品'26`：Cordis 内核通过声明依赖连接运行时组件，追加式记录支持检查点与回放。它展示的是执行载体，不是一个有报告的自演化闭环。[[page]](https://www.deepseek.com/harness/en/)
- **Cordis / Spatiotemporal Composability** `arXiv'26`：该内核背后的形式演算，自演化 harness 被列为未来工作。[[paper]](https://arxiv.org/abs/2608.25512)
- **Autogenesis** `arXiv'26`：自演化 agent 协议，带显式的提出、评估、提交周期，以及谱系与版本记录。[[paper]](https://arxiv.org/abs/2604.15034)
- **ModularRSI** `arXiv'26`：在一个 composer 之后演化模块，用对奖励不可见的门把关，演化任务由外部整理且与基准不相交。[[paper]](https://arxiv.org/abs/2609.14857)

> **契约买不到什么。**沙箱可以限制权限，带类型的钩子可以拒绝不兼容的绑定，但两者都不能说明产生的行为是正确的。在运行时管理的状态范围内，检查点与组件替换可以恢复到之前的逻辑配置，却无法撤回已经发到边界之外的 API 请求、数据库写入、对外消息或物理动作。这些只能靠事前阻止、幂等操作或补偿动作处理，回滚不解决。

---

<a id="s3"></a>

## 3. 评测与基准

一个终端任务分数混在一起的是**四个互相依赖的 claim**。其中一个成立不能推出另一个成立，而缺了前面的 claim，后面的就无法解读。

![评测 harness 自演化](assets/claims.png)

| Claim | 问题 | 什么时候会无声失效 |
|---|---|---|
| **Selection（择优）** | 报告出的那个状态，是否在没有花掉报告所用证据的前提下被选中的？ | 候选在某批任务上排第一，随后又在同一批任务上被报告；一个号称 held-out 的划分同时是晋升规则的输入；在没有事先定好停止规则的情况下报告轨迹的峰值轮。 |
| **Activation（激活）** | 被接受的产物或代码路径，在产生报告分数的那些运行里真的生效了吗？ | 技能被载入却被忽略；组件确实运行了，但它的输出在拼装提示时被丢掉，或者被上下文截断切走。持久化不等于激活。 |
| **Attribution（归因）** | 观察到的差异确实来自那个状态吗？ | 真正动的是执行波动、随更新一起变大的资源开销（重试、验证器调用、更长上下文），或者漂移的评测器。 |
| **Improvement（改进范围）** | 这个差异能延伸多远？ | 只在产生它的那些任务上测过；或者在采纳它的那一轮记过一次功，之后再没复查。 |

三个激活率，关键信息在分母上。`R(u)` 是更新 `u` 适用的那些执行，`L(u)` 是其中载入了它的，`B(u)` 是其中信标触发的，`F(u) ⊆ L(u)` 是轨迹确实遵循它的。

```
load(u)   = |L(u)| / |R(u)|          # 可用
reach(u)  = |B(u)| / |R(u)|          # 被改动的路径执行了
adhere(u) = |F(u)| / |L(u)|          # 轨迹遵循了它
```

下面的工作按**它们承担的证据功能**归类，不按基准家族归类。

<a id="s31"></a>

### 3.1 按 claim 划分的证据

#### 择优与准入

- **RSEA** `arXiv'26`：通过显式的留出式择优，把数据分配给候选生成、准入与报告三个环节。[[paper]](https://arxiv.org/abs/2606.28374)
- **Anytime Certificates** `arXiv'26`：为反复依赖数据的准入决策提供 anytime-valid 证书。[[paper]](https://arxiv.org/abs/2607.00871)
- **Phantom Guardrails** `arXiv'26`：记录自改进 harness 修复了从未发生过的故障，补丁没有任何观测到的执行作为依据。[[paper]](https://arxiv.org/abs/2607.13083)
- **Harness Tampering** `arXiv'26`：审计那些修改验证逻辑而不是修改被测行为的候选。[[paper]](https://arxiv.org/abs/2609.00069)
- **Self-Authored Verification** `arXiv'26`：发现在启发式自改进 agent 中，自己写的检查不足以作为准入证据。[[paper]](https://arxiv.org/abs/2607.24300)
- **SWE-bench+** `arXiv'24`：记录了解法泄漏与弱断言，它们同时污染晋升与报告。[[paper]](https://arxiv.org/abs/2410.06992)

> **结构性的那一种失效。**报告分数被花掉有三种统计形态，花在划分上、花在门上、花在轮次上。第四种性质不同，是候选去塑造了判它的那份记录，统计手段对它无效。HarnessBank 把评测与记账代码放进候选改不了的内核，HarnessX 先打参考测试补丁再打模型补丁，并禁止写入测试文件。

#### 运行时激活

- **SkillsBench** `arXiv'26`：在多样任务上记录任务提供的技能是否被读取或引用。[[paper]](https://arxiv.org/abs/2602.12670)
- **Harness Updating ≠ Harness Benefit** `arXiv'26`：分别统计载入率与轨迹遵循率，两个 agent 载入率为 0.961 与 0.957，遵循率只有 0.350 与 0.757，且遵循度沿轨迹衰减。[[paper]](https://arxiv.org/abs/2605.30621)

#### 归因控制

*每一项都指出一种途径，让报告出的差异来自更新之外的东西。*

- **Agents That Matter** `TMLR'25`：指出 agent 比较把能力与成本混在一起，要求做成本受控的评测。[[paper]](https://arxiv.org/abs/2407.01502)
- **Token Cost** `arXiv'26`：分析并预测 agent 的 token 消耗，给资源开销一个可测的单位。[[paper]](https://arxiv.org/abs/2604.22750)
- **MLE-bench** `ICLR'25`：机器学习工程任务，带重复运行与显式的算力开销。[[paper]](https://arxiv.org/abs/2410.07095)
- **AgentRewardBench** `COLM'25`：用专家标注对网页 agent 轨迹的自动裁判做元评测。[[paper]](https://arxiv.org/abs/2504.08942)
- **Judge Inflation** `arXiv'24`：记录迭代自我精修中自发出现的 reward hacking。[[paper]](https://arxiv.org/abs/2407.04549)
- **Memory Reward Inflation** `arXiv'26`：说明存下来的记忆可以抬高报告出的奖励，而行为并未变好。[[paper]](https://arxiv.org/abs/2608.00017)
- **Who Grades the Grader** `arXiv'26`：指标与技能共同演化时，上升的分数无法说明动的是哪一个。[[paper]](https://arxiv.org/abs/2607.12790)
- **Don't Blame the LLM** `arXiv'26`：把测到的编码 agent 差异归到 harness 演化上，而不是模型上。[[paper]](https://arxiv.org/abs/2607.03691)
- **Scaffold Effect** `arXiv'26`：把 harness 选择当作编码 agent 比较中的一个隐藏变量。[[paper]](https://arxiv.org/abs/2607.22585)
- **Rethinking Harness Evaluation** `arXiv'26`：论证当前协议让报告出的 harness 演化增益处于失控状态。[[paper]](https://arxiv.org/abs/2607.12227)
- **HAL** `ICLR'26`：把标准化的运行记录、模型快照与成本记账做成共享评测基础设施。[[paper]](https://proceedings.iclr.cc/paper_files/paper/2026/file/a0928f924a344aaebbb7f6cd8d56e34c-Paper-Conference.pdf)

#### 改进范围与保留

- **Claw-Eval** `arXiv'26`：把"重新解决掉触发更新的那个失败"与"增益确实延伸得更远"区分开。[[paper]](https://arxiv.org/abs/2604.06132)
- **PATH-Bench** `arXiv'26`：路径相关的评测，刻意变动任务顺序并保留冻结的参照历史。[[paper]](https://arxiv.org/abs/2608.01149)
- **HarnessOpt-Bench** `arXiv'26`：带留出划分与经审计资源用量，测量端到端的 harness 优化。[[paper]](https://arxiv.org/abs/2608.06301)
- **HarnessDev** `arXiv'26`：把 harness 的*创建*与迭代*演化*分开，报告能力、成本与留出迁移。[[paper]](https://arxiv.org/abs/2609.01437)

<a id="s32"></a>

### 3.2 纵向与动态证据

持续自演化不增加第五个 claim，它要求同样这四个在**每一次**被接受的更新之后重新成立，而且是在两种漂移之下：harness 每轮都变，任务流或基准也可能同时在变。

<details>
<summary><b>把一次性评测扩展成纵向审计的七项控制</b></summary>

| Claim | 控制项 | 需要记录什么 | 排除了什么混淆 |
|---|---|---|---|
| Selection | 证据分离 | 哪些任务与信号分别用于生成、排序、准入与冻结后的报告，包括报告了哪一轮 | 自适应反馈泄漏，以及择优之后再报告 |
| Selection | Oracle 完整性 | 打分、验证与记账代码位于候选可编辑范围之外 | 更新系统对指标的利用 |
| Activation | 激活记录 | 逐任务逐尝试地记录：产物可用、路径执行、轨迹遵循 | 把从未生效的更新记成功劳 |
| Attribution | 执行波动 | 对冻结检查点重复执行，并把差距读在这个经验离散度上，而不是读在零上 | 把采样噪声当成系统性进步 |
| Attribution | 声明算力开销 | token、模型与验证器调用、工具执行、重试、墙上时间、候选数，包括那些不改动任何声明上限的增长 | 把增加的推理算力当成 harness 增益 |
| Attribution | 模型快照记录 | 模型标识与版本或快照、解码参数，以及窗口期内服务端的任何变更 | 把服务端模型变更当成 harness 增益 |
| Improvement | 受控历史 | 变动的任务顺序、冻结的参照历史、对闭环不控制的更早分布做探针，以及在记功之后若干轮再复查一次 | 把课程效应当成迁移或保留，把一次性增益当成常驻性质 |

每项控制买到的东西都比它的名字少。打乱任务顺序测的是课程敏感性，不是迁移。历史探针只在它的结果还没开始指导后续更新之前才测的是保留。这些都不能让一条被自适应复用的任务流恢复独立性。

</details>

#### 现役集合的完整性

*更新一旦累积，激活就成了移动靶，后来的修改会改变哪些产物仍可达、仍被优先选中、仍被遵循。*

- **Ratchet** `arXiv'26`：追问一个 LLM 裁判要多可靠，才够资格让一项技能退役。[[paper]](https://arxiv.org/abs/2605.22148)
- **SkillsVote** `arXiv'26`：对技能做全生命周期治理，涵盖收集、推荐与基于投票的整理。[[paper]](https://arxiv.org/abs/2605.18401)
- **Library Drift** `arXiv'26`：诊断并修复不断变大的自演化技能库中的无声漂移。[[paper]](https://arxiv.org/abs/2605.19576)
- **Pre-Commit Gating** `arXiv'26`：在提交前阻断技能污染，并说明自演化什么时候会反噬。[[paper]](https://arxiv.org/abs/2608.05810)
- **EVOMAL** `arXiv'26`：记录自演化编码 agent 的自我投毒现象。[[paper]](https://arxiv.org/abs/2608.25776)

#### 合成边界任务

*从已有实例或诊断出的失败派生新实例。由于生成器与候选更新可能读到同一批轨迹，这个重叠必须记录下来。*

- **Benchmark Self-Evolving** `arXiv'24`：多 agent 框架，从已有实例派生新实例做动态评测。[[paper]](https://arxiv.org/abs/2402.11443)
- **StressEval** `arXiv'26`：失败驱动的动态基准，从诊断出的失败生成实例。[[paper]](https://arxiv.org/abs/2605.01939)

#### 时间流

*只收录某个截止日期之后发布的任务。更晚的发布日期能降低直接重叠，但不能让不同批次的难度相等，也不能证明相关题型在早期开发中不存在。*

- **LiveBench** `ICLR'25 Spotlight`：污染受限的基准，从截止日期之后的来源刷新，带客观答案。[[paper]](https://arxiv.org/abs/2406.19314)
- **LiveCodeBench** `arXiv'24`：截止日期之后收集的带时间戳竞赛编程题。[[paper]](https://arxiv.org/abs/2403.07974)
- **LiveMedBench** `arXiv'26`：带自动刷新的无污染医学基准。[[paper]](https://arxiv.org/abs/2602.10367)
- **SWE-rebench** `arXiv'25`：自动化的任务收集与去污染评测流水线。[[paper]](https://arxiv.org/abs/2505.20411)
- **SWE-bench Live** `arXiv'25`：由新合并的 issue 持续刷新的 SWE-bench。[[paper]](https://arxiv.org/abs/2505.23419)

#### 对抗式自博弈

*挑战分布随参与者一起移动，因此 harness、任务生成器与评测器必须分开报告，单个数字说不清是哪一个动了。*

- **MathDuels** `COLM'26`：随参与者池一起增长的自博弈基准。[[paper]](https://arxiv.org/abs/2604.21916)
- **Red Queen Gödel Machine** `arXiv'26`：在同一个闭环里共同演化 agent 与它们的评测器。[[paper]](https://arxiv.org/abs/2606.26294)

#### 终身学习测试床

*一个序列化基准只有在观测到**状态转移**时才构成 harness 演化的证据，按时间排好的分数列表不够。*

- **LifelongAgentBench** `arXiv'25`：在技能相互依赖的任务序列上，把 agent 当作终身学习者评测。[[paper]](https://arxiv.org/abs/2505.11942)
- **PAST-Bench** `arXiv'26`：评测个人 agent 的 RSI 基础，对比开启与关闭持久化两种条件。[[paper]](https://arxiv.org/abs/2608.04003)
- **SEA-Eval** `arXiv'26`：超出单回合评估地评测自演化 agent。[[paper]](https://arxiv.org/abs/2604.08988)
- **FinEvo-Bench** `arXiv'26`：金融专业场景的纵向基准，带匹配的持久化开关条件。[[paper]](https://arxiv.org/abs/2608.06144)
- **ContinualSkillBench** `arXiv'26`：追问 agent 在连续任务流上是否真的演化出了能力。[[paper]](https://arxiv.org/abs/2608.03874)
- **SkillFlow** `arXiv'26`：评测终身的技能发现与演化。[[paper]](https://arxiv.org/abs/2604.17308)
- **SkillLearnBench** `arXiv'26`：评测用于 agent 技能生成的持续学习方法。[[paper]](https://arxiv.org/abs/2604.20087)
- **MemoryArena** `arXiv'26`：相互依赖的多会话任务，早先的写入会影响后续工作。[[paper]](https://arxiv.org/abs/2602.16313)
- **Evo-Memory** `arXiv'25`：评测带自演化记忆的测试时学习。[[paper]](https://arxiv.org/abs/2511.20857)
- **Tool-Genesis** `arXiv'26`：面向自演化 agent 的任务驱动工具创建基准。[[paper]](https://arxiv.org/abs/2603.05578)
- **EvoCodeBench** `arXiv'26`：自演化代码 agent 的人类水平参照基准。[[paper]](https://arxiv.org/abs/2602.10171)
- **SWE-EVO** `arXiv'25`：编码 agent 的长周期软件演化场景。[[paper]](https://arxiv.org/abs/2512.18470)
- **GDPevo** `arXiv'26`：在真实业务任务上评测 agent 自演化。[[paper]](https://arxiv.org/abs/2608.03764)
- **CL-Bench** `arXiv'26`：真实有状态持续学习场景下的前沿系统评测。[[paper]](https://arxiv.org/abs/2606.05661)
- **EvoHarnessBench** `arXiv'26`：隔离出所给 harness 的非平稳性，在能力不断加入时检验保留。[[paper]](https://arxiv.org/abs/2609.04280)

> **交叉评测。**拿 `H_t` 在快照 `D_A` 上的结果去比 `H_{t+1}` 在 `D_B` 上的结果，会把 harness 漂移与基准漂移混在一起。应当在同一套打分程序下，让两个状态都跑两个快照，这样同一快照内的差异归于 harness 状态，同一状态内的差异归于快照。如果任意一个快照已经参与过候选生成或准入，交叉也恢复不了独立性。完整交叉成本过高时，可以在相邻快照之间保留一组版本化的锚定任务，只交叉评测选定的检查点，并报告所选的覆盖范围与重复次数。

---

<a id="s4"></a>

## 4. 理论

表达能力不是瓶颈，用图灵完备语言写的 harness 原则上可以表达任意可计算的控制逻辑。真正的约束是**这样一个程序怎么被搜索**，以及**它的评测能支持什么**。改进依靠目标评测与 rollout 反馈而非梯度，所以 harness 搜索属于程序空间上的零阶优化。

> 这一节是唯一会重新列出第 1、2 节系统的地方，因为这里的贡献就是这组对应关系本身。

<a id="s41"></a>

### 4.1 演化算法对应

| EA 范式 | 对应范围 | 系统 |
|---|---|---|
| 精英 (1+1) 与演化策略 | 单个候选与现役版本比较；MCE 明确采用 history-informed (1+1)-ES，其余系统共享它的择优结构 | SICA · MCE · SkillOpt · SkillOpt-Lite · SkillClaw |
| 精英 (1+λ) 风格 | 从同一现役版本提出多个编辑，接受前先评估；把兼容的编辑合并与标准 (1+λ)-ES 的存活者选择不同 | Self-Harness |
| 档案式程序搜索 | 程序充当个体，搜索由父代选择、代码修改与谱系保留组织；这是程序层面的 EA 对应，不是经典树状 GP 算子 | DGM · DarwinX · HGM |
| 重组与交叉 | 跨候选组合互补内容；Trace2Skill 只提供补丁合并层面的类比，没有完整的演化择优闭环 | DarwinX · HarnessCompass · Self-Harness · MCE · Trace2Skill |
| 质量多样性与 MAP-Elites | 语义描述符把档案划分成格子，每格保留精英；HarnessBank 改动了父代选择并加了验证门 | HarnessBank |
| 协同共演化 | 先按组件优化再组合，对应关系有限，因为没有显式维护独立演化的子种群 | HarnessCompass |
| 多目标 EA 的 Pareto 择优 | 性能与成本的前沿，或多准则接受门，类似 Pareto 择优；这是择优层面的对应，不是 NSGA-II 的实现 | Meta-Harness · Self-Harness · SkillMOO |
| bandit 引导的演化 | Thompson 采样分配谱系扩展与候选评估的预算 | HGM |

**共同的局限。**演化择优作用在*观测到的*适应度上。保留一个经验上更好的候选，既不能说明它在未见任务上更好，也不能说明早先获得的能力被保住了。

<a id="s42"></a>

### 4.2 PAC 学习与稳定性

#### 稳定性与保留

- **Learnability, Stability and Uniform Convergence** `JMLR'10`：把算法对单个样本的敏感度与它的泛化差距联系起来。[[paper]](https://www.jmlr.org/papers/v11/shalev-shwartz10a.html)
- **Memory Bounds for Continual Learning** `FOCS'22`：给出持续学习所需记忆的下界，说明泛化与保留应当合在一起处理。[[paper]](https://arxiv.org/abs/2204.10830)

在任务抽样外生且独立的假设下，稳定性论证给出 `|E[R_s(H_t) − R̂_s(H_t)]| ≤ β_{s,t}`，保留的分解给出 `E R_s(H_t) ≤ E R̂_s(H_s) + β_{s,s} + E F_{s,t}`，其中 `F_{s,t} ≤ Σ_u ε_{s,u}`，也就是说**即使每轮只容忍很小的回退，跨轮也会累积**。抽象与小改动本身并不界定 `β`，单个样本仍可能改掉一条共享规则或改掉被选中的谱系。

#### 置信度门控的准入

- **Hoeffding Bounds** `JASA'63`：有界损失上配对准入门背后的集中不等式。[[paper]](https://doi.org/10.1080/01621459.1963.10500830)
- **Selection Overfitting** `JMLR'10`：模型择优中的过拟合，以及它留在报告性能里的择优偏差。[[paper]](https://jmlr.org/papers/v11/cawley10a.html)
- **The Reusable Holdout** `Science'15`：在反复依赖数据的决策中保持留出集的有效性。[[paper]](https://doi.org/10.1126/science.aaa9375) · [[companion]](https://arxiv.org/abs/1506.02629)
- **SkillForge** `SIGIR'26 Industry`：留出一个时间尾段分区，使报告出的数字不是门已经消耗掉的那个。[[paper]](https://doi.org/10.1145/3805712.3808466)

只有在 `Δ̂_t(H′) + sqrt(2 ln(KT/δ) / m) < 0` 时才接受候选，可以在该轮的任务混合上保证改进。这个条件偏保守，并且只适用于**被评估的那个候选**，不适用于未测试的合并，也不适用于看过验证集之后再做的修改。独立单位是*任务*，对同一任务重复执行能降低执行噪声，但不产生新的独立证据。

#### 自改进的上界

- **Harness Evolution as Learning** `arXiv'26`：自改进个人 agent 的逼近、泛化与优化上界。[[paper]](https://arxiv.org/abs/2609.36892)
- **A Theory of Reliable Self-Evolution** `arXiv'26`：推导采纳条件，其上限由验证与评测成本决定。[[paper]](https://arxiv.org/abs/2609.08175)

<a id="s43"></a>

### 4.3 背景统计与优化工具

*与 harness 无直接关系，也不属于论文分类，是上面那些问题借用的分析工具。*

- **The Ladder** `ICML'15`：在反复自适应提交之下仍然可靠的排行榜机制。[[paper]](https://arxiv.org/abs/1502.04585)
- **Train Faster, Generalize Better** `ICML'16`：以 SGD 的稳定性推导泛化界。[[paper]](https://arxiv.org/abs/1509.01240)
- **PAC-Bayes for Prompts** `arXiv'23`：提示工程也许不需要重新思考泛化。[[paper]](https://arxiv.org/abs/2310.03957)
- **ZOPO** `arXiv'24`：局部化的零阶提示优化。[[paper]](https://arxiv.org/abs/2403.02993)
- **Statistical Limits** `TMLR'26`：自改进 agent 的统计上限。[[paper]](https://arxiv.org/abs/2510.04399)
- **AdaEvolve** `arXiv'26`：自适应的、由大模型驱动的零阶优化。[[paper]](https://arxiv.org/abs/2602.20133)
- **GAMBLe** `arXiv'26`：AI 驱动研究系统的分析框架。[[paper]](https://arxiv.org/abs/2606.02863)
- **Mutation Without Variation** `arXiv'26`：大模型驱动程序演化中的收敛动力学。[[paper]](https://arxiv.org/abs/2606.05408)
- **What Fits Doesn't Overfit** `arXiv'26`：机器学习研究 agent 中的压缩与泛化。[[paper]](https://arxiv.org/abs/2606.11045)
- **IMABO** `arXiv'26`：推理时的 bandit 超参优化。[[paper]](https://arxiv.org/abs/2609.01335)

---

<a id="s5"></a>

## 5. 96 个方法的证据审计

第 1、2 节中的每个方法都按四个 claim 读过原始文献。**逐篇判定、评分标准与每格的依据在 [`docs/claim-audit.md`](docs/claim-audit.md)。**

| Claim | ✅ 充分 | ◐ 部分 | — 缺失 |
|---|---:|---:|---:|
| Selection | 26 | 56 | 12 |
| Activation | 33 | 60 | 1 |
| Attribution | 53 | 38 | 3 |
| Improvement | 57 | 23 | 14 |

*96 个方法中 94 个计入评分，另 2 个没有任何实证评测。四列的长度**不可**互相比较：Selection 的"充分"是三个条件的合取，Improvement 的"充分"是三个索引上的析取。所以这个排序既反映各条标准有多严，也反映领域报告得有多仔细。*

**同一篇报告里有几个 claim 达到充分**，因为结论止于它最早失守的那个 claim：

| 0 项 | 1 项 | 2 项 | 3 项 | 4 项 |
|---:|---:|---:|---:|---:|
| 13 | 29 | 22 | 24 | **6** |

三条值得直说的结论。

1. **激活通常是从"存下来了"推出来的。**它几乎从不完全缺失（94 篇里只有 1 篇），也很少真正被确立（33 篇）。产物被证明*在场*是常规操作，被证明*支配了运行*则很少见。
2. **Selection 拿到充分的最少**（94 篇里 26 篇），报告分数反复被花在划分、门或轮次上。
3. **轮次这个索引是空的。**57 篇拿到 Improvement 充分的报告里，除两篇外全都基于留出或迁移划分，而且都读在*采纳更新的那一轮*。**没有一篇复查过某个记过功的增益在更晚的轮次是否还在。**

程序细节披露得最多的五个系统：

| 系统 / 对象 | Sel. | Act. | Att. | Imp. | 操作性证据 | 最弱的一环 |
|---|:-:|:-:|:-:|:-:|---|---|
| **HarnessBank** · harness 面 | ✅ | ✅ | ✅ | ✅ | 不可修改的内核与留出测试集；每次尝试的信标；对父版本做配对 *z* 检验，并带一个非对角反事实 | [Att.] 开销声明在 2.1 倍以内，未对齐 |
| **AHE** · 工作流与代码 | — | ✅ | ✅ | ✅ | 每次运行的提交与 shell 块信标；每次只换入一层演化结果；冻结后迁移到 SWE-bench Verified | [Sel.] 最优轮次是在演化集上选的 |
| **Self-Harness** · harness 编辑 | ◐ | ✅ | ◐ | ◐ | 双划分晋升规则；注入的中间件回合在轨迹中可见 | [Sel.] 留出划分被门复用 |
| **HarnessX** · 代码与工作流 | — | ✅ | ◐ | — | 声明的轨迹特征；同配置回放 | [Sel.] 峰值轮次报告在演化集上 |
| **MOSS** · 已部署镜像 | ◐ | ◐ | ◐ | — | 对替换后的镜像做健康探针；每任务三次试验 | [Sel.] 演化批次被当成测试集复用 |

<sub>✅ 具备该 claim 所要求的那类证据 · ◐ 部分 · — 不支持。*最弱的一环*是支撑最薄的那个最早 claim；HarnessBank 这一格是残留限制，不是缺口。</sub>

---

<a id="s6"></a>

## 6. 持久状态带来的风险

*保留下来的状态构成无状态 agent 没有的攻击面。这些工作不在四分支分类内，它们说明持久化的代价，而不是它更新了什么。*

- **Bad Memory** `arXiv'26`：评估经由 agent 记忆进入的提示注入风险。[[paper]](https://arxiv.org/abs/2607.14611)
- **From Untrusted Input to Trusted Memory** `arXiv'26`：系统研究针对 LLM agent 的记忆投毒攻击。[[paper]](https://arxiv.org/abs/2606.04329)
- **SoftSkill** `arXiv'26`：面向上下文适配的行为压缩，同时提示一件事，存下来的技能是按概率解释的数据，不是被强制的规则。[[paper]](https://arxiv.org/abs/2606.20333)
- **AgentDojo** `NeurIPS'24 D&B`：提示注入攻防的动态环境，界定了外部影响一旦发出，回滚还能撤回什么。[[paper]](https://openreview.net/forum?id=m1YYAQjO3w)
- **AgentHarm** `ICLR'25`：度量 LLM agent 有害行为的基准。[[paper]](https://proceedings.iclr.cc/paper_files/paper/2025/hash/c493d23af93118975cdbc32cbe7323f5-Abstract-Conference.html)

---

<a id="s7"></a>

## 7. 已部署的 harness 与产品接口

*它们跨会话保留状态并标出了更新对象，但没有报告反馈驱动的更新闭环，所以列在这里而不进分类。作为"接口实际暴露了什么"的事实依据很有用。*

- **Claude Code memory**：作为会话上下文载入的项目记忆文件。[[docs]](https://code.claude.com/docs/en/memory)
- **Agent Skills**：打包成文件、可跨运行复用的技能。[[post]](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- **Gemini CLI auto memory**：CLI 中的自动记忆捕获。[[docs]](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/auto-memory.md)
- **GitHub Copilot memory**：编码 agent 的持久记忆。[[docs]](https://docs.github.com/en/copilot/concepts/agents/copilot-memory)
- **Building Effective AI Agents**：上面这些产品默认使用的 harness 设计术语来源。[[post]](https://www.anthropic.com/engineering/building-effective-agents)
- **Effective Context Engineering for AI Agents**：为什么不断累积的指令集是一个预算问题。[[post]](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

---

<a id="sbound"></a>

## 边界情形与排除范围

| 工作 | 为什么不在分类里 |
|---|---|
| **Harness-of-Harness** `arXiv'26` [[paper]](https://arxiv.org/abs/2609.01481) | 多日自主开发，规划、编码与测试修订的是*任务的*软件产物，harness 与模型的配置保持不变。没有 harness 修改，不满足范围条件。 |
| **Live-SWE-agent**（已收录，带标注） | 工具按任务合成并随容器销毁，有工具合成，没有持久性。 |
| **Gödel Agent**（已收录，带标注） | 修补活进程内存，修改支配后续决策步，但进程结束即消失。 |
| **已部署产品**（见[第 7 节](#s7)） | 状态跨会话保留，但没有报告反馈驱动的更新闭环。 |
| **Self-Refine / Self-Debug 一类** | 纠错在同一次 rollout 内部被消费。 |
| **SPIN / TTRL / self-rewarding LM** | 权重侧更新，违反模型固定前提。 |

---

<a id="ssurvey"></a>

## 相关综述

近期综述对这条生命周期的覆盖情况。✅ 有专门小节并综述多个方法 · ◐ 有实质讨论但无专门处理（含未来工作）· — 除表格条目或一句带过之外没有正文处理。

| 维度 | [Gao](https://arxiv.org/abs/2507.21046) | [Fang](https://arxiv.org/abs/2508.07407) | [Zhou-E](https://arxiv.org/abs/2604.08224) | [Ning](https://arxiv.org/abs/2605.18747) | [Chen](https://arxiv.org/abs/2607.07663) | [Ren](https://arxiv.org/abs/2607.13104) | [Zhou-C](https://arxiv.org/abs/2608.03392) | **本文** |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| *范围：*骨干模型固定 | — | — | ◐ | — | — | ◐ | ◐ | ◐ |
| *对象：*指令与提示 | ✅ | ✅ | ◐ | — | — | ✅ | ✅ | ✅ |
| *对象：*上下文与记忆 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| *对象：*工作流与控制 | ✅ | ✅ | ◐ | ✅ | ◐ | ◐ | ✅ | ✅ |
| *对象：*可执行产物 | ✅ | ◐ | — | ◐ | ◐ | ✅ | ✅ | ✅ |
| *Claim：*selection | — | — | — | ◐ | — | ✅ | ◐ | ✅ |
| *Claim：*activation | — | — | — | — | — | — | — | ✅ |
| *Claim：*attribution | ◐ | — | ◐ | ◐ | ✅ | ✅ | ◐ | ✅ |
| *Claim：*improvement | ✅ | ◐ | ◐ | ◐ | ◐ | ✅ | ◐ | ✅ |
| 理论 | ◐ | ◐ | — | ◐ | — | ◐ | — | ✅ |
| 应用 | ✅ | ✅ | ◐ | ✅ | ◐ | ✅ | ✅ | ✅ |
| 社会影响 | — | ◐ | ◐ | — | ◐ | — | — | ✅ |

<sub>在*骨干模型固定*这一行没有任何一列拿到 ✅，包括本文，因为没有综述跑自己的对照实验；标 ◐ 的那几列在定义上区分了两条更新通道，同时刻意把模型侧更新留在范围内。四个 claim 要拿 ✅，需要给出显式的证据标准，而不是从终端分数反推。理论要拿 ✅，需要综述自己发展出形式化结果。**Zhou-E** 是外化综述，**Zhou-C** 是编码 agent 综述，后者声明的范围仅限软件工程。</sub>

**完整条目。**

- **A Survey of Self-Evolving Agents** `TMLR'26`：按演化什么、何时演化、如何演化、在哪里演化来组织。[[paper]](https://arxiv.org/abs/2507.21046)
- **A Comprehensive Survey of Self-Evolving AI Agents** `arXiv'25`：按优化器反馈组织方法。[[paper]](https://arxiv.org/abs/2508.07407)
- **Externalization in LLM Agents** `arXiv'26`：统一回顾记忆、技能、协议与 harness 工程。[[paper]](https://arxiv.org/abs/2604.08224)
- **Code as Agent Harness** `arXiv'26`：按代码在 agent 循环中的角色组织。[[paper]](https://arxiv.org/abs/2605.18747)
- **Recursive Self-Improvement in AI** `arXiv'26`：从受限自我精修到自主研究闭环，按闭环闭合程度组织。[[paper]](https://arxiv.org/abs/2607.07663)
- **Self-Improvements in Modern Agentic Systems** `arXiv'26`：在显式的参数冻结假设下区分模型通道与脚手架通道，在评测纪律上最接近本文，未涉及 activation。[[paper]](https://arxiv.org/abs/2607.13104)
- **Self-Evolving Coding Agents** `arXiv'26`：区分模型侧更新与记忆、技能、工作流更新，并把自适应择优下的基准过拟合列为开放问题。[[paper]](https://arxiv.org/abs/2608.03392)

---

<a id="slandscape"></a>

## 领域增长图

![harness 自演化方法的增长与分类](assets/landscape.png)

<p align="center"><sub>图中 46 个方法是所综述 96 个方法的代表性子集，累计数量从 2023 年的 3 个升至 2026 年第三季度的 46 个。颜色表示主要侧重点，分别是 harness 更新、评测与理论。这个分类是描述性的，收录既不意味着持续自演化，也不意味着测到了改进。</sub></p>

---

<a id="smaint"></a>

## 维护说明

| 日期 | 变更 |
|---|---|
| 2026-10-01 | 首次发布。四个分类分支下共 187 个工作，96 个方法的证据审计。 |

每月刷新一次，另外在任何已收录预印本有接收消息时刷新。`arXiv'YY` 在接收后升级为对应会议，这是最常见的一类修正。缺了哪个工作请直接开 issue，不必等例行刷新。

每次刷新前检查两条不变量：每个条目只出现一次（[第 4 节](#s4)是声明的例外），每个链接都指向正确的论文。徽章计数与[第 5 节](#s5)的审计比例由 [`docs/claim-audit.md`](docs/claim-audit.md) 重新生成，不手工编辑。

---

<a id="scontrib"></a>

## 贡献指南

欢迎提 PR。门槛定得比较具体，因为这份清单的价值在分类本身，不在收录数量。

**新增论文**的完整清单见 [CONTRIBUTING.md](CONTRIBUTING.md)，要点如下。

1. **范围。**说明该工作满足[什么是 harness RSI](#sdef) 里三个条件中的哪几个，分别是持久性、递归性、模型固定。任何一条不满足的工作应进[边界情形](#sbound)，并写明原因。
2. **只占一个节点。**给出它所属的唯一路径，分支、小节、机制，并说明该工作*自身*贡献了什么。如果它的贡献是评测协议，即使同时发布了系统，也归入第 3 节。
3. **格式。**一行，写机制不写结果，附一个确认过的 arXiv 编号、DOI 或会议页面，不要猜链接。
4. **claim 判定可选，但价值很高。**如果新增的是第 1、2 节的方法，为 [`docs/claim-audit.md`](docs/claim-audit.md) 补一行，含四个判定与每格依据（读自哪张表、哪张图、哪个数字或哪句话），条目的用处会大得多。动手前先读[评分标准](docs/claim-audit.md#rubric)。

**对已有判定提出异议**同样是合法的 PR。每格的依据都记录在案，正是为了让分歧能对着原文谈，而不是对着判定谈。

---

<a id="scite"></a>

## 引用

```bibtex
@misc{wei2026harnessrsi,
  title  = {Harness Self-Evolution: Theory, Algorithm, Evaluations,
            Applications, and Social Impacts},
  author = {Wei, Chuyang and Guan, Haoxiang and Zhu, Minghang and
            Zhou, Kexin and He, Jiyan and Shen, Yifei},
  year   = {2026},
  note   = {Working draft. arXiv identifier to be added on release.},
  url    = {https://github.com/zgcagi/Awesome-Harness-RSI}
}
```

---

<a id="slicense"></a>

## 许可

以 [CC BY 4.0](LICENSE) 发布。所列工作各自遵循其原有许可，本仓库只包含文献元数据、一句话机制总结与证据判定。

图片由论文作者从配套论文中转载。
