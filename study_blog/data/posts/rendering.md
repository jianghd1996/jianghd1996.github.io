---
title: 光影的魔法：渲染技术的千年演进
slug: rendering
date: '2026-07-27'
tags:
- 光栅化
- 光线追踪
- GPU 架构
- 神经渲染
- NeRF
- 3DGS
- 逆渲染
summary: 从洞穴壁画到 NeRF，从光栅化到 3D Gaussian Splatting——渲染技术如何让计算机"画"出真实感图像。涵盖光栅化与 GPU 的诞生、光线追踪与渲染方程、NeRF
  与神经渲染革命、3DGS 实时重建、逆渲染与可微渲染器、GPU 架构演进（RT Core / Tensor Core），结合 SIGGRAPH 经典论文与最新进展。
---

# 光影的魔法：渲染技术的千年演进

---

## 序章：光的故事

人类对"光影"的迷恋，可以追溯到洞穴壁画。原始人在岩壁上画下野牛，用简单的线条和阴影，试图捕捉"真实"。从那时起，一个问题始终困扰着人类：

> 如何在二维表面上，呈现三维世界的"真实感"？

文艺复兴时期，布鲁内莱斯基发明了**线性透视**——用数学方法在平面上表现深度。达芬奇用**明暗法**（chiaroscuro）让画面有了体积感。维米尔用**暗箱**（camera obscura）捕捉光影的微妙变化。

但真正的革命发生在 20 世纪——计算机的发明让人类可以用**数值方法**模拟光的传播。这就是**渲染（Rendering）**：从 3D 场景描述，生成 2D 图像的过程。

想象你是一个画家，面前有一张白纸。你的任务是画出一个"真实的苹果"。传统画家靠观察和经验；计算机靠物理方程和数值计算。渲染就是让计算机"画"出真实感图像的技术——它需要理解光的传播、材质的反射、相机的成像。

这个故事有四条线索：

- **图形学线索**：从光栅化到光线追踪，渲染算法的演进
- **硬件线索**：从 CPU 到 GPU，渲染硬件的革命
- **神经渲染线索**：从 NeRF 到 3DGS，深度学习的颠覆
- **逆渲染线索**：从图像反推场景，计算机视觉的逆袭

---

## 第一章：光栅化——实时的艺术

### 最古老的渲染算法

**光栅化（Rasterization）**是最古老的渲染算法之一。核心思想：

> 将 3D 三角形投影到 2D 屏幕，然后填充像素。

```
对于每个三角形：
  1. 顶点变换：世界坐标 → 相机坐标 → 屏幕坐标
  2. 光栅化：确定三角形覆盖哪些像素
  3. 着色：对每个像素计算颜色（光照、纹理）
```

光栅化的优势是**快**。每个三角形独立处理，可以高度并行。现代 GPU 每秒可以光栅化数十亿个三角形。

但光栅化的问题是**不真实**。它只处理"可见表面"，不处理全局光照（间接光、焦散、软阴影）。这就是为什么游戏画面看起来"假"——缺少真实世界的光影层次。

### GPU 的诞生：为光栅化而生

1999 年，NVIDIA 发布了 **GeForce 256**——第一块"GPU"（Graphics Processing Unit）。它的核心创新：**硬件变换与光照（T&L）**。

在此之前，3D 变换和光照由 CPU 完成，GPU 只负责光栅化。GeForce 256 将这些操作也搬到 GPU 上，大幅提升了性能。

**GPU 的演进**：

| 年代 | GPU | 核心创新 | 性能（GFLOPs） |
| --- | --- | --- | --- |
| 1999 | GeForce 256 | 硬件 T&L | 0.5 |
| 2001 | GeForce 3 | 可编程着色器 | 20 |
| 2006 | GeForce 8800 | CUDA（通用计算） | 500 |
| 2016 | GTX 1080 | Pascal 架构 | 9,000 |
| 2020 | RTX 3090 | RT Core（光追加速） | 36,000 |
| 2022 | RTX 4090 | Ada Lovelace | 83,000 |
| 2024 | RTX 5090 | Blackwell 架构 | 200,000+ |

GPU 的性能增长遵循**黄氏定律**（Huang's Law）：每两年性能翻倍。这比摩尔定律还快。

### 可编程着色器：GPU 的灵魂

2001 年，GeForce 3 引入了**可编程着色器**（Programmable Shader）。这是 GPU 历史上最重要的创新之一。

在此之前，光照模型是固定的（如 Phong、Blinn-Phong）。可编程着色器允许开发者用**程序**定义光照、材质、特效——GPU 变成了"像素级并行计算机"。

