

</div>
<div align="center">
<p align="center">
  <img src="assets/logo.png" width="10%" height="10%" />
</p>
</div>

<div align="center">
<h1>OmniThink</h1>
</div>
<div align="center">
<h3>Expanding Knowledge Boundaries in Machine Writing
through Thinking</h3>
</div>

<div align="center">


<!-- **Affiliations:** -->

👏 Welcome to try OmniThink in our **[<img src="./assets/tongyi.png" width="14px" style="display:inline;"> Modelscope online demo](https://www.modelscope.cn/studios/iic/OmniThink)**!

<p align="center">
<a href="https://zjunlp.github.io/project/OmniThink">[🤖Project]</a>
<a href="">[📄Paper]</a>
<!-- <a href="## 🚩Citation">[🚩Citation]</a> -->

</div>
<div align="center">
<p align="center">
  <img src="assets/overview.jpg" width="50%" height="50%" />
</p>
</div>

## Table of Contents

- ⚠️[Announcement](#Announcement)
- 🌻[Quick Start](#quick-start)
- 🌟[Introduction](#Introduction)
- 🔧[Dependencies](#Dependencies)
- 📉[Results](#Results)
- 🧐[Evaluation](#evaluation)
- 🚩[Acknowledgement](#Acknowledgement)

---
## ⚠️ Announcement 
Due to the recent high volume of visitors, search API quota limitations, you may encounter an error: 'ValueError: Expected 2D array, got 1D array instead: array=[]. Reshape your data either using array.reshape(-1, 1) if your data has a single feature or array.reshape(1, -1) if it contains a single sample.' If this error occurs, please try again in a few hours.

## 📖 Quick Start

- 🌏 The **Online Demo** is avaiable at [ModelScope](https://www.modelscope.cn/studios/iic/OmniThink) now！


<img src="assets/demo.gif">

# 📌 Introduction

Welcome to **OmniThink**, an innovative machine writing framework designed to replicate the human cognitive process of iterative expansion and reflection in generating insightful long-form articles. 

- **Iterative Expansion and Reflection**: OmniThink uses a unique mechanism that simulates human cognitive behaviors to deepen the understanding of complex topics.
- **Enhanced Knowledge Density**: OmniThink focuses on expanding knowledge boundaries, resulting in articles that are rich in information and insights.
- **Comprehensive Article Generation**: OmniThink constructs outlines and generates articles, delivering high-quality content that is both coherent and contextually robust.
<div align="center">
    <img src="assets/main.jpg" width="80%" height="auto" />
</div>



# 🛠 Dependencies

```bash
conda create -n OmniThink python=3.11
git clone https://github.com/zjunlp/OmniThink.git
cd OmniThink
# Install requirements
pip install -r requirement.txt

```
🔑 Before running, please export the OPENAI API key or Dashscope API key and SEARCH key as an environment variable:

```bash
export OPENAI_API_KEY=YOUR_API_KEY
export SEARCHKEY=YOUR_SEARCHKEY
```

or

```bash
export DASHSCOPE_KEY=YOUR_API_KEY
export SEARCHKEY=YOUR_SEARCHKEY
```
> You can define your own [LLM API](https://github.com/zjunlp/OmniThink/blob/main/src/tools/lm.py) and [SEARCH API](https://github.com/zjunlp/OmniThink/blob/main/src/tools/rm.py)

> Note that the output of the LLM should be a LIST.

# Results in OmniThink
The preformance of OmniThink is shown below:
<div align="center">
    <img src="assets/table.jpg" width="95%" height="auto" />
</div>

# Generate Article in OmniThink
Just one command required
```bash
sh run.sh
```
You can find your Article, Outline and mindmap in ./results/

# 🔍 Evaluation

We are organizing the evaluation code and will open source it soon.


# 🌻Acknowledgement

- This work is implemented by [DsPY](https://github.com/stanfordnlp/dspy), [STORM](https://github.com/stanford-oval/storm) Sincere thanks for their efforts.
- if you have any questions, please feel free to contact via xizekun.xzk@alibaba-inc.com, 1786594371@qq.com or xizekun2023@zju.edu.cn or create an issue.


