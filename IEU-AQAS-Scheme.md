# Introduction

The scheme here adapts IEU specific structure of Business Faculty curriculum into a general scheme usable for AQAS accreditation.

# Design: Curriculum and its outcomes

## Program outcomes (PO)

Each program, $p$, is defined as a set of program outcomes, $O_p$.

## Curriculum courses and learning outcomes (LO)

Let $C_p$ be the set of core courses in a diploma programme, $p$. For any course, $c \in C_p$, there is a set of learning outcomes, $L_c$.

Each course has a set of assessment activities, $A_c$. Each activity of a course, $a \in A_c$, contributes to one or more of the course learning outcomes. For example, $LOcontrib(a,l)$ is the  contribution of activity $a \in A_c$ to learning outcome $l \in L_c$. These contributions form a preliminarly A-to-LO contribution matrix for the course, $`X'_c`$ , whose elements are $`x'_{a,l}= LOcontrib(a,l)`$ .

For the sake of simplicity the matrix $X'_c$ is a binary matrix, i.e. the values $LOcontrib(a,l)$ can take only values 0 or 1. However, there is also the problem that activities are of  different weightage, $w_{c,a}$, for ming a weightage matrix of the course activities, $\mathbf{w_c}$. For example, weight of final exam can be 30% (i.e. 0.3) whereas a homework can be 10%. To account for these differences we use a weighted A-to-LO contribution matrix: $X_c=\mathbf{w_c} X'_c$

Each course also has an ECTS credit value, $ects(c)$ which will be used later for the level of contribution.

# From LO to PO

In order to assess achievement of program outcomes, $O_p$, for a course in the program, $c \in C_p$ its learning outcomes will be mapped to program outcomes. For example contribution value of a learning outcome, $l \in L_c$ to a program outcome, $o \in O_p$ is denoted as $POcontrib(l,o)$. These contributions form a LO-to-PO contribution matrix for the program, $Y_c$, whose elements are $y_{l,o}=POcontrib(l,o)$.

For the sake of simplicity the matrix $Y_c$ is a binary matrix, i.e. the values $POcontrib(l,o)$ can take only values 0 or 1.

# Evaluation

## Curriculum level evaluation: Support for program outcomes

Here the aim is to evaluate the level which courses in the curriculum, via their learning outcomes, support the program outcomes.

A first step to compute this would be to compute contribution of a course to programme outcomes as $T^c=Y_c^T X_c$, and collapse the activities level to obtain a vector of PO contributions of a course. Let us denote this resulting vector as $\mathbf{z^c}$ whose elements represent contribution of the course to each program outcome, $z^c_i=\sum_{j}t_{i,j}$

One can then sum this over all courses in a program's curriculum to find the support for program outcomes: $\sum_{c \in C_p}\mathbf{z^c}$. However, the main problem here is that courses have different ECTS values, different number of outcomes and different number of program outcomes each contributes to. Thus, the total contribution of a course, $TotalContrib(c)=\sum\mathbf{z^c}$, can be very different across courses and not necessarily proportional to course credits. Hence a **normalization** is needed. A straightforward solution is to ensure that sum of contributions of a course is equal to its ECTS credit, by normalizing as:

$$ \mathbf{z^c_{norm}}=\mathbf{z^c} \frac{ects(c)}{TotalContrib(c)}$$

### Summary program outcomes matrix

To find the support of the whole curriculum for each of the program outcomes sum normalized contributions of all courses: 

$$\sum_{c \in C_p} \mathbf{z^c_{norm}}$$

## Field level: Evidence based evaluation

Let's say a student get some grades from all his/her courses. How much he/she achieved program outcomes? YUKARIDAKİ HESABI YAPARKEN X MATRİSİNİ ÖĞRENCİ NOT MATRİSİYLE ÇARPARAK YAPILACAK.

Let's say the program has several students. What is the overall level of achievement of program outcomes? TÜM BÖLÜM ÖĞRENCİLERİNİN ACHIEVEMENT'LARIN ORTALAMASI ALINACAK.