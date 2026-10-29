# 运行结果

## 已通过
- Docker 中 GPU 矩阵乘法。
- 官方入口 --help（完成最小导入修复后）。
- 官方教师 checkpoint 结构验证和加载。
- scripts/smoke.py：两类 KL 对照 PyTorch 分布、有限梯度、GPU 学生更新、教师参数与 BatchNorm 状态不变、checkpoint 重载一致。
- 冒烟结构化结果：artifacts/smoke-results.json；输出日志：logs/smoke.log。

## 待完成
原始数据校验、完整测试集教师评估、原 trainer 一轮训练/评估/保存冒烟、240 轮正式训练、独立重载最佳/末轮学生评估。

冒烟的随机输入只验证执行正确性，不能用于报告模型准确率或蒸馏收益。

## 真实数据验证
- CIFAR-100 原始包 MD5 校验成功。
- 官方证据教师：10,000 张测试图 Top-1 **79.53%**，Top-5 **94.86%**，与论文表1教师一致。artifacts/teacher-eval.json。
- 原入口 1 epoch：50,000 张训练图，10,000 张测试图，训练/验证/保存完整通过；Top-1 15.72%，仅作闭环检查。logs/student-one-epoch.log。
- 正式训练：重新 seed=42 初始化学生，240 epochs，使用同一官方证据教师。启动命令记录在 README；输出 logs/train-student.log，checkpoint artifacts/runs/cifar100_baselines/resnet32x4_resnet8x4_seed42/。
- artifacts/training-status.txt 记录 running/failed/completed；只有 latest 的 epoch=240 且全部参数有限、两次重载评估完成后才写 completed。
