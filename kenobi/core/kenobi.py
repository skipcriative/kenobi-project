#kenobi/core/kenobi.py

import requests
import os
import json
from datetime import datetime, date
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from kenobi.dtos import ResponseDTO, EmailLogDTO, AuditEventDTO
from kenobi.services import build_email_html, send_email, create_email_log, create_audit_event, get_email_log_by_id


# Load OpenAI API Key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

FINEP_URL = "http://www.finep.gov.br/chamadas-publicas?situacao=aberta" #"http://www.finep.gov.br/chamadas-publicas/chamadaspublicas"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def fetch_finep_calls():
    """Scrapes FINEP website for public calls."""
    response = requests.get(FINEP_URL)
    if response.status_code != 200:
        return f"Erro ao acessar o site: {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")

    return soup 

def parseToResponseDTO(responseText):
    """Parses the JSON response and converts it into DTOs."""
    # Extract JSON part from the response

    # print(f"This is the original text: {responseText}")
    jsonStart = responseText.find("{")  # Locate where JSON starts
    jsonEnd = responseText.rfind("```")
    jsonData = responseText[jsonStart:jsonEnd]  # Extract only JSON content
    
    # print(f"This is the json after tretment: {jsonData}")
    # Parse JSON
    try:
        parsedJson = json.loads(jsonData)
        calls = parsedJson.get("oportunidades", [])  # Get the 'chamadas' array
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return []
    
    # Validate if the edital is still open
    open_calls = []
    for call in calls:
        deadline_str = call.get("prazo_envio", None)
        if deadline_str:
            try:
                deadline_date = datetime.strptime(deadline_str, "%d/%m/%Y").date()
                if date.today() <= deadline_date:
                    open_calls.append(call)
            except ValueError:
                print(f"⚠️ Invalid date format: {deadline_str}")

    # Convert JSON into DTOs
    opportunities = [
        ResponseDTO(
            title=call.get("titulo", "N/A"),
            resume = call.get("objetivo","N/A"),
            publication_date=call.get("data_publicacao", "N/A"),
            deadline=call.get("prazo_envio", "N/A"),
            funding_source=call.get("fonte_recurso", "N/A"),
            target_audience=call.get("publico_alvo", "N/A"),
            theme=call.get("tema_areas", "N/A"),
            link=call.get("link", "N/A"),
            status=call.get("status","N/A")
        )
        for call in open_calls
    ]

    return opportunities

def ask_chatgpt():
    """Sends scraped data to ChatGPT for analysis."""
    # content = title + "" + link

    content = fetch_finep_calls()
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "Você é um assistente útil que analisa sites de chamadas públicas."},
            {"role": "user", "content": f"Esse é o conteúdo de um site de chamadas públicas extraídas do site FINEP:\n{content}\n\nResuma as oportunidades disponíveis. Traga a resposta em formato json, o array que contém toda informação deve ter o nome de oportunidades, e os seguintes campos: titulo, objetivo, data_publicacao, prazo_envio, fonte_recurso, publico_alvo, tema_areas, link, status"}
        ],
        "temperature": 0.7
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Erro na API: {response.status_code}, {response.text}"

if __name__ == "__main__":
    response_gpt = ask_chatgpt()
    responseDTO = parseToResponseDTO(response_gpt)   
    html = build_email_html(responseDTO,"")

    subject = "Testing Persistence - on HT"
    recipients = "eduardo.lemos16@gmail.com,eduardo.lemos@gruposkip.com,lizmatiaslisboa@gmail.com,thallescarvalhocm@gmail.com"
    
    response = send_email(
    from_addr="naoresponder@gruposkip.com",
    to_addr= recipients,
    subject= subject,
    html_body=html,
    api_url="http://18.222.179.149:8080//api/email")

    if(response.ok):
        print("✅ Email sent!")
        email_log = create_email_log(
            EmailLogDTO(
                subject= subject,
                recipients=recipients,
                raw_payload="mockRaw-timestampTest3", #response_gpt,
                opportunities=str(responseDTO),
                html_content=html,
                status="sent",
                api_response_code="mockValue", #response.status_code,
            )
        )
        create_audit_event(
            AuditEventDTO(
                event_type="success",
                message="mockValue", #response.text,
                status_code="mockValue", #response.status_code,
                data=str(responseDTO), 
                email_log_id= email_log.id
            )
        )
    else:
        print("Fail to send email!")
        create_audit_event(
            AuditEventDTO(
                event_type="Mock error",
                resume="Fail to send email",
                message="mockValue", #response.text,
                status_code="mockValue", #response.status_code,
                metadados=str(responseDTO)
            )
        )
    




    
        

