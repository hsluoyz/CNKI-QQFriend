# coding=utf-8

from subprocess import Popen, PIPE
import re


def get_filename(line):
    # line = "Download success (J:\\github_repos\\CNKI-QQFriend\\seek201512039.pdf) "
    print "the line is: " + line
    pattern_filename = "([^\\\\]*)\\)"
    regex_filename = re.compile(pattern_filename)
    res = regex_filename.findall(line)
    print "the regex result is: " + str(res)
    return str(res[0])

def get_output(p, line_no):
    for i in range(0, line_no):
        print p.stdout.readline(),

def input_command(p, str_input):
    print >> p.stdin, str_input
    p.stdin.flush()
    print "[Input]: " + str_input

def download_document():
    p = Popen(["cnki-downloader.exe"], stdin=PIPE, stdout=PIPE, bufsize=1)

    print "**********************************************"
    get_output(p, 13)
    input_command(p, "中德两国高中生数学能力的分析及比较")

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

print "file name: " + download_document()

