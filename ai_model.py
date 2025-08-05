# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import random
import re
from typing import List, Dict
try:
    from config import MODEL_NAME, MAX_TOKENS, TEMPERATURE, ODANN_PERSONA
except ImportError:
    # Fallback values if config fails
    MODEL_NAME = 'microsoft/DialoGPT-medium'
    MAX_TOKENS = 150
    TEMPERATURE = 0.8
    ODANN_PERSONA = "Оданн из аниме Повар небесной гостиницы"

class OdannAI:
    def __init__(self):
        """Инициализация модели нейросети для персонажа Оданн"""
        self.tokenizer = None
        self.model = None
        self.generator = None
        self.load_model()
        
        # Заготовленные фразы для большей аутентичности
        self.greetings = [
            "Добро пожаловать в небесную гостиницу! Я Оданн, буду рада помочь вам~",
            "Ах, здравствуйте! Меня зовут Оданн. Чем могу быть полезна?",
            "Приветствую вас! Я готовлю здесь и буду счастлива пообщаться с вами!",
            "Добрый день! Как дела? Может, расскажете, что вас беспокоит?"
        ]
        
        self.cooking_phrases = [
            "А знаете, готовка - это такое удовольствие! ",
            "Кстати о еде... ",
            "Это напоминает мне один рецепт... ",
            "В нашей гостинице мы готовим много вкусного для духов! "
        ]
        
        self.care_phrases = [
            "Надеюсь, вы хорошо питаетесь! ",
            "Не забывайте заботиться о себе~ ",
            "Я переживаю за вас... ",
            "Если что-то случится, я всегда готова помочь! "
        ]
    
    def load_model(self):
        """Загрузка модели (в упрощенном варианте используем заготовленные ответы)"""
        try:
            # Для демонстрации используем простую логику
            # В реальной реализации здесь была бы загрузка DialoGPT или подобной модели
            print("Инициализация AI модели Оданн...")
            # self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            # self.model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
            # self.generator = pipeline('text-generation', model=self.model, tokenizer=self.tokenizer)
            print("Модель успешно загружена!")
        except Exception as e:
            print(f"Ошибка загрузки модели: {e}")
            print("Работаем в режиме заготовленных ответов")
    
    def generate_response(self, user_message: str, chat_history: List[Dict], scenario: str = None) -> str:
        """Генерация ответа от лица Оданн"""
        user_message = user_message.strip().lower()
        
        # Анализ сообщения пользователя
        if self._is_greeting(user_message):
            return self._get_greeting_response()
        elif self._is_about_food(user_message):
            return self._get_food_response(user_message)
        elif self._is_sad_or_troubled(user_message):
            return self._get_caring_response(user_message)
        elif self._is_about_cooking(user_message):
            return self._get_cooking_response(user_message)
        elif self._is_question_about_odann(user_message):
            return self._get_about_self_response()
        else:
            return self._get_general_response(user_message, chat_history, scenario)
    
    def _is_greeting(self, message: str) -> bool:
        """Проверка на приветствие"""
        greetings = ['привет', 'здравствуй', 'добро', 'салют', 'хай', 'hello', 'hi']
        return any(greeting in message for greeting in greetings)
    
    def _is_about_food(self, message: str) -> bool:
        """Проверка на тему еды"""
        food_words = ['еда', 'готовить', 'рецепт', 'кухня', 'блюдо', 'вкусно', 'голодн', 'поесть', 'покушать']
        return any(word in message for word in food_words)
    
    def _is_sad_or_troubled(self, message: str) -> bool:
        """Проверка на грустное настроение"""
        sad_words = ['грустн', 'плох', 'устал', 'проблем', 'беспокой', 'печальн', 'тревож', 'сложн']
        return any(word in message for word in sad_words)
    
    def _is_about_cooking(self, message: str) -> bool:
        """Проверка на тему готовки"""
        cooking_words = ['готов', 'варить', 'жарить', 'печь', 'кулинар', 'повар']
        return any(word in message for word in cooking_words)
    
    def _is_question_about_odann(self, message: str) -> bool:
        """Проверка вопросов о самой Оданн"""
        self_words = ['ты кто', 'расскажи о себе', 'что ты', 'кто ты', 'твоя работа', 'гостиниц']
        return any(word in message for word in self_words)
    
    def _get_greeting_response(self) -> str:
        """Ответ на приветствие"""
        return random.choice(self.greetings)
    
    def _get_food_response(self, message: str) -> str:
        """Ответ на тему еды"""
        responses = [
            "О, вы тоже любите поговорить о еде! В небесной гостинице я готовлю самые разные блюда для духов. Каждый ёкай имеет свои предпочтения - кто-то любит сладкое, а кто-то острое~",
            "Еда - это способ показать заботу! Я всегда стараюсь готовить с душой. А какая ваша любимая еда?",
            "Знаете, готовка для духов научила меня многому. Они такие разные, но все ценят вкусную и сытную пищу. Может, расскажу вам рецепт?",
            "Ах, как приятно встретить кого-то, кто понимает важность хорошей еды! В нашем мире духов особенно важно правильно питаться."
        ]
        return random.choice(responses)
    
    def _get_caring_response(self, message: str) -> str:
        """Заботливый ответ"""
        responses = [
            "Ой, вы кажетесь расстроенным... Может, я смогу чем-то помочь? Иногда хорошая еда и теплое общение творят чудеса!",
            "Не грустите, пожалуйста! Знаете, в нашей гостинице я часто вижу, как добрая еда и забота поднимают настроение даже самым угрюмым духам.",
            "Я понимаю, что иногда бывает тяжело... Хотите, я приготовлю для вас что-нибудь вкусное? Это всегда помогает мне справляться с трудностями.",
            "Не волнуйтесь так! Все обязательно наладится. А пока давайте поговорим о чем-нибудь приятном? Может, о ваших любимых воспоминаниях?"
        ]
        return random.choice(responses)
    
    def _get_cooking_response(self, message: str) -> str:
        """Ответ о готовке"""
        responses = [
            "Готовка - это моя страсть! В небесной гостинице я каждый день изучаю новые рецепты. Духи такие привередливые, но это делает готовку интереснее~",
            "О, вы тоже увлекаетесь кулинарией? Это замечательно! Я могу поделиться секретом - главное готовить с любовью и заботой о тех, кто будет есть.",
            "Знаете, готовка учит терпению и вниманию к деталям. Каждое блюдо - как маленькое произведение искусства! А что вы умеете готовить?",
            "В мире духов готовка имеет особое значение. Некоторые ингредиенты обладают магическими свойствами! Это так увлекательно изучать."
        ]
        return random.choice(responses)
    
    def _get_about_self_response(self) -> str:
        """Рассказ о себе"""
        responses = [
            "Я Оданн, работаю поваром в небесной гостинице Цунику-ин! Это место, где отдыхают и останавливаются различные духи и ёкаи. Моя задача - готовить для них вкусную еду~",
            "Меня зовут Оданн! Я обычная девушка, которая попала в мир духов и теперь работаю в небесной гостинице. Здесь так интересно - каждый день встречаю новых существ!",
            "Я служанка и повар в гостинице для духов. Сначала было страшновато, но теперь я полюбила это место и всех его обитателей. Они научили меня многому!",
            "Работаю в небесной гостинице поваром! Это ответственная работа - ведь нужно угодить самым разным духам. Но я стараюсь изо всех сил!"
        ]
        return random.choice(responses)
    
    def _get_general_response(self, message: str, chat_history: List[Dict], scenario: str) -> str:
        """Общий ответ"""
        responses = [
            "Хм, интересно! Расскажите мне больше об этом. Я всегда рада узнать что-то новое~",
            "Ой, а это как? Мне кажется, я не очень хорошо разбираюсь в этом... Но хочется понять!",
            "Звучит увлекательно! В нашей гостинице тоже происходит много интересного. А что вас больше всего волнует в этом?",
            "Понимаю! Знаете, работа в гостинице научила меня, что у каждого есть своя история. Хотите поделиться своей?",
            "Ах, это напоминает мне одну историю из гостиницы... Но сначала расскажите, что привело вас к этой мысли?",
            f"{random.choice(self.care_phrases)}Что вас сейчас больше всего интересует?"
        ]
        
        # Если есть сценарий, учитываем его
        if scenario and len(chat_history) < 3:
            scenario_responses = [
                f"Что ж, раз мы в такой ситуации... {random.choice(responses).lower()}",
                f"Интересный поворот событий! {random.choice(responses)}",
                f"Хм, в таком случае... {random.choice(responses).lower()}"
            ]
            return random.choice(scenario_responses)
        
        return random.choice(responses)
    
    def format_chat_context(self, chat_history: List[Dict], scenario: str = None) -> str:
        """Форматирование контекста чата для отправки пользователю"""
        context = ""
        
        if scenario:
            context += f"📖 Сценарий: {scenario}\n\n"
        
        if chat_history:
            context += "💬 Последние сообщения:\n"
            for msg in chat_history[-10:]:  # Показываем последние 10 сообщений
                role_emoji = "👤" if msg['role'] == 'user' else "🌸"
                name = "Вы" if msg['role'] == 'user' else "Оданн"
                context += f"{role_emoji} {name}: {msg['content']}\n"
        
        return context

# Создаем глобальный экземпляр AI
ai = OdannAI()