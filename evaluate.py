import argparse, json
from pathlib import Path
from core import benchmark

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--live", action="store_true")
    a = p.parse_args()
    r = benchmark(a.live)
    out = "live_results.json" if a.live else "results.json"
    Path(out).write_text(json.dumps(r, indent=2) + "\n")
    print(json.dumps(r, indent=2))
