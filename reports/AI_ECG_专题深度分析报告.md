# AI-ECG in Electrophysiology: 专题深度分析报告

> 基于 6 本 EP 核心期刊 160 篇 AI/ML 文章（107 篇含摘要），2022-2026
> 期刊覆盖：Heart Rhythm (58), JACC EP (31), Europace (29), JICE (17), Circ AE (15), PACE (10)

---

## 一、领域全景

### 1.1 规模与增长

| 年份 | HR | Circ AE | Europace | JACC EP | PACE | JICE | 合计 |
|------|-----|---------|----------|---------|------|------|------|
| 2022 | 2 | 0 | 0 | 0 | 0 | 1 | 3 |
| 2023 | 14 | 4 | 10 | 8 | 1 | 5 | 42 |
| 2024 | 20 | 5 | 10 | 8 | 2 | 4 | 49 |
| 2025 | 17 | 4 | 7 | 12 | 5 | 5 | 50 |
| 2026 | 5 | 2 | 2 | 3 | 2 | 2 | 16 |

**趋势**: 2023-2025年呈稳定高位，未出现爆发式增长。但方向在分化——从早期的 AF 检测集中转向多目标多模态。

### 1.2 数据规模分布

- 69 篇报告了样本量，**中位数 688**，跨度极大（10 - 1,163,401）
- **>10,000**: 18 篇（26%）— 提示 AI-ECG 领域已进入大数据时代
- **>100,000**: 9 篇 — 主要集中在 HR 和 JACC EP
- 但仍有大量单中心 <500 样本研究

**使用的知名队列**: UK Biobank (6), Framingham (2), MIMIC (2), Cleveland Clinic (2), Mayo Clinic (1)

---

## 二、输入模态分析

### 2.1 分布

| 输入模态 | 篇数 | 典型场景 |
|---------|------|---------|
| CMR/CT 影像 | 53 | LGE-CMR 瘢痕分析、CT 心腔分割 |
| 12 导联标准 ECG | 25 | AF/心肌病筛查、生物年龄估算 |
| 单导联/可穿戴 ECG | 10 | 缓慢心律失常检测、AF 长程监测 |
| 多模态融合 | 6 | ECG + CMR + 临床数据 |
| 心内电图 (EGM/ICE) | 5 | GP 定位、ICE 解剖标注 |
| PPG/光电信号 | 4 | 心脏骤停检测、AF 连续监测 |

**关键发现**:
1. **CMR/CT 影像类意外占据主导（53篇）** — 这并非传统"AI-ECG"概念，而是影像+AI。说明 EP 领域的 AI 应用已超越 ECG 本身
2. **12 导联 ECG（25篇）** 是真正的 AI-ECG 核心，但占比仅 15.6%
3. **多模态融合（6篇）快速增长**（2025年4篇），这是最具潜力的方向
4. **心内电图 AI（5篇）** 极度稀少但价值高（术中实时分析）

### 2.2 多模态融合趋势（6篇）

| 研究 | 期刊 | 融合方式 | 目标 |
|------|------|---------|------|
| MAARS-CS | JACC EP 2025 | LGE-CMR + 临床数据 → 3D-CNN + FFN | SCD 风险预测 |
| FactorECG | HR 2026 | ECG 21因子 + 临床 + CMR | CRT 反应预测 |
| AI-ECG + CHARGE-AF | Circ AE 2025 | DNN-ECG + 临床评分 | AF 风险预测 |
| Tempus ECG-AF | HR 2026 | ECG-AI + 临床 | AF 风险筛查 |

**意义**: 单一模态正接近性能天花板（ECG-AF 单独 AUC ~0.82），融合模型可突破（AUC 0.85-0.86）。这是发表高影响力研究的最佳路径。

---

## 三、目标疾病/任务分析

### 3.1 AF 检测与预测（37篇 — 最大方向）