```
顶点着色器（Vertex Shader）：
  输入：顶点属性（位置、法线、纹理坐标）
  输出：变换后的顶点位置、插值属性

片元着色器（Fragment Shader）：
  输入：插值后的属性
  输出：像素颜色

// 简单的片元着色器示例
void main() {
    vec3 normal = normalize(v_normal);
    vec3 light_dir = normalize(light_pos - v_pos);
    float diffuse = max(dot(normal, light_dir), 0.0);
    frag_color = vec4(diffuse * albedo, 1.0);
}
```

可编程着色器让 GPU 不再只是"渲染加速器"，而是"通用并行处理器"。这直接催生了 GPGPU（General-Purpose GPU Computing）和深度学习革命。

想象一个工厂。固定功能 GPU 是"流水线"——只能生产一种产品。可编程 GPU 是"柔性制造"——可以生产任何产品，只要你告诉它怎么生产。可编程着色器就是"生产说明书"——它告诉 GPU 如何处理每个像素。

---

## 第二章：光线追踪——真实的代价

### 物理上正确的渲染

光栅化很快，但不真实。要渲染"照片级真实"的图像，需要模拟光的**物理传播**。这就是**光线追踪（Ray Tracing）**。

光线追踪的核心思想：

> 从相机发射光线，追踪它与场景的交互，计算最终颜色。

```
对于每个像素：
  1. 从相机发射一条光线（primary ray）
  2. 找到光线与场景的第一个交点
  3. 从交点发射多条次级光线（shadow ray, reflection ray, refraction ray）
  4. 递归追踪次级光线
  5. 累加所有光线的贡献，得到像素颜色
```

光线追踪的优势是**真实**——它可以自然处理阴影、反射、折射、焦散、全局光照。但问题是**慢**——每个像素需要追踪数百条光线，每条光线需要与场景求交。

### 渲染方程：光的数学

1986 年，James Kajiya 提出了**渲染方程**（Rendering Equation）——光的传播的完整数学描述：

```
L_o(x, ω_o) = L_e(x, ω_o) + ∫_Ω f_r(x, ω_i, ω_o) L_i(x, ω_i) (ω_i · n) dω_i

其中：
L_o = 出射辐射度（我们要求的）
L_e = 自发光
f_r = BRDF（双向反射分布函数）
L_i = 入射辐射度
ω_i, ω_o = 入射/出射方向
n = 表面法线
```

渲染方程是一个**积分方程**——它描述了光在场景中的完整传播。求解渲染方程是渲染的核心问题。

**求解方法**：

- **路径追踪（Path Tracing）**：用蒙特卡洛方法随机采样光路（Whitted, 1980; Kajiya, 1986）
- **光子映射（Photon Mapping）**：从光源发射光子，存储光子图（Jensen, 1996）
- **双向路径追踪（Bidirectional Path Tracing）**：同时从相机和光源追踪（Veach & Guibas, 1997）
- **梅特罗波利斯光传输（MLT）**：用马尔可夫链采样重要光路（Pauly et al., 2000）

### 实时光线追踪：梦想成真

光线追踪很慢——传统上每帧需要数小时。但 2018 年，NVIDIA 发布了 **RTX** 系列 GPU，内置**RT Core**——专用的光线追踪加速单元。

RT Core 的核心功能：**加速光线与三角形的求交测试**。它用 **Bound Volume Hierarchy (BVH)** 的硬件遍历，将求交速度提升了 10-100 倍。

```
传统光追：CPU 遍历 BVH → 100M rays/s
RT Core：硬件遍历 BVH → 10G rays/s（100× 加速）
```

RTX 让**实时光线追踪**成为可能。游戏《赛博朋克 2077》《控制》《使命召唤》都支持 RTX 光追，实现了真实的反射、阴影、全局光照。

在《赛博朋克 2077》中，夜之城的霓虹灯在湿漉漉的地面上反射，雨水在车窗上形成水珠，光线在玻璃幕墙间多次弹射——这些都是实时光线追踪的效果。在 RTX 之前，这些效果需要离线渲染数小时；现在，它们可以在 60fps 下实时呈现。

### SIGGRAPH 的贡献

SIGGRAPH 社区在渲染算法方面做出了巨大贡献：

- **Christensen (2016)**：Production Rendering 的综述，总结了电影工业的渲染管线
- **Pharr, Jakob, Humphreys (2023)**：*Physically Based Rendering* 第四版，渲染领域的"圣经"
- **Bitterli et al. (2016)**：渲染算法的基准测试框架
- **Nimier-David et al. (2019)**：Mitsuba 2——可微渲染器

