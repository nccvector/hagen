def OpenTag(tagName, **kwargs):
    output = '<' + tagName
    for key, val in kwargs.items():
        output += ' ' + key + '=' + val
    output += '>'
    return output


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
    _kwargs = {}
    def __init__(self, content: object, validElements=[], **kwargs):
        self._kwargs = kwargs
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
        return OpenTag(ClassName(self), **self._kwargs)

    def Close(self) -> str:
        return CloseTag(ClassName(self))

    def __str__(self) -> str:
        output = ''
        for fn in self._operations:
            output += fn()

        return output

    def GetContentString(self):
        return str(self._content)


# ================================================================================
# Head elements
# ================================================================================
class meta(AbstractBaseTag):
    def __init__(self, content: str, **kwargs):
        super(GetClassAttrib(self), self).__init__(content, **kwargs)


class title(AbstractBaseTag):
    def __init__(self, content: str, **kwargs):
        super(GetClassAttrib(self), self).__init__(content, **kwargs)


class head(AbstractBaseTag):
    def __init__(self, content: AbstractBaseTag, **kwargs):
        validElements = ['meta', 'link', 'title', 'style', 'script', 'noscript', 'base']
        super(GetClassAttrib(self), self).__init__(content, validElements, **kwargs)

# ================================================================================


# ================================================================================
# Body elements
# ================================================================================
class h1(AbstractBaseTag):
    def __init__(self, content: str, **kwargs):
        super(GetClassAttrib(self), self).__init__(content, **kwargs)

class p(AbstractBaseTag):
    def __init__(self, content: str, **kwargs):
        super(GetClassAttrib(self), self).__init__(content, **kwargs)

class body(AbstractBaseTag):
    def __init__(self, content: AbstractBaseTag, **kwargs):
        validElements = ['h1', 'p']
        super(GetClassAttrib(self), self).__init__(content, validElements, **kwargs)

# ================================================================================


# ================================================================================
# Body elements
# ================================================================================
class footer(AbstractBaseTag):
    def __init__(self, content: AbstractBaseTag, **kwargs):
        super(GetClassAttrib(self), self).__init__(content, **kwargs)

# ================================================================================


# ================================================================================
# HTML elements
# ================================================================================
class html(AbstractBaseTag):
    _head= None
    _body = None
    _footer = None
    def __init__(self, head: head, body: body, footer: footer, **kwargs):
        super(GetClassAttrib(self), self).__init__('', **kwargs)
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

# ================================================================================


if __name__ == '__main__':
    htmlString = '<!DOCTYPE html>'
    htmlString += str(
        html(
            head(title('I am Head', font="1.0"), someRandom="random", someRandom2="2"),
            body(p('I am body')),
            footer('I am footer'),
            randomHtmlAttrib="ABC"
        )
    )

    from bs4 import BeautifulSoup
    from bs4.formatter import HTMLFormatter

    soupObj = BeautifulSoup(htmlString)
    bhtml = soupObj.prettify(formatter=HTMLFormatter(indent=4))

    print(bhtml)