**细分**:
- AF 存在/发生风险预测（28篇）
- AF 消融后复发预测（9篇）

**代表性模型性能**:

| 研究 | 期刊/年 | AUC | 数据量 | 特点 |
|------|---------|-----|--------|------|
| ECG-AF DNN (Framingham+UK Biobank+ELSA-Brasil) | Circ AE 2025 | 0.82-0.85 | 71,661 | 三队列多国验证 |
| Tempus ECG-AF | HR 2026 | 特异性 92% | 4,017 | 3 中心外部验证 |
| 单导联 AI-AF | Europace 2023 | 0.80 | 831 | 单导联 CNN |
| PPG 连续 AF | JACC EP 2024 | 0.994 | — | 光电信号 |

**矛盾与问题**:
1. **性能报告不一致**: AUC 从 0.80 到 0.994，但评估条件差异大（连续信号 vs 单次 ECG，诊断 vs 筛查）
2. **"预测"的定义不统一**: 有的是从当前 ECG 预测未来 AF 风险，有的是检测隐匿性 AF，有的是从 PPG 实时判断当前节律
3. **外部验证稀缺**: 37 篇中仅 3 篇有严格多中心外部验证
4. **临床可操作性不明**: AUC 0.82 在群体筛查中的 PPV 极低（因 AF 基线发病率低），但鲜有研究讨论此问题

**AF 复发预测（9篇）**:
- JICE (2023): SCALE-CryoAF 模型验证，AUC 0.74 — 性能中等
- JICE (2025): AI-guided spatiotemporal dispersion mapping 个性化消融
- **消融后复发预测的模型性能普遍低于 AF 检测**（AUC 0.70-0.80），原因是复发受多因素影响

### 3.2 消融靶点与引导（22篇 — 第2大方向）

**年度趋势**: 2023:5 → 2024:6 → 2025:7 → 2026:4（稳步增长）

**细分应用**:
1. **Mapping/靶点识别**: AI 自动识别 slow pathway、ganglionated plexi、critical isthmus
2. **PVI 完成度判断**: ML 算法验证 PVI 隔离状态
3. **消融后食管损伤预测**: 热损伤风险模型
4. **ICE 解剖自动标注**: 深度学习标注 15 个心腔内解剖结构（JACC EP 2025）

**代表性研究**:
- JICE (2026): CNN 从心内双极电图实时定位 ganglionated plexi（AUC 0.87，但 n=18）
- JICE (2025): AI-guided spatiotemporal dispersion mapping 指导个性化 AF 消融
- JICE (2026): AI-guided PFA + peak frequency mapping 预测终止点和持久性控制
- Europace (2024): ML 验证 PVI 完成，AUC 0.92

**问题**:
- 样本量普遍极小（<100），尤其术中实时引导类
- **无前瞻性 RCT 比较 AI-guided vs 标准消融结局**
- 不同 mapping 系统之间模型不可移植

### 3.3 生物年龄/整体心血管风险（29篇）

**概念**: AI-ECG 从 ECG 估算"生物年龄"，与实际年龄的差值（δage）作为整体心血管风险标志物。

**代表性研究**:
- JACC EP (2025): δage 预测 CRT-D 术后生存（time ratio 0.96 per year）
- Circ AE (2025): AI-vascular age 预测新发 AF（Framingham）
- JACC EP (2024): AI-ECG 血清钾监测（AUC 0.876, n=293,557）
- JACC EP (2025): 儿科 ECG 自动诊断（AUC 0.99, n=583,134）

**批判性分析**:
1. **"AI-ECG age" 概念泛化严重**: 29 篇中许多只是将 ECG-AI 输出与年龄相关指标关联，缺乏明确的临床决策节点
2. **Circular reasoning 风险**: ECG 本身包含年龄信息，AI 模型可能只是精确提取了这些已知特征，而非发现新的生物标志物
3. **但也有真正的突破**: MAARS-CS（JACC EP 2025）通过多模态 AI 预测 SCD，AUC 0.86 显著优于 LVEF 标准（0.59）
4. **临床实用性争论**: editorial "From Algorithm to Bedside"（JACC EP 2025）直接质疑 AI 模型的临床可操作性

