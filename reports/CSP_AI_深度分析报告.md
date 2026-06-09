# CSP/LBBAP 与 AI 领域深度分析报告

> 基于 6 本 EP 核心期刊 613 篇文章（414 篇含摘要），2023-2026

---

## 一、文章总量与分布

| 期刊 | 总计 | CSP/LBBAP | AI/ML | 交叉 |
|------|------|-----------|-------|------|
| Heart Rhythm | 204 | 150 | 54 | 0 |
| PACE | 105 | 99 | 7 | 1 |
| JACC EP | 97 | 66 | 31 | 0 |
| JICE | 94 | 80 | 14 | 0 |
| Europace | 88 | 61 | 28 | 1 |
| Circ AE | 25 | 10 | 15 | 0 |
| **总计** | **613** | **466** | **149** | **2** |

**关键发现**：CSP/LBBAP 与 AI/ML 几乎零交叉（仅2篇），提示 **AI+CSP 交叉研究** 是一个显著的空白领域。JICE 是 CSP 发文量第三大期刊（80篇），仅次于 HR 和 PACE。

---

## 二、CSP/LBBAP 细分类别

### 2.1 子方向分布

| 子方向 | 篇数 | 核心关注点 |
|--------|------|-----------|
| LBBAP 技术/植入 | 186 | 导线设计、植入技术、鞘管、RF辅助植入 |
| LBBAP 生理/机制 | 172 | 夺获标准、QRS形态、电激动模式 |
| LBBAP 预后/安全 | 152 | 长期参数、并发症、穿孔、阈值变化 |
| CSP 综述/总论 | 109 | 生理性起搏综述、指南、共识 |
| LBBAP 用于 CRT | 103 | 心衰、再同步化、LVEF改善 |
| LBBAP vs RV Pacing | 80 | 与传统右室起搏的比较 |
| His 束起搏 | 78 | HBP技术、与LBBAP对比 |
| CSP 特殊人群 | 24 | 儿科、高龄、先心病、TAVR后 |
| CSP + ICD/除颤 | 14 | CSP与ICD联合、除颤导线 |

### 2.2 年度趋势

| 年份 | LBBAP技术 | LBBAP机制 | LBBAP预后 | CRT | His束 |
|------|-----------|-----------|-----------|-----|-------|
| 2023 | 60 | 57 | 46 | 35 | 24 |
| 2024 | 39 | 39 | 37 | 23 | 24 |
| 2025 | 45 | 43 | 38 | 23 | 13 |
| 2026(5月) | 38 | 30 | 27 | 19 | 7 |

**趋势**：
- LBBAP 持续高产；His 束起搏明显下降（2023:24→2026:7），被 LBBAP 替代
- LBBAP 技术/植入类文章最多，但增速放缓 → 技术趋于成熟
- LBBAP for CRT 保持稳定 → 仍有大量临床证据需要积累

### 2.3 各期刊 CSP 特色

- **Heart Rhythm**: 最全面，机制研究占比高（in-silico模型、电生理映射），发表 CORE-CPP 等大型真实世界研究
- **PACE**: 偏临床实践，高龄患者、儿科、zero-fluoroscopy、stylet-driven lead 等技术细节丰富
- **JACC EP**: 大量 editorial/commentary（如 "LBBAP Is Not LBBP", "Does Lead Position Matter?"），His-Alternative I 等 RCT 长期随访
- **Europace**: meta-analysis 多，比较研究多（CSP vs RVP，SDL vs LLL），欧洲多中心数据
- **JICE**: CSP 第三大发文量（80篇），技术比较研究丰富（LBBP vs LVSP、SDL vs LLL、CSP vs BiVP），多中心前瞻性研究增多
- **Circ AE**: 量少但质高，选题前沿（delivery system机制、选择性LBB夺获特征）

---

## 三、AI/ML 细分类别

### 3.1 子方向分布

| 子方向 | 篇数 | 代表性应用 |
|--------|------|-----------|
| AI-ECG 诊断/筛查 | 83 | ATTR-CM检测、AF预测、CHD筛查 |
| AI 风险预测 | 51 | CRT反应预测、SCD风险、ICD预后 |
| AI Mapping/成像 | 38 | 自动ICE标注、LGE-CMR分析 |
| AI 引导消融 | 29 | 自动靶点识别、术中辅助 |
| AI 心律失常检测 | 27 | 自动心律分类、AF检测 |
| 数字健康/可穿戴 | 14 | PPG心脏骤停检测、远程监测 |
| NLP/LLM | 5 | ChatGPT在EP中应用（极少）|

