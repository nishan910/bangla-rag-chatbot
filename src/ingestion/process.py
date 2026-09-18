from pathlib import Path
import re

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text):
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def process_files():
    files = sorted(RAW_DIR.glob("chapter_*.txt"))

    print(f"মোট chapter পাওয়া গেছে: {len(files)}")
    print("Processing শুরু হচ্ছে...")

    for file_path in files:

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        cleaned_text = clean_text(text)

        output_path = PROCESSED_DIR / file_path.name

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(cleaned_text)

        print(f"Processed: {output_path}")

    print()
    print("================================")
    print("Processing সম্পন্ন।")
    print(f"মোট processed chapter: {len(files)}")
    print("================================")


if __name__ == "__main__":
    process_files()