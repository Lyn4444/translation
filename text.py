import xml.etree.ElementTree as ET

fileName = 'xmlRead.txt'
with open(fileName, 'w', encoding='utf-8') as f:
    tree = ET.parse("text.xml")
    root = tree.getroot()

    indexAhead = 0
    indexBehind = 0
    for child in root:
        root = tree.getroot()
        indexBehind = 0
        if root[indexAhead].text is not None:
            f.write(root[indexAhead].text)
            f.write("\n")

        for children in child:
            if root[indexAhead][indexBehind].text is not None:
                f.write(children.tag)
                f.write(":")
                f.write(root[indexAhead][indexBehind].text)
                f.write("\n")
            indexBehind += 1

        indexAhead += 1

f.close()
