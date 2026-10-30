EKD experiment evidence archive. Contains full training logs, all retained run checkpoints, official evidence teachers and environment snapshots. Raw CIFAR data, download fragments, caches, papers and duplicate smoke models are excluded because they are reproducible from recorded sources.

Lossless zstd long-window compression preserves all evidence while deduplicating checkpoint content.

Restore: `cat evidence.tar.zst.part*.bin > /tmp/ekd-evidence.tar.zst`; verify the archive and part SHA256 checksums in manifest.json; then `zstd -d --long=29 /tmp/ekd-evidence.tar.zst -c | tar -xf -`. Code, fixes, reports and replay scripts are in the repository root.

Archive parts use Git LFS. Install Git LFS, clone normally, and run `git lfs pull` before verifying and concatenating the parts. LFS authenticates through the same SSH GitHub remote.
