---
title: 生成式重建：从几何恢复到内容生成
slug: generative-reconstruction
date: '2026-07-25'
tags:
- 3D重建
- 前馈模型
- 生成先验
- 基础模型
- 4D重建
summary: 从 NeRF 到 3DGS，从逐场景优化到前馈重建——当生成模型的先验知识遇上3D视觉，重建不再是"恢复已有"，而是"推断缺失"。涵盖 DUSt3R
  家族爆发、VGGT 优化浪潮、扩散先验注入、4D 生成、语义 3D、世界模型等 60+ 篇 2025-2026 最新进展。
---

# 生成式重建：从几何恢复到内容生成

## 时间线

2006
**Photo Tourism** — 开创性 SfM 工作，从 Flickr 照片重建著名景点三维模型

2020
**NeRF** — 神经辐射场，用 MLP 表示场景 + 可微渲染，照片级新视角合成

2021
**PixelNeRF** — 第一个前馈 NeRF 方法，训练一次即可推理新场景

2023
**3DGS** — 三维高斯溅射，显式表示 + 实时渲染  
**DUSt3R** — 直接预测像素级三维坐标，端到端几秒钟出点云+位姿

2024
**pixelSplat** / **MVSplat** — 前馈 3DGS 重建  
**LRM** — 大型重建模型，5 亿参数，单图 5 秒出 NeRF  
**LVSM** — 纯 Transformer 视图合成，抛弃显式 3D 表示  
**MVSplat360** — 首次将扩散先验注入前馈 3DGS  
**LatentSplat** — 潜空间语义高斯 + 变分 3D 表示  
**L4GM** — 大型 4D 高斯重建模型

2025
**VGGT** — 统一基础模型，同时做位姿/深度/点云/光流  
**Matrix3D** — 多模态 DiT，掩码学习统一位姿/深度/新视角合成  
**MUSt3R** — 对称多视图架构，支持千视图级大规模重建  
**FlashVGGT** — 推理时间仅为 VGGT 的 9.3%，可扩展至 3000+ 视图  
**Bolt3D** — 潜扩散模型前馈 3D 场景生成，7 秒完成，推理成本降低 300×  
**4D-LRM** / **4DNeX** — 前馈 4D 重建与生成  
**STORM** — 200ms 完成大规模动态户外场景重建  
**OracleGS** — "提议-验证"框架，用 MVS 验证扩散模型的"幻觉"

2026
**PhysGM** — 大型物理高斯模型，单次前向传播预测 3D + 物理属性  
**Diff4Splat** — 视频扩散先验 + 几何运动约束，单图到可控 4D（CVPR 2026）

---

## 序章：一个根本问题

三维重建是计算机视觉的核心任务之一。它的目标很简单：**从二维图像中恢复三维世界**。

但这个问题背后隐藏着一个更深的哲学分歧：重建到底是"恢复已有"，还是"推断缺失"？

传统方法认为：重建就是恢复。相机拍到了什么，就还原什么。没拍到的部分？那是未知的，不应该瞎猜。

但新一代研究者说：重建应该是推断。你没拍到的部分，我可以"想象"出来——而且想象得还挺准。

这就是**生成式重建（Generative Reconstruction）**的故事。它不是渐进式的改进，而是一次根本性的范式转变。

---

## 第一章：传统重建的困境（2006-2022）

### SfM 和 MVS：几何派的黄金时代

2006 年，Noah Snavely 等人在 SIGGRAPH 上发表了一篇开创性论文——*Photo Tourism*。他们从 Flickr 上收集了大量游客照片，通过多视图几何约束，重建出了罗马斗兽场、巴黎圣母院等著名景点的三维模型。

这就是 **SfM（Structure-from-Motion）**的核心思想：从多张照片中恢复相机位姿和稀疏点云。

随后，**MVS（Multi-View Stereo）**进一步 densify 了点云——从稀疏的几千个点变成密集的几百万个点。

想象你站在埃菲尔铁塔前，用相机拍了 100 张照片。SfM 能从这些照片中找到几千个特征点，恢复出相机在哪里、铁塔的大致形状。MVS 则能把这些点变密，生成一个看起来像铁塔的三维模型。

这套方法统治了三维重建领域十几年。但它有一个根本性的局限：**逐场景优化**。

每个场景都需要独立的优化过程，耗时从分钟到小时不等。而且它只能"恢复已有"——如果某个角度没拍到，那就是空洞，模型不会帮你"脑补"。

### NeRF：神经渲染的革命