### 3.2 年度趋势

- AI-ECG 持续主导（2023:22 → 2025:32），但增速放缓
- AI Risk Prediction 快速增长（2023:9 → 2025:18），尤其 CRT 反应预测
- AI Mapping/Imaging 2024年达峰（11篇），技术驱动
- NLP/LLM 刚起步（5篇），巨大增长空间

### 3.3 各期刊 AI 特色

- **Heart Rhythm**: AI-ECG 最多，Willem AI平台、FactorECG算法等创新模型
- **Circ AE**: 偏高影响力验证研究（多中心、Framingham、UK Biobank），AI深度学习检测传导异常
- **JACC EP**: editorial 讨论多（"From Algorithm to Bedside"），multimodal AI (MAARS-CS) 等突破
- **Europace**: mapping/imaging AI 较多，ML预测模型
- **PACE**: AI极少（7篇），以综述和ML预后模型为主

---

## 四、重要发现与创新点

### 4.1 CSP/LBBAP 里程碑研究

| 研究 | 期刊 | 创新点 |
|------|------|--------|
| CORE-CPP (2026) | HR | 首个基于Medicare真实世界数据的CSP vs CRT-P大样本研究（n=7900），证实CSP非劣效，且全因死亡更低 |
| His-Alternative I 5年 (2026) | JACC EP | 首个His-CRT vs BiV-CRT的RCT长期随访（5.3年），生态学反应相当但His-CRT再干预率高 |
| ChiCSP (2026) | JACC EP | 中国多中心注册（n=3336），首次系统分类LBBAP（LBBP/LVSP/未分类），证实LBBP>LVSP |
| RF辅助LBBP植入 (2026) | HR | 射频电流辅助间隔穿透的创新技术（n=37），解决纤维化间隔植入困难 |
| LVSeP ≈ LBBP (2026) | HR | 超高频ECG证实左室心内膜下起搏与直接LBB夺获同步性和血流动力学相当 |
| LBBAP抗心律失常 (2026) | HR | 计算模型证实LBBAP通过恢复LV激动降低室性心律失常易损性 |
| LBBAP 抗心动过速起搏 (2026) | JACC EP | 动物模型首次证实LBBA-ATP终止VT成功率显著高于RV-ATP (70.2% vs 47.3%) |

### 4.2 AI 突破性研究

| 研究 | 期刊 | 创新点 |
|------|------|--------|
| MAARS-CS (2025) | JACC EP | 多模态AI（LGE-CMR+临床数据）预测心脏结节病SCD风险，AUC=0.86 远超LVEF标准 |
| AI-ECG 生物年龄与CRT (2025) | JACC EP | AI-ECG年龄差(δage)独立预测CRT-D术后生存 |
| Deep Learning 检测传导疾病 (2025) | Circ AE | 24小时单导联ECG检测无症状缓慢心律失常，AUC 0.89 |
| Willem AI ATTR-CM (2026) | HR | AI平台从12导联ECG检测心脏淀粉样变，早期无症状阶段灵敏度68% |
| 多中心AI-AF预测验证 (2026) | HR | Tempus ECG-AF模型3中心外部验证（n=4017），特异性92% |
| 自动ICE解剖标注 (2025) | JACC EP | 深度学习自动标注心腔内超声15个解剖结构 |

### 4.3 CSP 中被忽视但重要的发现

- **性别差异**: LBBAP中女性V6-RWPT比男性短~7ms，现有LBB夺获标准可能对女性过于宽松（PACE, Shadrin 2026）
- **间隔瘢痕预测CRT反应**: CMR评估导线部署部位周围瘢痕负荷可预测LBBAP疗效（AUC=0.87），瘢痕>12.3%反应率显著下降（PACE, Yin 2026）
- **PC-CT精确定位**: 光子计数CT证实导线尖端距LV内膜≤3.2mm预测LBB夺获（HR, Goto 2026）
- **CSP后新发房颤更少**: Meta-analysis证实CSP vs RVP新发AF风险降低62%（PACE, Li 2025）

