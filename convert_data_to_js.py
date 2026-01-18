import json
import os

def convert_json_to_js(json_path, js_path, var_name):
    print(f"Converting {json_path} to {js_path} (var: {var_name})...")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        js_content = f"const {var_name} = {json.dumps(data, ensure_ascii=False)};"
        
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
            
        print("Success.")
    except Exception as e:
        print(f"Error: {e}")

convert_json_to_js('quran_arabic.json', 'quran_arabic_js.js', 'GLOBAL_QURAN_ARABIC')
convert_json_to_js('quran_data/quran_tr.json', 'quran_tr_js.js', 'GLOBAL_QURAN_TR')
