import requests
from typing import List, Dict, Any
from bs4 import BeautifulSoup

EntrezBaseURL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def search_pubmed(query: str, max_results: int = 50) -> List[str]:
    """Search PubMed for a given query and return a list of PMIDs."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    response = requests.get(f"{EntrezBaseURL}/esearch.fcgi", params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])


def fetch_pubmed_articles(pmids: List[str]) -> List[Dict[str, Any]]:
    """Fetch detailed information for a list of PubMed IDs."""
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }
    response = requests.get(f"{EntrezBaseURL}/efetch.fcgi", params=params)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "xml")
    return soup.find_all("PubmedArticle")



