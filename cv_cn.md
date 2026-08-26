%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 中文求职简历
% Based on LaTeX resume template
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%----------------------------------------------------------------------------------------
%	PACKAGES AND OTHER DOCUMENT CONFIGURATIONS
%----------------------------------------------------------------------------------------

\documentclass[UTF8]{ctexart}
\usepackage[left=0.5in,top=0.6in,right=0.5in,bottom=0.6in]{geometry}
\usepackage{xcolor}
\usepackage{hyperref}

\newcommand{\LINK}[1]{\textcolor{blue}{#1}}

\name{蒋鸿达 / Hongda Jiang}

\begin{document}

\centerline{Email: \href{mailto:hongda.jiang@pku.edu.cn}{\LINK{hongda.jiang@pku.edu.cn}} \quad Phone: +86 18811319676 \quad Location: Beijing, China}

\smallskip

%----------------------------------------------------------------------------------------
%	个人简介
%----------------------------------------------------------------------------------------

\begin{rSection}{个人简介}
计算机科学博士，5年以上科研与工程经验，研究方向包括三维视觉、相机控制与深度学习。在 SIGGRAPH、SIGGRAPH Asia、Eurographics 等顶会发表多篇论文，并具备将研究成果落地为生产系统的能力。目前专注于视频生成与三维重建，致力于数字人及物体的高质量合成。求职方向：三维视觉、视频生成、角色动画相关的高级研究员/主任工程师岗位。
\end{rSection}

%----------------------------------------------------------------------------------------
%	教育背景
%----------------------------------------------------------------------------------------

\begin{rSection}{教育背景}

{\bf 计算机科学博士, \emph{北京大学}} \hfill {\em 2019.7-2024.7} 
\\ 导师：Prof. \href{https://baoquanchen.info/}{\LINK{Baoquan Chen}}

{\bf 计算机科学学士, \emph{北京大学}} \hfill {\em 2015.7-2019.7} 
\\ 导师：Prof. \href{https://baoquanchen.info/}{\LINK{Baoquan Chen}}, Prof. \href{https://scholar.google.com/citations?user=-OcSne0AAAAJ&hl=zh-CN}{\LINK{Jiaying Liu}}

\end{rSection}

%----------------------------------------------------------------------------------------
%	工作经历
%----------------------------------------------------------------------------------------

\begin{rSection}{工作经历}

{\bf 高级工程师, \emph{华为技术有限公司 北京}} \hfill {\em 2024.7-至今} 
\\ 方向：三维重建、视频生成、角色动画、相机控制
\\ 工作内容：
\begin{itemize}
\item 负责稀疏视角三维重建的深度学习算法研发，利用生成式视频模型从有限几何中合成密集观测，实现数字人与物体的高保真重建。
\item 研究基于视频模型与姿态引导的角色动画，集成可控相机运动以提升视频美学与电影效果，优化生产管线。
\item 推动生成式视频模型与传统动画及重建流程的融合，提升生产效率与质量。
\end{itemize}

\end{rSection}

%----------------------------------------------------------------------------------------
%	代表性论文
%----------------------------------------------------------------------------------------

\begin{rSection}{代表性论文}
\item \textbf{Hongda Jiang}, Marc Christie, Xi Wang, Libin Liu, Baoquan Chen. Cinematographic Camera Diffusion Model. \emph{Computer Graphics Forum (Proc. of the Eurographics)}, 2024. [\href{https://arxiv.org/abs/2402.16143}{\LINK{pdf}}]
\item \textbf{Hongda Jiang}, Marc Christie, Xi Wang, Libin Liu, Bin Wang, Baoquan Chen. Camera Keyframing with Style and Control. \emph{ACM Transactions on Graphics (Proc. of the SIGGRAPH Asia)}, 2021. [\href{https://dl.acm.org/doi/abs/10.1145/3478513.3480533}{\LINK{pdf}}][\href{https://www.youtube.com/watch?v=d_viqpC_a-Q}{\LINK{video}}]
\item \textbf{Hongda Jiang}, Bin Wang, Xi Wang, Marc Christie, Baoquan Chen. Example-driven virtual cinematography by learning camera behaviors. \emph{ACM Transactions on Graphics (Proc. of the SIGGRAPH)}, 2020. [\href{https://dl.acm.org/doi/abs/10.1145/3386569.3392427}{\LINK{pdf}}][\href{https://www.youtube.com/watch?v=xwHdChwNi8s}{\LINK{video}}]
\end{rSection}

%----------------------------------------------------------------------------------------
%	获奖情况
%----------------------------------------------------------------------------------------

\begin{rSection}{获奖情况}
北京大学第16届程序设计竞赛 第一名（2017）\\
北京大学第15届程序设计竞赛 二等奖（2016）\\
ACM CCPC 杭州站 银奖（2016）\\
NOI 全国青少年信息学奥林匹克竞赛 二等奖（2014）\\
CTSC 中国信息学 Olympiad 中国队选拔赛 金奖（2014）
\end{rSection}

\end{document}
