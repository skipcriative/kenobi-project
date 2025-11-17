#kenobi/core/kenobi.py

import requests
import os
import json
import logging
from datetime import datetime, date
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import re
from kenobi.dtos import ResponseDTO, EmailLogDTO, AuditEventDTO
from kenobi.services import build_email_html, send_email, create_email_log, create_audit_event, get_email_log_by_id, get_all_email_recipient_paginated


# Load OpenAI API Key
load_dotenv(override=True)
API_KEY = os.getenv("OPENAI_API_KEY")

FINEP_URL = "https://fapemig.br/oportunidades/chamadas-e-editais" #"http://www.finep.gov.br/chamadas-publicas?situacao=aberta"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Mapa manual para meses abreviados da FAPEMIG
MESES_PT = {
    "jan": 1,
    "fev": 2,
    "mar": 3,
    "abr": 4,
    "mai": 5,
    "jun": 6,
    "jul": 7,
    "ago": 8,
    "set": 9,
    "out": 10,
    "nov": 11,
    "dez": 12,
}

def parse_deadline(deadline_str: str):
    if not deadline_str:
        return None

    deadline_str = deadline_str.strip().lower()

    # 1️⃣ Fluxo contínuo → sempre aberto
    if "fluxo contínuo" in deadline_str or "fluxo continuo" in deadline_str:
        return "fluxo_continuo"

    # 2️⃣ Formato padrão (25/11/2025)
    try:
        return datetime.strptime(deadline_str, "%d/%m/%Y").date()
    except:
        pass

    # 3️⃣ Formato textual: "25 de nov. de 2025"
    # remover pontos
    clean = deadline_str.replace(".", "")

    match = re.match(r"(\d+)\s+de\s+([a-zA-Z]+)\s+de\s+(\d{4})", clean)
    if match:
        dia = int(match.group(1))
        mes_txt = match.group(2)[:3]  # pega "nov" de "nov" ou "novembro"
        ano = int(match.group(3))

        mes = MESES_PT.get(mes_txt)
        if mes:
            return date(ano, mes, dia)

    # se nada funcionar → inválida
    return None


def fetch_calls(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the page
        page.goto(url, wait_until="networkidle")

        # Wait for the grid or shadow DOM to appear
        page.wait_for_selector(".calls__grid", timeout=15000)

        # Evaluate JS inside the page
        calls_grid_html = page.eval_on_selector(
            ".calls__grid",
            "element => element.innerHTML"
        )

        browser.close()
        return calls_grid_html


def parseToResponseDTO(responseText):

    logger.info("Parsing response from ChatGPT to DTO.")

    # Extract JSON part from the response
    jsonStart = responseText.find("{")  # Locate where JSON starts
    jsonEnd = responseText.rfind("```")
    jsonData = responseText[jsonStart:jsonEnd]  # Extract only JSON content
    
    # Parse JSON
    try:
        parsedJson = json.loads(jsonData)
        calls = parsedJson.get("oportunidades", [])  # Get the 'chamadas' array
    except json.JSONDecodeError as e:
        logger.exception("Error parsing JSON from ChatGPT response.")
        return []
    logger.info(f"Got the opportunities.")

    # Validate if the edital is still open
    open_calls = []
    for call in calls:
        deadline_str = call.get("prazo_envio", None)
        parsed = parse_deadline(deadline_str)

        if parsed is None:
            logger.warning(f"Invalid date format in edital: {deadline_str}")
            continue

        # Fluxo contínuo → sempre aberto
        if parsed == "fluxo_continuo":
            open_calls.append(call)
            continue

        # Data válida → comparar com agora
        if date.today() <= parsed:
            open_calls.append(call)

        logger.info(f"Parsed {len(open_calls)} open opportunity calls.")
    
    # Convert JSON into DTOs
    opportunities = []
    for call in open_calls:
        funding_source = call.get("fonte_recurso", "Não especificado.")
    
        #removes brackets and quotes if funding_source is a list type
        if isinstance(funding_source, list):
            funding_source = ", ".join(funding_source)

        opportunities.append(
            ResponseDTO(
                title=call.get("titulo", "Não especificado."),
                resume=call.get("objetivo", "Não especificado."),
                publication_date=call.get("data_publicacao", "Não especificado."),
                deadline=call.get("prazo_envio", "Não especificado."),
                funding_source=funding_source,  # normalized
                funding=call.get("recurso","Não especificado"),
                target_audience=call.get("publico_alvo", "Não especificado."),
                theme=call.get("tema_areas", "Não especificado."),
                link="https://fapemig.br"+call.get("link", "Não especificado."),
                status=call.get("status", "Não especificado.")
            )
        )
    logger.info(f"DTO mounted with {len(opportunities)} opportunities.")

    return opportunities

def ask_chatgpt():
    
    logger.info("Sending content to OpenAI API.")

    content = fetch_calls("https://fapemig.br/oportunidades/chamadas-e-editais")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "Você é um assistente útil que analisa sites de chamadas públicas."},
            {"role": "user", "content": f"Esse é o conteúdo de um site de chamadas públicas extraídas do site FINEP:\n{content}\n\nResuma as oportunidades disponíveis. Traga a resposta em formato json, o array que contém toda informação deve ter o nome de oportunidades, e os seguintes campos: titulo, objetivo(este campo deve ser um resumo de 1 linha com base nas áreas tema) , data_publicacao, prazo_envio, fonte_recurso, recurso(este campo dever trazer o valor em reais R$ total disponível para a oportunidade), publico_alvo(este campo deve ser um resumo de 1 linha com base nas áreas, e resumo disponíveis na página), tema_areas, link, status"}
        ],
        "temperature": 0.7
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        logger.info(f"Received valid response from OpenAI.{response.json()["choices"][0]["message"]["content"]}")
        return response.json()["choices"][0]["message"]["content"]
    else:
        logger.error(f"Error in OpenAI API: {response.status_code}, {response.text}")
        return f"Erro na API: {response.status_code}, {response.text}"


