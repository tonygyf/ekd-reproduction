"""Check official losses, frozen teacher, GPU update, and checkpoint roundtrip."""
import json
from pathlib import Path
import torch
from mdistiller.engine.cfg import CFG
from mdistiller.models import cifar_emodel_dict
from mdistiller.distillers import distiller_dict
from mdistiller.distillers.EKD import compute_ekd_loss, evidential_first_order_loss

root = Path('/workspace')
torch.manual_seed(42)
torch.set_num_threads(8)
s = (torch.rand(8, 100, dtype=torch.float64) + .3).requires_grad_()
t = torch.rand(8, 100, dtype=torch.float64) + .3
actual = compute_ekd_loss(s, t)
expected = torch.distributions.kl_divergence(torch.distributions.Dirichlet(t), torch.distributions.Dirichlet(s)).mean()
torch.testing.assert_close(actual, expected)
torch.testing.assert_close(compute_ekd_loss(t, t), torch.tensor(0., dtype=torch.float64))
first = evidential_first_order_loss(s, t)
first_expected = torch.distributions.kl_divergence(torch.distributions.Categorical(probs=t), torch.distributions.Categorical(probs=s)).mean()
torch.testing.assert_close(first, first_expected)
(actual + first).backward()
assert torch.isfinite(s.grad).all()
cfg = CFG.clone()
cfg.merge_from_file('configs/cifar100/ekd/resnet32x4_resnet8x4.yaml')
teacher = cifar_emodel_dict['resnet32x4'][0](num_classes=100)
teacher.load_state_dict(torch.load('evidential_teacher/resnet32x4', map_location='cpu', weights_only=True)['model'])
student = cifar_emodel_dict['resnet8x4'][0](num_classes=100)
d = distiller_dict['EKD'](student, teacher, cfg).cuda().train()
optimizer = torch.optim.SGD(d.get_learnable_parameters(), lr=.05, momentum=.9)
x = torch.randn(8, 3, 32, 32, device='cuda')
y = torch.arange(8, device='cuda')
before = d.student.conv1.weight.detach().clone()
teacher_before = {k:v.clone() for k,v in d.teacher.state_dict().items()}
_, losses = d(image=x, target=y, epoch=1)
loss = sum(losses.values())
assert torch.isfinite(loss)
loss.backward()
assert all(p.grad is None for p in d.teacher.parameters())
assert all(torch.isfinite(p.grad).all() for p in d.student.parameters() if p.grad is not None)
optimizer.step()
assert not torch.equal(before, d.student.conv1.weight)
assert all(torch.equal(v, teacher_before[k]) for k,v in d.teacher.state_dict().items())
d.eval()
with torch.no_grad(): reference = d(image=x)
checkpoint = root / 'artifacts/smoke_student.pt'
torch.save({'model': d.student.state_dict()}, checkpoint)
reloaded = cifar_emodel_dict['resnet8x4'][0](num_classes=100).cuda().eval()
reloaded.load_state_dict(torch.load(checkpoint, weights_only=True)['model'])
with torch.no_grad(): torch.testing.assert_close(reference, reloaded(x)[0])
result = {'status':'passed', 'device':torch.cuda.get_device_name(), 'dirichlet_kl':actual.item(), 'first_order_kl':first.item(), 'gpu_losses':{k:v.item() for k,v in losses.items()}, 'teacher_frozen':True,'student_updated':True,'checkpoint_roundtrip':True}
(root/'artifacts/smoke-results.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
