import streamlit as st
import pandas as pd
from datetime import datetime  # <-- Bổ sung thư viện quản lý thời gian

st.set_page_config(page_title="Order Nhà Hàng & Admin", layout="wide")

# Khởi tạo dữ liệu mẫu cho Admin (Lịch sử đơn hàng đã thanh toán)
if 'history_orders' not in st.session_state:
    st.session_state.history_orders = []

if 'order_dict' not in st.session_state:
    st.session_state.order_dict = {}

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
        st.subheader("Chọn Món")
        category = st.selectbox("Chọn loại:", list(menu.keys()))
        item = st.selectbox("Chọn món:", list(menu[category].keys()))
        quantity = st.number_input("Số lượng:", min_value=1, step=1, value=1)
        
        if st.button("Thêm vào giỏ"):
            price = menu[category][item]
            if item in st.session_state.order_dict:
                st.session_state.order_dict[item]["Số lượng"] += quantity
                st.session_state.order_dict[item]["Thành tiền"] = (
                    st.session_state.order_dict[item]["Số lượng"] * price
                )
            else:
                st.session_state.order_dict[item] = {
                    "Tên món": item,
                    "Đơn giá": price,
                    "Số lượng": quantity,
                    "Thành tiền": price * quantity
                }
            st.success(f"Đã cập nhật {item} vào giỏ!")

    with col2:
        st.subheader("Giỏ hàng")
        if st.session_state.order_dict:
            df = pd.DataFrame.from_dict(st.session_state.order_dict, orient='index')
            st.table(df[["Tên món", "Đơn giá", "Số lượng", "Thành tiền"]])
            
            tam_tinh = df["Thành tiền"].sum()
            giam_gia = (tam_tinh * 0.5) if tam_tinh > 1000000 else 0
            
            if giam_gia > 0:
                st.info(f"🎉 Giảm 50% cho hóa đơn trên 1 triệu!")
            
            tong_thanh_toan = tam_tinh - giam_gia
            
            st.write(f"**Tạm tính:** {tam_tinh:,.0f} VNĐ")
            if giam_gia > 0:
                st.write(f"**Giảm giá (50%):** -{giam_gia:,.0f} VNĐ")
            st.metric(label="Tổng thanh toán", value=f"{tong_thanh_toan:,.0f} VNĐ")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🔥 Gửi Order / Thanh Toán"):
                    # Lấy thời gian hiện tại lúc khách bấm nút đặt hàng
                    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    
                    # Lưu đơn hàng kèm theo cột thời gian vào lịch sử cho Admin
                    order_details = {
                        "Thời gian đặt": now, # <-- Lưu thời gian vào đây
                        "Chi tiết đơn hàng": ", ".join([f"{v['Tên món']} (x{v['Số lượng']})" for v in st.session_state.order_dict.values()]),
                        "Tổng tiền (VNĐ)": tong_thanh_toan
                    }
                    st.session_state.history_orders.append(order_details)
                    st.success("🎉 Đặt món thành công! Bếp đang chuẩn bị...")
                    st.session_state.order_dict = {} # Xóa giỏ hàng sau khi đặt
                    st.rerun()
                    
            with col_btn2:
                if st.button("❌ Xóa giỏ hàng"):
                    st.session_state.order_dict = {}
                    st.rerun()
        else:
            st.info("Giỏ hàng đang trống.")

# =================================================================
# 2. GIAO DIỆN TRANG ADMIN (BẢO MẬT BẰNG MẬT KHẨU)
# =================================================================
elif page == "🔐 Trang Quản Trị (Admin)":
    st.title("📊 Hệ thống Quản Lý & Admin - Nhóm Chủ Đề 2")
    
    # Form đăng nhập đơn giản
    password = st.text_input("Nhập mật khẩu Admin:", type="password")
    
    if password == "admin123": # Mật khẩu đăng nhập Admin
        st.success("Đăng nhập quyền Admin thành công!")
        st.write("---")
        
        # Thống kê tổng quan
        st.subheader("📈 Tổng quan doanh thu thực tế")
        if st.session_state.history_orders:
            df_history = pd.DataFrame(st.session_state.history_orders)
            
            total_revenue = df_history["Tổng tiền (VNĐ)"].sum()
            total_orders = len(df_history)
            
            c1, c2 = st.columns(2)
            c1.metric("Tổng doanh thu nhận được", f"{total_revenue:,.0f} VNĐ")
            c2.metric("Tổng số đơn đã phục vụ", f"{total_orders} đơn")
            
            st.write("### 📝 Danh sách chi tiết các đơn hàng đã đặt:")
            # Định dạng hiển thị số tiền có dấu phẩy ngăn cách hàng nghìn trong bảng dataframe
            st.dataframe(
                df_history.style.format({"Tổng tiền (VNĐ)": "{:,.0f}"}), 
                use_container_width=True
            )
        else:
            st.info("Chưa có đơn hàng nào được đặt trong phiên làm việc này.")
            
    elif password != "":
        st.error("❌ Sai mật khẩu! Vui lòng thử lại.")
