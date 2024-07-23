import streamlit as st
from PIL import Image
import io

# Mapeamento dos formatos para serem usados pelo Pillow
format_mapping = {
    "JPEG": "JPEG",
    "PNG": "PNG",
    "BMP": "BMP",
    "TIFF": "TIFF",
    "GIF": "GIF",
    "WebP": "WEBP",
    "ICO": "ICO"
}

# Função para redimensionar e converter a imagem
def process_image(image, format, size=None):
    try:
        img = Image.open(image)
        if size:
            img = img.resize((size, size))
        if format == "JPEG" and img.mode == "RGBA":
            img = img.convert("RGB")
        buffer = io.BytesIO()
        img.save(buffer, format=format_mapping[format])
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error(f"Erro ao processar a imagem: {e}")
        return None

# Título do aplicativo
st.title("Conversor de Imagens")

# Upload da imagem
uploaded_file = st.file_uploader("Escolha uma imagem", type=["png", "jpg", "jpeg", "bmp", "tiff", "gif", "webp", "ico"])

# Opções de formato de conversão
format_option = st.selectbox(
    "Escolha o formato para converter",
    ("JPEG", "PNG", "BMP", "TIFF", "GIF", "WebP", "ICO")
)

# Caixa de seleção para manter o tamanho original
keep_original_size = st.checkbox("Manter tamanho original", value=True)

# Input para o tamanho da imagem, habilitado/desabilitado conforme a caixa de seleção
size = None
if not keep_original_size:
    size = st.number_input("Defina o tamanho (pixels)", min_value=1, value=100)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Imagem original")
    processed_image = process_image(uploaded_file, format_option, size)
    
    if processed_image:
        st.image(processed_image, caption="Imagem processada")

        # Botão para download da imagem convertida
        st.download_button(
            label="Baixar imagem convertida",
            data=processed_image,
            file_name=f"converted_image.{format_option.lower()}",
            mime=f"image/{format_option.lower()}"
        )
