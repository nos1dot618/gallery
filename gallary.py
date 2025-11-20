import os

INPUT_FILE = "images.txt"
OUTPUT_FILE = "index.html"
IMAGE_DIR = "images"

HTML_TEMPLATE_START = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <title>Nosferatu's Gallary</title>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #1d2021;
            padding: 20px;
            font-family: system-ui, sans-serif;
            display: flex;
            justify-content: center;
        }

        .frame {
            max-width: 1200px;
            width: 100%;
            position: relative;
        }

        .frame::after {
            content: "";
            pointer-events: none;
            position: absolute;
            inset: 0;
            background: repeating-linear-gradient(
                to bottom,
                rgba(0,0,0,0.1) 0px,
                rgba(0,0,0,0.1) 1px,
                transparent 2px,
                transparent 4px
            );
            mix-blend-mode: multiply;
            opacity: 0.17;
        }

        .gallery {
            column-count: 4;
            column-gap: 12px;
        }

        .gallery figure {
            position: relative;
            margin: 0 0 12px 0;
            break-inside: avoid;
        }

        .gallery img {
            width: 100%;
            display: block;
            border: #ebdbb2 solid 2px;
            loading: lazy;
            image-rendering: crisp-edges;
            transition: opacity 0.15s ease-out, transform 0.15s ease-out;
        }

        .gallery img:hover {
            opacity: 0.85;
            transform: scale(1.02);
            box-shadow: 0 0 8px #ebdbb299;
        }

        .gallery figcaption {
            position: absolute;
            left: 4px;
            bottom: 4px;
            background: rgba(29, 32, 33, 0.85);
            color: #ebdbb2;
            padding: 3px 6px;
            font-size: 0.75rem;
            border: 1px solid #ebdbb2;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.15s ease-in-out;
            font-family: monospace;
        }

        figure:hover figcaption {
            opacity: 1;
        }

        @media (max-width: 1000px) {
            .gallery { column-count: 3; }
        }

        @media (max-width: 700px) {
            .gallery { column-count: 2; }
        }

        @media (max-width: 480px) {
            .gallery { column-count: 1; }
        }
    </style>
</head>

<body>
<div class="frame">
    <div class="gallery">
"""

HTML_TEMPLATE_END = """
    </div>
</div>
</body>
</html>
"""


def parse_kv_file(path):
    pairs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Skip comments or blank lines
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                print(f"WARN: Invalid line (ignored): {line}.")
                continue
            file, alt = line.split("=", 1)
            pairs.append((file.strip(), alt.strip()))
    return pairs


def generate_html(image_pairs):
    html = [HTML_TEMPLATE_START]
    for filename, alt_text in image_pairs:
        img_path = f"{IMAGE_DIR}/{filename}"
        html.append(f"""
        <figure>
            <img src="{img_path}" alt="{alt_text}">
            <figcaption>{alt_text}</figcaption>
        </figure>
        """)
    html.append(HTML_TEMPLATE_END)
    return "".join(html)


def main():
    pairs = parse_kv_file(INPUT_FILE)
    html = generate_html(pairs)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"INFO: HTML generated successfully to {OUTPUT_FILE}.")


if __name__ == "__main__":
    main()
