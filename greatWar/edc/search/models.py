from existdb.db import XpathInteger, XpathString, XpathStringList, XpathObjectList, QueryResult
from django.conf import settings
import re #RegExp library
from Ft.Xml.Domlette import NonvalidatingReader

class FileDscr(object):
    id          = XpathString('@ID')
    filename    = XpathString('fileName')
    fileStrc    = XpathString('fileStrc/@type')
    caseQnty    = XpathString('dimensns/caseQnty')
    varQnty     = XpathString('dimensns/varQnty')
    logRecL     = XpathString('dimensns/logRecL')
    recPrCas    = XpathString('dimensns/recPrCas')
    extLink     = XpathString('fileType/ExtLink/@URI')
    fileType    = XpathString('fileType')

    def __init__(self, dom_node):
        self.dom_node = dom_node

class DownloadableFile:
    name    = XpathString('@name')
    dir     = XpathString('@dir')
    href    = XpathString('@href')
    size    = XpathString('@size')

    def __init__(self, dom_node):
        self.dom_node = dom_node

    def __cmp__(self, other):
        return cmp(self.name, other.name)

class DownloadableDocuments:
    #files = XpathObjectList("/ICPSR/IDNo[@id = '0001']/file", DownloadableFile)

    def __init__(self, index_key):
        self.dom        = NonvalidatingReader.parseUri(settings.ADDITIONAL_DATA_INDEX)
        self.dom_node   = self.dom.documentElement
        self.index_key  = index_key

    @property
    def files(self):
        match_nodes = self.dom_node.xpath("/ICPSR/IDNo[@id = '%(id)s']/file" % {'id': self.index_key} )

        rVal = []
        for n in match_nodes:
            rVal.append(DownloadableFile(n))
        return rVal

    def group_for_display(self):
        #groups files for display
        labels = {'sav': 'SPSS data',
                  'por': 'SPSS data',
                  'dta': 'Stata data',
                  'do' : 'Strata command files',
                  'cb' : 'code book',
                  'da' : 'data',
                  'sa' : 'SAS command files',
                  'sp' : 'SPSS command files',
                  'default': 'other files',}

        rVal = {}
        for f in self.files:
            m = re.search("(sav|por|dta|do)$", f.name)
            if m:
                if not labels[m.group(0)] in rVal:
                    rVal[labels[m.group(0)]] = []
                rVal[labels[m.group(0)]].append(f)
            else:
                m = re.search("^(cb|da|sa|sp)", f.name)
                if m:
                    if not labels[m.group(0)] in  rVal:
                        rVal[labels[m.group(0)]] = []
                    rVal[labels[m.group(0)]].append(f)
                else:
                    if not labels['default'] in rVal:
                        rVal[labels['default']] = []
                    rVal[labels['default']].append(f)
        return rVal

