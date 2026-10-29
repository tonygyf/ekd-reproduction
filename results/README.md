# 验证结果

本次 CIFAR-100 / ResNet32×4 → ResNet8×4 / seed 42 完成 240 轮。

最佳学生 Top-1 **77.21%**，末轮 **77.11%**，官方教师 **79.53%**。

summary.json 保存实验摘要；training-metrics.csv 保存上游舍入后的逐轮指标；learning-curves.png/svg 为训练曲线；其余 JSON 是独立重载或冒烟检查结果。详细解释见 ../docs/05-results.md。
