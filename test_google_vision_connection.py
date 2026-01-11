#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Cloud Vision API Baglanti Testi
Bu script Google Cloud credentials'in dogru kurulup kurulmadigini test eder.
"""

import os
import sys

def test_google_vision_connection():
    """Google Cloud Vision API baglantisini test eder"""
    
    print("=" * 80)
    print("GOOGLE CLOUD VISION API BAGLANTI TESTI")
    print("=" * 80)
    print()
    
    # 1. Environment variable kontrolu
    print("[1/3] Environment variable kontrolu...")
    cred_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    
    if not cred_path:
        print("[HATA] GOOGLE_APPLICATION_CREDENTIALS environment variable tanimli degil!")
        print()
        print("Cozum (PowerShell):")
        print('  $env:GOOGLE_APPLICATION_CREDENTIALS="d:\\KuranTaskent\\google-credentials.json"')
        print()
        return False
    
    print(f"[OK] Credentials path: {cred_path}")
    
    # 2. Credentials dosyasi var mi?
    print()
    print("[2/3] Credentials dosyasi kontrolu...")
    
    if not os.path.exists(cred_path):
        print(f"[HATA] Credentials dosyasi bulunamadi: {cred_path}")
        print()
        print("Google Cloud Console'dan service account key (JSON) indirin")
        return False
    
    print(f"[OK] Credentials dosyasi mevcut")
    
    # 3. Google Cloud Vision kutuphanesi yuklu mu?
    print()
    print("[3/3] Google Cloud Vision kutuphane testi...")
    
    try:
        from google.cloud import vision
        print("[OK] google-cloud-vision kutuphane yuklu")
    except ImportError:
        print("[HATA] google-cloud-vision kutuphane yuklu degil!")
        print()
        print("Cozum:")
        print("  pip install google-cloud-vision")
        print()
        return False
    
    # 4. API baglantisi testi
    print()
    print("[BONUS] API baglanti testi...")
    
    try:
        client = vision.ImageAnnotatorClient()
        print("[OK] Vision API client basariyla olusturuldu!")
        
        # Service account bilgisini goster
        import json
        with open(cred_path, 'r') as f:
            cred_data = json.load(f)
            service_account = cred_data.get('client_email', 'Bilinmiyor')
            project_id = cred_data.get('project_id', 'Bilinmiyor')
        
        print(f"[OK] Service Account: {service_account}")
        print(f"[OK] Project ID: {project_id}")
        
    except Exception as e:
        print(f"[UYARI] API client olusturulamadi: {e}")
        print("Bu genellikle API'nin henuz enable edilmedigini gosterir.")
        print("Google Cloud Console -> APIs & Services -> Library -> Cloud Vision API -> Enable")
        return False
    
    # Basarili!
    print()
    print("=" * 80)
    print("[BASARILI] Google Cloud Vision API hazir!")
    print("=" * 80)
    print()
    print("Bir sonraki adim: Tek sayfa OCR testi")
    print("  python ocr_google_vision.py --page 3")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = test_google_vision_connection()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[HATA] Beklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
