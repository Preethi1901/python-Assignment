import os
import sys
import argparse
import pandas as pd
from new_project.get_links import search_pubmed, fetch_pubmed_articles
from new_project.filter import extract_info

#from new_project.get_links import search_pubmed, fetch_pubmed_articles, extract_info
from typing import Optional


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch PubMed papers with pharma/biotech affiliations."
    )
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Print debug information"
    )
    parser.add_argument(
        "-f", "--file", type=str, help="CSV output file name (default: print to console)"
    )

    args = parser.parse_args()
    query: str = args.query
    debug: bool = args.debug
    filename: Optional[str] = args.file

    if debug:
        print(f"[DEBUG] Searching for: {query}")

    try:
        pmids = search_pubmed(query, max_results=50)
        if not pmids:
            print("❌ No articles found.")
            return

        articles = fetch_pubmed_articles(pmids)

        if not isinstance(articles, list):
            articles = [articles]

        records = []
        for article in articles:
            info = extract_info(article)
            if info["Non-academic Author(s)"]:
                records.append(info)

        if not records:
            print("❌ No pharma/biotech affiliations found.")
            return

        df = pd.DataFrame(records)

        if filename:
            os.makedirs("output", exist_ok=True)
            full_path = os.path.join("output", filename)
            df.to_csv(full_path, index=False)
            print(f"✅ Results saved to '{full_path}'")
        else:
            print(df.to_string(index=False))

    except Exception as e:
        print(f"❌ Error: {e}")
        if debug:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