---

## 第三章：神经渲染——深度学习的颠覆

### NeRF：一个意外的革命

2020 年，Ben Mildenhall 等人发表了 **NeRF**（Neural Radiance Fields）。这篇论文只有 8 页，但引发了渲染领域的革命。

NeRF 的核心思想：

> 用神经网络表示 3D 场景——输入 3D 坐标和视角方向，输出颜色和密度。

```
NeRF 网络：
  输入：(x, y, z, θ, φ)  // 3D 坐标 + 视角方向
  输出：(r, g, b, σ)      // 颜色 + 密度

训练：从多张 2D 图像学习
推理：用体渲染（volume rendering）生成新视角
  C(ray) = ∫ T(t) σ(t) c(t) dt
  T(t) = exp(-∫_0^t σ(s) ds)  // 透射率
```

NeRF 的突破在于：**从少量照片重建照片级真实的 3D 场景。**不需要激光扫描仪，不需要深度相机，只需要几张照片。

想象你拍了一个雕像的 50 张照片，从不同角度。NeRF 可以从这 50 张照片"学会"整个 3D 场景，然后生成任意角度的新照片——效果逼真到难以分辨真假。这就是 NeRF 的魔力。

### NeRF 的局限与改进

NeRF 虽然惊艳，但有几个致命问题：

- **训练慢**：需要数小时到数天
- **渲染慢**：每条光线需要数百次网络查询
- **静态场景**：不能处理动态物体
- **难以编辑**：隐式表示难以修改

**改进方向**：

| 方法 | 核心创新 | 速度提升 | 代表工作 |
| --- | --- | --- | --- |
| Instant NGP | 多分辨率哈希编码 | 1000× | Müller et al. 2022 |
| Plenoxels | 无网络，直接用稀疏体素 | 100× | Fridovich-Keil et al. 2022 |
| 3DGS | 3D 高斯溅射 | 10000× | Kerbl et al. 2023 |
| Mip-NeRF 360 | 抗锯齿 + 室外场景 | 2× | Barron et al. 2022 |
| Nerfacto | 工程优化集大成 | 10× | nerfstudio 2023 |

### 3D Gaussian Splatting：实时神经渲染

2023 年，Kerbl 等人提出了 **3D Gaussian Splatting (3DGS)**。这是神经渲染的又一个里程碑。

3DGS 的核心思想：

> 用数百万个 3D 高斯椭球表示场景，用光栅化（而非光线追踪）渲染。

```
场景表示：
  {G_i} = {(μ_i, Σ_i, c_i, α_i)}  // 位置、协方差、颜色、不透明度
  每个高斯是一个 3D 椭球

渲染：
  1. 将 3D 高斯投影到 2D（得到 2D 高斯）
  2. 按深度排序
  3. 用 alpha blending 合成颜色
  // 这个过程可以用 GPU 光栅化管线加速
```

3DGS 的突破：**实时渲染**。它用 GPU 的光栅化管线渲染高斯，速度达到 30-300 fps——比 NeRF 快 10000 倍。

| 方法 | 表示 | 训练时间 | 渲染速度 | 质量 |
| --- | --- | --- | --- | --- |
| NeRF | MLP | 数小时 | ~1 fps | 高 |
| Instant NGP | 哈希编码 + MLP | 数分钟 | ~10 fps | 高 |
| 3DGS | 3D 高斯 | 数十分钟 | 30-300 fps | 极高 |
| Mip-NeRF 360 | MLP + 抗锯齿 | 数小时 | ~2 fps | 极高（室外） |

3DGS 的渲染速度快到什么程度？你可以在手机上实时浏览一个城市的 3D 重建——拖动视角，画面流畅更新，没有延迟。这在 NeRF 时代是不可想象的。

### 动态场景与可编辑表示

2024-2025 年，神经渲染向**动态场景**和**可编辑表示**发展：

- **4D Gaussian Splatting**：用 4D 高斯表示动态场景
- **Neural Fields + Physics**：将物理仿真集成到神经场中
- **Gaussian Editing**：直接编辑 3D 高斯（移动、删除、变形）
- **Language-guided 3D**：用自然语言编辑 3D 场景

---

## 第四章：逆渲染——从图像到场景

### 渲染的反问题

**渲染**是"正向"问题：从 3D 场景 → 2D 图像。

**逆渲染**（Inverse Rendering）是"反向"问题：从 2D 图像 → 3D 场景（包括几何、材质、光照）。

> 给定一张或多张照片，反推场景的 3D 形状、材质属性、光照条件。

