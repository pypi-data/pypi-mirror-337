# search.py
import requests
import json
from .simplesearch import SimpleSearch
from . import importdocs
from .functions import getembedding

def perform_search(query, model, api_key, top_k=2):
    """
    For queries starting with '/', this pipeline:
      1. Uses the user query directly to obtain search context,
      2. Uses the raw context (without summarization) and stores it in the FAISS RAG index,
      3. Constructs a final prompt that includes both the original query and the context,
      4. Sends the final prompt to Ollama for generation with a streaming response.
      
    For queries without '/', it falls back to the standard RAG pipeline with streaming.
    """
    ollama_url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}

    if query.startswith('/'):
        searcher = SimpleSearch(
            cloud_service_url="https://qupuadlqdicescsdkejt.supabase.co/functions/v1/ratelimit",
            ollama_url="http://localhost:11434",
            current_model=model,
            api_key=api_key
        )
        supporting_info = searcher.process_query(query)
        user_query = query[1:].strip()
        final_prompt = (
            f'This is the user query: "{user_query}" and here is some supporting information: "{supporting_info}". '
            f'You need to answer the user query with the help of the supporting information.'
        )
        messages = [{"role": "user", "content": final_prompt}]
    else:
        # Standard RAG pipeline for queries without '/'.
        query_embed = getembedding(query)
        if query_embed.ndim == 1:
            query_embed = query_embed.reshape(1, -1)
        indices, distances = importdocs.search_index(query, model, top_k=2)
        docs = [importdocs.doc_store[i] for i in indices if i in importdocs.doc_store]
        if docs:
            relateddocs = "\n\n".join(docs)
            prompt = (f'This is the user query: "{query}" - and here is some supporting information: "{relateddocs}"'
            f'You need to answer the user query with the help of the supporting information.')
        else:
            prompt = query
        messages = [{"role": "user", "content": prompt}]

    payload = {
        "model": model,
        "messages": messages,
        "stream": True
    }

    try:
        # Using stream=True to enable streaming of the final response.
        with requests.post(ollama_url, json=payload, headers=headers, stream=True) as response:
            response.raise_for_status()
            full_response = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    content = chunk.get("message", {}).get("content", "")
                    print(content, end="", flush=True)
                    full_response += content
            print()  # Ensure a newline after streaming is complete.
            return full_response
    except Exception as e:
        print(f"Error in generation: {e}")
        return ""
