import urllib
import urllib2
import sys
import re
import requests
url = sys.argv[1]
aResp = urllib2.urlopen(url);
webdata = aResp.read()
op = re.search('<input type="hidden" name="op" value="([\w.-]+)">', webdata).group(1)
vid = re.search('<input type="hidden" name="id" value="([\w.-]+)">', webdata).group(1)
fname = re.search('<input type="hidden" name="fname" value="([\w.-]+)">', webdata).group(1)
print "Sending post request for episode " + fname 
r = requests.post(url, data={'op': op, 'id':vid, 'fname':fname, 'usr_login':'', 'referer':'','channel':'','method_free':'Free+Download'})

video_link = re.search('file: "([\w:\/\.]+\/[\w]+[\.mp4|\.flv]+)"', r.text).group(1)
print video_link
file_name = fname
u = urllib2.urlopen(video_link)
f = open(file_name, 'wb')
meta = u.info()
file_size = int(meta.getheaders("Content-Length")[0])
print "Downloading: %s Bytes: %s" % (file_name, file_size)

file_size_dl = 0
block_sz = 8192
while True:
    buffer = u.read(block_sz)
    if not buffer:
        break
    file_size_dl += len(buffer)
    f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    done = int(50 * file_size_dl / file_size)
    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
    sys.stdout.flush()
    status = status + chr(8)*(len(status)+1)
    print status,

f.close()
