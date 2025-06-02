import os
import numpy as np
from dotenv import load_dotenv
from pypdf import PdfReader
from google.genai import types
from google import genai

# Ladda API nyckeln för Google gemini AI 

client = genai.Client(api_key="AIzaSyALzrmgZlrjxoeO-XOxemrT_0X8vbBju7U")

# Använda RAG-Teknik för att hämta infromation från text-data genom ett PDF-dokument
def extract_text(pdf_path):
    # Läser in text från PDF-filen
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

#Dela upp texten i mindre delar med "Chunkning". Nedan skapas chunks som innehåller 1000 tecken med ett överlapp på 200 tecken.
def chunk_text(text, n =500, overlap=100):
    chunks = []
    for i in range(0, len(text), n - overlap):
        chunks.append(text[i:i + n])
    print(f"Antal chunks: {len(chunks)}.")
    return chunks

# Skapa embedding, numerisk representation av texten, för att en dator ska kunna förstå betydelse av texten.
def create_embeddings(texts):
    """
    Skapar embeddings för en lista av texter.
    """
    return [
        client.models.embed_content(
            model="text-embedding-004",
            contents=text,
            config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
        ).embeddings[0].values
        for text in texts
    ]


# Skapa en semantisk sökning med cosine similarity för att hitt
def cosine_similarity(vec1, vec2):
     """
     räkna ut likheten mellan två vektorer genom att jämföra deras riktning, ju mer lika riktning desto mer lika är de.
     ska användas för att hitta chunks i instruktionen som är mest lika frågan.
     """

     return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def semantic_search(query, chunks, embeddings, k=5):
    """
    Gör embedding av frågan och jämföra den med alla chunks för att hitta mest likhet
    """
    query_embedding = create_embeddings([query])[0]
    scores = [(i, cosine_similarity(query_embedding, emb)) for i, emb in enumerate(embeddings)]
    top_indices = sorted(scores, key=lambda x: x[1], reverse=True)[:k]
    return [chunks[i] for i, _ in top_indices]

# Generara svar baserat på kotext från PDF dokumentet
system_prompt = """
Du är en hjälpsam AI-assistent. Använd informationen i kontexten nedan för att besvara frågan så bra du kan.
Om inget svar finns, säg att du inte vet.
"""


def generate_response(query, chunks, embeddings):
    context = "\n".join(semantic_search(query, chunks, embeddings))

    user_prompt = f"Fråga: {query}\n\nKontekst:\n{context}"
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(system_instruction=system_prompt),
        contents=user_prompt
    )
    return response.text

#skapa en textbaserad chattbot som kan köras i terminalen

if __name__ == "__main__":
    print(" Chattbot (skriv 'q' för att avsluta)")

  
    pdf_instruktion = (r"D:\Utbildning\VSCODE codes\instruktion.pdf")

    pdf_text = extract_text(pdf_instruktion)

    " === denna kod nedan användes endast för att kontrollera att texten har extraherats korrekt ==="
   # print("\n🔎 UTDRAGEN TEXT (första 1000 tecken):\n")
   # print(pdf_text[:1000])
   # print("\n============================\n") 

# Dela upp texten i mindre delar "Chunks" för att hantera stora textmängder
    chunks = chunk_text(pdf_text)
    embeddings = [create_embeddings([chunk])[0] for chunk in chunks]

    # Starta en enkel terminalbaserad chattbot
    while True:
        prompt = input("Användare: ")
        if prompt == 'q':
            break
        else:
            response = generate_response(prompt, chunks, embeddings)
            print(f"chattbot: " + response)


# REFLEKTION 

"""
Användning i verkligeheten:
Denna chattbot skulle kunna användas av nyanställda eller operatörer för att snabbt hitta svar för instruktioner och riktlinjer i hantering av ett moment

Möjligheter:
Effektiv och snabb åtkomst till information
Färre fel vid tolkning av instruktioner
Möjlighet till att integrera med fler instruktioner och dokument

Utmaningar:
Tydlighet i dokumentationen kan påverka svarens kvalitet
Om dokument ändras måste chattboten uppdateras
Svar kan vara begränsade till det som finns i dokumentet, vilket kan leda till frustration om information saknas
 """