2020 年，一个叫做 **NeRF（Neural Radiance Fields）** 的工作横空出世 [[1]](https://arxiv.org/abs/2003.08934)。

NeRF 的核心思想很优雅：用一个神经网络表示整个场景。输入一个三维坐标和观察方向，输出颜色和密度。

```
MLP(x, y, z, θ, ϕ) → (颜色, 密度)
```

具体来说，网络输出体密度 $\sigma$ 和视图相关颜色 $\mathbf{c}$，然后通过**体渲染（Volume Rendering）**沿射线 $\mathbf{r}(t) = \mathbf{o} + t\mathbf{d}$ 积分：

$$C(\mathbf{r}) = \int\_{t\_n}^{t\_f} T(t)\, \sigma(\mathbf{r}(t))\, \mathbf{c}(\mathbf{r}(t), \mathbf{d})\, dt, \quad T(t) = \exp\!\left(-\int\_{t\_n}^{t} \sigma(\mathbf{r}(s))\, ds\right)$$

然后通过可微渲染，让这个网络"学会"从 2D 图像中恢复 3D 场景。

效果是惊人的：NeRF 能生成照片级真实感的新视角合成。你从没见过这个角度，但它能"画"出来，而且看起来完全真实。

但 NeRF 继承了 SfM/MVS 的致命缺陷：**逐场景优化**。每个场景都要重新训练一个网络，耗时几十分钟到几小时。它不能"举一反三"——训练时没见过的新场景，它无能为力。

---

## 第二章：前馈重建的革命（2021-2024）

### PixelNeRF：第一次尝试

2021 年，Alex Yu 等人提出了 **PixelNeRF** [[2]](https://arxiv.org/abs/2012.02190)——第一个"前馈"NeRF 方法。

它的思路是：不再为每个场景单独训练一个网络，而是学习一个**通用的映射函数**。输入图像，直接输出 NeRF 参数。

这意味着：训练一次，推理时只需要一次前向传播（几秒钟），就能重建新场景。

但 PixelNeRF 的性能有限——它只能处理简单的物体，复杂场景效果不佳。

### DUSt3R：几何派的反击

2023 年，Meta FAIR 的 Shuzhe Wang 等人发布了一个大胆的工作——**DUSt3R** [[3]](https://arxiv.org/abs/2312.14132)。

DUSt3R 的核心洞察是：**与其预测复杂的 NeRF 或 3DGS，不如直接预测每个像素的三维坐标**。

```
图像 → 网络 → 每个像素的 (x, y, z) 坐标
```

形式化地，给定图像对 $(\mathbf{I}\_1, \mathbf{I}\_2)$，DUSt3R 的 Transformer 编码器-解码器直接回归**点图（Pointmap）**：

$$\hat{\mathbf{P}}\_1, \hat{\mathbf{P}}\_2 = f\_\theta(\mathbf{I}\_1, \mathbf{I}\_2), \quad \hat{\mathbf{P}} \in \mathbb{R}^{H \times W \times 3}$$

每个像素映射到三维空间中的一个点。损失函数是简单的 $L\_2$ 回归：$\mathcal{L} = \|\hat{\mathbf{P}} - \mathbf{P}^\*\|\_2^2$。

就这么简单。没有复杂的 3D 表示，没有耗时的优化。输入图像，输出点云。

更惊人的是：DUSt3R 同时预测相机位姿。你给它两张照片，它不仅能重建三维场景，还能告诉你相机在哪里、朝哪个方向。

传统方法需要：先跑 SfM 恢复位姿 → 再跑 MVS 生成点云 → 再跑网格重建。DUSt3R 一步到位：输入图像，输出点云 + 位姿。端到端，几秒钟。

DUSt3R 的意义在于：它证明了**前馈重建可以比传统方法更快、更简单，而且效果相当**。

### 3DGS：渲染派的逆袭

2023 年，另一个工作彻底改变了 3D 表示的格局——**3D Gaussian Splatting（3DGS）** [[4]](https://arxiv.org/abs/2308.04079)。

3DGS 的核心思想是：用几百万个各向异性的三维高斯椭球表示场景。每个高斯 $\mathcal{G}\_i$ 由位置 $\boldsymbol{\mu}\_i$、协方差 $\boldsymbol{\Sigma}\_i$、不透明度 $\alpha\_i$ 和球谐颜色 $\mathbf{c}\_i$ 参数化：

$$\mathcal{G}\_i(\mathbf{x}) = \exp\!\left(-\tfrac{1}{2}(\mathbf{x}-\boldsymbol{\mu}\_i)^T \boldsymbol{\Sigma}\_i^{-1} (\mathbf{x}-\boldsymbol{\mu}\_i)\right)$$

渲染时按深度排序，做 alpha blending：

$$C = \sum\_{i \in \mathcal{N}} c\_i \, \alpha\_i \prod\_{j=1}^{i-1}(1 - \alpha\_j)$$

相比 NeRF 的隐式表示（MLP），3DGS 是显式的——你可以直接看到、编辑、操作这些高斯。

更重要的是：3DGS 支持**实时渲染**。NeRF 渲染一帧需要几秒，3DGS 只需要几毫秒。

很快，研究者开始把 3DGS 和前馈重建结合：

- [**pixelSplat**](https://dcharatan.github.io/pixelsplat) [[5]](https://arxiv.org/abs/2312.12337)：输入两张图像，直接预测 3DGS 参数。核心是用可微的 reparameterization trick 从高斯分布中采样均值：$\boldsymbol{\mu}\_i = \boldsymbol{\mu}\_i^{\text{pred}} + \sigma\_i \cdot \boldsymbol{\epsilon}$
- [**MVSplat**](https://donydchen.github.io/mvsplat) [[6]](https://arxiv.org/abs/2403.14627)：用平面扫描代价体（Cost Volume）定位高斯中心。在深度假设 $\{d\_k\}$ 上构建代价体，跨视图特征相似度提供几何线索：$\mathbf{C}(\mathbf{p}, d\_k) = \frac{1}{N}\sum\_{j} \mathbf{F}\_1(\mathbf{p})^T \mathbf{F}\_j(\mathbf{w}(\mathbf{p}, d\_k))$

现在，前馈重建有了两条路线：

- **点图路线（DUSt3R）**：直接预测像素级 3D 坐标，简单快速
- **3DGS 路线（pixelSplat）**：预测高斯参数，支持高质量渲染

### 大规模前馈模型：三条路线

2024 年，"前馈"思想开始和"大模型"碰撞。但怎么把大模型用到 3D 重建？研究者分成了三个阵营。

第一条路线：**大模型 + 显式 3D 表示**。代表是 **LRM** [[7]](https://arxiv.org/abs/2311.04400)——5 亿参数的 Transformer，输入一张图像，5 秒输出完整的 NeRF。它证明了 3D 重建可以走"大模型"路线，训练一次，几秒钟重建新场景。

第二条路线：**大模型 + 抛弃 3D 表示**。**LVSM** [[8]](https://arxiv.org/abs/2410.17242) 更激进——它连 NeRF 和 3DGS 都不要了。一个纯 Transformer，输入视图和位姿，直接输出新视角的图像。没有显式的三维中间表示，没有可微渲染。模型从数据中直接学习"从这个角度看，那个角度应该是什么样"。它的 decoder-only 变体在多个基准上超越了所有先前的方法——甚至不需要 3D 归纳偏置。

第三条路线：**大模型 + 多任务统一**。**Matrix3D** [[9]](https://arxiv.org/abs/2502.07685)（CVPR 2025）用多模态扩散 Transformer 统一了位姿估计、深度预测和新视角合成。它的巧妙之处在于**掩码学习策略**——即使训练数据只有部分模态（比如只有图像-位姿对或图像-深度对），模型也能训练。这让它可以利用大量异构数据，还能通过多轮交互实现细粒度控制。

三条路线，三种哲学：LRM 说"给我一个好的 3D 表示，我用大模型学映射"；LVSM 说"3D 表示是多余的，直接学视图间的映射"；Matrix3D 说"别争了，一个模型做所有任务"。

2025 年，**VGGT** [[10]](https://arxiv.org/abs/2503.11651) 把第三条路线推向了极致。它的核心洞察是：**位姿估计、深度预测、点云生成、光流估计，这些任务本质上是相关的**。一个 Transformer 同时输出：

$$\{\hat{\mathbf{P}}, \hat{\mathbf{D}}, \hat{\mathbf{T}}, \hat{\mathbf{F}}\} = f\_\theta(\mathbf{I}\_{1:N})$$

通过多任务预训练，任务间共享特征表示，互相提供监督信号。VGGT 在各个任务上都达到了 SOTA，而且可以泛化到未见过的场景。

---

## 第三章：生成先验的注入（2024-2025）

前馈重建解决了"速度"问题，但遇到了新挑战：**稀疏输入**。

如果你只有一张图像，或者视角很稀疏，前馈方法的效果会急剧下降。因为它只能"看到什么重建什么"——没看到的部分，就是空洞。

这时候，一个关键洞察出现了：**生成模型（尤其是扩散模型）已经学会了丰富的视觉先验。能不能把这些先验"注入"到重建中？**

### MVSplat360：扩散先验的第一次尝试

2024 年，研究者提出了 **MVSplat360** [[11]](https://arxiv.org/abs/2411.04924)——第一个把扩散模型和前馈 3DGS 结合的工作。

它的思路是：先用前馈方法预测初始的 3DGS，然后用 Stable Video Diffusion 模型"细化"渲染结果。

具体来说，前馈模型预测的 3DGS 参数 $\hat{\boldsymbol{\theta}}\_{\text{3DGS}}$ 渲染出初始图像，然后送入预训练的 SVD 进行条件去噪。扩散模型的作用是：**"脑补"缺失的部分**。如果你只看到物体的正面，扩散模型能根据它学到的先验，"想象"出背面应该是什么样子。

去噪过程可以形式化为：给定含噪渲染 $\mathbf{x}\_t$，单步去噪网络预测干净结果：

$$\hat{\mathbf{x}}\_0 = \epsilon\_\theta(\mathbf{x}\_t, t, \mathbf{c}\_{\text{3DGS}})$$

其中 $\mathbf{c}\_{\text{3DGS}}$ 是前馈 3DGS 提供的几何条件。

你给 MVSplat360 一张椅子的正面照片。前馈方法只能重建正面。但扩散模型"知道"椅子有四条腿、有靠背。它能"幻觉"出背面和侧面，生成一个完整的 3D 椅子。

### LatentSplat：潜空间中的语义高斯

同年，**LatentSplat** [[12]](https://arxiv.org/abs/2403.16292) 提出了一个更优雅的方案：**在潜空间中预测语义高斯**。

传统前馈方法直接在像素空间预测高斯参数。LatentSplat 的做法是：先在**3D 潜空间**中预测语义高斯，然后用一个轻量级的 2D 生成架构解码渲染。核心是**变分 3D 高斯**表示——每个高斯编码的不是确定值，而是一个分布：

$$q(\mathbf{z}\_i | \mathbf{x}) = \mathcal{N}(\boldsymbol{\mu}\_\phi(\mathbf{x}),\, \boldsymbol{\sigma}\_\phi(\mathbf{x}))$$

这样做的好处是：潜空间更紧凑，能捕捉更丰富的语义信息；而且可以用预训练的 2D 生成模型作为解码器，注入强大的视觉先验。

### 单步扩散细化：Difix3D+ 与 ProSplat

2025 年，两个独立的工作几乎同时提出了同一个想法：**用单步扩散模型做后处理增强**。

**Difix3D+** [[13]](https://arxiv.org/abs/2503.09585) 来自 NVIDIA / Meta 团队。它的核心是一个叫 Difix 的单步图像扩散模型——输入一张有伪影的渲染图，一步去噪，输出干净的结果。把它插入到任何前馈 3DGS 流程的末端，就能"修复"新视角渲染中的模糊和伪影。

**ProSplat** [[14]](https://arxiv.org/abs/2506.07670) 则更专注于**宽基线稀疏视角**场景。它额外引入了对极约束注意力（DWEA）和最大重叠参考视图注入（MORI），确保扩散细化不会破坏多视图几何一致性。

### "提议-验证"范式：OracleGS 与 CoherentGS

但扩散模型的"幻觉"真的可靠吗？2025 年，一个关键问题浮出水面：**如何确保生成先验不会引入结构性错误？**

**OracleGS** [[15]](https://arxiv.org/abs/2509.23258) 提出了一个优雅的"提议-验证"框架。它的思路是：先用 3D 感知扩散模型"提议"一个完整的场景，然后用多视图立体（MVS）模型作为"3D 感知 oracle"来"验证"——通过注意力图揭示哪些区域有多视图证据支持，哪些区域是高不确定性区域。最终用不确定性加权损失优化 3DGS，过滤掉"幻觉"伪影，保留合理的补全。

OracleGS 就像一个谨慎的画家：先用想象力画出整幅画（扩散模型提议），然后用尺子量一量哪些部分是准确的（MVS 验证），最后只保留画得对的部分。

**CoherentGS** [[16]](https://arxiv.org/abs/2512.10369) 则走得更远——它用**双先验策略**同时解决稀疏视图和运动模糊两个问题：一个专业的去模糊网络恢复锐利细节，一个扩散模型提供几何先验填充未观测区域。两者通过一致性引导的相机探索模块协调工作。

同期还有 **FixingGS** [[17]](https://arxiv.org/abs/2509.18759)（免训练方法蒸馏扩散先验）、**GSFix3D** [[18]](https://arxiv.org/abs/2508.14717)（定制微调的潜扩散模型适配多种环境）、**ExploreGS** [[19]](https://arxiv.org/abs/2508.06014)（信息增益驱动的虚拟相机 + 视频扩散先验）等工作，共同构成了"生成增强"这一活跃方向。

---

## 第四章：走向基础模型（2024-2025）

DUSt3R 证明了前馈重建可以又快又好。但它有一个根本性的限制：**只能处理两张图像**。现实世界不是两张照片——你可能有几十张、几百张、甚至上千张。怎么办？

### 从成对到多视图

Meta FAIR 的团队用两步回答了这个问题。

第一步是 **MASt3R** [[20]](https://arxiv.org/abs/2406.09756)。它在 DUSt3R 的基础上加了一个密集局部特征头——不仅能重建 3D 场景，还能做特征匹配。这意味着它可以接入 SfM 和 SLAM 的管线，不再是一个孤立的"点云生成器"。

第二步是 **MUSt3R** [[21]](https://arxiv.org/abs/2503.01661)。它把 DUSt3R 的非对称架构改成了对称的，并引入多层内存机制，把计算复杂度从 $O(n^2)$ 降到了可管理的范围。结果：可以处理**数千张图像**的大规模集合，以高帧率推断 3D 点图。

DUSt3R 像一个只能看两张照片的画家。MUSt3R 则像一个能同时看几千张照片的画家——而且看得又快又好。

### VGGT：统一的野心

如果说 MUSt3R 解决的是"多视图"问题，那 **VGGT** [[10]](https://arxiv.org/abs/2503.11651) 解决的是"多任务"问题。

VGGT 的野心很大：一个 Transformer 同时做位姿估计、深度预测、点云生成、光流估计。它的核心洞察是——这些任务本质上是相关的。深度图可以帮助位姿估计，位姿可以帮助点云生成，点云可以反过来约束深度。通过多任务预训练，任务间共享特征表示，互相提供监督信号。

但 VGGT 有一个现实问题：**太慢了**。它需要对所有图像 token 做密集全局注意力，token 数量随视图数平方增长。

这催生了一轮优化竞赛。**FastVGGT** 用免训练 token 合并提速 2 倍，**Sparse VGGT** 用自适应块稀疏核提速 3 倍，**Evict3R** 用 KV 缓存驱逐减少 50% 内存。其中最激进的是 **FlashVGGT** [[22]](https://arxiv.org/abs/2512.01540)：它不再对所有 token 做密集注意力，而是把每帧压缩为一组描述子 token，全局注意力变成图像 token 与描述子的交叉注意力。结果：1000 张图像的推理时间仅为 VGGT 的 **9.3%**，可扩展到 3000+ 视图。

### 基础模型也需要"微调"

基础模型见多识广，但细节不够。2025 年出现了两个有趣的"元学习"方向。

**Fin3R** [[23]](https://arxiv.org/abs/2511.22429)（NeurIPS 2025）的思路很简单：冻结解码器，只用轻量 LoRA 微调图像编码器，从强单目教师模型蒸馏精细几何细节。在 DUSt3R、MASt3R、VGGT 上都有效，几乎不增加推理成本。

**Test3R** [[24]](https://arxiv.org/abs/2506.13750) 更激进——它甚至不需要训练。利用图像三元组 $(I\_1, I\_2, I\_3)$，在测试时通过自监督目标最大化两个重建的几何一致性。几乎零成本，普遍适用。

### 最终目标：大规模 SfM

所有这些努力的终极目标是：**用前馈模型替代传统的逐场景 SfM 管线**。

2025 年，多个工作从不同角度逼近这个目标。**Regist3R** [[25]](https://arxiv.org/abs/2504.12356) 用增量式配准首次实现千视图级别的大规模重建。**Light3R-SfM** [[26]](https://arxiv.org/abs/2501.14914) 用可学习注意力替代传统全局优化。**SAIL-Recon** [[27]](https://arxiv.org/abs/2508.17972) 给场景回归网络赋予视觉定位能力。**AMB3R** [[28]](https://arxiv.org/abs/2511.20343) 用体积场景表示做后端，甚至超越了基于优化的 SLAM 方法。

这些工作共同说明了一件事：**前馈重建不再只是"玩具"——它开始能处理真实世界的大规模场景了**。

---

## 第五章：3DGS 的几何觉醒（2025）

第四章讲的是点图路线——直接预测像素级 3D 坐标。另一条路线是 3DGS——预测高斯参数，支持高质量渲染。

2024 年，pixelSplat 和 MVSplat 证明了前馈 3DGS 可以工作。但 2025 年，一个尴尬的事实浮出水面：**大多数前馈 3DGS 方法预测的高斯方向/尺度没有几何含义**。

原因很简单：它们通过视图合成损失训练，但视图合成本身对方向和尺度的约束太弱。模型可以"作弊"——用几何上不合理的高斯参数达到好的渲染效果。看起来不错，但几何是错的。

### G3Splat：几何先验的注入

**G3Splat** [[29]](https://arxiv.org/abs/2512.17547) 解决了这个问题。它引入了**可微几何先验**：鼓励每个像素的高斯保持在 viewing ray 上，并根据局部表面方向定位。这些先验是架构无关的，可以插入任何已有的骨干网络。结果：高斯的几何保真度显著提升——在新视角深度、mesh 重建和位姿估计上都达到了 SOTA。

G3Splat 的意义在于：它揭示了一个深层问题——**渲染质量不等于几何质量**。未来的前馈 3DGS 方法不能只看 PSNR，还要看几何是否合理。

### 从几何到语义

几何问题解决后，下一个挑战是：**真实场景的多样性**。输入视图可能基线很大也可能很小，场景可能简单也可能复杂。

**MuGS** [[30]](https://arxiv.org/abs/2508.04297)（ICCV 2025）融合了 MVS 和单目深度估计的特征来处理多基线问题。**H3R** [[31]](https://arxiv.org/abs/2508.03118)（ICCV 2025）则提出了一个混合框架——体积潜空间融合 + 注意力特征聚合。它还发现了一个有趣的事实：**空间对齐的基础模型（如 SD-VAE）在重建任务上大幅优于语义对齐的模型（如 DINOv2）**——语义表示和空间重建之间存在根本矛盾。

更激动人心的趋势是**将语义理解融入 3D 重建**。**UniForward** [[32]](https://arxiv.org/abs/2506.09378) 是第一个统一 3D 场景和语义场的前馈模型——从稀疏无位姿图像中预测带语义特征的 3D 高斯，支持开放词汇的密集分割。**TextSplat** [[33]](https://arxiv.org/abs/2504.09588) 则用文本引导融合深度先验和语义信息。这些工作共同指向一个方向：**3D 重建不再只是"几何"的，而是"语义"的**。

### 从短序列到长序列

前馈 3DGS 的最后一个挑战是**长视频序列**。逐像素预测高斯会导致大量冗余——相邻帧的高斯高度重叠，但不完全一致。

**SaLon3R** [[34]](https://arxiv.org/abs/2510.15072) 是第一个支持 50+ 视图在线重建的可泛化 GS 方法。它引入紧凑的锚点原语，通过显著性感知量化消除 50%-90% 的冗余，再用 3D Point Transformer 精炼锚点属性。在压缩方面，一个基于 Morton 序列化的前馈压缩框架 [[35]](https://arxiv.org/abs/2512.00877) 实现了 20× 压缩比——全部在前馈推理中完成。

---

## 第六章：动态世界的挑战（2024-2026）

真实世界是动态的。人在走动，车在行驶，树叶在飘动。静态重建无法捕捉这些变化。

前馈重建进入动态世界，面临一个根本性的选择：**在线流式**还是**离线批处理**？

### 在线流式：逐帧跟踪

[**StreamSplat**](https://streamsplat3d.github.io/) [[36]](https://arxiv.org/abs/2506.08862) 选择了在线流式。它逐帧处理视频，增量更新 3DGS。每处理一帧，它不仅更新高斯的位置和颜色，还通过**双向变形场**预测每个高斯的运动轨迹：

$$\boldsymbol{\mu}\_i^{t+1} = \boldsymbol{\mu}\_i^t + \Delta\mathbf{v}\_i^t, \quad \Delta\mathbf{v}\_i^t = g\_\theta(\boldsymbol{\mu}\_i^t, \mathbf{F}^t)$$

你给 StreamSplat 一段行人在街上走动的视频。它逐帧处理，实时更新场景。行人移动时，对应的高斯也跟着移动——而不是在每一帧都重新生成。

但流式方法有一个固有缺陷：它只能看到当前帧和历史信息，不能"展望未来"。**DGS-LRM** [[37]](https://hubert0527.github.io/dgslrm/) 用前馈大模型解决了这个问题——首个从单目视频预测可变形 3D 高斯的方法，实时、可泛化，质量可比肩基于优化的方法。**STORM** [[38]](https://jiawei-yang.github.io/STORM/) 则专注于大规模户外场景，用自监督场景流聚合所有帧的高斯至目标时间步——**200ms 完成**，还能自动捕获动态实例。

### 离线批处理：一次看完整个视频

离线方法可以看到整个视频，更好地保证时序一致性。

[**L4GM**](https://research.nvidia.com/labs/toronto-ai/l4gm) [[39]](https://arxiv.org/abs/2406.10324) 是第一个大型 4D 重建模型。它基于 LGM 扩展到时间维度，加入**时间自注意力层**让不同帧的高斯互相"看到"彼此。**4D-LRM** [[40]](https://4dlrm.github.io/) 更进一步——输入不受约束的视图和时间戳，渲染任意新视角-时间组合，单 A100 GPU 上 1.5 秒重建 24 帧序列。

但这些都是"重建"——需要视频输入。能不能从**单张图像**生成 4D 场景？

**4DNeX** [[41]](https://4dnex.github.io/) 是第一个做到这一点的前馈框架。它构建了 4DNeX-10M 大规模数据集（1000 万高质量 4D 标注），将预训练视频扩散模型适配为 4D 建模工具。**Diff4Splat** [[42]](https://paulpanwang.github.io/Diff4Splat)（CVPR 2026）则走得更远——给定一张图像、一条相机轨迹和可选文本提示，在**单次前向传播**中直接预测可变形 3D 高斯场，编码外观、几何和运动，30 秒内完成。

（同期还有 **C4D** [[43]](https://littlepure2333.github.io/C4D) 利用光流和点跟踪将 3D 扩展到 4D，**D²USt3R** [[44]](https://cvlab-kaist.github.io/DDUSt3R/) 直接回归静态-动态对齐点图，**LIM** [[45]](https://arxiv.org/abs/2503.22537) 在连续时间插值隐式 3D 表示。）

---

## 第七章：从重建到世界模型（2025-2026）

到 2025 年，前馈重建已经解决了"速度"问题（毫秒级推理）、"泛化"问题（跨场景）、"几何"问题（G3Splat）、"语义"问题（UniForward）、"动态"问题（4D-LRM）。

下一步是什么？**从"重建"走向"生成"和"模拟"**。

### 3D 场景生成

**Bolt3D** [[46]](https://szymanowiczs.github.io/bolt3d)（ICCV 2025）用潜扩散模型在**不到 7 秒**内直接采样一个 3D 场景表示——比先前需要逐场景优化的方法快 300 倍。这不再是"重建"了，这是"生成"。

生成之后还需要编辑。**InstaInpaint** [[47]](https://dhmbb2.github.io/InstaInpaint_page/) 用掩码微调的 LRM 在 **0.4 秒**内完成 3D 场景修复。**Edit3r** [[48]](https://edit3r.github.io/edit3r/) 从无位姿编辑图像单次前向传播重建和编辑 3D 场景。**Tinker** [[49]](https://aim-uofa.github.io/Tinker) 利用扩散模型的 3D 感知，从一张图像实现多视图一致的编辑。

### 物理真实材质

但"生成"不只是几何——还需要**物理真实的材质**。目前的 3D 重建看起来真实，但不能"重光照"——因为缺少 PBR 属性（albedo、roughness、metallic）。

**MGM** [[50]](https://arxiv.org/abs/2509.22112) 微调了多视图材质扩散模型，让高斯不仅编码颜色，还编码 PBR 材质通道，支持动态重光照。**LIRM** [[51]](https://arxiv.org/abs/2504.20026)（CVPR 2025）在不到一秒内联合重建形状、材质和视角相关辐射场。**SViM3D** [[52]](http://svim3d.aengelhardt.com)（ICCV 2025）扩展潜视频扩散模型输出 PBR 参数和表面法线。

### 自动驾驶：最严苛的考验

自动驾驶对 3D 重建提出了最严苛的要求：**大规模、动态、实时、几何精确、可生成**。

**LSD-3D** [[53]](https://light.princeton.edu/LSD-3D) 直接生成大规模 3D 驾驶场景，支持地图布局条件化——桥接了神经重建（几何精确但不可控）和扩散生成（可控但缺乏几何基础）之间的鸿沟。**DriveGen3D** [[54]](https://lhmd.top/drivegen3d)（ICME 2026 Oral）统一了高效视频生成和前馈 3D 重建，支持 800×424 分辨率、12 FPS 的驾驶视频生成和对应 3D 场景重建。

想象你坐在自动驾驶汽车里。LSD-3D 可以根据地图布局"想象"出前方场景的完整 3D 模型。DriveGen3D 可以生成任意长度的驾驶视频，同时保持 3D 一致性。STORM 能在 200ms 内重建整个动态场景。这不是科幻——这些都在 2025 年实现了。

### 物理可交互性

但"生成"的终极目标不只是视觉真实——而是**物理可交互**。

如果你让机器人去抓一个重建出来的杯子，它可能会失败——因为重建的杯子没有物理属性（质量、摩擦力、刚度）。**PIXIE** [[55]](https://pixie-3d.github.io/) 从像素快速学习 3D 物理属性，利用 CLIP 特征零样本泛化到真实世界。**PhysGM** [[56]](https://arxiv.org/abs/2508.13911)（CVPR 2026）更进一步——大型物理高斯模型，单次前向传播同时预测 3D 场景和物理属性。

### 世界模型的萌芽

这些工作共同指向一个更宏大的愿景：**构建几何一致的世界模型**——不仅能重建和生成 3D 场景，还能模拟物理世界的演化。

**FantasyWorld** [[57]](https://arxiv.org/abs/2509.21657) 统一了视频预测和 3D 预测。**WorldPack** [[58]](https://arxiv.org/abs/2512.02473) 基于 3D 空间相关性动态压缩视频帧，扩展世界模型的有效上下文。**MILO** [[59]](https://arxiv.org/abs/2512.01821) 模拟人类空间想象力，增强多模态大语言模型的空间推理。

从"重建"到"生成"，从"生成"到"模拟"，从"模拟"到"世界模型"——这是三维重建的下一个十年。

---

## 第八章：那些还没解决的问题

### 泛化的天花板

目前的前馈方法大多在室内场景或简单物体上训练。部署到户外场景时，效果急剧下降。

不过，**LAM3C** [[60]](https://ryosuke-yamada.github.io/lam3c/)（CVPR 2026）给出了一个令人鼓舞的信号：它从互联网视频（房地产漫游视频）生成的点云进行自监督 3D 预训练——**完全不需要真实 3D 扫描**。在室内语义分割上，它竟然超越了使用真实 3D 扫描的方法。这说明：**互联网视频是 3D 自监督学习的丰富数据源**。

### "幻觉"的可靠性

生成式重建的核心优势是"脑补"缺失部分。但这带来了一个风险：**幻觉可能不可靠**。

你给模型一张汽车的照片，让它"脑补"出背面。如果训练数据里大多是轿车，它可能会生成一个轿车的背面。但如果实际是一辆 SUV，幻觉就错了。

在安全关键应用中，这种错误可能是致命的。OracleGS 的"提议-验证"范式是一个有前景的方向。**MEt3R** [[61]](https://geometric-rl.mpi-inf.mpg.de/met3r/) 则提出了一个独立于采样过程的**多视图一致性度量**——为评估生成式重建的可靠性提供了工具。

### 从 3D 重建到世界模拟

物理可交互性和世界模型已经在第七章讨论过。这里只补充一点：这些方向还处于非常早期的阶段。PIXIE 和 PhysGM 只处理了简单的物理属性（弹性、刚度），距离真正的"物理模拟"还很远。FantasyWorld 和 WorldPack 只处理了简单的视频预测，距离真正的"世界模拟"更远。

但这正是最令人兴奋的地方。**三维重建正在从一个"视觉"问题变成一个"认知"问题**——不只是"看到什么重建什么"，而是"看到什么理解什么、预测什么、模拟什么"。

---

## 尾声：一个隐喻

如果把三维重建比作"画画"，那么：

**传统方法（SfM/MVS）是"写生"。** 你看到什么，就画什么。没看到的部分，留白。

**NeRF 是"照片级写实画"。** 你能画出从未见过的角度，但每幅画都要花几个小时。

**前馈重建是"速写"。** 几秒钟就能画完，但细节不够。

**生成式重建是"有想象力的速写"。** 不仅画得快，还能"脑补"出没看到的部分——而且想象得还挺准。

从"恢复已有"到"推断缺失"，从"逐场景优化"到"一次前向传播"，从"几何重建"到"生成式重建"——这是三维重建领域的范式转变。

而这场变革的参与者——Meta FAIR 的 DUSt3R 家族、3DGS 的发明者、扩散模型的研究者、大模型的布道者——每一个人都在试图回答同一个问题：

**机器能否像人类一样，从有限的观察中"想象"出完整的世界？**

答案正在越来越近。

---

## 参考文献

[1] Mildenhall, B., et al. "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis." *ECCV 2020*. [arXiv:2003.08934](https://arxiv.org/abs/2003.08934)

[2] Yu, A., et al. "pixelNeRF: Neural Radiance Fields from One or Few Images." *CVPR 2021*. [arXiv:2012.02190](https://arxiv.org/abs/2012.02190)

[3] Wang, S., et al. "DUSt3R: Geometric 3D Vision Made Easy." *CVPR 2024*. [arXiv:2312.14132](https://arxiv.org/abs/2312.14132)

[4] Kerbl, B., et al. "3D Gaussian Splatting for Real-Time Radiance Field Rendering." *SIGGRAPH 2023*. [arXiv:2308.04079](https://arxiv.org/abs/2308.04079)

[5] Charat, D., et al. "pixelSplat: 3D Gaussian Splats from Image Pairs for Scalable Generalizable Novel View Synthesis." *CVPR 2024*. [arXiv:2312.12337](https://arxiv.org/abs/2312.12337) · [Project Page](https://dcharat.github.io/pixelsplat)

[6] Chen, C., et al. "MVSplat: Efficient 3D Gaussian Splatting from Sparse Multi-View Images." *ECCV 2024*. [arXiv:2403.14627](https://arxiv.org/abs/2403.14627) · [Project Page](https://donydchen.github.io/mvsplat)

[7] Hong, Y., et al. "LRM: Large Reconstruction Model for Single Image to 3D." *ICLR 2024*. [arXiv:2311.04400](https://arxiv.org/abs/2311.04400) · [Project Page](https://yiconghong.me/LRM)

[8] Jin, H., et al. "LVSM: A Large View Synthesis Model with Minimal 3D Inductive Bias." *arXiv 2024*. [arXiv:2410.17242](https://arxiv.org/abs/2410.17242) · [Project Page](https://haian-jin.github.io/projects/LVSM/)

[9] Lu, Y., et al. "Matrix3D: Large Photogrammetry Model All-in-One." *CVPR 2025*. [arXiv:2502.07685](https://arxiv.org/abs/2502.07685) · [Project Page](https://nju-3dv.github.io/projects/matrix3d)

[10] Wang, S., et al. "VGGT: Visual Geometry Grounded Transformer." *CVPR 2025*. [arXiv:2503.11651](https://arxiv.org/abs/2503.11651)

[11] Chen, Y., et al. "MVSplat360: Feed-Forward 360 Scene Synthesis from Sparse Views." *NeurIPS 2024*. [arXiv:2411.04924](https://arxiv.org/abs/2411.04924) · [Project Page](https://donydchen.github.io/mvsplat360)

[12] Wewer, C., et al. "latentSplat: Autoencoding Variational Gaussians for Fast Generalizable 3D Reconstruction." *arXiv 2024*. [arXiv:2403.16292](https://arxiv.org/abs/2403.16292) · [Project Page](https://geometric-rl.mpi-inf.mpg.de/latentsplat/)

[13] Wu, J. Z., et al. "Difix3D+: Improving 3D Reconstructions with Single-Step Diffusion Models." *arXiv 2025*. [arXiv:2503.09585](https://arxiv.org/abs/2503.09585)

[14] Lu, X., et al. "ProSplat: Improved Feed-Forward 3D Gaussian Splatting for Wide-Baseline Sparse Views." *arXiv 2025*. [arXiv:2506.07670](https://arxiv.org/abs/2506.07670)

[15] Topaloglu, A., et al. "OracleGS: Grounding Generative Priors for Sparse-View Gaussian Splatting." *arXiv 2025*. [arXiv:2509.23258](https://arxiv.org/abs/2509.23258)

[16] Xu, Z., et al. "CoherentGS: Breaking the Vicious Cycle: Coherent 3D Gaussian Splatting from Sparse and Motion-Blurred Views." *arXiv 2025*. [arXiv:2512.10369](https://arxiv.org/abs/2512.10369)

[17] Wang, Z., et al. "FixingGS: Enhancing 3D Gaussian Splatting via Training-Free Score Distillation." *arXiv 2025*. [arXiv:2509.18759](https://arxiv.org/abs/2509.18759)

[18] Wei, J., et al. "GSFix3D: Diffusion-Guided Repair of Novel Views in Gaussian Splatting." *arXiv 2025*. [arXiv:2508.14717](https://arxiv.org/abs/2508.14717)

[19] Kim, M., et al. "ExploreGS: Explorable 3D Scene Reconstruction with Virtual Camera Samplings and Diffusion Priors." *ICCV 2025*. [arXiv:2508.06014](https://arxiv.org/abs/2508.06014)

[20] Leroy, V., et al. "MASt3R: Geometry-Aware Visual Correspondences." *CVPR 2025*. [arXiv:2406.09756](https://arxiv.org/abs/2406.09756)

[21] Cabon, Y., et al. "MUSt3R: Multi-view Network for Stereo 3D Reconstruction." *CVPR 2025*. [arXiv:2503.01661](https://arxiv.org/abs/2503.01661)

[22] Wang, Z. & Xu, D. "FlashVGGT: Efficient and Scalable Visual Geometry Transformers with Compressed Descriptor Attention." *CVPR 2026*. [arXiv:2512.01540](https://arxiv.org/abs/2512.01540)

[23] Ren, W., et al. "Fin3R: Fine-tuning Feed-forward 3D Reconstruction Models via Monocular Knowledge Distillation." *NeurIPS 2025*. [arXiv:2511.22429](https://arxiv.org/abs/2511.22429)

[24] Yuan, Y., et al. "Test3R: Learning to Reconstruct 3D at Test Time." *arXiv 2025*. [arXiv:2506.13750](https://arxiv.org/abs/2506.13750)

[25] Liu, S., et al. "Regist3R: Incremental Registration with Stereo Foundation Model." *ACM MM 2025*. [arXiv:2504.12356](https://arxiv.org/abs/2504.12356)

[26] Elflein, S., et al. "Light3R-SfM: Towards Feed-forward Structure-from-Motion." *arXiv 2025*. [arXiv:2501.14914](https://arxiv.org/abs/2501.14914)

[27] Deng, J., et al. "SAIL-Recon: Large SfM by Augmenting Scene Regression with Localization." *arXiv 2025*. [arXiv:2508.17972](https://arxiv.org/abs/2508.17972)

[28] Wang, H. & Agapito, L. "AMB3R: Accurate Feed-forward Metric-scale 3D Reconstruction with Backend." *arXiv 2025*. [arXiv:2511.20343](https://arxiv.org/abs/2511.20343)

[29] Hosseinzadeh, M., et al. "G3Splat: Geometrically Consistent Generalizable Gaussian Splatting." *arXiv 2025*. [arXiv:2512.17547](https://arxiv.org/abs/2512.17547)

[30] Lou, Y., et al. "MuGS: Multi-Baseline Generalizable Gaussian Splatting Reconstruction." *ICCV 2025*. [arXiv:2508.04297](https://arxiv.org/abs/2508.04297)

[31] Jia, H., et al. "H3R: Hybrid Multi-view Correspondence for Generalizable 3D Reconstruction." *ICCV 2025*. [arXiv:2508.03118](https://arxiv.org/abs/2508.03118)

[32] Tian, Q., et al. "UniForward: Unified 3D Scene and Semantic Field Reconstruction via Feed-Forward Gaussian Splatting." *arXiv 2025*. [arXiv:2506.09378](https://arxiv.org/abs/2506.09378)

[33] Wu, Z., et al. "TextSplat: Text-Guided Semantic Fusion for Generalizable Gaussian Splatting." *arXiv 2025*. [arXiv:2504.09588](https://arxiv.org/abs/2504.09588)

[34] Guo, J., et al. "SaLon3R: Structure-aware Long-term Generalizable 3D Reconstruction from Unposed Images." *arXiv 2025*. [arXiv:2510.15072](https://arxiv.org/abs/2510.15072)

[35] Liu, Z., et al. "Feed-Forward 3D Gaussian Splatting Compression with Long-Context Modeling." *arXiv 2025*. [arXiv:2512.00877](https://arxiv.org/abs/2512.00877)

[36] Wu, Z., et al. "StreamSplat: Towards Online Dynamic 3D Reconstruction from Uncalibrated Video Streams." *ICLR 2026*. [arXiv:2506.08862](https://arxiv.org/abs/2506.08862) · [Project Page](https://streamsplat3d.github.io/)

[37] Lin, C. H., et al. "DGS-LRM: Real-Time Deformable 3D Gaussian Reconstruction From Monocular Videos." *arXiv 2025*. [arXiv:2506.09997](https://arxiv.org/abs/2506.09997) · [Project Page](https://hubert0527.github.io/dgslrm/)

[38] Yang, J., et al. "STORM: Spatio-Temporal Reconstruction Model for Large-Scale Outdoor Scenes." *arXiv 2025*. [arXiv:2501.00602](https://arxiv.org/abs/2501.00602) · [Project Page](https://jiawei-yang.github.io/STORM/)

[39] Ren, J., et al. "L4GM: Large 4D Gaussian Reconstruction Model." *arXiv 2024*. [arXiv:2406.10324](https://arxiv.org/abs/2406.10324) · [Project Page](https://research.nvidia.com/labs/toronto-ai/l4gm)

[40] Ma, Z., et al. "4D-LRM: Large Space-Time Reconstruction Model From and To Any View at Any Time." *arXiv 2025*. [arXiv:2506.18890](https://arxiv.org/abs/2506.18890) · [Project Page](https://4dlrm.github.io/)

[41] Chen, Z., et al. "4DNeX: Feed-Forward 4D Generative Modeling Made Easy." *arXiv 2025*. [arXiv:2508.13154](https://arxiv.org/abs/2508.13154) · [Project Page](https://4dnex.github.io/)

[42] Pan, P., et al. "Diff4Splat: Controllable 4D Scene Generation with Latent Dynamic Reconstruction Models." *CVPR 2026*. [arXiv:2511.00503](https://arxiv.org/abs/2511.00503)

[43] Wang, S., et al. "C4D: 4D Made from 3D through Dual Correspondences." *ICCV 2025*. [arXiv:2510.14960](https://arxiv.org/abs/2510.14960)

[44] Han, J., et al. "D²USt3R: Enhancing 3D Reconstruction for Dynamic Scenes." *NeurIPS 2025*. [arXiv:2504.06264](https://arxiv.org/abs/2504.06264)

[45] Sabathier, R., et al. "LIM: Large Interpolator Model for Dynamic Reconstruction." *arXiv 2025*. [arXiv:2503.22537](https://arxiv.org/abs/2503.22537)

[46] Szymanowicz, S., et al. "Bolt3D: Generating 3D Scenes in Seconds." *ICCV 2025*. [arXiv:2503.14445](https://arxiv.org/abs/2503.14445)

[47] You, J., et al. "InstaInpaint: Instant 3D-Scene Inpainting with Masked Large Reconstruction Model." *arXiv 2025*. [arXiv:2506.10980](https://arxiv.org/abs/2506.10980)

[48] Liu, J., et al. "Edit3r: Instant 3D Scene Editing from Sparse Unposed Images." *arXiv 2025*. [arXiv:2512.25071](https://arxiv.org/abs/2512.25071)

[49] Zhao, C., et al. "Tinker: Diffusion's Gift to 3D--Multi-View Consistent Editing From Sparse Inputs." *arXiv 2025*. [arXiv:2508.14811](https://arxiv.org/abs/2508.14811)

[50] Ye, J., et al. "MGM: Large Material Gaussian Model for Relightable 3D Generation." *arXiv 2025*. [arXiv:2509.22112](https://arxiv.org/abs/2509.22112)

[51] Li, Z., et al. "LIRM: Large Inverse Rendering Model for Progressive Reconstruction of Shape, Materials and View-dependent Radiance Fields." *CVPR 2025*. [arXiv:2504.20026](https://arxiv.org/abs/2504.20026)

[52] Engelhardt, A., et al. "SViM3D: Stable Video Material Diffusion for Single Image 3D Generation." *ICCV 2025*. [arXiv:2510.08271](https://arxiv.org/abs/2510.08271)

[53] Ost, J., et al. "LSD-3D: Large-Scale 3D Driving Scene Generation with Geometry Grounding." *arXiv 2025*. [arXiv:2508.19204](https://arxiv.org/abs/2508.19204)

[54] Wang, W., et al. "DriveGen3D: Boosting Feed-Forward Driving Scene Generation with Efficient Video Diffusion." *ICME 2026*. [arXiv:2510.15264](https://arxiv.org/abs/2510.15264)

[55] Le, L., et al. "PIXIE: Fast and Generalizable Supervised Learning of 3D Physics from Pixels." *arXiv 2025*. [arXiv:2508.17437](https://arxiv.org/abs/2508.17437) · [Project Page](https://pixie-3d.github.io/)

[56] Lv, C., et al. "PhysGM: Large Physical Gaussian Model for Feed-Forward 4D Synthesis." *CVPR 2026*. [arXiv:2508.13911](https://arxiv.org/abs/2508.13911)

[57] Dai, Y., et al. "FantasyWorld: Geometry-Consistent World Modeling via Unified Video and 3D Prediction." *arXiv 2025*. [arXiv:2509.21657](https://arxiv.org/abs/2509.21657)

[58] Oshima, Y., et al. "WorldPack: Dynamic Frame Compression for Long-context Video World Modeling." *arXiv 2025*. [arXiv:2512.02473](https://arxiv.org/abs/2512.02473)

[59] Cao, M., et al. "MILO: Learning Scene Geometry via Implicit Spatial World Modeling." *arXiv 2025*. [arXiv:2512.01821](https://arxiv.org/abs/2512.01821)

[60] Yamada, R., et al. "3D sans 3D Scans: Scalable Pre-training from Video-Generated Point Clouds." *CVPR 2026*. [arXiv:2512.23042](https://arxiv.org/abs/2512.23042)

[61] Asim, M., et al. "MEt3R: Measuring Multi-View Consistency in Generated Images." *arXiv 2025*. [arXiv:2501.06336](https://arxiv.org/abs/2501.06336)

---

*最后更新：2026-07-25 · 新增 60+ 篇 2025-2026 年最新论文 · 将持续更新*
