import os
import yt_dlp
import whisper

from langchain.schema import Document
from langchain_community.document_loaders import RecursiveUrlLoader
from bs4 import BeautifulSoup


def youtube_loader(url: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio.%(ext)s',
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}
        ],
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])  # 오디오 다운로드
            title = ydl.extract_info(url, download=False)['title']

        model = whisper.load_model("small")  # Whisper large 모델 사용

        # 3. 오디오 파일을 Whisper로 텍스트로 변환
        result = model.transcribe("temp_audio.mp3")
        content = result['text']

        # 임시 오디오 파일 삭제
        os.remove("temp_audio.mp3")

        return title, content
    except Exception as e:
        print(f"Error processing audio: {e}")
        return []


def clean_html(content):
    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(content, "html.parser")

    for tag in soup([
            'script', 'style', 'meta', 'link', 'title', 'aside', 'figure', 'figcaption', 'label', 'input', 'select',
            'footer', 'header', 'nav', 'iframe', 'form', 'button', 'section', 'img', 'svg', 'path', 'video', 'audio',
            'source', 'track', 'map', 'area', 'canvas', 'embed', 'object', 'param', 'applet', 'frame', 'frameset',
            'noframes', 'base', 'basefont', 'bgsound', 'blink', 'isindex', 'keygen', 'menu', 'menuitem', 'noembed', 'a'
    ]):
        tag.decompose()

    # 모든 태그 제거하고 텍스트만 추출
    text = soup.get_text(separator="\n", strip=True)

    return str(text)


def universal_url_loader(source):
    if 'youtu' in source:
        title, content = youtube_loader(source)
        return [Document(page_content=content, metadata={'source': source, 'title': title})]
    else:
        loader = RecursiveUrlLoader(
            source,
            prevent_outside=True,
            link_regex=r'<a\s+(?:[^>]*?\s+)?href="([^"]*(?=index)[^"]*)"'
        )
        docs = loader.load()
        return [
            Document(page_content=clean_html(doc.page_content), metadata=doc.metadata)
            for doc in docs
        ]
