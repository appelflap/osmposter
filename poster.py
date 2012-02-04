import Image, ImageDraw, sys, os, time, re

global application_name, version_number
global filename, top_tile, left_tile, height, width, server_url, zoom, styleId

version_number = "0.0.2"
server_url = "http://a.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/{styleId}/{tilesize}/{z}/{x}/{y}.png"
zoom = 18
tilesize = 256
styleId = 1
dirname= "tiles.tmp"
sleep = 1

def execute_cmd(cmd):
	value = os.system(cmd)
	if value != 0: raise Exception(cmd + " failed.") 

def clean():
	print "Deleting temporary files..."
	if os.path.isdir(dirname):
		execute_cmd("rm -R "+dirname)

def download_tiles():
	clean()
	execute_cmd("mkdir "+dirname)

	global server_url

	print "Downloading "+str((int(height)/tilesize + 1)*(int(width)/tilesize + 1))+" tiles",
	for x in range(0, int(height)/tilesize + 1):
		for y in range(0, int(width)/tilesize + 1):
			tmp_url = re.sub('{x}', str(int(top_tile) + x), server_url)
			tmp_url = re.sub('{y}', str(int(left_tile) + y), tmp_url)
			execute_cmd("wget -qO "+dirname+"/"+ str(x) + "_" + str(y) + ".png " + tmp_url)
			print ".",
			sys.stdout.flush()
		time.sleep(sleep)
	print ""

def generate_poster():
	img = Image.new("RGBA", (int(width), int(height)))

	print "Placing tiles..."
	for x in range(0, int(width)/tilesize + 1):
		for y in range(0, int(height)/tilesize + 1):
			tile = Image.open(dirname+"/" + str(x) + "_" + str(y) + ".png")
			img.paste(tile, (x * tilesize, y * tilesize))
	img.save(filename)
	print "Your file is now available as "+filename
	return


def version():
	print "This is " + application_name + " " + version_number

def help():
	version()
	print ""
	print "Usage: " + sys.argv[0] + " filename top_tile left_tile height width [zoom [server_url [tilesize [styleId]]]]"
	print ""
	print ""
	
	print " == Parameter specification =="
	print "  "
	print "  * filename      - the filename of the resulting image (supported formats include .png, .jpg and others)"
	print "  * top_tile      - number of the top tiles (see below)"
	print "  * left_tile     - number of the left tiles (see below)"
	print "  * height        - height of the resulting image in pixels"
	print "  * width         - width of the resulting image in pixels"
	print "  * zoom          - zoomlevel 1-18, default 16"
	print "  "
	print "  * server_url    - should contain the following variables"
	print "                    {x}       -> x position variable"
	print "                    {y}       -> y position variable"
	print "                    optional:"
	print "                    {s}       -> tile mirror. comma separated server mirrors, example: a,b,c (not yet available)"
	print "                    {z}       -> zoom"
	print "                    {styleId} -> styleId for CloudMade urls. You can also just incorporate it into the url, default: 1"
	print "  "
	print "                    e.g. 'http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/{styleId}/{tilesize}/{z}/{x}/{y}.png'"
	print "  "
	print "  * tilesize      - in pixels, default: 256"
	print "  * styleId       - CloudMade style id, default: 1"

#Main program
if len(sys.argv) > 5:
	filename = sys.argv[1]
	top_tile = sys.argv[2]
	left_tile = sys.argv[3]
	height = sys.argv[4]
	width = sys.argv[5]
	if len(sys.argv) > 6: zoom = sys.argv[6]
	if len(sys.argv) > 7: server_url = str(sys.argv[7])
	if len(sys.argv) > 8: tile4size = sys.argv[8]
	if len(sys.argv) > 9: styleId = sys.argv[9]
	
	server_url = re.sub('{styleId}', str(styleId), server_url)
	server_url = re.sub('{tilesize}', str(tilesize), server_url)
	server_url = re.sub('{z}', str(zoom), server_url)
	
	tilesize = int(tilesize)
	download_tiles()
	generate_poster()
else:
	print "FAILED: You need to specifiy all attributes."
	help()