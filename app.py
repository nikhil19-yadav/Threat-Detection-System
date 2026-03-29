import streamlit as st
import pandas as pd
import cv2

from bluetooth_scanner import scan_ble_sync
from wifi_scanner import scan_wifi
from drone_detector import start_camera, stop_camera, process_frame

st.set_page_config(page_title="Threat Detection System", layout="wide")

st.title("🛡️ Surrounding Threat Detection System")

# =========================
# 🔵 BLUETOOTH
# =========================
st.subheader("🔵 Bluetooth / BLE Devices")

if st.button("Scan BLE Devices"):
    try:
        devices = scan_ble_sync()

        if devices:
            df = pd.DataFrame(devices)

            df.rename(columns={
                "name": "Device Name",
                "address": "MAC Address",
                "rssi": "Signal Strength"
            }, inplace=True)

            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No Bluetooth devices found")

    except Exception as e:
        st.error(f"Bluetooth Error: {e}")

# =========================
# 📶 WIFI
# =========================
st.subheader("📶 Wi-Fi Networks")

if st.button("Scan Wi-Fi"):
    try:
        networks = scan_wifi()

        if networks:
            df = pd.DataFrame(networks)

            df.rename(columns={
                "ssid": "Network Name",
                "signal": "Signal Strength",
                "auth": "Security"
            }, inplace=True)

            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No Wi-Fi networks found")

    except Exception as e:
        st.error(f"WiFi Error: {e}")

# =========================
# 🚁 DRONE DETECTION
# =========================
st.subheader("🚁 Drone / Object Detection")

if "camera_on" not in st.session_state:
    st.session_state.camera_on = False

col1, col2 = st.columns(2)

with col1:
    if st.button("Start Camera Detection"):
        st.session_state.camera_on = True
        start_camera()

with col2:
    if st.button("Stop Camera Detection"):
        st.session_state.camera_on = False
        stop_camera()

frame_placeholder = st.empty()

if st.session_state.camera_on:
    frame = process_frame()

    if frame is not None:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame)
    else:
        st.error("Camera not accessible ❌")