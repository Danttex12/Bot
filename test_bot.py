#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый скрипт для проверки функциональности бота Оданна
Запускается без Telegram API для локального тестирования
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from odanna_bot import DatabaseManager, AIManager, OdannaBot
import sqlite3
import tempfile

def test_database():
    """Тест базы данных"""
    print("🗃️ Тестирование базы данных...")
    
    # Создаем временную БД
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_db:
        db_path = temp_db.name
    
    try:
        db = DatabaseManager(db_path)
        
        # Тест добавления пользователя
        db.add_user(12345, "test_user", "Тест", "Пользователь", "female")
        print("✅ Пользователь добавлен")
        
        # Тест создания чата
        chat_id = db.create_chat(12345, "Тестовый чат")
        print(f"✅ Чат создан: {chat_id}")
        
        # Тест добавления сообщения
        db.add_message(chat_id, 12345, "Привет, Оданна!", "Добро пожаловать в гостиницу.", "радость", 45)
        print("✅ Сообщение добавлено")
        
        # Тест получения истории
        history = db.get_chat_history(chat_id)
        assert len(history) == 1
        print("✅ История чата получена")
        
        # Тест функции "забыть"
        db.ignore_message(chat_id, "Привет, Оданна!")
        print("✅ Сообщение помечено как забытое")
        
        print("🎉 Все тесты базы данных пройдены!")
        
    finally:
        os.unlink(db_path)

def test_ai_manager():
    """Тест ИИ-менеджера"""
    print("\n🧠 Тестирование ИИ-менеджера...")
    
    ai = AIManager()
    
    # Тест анализа эмоций
    emotions = ai.analyze_emotion("Мне очень грустно сегодня...")
    print(f"✅ Анализ эмоций: {emotions}")
    
    emotions2 = ai.analyze_emotion("Как дела? Что нового?")
    print(f"✅ Анализ эмоций: {emotions2}")
    
    # Тест расчета эмпатии
    empathy = ai.calculate_empathy_level("грусть", 35, 5)
    print(f"✅ Уровень эмпатии: {empathy}%")
    
    # Тест генерации ответа (fallback)
    response = ai._fallback_response("Мне плохо", 60, "грусть")
    print(f"✅ Ответ сгенерирован: {response[:50]}...")
    
    print("🎉 Все тесты ИИ-менеджера пройдены!")

def test_character_responses():
    """Тест характерных ответов Оданны"""
    print("\n🎭 Тестирование характера Оданны...")
    
    ai = AIManager()
    
    test_cases = [
        ("Здравствуйте", 35, "нейтральное"),
        ("Мне очень плохо...", 70, "грусть"),
        ("Спасибо вам!", 50, "радость"),
        ("Что это за место?", 40, "любопытство"),
        ("Я устал от всего", 65, "грусть, усталость")
    ]
    
    for message, empathy, emotion in test_cases:
        response = ai._fallback_response(message, empathy, emotion)
        print(f"\n📨 Сообщение: {message}")
        print(f"😊 Эмпатия: {empathy}%")
        print(f"💭 Эмоция: {emotion}")
        print(f"🏮 Оданна: {response}")
        
        # Проверяем, что ответ соответствует характеру
        if empathy < 45:
            assert any(marker in response for marker in ["*", "Как... любопытно", "прищуривает"]), \
                "Низкая эмпатия должна содержать ироничные элементы"
        
        if empathy > 60 and "грусть" in emotion:
            assert any(word in response for word in ["понимание", "забота", "не волнуйтесь", "доверьтесь"]), \
                "Высокая эмпатия должна содержать элементы поддержки"
    
    print("\n🎉 Все тесты характера пройдены!")

def test_memory_system():
    """Тест системы памяти"""
    print("\n💾 Тестирование системы памяти...")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_db:
        db_path = temp_db.name
    
    try:
        db = DatabaseManager(db_path)
        
        # Создаем тестовые данные
        db.add_user(12345, "test_user")
        chat_id = db.create_chat(12345, "Тест памяти")
        
        # Добавляем сообщения
        messages = [
            "Привет!",
            "Как дела?",
            "Расскажи о себе",
            "Забудь про вчерашний разговор"
        ]
        
        for i, msg in enumerate(messages):
            db.add_message(chat_id, 12345, msg, f"Ответ {i+1}", "нейтральное", 40)
        
        # Тест получения истории
        history = db.get_chat_history(chat_id)
        assert len(history) == 4
        print("✅ История из 4 сообщений создана")
        
        # Тест функции "забыть"
        db.ignore_message(chat_id, "Расскажи о себе")
        
        # Проверяем, что сообщение помечено как забытое
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT is_ignored FROM messages 
            WHERE chat_id = ? AND message_text = ?
        ''', (chat_id, "Расскажи о себе"))
        result = cursor.fetchone()
        conn.close()
        
        assert result[0] == 1  # TRUE в SQLite = 1
        print("✅ Сообщение помечено как забытое")
        
        # Тест восстановления сообщения
        db.unignore_message(chat_id, "Расскажи о себе")
        print("✅ Сообщение восстановлено")
        
        print("🎉 Все тесты системы памяти пройдены!")
        
    finally:
        os.unlink(db_path)

def test_empathy_progression():
    """Тест прогрессии эмпатии"""
    print("\n📈 Тестирование прогрессии эмпатии...")
    
    ai = AIManager()
    
    # Симулируем диалог
    dialogue_stages = [
        (1, "нейтральное", 35),  # Начало
        (3, "любопытство", 35),  # Первые сообщения
        (5, "радость", 50),      # Середина диалога
        (8, "грусть", 50),       # Продолжение
        (12, "грусть", 70),      # Долгий диалог
        (15, "радость", 70),     # Завершение
    ]
    
    prev_empathy = 35
    for msg_count, emotion, expected_base in dialogue_stages:
        empathy = ai.calculate_empathy_level(emotion, prev_empathy, msg_count)
        print(f"Сообщение {msg_count}: {emotion} → Эмпатия {empathy}%")
        
        # Проверяем, что эмпатия изменяется логично
        if "грусть" in emotion:
            assert empathy >= prev_empathy, "Эмпатия должна расти при грусти"
        
        assert 35 <= empathy <= 85, "Эмпатия должна быть в диапазоне 35-85%"
        prev_empathy = empathy
    
    print("🎉 Тест прогрессии эмпатии пройден!")

def run_all_tests():
    """Запуск всех тестов"""
    print("🚀 Запуск тестов бота Оданна...\n")
    
    try:
        test_database()
        test_ai_manager()
        test_character_responses()
        test_memory_system()
        test_empathy_progression()
        
        print("\n" + "="*50)
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО! 🎉")
        print("🏮 Оданна готов к работе!")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ Ошибка в тестах: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)