import argparse
import csv
import json
import time
import sys
import io
from pubmed_fetcher.pubmed_api import fetch_pubmed_papers

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(
        description="Fetch research papers from PubMed.",
        epilog="Example usage:\n  python cli.py 'Machine Learning in Healthcare' --max_results 5 --file results.csv",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("query", type=str, help="Search query for PubMed (e.g., 'AI in medicine')")
    parser.add_argument("--max_results", type=int, default=10, help="Number of results to fetch (default: 10)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode to print detailed API responses")
    parser.add_argument("--file", type=str, help="Save results to a CSV file")
    
    args = parser.parse_args()

    if not args.query.strip():
        print("❌ Error: Query cannot be empty!", file=sys.stderr)
        sys.exit(1)

    print(f"🔍 Searching PubMed for: {args.query} (max {args.max_results} results)...")

    retries = 3
    delay = 2  # Initial delay in seconds

    for attempt in range(retries):
        try:
            papers = fetch_pubmed_papers(args.query, max_results=args.max_results)
            if papers:
                break
        except Exception as e:
            print(f"⚠️ Attempt {attempt+1}/{retries} failed: {e}", file=sys.stderr)
            time.sleep(delay)
            delay *= 2  # Exponential backoff
    else:
        print("❌ Error: Failed to fetch data after multiple attempts.", file=sys.stderr)
        sys.exit(1)

    if args.debug:
        print(json.dumps(papers, indent=2))

    if args.file:
        try:
            save_to_csv(args.file, papers)
            print(f"✅ Results saved to {args.file}")
        except Exception as e:
            print(f"❌ Error saving to file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        for paper in papers:
            print(f"\n📄 Title: {paper.get('Title', 'N/A')}")
            print(f"👥 Authors: {', '.join(paper.get('Authors', []))}")
            print(f"🏢 Affiliations: {', '.join(paper.get('Affiliations', []))}")
            print(f"🔬 Non-Academic: {paper.get('Non-Academic', 'Unknown')}\n")

def save_to_csv(filename, papers):
    """Saves research paper data to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["PubmedID", "Title", "Publication Date", "Authors", "Affiliations", "Corresponding Author Email", "Non-Academic"])
        writer.writeheader()
        for paper in papers:
            writer.writerow(paper)

if __name__ == "__main__":
    main()
