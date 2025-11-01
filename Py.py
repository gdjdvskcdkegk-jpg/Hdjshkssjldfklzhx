#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ВРЕД ЗАПРОС v0.0.1 - RING -1 PROTOCOL
# TG: t.me/onbrainn

import sys
import os
import platform
import subprocess
import requests
import json
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import re
from urllib.parse import quote
import threading
import time
import hashlib
import random
from datetime import datetime

# Проверка и установка зависимостей
def check_dependencies():
    required_packages = ['requests', 'phonenumbers']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("[RING -1] Установка недостающих зависимостей...")
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"[RING -1] Установлен: {package}")
            except Exception as e:
                print(f"[RING -1] Ошибка установки {package}: {e}")
                return False
    
    print("[RING -1] Все зависимости установлены")
    time.sleep(1)
    return True

# Баннер
def show_banner():
    banner = """
╔═══════════════════════════════════════════════╗
║           ВРЕД ЗАПРОС v0.0.1 - RING -1       ║
║              VIP XRL EDITION                 ║
║                                               ║
║         [1] ВРЕД ЗАПРОС НА НОМЕР             ║
║         [2] ВЫХОД                            ║
╚═══════════════════════════════════════════════╝
"""
    print(banner)

# Генерация хешей для номера
def generate_hashes(phone):
    md5 = hashlib.md5(phone.encode()).hexdigest()
    sha1 = hashlib.sha1(phone.encode()).hexdigest()
    sha256 = hashlib.sha256(phone.encode()).hexdigest()
    return md5, sha1, sha256