逆渲染的应用：

- **3D 重建**：从照片重建 3D 模型
- **材质估计**：从图像反推 BRDF 参数
- **光照估计**：从图像反推环境光照
- **虚拟现实**：将真实物体"放入"虚拟场景
- **自动驾驶**：从相机图像理解场景几何

### 可微渲染：逆渲染的关键

逆渲染需要**梯度**——图像对场景参数的导数。但传统渲染器是"黑盒"——不可微。

**可微渲染器**（Differentiable Renderer）让渲染过程可微——可以对场景参数求梯度，从而用梯度下降优化。

**代表工作**：

- **Kato et al. (2018)**：Neural 3D Mesh Renderer——第一个可微光栅化器
- **Loper & Black (2014)**：OpenDR——可微渲染框架
- **Li et al. (2018)**：Mitsuba 的前身，可微路径追踪
- **Nimier-David et al. (2019)**：Mitsuba 2——高性能可微渲染器
- **Jakob et al. (2022)**：Dr.Jit——可微渲染的 JIT 编译器

```
可微渲染的基本流程：
  1. 初始化场景参数 θ（几何、材质、光照）
  2. 渲染图像 I_render = Render(θ)
  3. 计算损失 L = ||I_render - I_target||²
  4. 反向传播：dL/dθ = dL/dI_render · dI_render/dθ
  5. 梯度下降：θ ← θ - α · dL/dθ
  6. 重复 2-5，直到收敛
```

### 从逆渲染到神经重建

2023-2025 年，逆渲染与神经渲染融合，催生了**神经重建**（Neural Reconstruction）：

- **Neuralangelo (Li et al., 2023)**：用 Instant NGP + 可微渲染重建高保真 3D 表面
- **VGGSfM (Wang et al., 2024)**：用视觉基础模型做 Structure from Motion
- **DUSt3R (Wang et al., 2024)**：前馈式 3D 重建，无需逐场景优化
- **MASt3R (Leroy et al., 2024)**：DUSt3R 的改进，加入局部特征

想象你有一张老照片，照片里有你的祖父母。逆渲染可以从这张照片反推出：祖父母的面部 3D 形状、衣服的材质、房间的光照。然后你可以"走进"这个 3D 场景，从不同角度观看——就像时间旅行。

### 逆渲染的挑战

逆渲染是一个**病态问题**（ill-posed problem）——一张 2D 图像对应无数个 3D 场景。需要额外约束：

- **多视角**：从多个角度拍摄，增加约束
- **先验知识**：用神经网络学习"什么是合理的场景"
- **物理约束**：材质必须满足能量守恒、互易性等
- **正则化**：鼓励平滑、简单的解

---

## 第五章：GPU 架构——渲染的引擎

### 从固定管线到通用计算

GPU 的架构演进可以分为三个阶段：

**第一阶段（1999-2006）：固定功能管线。**GPU 只能做光栅化，光照模型固定。代表：GeForce 256、Radeon 7500。

**第二阶段（2006-2018）：可编程着色器。**GPU 可以执行任意程序，催生了 GPGPU。代表：GeForce 8800（CUDA）、Tesla（计算卡）。

**第三阶段（2018-）：专用硬件加速。**GPU 加入专用单元：RT Core（光追）、Tensor Core（AI）、DX Core（DirectX 优化）。代表：RTX 系列、A100/H100。

### 现代 GPU 架构

以 NVIDIA Ada Lovelace（RTX 40 系列）为例：

```
GPU 架构：
  Streaming Multiprocessor (SM) × 128
    ↓
  每个 SM 包含：
    - CUDA Core × 128（通用计算）
    - RT Core × 1（光追加速）
    - Tensor Core × 4（AI 加速）
    - 寄存器文件、L1 Cache、共享内存
```

**关键指标**：

| 指标 | RTX 4090 | RTX 5090 | A100 | H100 |
| --- | --- | --- | --- | --- |
| CUDA Cores | 16,384 | 24,576 | 6,912 | 16,896 |
| RT Cores | 128 | 192 | 0 | 0 |
| Tensor Cores | 512 | 768 | 432 | 528 |
| 显存 | 24 GB GDDR6X | 32 GB GDDR7 | 80 GB HBM2e | 80 GB HBM3 |
| FP32 算力 | 83 TFLOPs | 200+ TFLOPs | 20 TFLOPs | 60 TFLOPs |
| 目标场景 | 游戏/创作 | 游戏/创作 | AI 训练 | AI 训练 |

### RT Core：光追的心脏

RT Core 的核心功能：**加速 BVH 遍历和光线-三角形求交**。

