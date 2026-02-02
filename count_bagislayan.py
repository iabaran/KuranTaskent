import io

def count_word(file_path, word):
    try:
        with io.open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return content.count(word)
    except Exception as e:
        return str(e)

file_path = 'd:/KuranTaskent/quran_tr_js.js'
target_word = u'Ba\u011f\u0131\u015flayan' # Bağışlayan

count = count_word(file_path, target_word)
print(f"Count of '{target_word}': {count}")
