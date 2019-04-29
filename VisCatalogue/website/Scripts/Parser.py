from xml.dom import minidom
import os
import re
import html
from functools import reduce

INPUT_DIR = "Input"
TEMPLATE_DIR = "Templates"
BODY_HTML = open(TEMPLATE_DIR + "/body.html").read()
ARTICLE_HTML = open(TEMPLATE_DIR + "/article.html").read()
CATEGORY_HTML = open(TEMPLATE_DIR + "/category.html").read()
MAINTAINER_HTML = open(TEMPLATE_DIR + "/maintainer.html").read()
TAG_HTML = open(TEMPLATE_DIR + "/tag.html").read()

META = {
    'FORMATS': ({}, ['input', 'output']),
    'DEPLOYMENTS': ({}, ['deployment']),
    'DISPLAYS': ({}, ['display']),
    'HBP': ({}, ['HBP']),
    'ABSTRACT': ({}, ['abstract']),
    '2D': ({}, ['d2']),
    '3D': ({}, ['d3']),
    'USAGE': ({}, ['usage'])
}

Formats = {}
Categories = {}
Deployments = {}
Displays = {}
HBP = {}


def getNodeText(node):
    if (node == []):
        return ""

    if isinstance(node, list):
        node = node[0]

    nodelist = node.childNodes
    result = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            result.append(node.data)
    return ''.join(result)


def insertMetaData(html):
    for key in META:
        list = []

        for format, software in sorted(META[key][0].items()):
            formatstring = "<li class=\"cat-item cat-item-3\"><input name=\"filterCheckbox\" type=\"checkbox\" onclick=\"handleClick();\" data-software=\""
            nameList = []
            for s in software:
                nameList.append(s.replace(" ", "-").lower())
            '''
            formatstring = "<li class=\"cat-item cat-item-3\"><details><summary><label>" + format + "</label></summary><ul class=\"children\">"
            for s in software:
                formatstring += "<li class=\"cat-item cat-item-3\"><a href=\"#" + s.replace(" ",
                                                                                            "-").lower() + "\">" + s + "</a></li></br>"
            '''
            formatstring += " ".join(nameList) + "\">" + format + "</input></li>"
            list.append(formatstring)

        html = html.replace("<!--{"+key+"}-->", " ".join(list))


    return html


def generateMetaData(xml):
    name = xml.getElementsByTagName("name")[0].getAttribute("name")
    for key in META:
        tmp = reduce(lambda x,y: x+y,[xml.getElementsByTagName(x) for x in META[key][1]])
        for elements in tmp:
            text = getNodeText(elements)
            if getNodeText(elements) not in META[key][0]:
                META[key][0][text] = []

            if name not in META[key][0][getNodeText(elements)]:
                META[key][0][text].append(name)


def generateSimpleList(list, seperator):
    tmplilst = []
    for p in sorted(list, key=lambda p: getNodeText(p)):
        tmplilst.append(p.firstChild.nodeValue)

    if tmplilst == []:
        return ""

    return seperator.join(tmplilst)


def generateFormats(formats):
    tmplilst = []
    for p in sorted(formats, key=lambda p: getNodeText(p)):
        tmplilst.append(p.firstChild.nodeValue)

    if tmplilst == []:
        return ""

    return ", ".join(tmplilst)


def generateTags(tags):
    taglist = []
    for tag in sorted(tags, key=lambda p: getNodeText(p)):
        tagHTML = TAG_HTML.replace("<!--{NAME}-->", tag.firstChild.nodeValue.title())
        tagHTML = tagHTML.replace("<!--{HREF_NAME}-->", tag.firstChild.nodeValue.replace(" ", "-").lower())
        taglist.append(tagHTML)

    return ', '.join(taglist)


def generateCategories(categories):
    catlist = []
    for cat in sorted(categories, key=lambda p: getNodeText(p)):
        catHTML = CATEGORY_HTML.replace("<!--{NAME}-->", cat.firstChild.nodeValue.title())
        catHTML = catHTML.replace("<!--{HREF_NAME}-->", cat.firstChild.nodeValue.replace(" ", "-").lower())
        catlist.append(catHTML)

    return ' '.join(catlist)


