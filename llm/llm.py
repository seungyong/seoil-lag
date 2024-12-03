from abc import ABC, abstractmethod
from langchain_community.llms.ollama import Ollama
from openai import OpenAI
from langchain.prompts import ChatPromptTemplate
import anthropic
from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM

PROMPT_TEMPLATE = """
Basing only on the following context:

{context}

---

Answer the following question: {question}
Avoid to start the answer saying that you are basing on the provided context and go straight with the response.
"""

class LLM(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def invoke(self, prompt: str) -> str:
        pass

    def generate_response(self, context: str, question: str) -> str:
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context, question=question)
        response_text = self.invoke(prompt)
        return response_text

class OllamaModel(LLM):
    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.model = Ollama(model=model_name)

    def invoke(self, prompt: str) -> str:
        return self.model.invoke(prompt)

class GPTModel(LLM):
    def __init__(self, model_name: str, api_key: str):
        super().__init__(model_name)
        self.client = OpenAI(api_key=api_key)

    def invoke(self, prompt: str) -> str:
        messages = [
            #{"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()


class YanoljaModel(LLM):
    def __init__(self, model_name: str):
        super().__init__(model_name)
        # 모델과 토크나이저를 초기화 시 한 번만 로드
        print(model_name)
        self.client = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype="float16",
                                                            device_map="auto", low_cpu_mem_usage=True)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, low_cpu_mem_usage=True)

    def invoke(self, prompt: str) -> str:
        # 입력 길이 제한을 적용 (모델의 최대 입력 토큰 길이 확인)
        max_input_length = self.tokenizer.model_max_length
        encoded_input = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=max_input_length)

        # 모델 출력 생성
        outputs = self.client.generate(
            **encoded_input,
            max_new_tokens=256
        )

        # 출력 텍스트 디코딩 및 공백 제거
        output_text = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

        return output_text

class AnthropicModel(LLM):
    def __init__(self, model_name: str, api_key: str):
        super().__init__(model_name)
        self.client = anthropic.Anthropic(api_key=api_key)

    def invoke(self, prompt: str) -> str:
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=1000,
            temperature=0.7,
            messages=messages
        )
        # Extract the plain text from the response content
        text_blocks = response.content
        plain_text = "\n".join(block.text for block in text_blocks if block.type == 'text')
        return plain_text