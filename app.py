from flask import Flask, render_template, request, jsonify
from googleapiclient.discovery import build
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)


def configure():
    load_dotenv()


configure()

youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    content_type = request.form.get('content_type', '')  
    results = aggregate_results(query, content_type)
    return jsonify(results)

def aggregate_results(query, content_type):
    results = {}
    if content_type == 'youtube':
        results['youtube'] = youtube_search_with_ranking(query)
    elif content_type == 'articles':
        results['articles'] = article_search_with_ranking(query)
    elif content_type == 'academic_papers':
        results['academic_papers'] = academic_paper_search(query)
    elif content_type == 'blogs':
        results['blogs'] = blog_search_with_ranking(query)
    else:
        
        results = {
            'youtube': youtube_search_with_ranking(query),
            'articles': article_search_with_ranking(query),
            'academic_papers': academic_paper_search(query),
            'blogs': blog_search_with_ranking(query)
        }
    return results

def youtube_search_with_ranking(query):
    
    search_response = youtube.search().list(q=query, part='id', type='video', maxResults=10).execute()
    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
    video_response = youtube.videos().list(id=','.join(video_ids), part='snippet,statistics').execute()

    videos = []
    for item in video_response.get('items', []):
        stats = item.get('statistics', {})
        video = {
            'title': item['snippet']['title'],
            'url': f"https://www.youtube.com/watch?v={item['id']}",
            'description': item['snippet']['description'],
            'viewCount': int(stats.get('viewCount', 0)),
            'likeCount': int(stats.get('likeCount', 0))
        }
        videos.append(video)

    
    videos.sort(key=lambda x: (0.7 * x['viewCount'] + 0.3 * x['likeCount']), reverse=True)
    return videos

def article_search_with_ranking(query):
    
    google_cse_url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={os.getenv('GOOGLE_CSE_ID')}&key={os.getenv('GOOGLE_CSE_API_KEY')}"
    response = requests.get(google_cse_url)
    search_results = response.json().get('items', [])

    articles = []
    for item in search_results:
        article = {
            'title': item.get('title'),
            'url': item.get('link'),
            'snippet': item.get('snippet'),
            'score': item.get('score', 0)  
        }
        articles.append(article)

    
    articles.sort(key=lambda x: x['score'], reverse=True)
    return articles

def academic_paper_search(query):

    pubmed_url = f"{os.getenv('PUBMED_API_BASE_URL')}?db=pubmed&term={query}&retmode=json&retmax=10"
    response = requests.get(pubmed_url)
    pubmed_data = response.json()

    paper_ids = pubmed_data.get('esearchresult', {}).get('idlist', [])
    papers = []

    if paper_ids:
        
        summary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={','.join(paper_ids)}&retmode=json"
        summary_response = requests.get(summary_url)
        summary_data = summary_response.json().get('result', {})

        for id_ in paper_ids:
            paper_info = summary_data.get(id_, {})
            paper = {
                'title': paper_info.get('title', 'No title available'),
                'url': f"https://pubmed.ncbi.nlm.nih.gov/{id_}/",
                'description': paper_info.get('source', 'No description available')
            }
            papers.append(paper)

    return papers

def blog_search_with_ranking(query):
    google_cse_url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={os.getenv('GOOGLE_CSE_ID')}&key={os.getenv('GOOGLE_CSE_API_KEY')}&siteSearch=medium.com"
    response = requests.get(google_cse_url)
    search_results = response.json().get('items', [])

    blogs = []
    for item in search_results:
        blog = {
            'title': item.get('title'),
            'url': item.get('link'),
            'snippet': item.get('snippet'),
            'score': item.get('score', 0)  
        }
        blogs.append(blog)

    blogs.sort(key=lambda x: x['score'], reverse=True)
    return blogs

if __name__ == '__main__':
    app.run(debug=True)
