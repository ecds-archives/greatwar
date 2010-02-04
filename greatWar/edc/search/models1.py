class NonPoem(object):
    id          = XpathString('@ID')
    headrend    = XpathString('@rend')
    type        = XpathString('@type')

    def __init__(self, dom_node):
        self.dom_node = dom_node



class Poem(object):
    id          = XpathString('@ID')
    headrend    = XpathString('@rend')
    docAuthor   = XpathString('docAuthor/@n')
    byline      = XpathString('docAuthor/byline')
    title       = XpathString('docAuthor/title')

    def __init__(self, dom_node):
        self.dom_node = dom_node


class Layer(object):
    title       = XpathString('teiHeader/fileDesc/titleStmt/title')
    name        = XpathString('teiHeader/fileDesc/titleStmt/editor/name')


    def __init__(self, dom_node):
        self.dom_node = dom_node