### 3.4 心肌病筛查（5篇 — 增长最慢）

| 心肌病类型 | 篇数 | 代表性 AUC |
|-----------|------|-----------|
| ATTR-CM（淀粉样变）| 2 | 0.88-0.92 |
| HCM | 1 | — |
| DCM/TTNtv | 1 | 0.83-0.86 |
| General | 1 | — |

- HR (2026): Willem AI 检测 ATTR-CM，AUC 0.88，早期无症状灵敏度 68%
- JACC EP (2025): DNN 从 ECG 识别 TTNtv-DCM，C-statistic 0.83-0.86

**明显空白**: **AI-ECG 检测心肌淀粉样变以外的心肌病**（如 ARVC、CS）几乎空白。ATTR-CM 被重点关注是因为 tafamidis 等治疗的出现使早期检测有明确临床价值。

### 3.5 CRT 反应预测（7篇 — 快速增长）

**年度趋势**: 2023:1 → 2024:1 → 2025:2 → 2026:3（增速最快的子方向之一）

| 研究 | 期刊/年 | 方法 | 核心发现 |
|------|---------|------|---------|
| FactorECG | HR 2026 | ECG 21因子 + 临床 | 外部验证预测 CRT 非反应 |
| AI-ECG age for CRT | JACC EP 2025 | δage 评分 | 低 δage → CRT 后生存更长 |
| MLP for ICD/CRT-D | PACE 2025 | 多层感知器 + SHAP | AUC 0.70-0.72，GFR 最重要特征 |
| Super-response | JICE 2024 | 传统 ML | 预测 CRT super-response |

