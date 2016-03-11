#resumeParser.py
#a tool for parsing resume with user keywords in docx and pdf format.
#Steve M Song(stevemsong@yahoo.com)
#usage: resumeParser.py
#       type keyword followed by a space:
#       python c++ javascript etc
#!/bin/python
import PyPDF2,docx,re,glob

print('type keyword followed by a space:')
keyword = raw_input().split() #in a list format

def pdfParser():
    for file in glob.glob('c:\\python27\\Resume\\*.pdf'):
        pdfFile = open(file,'rb')
        reader = PyPDF2.PdfFileReader(pdfFile)
        pdfString = ''
        for pageNum in range(reader.numPages):
            pdfString = pdfString + reader.getPage(pageNum).extractText()
        matched=''
        for i in keyword:
            keymatch = re.search(re.escape(i),pdfString,re.IGNORECASE)
            if keymatch:
                matched = matched + keymatch.group() + ', '
        if matched != '':
            print(file+str(': ')+matched[:-2].upper())

def docxParser():
    for file in glob.glob('c:\\python27\\Resume\\*.docx'):
        doc = docx.Document(file)
        fullText = []
        for i in doc.paragraphs:
            fullText.append(i.text)
        fullTextString = '\n'.join(fullText) #list to a string

        matched=''
        for i in keyword:
            keymatch = re.search(re.escape(i),fullTextString,re.IGNORECASE)
            if keymatch:
                matched = matched + keymatch.group() + ', '
        if matched != '':
            print(file+str(': ')+matched[:-2].upper())

docxParser()
pdfParser()