class CodeBookResult(object):
    hits                    = XpathInteger('hits')
    authEnty                = XpathStringList('docDscr/citation/rspStmt/AuthEnty')
    title                   = XpathString('stdyDscr/citation/titlStmt/titl')
    id                      = XpathString('docDscr/citation/titlStmt/IDNo')
    principal_investigator  = XpathStringList('stdyDscr/citation/rspStmt/AuthEnty')
    otherID                 = XpathString('docDscr/citation/rspStmt/othId')
    copyright               = XpathString('docDscr/citation/prodStmt/copyright')
    prodDate                = XpathString('docDscr/citation/prodStmt/prodDate')
    citation_version        = XpathString('docDscr/citation/verStmt/version')
    citation_verResp        = XpathString('docDscr/citation/verStmt/verResp')
    citation_notes          = XpathString('docDscr/citation/verStmt/notes')
    stdy_title              = XpathString('stdyDscr/citation/titlStmt/titl')
    stdy_subtitle           = XpathString('stdyDscr/citation/titlStmt/subTitl')
    stdy_alttitle           = XpathString('stdyDscr/citation/titlStmt/altTitl')
    stdy_authEntity         = XpathStringList('stdyDscr/citation/rspStmt/AuthEnty')
    stdy_version            = XpathString('stdyDscr/citation/verStmt/version')
    collection_size         = XpathString('stdyDscr/dataAccs/setAvail/collSize')
    stdy_notes              = XpathString('stdyDscr/citation/verStmt/notes')
    subjectKeywords         = XpathStringList('stdyDscr/stdyInfo/subject/keyword')
    subjectTopics           = XpathStringList('stdyDscr/stdyInfo/subject/topcClas')
    universe                = XpathString('stdyDscr/stdyInfo/sumDscr/universe')
    biblioCit               = XpathString('stdyDscr/citation/biblCit')
    versionHistory          = XpathStringList('stdyDscr/citation/verStmt/version')
    abstract                = XpathString('stdyDscr/stdyInfo/abstract')
    timePrd_start           = XpathString('stdyDscr/stdyInfo/sumDscr/timePrd[@event = "start"]/@date')
    timePrd_end             = XpathString('stdyDscr/stdyInfo/sumDscr/timePrd[@event = "end"]/@date')
    geoCoverages            = XpathStringList('stdyDscr/stdyInfo/sumDscr/geogCover')
    nations                 = XpathStringList('stdyDscr/stdyInfo/sumDscr/nation')
    geoUnits                = XpathStringList('stdyDscr/stdyInfo/sumDscr/geogUnit')
    anlyUnit                = XpathString('stdyDscr/stdyInfo/sumDscr/anlyUnit')
    dataKind                = XpathString('stdyDscr/stdyInfo/sumDscr/dataKind')
    stdyDscr_notes          = XpathString('stdyDscr/stdyInfo/notes')
    frequency               = XpathString('stdyDscr/method/dataColl/frequenc')
    cleanOps                = XpathString('stdyDscr/method/dataColl/cleanOps')
    method_notes            = XpathString('stdyDscr/method/notes')
    locations               = XpathStringList('stdyDscr/dataAccs/setAvail/accsPlac')
    restriction             = XpathString('stdyDscr/dataAccs/useStmt/restrctn')
    conditions              = XpathString('stdyDscr/dataAccs/useStmt/conditions')
    access_notes            = XpathString('stdyDscr/dataAccs/notes')
    file_notes              = XpathString('fileDscr/notes')

    # FileDscr must be defined before this
    parts                   = XpathObjectList('fileDscr/fileTxt', FileDscr)    

    def __init__(self, dom_node):
        self.dom_node = dom_node
        self.downloadable_files = DownloadableDocuments(self.id)

    @property
    def doi_id(self):
        #parse the doi_id from the biblioCit
        m = re.search('doi:(\S*)', self.biblioCit)
        if m:
            return m.group(1)

    @property
    def doi_url(self):
        if self.doi_id:
            return settings.DOI_PURL_HOST + self.doi_id

    def download_files_links(self):
        files = AdditionalDocuments

# extend default exist query result to add mapping for codeBook results
class CodeBookQueryResult(QueryResult):
    codeBooks = XpathObjectList('codeBook', CodeBookResult)
    
     
class BookDetailResult(object):
	id						=XpathString('id')
	category				=XpathString('@category')
	title					=XpathString('title')
	lang					=XpathString('title/@lang')
	authors					=XpathStringList('author')
	year					=XpathString('year')
	
	def __init__(self, dom_node):
		self.dom_node = dom_node

	@property
	def doi_id(self):
        #parse the doi_id from the biblioCit
		m = re.search('doi:(\S*)', self.biblioCit)
		if m:
			return m.group(1)

	@property
	def doi_url(self):
		if self.doi_id:
			return settings.DOI_PURL_HOST + self.doi_id

	def download_files_links(self):
		files = AdditionalDocuments
		
	
    
class BookDetailQueryResult(QueryResult):
    books = XpathObjectList('book', BookDetailResult)	   
    
class BookResult(object):
	id						=XpathString('id')
	title					=XpathString('title')
	authors					=XpathStringList('author')
	
	def __init__(self, dom_node):
		self.dom_node = dom_node

	@property
	def doi_id(self):
        #parse the doi_id from the biblioCit
		m = re.search('doi:(\S*)', self.biblioCit)
		if m:
			return m.group(1)

	@property
	def doi_url(self):
		if self.doi_id:
			return settings.DOI_PURL_HOST + self.doi_id

	def download_files_links(self):
		files = AdditionalDocuments
	
class BookQueryResult(QueryResult):
    books = XpathObjectList('book', BookResult)
    
    
class BookStoreResult(object):
    hits                    = XpathInteger('hits')
    authList                = XpathStringList('book/author')
    title                   = XpathString('book/title')
    year                   	= XpathString('book/year')
    price                   = XpathString('book/price') 

    def __init__(self, dom_node):
        self.dom_node = dom_node
        #self.downloadable_files = DownloadableDocuments(self.id)

    @property
    def doi_id(self):
        #parse the doi_id from the biblioCit
        m = re.search('doi:(\S*)', self.biblioCit)
        if m:
            return m.group(1)

    @property
    def doi_url(self):
        if self.doi_id:
            return settings.DOI_PURL_HOST + self.doi_id

    def download_files_links(self):
        files = AdditionalDocuments
       

class BookStoreQueryResult(QueryResult):
    bookstores = XpathObjectList('bookstore', BookStoreResult)
    
class BriefPoem1(object):
	id						=XpathString('@id')
	bpType					=XpathString('@type')
	title					=XpathString('head')
	author					=XpathString('docAuthor')
	
	def __init__(self, dom_node):
		self.dom_node = dom_node
	
