from typing import List, Dict, Any
import re

def extract_info(article: Any) -> Dict[str, str]:
    """Extract required info from a PubMedArticle XML node."""

    pubmed_id = article.PMID.text if article.PMID else "N/A"
    title = article.ArticleTitle.text if article.ArticleTitle else "N/A"

    # Get publication date
    pub_date = article.find("PubDate")
    date = "N/A"
    if pub_date:
        year = pub_date.find("Year")
        medline_date = pub_date.find("MedlineDate")
        date = year.text if year else (medline_date.text if medline_date else "N/A")

    non_academic_authors = []
    companies = []
    corresponding_email = "N/A"

    # Define keyword filters
    pharma_keywords = ["pharma", "biotech", "inc", "ltd", "corporation", "gmbh", "company", "therapeutics", "biosciences"]
    academic_keywords = ["university", "college", "institute", "hospital", "center", "faculty", "department", "school", "research foundation"]

    authors = article.find_all("Author")
    for author in authors:
        affil = author.find("AffiliationInfo")
        if affil and affil.Affiliation:
            affil_text = affil.Affiliation.text.strip()
            affil_lower = affil_text.lower()

            is_pharma = any(word in affil_lower for word in pharma_keywords)
            is_academic = any(word in affil_lower for word in academic_keywords)

            # Only include if it's clearly non-academic
            if is_pharma and not is_academic:
                name = author.LastName.text if author.LastName else "Unknown"
                non_academic_authors.append(name)
                companies.append(affil_text)

            # Extract email if available
            if "@" in affil_text and corresponding_email == "N/A":
                corresponding_email = extract_email(affil_text)

    return {
        "PubmedID": pubmed_id,
        "Title": title,
        "Publication Date": date,
        "Non-academic Author(s)": "; ".join(non_academic_authors),
        "Company Affiliation(s)": "; ".join(companies),
        "Corresponding Author Email": corresponding_email,
    }

def extract_email(text: str) -> str:
    """Extract first email address found in text."""
    match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return match.group(0) if match else "N/A"
