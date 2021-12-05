# Code for the course project

## Index

1. Introduction of the code organization
2. Usage

## Introduction

This code contains two folders. The src folder contains the code you are going
to run.

The graphs folder contains the graphs I generated with this code and
two original figures I selected from the paper to replicate. Graphs I generated
with this code are saved in `./graphs/generated/` and original figures for your
refrence is saved in `./graphs/original_figures/`.

Only the rca_m.py file will be used to generate those two graphs. The ucb_m.py
script does not generate exact same graph and will need more work. The dataset.py
does not contain any useful code besides two classes defined there. The rests are
transition probability table, mean reward for each arms, and some customized data.

## Usage

All you need to do is just type `python3 src/rca_m.py`. Graphs will be generated
in `./graphs/`.

Depends on the performance of the host computer, the whole process should be
finished in 1 min, at maximum. On my computer, it only took around 20 seconds
and I am using a laptop with i7-6700HQ, so it should take less time on your
computer.
