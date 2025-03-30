import requests
import xml.etree.ElementTree as ET
import re
import time
from urllib.parse import quote

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def fetch_pubmed_papers(query, max_results=10, retries=3, delay=2):
    """
    Fetches PubMed papers based on a search query.
    """
    pubmed_ids = get_pubmed_ids(query, max_results, retries, delay)
    if not pubmed_ids:
        return []
    
    return fetch_paper_details(pubmed_ids, retries, delay)

def get_pubmed_ids(query, max_results, retries, delay):
    """
    Retrieves PubMed IDs for a given search query.
    Implements retry logic in case of request failures.
    """
    encoded_query = quote(query)  # Encode special characters in query
    search_url = f"{BASE_URL}/esearch.fcgi?db=pubmed&term={encoded_query}&retmax={max_results}&retmode=xml"

    for attempt in range(retries):
        try:
            response = requests.get(search_url, timeout=5)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            return [id_elem.text for id_elem in root.findall(".//Id")]
        except (requests.RequestException, ET.ParseError) as e:
            print(f"Error fetching PubMed IDs (Attempt {attempt+1}/{retries}): {e}")
            time.sleep(delay)

    return []

def fetch_paper_details(pubmed_ids, retries, delay):
    """
    Fetches detailed paper information using PubMed IDs in batches (max 200 per request).
    """
    batch_size = 200  # PubMed API limit
    all_papers = []
    
    for i in range(0, len(pubmed_ids), batch_size):
        batch_ids = pubmed_ids[i:i+batch_size]
        details_url = f"{BASE_URL}/efetch.fcgi?db=pubmed&id={','.join(batch_ids)}&retmode=xml"

        for attempt in range(retries):
            try:
                response = requests.get(details_url, timeout=5)
                response.raise_for_status()
                all_papers.extend(parse_pubmed_response(response.content))
                break  # Success, no need to retry
            except (requests.RequestException, ET.ParseError) as e:
                print(f"Error fetching paper details (Attempt {attempt+1}/{retries}): {e}")
                time.sleep(delay)

    return all_papers

def parse_pubmed_response(xml_data):
    """
    Parses PubMed XML response and extracts relevant details.
    """
    root = ET.fromstring(xml_data)
    papers = []
    
    for article in root.findall(".//PubmedArticle"):  
        pmid = article.find(".//PMID").text if article.find(".//PMID") is not None else "N/A"
        title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "No Title"
        pub_date = article.find(".//PubDate/Year")
        pub_date = pub_date.text if pub_date is not None else "Unknown Date"
        
        authors = []
        affiliations = []
        corresponding_email = ""
        
        for author in article.findall(".//Author"):
            lastname = author.find("LastName")
            firstname = author.find("ForeName")
            name = f"{firstname.text} {lastname.text}" if firstname is not None and lastname is not None else "Unknown"
            
            aff = author.find(".//Affiliation")
            affiliation = aff.text if aff is not None else "Unknown"
            
            authors.append(name)
            affiliations.append(affiliation)
            
            # Extract email (heuristically checking for @ symbol)
            if "@" in affiliation:
                email_matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', affiliation)
                if email_matches:
                    corresponding_email = email_matches[0]
                    
        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Authors": authors,
            "Affiliations": affiliations,
            "Corresponding Author Email": corresponding_email,
            "Non-Academic": detect_non_academic(affiliations)
        })
    
    return papers

def detect_non_academic(affiliations):
    """
    Detects whether an author is company-affiliated based on keywords in affiliations.
    """
    company_keywords = [
        "Inc", "Ltd", "LLC", "Corporation", "Biotech", "Pharmaceuticals",
        "Technologies", "Solutions", "Healthcare", "Company", "Research Institute"
    ]
    
    return any(any(keyword in aff for keyword in company_keywords) for aff in affiliations)

# Example Usage
if __name__ == "__main__":
    results = fetch_pubmed_papers("Machine Learning in Healthcare", max_results=5)
    for paper in results:
        print(paper)
