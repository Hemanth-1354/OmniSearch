
# OmniSearch

OmniSearch is a search engine that aggregates results from various sources based on user-provided search terms. It enables users to find relevant content, including YouTube videos, articles, academic papers, and blog posts.

## How It Works
- **User Input**: Users enter a search term in the search bar.
- **API Calls**:
  - Fetches results from the **YouTube Data API** for videos.
  - Retrieves articles and blog posts from **Google Custom Search API** or **Bing Search API**.
  - Gathers academic papers from **Google Scholar API** or **PubMed API**.
- **Result Aggregation**: Compiles and ranks results based on relevance, views, and likes.
- **Display Results**: Presents results in a user-friendly interface with filtering options.

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Hemanth-1354/OmniSearch.git
   ```

2. **Navigate to the Project Directory**:
   
   cd OmniSearch


3. **Install Dependencies**:
   For Python projects:
   pip install -r requirements.txt

4. **Set Up Environment Variables**:
   - Create a `.env` file and add your API keys:
     
     YOUTUBE_API_KEY=your_youtube_api_key
     GOOGLE_API_KEY=your_google_api_key
     GOOGLE_SCHOLAR_API_KEY=your_google_scholar_api_key
     

5. **Run the Application**:
   - For Flask:
     
     python app.py
     
   

6. **Access the Application**:
   - Open a web browser and go to `http://127.0.0.1:5000` .
