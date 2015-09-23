import requests
import bs4
import re
import os

root_url = 'http://met.guc.edu.eg'
semester = '5'
semester_tag = 'Winter 2015'
major = 'Computer Science & Engineering'

cat_url = root_url + '/Courses/Catalogue.aspx?semester=' + semester
mat_url = root_url + '/Courses/Material.aspx?crsEdId='

def get_subjs():
    response = requests.get(cat_url)
    soup = bs4.BeautifulSoup(response.text,'lxml')
    elms = soup(text=re.compile(major))
    sub_list = []
    for elm in elms:
	div = elm.parent.parent.parent.parent
	link = div.a.attrs.get('href')
	response = requests.get(root_url + "/Courses/"  + link)
	soup = bs4.BeautifulSoup(response.text,'lxml')
	a = soup('a',text=re.compile(semester_tag))[0]  #.findAll(href=re.compile('crsEdId'))[0]  #.select('ul.materialList li a[href*=crsEdId]')[0]
	sub = {}
	sub['id'] = a.attrs.get('href').split("crsEdId=")[-1]	
	sub['name'] = div.a.string
	sub_list.append(sub)
    return sub_list

def get_mat_links(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text,'lxml')
    links = [a.attrs.get('href') for a in soup.select('ul.materialList li a[href$=".pdf"],a[href$=".ppt"],a[href$=".pptx"]')]
    return links

def save_mats(links,dir):
    for url in links:
        fname = os.path.join(dir,url.split("file=")[-1])
	if not os.path.exists(fname):
            response = requests.get(root_url + url[2:])
	    file = open(fname, 'w')
	    file.write(response.content)
	    file.close()

def main():
    subjs = get_subjs()
    for sbj in subjs:
	links = get_mat_links(mat_url + sbj['id'])
	directory = sbj['name']
	if not os.path.exists(directory):
    	    os.makedirs(directory)
	print("Downloading %s ..." % directory)
	save_mats(links,directory)

main()
