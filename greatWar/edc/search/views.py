from django.http import HttpResponse
from django import forms
from django.shortcuts import render_to_response
from existdb.db import ExistDB, ResultPaginator,ExistDBException
from edc.search.forms import SimpleSearchForm, ExtendedSearchForm, SearchFormSet,BasicSearchForm,BasicSearchBox,AdvancedSearchBox
from edc.search.models import CodeBookQueryResult, BookStoreQueryResult,BookQueryResult,BookResult,BookDetailResult,BookDetailQueryResult,BriefPoemList,FullPoemList,BriefVolList,BriefPoemList1,DetailPoem,VolumeContent,FrontContent
from django.forms.formsets import BaseFormSet, ValidationError
from django.conf import settings

PER_PAGE = 10

#display/process basic search from
def index(request):
    return renderForm(SimpleSearchForm, request, 'search/basic.xhtml', 'search')
    
def index_test(request):
    return renderForm_test(BasicSearchForm, request, 'search/basic_test.xhtml', 'search')
    
    
def book_detail(request,book_id):
    db = ExistDB(resultType=BookDetailQueryResult)
    results = db.query(xQry_by_id(book_id))
    return  render_to_response('search/show_test.xhtml', {
                        'data': results.books,
                        'book_id':        book_id,
                        'app_root':         request.META['SCRIPT_NAME'],
                        'previous_page':    request.GET.get('search_type', None),
                        'previous_data':    request.META['QUERY_STRING']
                        })
          
def poem_detail(request, parent_type,poem_id):
    db = ExistDB(resultType=DetailPoem)
    xQry = xQry_by_id1(poem_id)
    results = db.query(xQry)
    #assert False
    return  render_to_response('poetry/view.xhtml', {
                        'fullPoem': results,
                            'basicSearchBox': BasicSearchBox()
                        })
                  
def extended(request):
    return renderForm(SearchFormSet, request, 'search/extended.xhtml', 'extended')

def study(request, book_id):
    db = ExistDB(resultType=CodeBookQueryResult)
    results = db.query(xQry_by_id(survey_id))

    return  render_to_response('search/show.xhtml', {
                        'data': results.codeBooks,
                        'survey_id':        survey_id,
                        'app_root':         request.META['SCRIPT_NAME'],
                        'previous_page':    request.GET.get('search_type', None),
                        'previous_data':    request.META['QUERY_STRING']
                        })

def download(request, survey_id):
    db = ExistDB(resultType=CodeBookQueryResult)
    results = db.query(xQry_by_id(survey_id))

    return  render_to_response('search/download.xhtml', {
                        'data': results.codeBooks,
                        'survey_id':        survey_id,
                        'app_root':         request.META['SCRIPT_NAME'],
                        'previous_page':    request.GET.get('search_type', None ),
                        'previous_data':    request.META['QUERY_STRING']
                        })

def widget(request, type='simple'):
    if type == 'extended':
        return extended(request)
    else:
        return index(request)

#HELPER METHODS
def xQry(filter_list, condition='and', collection=settings.EXISTDB_ROOT_COLLECTION):

    filters = []
    terms   = []
    for f in filter_list:
        if ('field' not in f):
            key = 'entireDoc'
        else:
            key = f['field']

        if f['term'] != '':
            search_filter = {}
            search_filter['title']      = "(docDscr/citation/titlStmt/titl &= '%(term)s' or docDscr/citation/titlStmt/IDNo = '%(term)s')" % {'term': f['term']}
            search_filter['abstract']   = "stdyDscr/stdyInfo/abstract &= '%(term)s'" % {'term': f['term']}
            search_filter['pi']         = "stdyDscr/citation/rspStmt/AuthEnty &= '%(term)s'" % {'term': f['term']}
            search_filter['subject']    = "stdyDscr/stdyInfo/subject/keyword &= '%(term)s'" % {'term': f['term']}
            search_filter['geoCover']   = "stdyDscr/stdyInfo/sumDscr/geogCover &= '%(term)s'" % {'term': f['term']}
            search_filter['timePrd']    = "stdyDscr/stdyInfo/sumDscr/timePrd/@date &= '%(term)s'" % {'term': f['term']}
            search_filter['entireDoc']   = ". &= '%(term)s'" % {'term': f['term']}

            filters.append(search_filter[key])
            terms.append(f['term'])

   # import module namespace date="http://www.library.emory.edu/xquery/date" at
    #          "xmldb:exist:///db/xquery-modules/date.xqm";
	xqry = '''for $a in collection("/db%(collection)s")/codeBook[%(filter)s][.|='%(terms)s']
              let $matchcount := text:match-count($a)
              order by $a/docDscr/citation/titlStmt/titl
              return <codeBook>{$a/*} <hits>{$matchcount}</hits></codeBook>'''
    
    return xqry % {'filter': condition.join(filters), 'terms': ' '.join(terms), 'collection': collection}
    
    
    