**关键发现**: AI 预测 LBBAP-CRT 反应已有萌芽——Europace 2024（PMC10803037）报道 Mayo AI-ECG 平台预测 LBBAP 后 CRT 结局（单中心），Mayo 还注册了前瞻性试验 [NCT07206602](https://clinicaltrials.gov/study/NCT07206602)（2026年启动）。但现有研究均为单中心小样本，缺乏外部验证。JCE 2026 (Okubo, [DOI](https://doi.org/10.1111/jce.70339)) 报道了 ML 预测 LBBAP 植入失败的 nomogram（AUC 0.84），是该交叉领域的另一条路径。**多中心外部验证的 AI-LBBAP-CRT 预测模型** 和 **AI 区分 LBBP/LVSP 夺获类型**（完全空白）是最高价值选题。

### 3.6 VT/VF/SCA 检测与风险预测（8篇）

- JACC EP (2025): MAARS-CS 多模态 AI 预测心脏结节病 SCD，AUC 0.86
- Europace (2023): ML 优化 ICD 一级预防患者选择，AUC 0.90
- JACC EP (2024): AI-ECG 预测 TOF 修复后死亡率，AUC 接近 1.0（但可能过拟合）
- HR (2026): AI-ECG 心脏骤停检测（PPG，外部验证）

**方法论问题**: AUC 接近 1.0 的报告（JACC EP 2024）在 n=13,077 的非随机数据上需谨慎解读，过拟合风险高。

### 3.7 传导异常检测（4篇 — 极度稀少）

- Circ AE (2025): 深度学习从 24h 单导联 ECG 检测缓慢心律失常（停搏、完全性 AV block），AUC 0.89
- **这是 AI + CSP 最直接的交叉点**: 如果 AI 能检测传导系统疾病，则可辅助 CSP 适应症筛选和患者选择

### 3.8 PVC 定位（3篇）

- PACE (2024): ML review 综述 PVC 起源定位方法
- JICE (2023): "Two-step" ML 无创定位 PVC

**现状**: 算法停留在分类定位（RVOT/LVOT 等区域级别），未达到消融可用的精确度。

---

## 四、方法论分析

### 4.1 ML 方法分布

| 方法 | 篇数 | 趋势 |
|------|------|------|
| CNN/卷积网络 | 20 | 主流，稳定 |
| 传统 ML (RF/SVM/XGB) | 9 | 仍活跃 |
| 多模型比较/集成 | 16 | 常见 |
| NLP/LLM | 5 | 起步 |
| 可解释性 (SHAP/Grad-CAM) | 4 | 增长中 |
| Transformer/Attention | 3 | 极少（仅2024年） |
| RNN/LSTM | 2 | 近乎消失 |

### 4.2 方法论争议

#### CNN 独大 vs Transformer 缺位

EP 领域 AI-ECG 研究几乎完全由 CNN 主导（20 篇），Transformer 仅 3 篇（全在 2024 年）。这与 NLP/CV 领域 Transformer 已成主流形成鲜明对比。

**原因分析**:
- ECG 是时序信号，CNN（特别是 1D-CNN 和 ResNet）在固定长度信号分类上已足够有效
- EP 领域研究者多为临床背景，偏好成熟框架
- Transformer 的优势（长距离依赖、attention 机制）在短窗口 ECG 分析中优势不明显

**但 Transformer 在以下场景可能更优**:
- 多导联间关系建模（跨导联 attention）
- 长程 Holter/可穿戴 ECG 分析
- 多模态融合（ECG + 临床 + 影像）

**选题机会**: Transformer vs CNN 在 EP-specific ECG 任务上的系统性比较（目前文献空白）。

#### 传统 ML 仍有价值

9 篇使用 RF/SVM/XGB 的研究中，部分性能不逊于深度学习：
- HR (2025): RF 评估药物致 QT 延长风险，AUC 0.874（n=345,371）
- HR (2024): ML 识别心肌病 QRS 碎裂特征，AUC 0.88

**启示**: 当特征已明确（如 QRS 碎裂形态学特征）时，传统 ML 的可解释性优势明显。**不必追求深度学习**。

#### 可解释性要求升高

- SHAP/Grad-CAM 从 2024 年起被要求或推荐（4 篇）
- JACC EP editorial "From Algorithm to Bedside"（2025）直接呼吁可解释性
- PACE (2025): MLP + SHAP 识别 ICD 患者预后关键特征（GFR 最重要）
- **趋势**: 可解释性正从"加分项"变为"必需品"，尤其在 HR 和 JACC EP

### 4.3 验证标准

| 验证级别 | 篇数 | 现状 |
|---------|------|------|
| 内部验证（train/test split）| ~90+ | 标配 |
| 外部验证（独立机构）| 6 | **极度不足** |
| 多中心验证 | 8 | 增长中 |
| 前瞻性验证 | 1 | **几乎空白** |

**核心问题**: **绝大多数 AI-ECG 研究缺乏外部验证**。160 篇中仅 6 篇有严格外部验证，1 篇前瞻性验证。这严重限制了临床可信度。

**期刊态度差异**:
- **Circ AE** 和 **HR** 偏好多中心、多队列验证（如 Framingham + UK Biobank）
- **JICE** 和 **PACE** 对验证要求较低，接受单中心回顾性
- **JACC EP** 通过 editorial 质疑验证不足

---

## 五、研究间矛盾与争议

### 5.1 AI-ECG AF 预测：检测能力 vs 临床可操作性

**争论焦点**: AUC 0.82 的 AF 预测模型在临床中如何使用？

- **正方**（Circ AE 2025, HR 2026）: 可与临床评分联合提高预测（AUC 0.85）
- **反方**（JACC EP 2025 editorial）: 在低先验概率人群中，即使 AUC 0.85 的模型 PPV 也很低，可能导致大量假阳性和不必要检查
- **未解决**: 缺乏 cost-effectiveness 分析和 RCT 证据

### 5.2 深度学习 vs 传统方法：什么时候该用什么？

- HR (Circ AE): CNN/DNN 在 ECG-based 任务上表现优异
- HR (2024): 传统 ML (RF) 在 QRS 碎裂特征分析上 AUC 0.88
- JACC EP (2025): DNN 和传统 ECG 分析在 TTNtv-DCM 检测上性能相似（C-statistic 0.83 vs 0.86, P = 0.197）
- **启示**: **深度学习并非总是更优**。当已知特征充分时，传统方法可能更合适（且更可解释）

### 5.3 报告性能的过度乐观

- JACC EP (2024): AI-ECG 预测 TOF 修复后死亡率，AUC 接近 1.0 — 极可能过拟合
- JACC EP (2024): PPG AF 检测 AUC 0.994 — 在理想条件下测试
- **对比**: Tempus ECG-AF 外部验证（HR 2026）灵敏度仅 31%，远低于内部验证

**关键教训**: 内部验证性能显著高于外部验证是常态，发表时应透明报告两者差距。

### 5.4 "ECG 生物年龄"的科学性

- 29 篇使用"生物年龄"概念，但定义不统一
- 部分研究可能存在 **circular reasoning**：ECG 包含年龄信号 → AI 提取年龄信号 → 用于预测年龄相关疾病
- JACC EP (2025) δage 预测 CRT 生存是有意义的发现，但需排除混杂（更年轻的患者本身预后更好）

---

## 六、各期刊 AI-ECG 发文定位

| 期刊 | 发文量 | 核心定位 | 偏好 | 门槛 |
|------|--------|---------|------|------|
| **HR** | 58 | 大数据验证、平台型AI | 多中心大样本、FDA/CE相关、named platforms (Willem, Tempus) | 高——需外部验证或>10000样本 |
| **JACC EP** | 31 | 临床影响力、editorial批判 | 多模态、SCD预测、可解释性、editorial讨论 | 中高——接受小样本但需强clinical message |
| **Europace** | 29 | 方法比较、消融引导 | CNN vs 传统ML、ICD优化、mapping AI | 中——接受单中心但需方法论严谨 |
| **Circ AE** | 15 | 高质量验证、机制导向 | 多队列验证(Framingham级)、传导疾病检测 | 最高——仅接受高影响力创新 |
| **JICE** | 17 | 消融引导、技术应用 | 实时术中AI、mapping AI、比较验证 | 中低——接受pilot study |
| **PACE** | 10 | 临床实践、CIED相关 | CRT预测、远程监测AI、综述 | 低——接受综述和小样本 |

---

## 七、高优先级发表方向

### 7.1 直接空白区域（无/极少竞争）

| 选题 | 现状 | 创新性 | 推荐期刊 | 预期影响力 |
|------|------|--------|---------|-----------|
| **AI 区分 LBBP vs LVSP 夺获类型** | 0 篇（完全空白）| ★★★★★ | Circ AE / HR | 极高 — 直接解决分类争议 |
| **AI-ECG 预测 LBBAP-CRT 反应（多中心外部验证）** | ~2 篇萌芽（Europace 2024 单中心; Mayo 注册试验 NCT07206602 未启动）| ★★★★★ | Circ AE / HR | 极高 — 首个多中心验证 |
| **AI 实时辅助 LBB 夺获判断** | ~1-2 篇概念验证（EDEN JACC EP 2023; 首例 case PMC 2025）| ★★★★ | HR / JICE | 高 — 降低 LBBAP 学习曲线 |
| **AI 预测 LBBAP 植入失败** | 1 篇 (JCE 2026, AUC 0.84, 单中心) | ★★★★ | HR / JICE | 高 — 需多中心验证 |
| **Transformer 在 EP-ECG 任务上的性能** | 0 篇系统比较 | ★★★★ | Europace / HR | 中高 — 方法论创新 |
| **AI-ECG 预测 CSP 适应症/传导系统疾病** | 1 篇 (Circ AE) | ★★★★ | Circ AE / HR | 高 — 扩展 AI 临床场景 |
| **AI-ECG 检测 ARVC/CS/非ATTR心肌病** | ~1 篇 | ★★★★ | JACC EP / HR | 高 — 心肌病筛查扩展 |
| **联邦学习在多中心EP数据上的应用** | 0 篇 | ★★★ | Europace | 中 — 方法论前沿 |

> **注**: 上述"现状"评估基于 6 本 EP 核心期刊 + PubMed 全库 + ClinicalTrials.gov 扩展检索。AI+LBBAP 交叉领域并非完全空白，而是处于 proof-of-concept 萌芽阶段，Mayo 团队（AI-ECG for LBBAP-CRT + NCT07206602）走在最前面。核心空白是 **AI 区分 LBBP/LVSP 夺获类型** — 临床价值最高且完全无人触及。

### 7.2 增量创新（有基础但仍有大空间）

| 选题 | 现有证据 | 差距 | 推荐期刊 |
|------|---------|------|---------|
| **AI-ECG AF 预测的 cost-effectiveness** | 多个 AUC 0.80+ 模型 | 无经济学评估 | HR / Europace |
| **多模态 AI (ECG+CMR+临床) for SCD** | MAARS-CS (n=317) | 需更大样本+外部验证 | JACC EP / Circ AE |
| **AI-ECG 消融后复发预测的外部验证** | 多个模型 AUC 0.70-0.80 | 缺外部验证 | HR / JICE |
| **可穿戴 ECG + AI 长程缓慢心律失常检测** | 1 篇 (Circ AE) | 需前瞻性验证 | HR / Circ AE |
| **AI 辅助 ICE 实时导航** | 1 篇 (JACC EP) | 需临床验证 | JICE |
| **SHAP/可解释性在 EP-AI 中的系统性评估** | 4 篇零散 | 需方法论综述 | Europace / JACC EP editorial |

### 7.3 综述/Meta-analysis 机会

| 选题 | 可纳入研究数 | 推荐期刊 |
|------|-------------|---------|
| AI-ECG AF 检测/预测诊断准确性 meta-analysis | ~30 篇 | Europace |
| AI 在心律失常消融中的应用 systematic review | ~22 篇 | HR / JICE |
| Deep learning vs 传统 ML 在 EP 中的性能比较 | ~40 篇 | Europace |
| AI-ECG 模型外部验证现状批判性综述 | 全部 160 篇 | JACC EP editorial / HR |
| 多模态 AI 在 EP 中的应用前景 | ~6 篇 + 相关 | Circ AE review |

### 7.4 具体研究设计建议

#### 最高优先级：AI 区分 LBBP vs LVSP 夺获类型

**为什么是第一优先级**: LBBP vs LVSP 是 CSP 领域最大争议（JACC EP editorial "LBBAP Is Not LBBP"），ChiCSP 证实 LBBP 预后优于 LVSP，但术中判断仍依赖人工 ECG 解读且一致性差。这是 **临床价值最高且完全无人触及** 的方向。

**研究设计**:
- 收集已确认夺获类型（LBBP/LVSP/LBFP，基于 output-dependent QRS transition 金标准）的术中 paced 12 导联 ECG
- 训练 CNN/Transformer 自动分类夺获类型
- 特征对比：V6 upstroke/downstroke ratio（Cano JACC EP 2025 标准，灵敏度 0.97）vs AI 模型
- SHAP/Grad-CAM 可视化：AI 关注哪些导联/时间窗口？是否与电生理学知识一致？
- 关键亚组：DCM 患者（现有人工标准准确性仅 70.4%，AI 有望提升）
- 外部验证（至少 1 个独立中心）

**预期**: 直接解决分类争议的客观工具，降低术者依赖性。如 AI 在 DCM 亚组优于人工标准，是突破性发现。

**投稿策略**: HR（机制+大样本）> Circ AE（技术前沿）> JACC EP（如附 editorial 讨论）

**竞争态势**: 完全空白。Mayo NCT07206602 侧重 CRT 结局，非夺获分类。Cano (JACC EP 2025) 提出人工形态学标准但未用 AI。

#### 第二优先级：AI-ECG 预测 LBBAP-CRT 反应（多中心外部验证）

**竞争态势**: Europace 2024 已有单中心 proof-of-concept；Mayo NCT07206602 正在启动但尚未产出。**窗口期约 1-2 年**——第一个多中心外部验证的研究将有极高影响力。

**研究设计**:
- 回顾性多中心队列（≥3 中心）：LBBAP-CRT 患者术前 12 导联 ECG + 临床数据 + 6 月 LVEF
- 训练 CNN/Transformer 预测 LBBAP 反应（LVEF 改善 ≥15%）和超反应（LVEF 改善 ≥20% 或 >50%）
- 与 CHARGE-HF 评分、传统 ECG 参数、已有 BiVP-CRT 预测模型对比
- 外部验证（独立中心，时间分割验证）
- SHAP 可解释性：哪些 ECG 特征驱动 LBBAP-CRT 反应预测？与 BiVP 预测因素有何不同？
- 亚组分析：LBBB vs non-LBBB, ischemic vs non-ischemic

**投稿策略**: Circ AE（多中心+外部验证+机制洞察）> HR（大样本）> JACC EP（强 clinical message）

#### 第三优先级：AI 实时辅助 LBB 夺获判断

**竞争态势**: EDEN (JACC EP 2023) 提供了心肌内深度导航的概念验证（ML 分类器 97% 准确率），PMC 2025 有首例 AI-ECG mapping 引导 LBBAP case report。但系统性研究仍空白。

**研究设计**:
- 收集 LBBAP 术中实时 ECG（不同夺获类型 + penetration 过程动态变化）
- 训练模型：(1) 实时分类当前夺获状态；(2) 预测是否需要继续深入
- Pilot 前瞻性验证：AI 判断 vs 术者判断一致性
- 基于 EHRA 2023 共识分类标准

**投稿策略**: JICE（pilot study 门槛低）> HR（如样本充足）

---

## 八、方法论建议（给研究者）

### 8.1 发表门槛逐年升高

| 年份 | 可接受 | 趋势 |
|------|--------|------|
| 2023 | 单中心内部验证 | 基线 |
| 2024 | 多中心或外部验证优先 | 验证要求升级 |
| 2025 | 可解释性 + 外部验证 | 新常态 |
| 2026+ | 前瞻性验证 / RCT | 下一门槛 |

### 8.2 最佳实践检查清单

1. ☐ 样本量 >500（理想 >5000）
2. ☐ 外部验证（独立中心或时间分割）
3. ☐ 报告 AUC + 灵敏度 + 特异度 + PPV/NPV
4. ☐ 可解释性分析（SHAP 或 attention map）
5. ☐ 与现有临床标准/评分对比
6. ☐ 讨论临床可操作性（不仅是性能数字）
7. ☐ 代码/模型可复现性声明
8. ☐ 偏倚分析（年龄、性别、种族子群体性能）

### 8.3 避免的常见问题

- 不要报告看起来"太好"的 AUC（>0.95 在外部数据上很可能不可复现）
- 不要用"AI"作为卖点而忽视临床问题本身的价值
- 不要在 ECG 任务上默认使用最复杂的模型（ResNet 可能不比 XGBoost 好）
- 不要忽视预处理和数据质量对结果的影响

---

*报告生成时间: 2026-05-26 | 数据: PubMed 160 篇 AI/ML in EP 文章 | 分析方法: Python 多维分类 + 性能指标提取 + 定性深度阅读*
