# Skills 迭代方法论与经验(本窗口复盘)

把两个 EP 期刊 skill(abstract / title)从"凭印象写"升级为"全语料 + 双模型验证 + 生成对比迭代"的完整过程与教训。可作为今后做任何"基于语料的写作/分类类 skill"的模板。

---

## 一、整体方法弧(从不可信到可信)

1. **起点(不可信)**:读 8–12 篇摘要 → 归纳期刊画像。快,但是假设,非结论。
2. **建码本 + 盲编码**:13 维内容码本,**盲于期刊**(消除确认偏差),先 414 篇,后扩到 **1677 篇全主题代表性语料**。
3. **双模型独立编码**:Claude(Sonnet)+ Codex(GPT-5.4)各编一遍,算跨模型 κ;另做单模型双轮信度。
4. **量化验证中心主张**:用**防识别的内容分类器**(只用编码特征,不用文本)测"内容能否预测期刊"。
5. **重构 skill 架构**:精简 SKILL.md + `references/`(渐进披露)。
6. **Codex 跨模型红队**:第二个前沿模型审 skill 断言 vs 证据。
7. **生成-对比迭代**:held-out 真实摘要 → 抽 brief → skill 生成 vs 裸生成 → 双模型盲评 → 据弱点改 → 全新数据复测(R1/R2/CircAE)。

---

## 二、核心结论(内容层)

- **不存在"某期刊特殊的写法"**:六刊内容分布平均每维重叠 ≥86%(双模型),内容分类器仅 30% vs 基线 24%。差异主要是 **scope(收什么研究)+ 薄格式 + JACC 非人称语态**。
- skill 的正确结构 = **通用内容引擎(6 步论证弧,主体)+ 期刊 fit/定位层 + 格式合规脚注**,而非"六种话术"。
- skill 实测有效:5 个充分采样期刊,skill > 无skill 双模型/两组全新数据稳健(60–80%),驱动力是 journal-fit + 确定性纪律。CircAE 因数据受限(n=4)未确认。

---

## 三、方法论教训(最可复用的部分)

1. **几篇精读 = 假设,不是结论。** 全语料编码推翻了我 5 条手读判断(如"Circ AE=AI 刊"→实为机制/基础;"unstructured"→实为 86–96% 结构化)。用户坚持严格性是对的。

2. **样本是否代表问题本身,先于一切。** 窄主题语料(只抓 CSP/LBBAP+AI)制造了"Circ AE=AI"假象;全主题代表性抽样才纠正。**先问:我的样本能回答这个问题吗?**

3. **凡判断必跨模型。** 单模型(编码/评审/红队)有自偏好偏见。Claude+Codex 双编码、Codex 红队、Codex 评 Claude 生成——**跨模型一致才让结论可信**。同模型评自己生成 vs 人类原文(AvO 臂)被自偏好污染,只能打折。

4. **用 κ 量化可靠度,据此校准措辞。** gap_type/contribution_frame κ≈0.7(硬,可下结论);conclusion_stance κ≈0.49(软,只报粗分);certainty κ=0.16(kappa 悖论,看原始一致率)。**别把低信度维度当强结论写。**

5. **警惕"识别"冒充"推理"。** 文本版盲分类 100% 准——因为 Codex 认出了真实论文(引 DOI)。**真实发表内容会被前沿模型记住。** 防识别做法:在编码特征上测、不在原文上测。凡用真实数据,先问:模型是在推理还是在回忆?

6. **No silent fallback 救命。** 聚合脚本的守卫抓出:编码越界标签、空分布期刊导致 `tvd({},pooled)=0.5` 静默拉高均值、id-join 的 Windows 路径 bug。每个都会无声出错却产出"看似合理"的数字。

7. **迭代有收益递减,要知道何时停。** R2 的 3 处微调在全新数据上无可测增量——核心价值已被前面捕获。继续微调不划算。

8. **skill 架构(官方 skill-creator 规范)**:SKILL.md <500 行纯操作指令,分析/数据/证据下沉 `references/`(复数),渐进披露三层。**别把叙述混进 SKILL.md。**

9. **生成-对比 eval 的纪律**:① brief 提取与生成用**分离 agent**(生成端不看原文,杜绝泄漏);② 主臂用 **skill vs 无skill(对称)**,抗自偏好;③ 调优集与**全新 held-out 测试集分离**,防过拟合评委;④ 盲评 + 随机顺序 + 抹除识别线索。