def xQry2(qry_data, collection=settings.EXISTDB_ROOT_COLLECTION):
	filter1=[]
	filter2=[]
	filter3=[]
	filter4=["@type=\"poem\""]
	filler1=""
	filler2=""
	filler3=""
	filler4=""
	
	if 'author' in qry_data:
		if qry_data['author']!='':
			filter1.append("docAuthor&=\"%(term)s\"" % {'term':qry_data['author']})
			filter4.append("docAuthor&=\"%(term)s\"" % {'term':qry_data['author']})
	if 'date' in qry_data:
		if qry_data['date']!='':
			filter1.append(".//bibl/date='%(term)s'" % {'term':qry_data['date']})
			filter3.append(".//bibl/date='%(term)s'" % {'term':qry_data['date']})
		
	if 'title' in qry_data:
		if qry_data['title']!='':
			filter2.append("head&=\"%(term)s\"" % {'term':qry_data['title']})
	if 'term' in qry_data:
		if qry_data['term']!='':
			filter2.append(".//l&=\"%(term)s\"" % {'term':qry_data['term']});
		
	if filter1:
		filler1="[%(term)s]" % {'term':' and '.join(filter1)}
	if filter2:
		filler2="where $poem[%(term)s]" % {'term':' and '.join(filter2)}
	if filter3:
		filler3="[%(term)s]" % {'term':' and '.join(filter3)}
	filler4="[%(term)s]" % {'term':' and '.join(filter4)}
	
	xqry = '''for $vol in collection("/db%(collection)s")/TEI.2
			return
			if ($vol//div/@type='Poetry')
			then for $poem in $vol//div%(filler1)s//div[@type="Poem"]
					%(filler2)s
					return <briefPoem><id>{data($poem/@id)}</id><author>{data($vol//div/docAuthor)}</author><title>{data($poem/head)}</title></briefPoem>
			else for $poem in $vol%(filler3)s//div%(filler4)s
					%(filler2)s
					return <briefPoem><id>{data($poem/@id)}</id><author>{data($poem/docAuthor)}</author><title>{data($poem/head)}</title></briefPoem>'''
	return xqry % {'collection': collection,'filler1':filler1,'filler2':filler2,'filler3':filler3,'filler4':filler4}
    
    
def xQry4(qry_data, collection=settings.EXISTDB_ROOT_COLLECTION):
	filter1=[]
	filter2=[]
	filter3=[]
	filter4=["@type=\"poem\""]
	filler1=""
	filler2=""
	filler3=""
	filler4=""
	
	if 'author' in qry_data:
		if qry_data['author']!='':
			filter1.append("docAuthor&=\"%(term)s\"" % {'term':qry_data['author']})
			filter4.append("docAuthor&=\"%(term)s\"" % {'term':qry_data['author']})
	if 'date' in qry_data:
		if qry_data['date']!='':
			filter1.append(".//bibl/date='%(term)s'" % {'term':qry_data['date']})
			filter3.append(".//bibl/date='%(term)s'" % {'term':qry_data['date']})
		
	if 'title' in qry_data:
		if qry_data['title']!='':
			filter2.append("head&=\"%(term)s\"" % {'term':qry_data['title']})
	if 'term' in qry_data:
		if qry_data['term']!='':
			filter2.append(".//l&=\"%(term)s\"" % {'term':qry_data['term']});
		
	if filter1:
		filler1="[%(term)s]" % {'term':' and '.join(filter1)}
	if filter2:
		filler2="where $poem[%(term)s]" % {'term':' and '.join(filter2)}
	if filter3:
		filler3="[%(term)s]" % {'term':' and '.join(filter3)}
	filler4="[%(term)s]" % {'term':' and '.join(filter4)}
	
	xqry = '''for $vol in collection("/db%(collection)s")/TEI.2
			return
			if ($vol//div/@type='Poetry')
			then for $poem in $vol//div%(filler1)s//div[@type="Poem"]
					%(filler2)s
					return <div>{$poem/*}<docAuthor>{data($vol//div/docAuthor)}</docAuthor></div>
			else for $poem in $vol%(filler3)s//div%(filler4)s
					%(filler2)s
					return $poem'''
	return xqry % {'collection': collection,'filler1':filler1,'filler2':filler2,'filler3':filler3,'filler4':filler4}

