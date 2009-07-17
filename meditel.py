# -*- coding: utf-8 -*-
""" Meditel sms sender  
    by Ali MEZGANI handrix@gmail.com 
    Licensed under GPL"""               

import httplib, sys, string, re, os

class Injector:

    def __init__(self, number, message, login, passwd):
        self.number = number
        self.message = message
	self.login = login
	self.passwd = passwd

    def post(self, host, selector, body, cookie):		
        h = httplib.HTTP(host)
        h.putrequest('POST', selector)
        h.putheader('HOST', host)
        h.putheader('User-Agent', "Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.8.1.9) Gecko/20071025 Firefox/2.0.0.9")
        h.putheader('Accept', "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5")
        h.putheader('Accept-Language', "fr,fr-fr;q=0.8,en-us;q=0.5,en;q=0.3")
        h.putheader('Accept-Encoding', "gzip,deflate")
        h.putheader('Accept-Charset', "ISO-8859-1,utf-8;q=0.7,*;q=0.7")
        h.putheader('Keep-Alive', '300')
        h.putheader('Connection', "keep-alive")
        h.putheader('Referer', "http://www.meditel.ma/clb/sms/index.jsp")
        if cookie:	
	      h.putheader('Cookie', cookie)
        h.putheader('content-type', "application/x-www-form-urlencoded")
        h.putheader('content-length', str(len(body)))
        h.endheaders()
        h.send(body)
        errcode, errmsg, headers = h.getreply()
        if cookie =='':
           tab=[]		
	   if headers.has_key("set-cookie"):
	       for line in headers.getallmatchingheaders ("set-cookie"):
		   header, value = string.split(line, ':', 1)
		   value=value.strip()
		   index=value.find(';')
		   tab.append(value[0:index])  
	       return tab


    def get(self, host, selector, cookie):		
        h = httplib.HTTP(host)
        h.putrequest('GET', selector)
        h.putheader('HOST', host)
        h.putheader('User-Agent', "Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.8.1.9) Gecko/20071025 Firefox/2.0.0.9")
        h.putheader('Accept', "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5")
        h.putheader('Accept-Language', "fr,fr-fr;q=0.8,en-us;q=0.5,en;q=0.3")
        h.putheader('Accept-Encoding', "gzip,deflate")
        h.putheader('Accept-Charset', "ISO-8859-1,utf-8;q=0.7,*;q=0.7")
        h.putheader('Keep-Alive', '300')
        h.putheader('Connection', "keep-alive")
        h.putheader('Referer', "http://www.meditel.ma/clb/sms/index.jsp")
        if cookie:	
	      h.putheader('Cookie', cookie)
       
        h.endheaders()
        errcode, errmsg, headers = h.getreply()
       

        
        if cookie =='':
           tab=[]		
	   if headers.has_key("set-cookie"):
	       for line in headers.getallmatchingheaders ("set-cookie"):
		   header, value = string.split(line, ':', 1)
		   value=value.strip()
		   index=value.find(';')
		   tab.append(value[0:index])  
	       return tab
        
        data=h.file.read()
        tab=re.findall('vous reste (\d+) SMS',data)
        return tab[0]
        
    


    def send(self):
	
        if len(self.number) != 10:
		sys.stderr.write("Mobile number is not valid\n")
	   	sys.exit(1)
		    
	for i in self.number:
		if i.isdigit():
	      		pass
	   	else:
			sys.stderr.write("Mobile number is not valid\n")
      			sys.exit(1)
		    
	if len(self.message) > 120:
         	sys.stderr.write("Message body is more than 120 char\n")
		sys.exit(1)
		     
	auth="from=sms&login="+self.login+"&mdp="+self.passwd
	value=self.post("www.meditel.ma","/clb/firstIdent.jsp",auth, '')
	cookie =value[0]+"; "+value[1]+"; "+value[2]+"; "+value[3]+"; "+value[4]
	nb=self.get("www.meditel.ma","/clb/sms/index.jsp", cookie)
	sms=int(nb)
	if sms > 0:
		body="langue=FR&compteur=108&message="+self.message+"&prefixe="+self.number[0:3]+"&tel="+self.number[3:]+"&choix=english"
		self.post("www.meditel.ma","/sms/smsSend",body, cookie)
		sms -= 1
	print >>sys.stdout, ("your sold is "+str(sms)+" SMS.")


	    
	
	
