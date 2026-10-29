# 复现范围与进度

用户决定：先复现原论文，不开展 OCR 迁移；完整跑一个师生组合的 240 轮训练和评估。单次结果不等于论文五次均值。

- 论文：ICCV 2025 Evidential Knowledge Distillation，Xiang / Gao / Xu。
- 官方仓库：https://github.com/Liangyu-Xiang/EKD
- 固定提交：1b65073126c3babe554ad57e78096c436fb6183a
- 实验：CIFAR-100，ResNet32×4 → ResNet8×4，seed=42，官方配置。
- 顺序：来源与图公式核对 → Docker GPU 验证 → 原始入口冒烟 → 最小阻塞修复 → 教师评估 → 学生训练与评估。
- GPU：只向容器暴露宿主 GPU 1。容器内编号为 0。宿主 GPU 0、3 有其他任务。
- 当前：完整 240 轮训练和最佳/末轮全量重载评估均完成。最佳学生 Top-1 77.21%，最佳 epoch=222。公开仓库：https://github.com/tonygyf/ekd-reproduction ，通过已验证的 SSH key 发布。

文档导航：01-sources.md 来源；02-environment.md 环境；03-issues.md 实际问题；04-paper-code.md 图与公式；05-results.md 运行结果。