---

## 四、工程教训(Codex CLI / 编排)

- **并发是 Codex 失败主因**:多个 `codex exec` 同时启动会抢共享 runtime 的 model-manager(`failed to refresh available models: timeout`),大批失败/卡死。**解法:串行(-P1)。**
- **文件读取是另一卡点**:让 Codex 经沙箱工具读多个文件 → 卡在 runtime。**解法:自包含 prompt(把内容内联,零文件读)**,像评委任务那样稳。
- **单次硬超时**:`timeout 150 codex exec ...`,卡住的调用被杀并标 FAIL 跳过,不阻塞整批;失败的重跑。
- **Codex 结构化输出**:`--output-schema schema.json -o out.json` 强制终止 + 捕获,比自由文本 `-o` 更可靠。
- **杀进程副作用**:反复 `taskkill codex.exe` 可能让 runtime 进入坏状态;杀后 `sleep` 再启。
- **并行用 Claude workflow**:需要快/可靠的并行扇出时用 Claude workflow(60–140 agent 并行稳),把 Codex 留给"独立验证"这类必须跨模型的环节。
- **Windows 路径**:`os.path.basename(f)` 而非 `f.split('/')[-1]`(glob 返回反斜杠)。

---

## 五、可复用的资产(本项目内)

> 目录已整理(2026-06-09):skill 在 `.claude/skills/`,规范数据在 `data/`,一次性脚本在 `archive/`,中间产物在 `data/_intermediate/`,早期选题报告在 `reports/`。详见 `CLAUDE.md`。

- 码本 + 工作流:`.claude/workflows/abstract-coding-v2.js`、`archive/run_codex_chunk.sh`、`data/*_schema.json`
- 验证脚本(根目录,被 skill `references/evidence.md` 引用):`cross_model.py`(跨模型 κ/TVD,含低 n 守卫)、`p2_content_classifier.py`(防识别分类器)、`reliability.py`、`aggregate_codings.py`
- 迭代框架:`.claude/workflows/loop-r{1,2}-generate/judge.js` + `archive/judge_prep.py` + `archive/run_judge_codex.sh`(串行+超时)+ `archive/judge_aggregate.py`
- 结果:`data/loop_r1/RESULTS.md`(R1/R2/CircAE 全表)、`data/loop_t1/RESULTS.md`(title R1/R2/R3)、`摘要深度分析_内容层.md`(内容定论)

---

## 六、title skill 迭代的追加教训(从"无用"到"有用")

title skill 一开始**实测无收益**(skill vs 无skill 双模型 15/15 打平),经诊断→修复→复测变为 **60% 跨模型胜出**。过程教训:

10. **验证能翻转判断,甚至救活一个"没用"的 skill。** 若不测,要么交付一个无用的 title skill,要么误以为"标题没法做"而放弃。**是测试本身,加上对失败样本的诊断,创造了价值。**

11. **格式/风格指导边际价值低;信息内容指导才赢。**(与 abstract"内容>格式"同构)强模型本就会写标题风格;skill 的真正杠杆是**强制塞入具体信息**(关键发现/具体结局/两个对照臂/器械名/队列量)——模型默认做得不够的地方。Step 2 从"风格优先"改成"信息密度优先"后,informativeness 4.0→4.73,胜率 50%→60%。

12. **从失败样本诊断,别凭假设。** 逐条读输掉的 A-vs-B 标题 + 评委理由,才看清确切失败:丢器械名、用"a registry analysis"而非具体结局、漏队列量、生搬"JACC 用问句"。修复精准命中这些。

13. **盯住修复引入的新 tradeoff。** 信息密度修复使 clarity 下降(塞太挤);第二轮精修("挑 2–3 个最关键具体信息,别全塞")恢复 clarity 同时胜率再升——单调 50→57→60%。**每次改动都要复测,别假设只改好不改坏。**

14. **确定性正则对机械特征可靠,对语义类别系统性低估**(case/versus/review)——必须用独立模型交叉验证正则定义(Codex 在 90 标题上发现正则漏掉的未标注个案;colon 则 90/90 完全一致)。

15. **跨模型要贯穿到每个 skill 的红队,不只一个。** title skill 初期只有 Codex 评审和指标交叉验证,**漏了独立 Codex 红队**(abstract 有);完整性 = 每个 skill 都过独立跨模型审计。
