import os
from django.test import Client, TestCase
from django.http import QueryDict
from glob import glob
from django.conf import settings

from existdb.db import ExistDB
from edc.search.forms import SimpleSearchForm, BasicSearchForm, ExtendedSearchForm, SearchFormSet
from edc.search.views import xQry, xQry_by_id
from edc.search.models import *

def normalize_ws(s):
    return ' '.join(s.split())

class SimpleSearchTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('/search')
        self.assertEquals(response.status_code, 301)
        self.assertEquals(response['Location'], 'http://testserver/search/')

        response = self.client.get('/search/')
        self.assertEquals(response.status_code, 200)

        self.assertContains(response, 'Search all study abstracts for:', 1)

    def test_basic_get(self):
        data = {'var': u'\xf2'}
        response = self.client.get('/search/', data)
        self.assertEquals(response.status_code, 200)

class OneFieldXqryTest(TestCase):

    def test_field_error(self):
        response = self.client.get('/extended/',
            {"form-0-term": "Court",
             "form-0-field": "not_a_valid_field",
             "form-TOTAL_FORMS": "4",
             "form-INITIAL_FORMS": "0",
             }
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Search field is not valid', 1)

    def test_basic_xqry_title(self):
        form = BasicSearchForm(QueryDict("term=Court&field=title"))
        self.assertTrue(form.is_valid())

        xqry = '''import module namespace date="http://www.library.emory.edu/xquery/date" at
				  "xmldb:exist:///db/xquery-modules/date.xqm";

                  for $a in collection("/db%s")/codeBook[(docDscr/citation/titlStmt/titl &= 'Court' or docDscr/citation/titlStmt/IDNo = 'Court')][.|='Court']
                  let $matchcount := text:match-count($a)
                  order by $a/docDscr/citation/titlStmt/titl
			      return <codeBook>{$a/*} <hits>{$matchcount}</hits></codeBook>''' % (settings.EXISTDB_ROOT_COLLECTION, )

        self.assertEquals(normalize_ws(xQry([form.cleaned_data])), normalize_ws(xqry))
        self.assertEquals(form.pretty_print_query(), "Title or Study No: Court")

    def test_invalid_qry_field(self):
        #should default to title
        form = BasicSearchForm(QueryDict("term=Court&field=not_a_valid_field"))
        self.assertFalse(form.is_valid())

    def test_basic_xqry_abstract(self):
        form = BasicSearchForm(QueryDict("term=Court&field=abstract"))
        self.assertTrue(form.is_valid())

        xqry = '''import module namespace date="http://www.library.emory.edu/xquery/date" at
				  "xmldb:exist:///db/xquery-modules/date.xqm";

                  for $a in collection("/db%s")/codeBook[stdyDscr/stdyInfo/abstract &= 'Court'][.|='Court']
                  let $matchcount := text:match-count($a)
                  order by $a/docDscr/citation/titlStmt/titl
			      return <codeBook>{$a/*} <hits>{$matchcount}</hits></codeBook>''' % (settings.EXISTDB_ROOT_COLLECTION, )

        self.assertEquals(normalize_ws(xQry([form.cleaned_data])), normalize_ws(xqry))
        self.assertEquals(form.pretty_print_query(), "Abstract: Court")

    def test_basic_xqry_pi(self):
        form = BasicSearchForm(QueryDict("term=Court&field=pi"))
        self.assertTrue(form.is_valid())

        xqry = '''import module namespace date="http://www.library.emory.edu/xquery/date" at
				  "xmldb:exist:///db/xquery-modules/date.xqm";

                  for $a in collection("/db%s")/codeBook[stdyDscr/citation/rspStmt/AuthEnty &= 'Court'][.|='Court']
                  let $matchcount := text:match-count($a)
                  order by $a/docDscr/citation/titlStmt/titl
			      return <codeBook>{$a/*} <hits>{$matchcount}</hits></codeBook>''' % (settings.EXISTDB_ROOT_COLLECTION, )

        self.assertEquals(normalize_ws(xQry([form.cleaned_data])), normalize_ws(xqry))
        self.assertEquals(form.pretty_print_query(), "Principal Investigator: Court")

    def test_basic_xqry_subject(self):
        form = BasicSearchForm(QueryDict("term=Court&field=subject"))
        self.assertTrue(form.is_valid())

        xqry = '''import module namespace date="http://www.library.emory.edu/xquery/date" at
				  "xmldb:exist:///db/xquery-modules/date.xqm";

                  for $a in collection("/db%s")/codeBook[stdyDscr/stdyInfo/subject/keyword &= 'Court'][.|='Court']
                  let $matchcount := text:match-count($a)
                  order by $a/docDscr/citation/titlStmt/titl
			      return <codeBook>{$a/*} <hits>{$matchcount}</hits></codeBook>''' % (settings.EXISTDB_ROOT_COLLECTION, )

        self.assertEquals(normalize_ws(xQry([form.cleaned_data])), normalize_ws(xqry))
        self.assertEquals(form.pretty_print_query(), "Subject: Court")

    def test_basic_xqry_geoCover(self):
        form = BasicSearchForm(QueryDict("term=Court&field=geoCover"))
        self.assertTrue(form.is_valid())

        xqry = '''import module namespace date="http://www.library.emory.edu/xquery/date" at
				  "xmldb:exist:///db/xquery-modules/date.xqm";

                  for $a in collection("/db%s")/codeBook[stdyDscr/stdyInfo/sumDscr/geogCover &= 'Court'][.|='Court']
                  let $matchcount := text:match-count($a)
                  order by $a/docDscr/citation/titlStmt/titl
			      return <codeBook>{$a/*} <hits>{$matchcount}</hits></codeBook>''' % (settings.EXISTDB_ROOT_COLLECTION, )

        self.assertEquals(normalize_ws(xQry([form.cleaned_data])), normalize_ws(xqry))
        self.assertEquals(form.pretty_print_query(), "Geographic Coverage: Court")

    def test_basic_xqry_timePrd(self):
        form = BasicSearchForm(QueryDict("term=Court&field=timePrd"))
        self.assertTrue(form.is_valid())

        xqry = '''import module namespace date="http://www.library.emory.edu/xquery/date" at
				  "xmldb:exist:///db/xquery-modules/date.xqm";

                  for $a in collection("/db%s")/codeBook[stdyDscr/stdyInfo/sumDscr/timePrd/@date &= 'Court'][.|='Court']
                  let $matchcount := text:match-count($a)
                  order by $a/docDscr/citation/titlStmt/titl
			      return <codeBook>{$a/*} <hits>{$matchcount}</hits></codeBook>''' % (settings.EXISTDB_ROOT_COLLECTION, )

        self.assertEquals(normalize_ws(xQry([form.cleaned_data])), normalize_ws(xqry))
        self.assertEquals(form.pretty_print_query(), "Time Period: Court")

    def test_basic_xqry_escaped_xml(self):
        #test with url_encoding %27 = '
        form = BasicSearchForm(QueryDict("term=Court%27s&field=timePrd"))
        self.assertTrue(form.is_valid())

        xqry = '''import module namespace date="http://www.library.emory.edu/xquery/date" at
				  "xmldb:exist:///db/xquery-modules/date.xqm";

                  for $a in collection("/db%s")/codeBook[stdyDscr/stdyInfo/sumDscr/timePrd/@date &= 'Court&apos;s'][.|='Court&apos;s']
                  let $matchcount := text:match-count($a)
                  order by $a/docDscr/citation/titlStmt/titl
			      return <codeBook>{$a/*} <hits>{$matchcount}</hits></codeBook>''' % (settings.EXISTDB_ROOT_COLLECTION, )

        self.assertEquals(normalize_ws(xQry([form.cleaned_data])), normalize_ws(xqry))

        #test without url_encoding
        form = BasicSearchForm(QueryDict("term=Court's&field=timePrd"))
        self.assertTrue(form.is_valid())
        self.assertEquals(normalize_ws(xQry([form.cleaned_data])), normalize_ws(xqry))

    def test_escapeXml(self):
        form = BasicSearchForm()
        self.assertEquals(form.escapeXml("<"), "&lt;")
        self.assertEquals(form.escapeXml(">"), "&gt;")
        self.assertEquals(form.escapeXml("&"), "&amp;")
        self.assertEquals(form.escapeXml("'"), "&apos;")
        self.assertEquals(form.escapeXml('"'), "&quot;")
        self.assertEquals(form.escapeXml("a"), "a")
        self.assertEquals(form.escapeXml(""), "")

class TestQueryResults(TestCase):

    COLLECTION = settings.EXISTDB_ROOT_COLLECTION

    def setUp(self):
        self.db = ExistDB(resultType=CodeBookQueryResult)
        self.db.createCollection(self.COLLECTION, True)        

        #traverse exist_fixtures and load all xml files
        module_path = os.path.split(__file__)[0]
        fixtures_glob = os.path.join(module_path, 'exist_fixtures', '*.xml')
        for fixture in glob(fixtures_glob):
            fname = os.path.split(fixture)[-1]
            exist_fname = os.path.join(self.COLLECTION, fname)
            self.db.load(open(fixture), exist_fname, True)

    def tearDown(self):
        self.db.removeCollection(self.COLLECTION)

    def test_query_results(self):
        form = BasicSearchForm(QueryDict("term=139658501&field=title"))
        self.assertTrue(form.is_valid())
        
        res = self.db.query(xQry([form.cleaned_data], self.COLLECTION))
        self.assertEquals(res.hits, 1)

        self.assert_(isinstance(res, CodeBookQueryResult), "exist query result is correct type")
        self.assert_(isinstance(res.codeBooks[0], CodeBookResult), "codeBook result is correct type")
        self.assertEquals(res.codeBooks[0].hits, 2)

        self.assertEquals(len(res.codeBooks[0].authEnty), 1)
        self.assertEquals(res.codeBooks[0].authEnty[0], "Rob O'Reilly")
        self.assertEquals(res.codeBooks[0].title, "Cingranelli-Richards (CIRI) Human Rights Dataset")
        self.assertEquals(res.codeBooks[0].id, "139658501")
        self.assertEquals(len(res.codeBooks[0].principal_investigator), 2)
        self.assertEquals(res.codeBooks[0].principal_investigator[0], "David Louis Cingranelli")
        self.assertEquals(res.codeBooks[0].principal_investigator[1], "David L. Richards")
        self.assertEquals(res.codeBooks[0].otherID, "Other ID")
        self.assertEquals(res.codeBooks[0].copyright, "docDscr Copyright Statement")
        self.assertEquals(res.codeBooks[0].prodDate, "June 01, 2006")
        self.assertEquals(res.codeBooks[0].citation_version, "October 2005 Data Version")
        self.assertEquals(res.codeBooks[0].citation_verResp, "Rob O'Reilly")
        self.assertEquals(res.codeBooks[0].citation_notes, "This DDI instance for the October 2005 version of the Cingarelli-Richards Human Rights Dataset.")
        self.assertEquals(res.codeBooks[0].stdy_title, "Cingranelli-Richards (CIRI) Human Rights Dataset")
        self.assertEquals(res.codeBooks[0].stdy_subtitle, "subtitle")
        self.assertEquals(res.codeBooks[0].stdy_alttitle, "alttitle")
        self.assertEquals(len(res.codeBooks[0].stdy_authEntity), 2)
        self.assertEquals(res.codeBooks[0].stdy_authEntity[0], "David Louis Cingranelli")
        self.assertEquals(res.codeBooks[0].stdy_authEntity[1], "David L. Richards")
        self.assertEquals(res.codeBooks[0].stdy_version, "2005 Version")
        self.assertEquals(res.codeBooks[0].collection_size, "Really Big")
        self.assertEquals(res.codeBooks[0].stdy_notes, "This description of the CIRI Dataset refers to its contents as of 2006-06-01.  Note that the contents of the dataset may have changed since then.")
        self.assertEquals(len(res.codeBooks[0].subjectKeywords), 1)
        self.assertEquals(res.codeBooks[0].subjectKeywords[0], "Human Rights")
        self.assertEquals(len(res.codeBooks[0].subjectTopics), 1)
        self.assertEquals(res.codeBooks[0].subjectTopics[0], "Governance and Institutional Quality")
        self.assertEquals(res.codeBooks[0].universe, "Is Infinate")
        self.assertEquals(res.codeBooks[0].biblioCit, "Bibliographic Citation")
        self.assertEquals(len(res.codeBooks[0].versionHistory), 1)
        self.assertEquals(res.codeBooks[0].versionHistory[0], "2005 Version")
        self.assertEquals(normalize_ws(res.codeBooks[0].abstract), normalize_ws('The CIRI Human Rights Dataset contains data on government practices with regard to human rights, including variables on torture, religious freedom, "disappearances," and workers\' rights. The data cover the years 1981-2004.'))
        self.assertEquals(res.codeBooks[0].timePrd_start, "1981")
        self.assertEquals(res.codeBooks[0].timePrd_end, "2004")
        self.assertEquals(len(res.codeBooks[0].geoCoverages), 1)
        self.assertEquals(res.codeBooks[0].geoCoverages[0], "Global")
        self.assertEquals(len(res.codeBooks[0].nations), 195)
        self.assertEquals(res.codeBooks[0].nations[0], "Afghanistan")
        self.assertEquals(res.codeBooks[0].nations[194], "Zimbabwe")
        self.assertEquals(len(res.codeBooks[0].geoUnits), 1)
        self.assertEquals(res.codeBooks[0].geoUnits[0], "Countries")
        self.assertEquals(res.codeBooks[0].anlyUnit, "Country-Year")
        self.assertEquals(res.codeBooks[0].dataKind, "Country-Level Time-Series")
        self.assertEquals(res.codeBooks[0].stdyDscr_notes, "Data coverage will vary by country and year.")
        self.assertEquals(res.codeBooks[0].frequency, "Annual")
        self.assertEquals(res.codeBooks[0].cleanOps, "Clean Operations")
        self.assertEquals(res.codeBooks[0].method_notes, "Method Notes")
        self.assertEquals(len(res.codeBooks[0].locations), 2)
        # whitespace issues...
        self.assertEquals(res.codeBooks[0].locations[0], "CIRI")
        self.assertEquals(res.codeBooks[0].locations[1], "CIRI (SUNY-Binghamton address)")
        self.assertEquals(res.codeBooks[0].restriction, "Data are available to the public free of charge, though registration is required for access.")
        self.assertEquals(res.codeBooks[0].conditions, "Please see the FAQ for the authors' preferred format for citing the data.")
        self.assertEquals(res.codeBooks[0].access_notes, "Access Notes")
        self.assertEquals(res.codeBooks[0].file_notes, "File Notes")
        self.assertEquals(len(res.codeBooks[0].parts), 2)
        self.assert_(isinstance(res.codeBooks[0].parts[0], FileDscr), "codeBook part is type FileDscr")
        self.assertEquals(res.codeBooks[0].parts[0].id, None) # more accurate than '' - not present
        self.assertEquals(res.codeBooks[0].parts[0].filename, None) # more accurate than '' - not present
        self.assertEquals(res.codeBooks[0].parts[0].extLink, "http://ciri.binghamton.edu/index.asp")
        self.assertEquals(res.codeBooks[0].parts[0].fileType, "Data are available as Excel and comma-separated value files.")
        self.assertEquals(res.codeBooks[0].parts[1].id, "Sample")
        self.assertEquals(res.codeBooks[0].parts[1].filename, "Sample Filename")
        self.assertEquals(res.codeBooks[0].parts[1].fileType, "Data are available as comma-separated value files.")
        self.assertEquals(res.codeBooks[0].parts[1].fileStrc, "rectangular")
        self.assertEquals(res.codeBooks[0].parts[1].caseQnty, "200")
        self.assertEquals(res.codeBooks[0].parts[1].varQnty, "300")
        self.assertEquals(res.codeBooks[0].parts[1].logRecL, "6 FL")
        self.assertEquals(res.codeBooks[0].parts[1].recPrCas, "79.2")
        self.assertEquals(res.codeBooks[0].parts[1].extLink, "http://web.library.emory.edu")
        self.assertEquals(res.codeBooks[0].doi_id, None)
        self.assertEquals(res.codeBooks[0].doi_url, None)
        self.assertEquals(len(res.codeBooks[0].downloadable_files.files), 1)
        self.assertEquals(res.codeBooks[0].downloadable_files.files[0].name, "sp139658501-Supplemental_syntax.sps")

    def test_doi_id(self):
        res = self.db.query(xQry_by_id(3291, self.COLLECTION))
        self.assertEquals(res.hits, 1)

        self.assert_(isinstance(res, CodeBookQueryResult), "exist query result is correct type")
        self.assert_(isinstance(res.codeBooks[0], CodeBookResult), "codeBook result is correct type")
        self.assertEquals(res.codeBooks[0].doi_id, "10.3886/ICPSR03291")
        self.assertEquals(res.codeBooks[0].doi_url, "http://dx.doi.org/10.3886/ICPSR03291")

class TestSearchSummary(TestCase):

    COLLECTION = settings.EXISTDB_ROOT_COLLECTION

    def setUp(self):
        self.client = Client()
        self.db = ExistDB()
        self.db.createCollection(self.COLLECTION, True)

        #traverse exist_fixtures and load all xml files
        module_path = os.path.split(__file__)[0]
        fixtures_glob = os.path.join(module_path, 'exist_fixtures', '*.xml')
        for fixture in glob(fixtures_glob):
            fname = os.path.split(fixture)[-1]
            exist_fname = os.path.join(self.COLLECTION, fname)
            self.db.load(open(fixture), exist_fname, True)

    def tearDown(self):
        self.db.removeCollection(self.COLLECTION)

    def test_simple_search_summary_display(self):
        response = self.client.get('/search/', {"term":"data"})
        self.assertContains(response, 'class="row odd"', 5)
        self.assertContains(response, 'class="row even"', 5)
        self.assertContains(response, 'Page 1 of 1', 2)
        self.assertContains(response, 'Showing 1 - 10 of 10', 1)

    def test_extended_search_summary_display(self):
        #title contains Dataset or Institute
        qdict = QueryDict("operator=or&form-0-term=Dataset&form-0-field=title&form-1-term=Institute&form-1-field=title&form-2-term=&form-2-field=title&form-3-term=&form-3-field=title&form-TOTAL_FORMS=4&form-INITIAL_FORMS=0")
        response = self.client.get('/extended/', qdict)
        self.assertContains(response, 'class="row odd"', 2)
        self.assertContains(response, 'class="row even"', 2)
        self.assertContains(response, 'Page 1 of 1', 2)
        self.assertContains(response, 'Showing 1 - 4 of 4', 1)

class TestComplexQueries(TestCase):

    COLLECTION = settings.EXISTDB_ROOT_COLLECTION

    def setUp(self):
        self.client = Client()

    def test_display(self):
        response = self.client.get('/extended')
        self.assertEquals(response.status_code, 301)
        self.assertEquals(response['Location'], 'http://testserver/extended/')

        response = self.client.get('/extended/')
        self.assertEquals(response.status_code, 200)

        self.assertContains(response, 'Search all study abstracts for:', 1)
        self.assertContains(response, '<span class="searchHeading"> from the </span>', 4)

    def test_xqry_title(self):
        qdict = QueryDict("operator=and&form-0-term=Children's&form-0-field=title&form-1-term=&form-1-field=title&form-2-term=&form-2-field=title&form-3-term=&form-3-field=title&form-TOTAL_FORMS=4&form-INITIAL_FORMS=0")

        form = ExtendedSearchForm(qdict)
        formset = SearchFormSet(qdict)
        self.assertTrue(form.is_valid())
        self.assertTrue(formset.is_valid())

        #AND operator
        xqry = '''import module namespace date="http://www.library.emory.edu/xquery/date" at
				  "xmldb:exist:///db/xquery-modules/date.xqm";

                  for $a in collection("/db%s")/codeBook[(docDscr/citation/titlStmt/titl &= 'Children&apos;s' or docDscr/citation/titlStmt/IDNo = 'Children&apos;s')][.|='Children&apos;s']
                  let $matchcount := text:match-count($a)
                  order by $a/docDscr/citation/titlStmt/titl
			      return <codeBook>{$a/*} <hits>{$matchcount}</hits></codeBook>''' % (settings.EXISTDB_ROOT_COLLECTION, )

        self.assertEquals(
            normalize_ws(xQry(formset.cleaned_data, form.cleaned_data['operator'])),
            normalize_ws(xqry)
        )

        self.assertEquals(form.pretty_print_query(formset.forms), 'All fields match:<br/>Title or Study No: Children\'s')


    def test_xqry_title_and_title(self):
        qdict = QueryDict("operator=and&form-0-term=Children&form-0-field=title&form-1-term=dataset&form-1-field=title&form-2-term=&form-2-field=title&form-3-term=&form-3-field=title&form-TOTAL_FORMS=4&form-INITIAL_FORMS=0")

        form = ExtendedSearchForm(qdict)
        formset = SearchFormSet(qdict)
        self.assertTrue(form.is_valid())
        self.assertTrue(formset.is_valid())

        #AND operator
        xqry = '''import module namespace date="http://www.library.emory.edu/xquery/date" at
				  "xmldb:exist:///db/xquery-modules/date.xqm";

                  for $a in collection("/db%s")/codeBook[(docDscr/citation/titlStmt/titl &= 'Children'
                    or
                    docDscr/citation/titlStmt/IDNo = 'Children')

                    and

                    (docDscr/citation/titlStmt/titl &= 'dataset'
                    or docDscr/citation/titlStmt/IDNo = 'dataset')][.|='Children dataset']
                  let $matchcount := text:match-count($a)
                  order by $a/docDscr/citation/titlStmt/titl
			      return <codeBook>{$a/*} <hits>{$matchcount}</hits></codeBook>''' % (settings.EXISTDB_ROOT_COLLECTION, )

        self.assertEquals(
            normalize_ws(xQry(formset.cleaned_data, form.cleaned_data['operator'])),
            normalize_ws(xqry)
        )

        pretty = 'All fields match:<br/>Title or Study No: Children<br/>Title or Study No: dataset'
        self.assertEquals(form.pretty_print_query(formset.forms), pretty)

    def test_xqry_title_or_title(self):
        #term-0  = Children's
        #field-0 = title
        #term-1  = dataset
        #field-1 = title
        
        qdict = QueryDict("operator=or&form-0-term=Children's&form-0-field=title&form-1-term=dataset&form-1-field=title&form-2-term=&form-2-field=title&form-3-term=&form-3-field=title&form-TOTAL_FORMS=4&form-INITIAL_FORMS=0")

        form = ExtendedSearchForm(qdict)
        formset = SearchFormSet(qdict)
        self.assertTrue(form.is_valid())
        self.assertTrue(formset.is_valid())

        #AND operator
        xqry = '''import module namespace date="http://www.library.emory.edu/xquery/date" at
				  "xmldb:exist:///db/xquery-modules/date.xqm";

                  for $a in collection("/db%s")/codeBook[(docDscr/citation/titlStmt/titl &= 'Children&apos;s'
                  or docDscr/citation/titlStmt/IDNo = 'Children&apos;s')

                  or

                  (docDscr/citation/titlStmt/titl &= 'dataset'
                  or docDscr/citation/titlStmt/IDNo = 'dataset')][.|='Children&apos;s dataset']

                  let $matchcount := text:match-count($a)
                  order by $a/docDscr/citation/titlStmt/titl
			      return <codeBook>{$a/*} <hits>{$matchcount}</hits></codeBook>''' % (settings.EXISTDB_ROOT_COLLECTION, )

        self.assertEquals(
            normalize_ws(xQry(formset.cleaned_data, form.cleaned_data['operator'])),
            normalize_ws(xqry)
        )

        pretty = '''Any fields match:<br/>Title or Study No: Children's<br/>Title or Study No: dataset'''
        self.assertEquals(form.pretty_print_query(formset.forms), pretty)

    def test_xqry_by_id(self):
        xqry = '''import module namespace date="http://www.library.emory.edu/xquery/date" at
            "xmldb:exist:///db/xquery-modules/date.xqm";
            for $a in collection("/db%s")/codeBook[docDscr/citation/titlStmt/IDNo = '54321']
            return <codeBook>{$a/*}</codeBook>''' % (settings.EXISTDB_ROOT_COLLECTION, )

        self.assertEquals(normalize_ws(xQry_by_id(54321)), normalize_ws(xqry))

    def test_entireDoc(self):
        xqry = '''import module namespace date="http://www.library.emory.edu/xquery/date" at
            "xmldb:exist:///db/xquery-modules/date.xqm";
            for $a in collection("/db%s")/codeBook[. &= 'data'][.|='data']
            let $matchcount := text:match-count($a) order by $a/docDscr/citation/titlStmt/titl
            return <codeBook>{$a/*} <hits>{$matchcount}</hits></codeBook>''' % (settings.EXISTDB_ROOT_COLLECTION, )

        f = SimpleSearchForm({"term":"data"})
        self.assertTrue(f.is_valid())
        self.assertEquals(normalize_ws(xQry([f.cleaned_data])), normalize_ws(xqry))

        f = SimpleSearchForm({"term":"data", "field":"entireDoc"})
        self.assertTrue(f.is_valid())
        self.assertEquals(normalize_ws(xQry([f.cleaned_data])), normalize_ws(xqry))


class TestExtendedSearch(TestCase):
    def setup(self):
        self.client = Client()

    def test_title_or_title_search(self):
        qdict = QueryDict("operator=or&form-0-term=Children's&form-0-field=title&form-1-term=dataset&form-1-field=title&form-2-term=&form-2-field=title&form-3-term=&form-3-field=title&form-TOTAL_FORMS=4&form-INITIAL_FORMS=0")
        response = self.client.get('/extended/', qdict)
        self.assertEquals(response.status_code, 200)

class TestSearchWidget(TestCase):
    def setup(self):
        self.client = Client()

    def test_default_search(self):
        response = self.client.get('/widget/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, '<input id="id_term" type="text" name="term" maxlength="100" />', 1)


    def test_basic_search(self):
        response = self.client.get('/widget/basic/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, '<input id="id_term" type="text" name="term" maxlength="100" />', 1)

    def test_extended_search(self):
        response = self.client.get('/widget/extended/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, '<option value="title">Title + Study No.</option>', 4)

class TestDownloadableDocuments(TestCase):
    def test_single(self):
        d = DownloadableDocuments('4521')

        self.assertEquals(len(d.files), 1)
        self.assertEquals(d.files[0].href, "http://einstein.library.emory.edu.proxy.library.emory.edu/pub/ICPSR/why_are_these_necessary/4521/TermsOfUse.html")
        self.assertEquals(d.files[0].dir, "why_are_these_necessary/4521")
        self.assertEquals(d.files[0].size, "3459 bytes")
        self.assertEquals(d.files[0].name, "TermsOfUse.html")

    def test_multiple(self):
        d = DownloadableDocuments('0001')

        self.assertEquals(len(d.files), 3)
        self.assertEquals(d.files[0].href, "http://einstein.library.emory.edu.proxy.library.emory.edu/pub/ICPSR/something_meaningless/0001/da0001.sav")
        self.assertEquals(d.files[0].dir, "something_meaningless/0001")
        self.assertEquals(d.files[0].size, "36 bytes")
        self.assertEquals(d.files[0].name, "da0001.sav")

        self.assertEquals(d.files[1].href, "http://einstein.library.emory.edu.proxy.library.emory.edu/pub/ICPSR/something_meaningless/0001/cb0001.Codebook.pdf")
        self.assertEquals(d.files[1].dir, "something_meaningless/0001")
        self.assertEquals(d.files[1].size, "36 bytes")
        self.assertEquals(d.files[1].name, "cb0001.Codebook.pdf")

        self.assertEquals(d.files[2].href, "http://einstein.library.emory.edu.proxy.library.emory.edu/pub/ICPSR/something_meaningless/0001/da0001.por")
        self.assertEquals(d.files[2].dir, "something_meaningless/0001")
        self.assertEquals(d.files[2].size, "36 bytes")
        self.assertEquals(d.files[2].name, "da0001.por")

    def test_no_match(self):
        d = DownloadableDocuments('NO_MATCH')
        self.assertEquals(len(d.files), 0)

    def test_group_for_display(self):
        group = DownloadableDocuments('4521').group_for_display()
        self.assertEquals(group.keys(), ['other files'])
        self.assertEquals(len(group['other files']), 1)
        self.assertEquals(group['other files'][0].name, 'TermsOfUse.html')

        group = DownloadableDocuments('0001').group_for_display()
        self.assertEquals(group.keys(), ['SPSS data', 'code book'])
        self.assertEquals(len(group['SPSS data']), 2)        
        self.assertEquals(group['SPSS data'][0].name, "da0001.sav")
        self.assertEquals(group['SPSS data'][1].name, "da0001.por")
        self.assertEquals(len(group['code book']), 1)
        self.assertEquals(group['code book'][0].name, "cb0001.Codebook.pdf")

        group = DownloadableDocuments('NO_MATCH').group_for_display()
        self.assertEquals(len(group), 0)
        
