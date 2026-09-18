import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import quote
import time

BASE_URL = "https://bn.wikisource.org/wiki/"

BOOK_TITLE = "কপালকুণ্ডলা (বঙ্কিমচন্দ্র চট্টোপাধ্যায়, ১৮৭০)"

VOLUMES = [
    ("প্রথম খণ্ড", [
        "প্রথম পরিচ্ছেদ",
        "দ্বিতীয় পরিচ্ছেদ",
        "তৃতীয় পরিচ্ছেদ",
        "চতুর্থ পরিচ্ছেদ",
        "পঞ্চম পরিচ্ছেদ",
        "ষষ্ঠ পরিচ্ছেদ",
        "সপ্তম পরিচ্ছেদ",
        "অষ্টম পরিচ্ছেদ",
        "নবম পরিচ্ছেদ",
    ]),
    ("দ্বিতীয় খণ্ড", [
        "প্রথম পরিচ্ছেদ",
        "দ্বিতীয় পরিচ্ছেদ",
        "তৃতীয় পরিচ্ছেদ",
        "চতুর্থ পরিচ্ছেদ",
        "পঞ্চম পরিচ্ছেদ",
        "ষষ্ঠ পরিচ্ছেদ",
    ]),
    ("তৃতীয় খণ্ড", [
        "প্রথম পরিচ্ছেদ",
        "দ্বিতীয় পরিচ্ছেদ",
        "তৃতীয় পরিচ্ছেদ",
        "চতুর্থ পরিচ্ছেদ",
        "পঞ্চম পরিচ্ছেদ",
        "ষষ্ঠ পরিচ্ছেদ",
        "সপ্তম পরিচ্ছেদ",
    ]),
    ("চতুর্থ খণ্ড", [
        "প্রথম পরিচ্ছেদ",
        "দ্বিতীয় পরিচ্ছেদ",
        "তৃতীয় পরিচ্ছেদ",
        "চতুর্থ পরিচ্ছেদ",
        "পঞ্চম পরিচ্ছেদ",
        "ষষ্ঠ পরিচ্ছেদ",
        "সপ্তম পরিচ্ছেদ",
        "অষ্টম পরিচ্ছেদ",
        "নবম পরিচ্ছেদ",
        "দশম পরিচ্ছেদ",
    ]),
]

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Educational RAG Project)"
}


def build_url(volume, chapter):
    page_title = f"{BOOK_TITLE}/{volume}/{chapter}"
    return BASE_URL + quote(page_title, safe="")


def get_soup(url):
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_text(soup):
    content = soup.select_one("#mw-content-text")

    if content is None:
        return ""

    for tag in content.select(
        "script, style, table, .mw-editsection, .navbox"
    ):
        tag.decompose()

    return content.get_text(
        "\n",
        strip=True
    )


def main():

    total_chapters = sum(
        len(chapters)
        for _, chapters in VOLUMES
    )

    print(f"মোট chapter: {total_chapters}")
    print("Wikisource থেকে chapter সংগ্রহ শুরু হচ্ছে...")

    chapter_number = 1

    for volume, chapters in VOLUMES:

        print()
        print(f"========== {volume} ==========")

        for chapter in chapters:

            url = build_url(volume, chapter)

            print()
            print(
                f"[{chapter_number}/{total_chapters}] "
                f"{volume} - {chapter}"
            )

            try:
                soup = get_soup(url)
                text = extract_text(soup)

                if not text:
                    print("ERROR: Text পাওয়া যায়নি।")
                    chapter_number += 1
                    continue

                filename = OUTPUT_DIR / f"chapter_{chapter_number:02d}.txt"

                with open(
                    filename,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write("বই: কপালকুণ্ডলা\n")
                    file.write(
                        "লেখক: বঙ্কিমচন্দ্র চট্টোপাধ্যায়\n"
                    )
                    file.write("সংস্করণ: ১৮৭০\n")
                    file.write(f"খণ্ড: {volume}\n")
                    file.write(f"পরিচ্ছেদ: {chapter}\n")
                    file.write(f"Source: {url}\n")
                    file.write("\n")
                    file.write(text)

                print(f"Saved: {filename}")

            except Exception as error:
                print(f"ERROR: {error}")

            chapter_number += 1
            time.sleep(1)

    print()
    print("================================")
    print("Crawling সম্পন্ন।")
    print(f"মোট chapter: {total_chapters}")
    print("================================")


if __name__ == "__main__":
    main()