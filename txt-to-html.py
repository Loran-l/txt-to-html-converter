#!/usr/local/bin/python3
###########################################################


#                txt-to-html-page
###########################################################
import argparse
import os
import sys

import json
import re



cloTagStack = []  # store closing tags


cloTagStack = []  # store closing tags

def o_tag(tag, params_str=None, close_tag=False, indent=""):
    '''
    Takes tag, generates closing tag, to be used with cloTag function
    Allows to use one-liner tags, like <link href=params_str> if close_tag is set to True
    :param tag: "html tag value"
    :param params_str: integ parameters, like [name="viewport" content="width=device-width, initial-scale=1"]
    :param close_tag: if this tag can close itself, and does not need separate closing tag, set to TRUE
    :return: opening teg with some optional parameters
    '''

    tag_line = indent + "<" + tag
    if params_str:
        tag_line += params_str
    if close_tag is False:
        global cloTagStack
        cloTagStack.append("</" + tag + ">")
        return tag_line + ">"

    return tag_line


def clo_tag():
    """
    closes the tag, that was open by the previous o_tag function
    :return:
    """
    global cloTagStack
    return cloTagStack.pop()


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
    i = 0
    global tabDepth
    tabDepth = 1
    with open(file, 'r', encoding=encode) as f:
        lines = f.readlines()

        # adding header and opening first paragraph
        out.extend([indent(tabDepth) + o_tag('h1') +
                   lines[0].rstrip() + clo_tag(),
                   indent(tabDepth) + o_tag('p')])  # opening first paragraph

        for i in range(3, len(lines)):
            if lines[i] in ['\n', '\r\n']:
                out.extend([indent(tabDepth) + clo_tag(),  # closing previous paragraph
                            indent(tabDepth) + o_tag('p')])
                continue  # who uses 'continue' nowdays, right?
            out.append(indent(tabDepth + 1) + lines[i].rstrip())

    out.append(indent(tabDepth) + clo_tag())
    return 1


def get_md_body(file, out):
    '''
    parses md file to get header and paragraphs
    :param file: name of the .md file to open
    :param out: array with body
    :return:
    '''
    count = 0
    i = 0
    global tabDepth
    global pline1
    global pline2
    global pline
    tabDepth = 1
    pline1 = ""
    pline2 = ""

    with open(file, 'r', encoding=encode) as f:
        for lines in f.readlines():
            # adding header
            if lines.startswith("#"):
                out.extend([indent(tabDepth) + o_tag('h1') +
                            lines.lstrip("#").strip() + clo_tag(),
                            indent(tabDepth) + o_tag('p')])  # opening first paragraph

            # the line has italic markdown

            pline1 = re.sub(r'(_[^\r\n\_].*?_)|(\*[^\r\n\*].*?\*)',
                            lambda s: "<i>{}</i>".format(s[0][1:-1]), lines)
            out.append(indent(tabDepth + 1) +
                       pline1)

            # the line has bold markdown

            pline2 = re.sub(r'(__[^\r\n\_].*?__)|(\*\*[^\r\n\*].*?\*\*)',
                            lambda s: "<b>{}</b>".format(s[0][2:-2]), lines)

        out.append(indent(tabDepth + 1) + pline2.rstrip())

    out.append(indent(tabDepth) + clo_tag())

    return 1


def create_html(file, lines):  # this is console debug version of this function
    for line in lines:
        print(line)
    return


if __name__ == '__main__':
    encode = "utf-8"
    lang = "en"
    title = "filename"
    tabDepth = 0
    versionNum = 0.1
    styleURL = None
    destDir = './dist/'
    source_dir = "."
    out_dir = "."
    input = None

    # here i am using argparse library, that will create help menu
    parser = argparse.ArgumentParser(
        description="Will convert txt file into html file",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=90, width=120))
    groupGeneral = parser.add_argument_group()

    groupGeneral.add_argument(
        '-i', '--input', help='input file location', metavar="FILE")
    groupGeneral.add_argument(
        '-v', '--version', help='version number', action='store_true')
    groupGeneral.add_argument(
        '-o', '--output', help='destination to place output file(s)', metavar="DESTDIR")
    groupGeneral.add_argument('-s', '--stylesheet', help='allow the user to optionally specify URL to a CSS '
                                                         'stylesheet to be used in the <head> of your generated HTML '
                                                         'files', metavar='URL')
    groupGeneral.add_argument(
        '-l', '--language', help='specify language such as: en, ru ...', metavar='LANG')
    groupGeneral.add_argument(
        '-e', '--encoding', help="specify page encoding, such as utf-8", metavar='ENCODE')
    groupGeneral.add_argument(
        '-c', '--config', help='specify config file to be used, must be JSON format', metavar='CONFIG'
    )
    args = parser.parse_args()

    if args.config:
        configPath = args.config
        if configPath == "" or not configPath.endswith(".json"):
            print("Invalid config file! Currently only support one *.json file")
            exit(-1)
        with open(configPath, encoding=encode) as configFile:
            configData = json.load(configFile)
            for key in configData:
                if key == 'input':
                    input = configData[key]
                elif key == 'output':
                    destDir = configData[key]
                elif key == 'language' or key == 'lang':
                    lang = configData[key]
                elif key == 'encode' or key == 'encoding':
                    encode = configData[key]
    else:
        if args.version:
            print("version: {}".format(versionNum))
        if args.language:
            lang = args.language
        if args.encoding:
            encode = args.encode
        if args.output:
            destDir += args.output
        if args.input:
            input = args.input

    if input and len(input) > 0:    # TODO for multiple files can loop over them
        """
            this is the main part of the program, where all html conversion happens
        """
        print("file name is {}".format(input))

        title = input
        outputName = destDir + title + ".html"

        Lines = ["<doctype html>",
                 o_tag("html", 'lang="{}"'.format(lang)),
                 o_tag("head"),
                 indent(1) + o_tag('meta', 'charset="{}"'.format(lang), True),
                 indent(1) + o_tag("title") + title + clo_tag(),
                 indent(1) + o_tag("meta",
                                   'content="width=device-width, initial-scale=1"', True)
                 ]

        if args.stylesheet:
            styleURL = args.stylesheet

            Lines.append(indent(
                1) + o_tag("link", 'rel="stylesheet" style="text/css" href="{}"'.format(styleURL), True))

        Lines.extend([clo_tag(),  # close head
                      o_tag("body")
                      ])
        if title.endswith(".txt"):
            body = getbody(title, Lines)
        elif title.endswith(".md"):
            body = get_md_body(title, Lines)

        Lines.extend([
            clo_tag(),  # close body tag
            clo_tag()  # close html close html tag
        ])


        create_html(outputName, Lines)
    
    elif not args.version:
        print("Invalid input")
        exit(-1)
