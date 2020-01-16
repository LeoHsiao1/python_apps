from PIL import Image
from imagehash import phash


h1 = phash(Image.open(r"c:\Users\Leo\Desktop\pic_test\QQ截图.jpg"))
h2 = phash(Image.open(r"c:\Users\Leo\Desktop\pic_test\加了两个水印.jpg"))

1 - (h1 - h2) / 64  # 相似度