def generateMaintainer(maintainers):
    mainlist = []
    for main in sorted(maintainers, key=lambda p: getNodeText(p)):
        mails = main.getElementsByTagName("mail")
        mail = "" if mails == [] else "(" + mails[0].firstChild.nodeValue + ")"
        mainHTML = MAINTAINER_HTML.replace("<!--{NAME}-->", getNodeText(main))
        mainHTML = mainHTML.replace("<!--{MAIL}-->", mail)
        mainlist.append(mainHTML)

    if mainlist == []:
        return ""

    return '<br>'.join(mainlist)


def generateArticle(name):
    xml = minidom.parse(INPUT_DIR + '/' + name)
    generateMetaData(xml)

    articleHTML = ARTICLE_HTML.replace("<!--{DESCRIPTION}-->",
                                       html.unescape(xml.getElementsByTagName("description")[0].toxml()) if len(
                                           xml.getElementsByTagName("description")) > 0 else "")
    articleHTML = articleHTML.replace("<!--{MAINTAINER_LIST}-->",
                                      generateMaintainer(xml.getElementsByTagName("maintainer")))
    articleHTML = articleHTML.replace("<!--{TAG_LIST}-->", generateTags(xml.getElementsByTagName("tag")))
    articleHTML = articleHTML.replace("<!--{CATEGORY_LIST}-->",
                                      generateCategories(xml.getElementsByTagName("category")))
    articleHTML = articleHTML.replace("<!--{NAME}-->", xml.getElementsByTagName("name")[0].getAttribute("name"))
    articleHTML = articleHTML.replace("<!--{HREF_NAME}-->",
                                      xml.getElementsByTagName("name")[0].getAttribute("name").replace(" ",
                                                                                                       "-").lower())
    articleHTML = articleHTML.replace("<!--{RELEASE_DATE}-->", getNodeText(xml.getElementsByTagName("release")))
    articleHTML = articleHTML.replace("<!--{VERSION}-->",
                                      generateSimpleList(xml.getElementsByTagName("version"), "<br>"))
    articleHTML = articleHTML.replace("<!--{DOC_VERSION}-->", getNodeText(xml.getElementsByTagName("docversion")))
    articleHTML = articleHTML.replace("<!--{LINK}-->", generateSimpleList(xml.getElementsByTagName("homepage"), "<br>"))
    articleHTML = articleHTML.replace("<!--{DOC_LINK}-->",
                                      generateSimpleList(xml.getElementsByTagName("source"), "<br>"))
    articleHTML = articleHTML.replace("<!--{REQ_DEP_LIST}-->",
                                      generateSimpleList(xml.getElementsByTagName("requirements"), ", "))
    articleHTML = articleHTML.replace("<!--{TARGET_SYSTEMS}-->",
                                      generateSimpleList(xml.getElementsByTagName("platform"), "<br>"))
    articleHTML = articleHTML.replace("<!--{INPUT}-->", generateFormats(xml.getElementsByTagName("input")))
    articleHTML = articleHTML.replace("<!--{OUTPUT}-->", generateFormats(xml.getElementsByTagName("output")))
    articleHTML = articleHTML.replace("<!--{HBP}-->", generateSimpleList(xml.getElementsByTagName("HBP"), ", "))
    articleHTML = articleHTML.replace("<!--{LICENSE}-->", generateSimpleList(xml.getElementsByTagName("license"), ", "))
    articleHTML = articleHTML.replace("<!--{DEPLOYMENT}-->",
                                      generateSimpleList(xml.getElementsByTagName("deployment"), "<br>"))
    articleHTML = articleHTML.replace("<!--{DISPLAY}-->",
                                      generateSimpleList(xml.getElementsByTagName("display"), "<br>"))
    articleHTML = articleHTML.replace("<!--{FRAMEWORK}-->",
                                      generateSimpleList(xml.getElementsByTagName("framework"), "<br>"))
    return articleHTML


articlelist = []
for name in os.listdir(INPUT_DIR):
    print("Generating article "+name+" ...\n")
    articlelist.append(generateArticle(name))

HTML = insertMetaData(BODY_HTML)
HTML = HTML.replace("<!--{ARTICLE_LIST}-->", "\n<hr>".join(articlelist))
HTML = re.sub("<!--{.*}-->", "", HTML)

open("index.html", "w+", encoding="utf-8").write(HTML)
