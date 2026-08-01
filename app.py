import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

st.set_page_config(page_title="نظام البقالة الشامل", page_icon="🛒", layout="centered")

# --- القواميس الخاصة باللغات ---
LANGUAGES = {
    "العربية": {
        "login_title": "تسجيل دخول النظام",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "login_btn": "دخول",
        "login_err": "اسم المستخدم أو كلمة المرور غير صحيحة",
        "logout": "تسجيل الخروج",
        "welcome": "مرحباً بك",
        "tab1": "💰 شاشة البيع (الكاشير)",
        "tab2": "📦 إدارة المخزون والأرباح",
        "tab3": "📊 تقارير المبيعات",
        "select_cat": "اختر فئة المنتج:",
        "select_item": "اختر المنتج:",
        "price": "السعر",
        "cost": "التكلفة",
        "stock": "المخزون المتوفر",
        "qty": "الكمية المباعة:",
        "sell_btn": "إتمام البيع وسحب المخزون",
        "success_sell": "تم البيع بنجاح! الإجمالي",
        "error_stock": "عذراً، الكمية غير متوفرة!",
        "add_item": "إضافة صنف جديد",
        "item_name": "اسم المنتج:",
        "item_cat": "الفئة الرئيسية:",
        "sell_price": "سعر البيع (د.ك):",
        "cost_price": "سعر الشراء/التكلفة (د.ك):",
        "initial_stock": "الكمية الأولية:",
        "add_btn": "إضافة الصنف",
        "net_profit": "صافي الربح",
        "daily": "المبيعات اليومية",
        "weekly": "المبيعات الأسبوعية",
        "monthly": "المبيعات الشهرية",
        "yearly": "المبيعات السنوية"
    },
    "English": {
        "login_title": "System Login",
        "username": "Username",
        "password": "Password",
        "login_btn": "Login",
        "login_err": "Invalid Username or Password",
        "logout": "Logout",
        "welcome": "Welcome",
        "tab1": "💰 POS (Cashier)",
        "tab2": "📦 Inventory & Profits",
        "tab3": "📊 Sales Reports",
        "select_cat": "Select Category:",
        "select_item": "Select Product:",
        "price": "Price",
        "cost": "Cost",
        "stock": "Available Stock",
        "qty": "Quantity Sold:",
        "sell_btn": "Complete Sale",
        "success_sell": "Sold successfully! Total",
        "error_stock": "Sorry, insufficient stock!",
        "add_item": "Add New Product",
        "item_name": "Product Name:",
        "item_cat": "Category:",
        "sell_price": "Selling Price (KD):",
        "cost_price": "Cost Price (KD):",
        "initial_stock": "Initial Stock:",
        "add_btn": "Add Product",
        "net_profit": "Net Profit",
        "daily": "Daily Sales",
        "weekly": "Weekly Sales",
        "monthly": "Monthly Sales",
        "yearly": "Yearly Sales"
    },
    "বাংলা": {
        "login_title": "সিস্টেম লগইন",
        "username": "ব্যবহারকারী নাম",
        "password": "পাসওয়ার্ড",
        "login_btn": "লগইন",
        "login_err": "ভুল ইউজারনেম বা পাসওয়ার্ড",
        "logout": "লগআউট",
        "welcome": "স্বাগতম",
        "tab1": "💰 ক্যাশিয়ার",
        "tab2": "📦 ইনভেন্টরি",
        "tab3": "📊 বিক্রয় রিপোর্ট",
        "select_cat": "বিভাগ নির্বাচন করুন:",
        "select_item": "পণ্য নির্বাচন করুন:",
        "price": "মূল্য",
        "cost": "ক্রয়মূল্য",
        "stock": "মজুদ",
        "qty": "পরিমাণ:",
        "sell_btn": "বিক্রি সম্পন্ন করুন",
        "success_sell": "সফলভাবে বিক্রি হয়েছে! মোট",
        "error_stock": "পর্যাপ্ত মজুদ নেই!",
        "add_item": "নতুন পণ্য যোগ করুন",
        "item_name": "পণ্যের নাম:",
        "item_cat": "বিভাগ:",
        "sell_price": "বিক্রয়মূল্য:",
        "cost_price": "ক্রয়মূল্য:",
        "initial_stock": "প্রাথমিক মজুদ:",
        "add_btn": "পণ্য যোগ করুন",
        "net_profit": "নিট লাভ",
        "daily": "দৈনিক বিক্রি",
        "weekly": "সাপ্তাহিক বিক্রি",
        "monthly": "মাসিক বিক্রি",
        "yearly": "বার্ষিক বিক্রি"
    },
    "اردو": {
        "login_title": "سسٹم لاگ ان",
        "username": "صارف کا نام",
        "password": "پاس ورڈ",
        "login_btn": "لاگ ان",
        "login_err": "غلط نام یا پاس ورڈ",
        "logout": "لاگ آؤٹ",
        "welcome": "خوش آمدید",
        "tab1": "💰 کیشئر (فروخت)",
        "tab2": "📦 انوینٹری اور منافع",
        "tab3": "📊 سیلز رپورٹس",
        "select_cat": "زمرہ منتخب کریں:",
        "select_item": "مصنوعات منتخب کریں:",
        "price": "قیمت",
        "cost": "لاگت",
        "stock": "موجودہ اسٹاک",
        "qty": "مقدار:",
        "sell_btn": "فروخت مکمل کریں",
        "success_sell": "کامیابی سے فروخت ہو گیا! کل",
        "error_stock": "اسٹاک ناکافی ہے!",
        "add_item": "نیا پروڈکٹ شامل کریں",
        "item_name": "پروڈکٹ کا نام:",
        "item_cat": "زمرہ:",
        "sell_price": "فروخت کی قیمت:",
        "cost_price": "خرید کی قیمت:",
        "initial_stock": "ابتدائی اسٹاک:",
        "add_btn": "پروڈکٹ شامل کریں",
        "net_profit": "خالص منافع",
        "daily": "روزانہ فروخت",
        "weekly": "ہفتہ وار فروخت",
        "monthly": "ماہانہ فروخت",
        "yearly": "سالانہ فروخت"
    },
    "हिन्दी": {
        "login_title": "सिस्टम लॉगिन",
        "username": "उपयोगकर्ता नाम",
        "password": "पासवर्ड",
        "login_btn": "लॉगिन",
        "login_err": "गलत उपयोगकर्ता नाम या पासवर्ड",
        "logout": "लॉग आउट",
        "welcome": "स्वागत है",
        "tab1": "💰 कैशियर",
        "tab2": "📦 इन्वेंट्री",
        "tab3": "📊 बिक्री रिपोर्ट",
        "select_cat": "श्रेणी चुनें:",
        "select_item": "उत्पाद चुनें:",
        "price": "कीमत",
        "cost": "लागत",
        "stock": "स्टॉक",
        "qty": "मात्रा:",
        "sell_btn": "बिक्री पूरी करें",
        "success_sell": "सफलतापूर्वक बेचा गया! कुल",
        "error_stock": "स्टॉक पर्याप्त नहीं है!",
        "add_item": "नया उत्पाद जोड़ें",
        "item_name": "उत्पाद का नाम:",
        "item_cat": "श्रेणी:",
        "sell_price": "विक्री मूल्य:",
        "cost_price": "लागत मूल्य:",
        "initial_stock": "प्रारंभिक स्टॉक:",
        "add_btn": "उत्पाद जोड़ें",
        "net_profit": "शुद्ध लाभ",
        "daily": "दैनिक बिक्री",
        "weekly": "साप्ताहिक बिक्री",
        "monthly": "मासिक बिक्री",
        "yearly": "वार्षिक बिक्री"
    }
}

