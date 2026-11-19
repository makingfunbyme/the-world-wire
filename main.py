"""Write the finished broadsheet to the competition output directory."""

import os
from pathlib import Path


def main():
    source = Path(__file__).resolve().with_name("entry.png")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    payload = source.read_bytes()
    with open(os.path.join(output_dir, "entry.png"), "wb") as output:
        count = output.write(payload)
    print(f"entry.png: {count} bytes")


if __name__ == "__main__":
    main()
