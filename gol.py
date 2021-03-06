#!/usr/bin/python 

import sys
import os
import time

def cls():
	pass
	os.system(['clear','cls'][os.name == 'nt'])

DEFAULT_MAP="default.golm"

def filemap(filename=DEFAULT_MAP):
	try:
		f = open(filename, 'r')
	except:
		print "Cant open filename."
		return None
	world=f.read()
	# del last newline, which not have file
	if world[ len(world)-1 ] == '\n': world = world[:-1]
	f.close()

	# Get row and col count
	cc = list( len(x) for x in world.split("\n") )
	cols = max(cc)
	rows = len(cc)

	print "Cols: "+str(cols)+"\nRows: "+str(rows)

	golmap=list( list( False for x in range(cols) ) for y in range(rows) )

	for i in range(rows):
		for j in range(cols):
			try:
				if world.split("\n")[i][j] != 'o': golmap[i][j] = True
			except: pass
	return golmap

def readmap():
	world=str()

	print """Input:
		space for dead;
		any symbol for live
	"""

	# Input from console.
	while True:
		try:
			tmp=raw_input("")
			if world == "": world += tmp
			else: world += "\n"+tmp
		except:
			break

	# Get row and col count
	cc = list( len(x) for x in world.split("\n") )
	cols = max(cc)
	rows = len(cc)

	print "Cols: "+str(cols)+"\nRows: "+str(rows)

	golmap=list( list( False for x in range(cols) ) for y in range(rows) )

	for i in range(rows):
		for j in range(cols):
			try:
				if world.split("\n")[i][j] != ' ': golmap[i][j] = True
			except: pass
	return golmap

def printmap(golmap):
	print "__",
	for x in  range(len(golmap[0])): print '\b_',
	print
	for row in golmap:
		print "|",
		for life in row:
			if os.name == 'posix':
				if life: print '\b\033[0;32m'+"#"+'\033[0m',
				else: print '\b\033[0;30m'+"o"+'\033[0m',
			else:
				if life: print "\b#",
				else: print "\bo",
		print "|"
	print "--",
	for x in  range(len(golmap[0])): print '\b-',
	print

def savemap(gmap,foutpath=DEFAULT_MAP):
	f = open(foutpath, 'w')
	for row in gmap:
		for life in row:
			if life: f.write("*")
			else: f.write("o")
		f.write("\n")
	f.close()

def lifecount(gmap, x, y):
	cols = len( gmap  )
	rows = len( gmap[0] )

	count=0

	if gmap[x-1][y-1]: count += 1
	if gmap[x-1][y]: count += 1
	if gmap[x-1][ (y+1) % rows ]: count += 1


	if gmap[x][y-1]: count += 1
	if gmap[x][ (y+1) % rows ]: count += 1

	if gmap[ (x+1) % cols ][y-1]: count += 1
	if gmap[ (x+1) % cols ][y]: count += 1
	if gmap[ (x+1) % cols ][ (y+1) % rows ]: count += 1

	return count

def loop(gmap, timesteps, interactive=False):
	cls()
	printmap(gmap)
	print "Initial population."
	if interactive:
		try: raw_input("")
		except: return
	cls()
	leny=len(gmap)
	lenx=len(gmap[0])
	step=0
	prevstep=1
	prevprevstep=2
	while True:
		prevprevstep=prevstep
		prevstep=gmap
		step+=1
		cls()
		tmp = list( list( False for x in range(lenx) ) for y in range(leny) )
		born=0
		dead=0
		alive=0
		population=0
		for i in range(leny):
			for j in range(lenx):
				lc = lifecount(gmap,i,j)
				if gmap[i][j]: # Live cell
					if lc == 2 or lc == 3:
						alive+=1
						tmp[i][j]=True
					else:
						dead += 1
						tmp[i][j]=False
				else: # Dead cell
					if lc == 3:
						tmp[i][j]=True
						born+=1
		printmap(tmp)
		population = born+alive
		print "Step: "+str(step)+". Born: "+str(born)+". Dead: "+str(dead)+". Alive: "+str(alive)+". Population: "+str(population)
		trueexist=False
		for a in tmp:
			if True in a:
				trueexist=True
		if not trueexist:
			print "Exit on apocalypse."
			break
		if gmap == tmp:
			print "Exit on stopped evolution."
			break
		if tmp == prevprevstep:
			print "Exit on 2-step cycles."
			break
		gmap = tmp

		if timesteps:
			try: time.sleep(0.1)
			except: return step
		else:
			try:
				raw_input("")
			except: return step
	return step

def usage():
	print """USAGE:
	"""+sys.argv[0]+""" file [filename]
	"""+sys.argv[0]+""" filename
		game on a map from file, if filename not given - read from """+DEFAULT_MAP+"""

	"""+sys.argv[0]+""" cmd
	"""+sys.argv[0]+"""
		game on user input

	"""+sys.argv[0]+""" generate [filename]
		generate map then exit, if filename not given - write to """+DEFAULT_MAP+"""
	"""

if __name__ == "__main__":
	print "Game Of Life. a1fred."
	timesteps=True
	try:
		a = sys.argv.index("-n")
		timesteps=False
		del sys.argv[a]
	except:
		pass
	if len(sys.argv) == 1 or sys.argv[1] == "cmd":
		print "Starting game from input."
		gmap = readmap()
		if gmap:
			print "Loaded map:"
			ret = loop(gmap,timesteps)
			sys.exit(ret)
		sys.exit(0)
	if sys.argv[1] == "--help":
		usage()
		sys.exit(0)
	if sys.argv[1] in ("file", "f"):
		print "Starting game from file..."
		try: gmap = filemap(sys.argv[2])
		except: gmap = filemap()
		if gmap:
			print "Loaded map:"
			ret = loop(gmap,timesteps)
			sys.exit(ret)
		sys.exit(0)
	if sys.argv[1] in ("generate", "gen", "g"):
		print "Generating map..."
		gmap = readmap()
		if len(gmap[0]):
			print "\nStart map:"
			printmap(gmap)
			try:
				savemap(gmap, sys.argv[2])
				print "Map saved to "+sys.argv[2]+"."
			except:
				savemap(gmap)
				print "Map saved to "+DEFAULT_MAP+"."
		sys.exit(0)
	usage()

