# Market Narrative Agent Setup Guide

This project automates the generation and delivery of a "Global Market Narrative Report" using Google Gemini and GitHub Actions.

## 1. Get Your Keys (준비물 챙기기)

### A. Gemini API Key (AI 두뇌)
1.  [Google AI Studio](https://aistudio.google.com/app/apikey)에 접속합니다.
2.  **"Create API key"** 버튼을 누릅니다.
3.  생성된 키를 복사해둡니다. (문자열이 `AIza`로 시작합니다)

### B. Gmail App Password (이메일 발송 권한)
1.  [Google 계정 보안 페이지](https://myaccount.google.com/security)로 이동합니다.
2.  **2단계 인증(2-Step Verification)**이 켜져 있는지 확인합니다. (꺼져 있다면 켜야 합니다)
3.  페이지 맨 위 검색창에 **"앱 비밀번호" (App passwords)**라고 검색해서 클릭합니다.
4.  앱 이름에 `MarketAgent`라고 적고 **만들기(Create)**를 누릅니다.
5.  나타나는 **16자리 비밀번호**를 복사해둡니다. (노란색 상자 안의 문자)

## 2. Put Keys in GitHub (입력하기)

만드신 GitHub 저장소(Repository) 페이지에서 다음 순서대로 클릭하세요:

1.  상단 메뉴 중 **Settings** (설정) 클릭.
2.  왼쪽 메뉴에서 **Secrets and variables** 클릭 -> **Actions** 클릭.
3.  오른쪽의 **New repository secret** (초록색 버튼) 클릭.
4.  아래 **4가지 항목**을 하나씩 추가합니다. (Name칸에 이름을, Secret칸에 값을 넣으세요)

| Name (이름) | Secret (값) | 설명 |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | `AIza...` | 아까 복사한 Gemini API 키 |
| `GMAIL_APP_PASSWORD` | `xxxx xxxx xxxx xxxx` | 아까 복사한 16자리 앱 비밀번호 |
| `EMAIL_SENDER` | `본인Gmail@gmail.com` | 발송할 이메일 주소 (본인) |
| `EMAIL_RECEIVER` | `본인Gmail@gmail.com` | 리포트 받을 이메일 주소 (본인) |

### 3. Test & Enjoy
1.  상단 **Actions** 탭 클릭.
2.  좌측 **Daily Market Narrative Report** 클릭.
3.  오른쪽 **Run workflow** 버튼 클릭 -> 초록색 **Run workflow** 버튼 클릭.
4.  약 1분 뒤 메일함을 확인하세요!

## Automation Schedule
매일 **한국 시간 오전 7시 (KST)**에 자동으로 리포트가 발송됩니다. (UTC 22:00)
