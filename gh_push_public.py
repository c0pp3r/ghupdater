#!/usr/bin/python
import urllib2
import re
import xml.etree.ElementTree as ET
user = #YOUR USER HERE
passu = #YOUR PASSWORD HERE
galaxy = #GALAXY ID NUMBER FOR YOUR SERVER
planets = ['corellia','dantooine','dathomir','endor','lok','naboo','rori','talus','tatooine','yavin4']
global token

def login():
	sessionRE = re.compile("success-(.*)", re.I)
	url  = 'http://galaxyharvester.net/authUser.py?loginu=' + user + '&passu=' + passu
	response = urllib2.urlopen(url)
	html = response.read()
	token = sessionRE.match(html)
	#print token.group(1)
	return token.group(1)

def checkSpawn(name):
	url = 'http://galaxyharvester.net/getResourceByName.py?name=' + name + '&galaxy=' + galaxy
	response = urllib2.urlopen(url)
	xml = response.read()
	xmldoc = ET.fromstring(xml)
	result = xmldoc.find('resultText').text
	if result == 'new':
		return True
	else:
		return False

def readSpawnOutput(token):
	tree = ET.parse('/home/vagrant/workspace/Core3/MMOCoreORB/bin/scripts/managers/ghoutput.xml')
	root = tree.getroot()
	for resource in root.findall('resource'):
			name = resource.find('SpawnName').text
			res = resource.find('resType').text
			planet = resource.find('planet').text
			#print name + " " + res + " " + planet
			CR = ''
			CD = ''
			DR = ''
			FL = ''
			HR = ''
			MA = ''
			PE = ''
			OQ = ''
			SR = ''
			UT = ''
			ER = ''
			for attribute in resource.findall('attribute'):
				attname = attribute.get('name')
				stat = attribute.text
				if attname == 'res_cold_resist':
					CR = stat
				elif attname == 'res_conductivity':
					CD = stat
				elif attname == 'res_decay_resist':
					DR = stat
				elif attname == 'res_flavor':
					FL = stat
				elif attname == 'res_heat_resist':
					HR = stat
				elif attname == 'res_malleability':
					MA = stat
				elif attname == 'res_potential_energy':
					PE = stat
				elif attname == 'res_quality':
					OQ = stat
				elif attname == 'res_shock_resistance':
					SR = stat
				elif attname == 'res_toughness':
					UT = stat
				elif attname == 'entangle_resistance':
					ER = stat
			postSpawn(token, name, res, planet, CR, CD, DR, FL, HR, MA, PE, OQ, SR, UT, ER)

def postSpawn(token, name, res, planet, CR, CD, DR, FL, HR, MA, PE, OQ, SR, UT, ER):
	if planet == 'yavin4':
		planet = 'yaviniv'
	url = "http://galaxyharvester.net/postResource.py?galaxy=" + galaxy + "&planet=" + planet + "&resName=" + name + "&resType=" + res + "&CR=" + CR + "&CD=" + CD + "&DR=" + DR + "&FL=" + FL + "&HR=" + HR + "&MA=" + MA + "&PE=" + PE + "&OQ=" + OQ + "&SR=" + SR + "&UT=" + UT + "&ER=" + ER


	#print url
	opener = urllib2.build_opener()
	ghsid = 'gh_sid=' + token
	opener.addheaders.append(('Cookie', ghsid))
	response = opener.open(url)
	xml = response.read()
	xmldoc = ET.fromstring(xml)
	result = xmldoc.find('resultText').text
	print result

token = login()
readSpawnOutput(token)

