# python读取XML文件和TMX文件


## 什么是XML文件
xml即可扩展标记语言，它可以用来标记数据、定义数据类型，是一种允许用户对自己的标记语言进行定义的源语言，同时是一种简单的数据存储语言。使用一系列简单的标记描述数据，而这些标记可以用方便的方式建立，虽然可扩展标记语言占用的空间比二进制数据要占用更多的空间，但可扩展标记语言极其简单易于掌握和使用。以一个简单的XML文件为例（text.xml）：


    <?xml version="1.0" encoding="utf-8"?>
	<data>
    <login username="pytest" passwd='2019'>
        <first>Python</first>
        <second>text</second>
		<third>XML</third>
    </login>
	</data>
	
	
**从中可以看出它有如下特征：
**1.有标签对组成：<data></data>
**2.标签可以有属性：<login username="pytest" passwd='2019'>
	

**3.标签对可以嵌入数据：<first>Python</first>
**4.标签可以嵌入子标签（具有层级关系）：<data><first>Python</first></data>


## 什么是TMX文件

这是翻译记忆交换（TMX）格式，是XML的一种特殊格式。一个开放中创建的文件XML用于交换由计算机辅助翻译（CAT）和本地化应用程序创建的翻译记忆库（TM）数据标准。它可以被用于保存的词或已翻译从一种语言到另一种的短语。使用这种文件格式的程序包括Maxprograms箭鱼，OmegaT，SDL Trados Studio中和AIT视觉本地化。


   
**有两种方法读取出在text.xml文件中first，second，third标签下的内容**

## 一.使用ElementTree处理xml文件
**1）.简单遍历**

该文件分为三层，通过一下方法遍历得到各层的标签名称，属性和对应的文本

	import xml.etree.ElementTree as ET

	tree = ET.parse("text.xml")
	root = tree.getroot()
	print(root.tag, ":", root.attrib)  # 打印根元素的tag和属性
	# 遍历xml文档的第二层
	for child in root:
	    # 第二层节点的标签名称，属性和对应的文本
	    print(child.tag, ":", child.attrib)
	    print(child.text)
	    # 遍历xml文档的第三层
	    for children in child:
	        # 第三层节点的标签名称，属性和对应的文本
	        print(children.tag, ":", children.attrib)
	        print(children.text)



**2).通过下标的方式直接访问节点**


	# 访问根节点下login的第0个节点first,获取对应的文本
	first = root[0][0].text    # first = python
	print(first)

以此为基础改动，也可以得到标签节点下对应的文本


	import xml.etree.ElementTree as ET

	tree = ET.parse("text.xml")
	root = tree.getroot()
	indexAhead = 0
	indexBehind = 0
	for child in root:
	    indexBehind = 0
	    print(root[indexAhead].text)
	
	    for children in child:
	        print(children.tag, ":", root[indexAhead][indexBehind].text, "\n")
	        indexBehind += 1
	    indexAhead += 1


**3).ElementTree提供的方法**


	find(match)                         # 查找第一个匹配的子元素， match可以时tag或是xpaht路径
	findall(match)                      # 返回所有匹配的子元素列表 
	iter(tag=None)                      # 以当前元素为根节点 创建树迭代器,如果tag不为None,则以tag进行过滤


	# 过滤出所有first标签和属性
	for fiest in root.iter("first"):
    	print(fiest.tag, ":", fiest.attrib)


**以上方法能够很快遍历小型的xml和tmx，对于大型文件，并不适用**


## 二.使用mxl.dom.minidom 模块被用来处理xml文件 

**1）获得标签属性（data）**


	import xml.dom.minidom  # mxl.dom.minidom 模块被用来处理xml文件，所以要先引入。

	# 打开xml文档
	dom = xml.dom.minidom.parse('text.xml')  # xml.dom.minidom.parse() 用于打开一个xml文件，并将这个文件对象dom变量.

	# 得到文档元素对象
	root = dom.documentElement  # documentElement 用于得到dom对象的文档元素，并把获得的对象给root
	print(root.nodeName)  # nodeName为结点名字。
	print(root.nodeValue)  # nodeValue是结点的值，只对文本结点有效。
	print(root.nodeType)  # nodeType是结点的类型。
	print(root.ELEMENT_NODE)  # data是ELEMENT_NODE