class BriefPoemList1(QueryResult):
    briefPoems = XpathObjectList('div', BriefPoem1)    

    
    
class BriefPoem(object):
	id						=XpathString('id')
	title					=XpathString('title')
	author					=XpathString('author')
	
	def __init__(self, dom_node):
		self.dom_node = dom_node
	
class BriefPoemList(QueryResult):
    briefPoems = XpathObjectList('briefPoem', BriefPoem)    

class Head(object):
	content = XpathString('.')
	rend = XpathString('@rend')
	def __init__(self, dom_node):
		self.dom_node = dom_node

class Line(object):
	content = XpathString('.')
	rend = XpathString('@rend')
	def __init__(self, dom_node):
		self.dom_node = dom_node
	
class Paragraph(object):
	lines = XpathObjectList('l', Line)    
	pType = XpathString('@type')
	def __init__(self, dom_node):
		self.dom_node = dom_node

class FullPoem(object):
	title       = XpathString('title')
	editor    	= XpathString('editor')
	publisher 	= XpathString('publisher')
	ptitle      = XpathString('ptitle')
	peditor    	= XpathString('peditor')
	pplace    	= XpathString('pplace')
	pdate    	= XpathString('pdate')
	heads    	= XpathObjectList('head', Head)
	paragraphs	= XpathObjectList('lg', Paragraph)
	byline      = XpathString('byline')
	dateline	= XpathStringList('.//dateline/*')

	def __init__(self, dom_node):
		self.dom_node = dom_node
		

class FullPoemList(QueryResult):
    fullPoems = XpathObjectList('fullPoem', FullPoem)


class DetailPoem(QueryResult):
	xmlFileName	= XpathString('.//xmlfilename')
	title       = XpathString('.//fileDesc/titleStmt/title')
	editor    	= XpathString('.//fileDesc/titleStmt/editor')
	author    	= XpathString('.//fileDesc/titleStmt/author')
	publisher 	= XpathString('.//sourceDesc/bibl/publisher')
	ptitle      = XpathString('.//sourceDesc/bibl/title')
	peditor    	= XpathString('.//sourceDesc/bibl/editor')
	pplace    	= XpathString('.//sourceDesc/bibl/pubPlace')
	pdate    	= XpathString('.//sourceDesc/bibl/date')
	heads    	= XpathObjectList('.//div/head', Head)
	paragraphs	= XpathObjectList('.//div/lg', Paragraph)
	byline      = XpathString('.//div/byline')
	dateline	= XpathStringList('.//div//dateline/*')

	#def __init__(self, dom_node):
	#	self.dom_node = dom_node
		

class DetailPoemList(QueryResult):
    fullPoems = XpathObjectList('fullPoem', DetailPoem)
    
class BriefVol(object):
	filename				=XpathString('xmlfilename')
	title					=XpathString('title')
	editor					=XpathString('editor')
	author					=XpathString('author')
	
	def __init__(self, dom_node):
		self.dom_node = dom_node
	
class BriefVolList(QueryResult):
    briefVols = XpathObjectList('briefvol', BriefVol)    		

class FrontComponent(object):
	id		= XpathString('@id')
	name	= XpathString('@n')
	fcType	= XpathString('@type')
	def __init__(self, dom_node):
		self.dom_node = dom_node
		
		
class EssayComponent(object):
	ecType 				= XpathString('@type')
	introductionContent = XpathStringList('./*')
	
	def __init__(self, dom_node):
		self.dom_node = dom_node
	
		
class SubBodyComponent(object):# poem or essay
	sbcType		= XpathString('@type')
	id			= XpathString('@id')
	title		= XpathString('head')
	author		= XpathString('docAuthor')
	isEssay		= XpathString('div[@type=\'poem\']/@id')
	#poem		= BriefPoem1('../')
	poems		= XpathObjectList('div[head]', BriefPoem1)
	
	def __init__(self, dom_node):
		self.dom_node = dom_node
	
	
class BodyComponent(object):#chapter, anthology, poetry
	id					= XpathString('@id')
	bcType				= XpathString('@type')
	title				= XpathString('head')
	name				= XpathString('@n')
	subBodyComponents	= XpathObjectList('div', SubBodyComponent)
	
	def __init__(self, dom_node):
		self.dom_node = dom_node		
		
class VolumeContent(QueryResult):# front, body
	#c = XpathString('''.//body//div[@id='clarke012']/@id''')
	frontComponents = XpathObjectList('vol/front/div', FrontComponent)
	bodyComponents	= XpathObjectList('vol/body/div', BodyComponent)
	
class ContentLine(object):
	rend = XpathString('@rend');
	content = XpathString('.');


class FrontContent(QueryResult):
	contentLines = XpathObjectList('.//*', ContentLine)
