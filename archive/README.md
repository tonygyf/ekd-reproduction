EKD experiment evidence archive. Contains full training logs, all retained run checkpoints, official evidence teacher and environment snapshots. Raw CIFAR data, download fragments, caches, papers and duplicate smoke models are excluded because they are reproducible from recorded sources.

Restore: `cat evidence.tar.gz.part*.bin > /tmp/ekd-evidence.tar.gz` then verify the SHA256 in manifest.json and extract with `tar -xzf /tmp/ekd-evidence.tar.gz`. Code, fixes, reports and replay scripts are in the repository root.
