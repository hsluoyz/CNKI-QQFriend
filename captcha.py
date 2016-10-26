# coding=gbk

import os
import shutil
from PIL import Image
import subprocess

captcha_folder = os.path.abspath('.') + '\\captcha\\'


def preprocess(src_file, dst_file):
    im = Image.open(captcha_folder + src_file)
    imgry = im.convert('L')

    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(1)
        else:
            table.append(0)

    out = imgry.point(table, '1')

    width, height = out.size
    print "the captcha image size = (%d, %d)" % (width, height)
    out = out.crop((2, 2, width - 2, height - 2))

    out.save(captcha_folder + dst_file)
    print "preprocess completed, output = " + captcha_folder + dst_file


def solve(filename):
    p = subprocess.Popen(['C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe', captcha_folder + filename, captcha_folder + 'result'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)

    print "**********************************************"
    print p.stdout.readline(),

    fp = open(captcha_folder + 'result.txt', 'r')
    result = fp.read()
    print "OCR result = " + result
    return result


def do_delete():
    if os.path.exists(captcha_folder):
        print "delete folder = " + captcha_folder.decode('gbk')
        shutil.rmtree(captcha_folder)
    else:
        print "folder doesn't exist, no need to delete, folder = " + document_folder.decode('gbk')


if __name__ == '__main__':
    preprocess('verifycode.jpg', 'verifycode1.jpg')
    solve('verifycode1.jpg')
    # do_delete()
