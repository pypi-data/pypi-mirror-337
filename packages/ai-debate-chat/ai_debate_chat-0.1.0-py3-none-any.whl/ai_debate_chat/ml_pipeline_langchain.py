import requests
import re
import logging
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import quote_plus

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Set up minimal logging for critical errors only
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Download required NLTK resources
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except Exception as e:
    logger.error(f"Error downloading NLTK resources: {e}")

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def scrape_wikipedia(query: str) -> str:
    try:
        url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        content_div = soup.find("div", {"id": "mw-content-text"})
        paragraphs = content_div.find_all("p") if content_div else soup.find_all("p")
        
        texts = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
        text = " ".join(texts)
        
        if not text:
            text = soup.get_text(separator=" ", strip=True)
        
        return text
    except Exception as e:
        logger.error("Error scraping Wikipedia: %s", e)
        return ""

def search_google(query: str, num_results=5) -> list:
    try:
        search_url = f"https://www.google.com/search?q={quote_plus(query)}&num={num_results * 2}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        skip_domains = ['youtube.com', 'pinterest.com', 'instagram.com', 'facebook.com', 'twitter.com']
        
        # Try primary selector
        for result in soup.select('div.yuRUbf > a'):
            href = result.get('href')
            if href and href.startswith('http') and 'google.com' not in href:
                domain = href.split("//")[-1].split("/")[0].replace("www.", "")
                if not any(skip in domain for skip in skip_domains):
                    links.append(href)
            if len(links) >= num_results:
                break
        
        # Try alternative selector if needed
        if len(links) < num_results:
            for result in soup.select('a'):
                href = result.get('href')
                if href and href.startswith('/url?q='):
                    actual_url = href.split('/url?q=')[1].split('&')[0]
                    if actual_url.startswith('http') and 'google.com' not in actual_url:
                        if actual_url not in links:
                            domain = actual_url.split("//")[-1].split("/")[0].replace("www.", "")
                            if not any(skip in domain for skip in skip_domains):
                                links.append(actual_url)
                if len(links) >= num_results:
                    break
        
        return links
    except Exception as e:
        logger.error(f"Error searching Google: {e}")
        return []
    
def search_duckduckgo(query: str, num_results=5) -> list:
    try:
        search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        skip_domains = ['youtube.com', 'pinterest.com', 'instagram.com', 'facebook.com', 'twitter.com']
        
        for result in soup.select('.result__a'):
            href = result.get('href')
            if not href:
                continue
            
            if href.startswith('/'):
                try:
                    parsed_url = result.get('href')
                    if parsed_url and 'uddg=' in parsed_url:
                        href = parsed_url.split('uddg=')[-1]
                except Exception:
                    continue
            
            if href.startswith('http') and not any(skip in href for skip in skip_domains):
                if href not in links:
                    links.append(href)
            
            if len(links) >= num_results:
                break
        
        return links
    except Exception as e:
        logger.error(f"Error searching DuckDuckGo: {e}")
        return []

def scrape_article(url: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove non-content elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
        
        # Try to find article content
        article_containers = soup.select('article, .article, .post, .content, .entry-content, #content, main, .main, .post-content, .page-content')
        
        if article_containers:
            paragraphs = article_containers[0].find_all('p')
        else:
            paragraphs = soup.find_all('p')
        
        texts = [p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 80]
        text = " ".join(texts)
        
        # Fallback methods if needed
        if not text or len(text) < 500:
            content_divs = [div.get_text().strip() for div in soup.find_all('div') 
                           if len(div.get_text().strip()) > 200 and len(div.get_text().strip()) < 5000]
            if content_divs:
                text = " ".join(content_divs)
        
        if not text or len(text) < 300:
            lines = [line.strip() for line in soup.get_text().splitlines() if len(line.strip()) > 40]
            text = " ".join(lines)
        
        return text
    except Exception as e:
        logger.error(f"Error scraping article from {url}: {e}")
        return ""

def preprocess_text(text: str) -> str:
    try:
        if not text:
            return ""
        
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text)
        tokens = text.split()
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]
        
        return " ".join(filtered_tokens)
    except Exception as e:
        logger.error(f"Error preprocessing text: {e}")
        return ""

def build_document(text: str, source: str) -> Document:
    return Document(page_content=text, metadata={"source": source})

def chunk_documents(documents: list) -> list:
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunked_docs = []
        for doc in documents:
            if not doc.page_content.strip():
                continue
            chunks = splitter.split_text(doc.page_content)
            for chunk in chunks:
                if chunk.strip():
                    chunked_docs.append(Document(page_content=chunk, metadata=doc.metadata))
        
        return chunked_docs
    except Exception as e:
        logger.error("Error chunking documents: %s", e)
        return []

def build_vector_store(documents: list):
    try:
        if not documents:
            return None
        
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        return FAISS.from_documents(documents, embeddings)
    except Exception as e:
        logger.error("Error building vector store: %s", e)
        return None

def prepare_debate_facts(topic: str, news_url: str = None) -> dict:
    documents = []
    sources = []
    
    # Get Wikipedia content
    wiki_text = scrape_wikipedia(topic)
    if wiki_text:
        preprocessed_wiki = preprocess_text(wiki_text)
        if preprocessed_wiki:
            documents.append(build_document(preprocessed_wiki, source="Wikipedia"))
            sources.append("Wikipedia")
    
    # Get additional sources
    num_results = 5 if not documents else 3
    search_urls = search_google(topic, num_results=num_results) or search_duckduckgo(topic, num_results=num_results)
    
    # Try alternative queries if needed
    if not search_urls:
        alternative_queries = [
            f"{topic} comparison",
            f"{topic} information",
            f"{topic} explained",
            f"{topic} differences",
            f"{topic} guide"
        ]
        
        for alt_query in alternative_queries:
            search_urls = search_google(alt_query, num_results=3) or search_duckduckgo(alt_query, num_results=3)
            if search_urls:
                break
    
    # Process search results
    if search_urls:
        for i, url in enumerate(search_urls):
            if i > 0:
                time.sleep(1 + random.random())
            
            article_text = scrape_article(url)
            if article_text:
                preprocessed_article = preprocess_text(article_text)
                if preprocessed_article:
                    domain = url.split("//")[-1].split("/")[0].replace("www.", "")
                    documents.append(build_document(preprocessed_article, source=f"Web: {domain}"))
                    sources.append(domain)
    
    # Process optional news article
    if news_url:
        news_text = scrape_article(news_url)
        if news_text:
            preprocessed_news = preprocess_text(news_text)
            if preprocessed_news:
                domain = news_url.split("//")[-1].split("/")[0].replace("www.", "")
                documents.append(build_document(preprocessed_news, source=f"News: {domain}"))
                sources.append(domain)
    
    # Create placeholder if no documents found
    if not documents:
        minimal_content = f"Information about {topic}. This is a placeholder as no detailed information could be found."
        documents.append(build_document(minimal_content, source="Placeholder"))
        sources.append("Placeholder")
    
    # Process documents and build vector store
    chunked_docs = chunk_documents(documents)
    vector_store = build_vector_store(chunked_docs) if chunked_docs else None
    
    return {"topic": topic, "vector_store": vector_store, "documents": chunked_docs, "sources": sources}

if __name__ == "__main__":
    topic = "Artificial intelligence"
    debate_facts = prepare_debate_facts(topic)
    
    if debate_facts["vector_store"]:
        print(f"Vector store created for topic: {debate_facts['topic']}")
        print(f"Documents: {len(debate_facts['documents'])}")
        print(f"Sources: {', '.join(debate_facts['sources'])}")
    else:
        print("Failed to build vector store.")