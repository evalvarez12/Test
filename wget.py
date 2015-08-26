import urllib2
import sys,os


#The url address comes as an argument
url = str(sys.argv[1])
file_name = url.split('/')[-1]

urlopener = urllib2.build_opener()

#If the file already exists resume download, otherwise start from scratch
if os.path.exists(file_name): 
  f=open(file_name,"ab")
  #Obtain file size to pass as a header
  file_size_downloaded = os.path.getsize(file_name)
  urlopener.addheaders+=[("Range","bytes=%s-" % (file_size_downloaded))]
  print "RESUMING DOWNLOAD from "+str(file_size_downloaded)
  
else :  
  f = open(file_name, 'wb')
  file_size_downloaded = 0
  print "STARTING DOWNLOAD"

#Open url and get the file size to be downloaded
u=urlopener.open(url)
meta = u.info()
file_size = int(meta.getheaders("Content-Length")[0]) + file_size_downloaded
print "Downloading: %s Size: %s" % (file_name, file_size)


#Start downloading
print_mark=0
while True:
    buffer = u.read(8192)
    if not buffer or os.path.getsize(file_name)>=file_size:
        break

    #Prints the percentaje of the download so far
    file_size_downloaded += len(buffer)
    f.write(buffer)
    status = "\r["+str(file_size_downloaded * 100. / file_size)+"%]"
    print_mark+=1
    if print_mark==30 :
      print status,
      print_mark=0
    sys.stdout.flush()
      
f.close()
    

