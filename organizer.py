import json
import queue

class BookmarkOrganizer:
	def __init__(self, filename):
		with open(filename) as f:
			self.raw_text = f.read()
			self.bookmark_dict = dict()
	def jsonify(self):
		self.json_object = json.loads(self.raw_text)
		current_obj = self.json_object
		obj_queue = queue.Queue()
		obj_queue.put(current_obj)

		links_list = []
		self.dupes = []

		while True:
			# loop until queue is empty
			if obj_queue.empty():
				break
			current_obj = obj_queue.get()

			# if current_obj is a dict, then we can create a Bookmark from it.
			if type(current_obj) == dict:
				canUpdate = True
				b = Bookmark(current_obj['guid'], current_obj['title'], current_obj['dateAdded'], 
					current_obj['lastModified'], current_obj['id'], current_obj['typeCode'], 
					current_obj['type'])
				if 'uri' in current_obj:
					b.addUri(current_obj['uri'])
					# we have found a duplicate, therefore do not add to dict
					if current_obj['uri'] in links_list:
						canUpdate = False
					if canUpdate:
						links_list.append(current_obj['uri'])
					# just double checking for now
					else:
						self.dupes.append(b)
				if canUpdate:
					self.bookmark_dict.update({current_obj['id']: b})
			# if not an object, but a list.. we iterate through the list
			# adding all objects to the queue
			elif type(current_obj) == list:
				for l in current_obj:
					obj_queue.put(l)

			# if there are children elements (ie.. it's a folder and not a bookmark)
			# then we add the 'children' object to the queue (which is of type list)
			if 'children' in current_obj:
				obj_queue.put(current_obj['children'])
				#print('current_obj changed')
class Bookmark:
	def __init__(self, guid, title, dateadded, lastmodified, bmid, typecode, bmtype):
			self.guid = guid
			self.title = title
			self.dateadded = dateadded
			self.lastmodified = lastmodified
			self.bmid = bmid
			self.typecode = typecode
			self.bmtype = bmtype
			self.uri = ''
	def addUri(self, uri):
		self.uri = uri
	def __repr__(self):
		formatted_text = 'Bookmark( '
		if len(self.title) > 10:
			formatted_text += self.title[0: 10]
		else:
			formatted_text += self.title + ' - ' + self.uri + " )"

		if len(self.uri) > 40:
			formatted_text += ' - ' + self.uri[0:40] + " )"
		else:
			formatted_text += ' - ' + self.uri + " )"

		return formatted_text

class BookmarkOutputter:
	def __init__(self, bmdict, dupes):
		self.bmdict = bmdict
		self.dupes = dupes
	def outputAsHTML(self, filename):
		# this function creates an HTML file for all of the bookmarks
		# to make it easy to add them to my bookmarks with the use of 
		# an extension.
		with open(filename, "w") as f:
			f.write('<!DOCTYPE NETSCAPE-Bookmark-file-1>\n');
			f.write('<!-- This is an automatically generated file.\n')
			f.write('It will be read and overwritten.\n')
			f.write('DO NOT EDIT -->\n')
			f.write('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n')
			f.write('<TITLE>Bookmarks</TITLE>\n')
			f.write('<H1>Bookmarks</H1>\n')
			f.write('<DL>')
			f.write('<p>\n')
			f.write('\t<DT><H3 ADD_DATE="1566999799" LAST_MODIFIED="1569205326">Bookmarks Bar</H3>\n')
			f.write('\t<DL><p>\n')
			for o in self.bmdict:
				if self.bmdict[o].uri != '':
					if self.bmdict[o].title == '':
						title = 'No title. URL: '
						title += self.bmdict[o].uri
						self.bmdict[o].title = title
					print('Adding: ', self.bmdict[o].uri, ' ...')
					f.write('\t\t<DT><A HREF="' + self.bmdict[o].uri + '" ADD_DATE="' + str(self.bmdict[o].dateadded) + '">' + self.bmdict[o].title + '</A>\n')
				else:
					f.write('<H3>' + self.bmdict[o].title + '</H3>')
			#f.write(str(len(self.bmdict.values())))
			f.write('\t</DL>')
			f.write('<p>\n')
			f.write('</DL><p>')
			f.write('\n')

if __name__ == '__main__':
	x = BookmarkOrganizer('bookmarks-2018-10-19.json')
	x.jsonify()
	o = BookmarkOutputter(x.bookmark_dict, x.dupes)
	o.outputAsHTML('bookmarks-new.html')
	

