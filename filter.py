from typing import List, Dict, Any
def extract_info(article: Any) -> Dict[str, str]:
    """Extract required info from a PubMedArticle XML node."""
    pubmed_id = article.PMID.text if article.PMID else "N/A"
    title = article.ArticleTitle.text if article.ArticleTitle else "N/A"
    pub_date = article.find("PubDate")
    date = "N/A"
    if pub_date:
        year = pub_date.find("Year")
        medline_date = pub_date.find("MedlineDate")
        date = year.text if year else (medline_date.text if medline_date else "N/A")

    non_academic_authors = []
    companies = []
    corresponding_email = "N/A"

    authors = article.find_all("Author")
    for author in authors:
        affil = author.find("AffiliationInfo")
        if affil:
            affil_text = affil.Affiliation.text.lower()
            if any(word in affil_text for word in ["pharma", "biotech", "inc", "ltd", "corporation", "gmbh", "company"]):
                non_academic_authors.append(author.LastName.text if author.LastName else "Unknown")
                companies.append(affil.Affiliation.text)

            if "@" in affil.Affiliation.text and corresponding_email == "N/A":
                corresponding_email = extract_email(affil.Affiliation.text)

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
    import re
    match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return match.group(0) if match else "N/A"
