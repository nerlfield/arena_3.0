import streamlit as st

def section():

    st.sidebar.markdown(
r"""
## Table of Contents

<ul class="contents">
    <li class='margtop'><a class='contents-el' href='#introduction'>Introduction</a></li>
    <li class='margtop'><a class='contents-el' href='#content-learning-objectives'>Content & Learning Objectives</a></li>
    <li><ul class="contents">
        <li><a class='contents-el' href='#rlhf-on-transformer-language-models'>RLHF on transformer language models</a></li>
        <li><a class='contents-el' href='#bonus'>Bonus</a></li>
    </ul></li>
    <li class='margtop'><a class='contents-el' href='#reading'>Reading</a></li>
    <li class='margtop'><a class='contents-el' href='#setup'>Setup</a></li>
</ul></li>""", unsafe_allow_html=True)

    st.markdown(
r"""
# [2.4] RLHF

### Colab: [**exercises**](https://colab.research.google.com/drive/13TDGeRdUcZ30nlfkN_PAxQxe8oX2x49u?usp=sharing) | [**solutions**](https://colab.research.google.com/drive/1KEXcflwuTGxf6JkAWdDCveXldDs6qgfw?usp=sharing)

Please send any problems / bugs on the `#errata` channel in the [Slack group](https://join.slack.com/t/arena-la82367/shared_invite/zt-1uvoagohe-JUv9xB7Vr143pdx1UBPrzQ), and ask any questions on the dedicated channels for this chapter of material.

You can toggle dark mode from the buttons on the top-right of this page.

Links to other chapters: [**(0) Fundamentals**](https://arena3-chapter0-fundamentals.streamlit.app/), [**(1) Transformer Interp**](https://arena3-chapter1-transformer-interp.streamlit.app/).

<img src="https://raw.githubusercontent.com/callummcdougall/computational-thread-art/master/example_images/misc/shoggoth.png" width="350">

## Introduction

In this section, you'll implement Deep Q-Learning, often referred to as DQN for "Deep Q-Network". This was used in a landmark paper [Playing Atari with Deep Reinforcement Learning](https://www.cs.toronto.edu/~vmnih/docs/dqn.pdf).

At the time, the idea that convolutional neural networks could look at Atari game pixels and "see" gameplay-relevant features like a Space Invader was new and noteworthy. In 2022, we take for granted that convnets work, so we're going to focus on the RL aspect and not the vision aspect today.



## Content & Learning Objectives


#### 1️⃣ RLHF on transformer language models

Most of the exercises today build towards the implementation of the `RLHFTrainer` class, similar to how DQN and PPO have worked these last few days.

> ##### Learning objectives
> 
> - Understand how the RL agent / action / environment paradigm works in the context of autoregressive transformer models
> - Understand how the RLHF algorithm works, and how it fits on top of PPO
> - Learn about value heads, and how they can be used to turn transformers into actor & critic networks with shared architectures
> - Write a full RLHF training loop, and use it to train your transformer with the "maximize output of periods" reward function
> - Observe and understand the instances of mode collapse that occur when training with this reward function
> - Experiment with different reward functions, and training parameters

#### 2️⃣ Bonus

This section offers some suggested ways to extend the core RLHF exercises.

> #### Learning objectives
>  
> - Improve your RLHF implementation via techniques like differential learning rates, frozen layers, or adaptive KL penalties
> - Perform some exploratory mechanistic interpretability on RLHF'd models
> - Learn about the trlX library, which is designed to train transformers via RLHF in a way which abstracts away many of the low-level details

## Reading

- [Illustrating Reinforcement Learning from Human Feedback (RLHF)](https://huggingface.co/blog/rlhf) (~10 minutes)
    - An accessible and mostly non-technical introduction to RLHF, which discusses it in context of the full pipeline for training autoregressive transformer language models (starting with pretraining, which is what we did in the first day of last week).
- [RLHF+ChatGPT: What you must know](https://www.youtube.com/watch?v=PBH2nImUM5c) (~5 minutes)
    - The first half of this video provides a high-level overview of RLHF, discussing things like mode collapse, and relates this to the [shoggoth meme](https://i.kym-cdn.com/photos/images/original/002/546/572/bd3.png) that many of you have likely seen!

## Setup


```python
import torch as t
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
import torch.optim as optim
import wandb
import torch
import transformers
from transformer_lens.hook_points import HookPoint
from transformer_lens import utils, HookedTransformer
from typing import List, Optional, Tuple, Union, Dict, Any, Callable
import einops
from jaxtyping import Float, Int
import os
import sys
from pathlib import Path
from rich import print as rprint
from rich.table import Table
from eindex import eindex
from dataclasses import dataclass
from IPython.display import display, clear_output
import numpy as np
import time
from functools import partial

# Make sure exercises are in the path
chapter = r"chapter2_rl"
exercises_dir = Path(f"{os.getcwd().split(chapter)[0]}/{chapter}/exercises").resolve()
section_dir = exercises_dir / "part4_rlhf"
if str(exercises_dir) not in sys.path: sys.path.append(str(exercises_dir))

import part4_rlhf.tests as tests
import part4_rlhf.solutions as solutions

device = t.device("cuda" if t.cuda.is_available() else "cpu")

MAIN = __name__ == "__main__"
```

""", unsafe_allow_html=True)
