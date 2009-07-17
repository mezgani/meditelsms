# -*- coding: utf-8 -*-
import meditel
import os
import sys

login="login"
passwd="password"

if __name__=="__main__":
	if len(sys.argv) != 2:
		sys.stderr.write("Usage: %s number\n" % sys.argv[0])
		sys.stderr.write("Example: echo \"hello meditel\" | python sms.py 0669119530\n")
                sys.exit(2)
	
	number=sys.argv[1]
	message=raw_input()
	sms=meditel.Injector(number,message,login,passwd)
	sms.send()
	
