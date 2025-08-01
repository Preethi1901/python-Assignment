--PubMed Pharma Paper Fetcher--

This tool allows you to search PubMed using any query and extract information about research papers with authors affiliated with pharmaceutical or biotech companies.


#Set up Instructions
1. git clone (github repository link)
   
    cd python-Assignment
________________________________________________________
#Install Dependencies

Run command - poetry install
This installs:
-requests
-beautifulsoup4
-pandas
___________________________________________________________
Run this command
poetry run get-papers-list "your query here"

Options:
-d or --debug: debug output
-f or --file: Save output to a CSV file in the output/ directory
___________________________________________________________

Example query-  poetry run get-papers-list "cancer immunotherapy" -f cancer_papers.csv

_____________________________________________________________
Tools / Libraries used
1. Requests -for HTTP requests	(https://docs.python-requests.org/)

2. Pandas -for CSV/Datafreame handling  (	https://pandas.pydata.org/)

3.Poetry - Dependency management & Packaging (	https://python-poetry.org/)

4.Entrez API-  pubMed API for  biomedical literature

5.BeautifulSoup4- for XML Parsing