def handle_success(response_dto, subject, recipients, html, response_gpt, response):
        logger.info("Starting handle success.")
        email_log = create_email_log(
            EmailLogDTO(
                subject= subject,
                recipients=str(recipients),
                raw_payload=response_gpt,
                opportunities=str(response_dto),
                html_content=html,
                status="sent",
                api_response_code=response.status_code,
            )
        )
        create_audit_event(
            AuditEventDTO(
                event_type="success",
                message=response.text,
                status_code=response.status_code,
                data=str(response_dto), 
                email_log_id= email_log.id
            )
        )
        logger.info("Finished handle success.")

def handle_failure(response_dto, response):
    create_audit_event(
        AuditEventDTO(
            event_type="error",
            resume="Fail to send email",
            message=response.text,
            status_code=response.status_code,
            data=str(response_dto)
        )
    )

def main():
    subject = "Beta HT: Que a força da captação de recursos esteja com você!"

    recipientsDTO = get_all_email_recipient_paginated()
    recipients = []
    for recipient in recipientsDTO:
        recipients.append(recipient.email)
    
    logger.info(f"Those are the recipients: {recipients}")

    logger.info("Starting Kenobi job - V1: O Despertar da Força.")

    # Step 1: Ask ChatGPT and build email content
    response_gpt = ask_chatgpt()
    response_dto = parseToResponseDTO(response_gpt)
    html = build_email_html(response_dto, "")

    logger.info(f"Sending email to: {recipients}")
    # Step 2: Send email
    response_email = send_email(
        from_addr='"Kenobi 🦘" <naoresponder@gruposkip.com>',
        to_addr= recipients,
        subject=subject,
        html_body=html,
        api_url="http://18.222.179.149:8080/api/email"
    )

    # Step 3: Handle email success or failure
    if response_email.ok:
        logger.info("Email sent successfully.")
        handle_success(response_dto, subject, recipients, html, response_gpt, response_email)
    else:
        logger.error(f"Failed to send email. With code: {response_email.status_code} and message: {response_email.text}")
        handle_failure(response_dto, response_email)
    
    logger.info("Finishig Kenobi job - V1: O Despertar da Força.")

if __name__ == "__main__":
    main()