import streamlit as st
import os
from PIL import Image
import piexif
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="LocalBoost", page_icon="📍", layout="wide")

st.title("📍 LocalBoost - Otimização Google Meu Negócio")

st.sidebar.image("assets/logo.png", width=200)
st.sidebar.header("Configurações")

# Informações do cliente
with st.sidebar:
    company_name = st.text_input("🧑‍💼 Nome da Empresa")
    address = st.text_input("📍 Endereço Completo")
    latitude = st.text_input("🗺️ Latitude")
    longitude = st.text_input("🗺️ Longitude")

st.subheader("🖼️ Upload de Imagens para Otimização")
uploaded_files = st.file_uploader(
    "Selecione as imagens", type=["jpg", "jpeg"], accept_multiple_files=True
)

if uploaded_files and latitude and longitude:
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    for uploaded_file in uploaded_files:
        img = Image.open(uploaded_file)

        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

        # Inserindo dados de geolocalização
        lat = float(latitude)
        lon = float(longitude)

        def deg_to_dmsRational(deg_float):
            min_float = deg_float % 1 * 60
            sec_float = min_float % 1 * 60
            deg = int(deg_float)
            min = int(min_float)
            sec = int(sec_float * 100)
            return ((deg, 1), (min, 1), (sec, 100))

        gps_ifd = {
            piexif.GPSIFD.GPSLatitudeRef: "S" if lat < 0 else "N",
            piexif.GPSIFD.GPSLatitude: deg_to_dmsRational(abs(lat)),
            piexif.GPSIFD.GPSLongitudeRef: "W" if lon < 0 else "E",
            piexif.GPSIFD.GPSLongitude: deg_to_dmsRational(abs(lon)),
        }

        exif_dict["GPS"] = gps_ifd
        exif_bytes = piexif.dump(exif_dict)

        # Renomeia a imagem
        filename = (
            f"{company_name.replace(' ', '-')}_{uploaded_file.name}".lower()
        )
        save_path = os.path.join(output_dir, filename)

        img.save(save_path, "jpeg", exif=exif_bytes)

        st.success(f"✅ {filename} otimizada e salva!")

    st.info("📥 Imagens processadas estão na pasta 'output' (faça o download manual).")

elif uploaded_files:
    st.warning("⚠️ Preencha latitude e longitude para aplicar geolocalização.")

st.markdown("---")
st.subheader("📍 Como usar:")
st.markdown(
    """
1. Preencha os dados da empresa (nome, endereço, latitude e longitude).
2. Faça o upload das imagens.
3. As imagens serão otimizadas, georreferenciadas e renomeadas.
4. Utilize essas imagens no Google Meu Negócio para melhorar sua posição no mapa!
"""
)
