import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

st.set_page_config(page_title="Order Nhà Hàng & Admin", layout="wide")

# Khởi tạo dữ liệu mẫu cho Admin (Lịch sử đơn hàng đã thanh toán)
if 'history_orders' not in st.session_state:
    st.session_state.history_orders = []

# Đổi order_dict thành list để quản lý các món trùng tên nhưng khác ghi chú dễ dàng hơn
if 'order_list' not in st.session_state:
    st.session_state.order_list = []

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
        
        # Ô nhập ghi chú riêng
        note = st.text_input("Ghi chú cho món này (Ví dụ: Không cay, ít đá...):", value="")
        
        if st.button("Thêm vào giỏ"):
            price = menu[category][item]
            
            # Kiểm tra xem món đó với ghi chú đó đã tồn tại trong giỏ chưa
            found = False
            for cart_item in st.session_state.order_list:
                if cart_item["Tên món"] == item and cart_item["Ghi chú"] == note.strip():
                    cart_item["Số lượng"] += quantity
                    cart_item["Thành tiền"] = cart_item["Số lượng"] * price
                    found = True
                    break
            
            if not found:
                st.session_state.order_list.append({
                    "Tên món": item,
                    "Đơn giá": price,
                    "Số lượng": quantity,
                    "Ghi chú": note.strip() if note.strip() != "" else "Không có",
                    "Thành tiền": price * quantity
                })
                
            st.success(f"Đã cập nhật {item} vào giỏ cho **{selected_table}**!")

    with col2:
        st.subheader(f"Giỏ hàng hiện tại của [{selected_table}]")
        if st.session_state.order_list:
            df = pd.DataFrame(st.session_state.order_list)
            # Hiển thị bảng giỏ hàng có cột Ghi chú rõ ràng cho khách xem
            st.table(df[["Tên món", "Đơn giá", "Số lượng", "Ghi chú", "Thành tiền"]])
            
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
                    unique_id = str(uuid.uuid4())[:8]
                    
                    # Tách riêng biệt Chi tiết món ăn và Toàn bộ ghi chú của đơn hàng
                    chi_tiet_mon = ", ".join([f"{v['Tên món']} (x{v['Số lượng']})" for v in st.session_state.order_list])
                    ghi_chu_tong = "; ".join([f"{v['Tên món']}: {v['Ghi chú']}" for v in st.session_state.order_list if v['Ghi chú'] != "Không có"])
                    
                    order_details = {
                        "id": unique_id,
                        "Số bàn": selected_table,
                        "Thời gian đặt": now,
                        "Chi tiết đơn hàng": chi_tiet_mon,
                        "Ghi chú từ khách": ghi_chu_tong if ghi_chu_tong != "" else "Không có ghi chú",
                        "Tổng tiền (VNĐ)": tong_thanh_toan
                    }
                    st.session_state.history_orders.append(order_details)
                    st.success(f"🎉 Đặt món thành công cho {selected_table}!")
                    st.session_state.order_list = [] 
                    st.rerun()
                    
            with col_btn2:
                if st.button("❌ Xóa giỏ hàng"):
                    st.session_state.order_list = []
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
            
            # Biểu đồ doanh thu
            st.write("### 🧮 Thống kê doanh thu theo vị trí bàn:")
            df_table_revenue = df_history.groupby("Số bàn")["Tổng tiền (VNĐ)"].sum().reset_index()
            st.bar_chart(data=df_table_revenue, x="Số bàn", y="Tổng tiền (VNĐ)")
            
            # --- KHU VỰC XỬ LÝ XÓA ĐƠN & XEM GHI CHÚ ---
            st.write("### 📝 Danh sách quản lý đơn hàng:")
            
            # Tăng số cột lên 6 cột để chèn riêng một cột lớn cho "Ghi chú"
            h_col1, h_col2, h_col3, h_col4, h_col5, h_col6 = st.columns([0.8, 1.2, 3.5, 2.5, 1.2, 0.8])
            h_col1.markdown("**Số bàn**")
            h_col2.markdown("**Thời gian**")
            h_col3.markdown("**Chi tiết đơn hàng**")
            h_col4.markdown("**📌 Ghi chú Admin**") # Cột xem ghi chú mới thêm
            h_col5.markdown("**Tổng tiền**")
            h_col6.markdown("**Thao tác**")
            st.write("---")
            
            order_to_delete = None
            
            for order in st.session_state.history_orders:
                b_col1, b_col2, b_col3, b_col4, b_col5, b_col6 = st.columns([0.8, 1.2, 3.5, 2.5, 1.2, 0.8])
                
                b_col1.write(order["Số bàn"])
                b_col2.write(order["Thời gian đặt"])
                b_col3.write(order["Chi tiết đơn hàng"])
                
                # Hiển thị dòng chữ ghi chú nổi bật (Nếu có ghi chú thì hiển thị màu cam/đỏ nhẹ để đầu bếp chú ý)
                if order["Ghi chú từ khách"] != "Không có ghi chú":
                    b_col4.warning(order["Ghi chú từ khách"])
                else:
                    b_col4.write(order["Ghi chú từ khách"])
                    
                b_col5.write(f"{order['Tổng tiền (VNĐ)']:,.0f} VNĐ")
                
                if b_col6.button("🗑️ Xóa", key=f"delete_{order['id']}"):
                    order_to_delete = order
            
            if order_to_delete is not None:
                st.session_state.history_orders.remove(order_to_delete)
                st.success(f"Đã xóa đơn hàng thành công!")
                st.rerun()
            
            st.write("---")
            if st.button("🚨 Xóa TOÀN BỘ lịch sử đơn hàng"):
                st.session_state.history_orders = []
                st.rerun()
        else:
            st.info("Chưa có đơn hàng nào được đặt từ các bàn.")
            
    elif password != "":
        st.error("❌ Sai mật khẩu! Vui lòng thử lại.")
