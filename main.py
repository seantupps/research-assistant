from arxiv import search_arxiv, parse_arxiv_response
from pdf import download_pdf, extract_text_from_pdf
from ai import summarize_text_with_gpt

def process_and_summarize_paper(pdf_url):
    print(f"\nDownloading PDF from {pdf_url}...")
    pdf_path = download_pdf(pdf_url, "temp_paper.pdf")
    
    print("Extracting text from PDF...")
    pdf_text = extract_text_from_pdf(pdf_path)
    
    print("Generating summary...")
    summary = summarize_text_with_gpt(pdf_text)
    
    # Clean up the temporary PDF file
    import os
    os.remove(pdf_path)
    
    return summary

def main():
    print("Welcome to the Research Assistant!")
    query = input("Enter your research topic or keywords: ")
    
    print("\nFetching papers from arXiv...")
    arxiv_response = search_arxiv(query)
    papers = parse_arxiv_response(arxiv_response)
    
    print(f"\nFound {len(papers)} papers. Here are the details:\n")
    for i, paper in enumerate(papers):
        print(f"Paper {i + 1}: {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"Link: {paper['link']}")
        
        pdf_url = paper["link"].replace("/abs/", "/pdf/") + ".pdf"
        summary = process_and_summarize_paper(pdf_url)
        print("\nSummary:")
        print(summary)
        print("\n" + "-" * 80 + "\n")

if __name__ == "__main__":
    main()