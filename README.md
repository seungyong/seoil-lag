## 🙌 소공과 C반 202003406 김승용

### 🔍 환경 설정 (필수)
기본적으로 모듈 설치가 필수입니다.

```
pip instsall -r requirements.txt
```

각 필요 모듈들은 다음과 같습니다.
- pypdf
- langchain
- chromadb
- langchain_community
- anthropic
- lxml
- transformers
- accelerate
- openai
- openai-whisper
- Flask
- python-dotenv
- bs4
- yt_dlp


```
No module name '~~~~~'
```
라고 발생한다면 해당 모듈을 설치해주시면 감사하겠습니다.

<br />
프로젝트 최상단에 .env 파일을 만들어 다음과 같은 형식으로 저장합니다.

```
OPENAI_API_KEY='MY_OPENAI_API_KEY'
CLAUDE_API_KEY='MY_CLAUDE_API_KEY'
HF_TOKEN='MY_HF_TOKEN'
VECTOR_DB_OPENAI_PATH=openai_vdb
VECTOR_DB_OLLAMA_PATH=ollama_vdb
DATA_PATH=data
NUM_RELEVANT_DOCS='5'
EMBEDDING_MODEL_NAME='openai'
LLM_MODEL_NAME='gpt-4o-mini'
LLM_MODEL_TYPE='gpt'
```

---
ollama는 필수 설치이어야 하며, model은 **llama3.2**를 사용합니다.

```
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
```


openai는 기본적으로 **4o-mini**를 사용합니다.

Yanolza는 적용해보았으나, 컴퓨터 성능 이슈로 인해서 실행해보지 못했습니다. (CPU, Memory 부족)

Claude 또한 적용해보았으나 결제가 되어 있지 않아 실행해보지 못했습니다.
<br /><br />

## ⌛ 실행
기본적으로, Flask를 시작하면 **data** 폴더 안 모든 파일들을 읽어내 **LAG**에 추가합니다.

또한, **env 설정** 또는 **실행 파라미터**로 특정 모델을 선택하여 **LAG**를 추가할 수 있습니다.
```
python app.py
```
<br />

## ✨ 기능
- Ollama 3.2 Chat Bot
- ChatGPT 3.5 turbo ~ 4o-mini Chat Bot
- Yanolza Chat Bot (테스트 X)
- Claude Chat Bot (테스트 X)
- LAG에 추가된 문서 확인
- 문서 갱신 (data 폴더 기반 문서 갱신)
- 문서 추가
  - url로 html 추가 (bs4를 사용하여 필요 텍스트만 가져옴)
  - youtube 추가 (whisper 사용)
  - pdf
  - excel
  - txt 파일 등
- 모델 변경
<br /><br />

## 📷 구동 화면

### 메인 화면 및 챗봇
