# 实际阻塞与最小修复

原则：先运行原实现，保留失败日志，再修复已经确认的阻塞；不改蒸馏算法和实验超参数。

## 1. 无用 GUI 依赖阻止导入
- 命令：容器中 `python tools/train.py --help`。
- 原始日志：logs/original-import.log。
- 报错：MLKD.py 导入 turtle，间接导入 tkinter，容器未安装 GUI 组件。
- 检查：`rg -n '\bst\b' mdistiller/distillers/MLKD.py` 只有导入行。
- 修复：删除未使用的 `from turtle import st`，无需安装桌面组件。
- 后续验证：logs/import-after-turtle.log。

## 2. 注册表类名与残留条目
- logs/import-after-turtle.log：导入不存在的 Teacher；实际类为 Evidential_Teacher。
- 同一注册表还引用了整个仓库中不存在的 Monitor。
- 修复类名，删除无效 Monitor 注册；`python tools/train.py --help` 通过，见 logs/import-fixed.log。

## 3. 教师构造读取未定义配置
- logs/teacher-constructor-original.log：AttributeError: CLF_TYPE。
- self.efunction 只有赋值、未被读取；实际前向固定 exp，与论文一致。
- 删除无用读取，不添加新超参数。

## 4. 下载与解压
- gdown 两次 IncompleteRead；使用 --continue 续传成功。logs/download-teachers*.log。
- 官方 tar 含作者目录前缀 data/mmc_lyxiang/KD/logit-standardization-KD-master/evidential_teacher/，不是 README 所写的直接根目录。
- 解压命令：`mkdir -p EKD/evidential_teacher; tar -xf artifacts/evidential_teachers.tar --strip-components=5 -C EKD/evidential_teacher`。
- tar SHA256：297b045897400770dee68a0a8add067efbefdaeed776dc6b5fb1988a6ff3a709。
- 初次宿主解压失败是目标 data 目录由容器 root 创建，改由容器解压到正确层级。

## 5. EKD 入口加载了普通教师路径
- tools/train.py 的 EKD 分支从 cifar_model_dict 读取普通 softmax 教师；下载的证据教师在 cifar_emodel_dict。
- 实际旧路径加载失败见 logs/teacher-wrong-path.log；证据教师可加载见 logs/teacher-load.log。
- 只修改 EKD 分支使用 cifar_emodel_dict，不影响其他蒸馏方法。

## 6. CIFAR-100 源站速度低
- 原入口自动下载约 70–90 KB/s，完整包需半小时以上。
- 为避免改数据格式，scripts/download_cifar.py 对原站支持 Range 的原始 tar 分段下载，检查每段 Content-Range/长度并最终校验 torchvision 的 MD5。
- 仍使用原图像、标签、划分、增强和官方 dataloader。没有用 Hugging Face 重编码数据冒充原始包。
- 发现源站 GET 会跳转到 cave.cs.toronto.edu，分段下载直接使用该地址。
- 早期入口只完成了部分下载即停止；之后用完整验证文件替换，不将中断日志作为训练证据。
