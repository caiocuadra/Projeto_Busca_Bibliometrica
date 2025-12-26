import requests
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import re
import nltk
import time
from collections import Counter
import os
from flask import Flask, request, jsonify

# Garante que os recursos do NLTK estão baixados
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# --- INÍCIO DAS FUNÇÕES AUXILIARES (IGUAL AO ANTERIOR) ---
def preprocess(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'[^\w\s]', '', text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

def search_semantic_scholar(query, total_results=100, step=100, max_retries=5):
    all_articles = []
    # Reduzido para ser mais rápido na resposta da API
    for offset in range(0, total_results, step):
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&offset={offset}&limit={step}&fields=title,abstract,authors,year,url,venue"
        print(f"Tentando acessar URL: {url}")
        
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json().get('data', [])
                    if not data: return all_articles
                    all_articles.extend(data)
                    if len(data) < step: return all_articles
                    break
                elif response.status_code == 429:
                    retries += 1
                    time.sleep(2 ** retries)
                else:
                    return all_articles
            except Exception as e:
                print(f"Erro: {e}")
                retries += 1
                time.sleep(1)
        time.sleep(1)
    return all_articles

def extract_keywords(articles, top_n=10):
    all_text = " ".join([str(article.get('title', '')) + " " + str(article.get('abstract', '')) for article in articles])
    all_text = preprocess(all_text)
    tokens = all_text.split()
    filtered_tokens = [word for word in tokens if word not in ENGLISH_STOP_WORDS]
    word_counts = Counter(filtered_tokens)
    return [word for word, count in word_counts.most_common(top_n)]

def realizar_busca_bibliometrica(query, limite_correspondencia=10.0):
    print(f"--- Iniciando busca por: '{query}' ---")
    
    # Busca Inicial (Limite reduzido para performance da API)
    articles = search_semantic_scholar(query, total_results=40)

    refined_query = query
    if articles:
        keywords = extract_keywords(articles)
        refined_query = f"{query} {' '.join(keywords)}"
        
        # Busca refinada
        total_articles_found = len(articles)
        refined_articles = search_semantic_scholar(refined_query, total_results=min(total_articles_found, 40))
    else:
        return []

    # TF-IDF e Similaridade
    results = []
    vectorizer = TfidfVectorizer()
    processed_query = preprocess(refined_query)
    
    if refined_articles:
        corpus = []
        for article in refined_articles:
            title = article.get('title', '') or ''
            abstract = article.get('abstract', '') or ''
            corpus.append(preprocess(title + ' ' + abstract))
        corpus.append(processed_query)
        
        try:
            vectors = vectorizer.fit_transform(corpus)
            query_vector = vectors[-1]
            
            for i, article in enumerate(refined_articles):
                similarity = cosine_similarity(vectors[i], query_vector)[0][0]
                correspondencia = similarity * 100
                
                if correspondencia >= limite_correspondencia:
                    results.append({
                        'titulo': article.get('title', 'N/A'),
                        'autores': ', '.join([author.get('name', 'N/A') for author in article.get('authors', [])]),
                        'ano': article.get('year', 'N/A'),
                        'doi': article.get('doi', 'N/A'),
                        'link': article.get('url') or f"https://www.semanticscholar.org/paper/{article.get('paperId', '')}",
                        'relevancia': round(correspondencia, 2),
                        'abstract': article.get('abstract', 'Resumo não disponível.')
                    })
        except ValueError:
            pass

    return sorted(results, key=lambda x: x['relevancia'], reverse=True)
# --- FIM DAS FUNÇÕES AUXILIARES ---

# --- CONFIGURAÇÃO DO SERVIDOR FLASK ---
app = Flask(__name__)

@app.route('/buscar', methods=['POST'])
def buscar():
    """
    Endpoint que recebe JSON: {"query": "termo", "limit": 10}
    """
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({"erro": "Parâmetro 'query' é obrigatório"}), 400
    
    termo = data['query']
    limite = float(data.get('limit', 10.0))
    
    try:
        resultados = realizar_busca_bibliometrica(termo, limite)
        return jsonify({
            "status": "sucesso",
            "total_encontrados": len(resultados),
            "dados": resultados
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "worker online"}), 200

if __name__ == "__main__":
    # O host='0.0.0.0' permite que o Docker exponha a porta para outros containers
    app.run(host='0.0.0.0', port=5000)