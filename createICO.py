from pathlib import Path
from PIL import Image

source_dir = Path("icons")
output_dir = Path("ico files")
output_dir.mkdir(exist_ok=True)

for png_path in source_dir.glob("*.png"):
    ico_path = output_dir / f"{png_path.stem}.ico"

    image = Image.open(png_path).convert("RGBA")
    image.save(
        ico_path,
        format="ICO",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48)]
    )

print("Done")