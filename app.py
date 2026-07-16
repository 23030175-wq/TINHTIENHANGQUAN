import streamlit as st
import pandas as pd
from datetime import datetime
import uuid  # <-- Thư viện tạo ID duy nhất cho mỗi đơn hàng để tránh lỗi Key trùng lặp

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
                st.session_state.order_dict[item_display_name]["Số lượng"] += quantity
                st.session_state.order_dict[item_display_name]["Thành tiền"] = (
                    st.session_state.order_dict[item_display_name]["Số lượng"] * price
                )
            else:
                st.session_state.order_dict[item_display_name] = {
                    "Tên món": item_display_name,
                    "Đơn giá": price,
                    "Số lượng": quantity,
                    "Thành tiền": price * quantity
                }
            st.success(f"Đã cập nhật {item_display_name} vào giỏ cho **{selected_table}**!")

    with col2:
        st.subheader(f"Giỏ hàng hiện tại của [{selected_table}]")
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
                    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    
                    # Tạo ID duy nhất cho mỗi hóa đơn mới gửi đi
                    unique_id = str(uuid.uuid4())[:8] # Lấy 8 ký tự đầu để định danh
                    
                    order_details = {
                        "id": unique_id,  # <-- Thêm id định danh độc nhất cho đơn
                        "Số bàn": selected_table,
                        "Thời gian đặt": now,
                        "Chi tiết đơn hàng": ", ".join([f"{v['Tên món']} (x{v['Số lượng']})" for v in st.session_state.order_dict.values()]),
                        "Tổng tiền (VNĐ)": tong_thanh_toan
                    }
                    st.session_state.history_orders.append(order_details)
                    st.success(f"🎉 Đặt món thành công cho {selected_table}!")
                    st.session_state.order_dict = {} 
                    st.rerun()
                    
            with col_btn2:
                if st.button("❌ Xóa giỏ hàng"):
                    st.session_state.order_dict = {}
                    st.rerun()
        else:
            st.info(f"Giỏ hàng của {selected_table} đang trống.")

# =================================================================
# 2. GIAO DIỆN TRANG ADMIN (BẢO MẬT BẰNG MẬT KHẨU)
# =================================================================
elif page == "🔐 Trang Quản Trị (Admin)":
    st.title("📊 Hệ thống Quản Lý & Admin - Nhóm Chủ Đề 2")
    
    password = st.text_input("Nhập mật khẩu Admin:", type="password")
    
    if password == "admin123":
        st.success("Đăng nhập quyền Admin thành công!")
        st.write("---")
        
        st.subheader("📈 Tổng quan doanh thu thực tế theo bàn")
        if st.session_state.history_orders:
            df_history = pd.DataFrame(st.session_state.history_orders)
            
            total_revenue = df_history["Tổng tiền (VNĐ)"].sum()
            total_orders = len(df_history)
            
            c1, c2 = st.columns(2)
            c1.metric("Tổng doanh thu nhận được", f"{total_revenue:,.0f} VNĐ")
            c2.metric("Tổng số đơn đã phục vụ", f"{total_orders} đơn")
            
            # Biểu đồ doanh thu theo bàn
            st.write("### 🧮 Thống kê doanh thu theo vị trí bàn:")
            df_table_revenue = df_history.groupby("Số bàn")["Tổng tiền (VNĐ)"].sum().reset_index()
            st.bar_chart(data=df_table_revenue, x="Số bàn", y="Tổng tiền (VNĐ)")
            
            # --- KHU VỰC XỬ LÝ XÓA ĐƠN LẺ ---
            st.write("### 📝 Danh sách quản lý & Xóa đơn hàng lẻ:")
            
            # Tạo header cho bảng tùy biến
            h_col1, h_col2, h_col3, h_col4, h_col5 = st.columns([1, 1.5, 4, 1.5, 1])
            h_col1.markdown("**Số bàn**")
            h_col2.markdown("**Thời gian**")
            h_col3.markdown("**Chi tiết đơn hàng**")
            h_col4.markdown("**Tổng tiền**")
            h_col5.markdown("**Thao tác**")
            st.write("---")
            
            # Khởi tạo một danh sách tạm thời để lưu các đơn cần xóa
            order_to_delete = None
            
            # Duyệt qua danh sách đơn hàng thực tế
            for order in st.session_state.history_orders:
                b_col1, b_col2, b_col3, b_col4, b_col5 = st.columns([1, 1.5, 4, 1.5, 1])
                
                b_col1.write(order["Số bàn"])
                b_col2.write(order["Thời gian đặt"])
                b_col3.write(order["Chi tiết đơn hàng"])
                b_col4.write(f"{order['Tổng tiền (VNĐ)']:,.0f} VNĐ")
                
                # Sử dụng "id" của đơn hàng làm key giúp giải quyết triệt để lỗi trùng lặp Widget hoặc lệch vị trí
                if b_col5.button("🗑️ Xóa", key=f"delete_{order['id']}"):
                    order_to_delete = order
            
            # Thực hiện hành động xóa an toàn bên ngoài vòng lặp vẽ UI
            if order_to_delete is not None:
                st.session_state.history_orders.remove(order_to_delete)
                st.success(f"Đã xóa đơn hàng thành công!")
                st.rerun()
            
            # Nút xóa tất cả
            st.write("---")
            if st.button("🚨 Xóa TOÀN BỘ lịch sử đơn hàng"):
                st.session_state.history_orders = []
                st.rerun()
        else:
            st.info("Chưa có đơn hàng nào được đặt từ các bàn.")
            
    elif password != "":
        st.error("❌ Sai mật khẩu! Vui lòng thử lại.")
