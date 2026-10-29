"""Evaluate a saved official CIFAR-100 model on all 10,000 test images."""
import argparse
import json
from pathlib import Path
import torch
from mdistiller.engine.cfg import CFG
from mdistiller.dataset import get_dataset
from mdistiller.models import cifar_emodel_dict

parser = argparse.ArgumentParser()
parser.add_argument('--model', required=True)
parser.add_argument('--checkpoint', required=True)
parser.add_argument('--output', required=True)
args = parser.parse_args()
cfg = CFG.clone()
cfg.DATASET.TEST.BATCH_SIZE = 256
_, loader, _, _ = get_dataset(cfg, torch.Generator().manual_seed(42), None)
model = cifar_emodel_dict[args.model][0](num_classes=100).cuda().eval()
checkpoint = Path(args.checkpoint)
model.load_state_dict(torch.load(checkpoint, map_location='cpu', weights_only=True)['model'])
top1 = top5 = total = 0
with torch.no_grad():
    for images, targets in loader:
        logits = model(images.cuda())[0]
        assert torch.isfinite(logits).all()
        predicted = logits.topk(5, dim=1).indices.cpu()
        top1 += predicted[:, 0].eq(targets).sum().item()
        top5 += predicted.eq(targets[:, None]).any(dim=1).sum().item()
        total += targets.numel()
assert total == 10000
result = {'model':args.model,'checkpoint':str(checkpoint),'test_images':total,'top1':100*top1/total,'top5':100*top5/total,'prediction':'argmax(logits), equivalent to argmax(Dirichlet expectation) with shared scalar prior'}
Path(args.output).write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
