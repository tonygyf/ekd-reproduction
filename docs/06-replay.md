# 亲手重走搭建过程

以下在同一工作区操作，不重复创建同名容器、不同时启动第二个正式训练。现有模型和数据可以直接复用。

1. 先读 papers/figure1_page.png 和 figure2_page.png，对照 04-paper-code.md。关键是教师也要是证据网络，而不是随便下载一个普通分类模型。
2. `git -C EKD rev-parse HEAD` 核对来源；`git -C EKD diff` 看最小修复。每一处修复对应 03-issues.md 和 logs 中的实际失败。
3. 看 Dockerfile，再按 02-environment.md 构建镜像、启动容器。NGC 内置 PyTorch/CUDA，不在宿主安装训练依赖。
4. 作者权重下载与解压（已有完整文件时不必重下）：

```bash
docker exec ekd-reproduction gdown --continue \
  19fXKTl_2DsZpiR4SuzXOePG_slyLTMks -O /workspace/artifacts/evidential_teachers.tar
docker exec ekd-reproduction bash -c \
  'mkdir -p evidential_teacher && tar -xf /workspace/artifacts/evidential_teachers.tar --strip-components=5 -C evidential_teacher'
```

5. `python3 scripts/download_cifar.py` 下载、校验原始数据；容器中复制到 data/cifar-100-python.tar.gz 并解压。分段缓存仅用于网络续传。
6. `docker exec ekd-reproduction python /workspace/scripts/smoke.py`：先确认损失公式、梯度和保存重载，不靠“没有报错”判断算法通过。
7. 教师全量评估：

```bash
docker exec ekd-reproduction python /workspace/scripts/evaluate.py \
  --model resnet32x4 --checkpoint evidential_teacher/resnet32x4 \
  --output /workspace/artifacts/teacher-eval.json
```

8. 查看真实数据一轮闭环日志 logs/student-one-epoch.log，再运行 README 中的正式训练命令。该脚本始终用原始 240 轮配置；不将烟测训练轮数带入正式实验。

监控：
```bash
tail -24 artifacts/runs/cifar100_baselines/resnet32x4_resnet8x4_seed42/worklog.txt
cat artifacts/training-status.txt
docker exec ekd-reproduction ps -eo pid,args
```

中断后恢复：保持同一容器、路径和配置，执行 `bash /workspace/scripts/train_student.sh --resume`。恢复使用作者保存的模型、优化器和 epoch；上游没有保存随机数发生器/数据采样器状态，恢复后的轨迹不保证逐位一致。不要在运行中的训练旁启动恢复进程。

最终检查 artifacts/student-best-eval.json 和 student-last-eval.json；`completed` 需 240 轮检查与两次全量评估都成功。论文比较是单次结果对五次均值，不能据此声称严格复现了论文均值。
