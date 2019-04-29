import html
import re
import requests

print("Crawling Database...")
r = requests.get(
    "https://www.nitrc.org/search/?type_of_search=group&offset=0&removeterm=&cat=&compare=&q=&search_explanation=&rows=1000000&s=name")
# matches = re.findall("<a href='([^<>]*)' title='' class=''>([^<>]*)</a>", r.text)
matches = re.findall('<h1 class="panel-title">[\s\S]*?<a href="([\s\S]*?)"[\s\S]*?>([\s\S]*?)<\/a>[\s\S]*?<\/h1>',
                     r.text)
count = 0
print("done\n")

for match in matches:
    name = html.escape(match[1].replace("\n", "").strip())
    print("Crawling " + name + "...")
    nameEsc = re.sub("[^a-zA-Z0-9]", "", name).lower()
    r = requests.get("https://www.nitrc.org" + match[0]).text.replace("\n", "").replace("\t", "")
    r = re.sub("  +", " ", r)
    r = r.replace("> <","><")
    xmlroot = "<root>\n<software>\n<--! PROPERTIES -->\n</software>\n</root>"
    properties = ['<name name="' + name + '" nitrc="' + "https://www.nitrc.org" + match[0] + '" />']

    descmatch = re.search(
        '<div class="col-md-12 tool-description">(<div .*?<\/div>.*?<\/a><\/div>)?(.*?)<\/div>',
        r)

    if descmatch == None:
        count += 1
        print("Not a valid tool!")
        continue

    g = descmatch.groups()
    desc = descmatch.group(
        2)


    #f2 = open(nameEsc + ".txt", "w+", encoding="utf-8")
    #f2.write(r)
    #f2.close()

    #g = descmatch.groups()
    #desc = descmatch


    imgIds = re.search('<a href="[^<>]*list_screenshots[^<>]*group_id=([0-9]+)[^<>]*screenshot_id=([0-9]+)"', r)

    if (imgIds != None):
        desc += '\n<p/><p/>\n' + '<a href="https://www.nitrc.org/project/screenshot.php?group_id=' + imgIds.group(
            1) + '&screenshot_id=' + imgIds.group(
            2) + '"><img class="size-full wp-image-1824" src="https://www.nitrc.org/project/screenshot.php?group_id=' + imgIds.group(
            1) + '&screenshot_id=' + imgIds.group(
            2) + '" alt="" width="458" height="248"/></a>\n'

    properties.append('<description>' + html.escape(desc) + '</description>')

    license = re.search('<a title="License .*?>([^<>]*)<\/a>', r)
    if license != None:
        properties.append('<license>' + license.group(1) + "</license>")

    for cat in re.findall('<a title="Category .*?>([^<>]*)<\/a>', r):
        properties.append('<category>' + cat + '</category>')
    for cat in re.findall('<a title="Operating System .*?>([^<>]*)<\/a>', r):
        properties.append('<platform>' + cat + '</platform>')
    for cat in re.findall('<a title="Supported Data Format .*?>([^<>]*)<\/a>', r):
        properties.append('<input>' + cat + '</input>')
        properties.append('<output>' + cat + '</output>')

    date = re.search('<strong>Registered:.*?<\/strong>([^<>]*)<\/p>', r)
    if date != None:
        properties.append('<release>' + date.group(1) + "</release>")

    url = re.search('<a href="([^<>]*?)">Home Page<\/a>', r)
    if url != None:
        properties.append('<homepage>' + url.group(1) + "</homepage>")

    maintainer = re.search('<strong>Organization:.*?<\/strong>([^<>]*)<\/p>', r)
    if maintainer != None:
        properties.append('<maintainer>' + maintainer.group(1) + "</maintainer>")

    properties.append("<HBP>External</HBP>")
    properties.append("<deployment>Standalone</deployment>")
    properties.append("<display>Desktop</display>")

    xmlroot = xmlroot.replace("<--! PROPERTIES -->", "\n".join(properties))
    f = open("Input/software_" + nameEsc + ".xml", "w+", encoding="utf-8")
    f.write(xmlroot)
    f.close()
    count += 1
    print("done (" + str(count) + "/" + str(len(matches)) + ")\n")

