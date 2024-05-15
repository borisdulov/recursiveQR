import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image


def generate_qr_code(data):
    # Создаем QR-код
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        border=0,
        box_size=1
    )
    qr.add_data(data)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")

    # # Сохраняем QR-код
    # image.save(result_path)

    # Возвращаем размер QR-кода
    return image


def recurse_qr(inner, outer, scale_factor=1):
    ratio = (outer.width * scale_factor) / inner.width
    inner = resize(inner, ratio) 

    outer_width, outer_height = outer.size
    new_width, new_height = outer_width ** 2 * scale_factor, outer_height ** 2 * scale_factor
    recursive = Image.new('RGB', (new_width, new_height))

    # Проходим по всем пикселям изображения
    for column in range(outer_width):
        for row in range(outer_height):
            # Получаем значение пикселя
            pixel = outer.getpixel((column, row))

            # Если пиксель белый, заменяем его
            if pixel == 255:
                recursive.paste(inner, 
                                (int(column * outer_width * scale_factor), 
                                 int(row * outer_height * scale_factor)))
    
    return recursive


def resize(image, scale_factor):
    # image = Image.open(image_path)
    upscaled_image = image.resize((int(image.width * scale_factor), int(image.height * scale_factor)))

    return upscaled_image


def main():
    st.title("Генератор рекурсивных QR-кодов")
    
    # Ввод данных для кодов
    data_inner = st.text_input("Введите данные для внутреннего QR-кода:")
    data_outer = st.text_input("Введите данные для внешнего QR-кода:")

    # Множитель разрешения изображений
    resolution = st.slider("Разрешение", min_value=1, max_value=10, value=1, step=1)
    
    if st.button("Сгенерировать"):
        # Генерируем внутренний QR
        inner = generate_qr_code(data_inner)

        # Генерируем внешний QR
        outer = generate_qr_code(data_outer)

        # Комбинируем внешний и внутренний коды в одну картинку
        recursive = recurse_qr(inner, outer, resolution)

        # Отображаем
        st.markdown("# Результат")
        st.image(recursive, use_column_width=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("## Внутренний")
            st.image(resize(inner, 10), use_column_width=True)
        with col2:
            st.markdown("## Внешний")
            st.image(resize(outer, 10), use_column_width=True)
        

if __name__ == "__main__":
    main()
