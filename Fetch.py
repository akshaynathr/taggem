from bs4 import BeautifulSoup
import requests
import json

# function returns html formatted preview of input url, preview will contain title and image.




def fetch(url):
	
	# whlile I was halfway deving this function and s searching through for writing image fetcher, came across embed.ly
	# so here we go :p
	calling="http://api.embed.ly/1/oembed?key=958d6b531d2f4e3d80e5ce9de3b85e86&url="+url
	resp=requests.get(calling)
	response=(resp.json())
	htmlrendered="<a style='text-decoration:none' href='"+url+"'><table style='border: 1px solid #aaa'><tr><td>"
	imageurl=""
	title=""
	link=url
	text=""

	try:
		imageurl=response['thumbnail_url']
		width=response['thumbnail_width']
		height=response['thumbnail_height']
		 
		title=response['title']
	 
		text=response['description']

	except:
		pass
	if imageurl.replace(' ','') == '':
		imageurl='/static/assets/img/default_feed_icon.png'

	if title.replace(' ','')=='':
		title="Shared article"

	if text.replace(' ','') =='':
		text=title



	t={'imageurl':imageurl	,'title':title	,'link':link, 'description':text[:60] }
	print t

	return t



# html_formatted_preview('http://www.google.com')