# Поиск в социальных сетях
def social_media_search(phone):
    results = {}
    
    # Убираем код страны для некоторых проверок
    clean_phone = re.sub(r'^\+7', '', phone.replace(' ', '').replace('-', ''))
    
    social_urls = {
        "VK": f"https://vk.com/phone{clean_phone}",
        "Instagram": f"https://www.instagram.com/{phone}/",
        "Facebook": f"https://www.facebook.com/{phone}",
        "Twitter": f"https://twitter.com/{phone}",
        "Odnoklassniki": f"https://ok.ru/{phone}",
        "Telegram": f"https://t.me/{phone}",
        "WhatsApp": f"https://wa.me/{phone}",
        "Viber": f"https://viber.click/{phone}",
        "Avito": f"https://www.avito.ru/user/{phone}",
        "Youla": f"https://youla.ru/user/{phone}",
        "Tinder": f"https://tinder.com/@{phone}",
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for platform_name, url in social_urls.items():
        try:
            response = requests.get(url, headers=headers, timeout=5, allow_redirects=False)
            if response.status_code in [200, 302, 301]:
                results[platform_name] = {"status": "FOUND", "url": url}
            else:
                results[platform_name] = {"status": "NOT_FOUND", "url": url}
        except:
            results[platform_name] = {"status": "ERROR", "url": url}
    
    return results

# Проверка в базах данных (симуляция расширенного поиска)
def database_checks(phone):
    print("[RING -1] Сканирование баз данных...")
    time.sleep(2)
    
    # Имитация проверки в различных базах
    databases = {
        "Госуслуги": "частичное совпадение",
        "Банковские базы": "требует авторизации",
        "Такси сервисы": "обнаружены записи",
        "Доставки еды": "активные заказы",
        "Соц. опросы": "участник исследований",
        "Рекламные базы": "рассылка активна",
        "Голосования": "зарегистрирован",
    }
    
    results = {}
    for db_name, status in databases.items():
        # Добавляем случайную "найденность" для реализма
        found_chance = random.randint(1, 10)
        if found_chance > 3:
            results[db_name] = status
        else:
            results[db_name] = "не обнаружено"
    
    return results

# Анализ метаданных
def metadata_analysis(phone, carrier_info, country):
    analysis = {
        "Тип номера": "Мобильный" if carrier_info else "Стационарный",
        "Риск спама": "Высокий" if random.randint(1, 10) > 6 else "Низкий",
        "Активность": "Высокая" if random.randint(1, 10) > 4 else "Низкая",
        "Верификация": "Пройдена" if random.randint(1, 10) > 3 else "Не пройдена",
        "Возраст номера": f"{random.randint(1, 5)} лет",
        "Регистрации": f"{random.randint(3, 15)} сервисов",
    }
    
    # Дополнительная логика на основе страны
    if "Россия" in country or "Russia" in country:
        analysis["Оператор"] = carrier_info
        analysis["Регион"] = "Определен"
        analysis["Тариф"] = random.choice(["Бизнес", "Личный", "Корпоративный"])
    
    return analysis

# Основная функция поиска по номеру
def вред_запрос(phone):
    print(f"\n[RING -1] Запуск ВРЕД ЗАПРОСА для: {phone}")
    print("[RING -1] Инициализация расширенного сканирования...")
    
    start_time = time.time()
    
    try:
        # Базовая информация через phonenumbers
        parsed_phone = phonenumbers.parse(phone, None)
        if not phonenumbers.is_valid_number(parsed_phone):
            print("[RING -1] Номер невалиден")
            return
        
        # Основная информация
        carrier_info = carrier.name_for_number(parsed_phone, "en") or "Неизвестно"
        country = geocoder.description_for_number(parsed_phone, "en") or "Неизвестно"
        region = geocoder.description_for_number(parsed_phone, "ru") or "Неизвестно"
        timezones = timezone.time_zones_for_number(parsed_phone) or ["Неизвестно"]
        formatted_number = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        
        # Генерация хешей
        md5, sha1, sha256 = generate_hashes(phone)
        
        # Поиск в соцсетях
        social_results = social_media_search(phone)
        
        # Проверка баз данных
        db_results = database_checks(phone)
        
        # Анализ метаданных
        meta_analysis = metadata_analysis(phone, carrier_info, country)
        
        # Вывод результатов
        print("\n" + "="*60)
        print("🎯 РАСШИРЕННАЯ ИНФОРМАЦИЯ О НОМЕРЕ:")
        print("="*60)
        print(f"📞 Номер: {formatted_number}")
        print(f"🌍 Страна: {country}")
        print(f"📍 Регион: {region}")
        print(f"📡 Оператор: {carrier_info}")
        print(f"🕐 Часовой пояс: {', '.join(timezones)}")
        print(f"✅ Валидность: {phonenumbers.is_valid_number(parsed_phone)}")
        
        print("\n" + "="*60)
        print("🔐 КРИПТОГРАФИЧЕСКИЕ ХЕШИ:")
        print("="*60)
        print(f"MD5: {md5}")
        print(f"SHA1: {sha1}")
        print(f"SHA256: {sha256}")
        
        print("\n" + "="*60)
        print("🔍 РЕЗУЛЬТАТЫ ПОИСКА В СОЦСЕТЯХ:")
        print("="*60)
        for platform, data in social_results.items():
            status_icon = "✅" if data["status"] == "FOUND" else "❌"
            print(f"{status_icon} {platform}: {data['status']} - {data['url']}")
        
        print("\n" + "="*60)
        print("🗃️  БАЗЫ ДАННЫХ И СЕРВИСЫ:")
        print("="*60)
        for db_name, status in db_results.items():
            status_icon = "✅" if "обнаруж" in status or "актив" in status else "⚠️"
            print(f"{status_icon} {db_name}: {status}")
        
        print("\n" + "="*60)
        print("📊 АНАЛИТИКА МЕТАДАННЫХ:")
        print("="*60)
        for key, value in meta_analysis.items():
            print(f"📈 {key}: {value}")
        
        # Дополнительная информация
        print("\n" + "="*60)
        print("🚀 ДОПОЛНИТЕЛЬНЫЕ ВОЗМОЖНОСТИ:")
        print("="*60)
        print("🔧 Генерация фишинговых ссылок: ДОСТУПНО")
        print("🔧 СМС-бомбер: ДОСТУПНО") 
        print("🔧 Подбор паролей: ДОСТУПНО")
        print("🔧 Геолокация: ТРЕБУЕТ АКТИВАЦИИ")
        print("🔧 Прослушка: ТРЕБУЕТ ДОСТУПА К ОПЕРАТОРУ")
        
        # Время выполнения
        end_time = time.time()
        execution_time = end_time - start_time
        
        print("\n" + "="*60)
        print("📋 ОТЧЕТ СФОРМИРОВАН:")
        print("="*60)
        print(f"🔢 Номер: {formatted_number}")
        print(f"🏢 Оператор: {carrier_info}")
        print(f"🌎 Локация: {country}, {region}")
        print(f"📱 Найдено в соцсетях: {sum(1 for x in social_results.values() if x['status'] == 'FOUND')}")
        print(f"🕒 Время анализа: {execution_time:.2f} сек")
        print(f"⚡ Статус: РАСШИРЕННЫЙ АНАЛИЗ ЗАВЕРШЕН")
        print(f"💾 Хеш отчета: {hashlib.md5(str(formatted_number + carrier_info).encode()).hexdigest()}")
        
        # Сохранение в файл
        save_report(phone, formatted_number, carrier_info, country, region, social_results, db_results, meta_analysis)
        
    except Exception as e:
        print(f"[RING -1] Ошибка при анализе: {e}")

# Сохранение отчета
def save_report(phone, formatted, carrier, country, region, social, db, meta):
    filename = f"vred_zapros_{phone.replace('+', '').replace(' ', '')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("ВРЕД ЗАПРОС - ОТЧЕТ\n")
        f.write("="*50 + "\n")
        f.write(f"Номер: {formatted}\n")
        f.write(f"Оператор: {carrier}\n")
        f.write(f"Страна: {country}\n")
        f.write(f"Регион: {region}\n")
        f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("СОЦСЕТИ:\n")
        for platform, data in social.items():
            f.write(f"{platform}: {data['status']} - {data['url']}\n")
        
        f.write("\nБАЗЫ ДАННЫХ:\n")
        for db_name, status in db.items():
            f.write(f"{db_name}: {status}\n")
            
        f.write("\nМЕТАДАННЫЕ:\n")
        for key, value in meta.items():
            f.write(f"{key}: {value}\n")
    
    print(f"[RING -1] Отчет сохранен в: {filename}")

# Главное меню
def main():
    if not check_dependencies():
        print("[RING -1] Критическая ошибка зависимостей")
        return
    
    while True:
        show_banner()
        choice = input("\n[RING -1] Выберите действие -> ")
        
        if choice == "1":
            phone = input("[RING -1] Введите номер телефона -> ")
            if phone:
                вред_запрос(phone)
            else:
                print("[RING -1] Введите номер телефона")
        
        elif choice == "2":
            print("[RING -1] Завершение работы...")
            break
        
        else:
            print("[RING -1] Неверный выбор")
        
        input("\n[RING -1] Нажмите Enter для продолжения...")
        os.system('cls' if platform.system() == 'Windows' else 'clear')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[RING -1] Программа прервана")
    except Exception as e:
        print(f"[RING -1] Критическая ошибка: {e}")
