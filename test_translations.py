#!/usr/bin/env python3
"""Test script to verify translations are loading correctly"""

import sys
import os
import json
from pathlib import Path

# Add app to path
sys.path.append('.')

def test_translation_files():
    """Test if translation files exist and are valid JSON"""
    translations_dir = Path("app/translations")
    languages = ['th', 'de', 'en']
    
    print("🔍 Testing translation files...")
    
    for lang in languages:
        file_path = translations_dir / f"{lang}.json"
        print(f"\n📁 {lang}.json:")
        
        if not file_path.exists():
            print(f"   ❌ File not found: {file_path}")
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"   ✅ Valid JSON with {len(data)} keys")
            
            # Test key translations
            test_keys = ['site_title', 'today', 'open', 'closed', 'contact']
            for key in test_keys:
                if key in data:
                    print(f"   ✅ {key}: {data[key]}")
                else:
                    print(f"   ❌ Missing key: {key}")
                    
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON error: {e}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_i18n_service():
    """Test the I18nService directly"""
    print("\n\n🔧 Testing I18nService...")
    
    try:
        from app.services.i18n import I18nService, t
        
        # Force load translations
        I18nService.load_translations()
        
        print(f"✅ Default language: {I18nService.DEFAULT_LANGUAGE}")
        print(f"✅ Supported languages: {I18nService.SUPPORTED_LANGUAGES}")
        print(f"✅ Loaded translations: {list(I18nService.translations.keys())}")
        
        # Test translations for each language
        for lang in I18nService.SUPPORTED_LANGUAGES:
            print(f"\n🌐 Testing {lang.upper()} translations:")
            
            if lang in I18nService.translations:
                trans = I18nService.translations[lang]
                print(f"   Keys: {len(trans)}")
                
                # Test specific translations
                test_key = 'site_title'
                result = I18nService.translate(test_key, language=lang)
                print(f"   {test_key}: {result}")
                
                test_key = 'today'
                result = I18nService.translate(test_key, language=lang)
                print(f"   {test_key}: {result}")
            else:
                print(f"   ❌ No translations loaded for {lang}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Service error: {e}")

def test_flask_app():
    """Test translations in Flask app context"""
    print("\n\n🌐 Testing Flask app context...")
    
    try:
        from app import create_app
        
        app = create_app()
        
        with app.app_context():
            from app.services.i18n import t, I18nService
            
            print(f"✅ Current language: {I18nService.get_current_language()}")
            
            # Test template function
            result = t('site_title')
            print(f"✅ t('site_title'): {result}")
            
            result = t('today')
            print(f"✅ t('today'): {result}")
            
            result = t('contact')
            print(f"✅ t('contact'): {result}")
            
    except Exception as e:
        print(f"❌ Flask app error: {e}")

if __name__ == "__main__":
    print("🧪 QR-Info-Portal Translation Tests")
    print("=" * 50)
    
    test_translation_files()
    test_i18n_service()
    test_flask_app()
    
    print("\n\n✅ Tests completed!")