---

## 五、研究间矛盾与争议

### 5.1 LBBAP vs LBBP — 定义之争

**矛盾核心**: LBBAP（left bundle branch area pacing）是否等同于 LBBP（left bundle branch pacing）？

- **JACC EP editorial "LBBAP Is Not LBBP"** (Joza, 2026): 强调需区分真正的LBB夺获与左室间隔心肌起搏
- **ChiCSP研究** (JACC EP, 2026): 数据支持 LBBP > LVSP，LVSP死亡/心衰住院率33.3% vs LBBP 8.6%
- **HR研究** (Poviser, 2026): 反方证据 — LVSeP与LBBP在LV同步性和血流动力学无差异
- **JACC EP** (Prinzen, 2025): 社论支持"LVSP力学与LBBP相似"

**现状**: 分类标准尚未统一，ChiCSP的LBBP优于LVSP与HR的LVSeP≈LBBP存在张力。可能的解释是患者群体和定义标准不同。

### 5.2 His 束起搏 vs LBBAP — 技术选择之争

- **His-Alternative I 5年** (JACC EP): His-CRT生态学反应与BiV-CRT相当（89% vs 90%），但再干预率高（37% vs 3%）
- **ChiCSP** (JACC EP): HBP阈值升高发生率显著高于LBBAP（5.03% vs 1.80%）
- **PACE多项研究**: His束起搏在AV结消融+pace-and-ablate策略中表现良好（47月随访阈值稳定）
- **共识趋势**: His束起搏正被LBBAP取代，但在特定场景（如先心病术后、近端传导系统疾病）仍有价值

### 5.3 Stylet-driven Lead vs Lumenless Lead

- **PACE meta-analysis** (Sripusanapan, 2024, n=8996): SDL成功率与LLL相当，但并发症更高（OR 1.80），脱位风险高（OR 3.26）
- **PACE另一meta-analysis** (Yu, 2025): SDL与LLL植入成功率、QRS持续时间无差异
- **PACE单中心** (Niehaus, 2025): 无专用鞘管植入LBBAP成功率79%，为简化手术提供可能
- **PACE** (Korkmaz, 2025): SDL在80岁以上高龄患者安全有效
- **矛盾**: 安全性数据不一致，SDL并发症是否真正更高需更大样本RCT验证

### 5.4 CSP 对 LVEF 正常患者的长期获益

- **多项研究证实**: CSP在高起搏负荷正常LVEF患者中保护心功能优于RVP
- **但**: LBBAP术后LVEF改善幅度在不同研究间差异大（HFrEF: +13%~+21%），影响因素不清
- **未解决**: 低起搏负荷（<20%）患者是否需要CSP？缺乏RCT证据

---

## 六、研究空白与选题方向

### 6.1 高优先级选题（创新性高 + 临床价值大）

| 选题方向 | 理由 | 推荐期刊 |
|---------|------|---------|
| **AI预测LBBAP疗效/CRT反应** | CSP与AI零交叉，AI-ECG预测CRT反应已有基础，延伸至LBBAP是自然方向 | Circ AE / HR |
| **AI辅助LBBAP植入（实时ECG分析）** | 术中自动判断LBB夺获仍依赖人工，AI实时辅助可降低学习曲线 | HR / JACC EP |
| **LBBAP vs BiVP RCT（大样本，非劣效）** | 仅有CORE-CPP（观察性）和His-Alt I（小样本），缺乏关键RCT | HR |
| **LBBAP中女性特异性夺获标准** | 仅1篇研究（PACE），性别差异可能导致误判LBB夺获 | HR / Europace |
| **AI-ECG预测LBBAP术后室性心律失常风险** | LBBAP抗心律失常机制已证实但缺乏预测工具 | JACC EP |
| **CMR瘢痕引导LBBAP导线定位** | 单篇报告瘢痕负荷预测反应，需多中心验证 | Circ AE / Europace |

### 6.2 中优先级选题（填补空白）