def xQry1(filter_list, condition='and', collection=settings.EXISTDB_ROOT_COLLECTION):

    filters = []
    terms   = []
    for f in filter_list:
        if ('field' not in f):
            key = 'entireDoc'
        else:
            key = f['field']
	xqry = '''for $a in collection("/db%(collection)s")/bookstore/book[title&='%(searchterm)s'] 
              return <book>{$a/*}</book>'''
    return xqry % {'collection': collection,'searchterm':f['term']}

def xQry_by_id(id, collection=settings.EXISTDB_ROOT_COLLECTION):
	#'''import module namespace date="http://www.library.emory.edu/xquery/date" at
	#      "xmldb:exist:///db/xquery-modules/date.xqm";
	return '''for $vol in collection("/db%(collection)s")/TEI.2
			let $poem := $vol//div[@id='%(id)s']
			where  $vol//div[@id='%(id)s']
			return <fullPoem><title>{data($vol/teiHeader/fileDesc/titleStmt/title)}</title>
			<editor>{data($vol/teiHeader/fileDesc/titleStmt/editor)}</editor>
			<ptitle>{data($vol//sourceDesc//bibl/title)}</ptitle>
			<peditor>{data($vol//sourceDesc//bibl/editor)}</peditor>
			<pplace>{data($vol//sourceDesc//bibl/pubPlace)}</pplace>
			<publisher>{data($vol//sourceDesc//bibl/publisher)}</publisher>
			<pdate>{data($vol//sourceDesc//bibl/date)}</pdate>
			{$poem/*}</fullPoem>''' % {'id': id, 'collection': collection}

def xQry_by_id1(id, collection=settings.EXISTDB_ROOT_COLLECTION):
	#'''import module namespace date="http://www.library.emory.edu/xquery/date" at
	#      "xmldb:exist:///db/xquery-modules/date.xqm";
		#	<xmlfilename>{substring-after(substring-before(substring-after(document-uri($doc),static-base-uri()),'.'),'/')}</xmlfilename>
	return '''for $doc in collection("/db%(collection)s")[TEI.2]
			let $poem := $doc//div[@id='%(id)s']
			where  $doc//div[@id='%(id)s']
			return <fullPoem>
			<xmlfilename>{substring-before(substring-after(substring-after(substring-after(document-uri($doc),'/'),'/'),'/'),'.')}</xmlfilename>
			{$doc/TEI.2/teiHeader}{$poem}
			</fullPoem>''' % {'id': id, 'collection': collection}

def xQry_volume_browse(collection=settings.EXISTDB_ROOT_COLLECTION):
	return '''for $doc in collection("/db%(collection)s")[TEI.2]
				return <briefvol>
				<xmlfilename>{substring-before(substring-after(substring-after(substring-after(document-uri($doc),'/'),'/'),'/'),'.')}</xmlfilename> 
				{$doc//fileDesc//titleStmt/*}
				</briefvol>''' % {'collection': collection}

def xQry_volume_content(filename,collection=settings.EXISTDB_ROOT_COLLECTION):
	return '''for $d in doc("/db%(collection)s/%(xmlFile)s")
		return <vol>{$d/TEI.2/text/*}</vol>''' % {'xmlFile':'.'.join([filename,'xml']), 'collection': collection}

def xQry_front_content(divId,collection=settings.EXISTDB_ROOT_COLLECTION):
	return '''for $content in collection("/db%(collection)s")//div[@id='%(id)s']/*
		return <frontcontent>{data($content)}</frontcontent>''' % {'id':divId, 'collection': collection}
	
