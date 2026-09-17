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
        """بحث عن كلمة مفتاحية أو سؤال داخل مواد القرار"""
        results = []
        lines = self.full_text.split('\n')
        for line in lines:
            if keyword.strip() and keyword.strip() in line:
                results.append(line)
        return results

# مسار ملف القرار
PDF_FILENAME = "قرار 151 - الحلقة الابتدائية (1).pdf"

@st.cache_resource
def load_decree_system():
    return DecreeQASystem(PDF_FILENAME)

decree_system = load_decree_system()

# تصميم واجهة المستخدم
st.title("📚 نظام الاستعلام الآلي - القرار الوزاري رقم (151)")
st.markdown("نظام تفاعلي للبحث في مواد وأحكام القرار الوزاري الخاص بنظام الدراسة والتقييم للحلقة الابتدائية.")

if not decree_system.full_text:
    st.error(f"⚠️ تنبيه: لم يتم العثور على ملف PDF باسم ({PDF_FILENAME}) في المجلد. تأكد من رفعه بجانب هذا الملف على مستودع GitHub.")
else:
    query = st.text_input("🔍 اطرح سؤالاً أو اكتب كلمة مفتاحية للبحث (مثال: الحضور، درجات، التقييم الأسبوعي، التربية الدينية):")
    
    if query:
        matches = decree_system.search_decree(query)
        st.subheader(f"نتائج البحث عن: ({query})")
        
        if matches:
            st.success(f"تم العثور على {len(matches)} نتيجة مطابقة:")
            for idx, match in enumerate(matches, 1):
                st.info(f"{idx}. {match}")
        else:
            st.warning("لم يتم العثور على نتائج مطابقة لهذا البحث. جرب كلمة أخرى (مثل: الغياب، النجاح، الدور الثاني).")
            
    with st.expander("📖 عرض النص الكامل للقرار الوزاري المستخرج"):
        st.text_area("نص القرار", decree_system.full_text, height=300)
