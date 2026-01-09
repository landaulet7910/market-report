import os
import sys
from dotenv import load_dotenv

load_dotenv()
import smtplib
import datetime
import markdown
import google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from duckduckgo_search import DDGS

# --- Configuration ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_RECEIVER = os.environ.get("EMAIL_RECEIVER")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_market_date():
    """Returns the market date string (KST Yesterday, aligning with US Close)."""
    # KST is UTC+9
    kst_timezone = datetime.timezone(datetime.timedelta(hours=9))
    now_kst = datetime.datetime.now(kst_timezone)
    yesterday_kst = now_kst - datetime.timedelta(days=1)
    return yesterday_kst.strftime("%Y-%m-%d")

def search_market_data(date_str):
    """Fetches market data and news using DuckDuckGo."""
    results = {}
    ddgs = DDGS()
    
    queries = [
        f"Nasdaq S&P 500 Russell 2000 closing price {date_str}",
        f"US 10 Year Treasury Yield US Dollar Index {date_str}",
        f"Nikkei 225 Shanghai Composite Euro Stoxx 50 closing price {date_str}",
        f"KOSPI KOSDAQ closing price {date_str}",
        f"top financial news Bloomberg Reuters {date_str}",
        f"key market narratives trending stocks {date_str}",
        f"Asian European market summary {date_str}",
        f"Korea stock market news {date_str}",
        f"analyst buy sell ratings Goldman Sachs Bank of America {date_str}"
    ]

    print(f"[*] Searching data for {date_str}...")
    full_text = ""
    for q in queries:
        try:
            search_results = ddgs.text(q, max_results=3)
            if search_results:
                for r in search_results:
                    full_text += f"- {r['title']}: {r['body']}\n"
        except Exception as e:
            print(f"[!] Error searching for '{q}': {e}")
    
    return full_text

def generate_report(date_str, search_context):
    """Generates the Markdown report using Gemini."""
    print("[*] Generating report with Gemini...")
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = f"""
        You are a 12-year experienced Financial Strategist and AI System Architect.
        Your specific role is 'Global Market Narrative Architect'.
        
        Current Date: {date_str}
        
        [CONTEXT DATA FROM WEB SEARCH]
        {search_context}
        
        [TASK]
        Create a 'Global Market Narrative Report' in Korean.
        Follow this exact structure:
        
        # Global Market Narrative Report
        **Date:** {date_str}
        **Role:** Global Market Narrative Architect

        ## [Big Picture] 오늘의 결론
        (One sharp sentence defining the market's gravity + Brief summary)

        ## [Market Metrics] 지수 및 1년 추세
        *기준일: {date_str}*
        (Create a Markdown Table with columns: Index, Price, Change, Analysis. Cover the following:)
        - **US**: Nasdaq, S&P 500, Russell 2000, 10Y Yield, DXY
        - **Global**: Nikkei 225, Shanghai Composite, Euro Stoxx 50
        - **Korea**: KOSPI, KOSDAQ

        ## [Small Pictures] 3가지 핵심 서사 (The 3-Filter Model)
        (Identify 3 key narratives. Include at least one global/macro theme if relevant. Filter each through: 1. CAPEX, 2. Policy, 3. Standard)
        *Format:*
        ### 1. [Title]
        **[현상]** ...
        - **CAPEX**: ...
        - **Policy**: ...
        - **Standard**: ...

        ## [Actionable] 수혜 섹터 및 종목
        (List Buy/Avoid sectors/tickers with reasoning)

        ## [Sentiment] 기관 리포트 분석
        (Analyze institutional sentiment and point out missed risks)
        
        *Style Note:* Professional, insightful, cynical yet constructive.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"[!] Gemini generation failed: {e}")
        return None

def send_email(subject, body_md):
    """Sends the report via Gmail SMTP."""
    print(f"[*] Sending email to {EMAIL_RECEIVER}...")
    
    try:
        # Convert Markdown to HTML
        html_content = markdown.markdown(body_md, extensions=['tables'])
        
        # Email Setup
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        
        # Handle multiple recipients
        if "," in EMAIL_RECEIVER:
            recipients = [r.strip() for r in EMAIL_RECEIVER.split(",")]
            msg['To'] = ", ".join(recipients)
        else:
            msg['To'] = EMAIL_RECEIVER
            recipients = [EMAIL_RECEIVER]
            
        msg['Subject'] = subject
        
        # Add HTML body (wrapped for better styling)
        final_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                h1, h2, h3 {{ color: #2c3e50; }}
                blockquote {{ border-left: 4px solid #ccc; margin: 0; padding-left: 10px; color: #666; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        msg.attach(MIMEText(final_html, 'html'))
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_SENDER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        print("[+] Email sent successfully!")
        return True
    except Exception as e:
        print(f"[!] Email failed: {e}")
        return False

def main():
    if not GEMINI_API_KEY:
        print("[!] GEMINI_API_KEY is missing")
        sys.exit(1)
        
    if not GMAIL_APP_PASSWORD or not EMAIL_SENDER or not EMAIL_RECEIVER:
        print("[!] Email configuration is missing")
        sys.exit(1)

    market_date = get_market_date()
    search_data = search_market_data(market_date)
    
    if not search_data:
        print("[!] No data found. Aborting.")
        sys.exit(1)

    report_md = generate_report(market_date, search_data)
    if not report_md:
        print("[!] Report generation failed.")
        sys.exit(1)
    
    email_subject = f"[Market Narrative] {market_date} Daily Report"
    success = send_email(email_subject, report_md)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
