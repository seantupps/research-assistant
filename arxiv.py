import requests
from xml.etree import ElementTree as ET

def search_arxiv(query, start=0, max_results=10):
    url = "https://export.arxiv.org/api/query"
    params = {
        "search_query": query,
        "start": start,
        "max_results": max_results,
        "sortBy": "lastUpdatedDate",
        "sortOrder": "descending",
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch arXiv papers. Status code: {response.status_code}")

def parse_arxiv_response(response):
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "opensearch": "http://a9.com/-/spec/opensearch/1.1/"
    }
    root = ET.fromstring(response)
    total_results = int(root.find("opensearch:totalResults", ns).text)
    papers = []
    for entry in root.findall("atom:entry", ns):
        published = entry.find("atom:published", ns).text
        date = published[:10]  # Get YYYY-MM-DD
        paper = {
            "title": entry.find("atom:title", ns).text.strip(),
            "summary": entry.find("atom:summary", ns).text.strip(),
            "authors": [author.find("atom:name", ns).text for author in entry.findall("atom:author", ns)],
            "link": entry.find("atom:id", ns).text,
            "date": date,
        }
        papers.append(paper)
    return total_results, papers