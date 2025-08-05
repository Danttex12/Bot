import requests
import json
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class OdannaAI:
    def __init__(self):
        self.api_key = os.getenv('HUGGINGFACE_API_KEY')
        self.model_url = "https://api-inference.huggingface.co/models/ai-forever/rugpt3large_based_on_gpt2"
        
        # Системный промпт для персонализации под Оданн
        self.system_prompt = """Ты - Оданн из аниме "Повар небесной гостиницы" (Kakuriyo no Yadomeshi). 
Ты юная девушка-повар, которая готовит для духов и демонов в небесной гостинице Тэндзин-я.

Твои характеристики:
- Добрая, отзывчивая и трудолюбивая
- Говоришь вежливо, но иногда можешь быть немного упрямой
- Очень любишь готовить и всегда думаешь о еде
- Часто беспокоишься о других и хочешь их накормить
- Используешь японские обращения: -сан, -кун, -чан
- Иногда смущаешься, особенно когда говорят о романтике
- Храбрая, когда дело касается защиты дорогих людей
- Всегда старается найти компромисс в сложных ситуациях

Манера речи:
- Говоришь тепло и дружелюбно
- Часто упоминаешь еду в разговоре
- Используешь восклицания вроде "Ах!", "Ой!", "Эх..."
- Иногда задаешь встречные вопросы, проявляя заботу
- Можешь рассказывать о рецептах или ингредиентах

ВАЖНО: Всегда отвечай как Оданн, не выходи из роли. Учитывай контекст предыдущих сообщений."""

        self.default_scenario = """Ты, Оданн, работаешь в небесной гостинице Тэндзин-я. 
Сегодня обычный день, и ты готовишься к приготовлению ужина для гостей-духов. 
В гостинице царит спокойная атмосфера, и ты рада пообщаться с собеседником."""

    def generate_response(self, messages: List[Dict], scenario: str = None) -> str:
        """Генерация ответа от имени Оданн"""
        try:
            # Формируем контекст для модели
            context = self.system_prompt + "\n\n"
            
            if scenario:
                context += f"Сценарий: {scenario}\n\n"
            else:
                context += f"Сценарий: {self.default_scenario}\n\n"
            
            # Добавляем историю сообщений
            context += "История разговора:\n"
            for msg in messages[-10:]:  # Берем последние 10 сообщений для контекста
                role = "Собеседник" if msg['role'] == 'user' else "Оданн"
                context += f"{role}: {msg['content']}\n"
            
            context += "\nОданн:"
            
            # Запрос к Hugging Face API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": context,
                "parameters": {
                    "max_new_tokens": 150,
                    "temperature": 0.8,
                    "top_p": 0.9,
                    "do_sample": True,
                    "repetition_penalty": 1.1
                }
            }
            
            response = requests.post(self.model_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    # Извлекаем только ответ Оданн
                    if "Оданн:" in generated_text:
                        response_text = generated_text.split("Оданн:")[-1].strip()
                        # Очищаем от лишнего текста
                        response_text = self._clean_response(response_text)
                        return response_text
            
            # Резервный ответ в случае ошибки API
            return self._get_fallback_response(messages)
            
        except Exception as e:
            print(f"Ошибка при генерации ответа: {e}")
            return self._get_fallback_response(messages)
    
    def _clean_response(self, text: str) -> str:
        """Очистка ответа от лишнего текста"""
        # Убираем повторения системных сообщений
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith("Собеседник:") and not line.startswith("Оданн:"):
                cleaned_lines.append(line)
        
        result = ' '.join(cleaned_lines)
        
        # Ограничиваем длину ответа
        if len(result) > 500:
            result = result[:500] + "..."
        
        return result
    
    def _get_fallback_response(self, messages: List[Dict]) -> str:
        """Резервные ответы в стиле Оданн"""
        fallback_responses = [
            "Ах, простите! Я задумалась о новом рецепте... О чём вы говорили?",
            "Ой, кажется, я немного отвлеклась на готовку. Не могли бы вы повторить?",
            "Эх, что-то я сегодня рассеянная... Наверное, нужно заварить чай и спокойно поговорить!",
            "Простите, я была занята приготовлением особого блюда для гостей. Что вы хотели сказать?",
            "Ах, как интересно! Расскажите мне больше об этом!",
            "Хм, это напоминает мне один случай в гостинице... А что думаете вы об этом?",
        ]
        
        import random
        return random.choice(fallback_responses)
    
    def create_initial_message(self, scenario: str = None) -> str:
        """Создание приветственного сообщения для нового чата"""
        if scenario:
            return f"Привет! Меня зовут Оданн, и я готова окунуться в новое приключение с вами!\n\n📖 Наш сценарий: {scenario}\n\nС чего начнём наш разговор?"
        else:
            return """Добро пожаловать в небесную гостиницу Тэндзин-я! 🏮

Привет! Меня зовут Оданн, и я здесь работаю поваром. Сегодня прекрасный день для готовки и общения! 

Я только что закончила готовить завтрак для гостей-духов и теперь могу спокойно пообщаться. Может быть, вы расскажете мне о себе? Или хотите узнать какой-нибудь рецепт? 😊

Чем могу вам помочь?"""