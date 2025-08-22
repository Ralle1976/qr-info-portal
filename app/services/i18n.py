from typing import Dict, Optional
from flask import request, session
import json
import os


class I18nService:
    """Simple internationalization service"""
    
    SUPPORTED_LANGUAGES = ['th', 'de', 'en']
    DEFAULT_LANGUAGE = 'th'
    
    translations = {}
    
    @classmethod
    def load_translations(cls):
        """Load translation files"""
        translations_dir = os.path.join(os.path.dirname(__file__), '..', 'translations')
        
        for lang in cls.SUPPORTED_LANGUAGES:
            file_path = os.path.join(translations_dir, f'{lang}.json')
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    cls.translations[lang] = json.load(f)
            else:
                cls.translations[lang] = {}
    
    @classmethod
    def get_current_language(cls) -> str:
        """Get current language from session or request"""
        # Check session first
        if 'language' in session:
            return session['language']
        
        # Check Accept-Language header
        if request:
            best_match = request.accept_languages.best_match(cls.SUPPORTED_LANGUAGES)
            if best_match:
                return best_match
        
        return cls.DEFAULT_LANGUAGE
    
    @classmethod
    def set_language(cls, language: str):
        """Set language in session"""
        if language in cls.SUPPORTED_LANGUAGES:
            session['language'] = language
    
    @classmethod
    def translate(cls, key: str, language: Optional[str] = None, **kwargs) -> str:
        """Translate a key to current or specified language"""
        if not cls.translations:
            cls.load_translations()
        
        lang = language or cls.get_current_language()
        
        # Try to get translation
        translation = cls.translations.get(lang, {}).get(key)
        
        # Fallback to default language
        if not translation and lang != cls.DEFAULT_LANGUAGE:
            translation = cls.translations.get(cls.DEFAULT_LANGUAGE, {}).get(key)
        
        # Fallback to key itself
        if not translation:
            translation = key
        
        # Format with parameters if any
        if kwargs:
            try:
                translation = translation.format(**kwargs)
            except:
                pass
        
        return translation
    
    @classmethod
    def get_translations_for_language(cls, language: str) -> Dict:
        """Get all translations for a language"""
        if not cls.translations:
            cls.load_translations()
        
        return cls.translations.get(language, {})


# Convenience function for templates
def t(key: str, **kwargs) -> str:
    """Template helper for translations"""
    return I18nService.translate(key, **kwargs)