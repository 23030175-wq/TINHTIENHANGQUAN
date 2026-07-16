import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Order Nhà Hàng & Admin", layout="wide")

# Khởi tạo dữ liệu mẫu cho Admin (Lịch sử đơn hàng đã thanh toán)
if 'history_orders' not in st.session_state:
    st.session_state.history_orders = []

if 'order_dict' not in st.session_state:
    st.session_state.order_dict = {}

# Danh sách 20 bàn của nhà hàng
danh_sach_ban = [f"Bàn {i}" for i in range(1, 21)]

# Thực đơn
menu = {
    "Đồ ăn": {
        "Pizza Hải Sản": 150000, "Mì Ý Bò Bằm": 95000, "Burger Gà": 65000,
        "Salad Trộn": 50000, "Bít tết Bò Mỹ": 250000, "Sườn nướng BBQ": 180000,
        "Cánh gà chiên mắm": 75000,"Lẩu cá diêu hồng":200000, "Lẩu Thái hải sản": 300000, "Lẩu Thái nấm chay": 200000
    },
    "Thức uống": {
        "Coca Cola": 20000, "Trà Đào Cam Sả": 35000, "Cà Phê Sữa": 25000,
        "Nước Suối": 10000, "Sinh tố Bơ": 45000, "Nước ép cam": 40000,"Trà đào hạt chia": 50000,
        "Mojito chanh dây": 55000, "Bia Heineken": 30000, "Bia Tiger": 30000
    }
}

# --- THANH ĐIỀU HƯỚNG (NAVIGATION BAR / SIDEBAR) ---
st.sidebar.title("🏨 MENU HỆ THỐNG")
page = st.sidebar.radio("Chọn trang quản lý:", ["🛒 Trang Gọi Món (Khách Hàng)", "🔐 Trang Quản Trị (Admin)"])

# =================================================================
# 1. GIAO DIỆN TRANG ORDER (KHÁCH HÀNG)
# =================================================================
if page == "🛒 Trang Gọi Món (Khách Hàng)":
    st.title("🍽️ Hệ thống Order Nhà Hàng MR. TUYỀN - Giảm 50% cho hoá đơn trên 1 triệu")
    
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("Chọn Món & Số Bàn")
        
        selected_table = st.selectbox("Chọn số bàn:", danh_sach_ban)
        st.write("---")
        
        category = st.selectbox("Chọn loại:", list(menu.keys()))
        item = st.selectbox("Chọn món:", list(menu[category].keys()))
        quantity = st.number_input("Số lượng:", min_value=1, step=1, value=1)
        
        note = st.text_input("Ghi chú cho món này (Ví dụ: Không cay, ít đá...):", value="")
        
        if st.button("Thêm vào giỏ"):
            price = menu[category][item]
            item_display_name = f"{item} ({note})" if note.strip() != "" else item
            
            if item_display_name in st.session_state.order_dict:
                st.session
