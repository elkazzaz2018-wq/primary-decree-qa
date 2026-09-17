import os
import pypdf
import streamlit as st

# إعداد صفحة الويب
st.set_page_config(
    page_title="مساعد القرار الوزاري 151",
    page_icon="📚",
    layout="wide"
)

class DecreeQASystem:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.full_text = self._extract_text_from_pdf()
        
    def _extract_text_from_pdf(self):
        """استخراج النصوص من ملف القرار الوزاري PDF"""
        if not os.path.exists(self.pdf_path):
            return ""
        reader = pypdf.PdfReader(self.pdf_path)
        extracted_text = ""
        for i, page in enumerate(reader.pages):
            extracted_text += f"\n--- صفحة {i+1} ---\n" + (page.extract_text() or "")
        return extracted_text

    def search_decree(self, keyword):
        """بحث مرن عن كلمة أو جزء من الكلمة داخل مواد القرار مع توحيد الحروف"""
        results = []
        
        def normalize(text):
            # توحيد أشكال الهمزات والتاء المربوطة والهاء لتسهيل البحث التطابقي
            return (text.replace('أ', 'ا')
                        .replace('إ', 'ا')
                        .replace('آ', 'ا')
                        .replace('ة', 'ه')
                        .replace('ى', 'ي'))
        
        normalized_keyword = normalize(keyword.strip())
        lines = self.full_text.split('\n')
        
        for line in lines:
            if normalized_keyword and normalized_keyword in normalize(line):
                results.append(line.strip())
        return results

# مسار ملف القرار (يجب أن يكون مطابقاً لاسم الملف المرفوع في المستودع)
PDF_FILENAME = "قرار 151 - الحلقة الابتدائية (1).pdf"

@st.cache_resource
def load_decree_system():
    return DecreeQASystem(PDF_FILENAME)

decree_system = load_decree_system()

# تصميم واجهة المستخدم
st.title("📚 نظام الاستعلام الآلي - القرار الوزاري رقم (151)")
st.markdown("نظام تفاعلي للبحث في مواد وأحكام القرار الوزاري الخاص بنظام الدراسة والتقييم للحلقة الابتدائية (2026/2027)[cite: 1].")

if not decree_system.full_text:
    st.error(f"⚠️ تنبيه: لم يتم العثور على ملف PDF باسم ({PDF_FILENAME}) في المجلد. تأكد من رفعه بجانب هذا الملف على مستودع GitHub.")
else:
    query = st.text_input("🔍 اطرح سؤالاً أو اكتب كلمة للبحث (مثال: الحضور، درجات، التقييم، التربية، 60):")
    
    if query:
        matches = decree_system.search_decree(query)
        st.subheader(f"نتائج البحث عن: ({query})")
        
        if matches:
            st.success(f"تم العثور على {len(matches)} نتيجة مطابقة:")
            for idx, match in enumerate(matches, 1):
                st.info(f"{idx}. {match}")
        else:
            st.warning("لم يتم العثور على نتائج مطابقة لهذا البحث. جرب كلمات أبسط (مثل: حضور، نجاح، دور).")
            
    with st.expander("📖 عرض النص الكامل للقرار الوزاري المستخرج"):
        st.text_area("نص القرار", decree_system.full_text, height=300)
