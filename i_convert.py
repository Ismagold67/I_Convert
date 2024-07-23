import streamlit as st
from PIL import Image
import io

# Redimensionar Imagem
def process_image(image, format, size):
    img = Image.open(image)
    if size:
        img = img.resize((size, size))
    buffer = io.BytesIO()
    img.save(buffer, format=format)
    buffer.seek(0)
    return buffer

# Título do aplicativo
st.title("Conversor de Imagens 📸")

# Upload da imagem
uploaded_file = st.file_uploader("Escolha uma imagem", type=["png", "jpg", "bmp", "tiff", "gif", "webp", "ico"])

# Opções de formato de conversão
format_option = st.selectbox(
    "Escolha o formato para converter",
    ("PNG","GIF","BMP")
)

# Caixa de seleção para manter o tamanho original
keep_original_size = st.checkbox("Manter tamanho original", value=True)
# Input para o tamanho da imagem
size = None
if not keep_original_size:
    size = st.number_input("Defina o tamanho (pixels)", min_value=1, value=100)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Imagem original")
    processed_image = process_image(uploaded_file, format_option, size)
    st.image(processed_image, caption="Imagem processada")

    # Botão para download da imagem convertida
    st.download_button(
        label="Baixar imagem convertida",
        data=processed_image,
        file_name=f"converted_image.{format_option.lower()}",
        mime=f"image/{format_option.lower()}"
    )
