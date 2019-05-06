import os
import urllib.request
import gzip
import sys
import time
import shutil
import logging
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)
import xml.etree.cElementTree as cet
#import threading

def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    #speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d seconds passed" %
                    (percent, progress_size / (1024 * 1024), duration))
    sys.stdout.flush()

    
def retrieve_file(fileno):
    ftp_path = 'ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed19n0' + str(fileno) + '.xml.gz'
    print(ftp_path)
    file = 'pubmed19n0' + str(fileno) + '.xml.gz'
    tmp = file
        
    # Download from ftp server
    urllib.request.urlretrieve(ftp_path, file, reporthook)
    print('\n;', file, ': Done\n')
    
    # Unzip
    with gzip.open(file, 'rb') as f_in:
        file = '.'.join(file.split('.')[:-1])
        with open(file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        
    if os.path.exists(tmp):
        os.remove(tmp)
    
    # Extract the abstracts
    context = cet.iterparse(file, events=('start','end'))
    context = iter(context)
    event, root = context.__next__()
        
    writepath = 'batch_data/'
    s = writepath + str(fileno) + '.txt'
    tmpfile = open(s, 'w', encoding = 'utf8')   
    for event, elem in context:
        if event == 'start' and elem.tag == 'AbstractText':
            text = elem.text
            if text:
                text = text.strip()
            else:
                continue
            tmpfile.write(elem.text.strip('\n'))
            tmpfile.write('\n')
            root.clear()
    tmpfile.close()
        
    if os.path.exists(file):
        os.remove(file)
    
#retrieve_file(10)
if __name__ == "__main__":
    for i in range(100,150):
        retrieve_file(i)
        print(i, ' done.\n')
        
        
