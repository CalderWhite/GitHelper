supported text editors:
	<untested> atom : https://atom.io/
	<untested> idle : https://www.python.org/ -> auto installed with python
	<untested> sublime text 2 : https://www.sublimetext.com/2
	<untested> sublime text 3 : https://www.sublimetext.com/3
KNOWN unsupported text editors:
	<untested> notepad : -> defaulty windows program
---------------------------
gitpanion should not be able to upload more that 2 500 files per hour.
the github api only allows 5 000 oauth requests per hour, and each file upload takes 1 - 2 requests.
(if the file exists, it will take 2. If it is a completely new file it takes 1 request)