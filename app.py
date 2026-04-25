import streamlit as st
from PIL import Image
import pytesseract
import re

# Конфигурация на Tesseract (ако си на Windows, посочи пътя до .exe файла)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Примерна база данни с "вредни" съставки
BAD_INGREDIENTS = {
    "aspartame": "Изкуствен подсладител, потенциално вреден за метаболизма.",
    "palm oil": "Високо съдържание на наситени мазнини, екологични проблеми.",
    "msg": "Мононатриев глутамат - може да причини главоболие при някои хора.",
    "high fructose corn syrup": "Свързва се със затлъстяване и диабет.",
    "e120": "Кармин - оцветител, който може да предизвика алергии.",
    "sodium nitrite": "Консервант, използван в месата, потенциално канцерогенен.",
    "trans fats": "Повишават нивата на лошия холестерол."
}

def analyze_text(text):
    text = text.lower()
    found_bad = {}
    
    for ing, desc in BAD_INGREDIENTS.items():
        if re.search(r'\b' + re.escape(ing) + r'\b', text):
            found_bad[ing] = desc
            
    return found_bad

# Streamlit Интерфейс
st.title("🔍 Анализатор на съставки")
st.write("Качете снимка на етикета със съставките, за да проверите за вредни добавки.")

uploaded_file = st.file_uploader("Изберете снимка...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Качена снимка', use_column_width=True)
    
    with st.spinner('Анализиране на текста...'):
        # Извличане на текст от снимката
        extracted_text = pytesseract.image_to_string(image, lang='eng+bul') # Поддържа английски и български
        
        st.subheader("Извлечен текст:")
        st.text(extracted_text)
        
        # Анализ
        results = analyze_text(extracted_text)
        
        st.divider()
        
        if results:
            st.error(f"Внимание! Открити са {len(results)} потенциално вредни съставки:")
            for ing, desc in results.items():
                st.warning(f"**{ing.upper()}**: {desc}")
        else:
            st.success("Не са открити известни вредни съставки в нашата база данни.")

st.info("Забележка: Тази програма е с образователна цел. Винаги се консултирайте със специалист при специфични диетични нужди.")
