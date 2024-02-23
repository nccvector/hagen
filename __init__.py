def OpenTag(tagName):
    return '<' + tagName + '>'


def CloseTag(tagName):
    return '</' + tagName + '>'


def GetClassAttrib(instance):
    return instance.__class__


def ClassName(instance):
    return GetClassAttrib(instance).__name__


def NewLine():
    return '\n'


class AbstractBaseTag:
    _validElements = None
    _content = None
    _operations = None
    def __init__(self, content: object, validElements=[]):
        self._validElements = validElements
        if len(self._validElements) > 0 and ClassName(content) not in self._validElements:
            raise Exception('Invalid args passed to "' + ClassName(self) + '"\nSupported elements are: ' + str(self._validElements))

        self._content = content
        self._operations = [
            self.Open,
            self.GetContentString,
            self.Close,
        ]

    def Open(self) -> str:
        return OpenTag(ClassName(self))

    def Close(self) -> str:
        return CloseTag(ClassName(self))

    def __str__(self) -> str:
        output = ''
        for fn in self._operations:
            output += fn()

        return output

    def GetContentString(self):
        return str(self._content)


class meta(AbstractBaseTag):
    def __init__(self, content: str):
        super(GetClassAttrib(self), self).__init__(content)


class title(AbstractBaseTag):
    def __init__(self, content: str):
        super(GetClassAttrib(self), self).__init__(content)


class head(AbstractBaseTag):
    def __init__(self, content: AbstractBaseTag):
        validElements = ['meta', 'link', 'title', 'style', 'script', 'noscript', 'base']
        super(GetClassAttrib(self), self).__init__(content, validElements)


class h1(AbstractBaseTag):
    def __init__(self, content: str):
        super(GetClassAttrib(self), self).__init__(content)


class body(AbstractBaseTag):
    def __init__(self, content: AbstractBaseTag):
        validElements = ['h1', 'p']
        super(GetClassAttrib(self), self).__init__(content, validElements)


class footer(AbstractBaseTag):
    def __init__(self, content: AbstractBaseTag):
        super(GetClassAttrib(self), self).__init__(content)


class html(AbstractBaseTag):
    _head= None
    _body = None
    _footer = None
    def __init__(self, head: head, body: body, footer: footer):
        super(GetClassAttrib(self), self).__init__('')
        self._head = head
        self._body = body
        self._footer = footer

        self._operations = [
            self.Open,
            self.GetHeadString,
            self.GetBodyString,
            self.GetFooterString,
            self.Close
        ]

    def GetHeadString(self):
        return str(self._head)

    def GetBodyString(self):
        return str(self._body)

    def GetFooterString(self):
        return str(self._footer)


if __name__ == '__main__':
    htmlString = '<!DOCTYPE html>'
    htmlString += str(
        html(
            head(title('I am Head')),
            body(h1('I am body')),
            footer('I am footer')
        )
    )

    from bs4 import BeautifulSoup
    from bs4.formatter import HTMLFormatter

    soupObj = BeautifulSoup(htmlString)
    bhtml = soupObj.prettify(formatter=HTMLFormatter(indent=4))

    print(bhtml)

