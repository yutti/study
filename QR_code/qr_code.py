import os
import csv
import pandas as pd
import qrcode
import PySimpleGUI as sg
from PIL import Image, ImageDraw, ImageFont
import cv2

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def qr_generator(number,name,url):
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=9,
        border=4,
    )
    qr.add_data(url)  # url
 #   qr.add_data('Hello!' + number) # url
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert('L')

#   画像の高さチェック  
    im_height = img.height
    if im_height <= 300:
        but_margin , draw_h = 50,  250
    elif im_height > 300 and im_height <= 350:
        but_margin , draw_h = 83,  283
    elif im_height > 350 and im_height <= 400:
        but_margin , draw_h = 117,  317
    else:
        but_margin , draw_h = 150, 350

    img_add = add_margin(img, -15, -15, but_margin, -15, '#ffffff')   
    draw = ImageDraw.Draw(img_add)

    font_path = 'C:\Windows\Fonts\meiryo.ttc'           # Windowsのフォントファイルへのパス  
    font = ImageFont.truetype(font_path, 20)
    num = number

    draw.text((15, draw_h), str(name), font=font, fill='#000000')      
    img_add.save('./my_qr_code/' + number + '.png', quality=95)

def select_csv():
    sg.change_look_and_feel('Light Blue 2')
    layout = [[sg.Text('Data'),
               sg.InputText('(file path)', key='filepath'),
               sg.FilesBrowse('Select a file', target='filepath',
                              file_types=(('csv file', '.csv'),))],
              [sg.Submit(), sg.Cancel()]
              
              ]
    window = sg.Window('Charting', layout)
    while True:
        event, values = window.read()
        if event in ('Cancel', sg.WIN_CLOSED):
            return None
        if event == 'Submit':
            break
    window.close()
    filepath = values.get('filepath')
    if filepath == '(file path)':
        filepath = None

    return filepath

def main():
    # Check the folder for qr codes
    new_path = "my_qr_code"#フォルダ名
    if not os.path.exists(new_path):#ディレクトリ有無確認
        os.mkdir(new_path)
    # get urls
    csv_path = select_csv()
    print(csv_path)
    if csv_path is None:
        return

    # get urls   
    df = pd.read_csv(csv_path)
#    df = pd.read_csv('C:/Users/1ban2/OneDrive/デスクトップ/python/QR_code/url.csv')
    df_name = df['name']
    df_url = df['url']    
    # make QR code
    for number in range(int(len(df))):
        qr_generator(str(10000+number),df_name[number],df_url[number])  
   

if __name__ == '__main__':
    main()