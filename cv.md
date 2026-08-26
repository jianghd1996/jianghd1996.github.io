%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Professional CV for Job Application
% LaTeX Template
% Version 2.0 (8/5/13)
%
% This template has been downloaded from:
% http://www.LaTeXTemplates.com
%
% Original author:
% Trey Hunner (http://www.treyhunner.com/)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%----------------------------------------------------------------------------------------
%	PACKAGES AND OTHER DOCUMENT CONFIGURATIONS
%----------------------------------------------------------------------------------------

\newcommand{\LINK}[1]{\textcolor{blue}{#1}}

\documentclass{resume} % Use the custom resume.cls style

\usepackage[left=0.5in,top=0.6in,right=0.5in,bottom=0.6in]{geometry} % Document margins
\usepackage{xcolor}
\usepackage{hyperref}

\newcommand{\tab}[1]{\hspace{.2667\textwidth}\rlap{#1}}
\newcommand{\itab}[1]{\hspace{0em}\rlap{#1}}

\name{Hongda Jiang} % Your name


\begin{document}

\centerline{Email: \href{mailto:hongda.jiang@pku.edu.cn}{\LINK{hongda.jiang@pku.edu.cn}} \quad Phone: +86 18811319676 \quad Location: Beijing, China}

\smallskip

%----------------------------------------------------------------------------------------
%	CONTACT & SUMMARY
%----------------------------------------------------------------------------------------

\begin{rSection}{Professional Summary}
PhD in Computer Science with 5+ years of research and engineering experience in 3D vision, camera control, and deep learning. Proven track record of publishing at top-tier venues (SIGGRAPH, SIGGRAPH Asia, Eurographics) and translating research into production-ready systems. Award-winning programmer with top placements in national/international informatics competitions. Currently focused on video generation and 3D reconstruction for digital human and object synthesis at Huawei. Seeking senior researcher / staff engineer roles in 3D vision, video generation, or character animation.
\end{rSection}

%----------------------------------------------------------------------------------------
%	EDUCATION SECTION
%----------------------------------------------------------------------------------------

\begin{rSection}{Education}

{\bf PhD in Computer Science, \emph{Peking University}} \hfill {\em 2019.7-2024.7} 
\\ Supervisor: Prof. \href{https://baoquanchen.info/}{\LINK{Baoquan Chen}}

{\bf BS in Computer Science, \emph{Peking University}} \hfill {\em 2015.7-2019.7} 
\\ Supervisor: Prof. \href{https://baoquanchen.info/}{\LINK{Baoquan Chen}}, Prof. \href{https://scholar.google.com/citations?user=-OcSne0AAAAJ&hl=zh-CN}{\LINK{Jiaying Liu}}

\end{rSection}

%----------------------------------------------------------------------------------------
%	WORK EXPERIENCE SECTION
%----------------------------------------------------------------------------------------

\begin{rSection}{Professional Experience}

{\bf Senior Engineer, \emph{Huawei Technologies Co., Ltd. Beijing, China}} \hfill {\em 2024.7-present} 
\\ Topics: 3D Reconstruction, Video Generation, Character Animation, Camera Control
\\ Content: 
\begin{itemize}
\item Developed deep learning algorithms for sparse-view 3D reconstruction, leveraging generative video models to synthesize dense observations from limited geometry for high-fidelity digital human and object reconstruction.
\item Researched character animation driven by video models and pose guidance, integrating controllable camera motion to enhance video aesthetics and cinematic effects in production pipelines.
\item Streamlined production workflows by bridging generative video models with traditional animation and reconstruction pipelines.
\end{itemize}

\end{rSection}

%----------------------------------------------------------------------------------------
%	RESEARCH & PROJECTS
%----------------------------------------------------------------------------------------

\begin{rSection}{Selected Publications}
\item \textbf{Hongda Jiang}, Marc Christie, Xi Wang, Libin Liu, Baoquan Chen. Cinematographic Camera Diffusion Model. \emph{Computer Graphics Forum (Proc. of the Eurographics)}, 2024. [\href{https://arxiv.org/abs/2402.16143}{\LINK{pdf}}]
\item \textbf{Hongda Jiang}, Marc Christie, Xi Wang, Libin Liu, Bin Wang, Baoquan Chen. Camera Keyframing with Style and Control. \emph{ACM Transactions on Graphics (Proc. of the SIGGRAPH Asia)}, 2021. [\href{https://dl.acm.org/doi/abs/10.1145/3478513.3480533}{\LINK{pdf}}][\href{https://www.youtube.com/watch?v=d_viqpC_a-Q}{\LINK{video}}]
\item \textbf{Hongda Jiang}, Bin Wang, Xi Wang, Marc Christie, Baoquan Chen. Example-driven virtual cinematography by learning camera behaviors. \emph{ACM Transactions on Graphics (Proc. of the SIGGRAPH)}, 2020. [\href{https://dl.acm.org/doi/abs/10.1145/3386569.3392427}{\LINK{pdf}}][\href{https://www.youtube.com/watch?v=xwHdChwNi8s}{\LINK{video}}]
\end{rSection}

%----------------------------------------------------------------------------------------
%	AWARDS & HONORS
%----------------------------------------------------------------------------------------

\begin{rSection}{Awards \& Honors}
First Place, 16th Computer Programming Contest of Peking University 2017 \\
Second Prize, 15th Computer Programming Contest of Peking University 2016 \\
Silver Award, ACM CCPC Hangzhou 2016 \\
Second Prize, CCF National Olympiad in Informatics (NOI), China 2014 \\
Gold Award, CCF China Team Selection Competition (CTSC), China 2014
\end{rSection}

\end{document}
