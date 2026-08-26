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

%----------------------------------------------------------------------------------------
%	CONTACT & SUMMARY
%----------------------------------------------------------------------------------------

\begin{rSection}{Contact Information}
Email: \href{mailto:hongda.jiang@pku.edu.cn}{\LINK{hongda.jiang@pku.edu.cn}} \hfill \href{https://jianghd1996.github.io/}{\LINK{Bio Page}} \\
Phone: +86 18811319676 \\
Location: Hangzhou, China
\end{rSection}

\begin{rSection}{Professional Summary}
PhD in Computer Science with 5+ years of research and engineering experience in 3D vision, camera control, and deep learning. Proven track record of publishing at top-tier venues (SIGGRAPH, SIGGRAPH Asia, Eurographics) and translating research into production-ready systems. Currently focused on video generation and 3D reconstruction for digital human and object synthesis at Huawei. Seeking senior researcher / staff engineer roles in 3D vision, video generation, or character animation.
\end{rSection}

%----------------------------------------------------------------------------------------
%	EDUCATION SECTION
%----------------------------------------------------------------------------------------

\begin{rSection}{Education}

{\bf PhD in Computer Science, \emph{Peking University}} \hfill {\em 2019.7-2024.7} 
\\ Supervisor: Prof. \href{https://baoquanchen.info/}{\LINK{Baoquan Chen}}
\\ Major: Computer Application Technology
\\ Thesis: \textit{Research on Intelligent Camera Movement Based on Multimodal Control}

{\bf BS in Computer Science, \emph{Peking University}} \hfill {\em 2015.7-2019.7} 
\\ Supervisor: Prof. \href{https://baoquanchen.info/}{\LINK{Baoquan Chen}}, Prof. \href{https://scholar.google.com/citations?user=-OcSne0AAAAJ&hl=zh-CN}{\LINK{Jiaying Liu}}
\\ Major: Computer Science
\\ Thesis: \textit{Research on Camera Trajectory Planning Based on Toric Space}

\end{rSection}

%----------------------------------------------------------------------------------------
%	TECHNICAL SKILLS
%----------------------------------------------------------------------------------------

\begin{rSection}{Technical Skills}
\begin{itemize}
\item \textbf{Programming:} Python, C++, CUDA, MATLAB, LaTeX
\item \textbf{Frameworks \& Libraries:} PyTorch, TensorFlow, OpenCV, OpenGL, Blender, Unity
\item \textbf{Research Areas:} 3D Vision, Neural Rendering, Camera Control, Computational Cinematography, Character Animation, Generative Video Models, Diffusion Models, Multi-modal Learning
\item \textbf{Tools \& Platforms:} Git, Docker, Linux, AWS, CI/CD, HPC clusters
\end{itemize}
\end{rSection}

%----------------------------------------------------------------------------------------
%	WORK EXPERIENCE SECTION
%----------------------------------------------------------------------------------------

\begin{rSection}{Professional Experience}

{\bf Senior Engineer, \emph{Huawei Technologies Co., Ltd. Hangzhou, China}} \hfill {\em 2025.8-present} 
\\ Topics: Sparse-view 3D Reconstruction, Generative Video Models
\\ Content: 
\begin{itemize}
\item Developed deep learning algorithms for 3D reconstruction from sparse-view inputs, improving reconstruction fidelity by leveraging generative video models to synthesize dense observations from limited geometry.
\item Adapted diffusion-based video generation frameworks to produce temporally consistent dense views, enabling high-fidelity reconstruction of objects and digital humans in production pipelines.
\end{itemize}

{\bf Senior Engineer, \emph{Huawei Technologies Co., Ltd. Beijing, China}} \hfill {\em 2024.7-2025.8}
\\ Topics: Character Animation, Camera Control, Video Models
\\ Content:
\begin{itemize}
\item Researched character animation driven by video models and pose guidance, integrating controllable camera motion to enhance video aesthetics and cinematic effects.
\item Streamlined production pipelines for high-quality character assets by bridging generative video models with traditional animation workflows.
\end{itemize}

{\bf Research Internship, \emph{Beijing Film Academy}}, \emph{\href{https://fve.bfa.edu.cn/}{AICFVE}} Lab \hfill {\em 2019-2021} 
\\ Topics: Learning-based virtual camera control
\\ Content: Developed machine learning approaches for automatic virtual camera motion generation in 3D animation, collaborating with researchers from Peking University, IRISA, and Peking University.

{\bf Teaching Assistant, \emph{Peking University}}  \hfill {\em 2019-2020} 
\\ Course: Frontier Computing Practices (Fall 2019, Spring 2020)

{\bf Teaching Assistant, \emph{Peking University}}  \hfill {\em 2018-2019} 
\\ Course: \href{https://computergive.github.io/2018-fall/index.html}{\LINK{Computer Generated Imagery and Visual Effects}} (Fall 2018)

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
{\bf Research} \\
Award for Contribution in Student Organizations, Peking University (Ubiquant Scholarship) 2023 \\
Award for Scientific Research, Peking University (Schlumberger Limited Scholarship) 2022 \\
Award for Scientific Research, Peking University (Third Class Scholarship) 2020 \\
Computing Star of EECS, Peking University 2020 \\
Excellent Project Award, Peking University Undergraduate President Fund 2018

{\bf Programming} \\
First Place, 16th Computer Programming Contest of Peking University 2017 \\
Second Prize, 15th Computer Programming Contest of Peking University 2016 \\
Silver Award, ACM CCPC Hangzhou 2016 \\
Second Prize, CCF National Olympiad in Informatics (NOI), China 2014 \\
Gold Award, CCF China Team Selection Competition (CTSC), China 2014
\end{rSection}

\end{document}
