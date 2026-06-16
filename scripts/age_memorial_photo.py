"""Apply vintage aging effects to the memorial photo."""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "沱龙峡留念.png"
OUTPUT_PATH = BASE_DIR / "沱龙峡留念.png"
SEED = 202507


def _sepia_tone(arr: np.ndarray) -> np.ndarray:
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    out = np.stack(
        [
            r * 0.393 + g * 0.769 + b * 0.189,
            r * 0.349 + g * 0.686 + b * 0.168,
            r * 0.272 + g * 0.534 + b * 0.131,
        ],
        axis=-1,
    )
    return np.clip(out, 0, 255)


def _vignette(arr: np.ndarray, strength: float = 0.42) -> np.ndarray:
    h, w = arr.shape[:2]
    y, x = np.ogrid[:h, :w]
    cy, cx = (h - 1) / 2.0, (w - 1) / 2.0
    max_dist = np.sqrt(cy**2 + cx**2)
    dist = np.sqrt((y - cy) ** 2 + (x - cx) ** 2) / max_dist
    mask = 1.0 - strength * (dist**1.8)
    return np.clip(arr * mask[..., None], 0, 255)


def _add_grain(arr: np.ndarray, amount: float = 14.0) -> np.ndarray:
    noise = np.random.normal(0, amount, arr.shape)
    return np.clip(arr + noise, 0, 255)


def _add_warm_fade(arr: np.ndarray) -> np.ndarray:
    h, w = arr.shape[:2]
    gradient = np.linspace(1.0, 0.92, h)[:, None]
    warm = np.array([18.0, 10.0, -8.0], dtype=np.float32)
    faded = arr * 0.88 + warm
    faded *= gradient[..., None]
    return np.clip(faded, 0, 255)


def _add_spots(draw: ImageDraw.ImageDraw, width: int, height: int, rng: random.Random) -> None:
    for _ in range(28):
        x = rng.randint(0, width - 1)
        y = rng.randint(0, height - 1)
        radius = rng.randint(2, 9)
        alpha = rng.randint(18, 45)
        color = (120, 90, 45, alpha)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)


def _add_scratches(draw: ImageDraw.ImageDraw, width: int, height: int, rng: random.Random) -> None:
    for _ in range(16):
        x1 = rng.randint(0, width - 1)
        y1 = rng.randint(0, height - 1)
        length = rng.randint(40, 220)
        angle = rng.uniform(-0.4, 0.4)
        x2 = int(x1 + length * np.cos(angle))
        y2 = int(y1 + length * np.sin(angle))
        alpha = rng.randint(25, 70)
        draw.line((x1, y1, x2, y2), fill=(220, 210, 180, alpha), width=1)


def _add_crease_overlay(overlay: Image.Image, width: int, height: int) -> None:
    draw = ImageDraw.Draw(overlay, "RGBA")
    draw.line((width * 0.18, 0, width * 0.22, height), fill=(90, 70, 40, 22), width=2)
    draw.line((width * 0.78, 0, width * 0.74, height), fill=(90, 70, 40, 18), width=1)


def apply_aging(input_path: Path, output_path: Path) -> None:
    rng = random.Random(SEED)
    np.random.seed(SEED)

    img = Image.open(input_path).convert("RGB")
    width, height = img.size

    arr = np.array(img, dtype=np.float32)
    arr = arr * 0.96 + 8.0
    arr = _sepia_tone(arr)
    arr = arr * 0.82 + np.array([34.0, 24.0, 8.0], dtype=np.float32)
    arr = _add_warm_fade(arr)
    arr = _vignette(arr, strength=0.38)
    arr = _add_grain(arr, amount=11.0)

    aged = Image.fromarray(arr.astype(np.uint8))
    aged = aged.filter(ImageFilter.GaussianBlur(radius=0.45))
    aged = ImageEnhance.Sharpness(aged).enhance(0.82)
    aged = ImageEnhance.Contrast(aged).enhance(0.9)
    aged = ImageEnhance.Brightness(aged).enhance(0.97)

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    _add_spots(draw, width, height, rng)
    _add_scratches(draw, width, height, rng)
    _add_crease_overlay(overlay, width, height)

    result = Image.alpha_composite(aged.convert("RGBA"), overlay).convert("RGB")
    result.save(output_path, quality=95)


if __name__ == "__main__":
    apply_aging(INPUT_PATH, OUTPUT_PATH)
    print(f"Aged photo saved to: {OUTPUT_PATH}")
