# Link Info
- NCERT textbook pdf download link:
https://ncert.nic.in/textbook/pdf/{chapterID}.pdf

- main issue is to get chapterIDs for all courses

- solution for this issue is to get js source code file for all options and from that try to find download-links using re module. One just needs to update source code file and the script does rest of the work.

# How to use this:
- Clone this repo
- change into repo folder
- simply run
```py
python downloader.py <class_no>
# here class_no is an integer between 1-14(both included)
# if one does not give class_no then it downloads all classes pdfs
```