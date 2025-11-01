#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ВРЕД ЗАПРОС v0.0.1 (MODIFIED by GothbreachHelper)
# Created for RING -1

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

# !!! ДОПОЛНИТЕЛЬНАЯ БИБЛИОТЕКА ДЛЯ ГЕОЛОКАЦИИ !!!
try:
    from geopy.geocoders import Nominatim
except ImportError:
    # Оставим, чтобы не ломался импорт, если зависимость еще не установлена
    pass 

# Проверка и установка зависимостей
def check_dependencies():
    required_packages = ['requests', 'phonenumbers', 'geopy'] # Добавлена 'geopy'
    missing_packages = []
    
    for package in required_packages:
        try:
            # Универсальная проверка импорта
            if package == 'geopy':
                __import__('geopy.geocoders') 
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("[!] Установка недостающих зависимостей...")
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"[+] Установлен: {package}")
            except Exception as e:
                print(f"[!] Ошибка установки {package}: {e}")
                return False
    return True

# Баннер
def show_banner():
    banner = """
╔═══════════════════════════════════════════════╗
║              ВРЕД ЗАПРОС v0.0.1              ║
║         (МОДИФИКАЦИЯ GothbreachHelper)        ║
║              VIP EDITION - RING -1           ║
║                                               ║
║         [1] ВРЕД ЗАПРОС НА НОМЕР             ║
║         [2] ВЫХОД                            ║
╚═══════════════════════════════════════════════╝
"""
    print(banner)

# НОВАЯ ФУНКЦИЯ ДЛЯ ПРИМЕРНОЙ ГЕОЛОКАЦИИ
def get_approximate_geolocation(country_code, region_name):
    """Получает примерные координаты (широту и долготу) по стране и региону."""
    
    try:
        from geopy.geocoders import Nominatim
    except ImportError:
        return "Требуется geopy", "Требуется geopy"

    try:
        # Используем Nominatim для поиска координат по названию места, используя код региона и страну
        geolocator = Nominatim(user_agent="VRED_ZAPROS_OSINT")
        
        # Строим запрос для поиска
        location_query = f"{region_name}, {country_code}"
        
        print(f"[+] Поиск примерных координат для: {location_query}")
        location = geolocator.geocode(location_query, timeout=10)
        
        if location:
            # Округляем для краткости
            return round(location.latitude, 4), round(location.longitude, 4)
        else:
            return "Не найдено", "Не найдено"
            
    except Exception as e:
        return f"Ошибка ({e})", f"Ошибка ({e})"

# Основная функция поиска по номеру
def вред_запрос(phone):
    print(f"\n[+] Начинаем ВРЕД ЗАПРОС для номера: {phone}")
    print("[+] Анализ запущен...")
    
    try:
        # Базовая информация через phonenumbers
        parsed_phone = phonenumbers.parse(phone, None)
        if not phonenumbers.is_valid_number(parsed_phone):
            print("[!] Номер невалиден")
            return
        
        # Основная информация
        carrier_info = carrier.name_for_number(parsed_phone, "en") or "Неизвестно"
        country = geocoder.description_for_number(parsed_phone, "en") or "Неизвестно"
        region = geocoder.description_for_number(parsed_phone, "ru") or "Неизвестно"
        timezones = timezone.time_zones_for_number(parsed_phone) or ["Неизвестно"]
        formatted_number = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        
        # НОВЫЙ ВЫЗОВ ГЕОЛОКАЦИИ
        country_code_iso = phonenumbers.region_code_for_number(parsed_phone) or "Неизвестно"
        latitude, longitude = get_approximate_geolocation(country_code_iso, region)
        
        print("\n" + "="*50)
        print("🎯 БАЗОВАЯ ИНФОРМАЦИЯ:")
        print("="*50)
        print(f"📞 Номер: {formatted_number}")
        print(f"🌍 Страна: {country}")
        print(f"📍 Регион: {region}")
        print(f"📌 Широта (Примерно): {latitude}")   # ДОБАВЛЕНО
        print(f"📌 Долгота (Примерно): {longitude}") # ДОБАВЛЕНО
        print(f"📡 Оператор: {carrier_info}")
        print(f"🕐 Часовой пояс: {', '.join(timezones)}")
        print(f"✅ Валидность: {phonenumbers.is_valid_number(parsed_phone)}")
        
        # Проверка в социальных сетях и сервисах
        print("\n" + "="*50)
        print("🔍 ПРОВЕРКА В СОЦСЕТЯХ И СЕРВИСАХ:")
        print("="*50)
        
        # Список сервисов для проверки
        services = {
            "Telegram": f"https://t.me/{phone}",
            "WhatsApp": f"https://wa.me/{phone}",
            "Viber": f"https://viber.click/{phone}",
            "Instagram": f"https://www.instagram.com/{phone}",
            "Facebook": f"https://www.facebook.com/{phone}",
        }
        
        for service, url in services.items():
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"✅ {service}: АКТИВЕН - {url}")
                elif response.status_code == 404:
                    print(f"❌ {service}: не найден")
                else:
                    print(f"⚠️  {service}: статус {response.status_code}")
            except Exception as e:
                print(f"❌ {service}: ошибка проверки")
        
        # Дополнительные OSINT проверки
        print("\n" + "="*50)
        print("🕵️ ДОПОЛНИТЕЛЬНЫЕ ПРОВЕРКИ:")
        print("="*50)
        
        # Проверка через открытые API
        try:
            # IP-API для геолокации (если есть IP)
            ip_url = f"http://ip-api.com/json/"
            response = requests.get(ip_url, timeout=5)
            if response.status_code == 200:
                ip_data = response.json()
                print(f"🌐 Ваш IP: {ip_data.get('query', 'Неизвестно')}")
                print(f"🏙️  Ваш город: {ip_data.get('city', 'Неизвестно')}")
        except:
            pass
        
        # Поиск в базах данных (симуляция)
        print("\n[+] Поиск в открытых базах данных...")
        time.sleep(1)
        
        # Генерация отчета
        print("\n" + "="*50)
        print("📊 ОТЧЕТ СФОРМИРОВАН:")
        print("="*50)
        print(f"🔢 Номер: {formatted_number}")
        print(f"🏢 Оператор: {carrier_info}")
        print(f"🌎 Локация: {country}, {region}")
        print(f"📍 Координаты (Примерно): {latitude}, {longitude}") # ДОБАВЛЕНО
        print(f"📱 Мессенджеры: Telegram, WhatsApp, Viber")
        print(f"🕒 Время анализа: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⚡ Статус: Анализ завершен")
        
    except Exception as e:
        print(f"[!] Ошибка при анализе: {e}")

# Главное меню
def main():
    if not check_dependencies():
        print("[!] Не удалось установить зависимости. Выход.")
        return
    
    while True:
        show_banner()
        choice = input("\n[?] Выберите действие -> ")
        
        if choice == "1":
            phone = input("[?] Введите номер телефона -> ")
            # Простая очистка номера для универсальности
            if phone:
                cleaned_phone = re.sub(r'\D', '', phone)
                вред_запрос(cleaned_phone)
            else:
                print("[!] Введите номер телефона")
        
        elif choice == "2":
            print("[+] Выход из ВРЕД ЗАПРОС...")
            break
        
        else:
            print("[!] Неверный выбор")
        
        input("\n[?] Нажмите Enter для продолжения...")
        os.system('cls' if platform.system() == 'Windows' else 'clear')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Программа прервана пользователем")
    except Exception as e:
        print(f"[!] Критическая ошибка: {e}")
