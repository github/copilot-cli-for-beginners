#!/usr/bin/env python3
"""
Generate chapter header images with baked-in text.
Usage: python .github/scripts/generate-chapter-headers.py
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# Configuration
CHAPTERS = {
    "00-quick-start": "Chapter 00: Quick Start",
    "01-setup-and-first-steps": "Chapter 01: First Steps",
    "02-context-conversations": "Chapter 02: Context and Conversations",
    "03-development-workflows": "Chapter 03: Development Workflows",
    "04-agents-custom-instructions": "Chapter 04: Agents and Custom Instructions",
    "05-skills": "Chapter 05: Skills System",
    "06-mcp-servers": "Chapter 06: MCP Servers",
    "07-putting-it-together": "Chapter 07: Putting It All Together",
}

# Get project root (parent of scripts folder)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
BACKGROUND_IMAGE = os.path.join(PROJECT_ROOT, "images", "chapter-header-bg.png")

# Font settings - 25% larger than original 36px
FONT_SIZE = 45
RIGHT_PADDING = 30


def find_font():
    """Find a suitable system font."""
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
        "C:\\Windows\\Fonts\\arial.ttf",  # Windows
    ]

    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, FONT_SIZE)
            except Exception:
                continue

    print("Warning: Using default font (may look different)")
    return ImageFont.load_default()


def generate_header(chapter_folder, title, font):
    """Generate a header image for a chapter."""
    # Load background
    bg = Image.open(BACKGROUND_IMAGE)
    bg = bg.convert("RGB")
    draw = ImageDraw.Draw(bg)

    width, height = bg.size

    # Minimum x position to avoid overlapping the copilot logo (logo is ~320px wide)
    MIN_X_POSITION = 350

    # Calculate text width for full title
    bbox = draw.textbbox((0, 0), title, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = width - text_width - RIGHT_PADDING

    # Check if text would overlap with logo
    if x < MIN_X_POSITION:
        # Need to wrap - split at the colon
        if ": " in title:
            line1, line2 = title.split(": ", 1)
            line1 = line1 + ":"
        else:
            # Fallback: split at middle space
            words = title.split()
            mid = len(words) // 2
            line1 = " ".join(words[:mid])
            line2 = " ".join(words[mid:])

        # Calculate dimensions for both lines
        bbox1 = draw.textbbox((0, 0), line1, font=font)
        bbox2 = draw.textbbox((0, 0), line2, font=font)

        line1_width = bbox1[2] - bbox1[0]
        line2_width = bbox2[2] - bbox2[0]
        line_height = bbox1[3] - bbox1[1]

        # Line spacing
        line_gap = 5
        total_height = line_height * 2 + line_gap

        # Right-align both lines
        x1 = width - line1_width - RIGHT_PADDING
        x2 = width - line2_width - RIGHT_PADDING

        # Vertically center the two lines
        y1 = (height - total_height) // 2
        y2 = y1 + line_height + line_gap

        # Draw both lines
        draw.text((x1, y1), line1, fill=(255, 255, 255), font=font)
        draw.text((x2, y2), line2, fill=(255, 255, 255), font=font)
    else:
        # Single line - fits fine
        y = (height - text_height) // 2
        draw.text((x, y), title, fill=(255, 255, 255), font=font)

    # Save to chapter's images folder
    output_dir = os.path.join(PROJECT_ROOT, chapter_folder, "images")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "chapter-header.png")
    bg.save(output_path)

    return output_path


def main():
    print("Generating chapter headers...")
    print(f"Background: {BACKGROUND_IMAGE}")
    print(f"Font size: {FONT_SIZE}px")
    print()

    if not os.path.exists(BACKGROUND_IMAGE):
        print(f"Error: Background image not found: {BACKGROUND_IMAGE}")
        sys.exit(1)

    font = find_font()

    for chapter_folder, title in CHAPTERS.items():
        chapter_path = os.path.join(PROJECT_ROOT, chapter_folder)
        if not os.path.exists(chapter_path):
            print(f"  Skipping {chapter_folder} (folder not found)")
            continue

        output_path = generate_header(chapter_folder, title, font)
        print(f"  {title}")
        print(f"    -> {os.path.relpath(output_path, PROJECT_ROOT)}")

    print()
    print("Done! Headers generated for all chapters.")


if __name__ == "__main__":
    main()
