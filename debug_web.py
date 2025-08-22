#!/usr/bin/env python3
"""Debug script to test the web interface and translations"""

import requests
from bs4 import BeautifulSoup

def test_web_translations():
    """Test translations on the live website"""
    base_url = "http://localhost:5001"
    
    print("🌐 Testing live website translations...")
    
    try:
        # Test homepage
        print(f"\n📱 Testing homepage: {base_url}")
        response = requests.get(base_url, timeout=5)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract key elements
            title = soup.find('title')
            h1 = soup.find('h1')
            nav_links = soup.find_all('a', href=lambda x: x and any(route in x for route in ['/week', '/month']))
            
            print(f"✅ Status: {response.status_code}")
            print(f"✅ Title: {title.text if title else 'Not found'}")
            print(f"✅ H1: {h1.text if h1 else 'Not found'}")
            
            # Check if Thai text is present
            if title and 'ห้องปฏิบัติการ' in title.text:
                print("✅ Thai text detected in title")
            else:
                print("❌ No Thai text in title - translation issue?")
            
            # Check navigation
            for link in nav_links[:3]:
                print(f"✅ Nav link: {link.text.strip()}")
            
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        print("💡 Make sure the server is running: python3 run.py")

def test_language_switching():
    """Test language switching functionality"""
    base_url = "http://localhost:5001"
    
    print(f"\n🔀 Testing language switching...")
    
    languages = ['th', 'de', 'en']
    session = requests.Session()
    
    for lang in languages:
        print(f"\n🌐 Testing {lang.upper()}:")
        
        try:
            # Set language
            switch_url = f"{base_url}/set-language/{lang}"
            response = session.get(switch_url, allow_redirects=True, timeout=5)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('title')
                
                expected_titles = {
                    'th': 'ห้องปฏิบัติการพัทยา',
                    'de': 'Labor Pattaya',
                    'en': 'Laboratory Pattaya'
                }
                
                actual_title = title.text if title else 'No title'
                expected_title = expected_titles.get(lang, 'Unknown')
                
                print(f"   Title: {actual_title}")
                
                if expected_title in actual_title:
                    print(f"   ✅ Correct {lang.upper()} translation")
                else:
                    print(f"   ❌ Expected '{expected_title}', got '{actual_title}'")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error: {e}")

def test_qr_endpoints():
    """Test QR code endpoints"""
    base_url = "http://localhost:5001"
    
    print(f"\n📱 Testing QR code endpoints...")
    
    endpoints = [
        ('/qr', 'image/png'),
        ('/qr.svg', 'image/svg+xml')
    ]
    
    for endpoint, expected_type in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                size = len(response.content)
                
                print(f"✅ {endpoint}: {response.status_code}, {content_type}, {size} bytes")
                
                if expected_type not in content_type:
                    print(f"   ❌ Expected {expected_type}, got {content_type}")
            else:
                print(f"❌ {endpoint}: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint}: {e}")

if __name__ == "__main__":
    print("🧪 QR-Info-Portal Web Interface Tests")
    print("=" * 50)
    
    test_web_translations()
    test_language_switching()
    test_qr_endpoints()
    
    print("\n✅ Web tests completed!")