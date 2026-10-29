# 论文图、公式和实现对应

已阅读正文 PDF，并渲染查看图1和方法页；原始页面保留在 papers/。

| 论文 | 原理 | 官方实现 |
| --- | --- | --- |
| 图1(a) | softmax 后只对齐一个类别概率向量 | distillers/KD.py |
| 图1(b) | 网络输出构造 Dirichlet，同时对齐期望和整个分布 | distillers/EKD.py |
| 式1 | 对 Dirichlet 积分后的监督交叉熵，含 digamma | EKD.forward_train 中 loss_ce；Evidential_Teacher.forward_train |
| 式3、4 | 期望为 alpha / sum(alpha)，对齐 KL(教师期望 || 学生期望) | evidential_first_order_loss |
| 式5 | KL(Dir(alpha_teacher) || Dir(alpha_student)) | compute_ekd_loss；lgamma、digamma 闭式表达 |
| 式6 | 结合一阶与二阶蒸馏，另加监督损失训练 | losses_dict 中 loss_ce + loss_ekd |
| 图2 | 比例相同但总浓度不同，期望相同，分布仍可不同 | smoke.py 的分布 KL 参考验证；该图是解释性示意，并非 OCR 结构图 |

实现中的正数先验为 exp(lamb)，配置 -1.22 对应约 0.295；不是负浓度。教师预训练时可学习该参数，学生配置固定复制作者值。

一阶与 CE 使用 alpha=exp(logits)+exp(lamb)；二阶使用 log1p(exp(logits))+exp(lamb)。正文式5之后明确提出 log(1+x) 平滑以避免数值过大，保留作者实际实现。二阶 warmup=min(epoch/30,1)。

配置：batch 64，SGD lr 0.05，momentum .9，weight decay .0005，240 epochs，150/180/210 衰减；CE/一阶/二阶权重为 1/4.5/4.5。

已知实现限制（未做无关修改）：EKD.ce_loss_weight 虽被读取但未乘到 loss_ce；本次官方配置 CE=1，因此没有数值影响。固定 lamb 是 CPU 标量张量而非 buffer，单卡 CUDA 实测正常。

验证方案：smoke.py 对照 torch.distributions 的 Dirichlet 和 Categorical KL，检验方向与公式；再检验真实教师加载、GPU 反向、教师不变和 checkpoint 重载。

评估按 logits 的 top1/top5，和共享正先验下 Dirichlet 期望的 argmax 相同。未把未校准 logits 当作置信度评估。

论文表1该组合：EDL 教师 79.53%，EDL 独训学生 72.77%，EKD 学生 77.21%，是五次运行均值。本轮单 seed=42 结果只能作单次比较。

图2可亲手算的例子：教师 alpha=(4,5,2)，学生 alpha=(8,10,4)，期望完全相同。实际调用官方损失，一阶 KL=0，Dirichlet KL>0（数值见 logs/figure2-scale-check.log）。这说明只匹配类别概率会漏掉浓度信息。
