import os
import re
import unicodedata
from pathlib import Path

import cloudinary
from cloudinary import uploader


ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "Images"


def public_id_for(path: Path) -> str:
    value = unicodedata.normalize("NFKD", path.stem)
    value = value.encode("ascii", "ignore").decode("ascii").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return f"chez-aigba/{value}"


cloudinary.config(
    cloud_name=os.environ["CLOUDINARY_CLOUD_NAME"],
    api_key=os.environ["CLOUDINARY_API_KEY"],
    api_secret=os.environ["CLOUDINARY_API_SECRET"],
    secure=True,
)

images = sorted(
    path for path in IMAGE_DIR.iterdir()
    if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
)

if not images:
    raise SystemExit("No images found in Images/")

for image in images:
    result = uploader.upload(
        str(image),
        public_id=public_id_for(image),
        overwrite=True,
        resource_type="image",
        use_filename=False,
        unique_filename=False,
    )
    print(f"Uploaded {image.name} -> {result['secure_url']}")
