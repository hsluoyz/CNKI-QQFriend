# coding=utf-8

from subprocess import Popen, PIPE
import re
import os
import sys

def get_filename(line):
    # line = "Download success (J:\\github_repos\\CNKI-QQFriend\\seek201512039.pdf) "
    print "target line = " + line
    pattern_filename = "([^\\\\]*)\\)"
    regex_filename = re.compile(pattern_filename)
    res = regex_filename.findall(line)
    print "get_filename() regex result = " + str(res)
    return str(res[0])

def get_new_filename(old_file_name, new_document_name):
    # old_file_name = "seek201512039.pdf"
    print "old_file_name = " + old_file_name
    pattern_filename = ".*(\.[^\.]*)$"
    regex_filename = re.compile(pattern_filename)
    new_file_name = regex_filename.sub(new_document_name + "\\1", old_file_name)
    print "new_file_name = " + new_file_name
    return new_file_name

def get_output(p, line_no):
    for i in range(0, line_no):
        print p.stdout.readline(),

def input_command(p, str_input):
    print >> p.stdin, str_input
    p.stdin.flush()
    print "[Input]: " + str_input

def download_document(document_name):
    p = Popen(["cnki-downloader.exe"], stdin=PIPE, stdout=PIPE, bufsize=1)

    print "**********************************************"
    get_output(p, 13)
    input_command(p, document_name)

    print "**********************************************"
    get_output(p, 5)
    input_command(p, "1")

    print "**********************************************"
    get_output(p, 6)
    input_command(p, "1")

    print "**********************************************"
    get_output(p, 5)
    input_command(p, "1")

    print "**********************************************"
    for i in range(0, 30):
        line = p.stdout.readline()
        print line,
        if line.startswith("We got"):
            break
    input_command(p, "get 1")

    print "**********************************************"
    for i in range(0, 6):
        line = p.stdout.readline()
        print line,
        if line.startswith("Download success"):
            return get_filename(line)
    input_command(p, "1")

    print "**********************************************"
    print "End\n"

def do_download(document_name):
    old_filename = download_document(document_name)
    # old_filename = "seek201512039.pdf"
    new_filename = get_new_filename(old_filename, document_name)
    os.rename(old_filename, new_filename.decode("utf-8"))


def fileDir():
    path = sys.path[0]
    print(path)
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

def suffix(file, *suffixName):
    array = map(file.endswith, suffixName)
    if True in array:
        return True
    else:
        return False

def do_delete():
    targetDir = fileDir()
    for file in os.listdir(targetDir):
        targetFile = os.path.join(targetDir, file)
        if suffix(file, '.pdf', '.caj'):
            print "removed file = " + file.decode("gbk")
            os.remove(targetFile)

if __name__ == '__main__':
    do_delete()
    do_download("中德两国高中生数学能力的分析及比较")
    # do_download("德国职前教师教育质量保障体系改革新举措——基于莱比锡大学的分析")
