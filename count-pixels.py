from PIL import Image
import numpy as np

# ---------------------------------------------------
# CONFIGURATION — must match the color map used in your PNG renderer
# ---------------------------------------------------

COLOR_MAP = {
    "🟥": (255, 0, 0),       # Red
    "🟧": (255, 128, 0),     # Orange
    "🟨": (255, 255, 0),     # Yellow
    "🟩": (0, 200, 0),       # Green
    "🟦": (0, 100, 255),     # Blue
    "🟪": (150, 0, 200),     # Violet
    "⬛": (0, 0, 0),         # Black (G+D letters)
    "⬜": (255, 255, 255),   # White (optional)
}

# If each emoji-pixel was rendered as N×N block
PIXEL_SIZE = 10   # Must match your md_pixels_to_png.py setting


# ---------------------------------------------------
# FUNCTION: Count occurrences of each logical pixel
# ---------------------------------------------------

def count_pixels_from_png(path):
    img = Image.open(path).convert("RGB")
    arr = np.array(img)

    height, width, _ = arr.shape

    # Compute logical grid size
    grid_h = height // PIXEL_SIZE
    grid_w = width // PIXEL_SIZE

    # Reverse lookup table: RGB → emoji name
    RGB_TO_LABEL = {v: k for k, v in COLOR_MAP.items()}

    # Counters
    counts = {emoji: 0 for emoji in COLOR_MAP.keys()}

    # Loop over logical pixel grid
    for gy in range(grid_h):
        for gx in range(grid_w):

            # Extract the RGB value of the block's top-left pixel
            # (all pixels in the block should match)
            pixel_rgb = tuple(arr[gy * PIXEL_SIZE, gx * PIXEL_SIZE])

            # Determine which emoji color it belongs to
            emoji = RGB_TO_LABEL.get(pixel_rgb, None)

            if emoji:
                counts[emoji] += 1
            else:
                # Unknown color — you may want to handle this
                pass

    return counts, grid_w * grid_h


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":
    png_path = "preview.png"   # Input file

    counts, total = count_pixels_from_png(png_path)

    # Filter out white and black pixels (only count color pixels)
    color_pixels = {emoji: count for emoji, count in counts.items() 
                      if emoji not in ["⬜", "⬛"]}
    color_total = sum(color_pixels.values())

    # Build markdown table
    table_lines = [
        "| Color | Count | Percentage |",
        "|-------|-------|------------|"
    ]
    for emoji, count in sorted(color_pixels.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            pct = (count / color_total) * 100
            table_lines.append(f"| {emoji} | {count} | {pct:.2f}% |")
    
    table_lines.append(f"\n**Total color pixels:** {color_total}")
    
    # Output to console
    for line in table_lines:
        print(line)
    
    # Write table to file for GitHub Action to use
    with open("pixel_summary.md", "w") as f:
        f.write("\n".join(table_lines))
