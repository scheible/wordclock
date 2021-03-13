from os import listdir, symlink, remove
from os.path import isfile, join, exists, realpath, basename


def __getDirectory(baseDir, folders=False):
	if (not exists(baseDir)):
		return []

	dat = []
	for obj in listdir(baseDir):
		if isfile(join(baseDir, obj)) != folders:
			dat.append(obj)
	return dat

def __getFiles(baseDir):
	return __getDirectory(baseDir, False)

def __getFolders(baseDir):
	return __getDirectory(baseDir, True)


def getTimezoneCategories():
	baseDir = '/usr/share/zoneinfo'
	return __getFolders(baseDir)

def getTimezones(category):
	baseDir = join('/usr/share/zoneinfo', category)
	return __getFiles(baseDir)

def getCurrentTimeZone():
	baseDir = '/etc/localtime'
	print(basename(realpath(baseDir)))

def setTimezone(category, timeZone):
	zoneInfo = join('/usr/share/zoneinfo', category, timeZone)
	if (exists(zoneInfo) and exists('/etc/localtime')):
		remove('/etc/localtime')
		symlink(zoneInfo, '/etc/localtime')