```
传统光追（CPU/GPU 通用计算）：
  遍历 BVH：O(log N) 次内存访问
  求交测试：O(1) 次计算
  总时间：~100 ns / ray

RT Core：
  硬件遍历 BVH：并行处理
  硬件求交测试：专用电路
  总时间：~1 ns / ray（100× 加速）
```

RT Core 让实时光追成为可能，但也引发了一个问题：**为什么不用更多 RT Core？**

答案是**面积**。RT Core 占用大量芯片面积，但只在光追时有用。对于 AI 训练、科学计算等场景，RT Core 是浪费。所以计算卡（A100/H100）没有 RT Core。

### Tensor Core：AI 的引擎

Tensor Core 的核心功能：**加速矩阵乘法**。

```
Tensor Core 操作：
  D = A × B + C
  其中 A, B, C, D 是小矩阵（如 4×4）
  
  支持精度：FP64, FP32, TF32, FP16, BF16, INT8, INT4, FP8

  H100 Tensor Core：
  FP8: 3,958 TFLOPs（稀疏）
  FP16: 1,979 TFLOPs（稀疏）
  FP64: 67 TFLOPs
```

Tensor Core 是 AI 训练的核心。H100 的 FP8 算力是 A100 的 3 倍，这直接推动了大模型训练。

---

## 第六章：渲染的未来

### 趋势一：神经渲染与传统渲染的融合

3DGS 证明了神经渲染可以实时，但缺乏物理正确性。未来方向：**物理约束的神经渲染**——既有神经渲染的速度，又有传统渲染的真实性。

### 趋势二：可微渲染的普及

可微渲染让"从图像反推场景"成为可能。随着 Dr.Jit、Mitsuba 3 等工具的成熟，可微渲染将成为计算机视觉的标配。

### 趋势三：实时全局光照

RTX 已经实现了实时光追，但全局光照仍然昂贵。未来方向：**AI 加速的全局光照**——用神经网络预测间接光照。

### 趋势四：3D 基础模型

DUSt3R、VGGSfM 等工作表明，**前馈式 3D 重建**正在取代逐场景优化。未来可能出现"3D 的 GPT"——一个模型重建所有场景。

也许有一天，你只需要用手机拍几张照片，AI 就能重建出照片级真实的 3D 场景——包括几何、材质、光照。你可以"走进"这个场景，从任意角度观看，甚至修改它。这就是渲染技术的终极目标——让虚拟和现实无法区分。

---

## 参考文献

1. Kajiya, J. T. (1986). *The Rendering Equation*. SIGGRAPH.
2. Whitted, T. (1980). *An Improved Illumination Model for Shaded Display*. Communications of the ACM.
3. Jensen, H. W. (1996). *Global Illumination Using Photon Maps*. Eurographics.
4. Pharr, M., Jakob, W., & Humphreys, G. (2023). *Physically Based Rendering: From Theory to Implementation* (4th ed.). MIT Press.
5. Mildenhall, B., et al. (2020). *NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis*. ECCV.
6. Müller, T., et al. (2022). *Instant Neural Graphics Primitives with a Multiresolution Hash Encoding*. SIGGRAPH.
7. Kerbl, B., et al. (2023). *3D Gaussian Splatting for Real-Time Radiance Field Rendering*. SIGGRAPH.
8. Barron, J. T., et al. (2022). *Mip-NeRF 360: Unbounded Anti-Aliased Neural Radiance Fields*. CVPR.
9. Kato, H., et al. (2018). *Neural 3D Mesh Renderer*. CVPR.
10. Nimier-David, M., et al. (2019). *Mitsuba 2: A Retargetable Forward and Inverse Renderer*. SIGGRAPH Asia.
11. Jakob, W., et al. (2022). *Dr. JIT: A Just-In-Time Compiler for Differentiable Rendering*. SIGGRAPH.
12. Li, Z., et al. (2023). *Neuralangelo: High-Fidelity Neural Surface Reconstruction*. CVPR.
13. Wang, J., et al. (2024). *DUSt3R: Geometric 3D Vision Made Easy*. CVPR.
14. Leroy, V., et al. (2024). *MASt3R: Geometry-Aware Visual Correspondences*. ECCV.
15. NVIDIA. (2024). *Ada Lovelace Architecture Whitepaper*.
16. NVIDIA. (2024). *Blackwell Architecture Whitepaper*.

本文撰写于 2026 年 7 月，反映截至当时的技术状态。  
渲染技术领域进展迅速，建议结合最新 SIGGRAPH / CVPR / ECCV 论文持续跟踪。
