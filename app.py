import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re

st.set_page_config(page_title="HealthScan AI", layout="centered")

# --- Инициализация на OCR ---
# При първото стартиране ще отнеме малко време, за да изтегли моделите (около 100-200MB)
@st.cache_resource
def load_ocr():
    # Задаваме български и английски език
    return easyocr.Reader(['bg', 'en'], gpu=False)

reader = load_ocr()

# --- БАЗА ДАННИ ---
BAD_INGREDIENTS = {
    "аспартам": "Изкуствен подсладител; потенциални метаболитни проблеми.",
    "палмово масло": "Високо съдържание на наситени мазнини.",
    "глутамат": "Мононатриев глутамат; може да причини главоболие.",
    "глюкозо-фруктозен сироп": "Свързва се със затлъстяване и диабет.",
    "е120": "Кармин (оцветител); възможни алергии.",
    "е171": "Титанов диоксид; забранен в ЕС.",
    "хидрогенирани": "Трансмазнини; риск от сърдечни заболявания.",
    "нитрит": "Консервант, потенциално канцерогенен.",
    "aspartame": "Artificial sweetener; metabolic concerns.",
    "palm oil": "High saturated fats.",
    "msg": "Flavor enhancer; can cause headaches."
}

def analyze_text(results):
    """Анализира резултатите от EasyOCR."""
    found_bad = {}
    # EasyOCR връща списък от кортежи (координати, текст, увереност)
    full_text = " ".join([res[1].lower() for res in results])
    
    for ing, desc in BAD_INGREDIENTS.items():
        if ing in full_text:
            found_bad[ing] = desc
    return found_bad, full_text

# --- ИНТЕРФЕЙС ---
st.title("🍎 Скенер за съставки")
st.write("Снимай етикета и аз ще потърся вредни добавки.")

uploaded_file = st.file_uploader("Качи снимка...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Качено изображение", use_container_width=True)
    
    if st.button("Анализирай"):
        with st.spinner("Изкуственият интелект чете етикета..."):
            # Превръщаме снимката във формат, който EasyOCR разбира
            img_array = np.array(image)
            
            # Извличане на текст
            ocr_results = reader.readtext(img_array)
            
            bad_stuff, raw_text = analyze_text(ocr_results)
            
            st.divider()
            
            if bad_stuff:
                st.error(f"⚠️ Открити са {len(bad_stuff)} проблемни съставки:")
                for name, info in bad_stuff.items():
                    st.warning(f"**{name.upper()}**: {info}")
            else:
                st.success("✅ Не открих нищо притеснително в нашия списък.")
            
            with st.expander("Виж разчетения текст"):
                st.write(raw_text)

st.markdown("---")
st.caption("Програмата използва EasyOCR за разпознаване на текст.")