# --- إعدادات اللغات في الشريط الجانبي ---
with st.sidebar:
    selected_lang = st.selectbox("🌐 Choose Language / اختر اللغة", list(LANGUAGES.keys()))
    t = LANGUAGES[selected_lang]
    st.markdown("---")

# --- إدارة المستخدمين (قاعدة بيانات خفيفة للمستخدمين) ---
USERS = {
    "admin": "1234",
    "cashier1": "1111",
    "abu_fahad": "2026"
}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.markdown(f"<h2 style='text-align: center;'>{t['login_title']}</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        u_input = st.text_input(t['username'])
        p_input = st.text_input(t['password'], type="password")
        if st.button(t['login_btn']):
            if u_input in USERS and USERS[u_input] == p_input:
                st.session_state.logged_in = True
                st.session_state.username = u_input
                st.rerun()
            else:
                st.error(t['login_err'])
    st.stop()

# زر تسجيل الخروج في الشريط الجانبي
with st.sidebar:
    st.write(f"{t['welcome']}: **{st.session_state.username}**")
    if st.button(t['logout']):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# --- ملفات الحفظ الدائم ---
INV_FILE = "inventory_v2.json"
SALES_FILE = "sales_v2.json"

def load_data():
    if os.path.exists(INV_FILE):
        with open(INV_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "حلويات وسكاكر": {
                "سنيكرز": {"price": 0.250, "cost": 0.150, "stock": 40},
                "جالكسي": {"price": 0.300, "cost": 0.180, "stock": 30}
            },
            "مشروبات وعصائر": {
                "ماء (صغير)": {"price": 0.100, "cost": 0.050, "stock": 100},
                "بيبسي / غازيات": {"price": 0.250, "cost": 0.150, "stock": 50}
            },
            "بطاقات اتصال": {
                "بطاقة زين 5دك": {"price": 5.000, "cost": 4.750, "stock": 15},
                "بطاقة اس تي سي 5دك": {"price": 5.000, "cost": 4.750, "stock": 15}
            }
        }

def save_data(inv):
    with open(INV_FILE, "w", encoding="utf-8") as f:
        json.dump(inv, f, ensure_ascii=False, indent=4)

def load_sales():
    if os.path.exists(SALES_FILE):
        with open(SALES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def save_sales(sales):
    with open(SALES_FILE, "w", encoding="utf-8") as f:
        json.dump(sales, f, ensure_ascii=False, indent=4)

if 'inventory' not in st.session_state:
    st.session_state.inventory = load_data()

if 'sales_history' not in st.session_state:
    st.session_state.sales_history = load_sales()

# --- واجهة التطبيق الرئيسية ---
st.markdown(f"<h3 style='text-align: center; color: #1E3A8A;'>🛒 نظام إدارة البقالة الذكي</h3>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([t['tab1'], t['tab2'], t['tab3']])

# 1. شاشة البيع (التصنيف الفرعي + الأرباح)
with tab1:
    st.subheader(t['tab1'])
    
    categories = list(st.session_state.inventory.keys())
    selected_cat = st.selectbox(t['select_cat'], categories)
    
    items_in_cat = list(st.session_state.inventory[selected_cat].keys())
    if items_in_cat:
        selected_item = st.selectbox(t['select_item'], items_in_cat)
        
        item_info = st.session_state.inventory[selected_cat][selected_item]
        price = item_info["price"]
        cost = item_info["cost"]
        stock = item_info["stock"]
        
        st.info(f"{t['price']}: {price} د.ك | {t['cost']}: {cost} د.ك | {t['stock']}: {stock}")
        
        qty = st.number_input(t['qty'], min_value=1, max_value=max(1, stock), value=1)
        
        if st.button(t['sell_btn']):
            if stock >= qty:
                st.session_state.inventory[selected_cat][selected_item]["stock"] -= qty
                total_price = qty * price
                total_cost = qty * cost
                profit = total_price - total_cost
                
                sale_record = {
                    "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "category": selected_cat,
                    "item": selected_item,
                    "qty": qty,
                    "total_price": total_price,
                    "total_cost": total_cost,
                    "profit": profit,
                    "cashier": st.session_state.username
                }
                st.session_state.sales_history.append(sale_record)
                save_data(st.session_state.inventory)
                save_sales(st.session_state.sales_history)
                
                st.success(f"{t['success_sell']}: {total_price:.3f} د.ك | {t['net_profit']}: {profit:.3f} د.ك")
                st.rerun()
            else:
                st.error(t['error_stock'])
    else:
        st.warning("لا توجد منتجات في هذا القسم حالياً.")

# 2. إدارة المخزون وإدخال التكلفة
with tab2:
    st.subheader(t['tab2'])
    
    flat_inv = []
    for cat, items in st.session_state.inventory.items():
        for itm, dat in items.items():
            flat_inv.append({
                "الفئة": cat,
                "المنتج": itm,
                "سعر البيع (د.ك)": dat["price"],
                "سعر التكلفة (د.ك)": dat["cost"],
                "المخزون": dat["stock"]
            })
    st.table(pd.DataFrame(flat_inv))
    
    st.markdown("---")
    st.subheader(t['add_item'])
    
    new_cat = st.text_input(t['item_cat'], value="عام")
    new_name = st.text_input(t['item_name'])
    new_price = st.number_input(t['sell_price'], min_value=0.001, value=0.250, format="%.3f")
    new_cost = st.number_input(t['cost_price'], min_value=0.000, value=0.150, format="%.3f")
    new_stock = st.number_input(t['initial_stock'], min_value=1, value=20)
    
    if st.button(t['add_btn']):
        if new_name:
            if new_cat not in st.session_state.inventory:
                st.session_state.inventory[new_cat] = {}
            st.session_state.inventory[new_cat][new_name] = {
                "price": new_price,
                "cost": new_cost,
                "stock": new_stock
            }
            save_data(st.session_state.inventory)
            st.success("تم إضافة المنتج وتحديد التكلفة بنجاح!")
            st.rerun()

# 3. تقارير المبيعات (يومي، أسبوعي، شهري، سنوي + صافي الربح)
with tab3:
    st.subheader(t['tab3'])
    
    if len(st.session_state.sales_history) > 0:
        df = pd.DataFrame(st.session_state.sales_history)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df['Date'] = df['datetime'].dt.date
        
        report_type = st.radio("اختر نطاق التقرير:", [t['daily'], t['weekly'], t['monthly'], t['yearly']])
        
        now = datetime.now()
        if report_type == t['daily']:
            filtered_df = df[df['datetime'].dt.date == now.date()]
        elif report_type == t['weekly']:
            filtered_df = df[df['datetime'] >= (now - pd.Timedelta(days=7))]
        elif report_type == t['monthly']:
            filtered_df = df[(df['datetime'].dt.month == now.month) & (df['datetime'].dt.year == now.year)]
        else:
            filtered_df = df[df['datetime'].dt.year == now.year]
            
        if not filtered_df.empty:
            st.dataframe(filtered_df[['datetime', 'category', 'item', 'qty', 'total_price', 'profit', 'cashier']], use_container_width=True)
            
            tot_rev = filtered_df['total_price'].sum()
            tot_profit = filtered_df['profit'].sum()
            
            col_a, col_b = st.columns(2)
            col_a.metric("إجمالي المبيعات", f"{tot_rev:.3f} د.ك")
            col_b.metric("صافي الربح الإجمالي", f"{tot_profit:.3f} د.ك")
        else:
            st.info("لا توجد مبيعات مسجلة في هذا النطاق الزمني.")
    else:
        st.info("لا توجد مبيعات مسجلة حتى الآن.")
