import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="نظام إدارة البقالة", page_icon="🛒", layout="centered")

# تصميم CSS مخصص لتجميل الواجهة
st.markdown("""
    <style>
    .stApp {
        background-color: #f7f9fc;
    }
    .main-header {
        font-size: 24px;
        color: #1E3A8A;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🛒 نظام نقاط البيع والمخزون - البقالة</div>', unsafe_allow_html=True)

# قاعدة بيانات المخزون والأصناف الافتراضية
if 'inventory' not in st.session_state:
    st.session_state.inventory = {
        "ماء (صغير)": {"price": 0.100, "stock": 50},
        "بيبسي / غازيات": {"price": 0.250, "stock": 30},
        "حليب طازج": {"price": 0.500, "stock": 20},
        "شيبس كويتي": {"price": 0.200, "stock": 40},
        "بسكويت شوكولاتة": {"price": 0.150, "stock": 25},
        "بطاقة تعبئة زين": {"price": 5.000, "stock": 10},
        "بطاقة تعبئة اس تي سي": {"price": 5.000, "stock": 10},
        "دخان مالبورو": {"price": 1.750, "stock": 15}
    }

if 'sales_history' not in st.session_state:
    st.session_state.sales_history = []

# القوائم الجانبية أو التبويبات الرئيسية
tab1, tab2, tab3 = st.tabs(["💰 شاشة البيع (الكاشير)", "📦 إدارة المخزون", "📊 تقارير المبيعات"])

with tab1:
    st.subheader("إتمام عملية بيع جديدة")
    
    # اختيار الصنف والكمية
    item_list = list(st.session_state.inventory.keys())
    selected_item = st.selectbox("اختر المنتج:", item_list)
    
    current_stock = st.session_state.inventory[selected_item]["stock"]
    item_price = st.session_state.inventory[selected_item]["price"]
    
    st.info(isinstance(current_stock, int) and f"السعر: {item_price} د.ك | المخزون المتوفر: {current_stock} حبة" or "")
    
    quantity = st.number_input("الكمية المباعة:", min_value=1, max_value=max(1, current_stock), value=1)
    
    if st.button("إتمام البيع وسحب من المخزون"):
        if current_stock >= quantity:
            st.session_state.inventory[selected_item]["stock"] -= quantity
            total_price = quantity * item_price
            
            # تسجيل الفاتورة
            sale_record = {
                "التاريخ والوقت": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "المنتج": selected_item,
                "الكمية": quantity,
                "الإجمالي (د.ك)": total_price
            }
            st.session_state.sales_history.append(sale_record)
            st.success(f"تم بيع {quantity}x {selected_item} بنجاح! الإجمالي: {total_price:.3f} د.ك")
        else:
            st.error("عذراً، الكمية المطلوبة غير متوفرة بالمخزون!")

with tab2:
    st.subheader("إدارة المنتجات والمخزون")
    
    # عرض المخزون الحالي كجدول
    inv_data = []
    for k, v in st.session_state.inventory.items():
        inv_data.append({"المنتج": k, "السعر (د.ك)": v["price"], "المخزون": v["stock"]})
    
    st.table(pd.DataFrame(inv_data))
    
    st.markdown("---")
    st.subheader("إضافة صنف جديد للبقالة")
    new_name = st.text_input("اسم المنتج الجديد:")
    new_price = st.number_input("سعر البيع (د.ك):", min_value=0.01, value=0.250)
    new_stock = st.number_input("الكمية الأولية بالمخزون:", min_value=1, value=20)
    
    if st.button("إضافة الصنف للقائمة"):
        if new_name and new_name not in st.session_state.inventory:
            st.session_state.inventory[new_name] = {"price": new_price, "stock": new_stock}
            st.success(f"تم إضافة المنتج '{new_name}' بنجاح!")
            st.rerun()
        elif new_name in st.session_state.inventory:
            st.warning("هذا المنتج موجود مسبقاً!")

with tab3:
    st.subheader("سجل مبيعات اليوم")
    if len(st.session_state.sales_history) > 0:
        df_sales = pd.DataFrame(st.session_state.sales_history)
        st.dataframe(df_sales, use_container_width=True)
        
        total_revenue = df_sales["الإجمالي (د.ك)"].sum()
        st.metric(label="إجمالي المبيعات", value=f"{total_revenue:.3f} د.ك")
    else:
        st.info("لا توجد مبيعات مسجلة حتى الآن اليوم.")
