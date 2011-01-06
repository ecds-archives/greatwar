from eulcore.django.existdb.manager import Manager
from eulcore.django.existdb.models import XmlModel
from eulcore.xmlmap import XmlObject
from eulcore.xmlmap.dc import DublinCore
from eulcore.xmlmap.fields import StringField, NodeField, StringListField, NodeListField
from eulcore.xmlmap.teimap import Tei, TeiHeader, TeiDiv, TeiLineGroup, TEI_NAMESPACE


# TEI poetry models
# currently just slightly-modified versions of tei xmlmap objects



class PoetryBook(XmlModel, Tei):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    objects = Manager('/tei:TEI')

    project_desc = StringField('tei:teiHeader/tei:encodingDesc/tei:projectDesc')
    geo_coverage = StringField('tei:teiHeader/tei:profileDesc/tei:creation/tei:rs[@type="geography"]')
    creation_date = StringField('tei:teiHeader/tei:profileDesc/tei:creation/tei:date')
    lcsh_subjects = StringListField('tei:teiHeader//tei:keywords[@scheme="#lcsh"]/tei:list/tei:item')

    source_title = StringField('tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:title')
    source_author = StringField('tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:author')
    source_editor = StringField('tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:editor')
    source_publisher = StringField('tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:publisher')
    source_pubplace = StringField('tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:pubPlace')
    source_date = StringField('tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:date')

    

    @property
    def dublin_core(self):
        dc = DublinCore()
        dc.title = self.title
        dc.creator_list.extend([n.reg for n in self.header.author_list])
        dc.contributor_list.extend([n.reg for n in self.header.editor_list])
        dc.publisher = self.header.publisher
        dc.date = self.header.publication_date
        dc.rights = self.header.availability
        dc.source = self.header.source_description
        dc.subject_list.extend(self.lcsh_subjects)
        dc.description = self.project_desc

        if self.geo_coverage:
            dc.coverage_list.append(self.geo_coverage)
        if self.creation_date:
            dc.coverage_list.append(self.creation_date)

        if self.header.series_statement:
            dc.relation_list.append(self.header.series_statement)
        # FIXME: should we also include url? site name & url are currently
        # hard-coded when setting dc:relation in postcard ingest

        return dc

    def bibl(self):
        """Creates formatted citation from sourceDesc"""
        cit = {"author" : self.source_author, "editor": self.source_editor, "title" : self.source_title, "pubplace" : self.source_pubplace, "publisher" :  self.source_publisher, "date" : self.source_date }
       
           
        if cit['author']:  return "%(author)s, <i>%(title)s</i>. %(pubplace)s: %(publisher)s, %(date)s." % cit
        elif cit['editor']:  return "%(editor)s, ed., <i>%(title)s</i>. %(pubplace)s: %(publisher)s, %(date)s." % cit
        else: return "<i>%(title)s</i>. %(pubplace)s: %(publisher)s, %(date)s." % cit
        
        
class Poem(XmlModel, TeiDiv):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    poet = StringField("tei:docAuthor/tei:name/tei:choice")
    poetrev = StringField("tei:docAuthor/tei:name/tei:choice/tei:reg")
    nextdiv = NodeField("following::tei:div[@type='poem'][1]", "self")
    prevdiv = NodeField("preceding::tei:div[@type='poem'][1]", "self")
    poem = NodeField("tei:div[@type='poem']", "self")
    line_matches = NodeListField('tei:l',"self")   # place-holder: must be retrieved with raw xpath to use ft:query

    # reference to top-level elements, e.g. for retrieving a single div
    doctitle = StringField('ancestor::tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title')
    doc_id   = StringField('ancestor::tei:TEI/@xml:id')

    objects = Manager("//tei:div")
    # NOTE: this object could be restricted to poems only using [@type='poem']
    # However, it is currently used to retrieve non-poem items, e.g. essays
    # such as "Swan Song" in Eaton.  This should probably be re-thought; at the
    # very least, we may want to rename the model so it is more accurate.

class Poet(XmlModel, XmlObject):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    first_letter = StringField("substring(tei:reg,1,1)")
    name  = StringField("tei:reg")
    objects = Manager("//tei:div[@type='poem']/tei:docAuthor/tei:name/tei:choice")

class PoemSearch(Poem):
    # FIXME: consolidate with Poem? is this xpath appropriate for default Poem object?
    objects = Manager("//tei:div[@type='poem' or @type='play' or @type='story' or @type='essay']")
    #using PoemSearch to retrieve only poem-level objects in the search, not chapters or whole books
