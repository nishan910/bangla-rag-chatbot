from pathlib import Path
import json

PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DIR / "chunks_500.json"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def split_text(text):
    words = text.split()

    chunks = []
    start = 0

    while start < len(words):
        end = start + CHUNK_SIZE
        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def get_metadata(text):
    metadata = {
        "book": "কপালকুণ্ডলা",
        "author": "বঙ্কিমচন্দ্র চট্টোপাধ্যায়",
        "edition": "১৮৭০",
        "volume": "",
        "chapter": "",
        "source": ""
    }

    for line in text.splitlines():
        line = line.strip()

        if line.startswith("খণ্ড:"):
            metadata["volume"] = line[5:].strip()

        elif line.startswith("পরিচ্ছেদ:"):
            metadata["chapter"] = line[9:].strip()

        elif line.startswith("Source:"):
            metadata["source"] = line[7:].strip()

    return metadata


def main():

    files = sorted(
        PROCESSED_DIR.glob("chapter_*.txt")
    )

    print("মোট chapter পাওয়া গেছে:", len(files))
    print("500-word chunking শুরু হচ্ছে...")

    all_chunks = []
    chunk_id = 1

    for file_path in files:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:
            text = file.read()

        metadata = get_metadata(text)

        content_lines = []

        for line in text.splitlines():

            if line.startswith("বই:"):
                continue

            if line.startswith("লেখক:"):
                continue

            if line.startswith("সংস্করণ:"):
                continue

            if line.startswith("খণ্ড:"):
                continue

            if line.startswith("পরিচ্ছেদ:"):
                continue

            if line.startswith("Source:"):
                continue

            content_lines.append(line)

        content = "\n".join(content_lines)

        chunks = split_text(content)

        for chunk in chunks:

            item = {
                "chunk_id": chunk_id,
                "text": chunk,
                "metadata": {
                    "book": metadata["book"],
                    "author": metadata["author"],
                    "edition": metadata["edition"],
                    "volume": metadata["volume"],
                    "chapter": metadata["chapter"],
                    "source": metadata["source"],
                    "file": file_path.name
                }
            }

            all_chunks.append(item)
            chunk_id += 1

        print(
            file_path.name,
            "->",
            len(chunks),
            "chunks"
        )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_chunks,
            file,
            ensure_ascii=False,
            indent=2
        )

    print()
    print("================================")
    print("500-word Chunking সম্পন্ন।")
    print("মোট chunks:", len(all_chunks))
    print("Saved:", OUTPUT_FILE)
    print("================================")


if __name__ == "__main__":
    main()
