import streamlit as st
import qrcode
from PIL import Image


def generate_qr_code(data):
    # Создаем QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        border=0,
        box_size=1
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Преобразуем в изображение
    image = qr.make_image(fill_color="black", back_color="white")

    return image


def recurse_qr(inner, outer, scale_factor=1):
    # Меняем размер внутренного QR, чтобы совпадал с размером внешнего
    ratio = (outer.width * scale_factor) / inner.width
    inner = resize(inner, ratio) 

    # Задаем размеры и создаем рекурсивный QR
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
    upscaled_image = image.resize((int(image.width * scale_factor), int(image.height * scale_factor)))

    return upscaled_image


def main():
    st.title("Recursive QR Generator")
    
    # Ввод данных для кодов
    data_inner = st.text_input("Data for inner QR:")
    data_outer = st.text_input("Data for outer QR:")

    # Множитель разрешения изображений
    resolution = st.slider("Image scale", min_value=1, max_value=10, value=1, step=1)

    white_color = st.color_picker('Pick a color', '#ffffff')
    black_color = st.color_picker('Pick a color', '#000000')
    
    if st.button("Generate"):
        # Генерируем внутренний QR
        inner = generate_qr_code(data_inner)

        # Генерируем внешний QR
        outer = generate_qr_code(data_outer)

        # Комбинируем внешний и внутренний коды в одну картинку
        recursive = recurse_qr(inner, outer, resolution)
        pixels = recursive.getdata()

        # Заменяем белые пиксели на выбранный цвет
        rgb_color = tuple(int(white_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        new_pixels = [rgb_color if pixel == (255, 255, 255) else pixel for pixel in pixels]
        recursive.putdata(new_pixels)

        # Заменяем черные пиксели на выбранный цвет
        rgb_color = tuple(int(black_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        new_pixels = [rgb_color if pixel == (0, 0, 0) else pixel for pixel in pixels]
        recursive.putdata(new_pixels)

        # Отображаем
        st.markdown("Result")
        st.image(recursive, use_column_width=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("## Inner QR")
            st.image(resize(inner, 10), use_column_width=True)
        with col2:
            st.markdown("## Outer QR")
            st.image(resize(outer, 10), use_column_width=True)
        

if __name__ == "__main__":
    main()
