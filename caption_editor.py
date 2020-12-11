import streamlit as st
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os
from io import BytesIO
import base64

imagetypes = ['png', ' jpg', 'JPG', 'JPEG']
options = ['Top','Bottom',]
colors = ['Red', 'Green', 'Blue', 'Yellow','Orange','Purple','Pink','Teal','White','Black','Magenta','Gray','Lime','Dark Green','Olive','Maroon','Navy Blue','Coral','Gold','Indigo']
color_map = {
    'Green':(0,255,0),
    'Red': (255,0,0),
    'Blue':(0,0,255),
    'Yellow':(255,255,0),
    'Orange':(255,153,51),
    'Purple':(153,51,255),
    'Pink':(255,102,255),
    'Teal':(0,153,153),
    'White':(255,255,255),
    'Black':(0,0,0),
    'Magenta':(255,51,153),
    'Gray':(192,192,192),
    'Lime': (128,255,0),
    'Dark Green': (0,153,0),
    'Olive': (128,128,0),
    'Maroon': (128,0,0),
    'Navy Blue': (0,0,128),
    'Coral': (255,127,80),
    'Gold': (255,215,0),
    'Indigo': (75,0,130)
}
# To Do: write condition to make caption top/bottom (take consideration of image and caption size. Based on these, set top or bottom; find out how to draw colored rectangle on image using pillow)

st.title('Image Caption Editor')
st.text('by Arkin')

def add_caption(image_bytes, caption_pos, caption_size, caption_text, selected_color, text_color):
    img = Image.open(image_bytes)
    # Creating a rectangle
    w = img.width
    h = caption_size + 40
    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('Optima.ttc',caption_size - 40)
    tw,th = d.textsize(caption_text, font=fnt)
    if caption_pos == "Top":
        shape = [(0,0),(w,h)]
        d.rectangle(shape, fill = color_map[selected_color])
        text_coord = ((w - tw)/2,10)
    elif caption_pos == "Bottom":
        shape = [(0,img.height - h),(w, img.height)]
        d.rectangle(shape, fill = color_map[selected_color])
        text_coord = ((w-tw)/2,img.height - h+10)
    d.text(text_coord, align='center', text = caption_text,fill = color_map[text_color], font=fnt)
    return img 
def save_image(img):
    b = BytesIO()
    if img.mode == 'RGB':
        img.save(b, format = 'jpeg')
        imgstr = base64.b64encode(b.getvalue()).decode()
        href = f'<a href = "data:file/jpg:;base64,{imgstr}" download = "img.jpg">Download Image</a>'
    if img.mode == 'RGBA':
        img.save(b, format = 'png')
        imgstr = base64.b64encode(b.getvalue()).decode()
        href = f'<a href = "data:file/png:;base64,{imgstr}" download = "img.png">Download Image</a>'
    return href
    

file = st.file_uploader(label = 'Upload Images',type = imagetypes)
if file:
    imgbox = st.empty()
    imgbox.image(file.read(),use_column_width=True)    
    caption_pos = st.sidebar.selectbox('Select a position for caption', options)
    caption_size = st.sidebar.slider('Caption Size', min_value = 45, max_value = 300)
    selected_color = st.sidebar.select_slider('Select Color of Box', colors)
    text_color = st.sidebar.selectbox('Select Color of Text', colors)
    caption_text = st.sidebar.text_area("Write your caption here:", height = 5)
    apply_btn = st.sidebar.button('Apply')





    if apply_btn and caption_text:
        img = add_caption(file, caption_pos, caption_size, caption_text, selected_color, text_color)
        imgbox.image(img, caption = 'edited', use_column_width = True)
        st.success('Task Completed')
        st.markdown(save_image(img),True)
    else:
        st.error('Please provide a caption')

        

    

# Add colors and test for errors/bugs