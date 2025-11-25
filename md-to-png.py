import re
from PIL import Image

# --------------------------------------------
# CONFIGURATION
# --------------------------------------------

# Map emojis to colors (RGB)
COLOR_MAP = {
    "🟥": (255, 0, 0),
    "🟧": (255, 128, 0),
    "🟨": (255, 255, 0),
    "🟩": (0, 200, 0),
    "🟦": (0, 100, 255),
    "🟪": (150, 0, 200),
    "⬛": (0, 0, 0),
    "⬜": (255, 255, 255),
}

# Size of each emoji-pixel in output PNG (scale factor)
PIXEL_SIZE = 10   # e.g., each "pixel" becomes 20×20 px


# --------------------------------------------
# FUNCTION TO PARSE MARKDOWN TABLE
# --------------------------------------------

def parse_markdown_pixel_table(md_path):
    """
    Extracts rows of emojis from a markdown table file.
    Returns a 2D list of emojis.
    """
    rows = []
    emoji_pattern = re.compile("|".join(map(re.escape, COLOR_MAP.keys())))

    with open(md_path, "r", encoding="utf-8") as f:
        for line in f:
            if "|" not in line:
                continue  # skip non-table lines

            # Extract emojis in the row
            cells = emoji_pattern.findall(line)
            if cells:
                rows.append(cells)

    return rows


# --------------------------------------------
# FUNCTION TO RENDER PNG
# --------------------------------------------

def render_png(emoji_grid, output_path):
    height = len(emoji_grid)
    width = len(emoji_grid[0])

    img = Image.new("RGB", (width * PIXEL_SIZE, height * PIXEL_SIZE))

    for y, row in enumerate(emoji_grid):
        for x, emoji in enumerate(row):
            color = COLOR_MAP.get(emoji, (255, 255, 255))  # default white

            for dy in range(PIXEL_SIZE):
                for dx in range(PIXEL_SIZE):
                    img.putpixel(
                        (x * PIXEL_SIZE + dx, y * PIXEL_SIZE + dy),
                        color
                    )

    img.save(output_path)
    print(f"Saved PNG to {output_path}")


# --------------------------------------------
# MAIN
# --------------------------------------------

if __name__ == "__main__":
    md_file = "logo.md"        # ← input markdown table
    output_png = "preview.png?"    # ← output PNG file

    grid = parse_markdown_pixel_table(md_file)
    render_png(grid, output_png)