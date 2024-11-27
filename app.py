from flask import Flask, render_template, request, jsonify
from arxiv import search_arxiv, parse_arxiv_response
from pdf import download_pdf, extract_text_from_pdf
from ai import summarize_text_with_gpt
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query')
    start = data.get('start', 0)
    max_results = data.get('max_results', 10)
    arxiv_response = search_arxiv(query, start=start, max_results=max_results)
    total_results, papers = parse_arxiv_response(arxiv_response)
    return jsonify({'total_results': total_results, 'papers': papers})

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    pdf_url = data.get('pdf_url')
    try:
        pdf_path = download_pdf(pdf_url, "temp_paper.pdf")
        pdf_text = extract_text_from_pdf(pdf_path)
        
        # Limit text length to avoid exceeding token limits (adjust as needed)
        max_length = 4000  # characters
        pdf_text = pdf_text[:max_length]
        
        summary = summarize_text_with_gpt(pdf_text)
        
        # Clean up the temporary PDF file
        os.remove(pdf_path)
        
        return jsonify({"summary": summary})
    except Exception as e:
        print(f"Error in /summarize: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)