def opening_page(request):
	if (request.GET):
		basicSearchBox = BasicSearchBox(request.GET)
		if basicSearchBox.is_valid():
			try:
				epg = int(request.GET.get('epg', 20))
			except ValueError:
				epg = 20
			try:
				start = ((int(request.GET.get('page', 1)) - 1) * epg) + 1
			except ValueError:
				start = 1
			search_data = basicSearchBox.cleaned_data
			#return HttpResponse(search_data['term'])
			#store request data for review on subsequent pages
			request.session['form_data'] = basicSearchBox.data
			#assert False
			try:
				db = ExistDB(resultType=BriefPoemList1)
				xqry=xQry4(search_data)
				
				results = db.query(xqry, start=start, how_many=epg)
				paginator = ResultPaginator(results, results.briefPoems)
				results_list = paginator.page(request.GET.get('page', '1'))
			except ExistDBException:
				return render_to_response("searchException.xhtml",{'errorMessage':'Exist data base exception',
                            'basicSearchBox': BasicSearchBox()})
			rqst = request.GET.copy()
			
			if('page' in rqst):
				rqst.pop('page')
			if('epg' in rqst):
				rqst.pop('epg')
			
			return render_to_response('poetry/search.xhtml', {
                            'result_list':      results_list,
                            'count':results.hits,
                            'epg':epg,
                            'qry_data':rqst.urlencode(),
                            'basicSearchBox': BasicSearchBox()})
		else:
			return render_to_response("searchException.xhtml",{'errorMessage':basicSearchBox.non_field_errors(),
                            'basicSearchBox': BasicSearchBox()})
	else:
		basicSearchBox=BasicSearchBox()
		return render_to_response('index.html', {'css_link':settings.CSS_LINK,'basicSearchBox' : basicSearchBox})
		
		
def advancedSearch(request):
	if (request.GET):
		advancedSearchBox = AdvancedSearchBox(request.GET)
		#assert False
		if advancedSearchBox.is_valid():
			try:
				epg = int(request.GET.get('epg', 20))
			except ValueError:
				epg = 20
			try:
				start = ((int(request.GET.get('page', 1)) - 1) * PER_PAGE) + 1
			except ValueError:
				start = 1
			search_data = advancedSearchBox.cleaned_data
			#store request data for review on subsequent pages
			request.session['form_data'] = advancedSearchBox.data
                
			#db = ExistDB(resultType=BriefPoemList)
			#xqry=xQry2(search_data)
			db = ExistDB(resultType=BriefPoemList1)
			xqry=xQry4(search_data)
			#assert False
			results = db.query(xqry, start=start, how_many=epg)
			paginator = ResultPaginator(results, results.briefPoems)
			results_list = paginator.page(request.GET.get('page', '1'))
			
			rqst = request.GET.copy()
			if('page' in rqst):
				rqst.pop('page')
			if('epg' in rqst):
				rqst.pop('epg')
			return render_to_response('poetry/search.xhtml', {
                            'result_list':results_list,
                            'count':results.hits,
                            'epg':epg,
                            'qry_data':rqst.urlencode(),
                            'basicSearchBox': BasicSearchBox()})
		else:
			return render_to_response("searchException.xhtml",{'errorMessage':advancedSearchBox.non_field_errors(),
                            'basicSearchBox': BasicSearchBox()})
	else:
		advancedSearchBox=AdvancedSearchBox()
		return render_to_response('poetry/searchform.xhtml', {'advancedSearchBox' : advancedSearchBox,
                            'basicSearchBox': BasicSearchBox()})
	
	
def volume_browse(request):
	db = ExistDB(resultType=BriefVolList)
	xqry=xQry_volume_browse()
	results = db.query(xqry)
	return render_to_response('poetry/browse.xhtml', {
                            'result_list': results.briefVols,
                            'basicSearchBox': BasicSearchBox()})
	
def volumeContent(request, volfile):
	db = ExistDB(resultType=VolumeContent)
	xqry=xQry_volume_content(volfile)
	results = db.query(xqry)
	#assert False
	return render_to_response('poetry/contents.xhtml', {
                            'volumeContent': results,
                            'basicSearchBox': BasicSearchBox()})
                            
                            
def front_detail(request, div_id):
	db = ExistDB(resultType=FrontContent)
	xqry=xQry_front_content(div_id)
	results = db.query(xqry)
	#assert False
	return render_to_response('poetry/front.xhtml', {
                            'frontContent': results,
                            'basicSearchBox': BasicSearchBox()})
	
def about(request):
	return render_to_response('about.xhtml',{'basicSearchBox': BasicSearchBox()})

def credits(request):
	return render_to_response('credits.xhtml',{'basicSearchBox': BasicSearchBox()})

def underconstruction(request):
	return render_to_response('underconstruction.xhtml',{'basicSearchBox': BasicSearchBox()})





	