**附：nodeTypes —— 有名常数**


|nodeType	|Named Constant		|
| --------	|--------		|
|	1	|ELEMENT_NODE		|
|	2	|ATTRIBUTE_NODE		|
|	3	|TEXT_NODE		|
|	4	|CDATA_SECTION_NODE	|
|	5	|ENTITY_REFERENCE_NODE	|
|	6	|ENTITY_NODE		|
|	7	|PROCESSING_INSTRUCTION_NODE|
|	8	|COMMENT_NODE		|
|	9	|DOCUMENT_NODE		|
|	10	|DOCUMENT_TYPE_NODE	|
|	11	|DOCUMENT_FRAGMENT_NODE	|
|	12	|NOTATION_NODE		|






**nodeName  —— 结点名字	和	nodeValue —— 结点的值**


|结点类型	|nodeName的返回值	|nodeValue的返回值	|
|--------   |:----:|:----:|
|Document|#document|null|
|DocumentType|doctype 名称|null|
|DocumentFragment|#document fragment|null|
|EntityReference|实体引用名称|null|
|Element|element name|null|
|Attr|属性名称|属性值|
|Comment|#comment|注释文本|
|ProcessingInstruction|target|结点的内容|
|Text|#text|结点内容|
|CDATASection|	#cdata-section|结点内容|
|Entity|实体名称|null|
|Notation|符号名称|null|



**2).获得子标签和属性**

调用getElementsByTagName方法获取name：

	
	name = root.getElementsByTagName('login')
	print(name)  # [<DOM Element: login at 0x1f6e1cdd340>]
	tagName = name[0]
	print(tagName.nodeName)  # login


调用getAttribute方法可以获得元素的属性所对应的值。
	
	itemList = root.getElementsByTagName('login')
	item = itemList[0]
	un = item.getAttribute("username")
	print(un)
	pd = item.getAttribute("password")
	print(pd)


**3).获得标签下对应的文本**

调用firstChild 属性返回被选节点的第一个子节点，.data表示获取该节点人数据。

	node = dom.getElementsByTagName('first')
	childrenNode = node[0]
	print(childrenNode.firstChild.data)  # python
	
	node = dom.getElementsByTagName('second')
	childrenNode = node[0]
	print(childrenNode.firstChild.data)  # text
	
	node = dom.getElementsByTagName('third')
	childrenNode = node[0]
	print(childrenNode.firstChild.data)  # XML
	

## 代码演示 

代码示例一：

	import xml.etree.ElementTree as ET

	tree = ET.parse("text.xml")
	root = tree.getroot()
	print(root.tag, ":", root.text)
	for child in root:
	    print(child.tag, ":", child.text)
	    for children in child:
	        print(children.tag, ":", children.text)


>>

	#输出示例
	data : 
    
	login : 
	        
	first : Python
	second : text
	third : XML



代码示例二：

	import xml.etree.ElementTree as ET
	
	tree = ET.parse("text.xml")
	root = tree.getroot()
	indexAhead = 0
	indexBehind = 0
	for child in root:
	    root = tree.getroot()
	    indexBehind = 0
	    print(root[indexAhead].text)	
	    for children in child:
	        print(children.tag, ":", root[indexAhead][indexBehind].text, "\n")
	        indexBehind += 1
	    indexAhead += 1


>>
	#输出示例
	
      
	first : Python 
	
	second : text 
	
	third : XML 
	
	
代码示例三：

	import xml.dom.minidom
	
	dom = xml.dom.minidom.parse('text.xml')
	
	root = dom.documentElement 
	
	name = root.getElementsByTagName('login')
	tagName = name[0]
	print(tagName.nodeName)
	
	itemList = root.getElementsByTagName('login')
	item = itemList[0]
	un = item.getAttribute("username")
	print(un)
	pd = item.getAttribute("password")
	print(pd)
	
	node = dom.getElementsByTagName('first')
	childrenNode = node[0]
	print(childrenNode.firstChild.data)
	
	node = dom.getElementsByTagName('second')
	childrenNode = node[0]
	print(childrenNode.firstChild.data)
	
	node = dom.getElementsByTagName('third')
	childrenNode = node[0]
	print(childrenNode.firstChild.data)

>>
	#输出示例
	login
	pytest
	2019
	Python
	text
	XML




