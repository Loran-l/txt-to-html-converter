###########################################################
#                txt-to-html-page
###########################################################
import argparse
import os
import sys
from collections import deque

encode = "utf-8"
lang = "en"
title = "filename"
tabDepth = 0
versionNum = 0.1
styleURL = None
destDir = './dist/'

cloTagQ = deque()  # store closing tags


def o_tag(tag, space="", params_str=None, close_tag=False):
    '''
    Takes tag, generates closing tag, to be used with cloTag function
    Allows to use one-liner tags, like <link href=params_str> if close_tag is set to True

    :param tag: "html tag value"
    :param space: amount of whitespace
    :param params_str: integ parameters, like [name="viewport" content="width=device-width, initial-scale=1"]
    :param close_tag: if this tag can close itself, and does not need separate closing tag, set to TRUE
    :return: opening teg with some optional parameters
    '''

    tag_line = space + "<" + tag
    if params_str:
        tag_line += params_str
    if close_tag is False:
        global cloTagQ
        cloTagQ.append(space + "</"+ tag + ">")
        return tag_line
    return tag_line + ">"


def clo_tag():
    """
    closes the tag, that was open by the previous o_tag function
    :return:
    """
    global cloTagQ
    return cloTagQ.popleft()


def indent(amount, thing="\t"):
    '''
    allows to add indentation.
    :param amount: depth of indentation
    :param thing: indentation symbol, such as " ", "/t", "/n"
    :return: string of indentation symbols of needed depth
    '''
    return thing * amount

def getbody(file, out):
    '''
    parses txt file to get header and paragraphs
    :param file: name of the txt file to open
    :param out: array with body
    :return:
    '''
    count = 0
    i=0
    global tabDepth
    tabDepth = 1
    with open (file, 'r', encoding=encode) as f:
        lines = f.readlines()

        #adding header and opening first paragraph
        out.append(indent(tabDepth) + o_tag('h1'),
                   lines[0] + colo_tag(),
                   o_tag(indent(tabDepth) + 'p')) # opening first paragraph

        for i in range[3, len(lines)]:
            if lines[i] in ['\n', '\r\n']:
                out.append(indent(tabDepth) + clo_tag(), #closing previous paragraph
                            o_tag('p'))
            out.append(indent(tabDepth) + lines[i])

    out.append(o_tag(tabDepth)+ clo_tag())

    return 1


def create_html(file, lines): #this is console debug version of this function
    for line in lines:
        print (line)
    return

if __name__ == '__main__':
    source_dir = "."
    out_dir = "."

    # here i am using lovely argparse library, that will creahe help menu, and allow my script to take arguments
    parser = argparse.ArgumentParser(
        description="Will convert txt file into html file",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=90, width=120))
    groupGeneral = parser.add_argument_group()

    groupGeneral.add_argument('-i', '--input', help='input file location', metavar="FILE")
    groupGeneral.add_argument('-v', '--version', help='version number', action='store_true')
    groupGeneral.add_argument('-o', '--output', help='destination to place output file(s)', metavar="DESTDIR")
    groupGeneral.add_argument('-s', '--stylesheet', help='allow the user to optionally specify URL to a CSS '
                                                         'stylesheet to be used in the <head> of your generated HTML '
                                                         'files', metavar='URL' )
    groupGeneral.add_argument('-l', '--language', help='specify language such as: en, ru ...', metavar='LANG')
    groupGeneral.add_argument('-e', '--encoding', help="specify page encoding, such as utf-8", metavar='ENCODE')
    args = parser.parse_args()

    if args.version:
        print("version: {}".format(versionNum))
    if args.language:
        global lang
        lang = args.language
    if args.encoding:
        global encode
        encode = args.encode
    if args.output:
        global destDir
        destDir += args.output

    if args.input:    # TODO for more files can loop over them
        """
            this is the main part of the program, where all html conversion happens
        """
        print("file name is {}".format(args.input))

        title = args.input
        outputName = destDir + title +".html"

        Lines = ["<doctype html>",
                 o_tag("html", 'lang="{}"'.format(lang), True),
                 o_tag("head"),
                 indent(1) + o_tag('meta','charset="{}"'.format(lang), True),
                 indent(1) + o_tag("title") + title + clo_tag(),
                 indent(1) + o_tag("meta", 'content="width=device-width, initial-scale=1"', True)
                 ]

        if args.stylesheet:
            global styleURL
            styleURL = args.stylesheet
            Lines.append(indent(1) + o_tag("link", 'rel="stylesheet" style="text/css" href="{}"'.format(styleURL), True))

        Lines.append(clo_tag(), # close head
                    o_tag("body")
                     )

        body = getbody(title, Lines)

        Lines.append(
                    clo_tag(), # close body tag
                    clo_tag() # close html close html tag
                     )

        create_html(outputName, Lines)



