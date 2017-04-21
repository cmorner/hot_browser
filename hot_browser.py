#!/usr/bin/python2.7

import sys
import gtk
import requests
from bs4 import BeautifulSoup


class HotBrowser:
	# This function is run when a website is requested
	def navigateToWebsite(self, siteAdress):
		# Making a get request
		r = requests.get(siteAdress)
		responseHtml = r.text
		print "navigate to site: " + siteAdress
		
		# Set new url based on response
		self.setNewURL(r.url)
		self.parseHtml(responseHtml)

	# This function is run when the navigate to site button is clicked
	def navigateButtonClickAction(self, button):
		# Get site adress from input field
		siteAdress = self.searchField.get_text()
		self.navigateToWebsite(siteAdress)


	def parseHtml(self, html):
		soup = BeautifulSoup(html, "html.parser")
		siteTitle = soup.title.string

		#print soup.body


		self.setTitle(siteTitle)

		# Extract site contents
		siteContent = []
		def walker(soup):
			if soup.name is not None:
				for child in soup.children:
					#process node
					#print str(child.name) + ":" + str(type(child))
					

					#Only add content of relevant tags
					if (str(child.name) == "a"):
						siteContent.append(str(child.contents))
						siteContent.append(' '.join(str(elem) for elem in child.contents))
						#print "a: " + str(child.contents)

					if(str(child.name) == "p"):
						siteContent.append(str(child.contents))
						siteContent.append(' '.join(str(elem) for elem in child.contents))
						#print "p: " + str(child.contents)

					if(str(child.name) == "span"):
						siteContent.append(str(child.contents))
						siteContent.append(' '.join(str(elem) for elem in child.contents))	
						#print "span: " + str(child.contents)

					# If any header element
					# Converting list elements to str before joining them
					if(str(child.name)[0] == "h" and child.name[1] in ['1', '2', '3', '4', '5', '6']):
						siteContent.append(' '.join(str(elem) for elem in child.contents))
						#print "h" + str(child.name[1]) + ': ' + str(child.contents)

					if(str(child.name) == "b"):
						siteContent.append(str(child.contents))
						siteContent.append(' '.join(str(elem) for elem in child.contents))
						#print "b: " + str(child.contents)
					
					if(str(child.name) == "th"):
						siteContent.append(str(child.contents))
						siteContent.append(' '.join(str(elem) for elem in child.contents))
						#print "th: " + str(child.contents)

					walker(child)
 
		walker(soup)

		# Join each element with a newline
		siteContent = '\n'.join(siteContent)

		# Send site content to be displayed for user
		self.displayContent(siteContent)



	# Set url(str) based on response
	def setNewURL(self, url):
		self.searchField.set_text(url)

	# Function used to set the new title(str) of the window to the sites title
	def setTitle(self, title):
		print "Setting new title to: " + title
		self.window.set_title(title)
		#self.window.show()

	# Display content of website
	def displayContent(self, siteContent):
		self.siteContentBuffer.set_text(siteContent)

	def magicButton(self):
		self.setTitle("Magic is Loving")


	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title("Hot Browser")
		self.window.set_size_request(1024,600)
		self.window.connect("delete_event",gtk.main_quit)


		# Create an outer container VBox
		self.outerContainerBox = gtk.VBox()

		# Create an HBox container for the navigation bar
		self.navBarContainer = gtk.HBox()

		# Create the website adress field widget
		self.searchField = gtk.Entry(max=0)
		self.searchField.set_text("http://google.com")

		# Create the navigation button
		self.navigateButton = gtk.Button("Go")
		self.navigateButton.set_tooltip_text("Navigate to website")
		self.navigateButton.connect("clicked",self.navigateButtonClickAction)

		# Pack the navbar
		self.navBarContainer.pack_start(self.searchField, True)
		self.navBarContainer.pack_start(self.navigateButton, False)

		# Create a text buffer to display site content
		self.siteContentBuffer = gtk.TextBuffer()
		self.siteContentBuffer.set_text("HEY THERE!")
		
		# Create window where site content will be displayed
		self.siteContentHolder = gtk.TextView(self.siteContentBuffer)
		
		# Make site content not editable in this view
		self.siteContentHolder.set_editable(False)
		self.siteContentHolder.set_wrap_mode(gtk.WRAP_WORD)
		
		# Set margins of the TextView
		self.siteContentHolder.set_left_margin(15)
		self.siteContentHolder.set_right_margin(15)


		# Create a scrolled window to provide scrollbars to the main content window
		self.scrolledContentWindow = gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
		self.scrolledContentWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

		# Add TextView widget to scrolled window
		self.scrolledContentWindow.add_with_viewport(self.siteContentHolder)

		# Pack Navbar and Entry widget into outer cointainer
		self.outerContainerBox.pack_start(self.navBarContainer, False)
		self.outerContainerBox.pack_start(self.scrolledContentWindow, True)


		self.window.add(self.outerContainerBox)
		self.outerContainerBox.show()
		self.navBarContainer.show()
		self.navigateButton.show()
		self.searchField.show()
		self.scrolledContentWindow.show()
		self.siteContentHolder.show()


		self.window.show()

		# Get potential starting website passed as argument from terminal
		try:
			self.navigateToWebsite(sys.argv[1])
			print str(sys.argv[1])
		except Exception as e:
			print e.message

HB = HotBrowser()
gtk.main()