| 选题方向 | 理由 | 推荐期刊 |
|---------|------|---------|
| CSP在TAVR后长期预后 | 已有小样本短期数据，需大样本长期随访 | PACE / Europace |
| LBBAP + ICD 联合策略的安全性 | 仅14篇，ICD检测与LBBAP交互影响不清 | HR / JACC EP |
| 可穿戴设备在CSP远程监测中的应用 | 目前AI+可穿戴+CSP无任何研究 | Europace / PACE |
| NLP/LLM 辅助EP临床决策 | 仅5篇，且无CSP相关 | JACC EP editorial |
| 儿科LBBAP长期结局（>2年） | 现有数据均为短期（<18月），儿科需终身起搏 | HR / PACE |
| LBBAP导线远期（>5年）性能 | 最长随访~4年（ChiCSP），缺乏更长期数据 | HR / Europace |
| LBBAP期间T波过感知的系统性研究 | 仅case report，需系统分析发生率和预测因素 | PACE / HR |

### 6.3 Meta-analysis/Systematic Review 机会

| 选题 | 数据基础 | 推荐期刊 |
|------|---------|---------|
| LBBAP vs BiVP for CRT: 系统综述 | 多个回顾性比较+小RCT | Europace / PACE |
| AI-ECG在心律失常预测中的诊断准确性 | >50篇独立验证研究 | Europace |
| CSP在AV block中长期安全性 | 5个RCT+多个注册研究 | PACE |
| LBBAP 在不同心肌病表型中的疗效比较 | 散在研究覆盖DCM/HCM/ICM/CS | HR |

---

## 七、摘要结构分析

### 7.1 各期刊摘要特征

| 特征 | HR | Circ AE | Europace | JACC EP | PACE | JICE |
|------|-----|---------|----------|---------|------|------|
| 平均词数 | 259 | 277 | 238 | 245 | 212 | 248 |
| 结构化摘要 | 0% | 0% | 0% | 0% | 2% | ~10% |
| 含统计数据 | 36% | 17% | 30% | 22% | 12% | 28% |
| 明确结论句 | 4% | 0% | 2% | 2% | 2% | 5% |
| 中位样本量 | 249 | 125 | 163 | 338 | 96 | 100 |

### 7.2 各期刊摘要写作风格

**Heart Rhythm**:
- 最长摘要（259词），信息密度最高
- 非结构化但遵循隐式 Background-Methods-Results-Conclusion 流程
- 统计数据详尽（36%含p值/CI/HR），倾向量化表达
- 结论措辞谨慎："may assist", "further research is warranted"
- 典型开头："[疾病/技术] is [现状]. This study aimed to..."

**Circ AE**:
- 篇幅较长（277词），但有效摘要仅13篇（其余为letter/editorial）
- 机制导向，强调方法论细节
- 统计数据相对较少（17%），更注重描述性发现
- 倾向于 "We hypothesized..." / "We aimed to..." 开头
- 结论强调临床转化意义

**Europace**:
- 篇幅适中（238词），结构最规范
- 偏好描述性统计（中位数、四分位）
- 比较研究最多，摘要中常见 "Group A vs Group B" 结构
- 结论常包含实践建议
- 典型开头：直接阐述研究背景和gap

**JACC EP**:
- 篇幅适中（245词），但editorial/commentary大量无摘要
- 原创研究摘要结构完整，强调"aim"和"clinical implications"
- 使用 "sought to" 多于 "aimed to"
- 结论倾向于强调发现的novelty和临床意义
- 大量无摘要的短篇（editorial、letter），以标题传递信息

**PACE**:
- 最短摘要（212词），最直接
- Case report 摘要简洁描述病例经过和教训
- Meta-analysis 摘要遵循 PRISMA 结构
- 统计数据最少（12%），临床描述为主
- 结论常以 "appears to be feasible and safe" 类表述结尾

**JICE**:
- 适中篇幅（248词），介于 HR 和 Europace 之间
- 部分摘要采用半结构化格式（带隐式分段，~10%）
- 统计数据丰富（28%），重视比较结果的定量表述
- 方法描述详细：强调 "multicenter prospective"、"systematic review" 等设计细节
- 结论措辞平衡谨慎与明确："may represent feasible procedural consideration"、"findings are exploratory"
- 典型开头：直接阐述技术现状和局限，然后描述研究目的
- 特色：比较研究摘要中明确列出两组数据和p值

---

*报告生成时间: 2026-05-26 | 数据: PubMed 613篇 CSP/LBBAP + AI 文章（含 JICE 94篇）| 分析方法: Python自动化+人工定性分析*
