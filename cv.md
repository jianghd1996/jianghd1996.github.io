%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Medium Length Professional CV
% LaTeX Template
% Version 2.0 (8/5/13)
%
% This template has been downloaded from:
% http://www.LaTeXTemplates.com
%
% Original author:
% Trey Hunner (http://www.treyhunner.com/)
%
% Important note:
% This template requires the resume.cls file to be in the same directory as the
% .tex file. The resume.cls file provides the resume style used for structuring the
% document.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%----------------------------------------------------------------------------------------
%	PACKAGES AND OTHER DOCUMENT CONFIGURATIONS
%----------------------------------------------------------------------------------------

\newcommand{\LINK}[1]{\textcolor{blue}{#1}}

\documentclass{resume} % Use the custom resume.cls style

\usepackage[left=0.5in,top=0.6in,right=0.5in,bottom=0.6in]{geometry} % Document margins

\newcommand{\tab}[1]{\hspace{.2667\textwidth}\rlap{#1}}
\newcommand{\itab}[1]{\hspace{0em}\rlap{#1}}

\name{Hongda Jiang} % Your name


\begin{document}

%----------------------------------------------------------------------------------------
%	EDUCATION SECTION
%----------------------------------------------------------------------------------------

\begin{rSection}{Contact Information}
Email: \href{mailto:hongda.jiang@pku.edu.cn}{\LINK{hongda.jiang@pku.edu.cn}} \hfill \href{https://jianghd1996.github.io/}{\LINK{Bio Page}} \\
Phone: +86 18811319676 \\
Address: Building Z8, No. 410 Jianghong Road, Binjiang District, Hangzhou City, China 310052.

\end{rSection}

\begin{rSection}{Education}

{\bf PhD in Computer Science, \emph{Peking University}} \hfill {\em 2019.7-2024.7} 
\\ Supervisor: Prof. \href{https://baoquanchen.info/}{\LINK{Baoquan Chen}}
\\ Collaborators: Prof. \href{https://people.irisa.fr/Marc.Christie/}{\LINK{Marc Christie}}, Prof. \href{http://libliu.info/}{\LINK{Libin Liu}}, Dr. \href{https://binwangbfa.github.io/}{\LINK{Bin Wang}}, Dr. \href{https://triocrossing.github.io/}{\LINK{Xi Wang}}
\\ Major: Computer Application Technology
\\ Thesis: \textit{Research on Intelligent Camera Movement Based on Multimodal Control}


{\bf BS in Computer Science, \emph{Peking University}} \hfill {\em 2015.7-2019.7} 
\\ Supervisor: Prof. \href{https://baoquanchen.info/}{\LINK{Baoquan Chen}}, Prof. \href{https://scholar.google.com/citations?user=-OcSne0AAAAJ&hl=zh-CN}{\LINK{Jiaying Liu}}
\\ Major: Computer Science
\\ Thesis: \textit{Research on Camera Trajectory Planning Based on Toric Space}

% \\
% \\ {\bf Senior High School, \emph{Changjun High School}} \hfill {\em 2012-2015}

\end{rSection}
%----------------------------------------------------------------------------------------
%	TECHNICAL STRENGTHS SECTION
%----------------------------------------------------------------------------------------



\begin{rSection}{Working and Professional Experience}

{\bf Senior Engineer,  \emph{Huawei Technologies Co., Ltd. Hangzhou, China}} \hfill {\em 2025.8-present} 
\\ Address: Building Z8, No. 410 Jianghong Road, Binjiang District, Hangzhou City, China.
\\ Topics: Sparse-view 3D Reconstruction via Deep Learning
\\ Content: Developed deep learning algorithms for 3D reconstruction from sparse-view inputs. Adapted generative video models to synthesize dense observations from limited geometry, enabling high-fidelity reconstruction of objects and digital humans.

{\bf Senior Engineer,  \emph{Huawei Technologies Co., Ltd. Beijing, China}} \hfill {\em 2024.7-2025.8}
\\ Address: Building Q20, Zhongguancun Environmental Protection Technology Demonstration Park, No. 156 Beiqing Road, Haidian District Beijing, China
\\ Topics: Character Animation, Camera Control
\\ Content: Researched character animation driven by video models and pose guidance. Integrated controllable camera motion to enhance video aesthetics and cinematic effects, streamlining the production pipeline for high-quality character assets.

{\bf Research Internship, \emph{Beijing Film Academy}}, \emph{\href{https://fve.bfa.edu.cn/}{AICFVE}} Lab \hfill {\em 2019-2021} 
\\ Topics: Learning based virtual camera control
\\ Collaborators: Prof. \href{https://baoquanchen.info/}{\LINK{Baoquan Chen}},  Prof. \href{https://people.irisa.fr/Marc.Christie/}{\LINK{Marc Christie}}, Prof. \href{http://libliu.info/}{\LINK{Libin Liu}}, Dr. \href{https://binwangbfa.github.io/}{\LINK{Bin Wang}}, Dr. \href{https://binwangbfa.github.io/}{\LINK{Xi Wang}}

{\bf Teaching Assistant, \emph{Peking University}}  \hfill {\em 2019-2020} 
\\ Course: Frontier computing practices (fall 2019, spring 2020)

{\bf Teaching Assistant, \emph{Peking University}}  \hfill {\em 2018-2019} 
\\ Course: \href{https://computergive.github.io/2018-fall/index.html}{\LINK{Computer Generated Imagery and Visual Effects}} (fall 2018)

{\bf Research Internship, \emph{Peking University}}, \emph{Wangxuan Institute of Computer Technology}  \hfill {\em 2017-2018} 
\\ Topics: Human action recognition, Multimodal fusion
\\ Supervised by: Prof. \href{https://scholar.google.com/citations?user=-OcSne0AAAAJ&hl=zh-CN}{\LINK{Jiaying Liu}}

\end{rSection}



%----------------------------------------------------------------------------------------
%	WORK EXPERIENCE SECTION
%----------------------------------------------------------------------------------------



% \begin{rSection}{Project}

% \begin{rSubsection}{Virtual Cinematography and Camera Control}{}{CFCS, Peking University}{Sept, 2019-Present}
% Designing a camera motion controller that can move a virtual camera automatically with the contents of a 3D animation, in a cinematographic and principled way, is a complex and challenging task. To solve this problem, I have done three projects with my collaborators:
% \item We first learn an \textbf{example-driven camera controller} that can extract camera behaviors from an example film clip and re-apply the extracted behaviors to a 3D animation, through learning from a collection of camera motions.
% \item We then propose a novel technique that enables 3D artists to synthesize camera motions in virtual environments following a \textbf{camera style}, while enforcing \textbf{user-designed camera keyframes} as constraints along the sequence.
% \item We further develop a \textbf{text and keyframe guided} diffusion model to generate camera motions through cinematographic properties and keyframe constraints.
% \end{rSubsection}

% \begin{rSubsection}{Data Visualization Analysis and Simulation Prediction for COVID-19}{}{CFCS, Peking University}{Jan, 2020-Mar, 2020}
% The COVID-19 (formerly, 2019-nCoV) epidemic raises a global health emergency and China takes the most hit since the outbreak of the virus. In this study, we collect and visualize publicly available data, and show patterns and characteristics of the epidemic development; we then employ a mathematical model of disease transmission dynamics to evaluate the effectiveness of some epidemic control measures, and more importantly, to offer a few tips on preventive measures.
% \end{rSubsection}

% \begin{rSubsection}{Give Henan A Hand}{}{CFCS, Peking University} {July, 2021-Aug, 2021}

% In July 2021, there was a sudden rainstorm in Henan, resulting in serious disaster. A large number of affected people published rescue information online. At the same time, forces from all over the country arrived in the disaster area to carry out rescue. Based on the rescue information on the network and the rescue documents maintained by various voluntary organizations, the project collects, updates and displays the rescue information on the map in real time, so that the rescue team can better help the rescue people and support disaster relief.
% \end{rSubsection}

% \end{rSection}


%	EXAMPLE SECTION
%----------------------------------------------------------------------------------------

% \begin{rSection}{Academic Achievements} \itemsep -2pt
% \item 1. Selected as {\bf DAAD-WISE Fellow} for carrying summer internship in {\bf Germany, 2019}
% \item 2. Selected as {\bf MITACS Globalink Fellow} to carry out summer internship at {\bf Calgary University, Canada, 2019}
% \item 3. Selected at {\bf SPARK Summer Internship Programme, 2018} to carry out summer internship at {\bf IIT Roorkee} 
% \item 4. Secured {\bf top 2 percent} position in {\bf JEE MAIN,2016} among 2 lakh candidates.
% \item 5. Secured 14th rank in state conducted by WBCHSE, 2016.
% \item 6. Secured 11th rank in state conducted by WBBSE, 2014.
% \end{rSection}

%----------------------------------------------------------------------------------------
\begin{rSection}{Publications}
\item \textbf{Hongda Jiang}, Marc Christie, Xi Wang, Libin Liu, Baoquan Chen. Cinematographic Camera Diffusion Model. \emph{Computer Graphics Forum (Proc. of the Eurographics)}, 2024. [\href{https://arxiv.org/abs/2402.16143}{\LINK{pdf}}]
\item \textbf{Hongda Jiang}, Marc Christie, Xi Wang, Libin Liu, Bin Wang, Baoquan Chen. Camera Keyframing with Style and Control. \emph{ACM Transactions on Graphics (Proc. of the SIGGRAPH Asia)}, 2021. [\href{https://dl.acm.org/doi/abs/10.1145/3478513.3480533}{\LINK{pdf}}][\href{https://www.youtube.com/watch?v=d_viqpC_a-Q}{\LINK{video}}]
\item \textbf{Hongda Jiang}, Bin Wang, Xi Wang, Marc Christie, Baoquan Chen. Example-driven virtual cinematography by learning camera behaviors. \emph{ACM Transactions on Graphics (Proc. of the SIGGRAPH)}, 2020. [\href{https://dl.acm.org/doi/abs/10.1145/3386569.3392427}{\LINK{pdf}}][\href{https://www.youtube.com/watch?v=xwHdChwNi8s}{\LINK{video}}]
\item Baoquan Chen, Mingyi Shi, Xingyu Ni, Liangwang Ruan, \textbf{Hongda Jiang}, Heyuan Yao, Mengdi Wang, Zhenhua Song, Qiang Zhou, Tong Ge. Data Visualization Analysis and Simulation Prediction for COVID-19. ArXiv preprint 2019. [\href{https://arxiv.org/abs/2002.07096}{\LINK{pdf}}]
\item \textbf{Hongda Jiang}, Yanghao Li, Sijie Song, and Jiaying Liu, Rethinking Fusion Baselines for Multi-modal Human Action Recognition. Pacific Rim Conference on Multimedia, 2018. [\href{https://link.springer.com/chapter/10.1007/978-3-030-00764-5_17}{\LINK{pdf}}]
\end{rSection}

\begin{rSection}{Research Interests}
3D Vision, Camera Control, Computational Cinematography, Character Animation, Cinematic Drones
\end{rSection}

\begin{rSection}{Activities}
{\bf Review} \\
SIGGRAPH/SIGGRAPH Asia (2022, 2023), Transactions on Graphics(2024), Eurographics(2024), Eurographics(2025).

{\bf Mentoring} \\
I am fortunate to (co-)mentor a few highly motivated junior students, Yulong Zhang, ~\href{https://asonin.github.io/}{\LINK{Jason Qin}}, Bangjun Xiao, ~\href{https://daydreamer-f.github.io}{\LINK{Yusu Fang}}.

{\bf Invited Talks}
\begin{itemize}
\item Invited talk on "Example-driven Virtual Cinematography by Learning Camera Behaviors", Apr 2021, Quick Worker Company, Beijing, China.
\item Invited talk on "Learning-based camera control in virtual cinematography", Aug 2022, Huawei Company, Beijing, China.
\item Invited talk on "Virtual Cinematography by Learning Camera Behaviors", Aug 2023, Shanghai AI Lab, Shanghai, China.
\item I also hold close relation with leading gaming and animation companies (Thought Pennies, NetEase, miHoYo, etc.) on discussion and communication to their animation/camera design module.
\end{itemize}

{\bf Public Services}
\begin{itemize}
\item In July 2021, there was a sudden rainstorm in Henan, resulting in a serious disaster. We did a project to collect, update and display the rescue information on the map in real-time. Within a week, we collected a total of \textbf{8,560} pieces of rescue information, \textbf{38,000} independent accounts accessed the web page, and \textbf{280,000} visits were made.
[\href{https://github.com/GiveHenanAHand/henan-rescue-viz-website}{\LINK{page}}][\href{https://mp.weixin.qq.com/s/VinRG0nYoUdkE4wA8_cRnQ}{\LINK{press}}][\href{https://v.youku.com/v_show/id_XNTE5OTAyODYyNA==.html?s=afdea97e2c954bcea2a3&spm=a2hje.13141534.${moduleIndex}_1.d_2_3&scm=20140719.apircmd.240189.video_XNTE5OTAyODYyNA==}{\LINK{documentary}}]
\item In Dec 2020, amidst the global COVID-19 pandemic, I actively engaged in the analysis and visualization of the epidemiological data. We formulated a sophisticated spread model to predict the epidemic's evolution. The work received over \textbf{120,000} visits and was published on \textit{International Journal of Educational Excellence}. [\href{https://arxiv.org/ftp/arxiv/papers/2002/2002.07096.pdf}{\LINK{pdf}}]
\end{itemize}
\end{rSection}
%----------------------------------------------------------------------------------------
% \begin{rSection}{Miscellanous} 
%  I love to travel a lot and trekking, hiking, clicking pictures, reading books and to watch tv series.
 % \item Member, Athletics Team, IIT Kanpur. Attended Summer Sport Camp as a long jumper.
%\item Trained and disciplined in National Cadet Corps (NCC), IIT Kanpur for a year.
 %\item  Participated in Vijyoshi Camp 2012 organized at Indian Institute of Science, Bangalore.
 %\item Won 2nd position in Kho-Kho in Intramurals conducted by Physical Education Section, IIT Kanpur.
 %\item Pursued French as second language during secondary school from Grade 6 to Grade 10. Also participated in French Song Competition and French G.K. Quiz in Class 10th. %

% \end{rSection}


\begin{rSection}{Award}
{\bf Research} \\
Award for Contribution in Student Organizations, Peking University (Ubiquant Scholarship) 2023 \\
Award for Scientific Research Award, Peking University (Schlumberger Limited Scholarship) 2022 \\
Award for Scientific Research Award, Peking University (Third Class Scholarship of Peking University) 2020 \\ 
Computing Star of EECS, Peking University 2020 \\
Excellent Project Award of Peking University Undergraduate President Fund 2018

{\bf Programming} \\
First Place in 16th Computer Programming Contest of Peking University 2017 \\ 
Second Prize in 15th Computer Programming Contest of Peking University 2016 \\ 
Silver Award of ACM CCPC, Hangzhou 2016 \\ 
Second Prize of CCF National Olympiad in Informatics (NOI), China 2014 \\ 
Gold Award of CCF China Team Selection Competition (CTSC), China 2014 \\ 
\end{rSection}

\end{document}

