# 来源与权重

- 正文：https://openaccess.thecvf.com/content/ICCV2025/papers/Xiang_Evidential_Knowledge_Distillation_ICCV_2025_paper.pdf
- 补充：https://openaccess.thecvf.com/content/ICCV2025/supplemental/Xiang_Evidential_Knowledge_Distillation_ICCV_2025_supplemental.pdf
- PDF、提取文本、图1整页渲染存于 papers/。
- 官方代码：https://github.com/Liangyu-Xiang/EKD ，论文旧地址 lyxiang-casia/EKD 已跳转到该仓库。
- 官方教师：README 链接 https://drive.google.com/file/d/19fXKTl_2DsZpiR4SuzXOePG_slyLTMks/view
- Hugging Face：公开 models/datasets API 搜索 Evidential，未发现可以确认属于该论文的权重。原始响应在 artifacts/hf_*_search.json。不能把其他同名 EKD 权重当作本论文教师。
- GitHub releases API 返回空列表，见 artifacts/github_releases.json。

2026-10-29 检索。官方分类实验没有 OCR 数据集、文本识别器或字符序列对齐代码。

CIFAR-100 原始包：`https://cave.cs.toronto.edu/kriz/cifar-100-python.tar.gz`（Toronto 原站重定向目标）；大小 169001437 bytes，MD5 `eb9058c3a382ffc7106e4002c42a8d85`，已核验。完整包为 artifacts/cifar-100-verified.tar.gz。训练读取 EKD/data/cifar-100-python/。
