# Ingenx TOT Reasoning

## Contents
- [Introduction](#introduction)
- [High-Level Overview](#high-level-overview)
- [Detailed Step-by-Step](#detailed-step-by-step)
  - [Initialization (Level 0)](#initialization-level-0)
  - [Generating Level 1](#generating-level-1)
  - [Generating Level 2](#generating-level-2)
  - [Growing the Tree & Pruning](#growing-the-tree--pruning)
- [Sorting & Score Propagation](#sorting--score-propagation)
- [Why This Approach Works](#why-this-approach-works)

## Introduction
Ingenx TOT (Tree of Thought) reasoning builds upon concepts from [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601). The approach systematically explores partial solutions in a tree structure using two models:

1. **Solver Model** - Proposes steps towards a solution.
2. **Reward Model** - Evaluates or rates each step.

## High-Level Overview

1. **Root Node (the question)**  
   - The process starts with a single node (Level 0), which contains only the **question** or **problem statement**.
   
2. **Expansion (Solver Model)**  
   - The solver model generates multiple candidate steps (e.g., 3 different approaches), creating new child nodes.
   
3. **Evaluation (Reward Model)**  
   - Each child node’s partial solution is **rated** by the reward model.

4. **Sorting & Pruning**  
   - Child nodes are sorted by their scores (lowest on the left, highest on the right).  
   - Low-rated nodes are pruned after a certain threshold to save memory.

5. **Iterative Tree Growth**  
   - This process (expand → evaluate → sort → prune) continues level by level.  
   - Eventually, the best path (or best few paths) from root to leaf is selected as the final solution.

## Detailed Step-by-Step
![image](https://github.com/user-attachments/assets/084402ce-fa30-4672-a8d4-8db7bf15ea8a)


### Initialization (Level 0)
- The **root node** contains only the problem statement.
- This represents **level 0** of the tree.

### Generating Level 1
1. **Expansion**: The solver model generates three possible step-1 approaches.
2. **Creating Child Nodes**: These three ideas become child nodes under the root.
3. **Evaluation & Sorting**: Each child is rated by the reward model and sorted from lowest to highest score.

### Generating Level 2
- Each node at Level 1 expands into **three children**, forming Level 2.
- Ingenx TOT introduces **sibling awareness**:
  - When expanding a node \(N\), you provide:
    - **Current approach** = node \(N\) and its parent steps.
    - **Low-score approach** = left sibling’s path (if it exists).
    - **High-score approach** = right sibling’s path (if it exists).
- Each of these nodes is scored, sorted, and possibly pruned.

### Growing the Tree & Pruning
1. The process continues iteratively at deeper levels.
2. After a chosen level (e.g., Level 3), nodes below a score threshold are **pruned**.
3. Eventually, the highest-rated path from root to leaf is chosen as the solution.

## Sorting & Score Propagation
- **Child-Level Sorting**: Children are sorted by their reward scores.
- **Parent Reordering**: Parent scores may be updated based on child scores and re-sorted.
- **Threshold-Based Pruning**: Nodes below a threshold are discarded.

## Why This Approach Works
1. **Multiple Paths Exploration**: Several candidate steps at each level allow exploration of different solutions.
2. **Feedback via Reward Model**: Each step is rated to prioritize promising paths.
3. **Sibling Awareness**: Passing low-score and high-score approaches helps refine solutions.
4. **Hierarchical Sorting & Pruning**: Sorting prioritizes strong candidates, and pruning prevents exponential growth.
5. **Iterative Deepening**: Solutions are refined step by step, ideal for complex reasoning tasks.

