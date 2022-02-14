import requests
from tqdm import tqdm
import os
import sys
import re

# to ignore warnings
import warnings
warnings.filterwarnings("ignore")

#===========Get user input
if len(sys.argv)==2:
    class_id=sys.argv[-1]
    if class_id.isnumeric():
        class_id=[int(class_id)]
    else:
        print('Give a valid class integer between 1 - 14')
        sys.exit()
else:
    list(range(1,15))

#===========Collecting Data
source_code_str=''
with open('source_code.js','r') as f:
    for line in f:
        source_code_str+=line

pattern=re.compile(r'document.test.tclass.value==(\d+)\) && \(document.test.tsubject.options\[sind\].text=="(\w+)')
book_result=pattern.findall(source_code_str)

pattern=re.compile(r'document.test.tbook.options\[(\d+)\].text="(\w.*)";\s+document.test.tbook.options\[\d+\].value="(\w.*)"')
data_result=pattern.findall(source_code_str)

overall_book_data=[]
i=0
while(i<len(data_result)):
    d=[]
    if data_result[i][0]=='1':
        d.append(data_result[i][1]+'/'+data_result[i][2].split('?')[-1])
        j=i+1
        while(j != len(data_result) and data_result[j][0]!='1'):
            d.append(data_result[j][1]+'/'+data_result[j][2].split('?')[-1])
            j+=1
        i=j
    overall_book_data.append(d)

download_data=[]
CLASSES=list(range(1,15))
j=0
for c in CLASSES:
    subject_data={}
    subject_names=[subject_data[1] for subject_data in book_result if int(subject_data[0])==c]
    for subject in subject_names:
        subject_data[subject]=overall_book_data[j]
        j+=1
    data={
        'class':c,
        'class_folder':f'class-{str(c)}',
        'subject_names':[subject_data[1] for subject_data in book_result if int(subject_data[0])==c],
        'subjects':subject_data,
    }
    download_data.append(data)

#=============Downloading Data
def downloader(url,name):

    if not(os.path.exists(name)):
        with open(name,'wb') as f:
            pass
    resume_headers={'Range':f'bytes={os.stat(name).st_size}-'}
    r=requests.get(url,stream=True,verify=False,headers=resume_headers)
    total_size=int(r.headers.get('Content-Length'))
    print(r.headers)
    inital_pos=0
    with open(name,'ab') as f:
        with tqdm(total=total_size,unit_scale=True,unit='B',desc=name,initial=inital_pos,ascii=True) as progress_bar:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)	
                    progress_bar.update(len(chunk))		
    
    print(f'Completed downloading of {name}.')

def make_dir(dir_name):
    if os.path.isdir(dir_name):
        os.chdir(dir_name)
    else:
        os.makedirs(dir_name)
        os.chdir(dir_name)

base_url='https://ncert.nic.in/textbook/pdf/'

make_dir('ncert-books')
for c in class_id:
    make_dir(download_data[c-1]['class_folder'])
    for subject in download_data[c-1]['subject_names']:
        make_dir(subject.lower()) # subject name changed in lower case
        for book in download_data[c-1]['subjects'][subject]:
            book_name='-'.join(book.split('/')[0].split(' '))
            make_dir(book_name)

            book_download_id=book.split('/')[1]
            book_id=book_download_id.split('=')[0]
            book_chapters=book_download_id.split('=')[1].split('-')[1]
            if book_chapters.isnumeric() and int(book_chapters)>1:
                chapters_list=list(range(1,int(book_chapters)+1))
                chapters_list=[str(chapter).zfill(2) for chapter in chapters_list]
                chapter_names=[f'chapter-{c}.pdf' for c in chapters_list]
                chapters_list.append('ps')
                chapter_names.append('prelims.pdf')
            
            for i,_ in enumerate(chapters_list):
                print(base_url+book_id+chapters_list[i]+'.pdf')
                downloader(base_url+book_id+chapters_list[i]+'.pdf',chapter_names[i])
            os.chdir('..')
        os.chdir('..')
    os.chdir('..')
os.chdir('..')
