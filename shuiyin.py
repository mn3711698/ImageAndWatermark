
# -*- coding: utf-8 -*-
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import os


#生成内容为 TEXT 的水印
def text2img(text, font_color="Blue", font_size=25):
    font = ImageFont.truetype('simsun.ttc', font_size)
    #多行文字处理
    text = text.split('\n')
    mark_width = 0
    for  i in range(len(text)):
        (width, height) = font.getsize(text[i])
        if mark_width < width:
            mark_width = width
    mark_height = height * len(text)

    #生成水印图片
    mark = Image.new('RGBA', (mark_width,mark_height))
    draw = ImageDraw.ImageDraw(mark, "RGBA")
    draw.setfont(font)
    for i in range(len(text)):
        (width, height) = font.getsize(text[i])
        draw.text((0, i*height), text[i], fill=font_color)
    return mark

# 设置透明度
def set_opacity(im, opacity):
    assert opacity >=0 and opacity < 1
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

#添加水印
def watermark(im, mark, position, opacity=1):
    try:
        if opacity < 1:
            mark = set_opacity(mark, opacity)
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        if im.size[0] < mark.size[0] or im.size[1] < mark.size[1]:
            return False

        #设置水印位置
        if position == 'left_top':
            x = 0
            y = 0
        elif position == 'left_bottom':
            x = 0
            y = im.size[1] - mark.size[1]
        elif position == 'right_top':
            x = im.size[0] - mark.size[0]
            y = 0
        elif position == 'right_bottom':
            x = im.size[0] - mark.size[0]-100  #右下角有偏移
            y = im.size[1] - mark.size[1]-50
        else:
            x = (im.size[0] - mark.size[0]) / 2
            y = (im.size[1] - mark.size[1]) / 2

        layer = Image.new('RGBA', im.size,)
        layer.paste(mark,(x,y),mask=mark)
        return Image.composite(layer, im, layer)
    except Exception as e:
        print str(e)
        return False

def main(path_no_shuiyin,path_add_shuiyin):
#     im = Image.open('/Users/imac/Desktop/pngs/dst/1.jpg')
    im = Image.open(path_no_shuiyin)
    shuiyin_ljhy =Image.open('/Users/imac/Desktop/水印文件/shuiyin.jpg')
    
    image = watermark(im,shuiyin_ljhy ,'right_bottom', 0.9)
    if image:
        image.save(path_add_shuiyin)
    else:
        print "添加失败"


if __name__ == '__main__':
    main()
