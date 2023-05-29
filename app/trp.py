"""AWS Textract Response Parser"""

class BaseBlock:
    def __init__(self, block, block_map):
        self._block = block
        self._confidence = block['Confidence']
        self._geometry = Geometry(block['Geometry'])
        self._id = block['Id']
        self._text = ""
        self._text_type = ""
        if 'Text' in block and block['Text']:
            self._text = block['Text']
        if "Custom" in block and block['Custom']:
            self._custom = block["Custom"]
        if 'TextType' in block and block['TextType']:
            self._text_type = block['TextType']
    
    def __str__(self):
        return self._text

    @property
    def custom(self):
        return self._custom

    @property
    def confidence(self):
        return self._confidence

    @property
    def geometry(self):
        return self._geometry

    @property
    def id(self):
        return self._id

    @property
    def text(self):
        return self._text

    @property
    def block(self):
        return self._block

    @property
    def textType(self):
        return self._text_type

   
class BoundingBox:

    def __init__(self, width, height, left, top):
        self._width = width
        self._height = height
        self._left = left
        self._top = top

    def __str__(self):
        return "width: {}, height: {}, left: {}, top: {}".format(self._width, self._height, self._left, self._top)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def left(self):
        return self._left

    @property
    def top(self):
        return self._top


class Polygon:

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __str__(self):
        return "x: {}, y: {}".format(self._x, self._y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Geometry:

    def __init__(self, geometry):
        boundingBox = geometry["BoundingBox"]
        polygon = geometry["Polygon"]
        bb = BoundingBox(boundingBox["Width"], boundingBox["Height"], boundingBox["Left"], boundingBox["Top"])
        pgs = []
        for pg in polygon:
            pgs.append(Polygon(pg["X"], pg["Y"]))

        self._boundingBox = bb
        self._polygon = pgs

    def __str__(self):
        s = "BoundingBox: {}\n".format(str(self._boundingBox))
        return s

    @property
    def boundingBox(self):
        return self._boundingBox

    @property
    def polygon(self):
        return self._polygon


class Word(BaseBlock):

    def __init__(self, block, blockMap):
        super().__init__(block, blockMap)


class Line(BaseBlock):

    def __init__(self, block, blockMap):
        super().__init__(block, blockMap)

        self._words = []
        if ('Relationships' in block and block['Relationships']):
            for rs in block['Relationships']:
                if (rs['Type'] == 'CHILD'):
                    for cid in rs['Ids']:
                        if (blockMap.get(cid, None)):
                            if (blockMap[cid]["BlockType"] == "WORD"):
                                self._words.append(Word(blockMap[cid], blockMap))

    def __str__(self):
        s = "Line\n==========\n"
        s = s + self._text + "\n"
        s = s + "Words\n----------\n"
        for word in self._words:
            s = s + "[{}]".format(str(word))
        return s

    @property
    def words(self):
        return self._words
    

class Page:

    def __init__(self, blocks, blockMap):
        self._blocks = blocks
        self._text = ""
        self._lines = []
        self._content = []
        self._custom = dict()

        self._parse(blockMap)

    def __str__(self):
        s = "Page\n==========\n"
        for item in self._content:
            s = s + str(item) + "\n"
        return s

    def _parse(self, blockMap):
        for item in self._blocks:
            if item["BlockType"] == "PAGE":
                self._geometry = Geometry(item['Geometry'])
                self._id = item['Id']
                if "Custom" in item:
                    self._custom = item["Custom"]
            elif item["BlockType"] == "LINE":
                l = Line(item, blockMap)
                self._lines.append(l)
                self._content.append(l)
                self._text = self._text + l.text + '\n'


    def getLinesInReadingOrder(self):
        columns = []
        lines = []
        for item in self._lines:
            column_found = False
            for index, column in enumerate(columns):
                bbox_left = item.geometry.boundingBox.left
                bbox_right = item.geometry.boundingBox.left + item.geometry.boundingBox.width
                bbox_centre = item.geometry.boundingBox.left + item.geometry.boundingBox.width / 2
                column_centre = column['left'] + column['right'] / 2
                if (bbox_centre > column['left'] and bbox_centre < column['right']) or (column_centre > bbox_left
                                                                                        and column_centre < bbox_right):
                    #Bbox appears inside the column
                    lines.append([index, item.text])
                    column_found = True
                    break
            if not column_found:
                columns.append({
                    'left': item.geometry.boundingBox.left,
                    'right': item.geometry.boundingBox.left + item.geometry.boundingBox.width
                })
                lines.append([len(columns) - 1, item.text])

        lines.sort(key=lambda x: x[0])
        return lines

    def getTextInReadingOrder(self):
        lines = self.getLinesInReadingOrder()
        text = ""
        for line in lines:
            text = text + line[1] + '\n'
        return text

    @property
    def blocks(self):
        return self._blocks

    @property
    def text(self):
        return self._text

    @property
    def lines(self):
        return self._lines

    @property
    def content(self):
        return self._content

    @property
    def geometry(self):
        return self._geometry

    @property
    def id(self):
        return self._id

    @property
    def custom(self):
        return self._custom


class Document:

    def __init__(self, responsePages):

        if (not isinstance(responsePages, list)):
            rps = []
            rps.append(responsePages)
            responsePages = rps

        self._responsePages = responsePages
        self._pages = []

        self._parse()

    def __str__(self):
        s = "\nDocument\n==========\n"
        for p in self._pages:
            s = s + str(p) + "\n\n"
        return s

    def _parseDocumentPagesAndBlockMap(self):

        blockMap = {}

        documentPages = []
        documentPage = None
        for page in self._responsePages:
            for block in page['Blocks']:
                if ('BlockType' in block and 'Id' in block):
                    blockMap[block['Id']] = block

                if (block['BlockType'] == 'PAGE'):
                    if (documentPage):
                        documentPages.append({"Blocks": documentPage})
                    documentPage = []
                    documentPage.append(block)
                else:
                    if documentPage:
                        documentPage.append(block)
                    else:
                        raise Exception("Invalid response received from Textract. No PAGE block found.")
        if (documentPage):
            documentPages.append({"Blocks": documentPage})
        return documentPages, blockMap

    def _parse(self):

        self._responseDocumentPages, self._blockMap = self._parseDocumentPagesAndBlockMap()
        for documentPage in self._responseDocumentPages:
            page = Page(documentPage["Blocks"], self._blockMap)
            self._pages.append(page)

    @property
    def blocks(self):
        return self._responsePages

    @property
    def pageBlocks(self):
        return self._responseDocumentPages

    @property
    def pages(self):
        return self._pages

    def getBlockById(self, blockId):
        block = None
        if (self._blockMap and blockId in self._blockMap):
            block = self._blockMap[blockId]
        return block