"""Download the unchanged official archive in ranges; validate torchvision MD5."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import time
import requests

ROOT = Path(__file__).resolve().parents[1]
URL = "https://cave.cs.toronto.edu/kriz/cifar-100-python.tar.gz"
SIZE = 169001437
CHUNK = 2 * 1024 * 1024
PARTS = ROOT / "artifacts/cifar-parts"
PARTS.mkdir(exist_ok=True)

def fetch(start):
    end = min(start + CHUNK, SIZE) - 1
    path = PARTS / str(start)
    if path.exists() and path.stat().st_size == end - start + 1:
        return path
    for attempt in range(5):
        try:
            response = requests.get(URL, params={"part": start}, headers={"Range": f"bytes={start}-{end}"}, timeout=90)
            response.raise_for_status()
            assert response.status_code == 206, response.status_code
            assert response.headers["Content-Range"] == f"bytes {start}-{end}/{SIZE}"
            assert len(response.content) == end - start + 1
            path.write_bytes(response.content)
            print(f"Downloaded {start}-{end}", flush=True)
            return path
        except (requests.RequestException, AssertionError):
            if attempt == 4:
                raise
            time.sleep(1)

with ThreadPoolExecutor(max_workers=16) as pool:
    paths = list(pool.map(fetch, range(0, SIZE, CHUNK)))
output = ROOT / "artifacts/cifar-100-verified.tar.gz"
with output.open("wb") as writer:
    for path in paths:
        writer.write(path.read_bytes())
assert hashlib.md5(output.read_bytes()).hexdigest() == "eb9058c3a382ffc7106e4002c42a8d85"
print(f"Verified original CIFAR-100 MD5: {output}", flush=True)
