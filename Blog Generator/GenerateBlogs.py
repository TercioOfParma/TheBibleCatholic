from html.parser import HTMLParser
import pypandoc
import re
import os
import sys

pdoc_args = ["-s"]
outputDir="output/"
def openHeader(fileName):
    with open(fileName, 'r') as content_file:
        content = content_file.read()
    return content
def openFooter(fileName):
    with open(fileName, 'r') as content_file:
        content = content_file.read()
    return content


def generateBlog(fileName, pathForFiles):
    blogFile = openHeader("header.html")
    newFile =  fileName.replace(".tex",".html")
    print("File to Open " + pathForFiles + fileName)
    pypandoc.convert_file(pathForFiles + fileName, to='html', format="latex",extra_args=pdoc_args,outputfile=newFile)
    print("File to Open 2 " + fileName)
    with open(newFile, 'r') as content_file:
        toAdd = content_file.read()
    toAdd = re.sub("<head>(.|\n)*?</head>", "", toAdd, flags=re.DOTALL)
    toAdd = re.sub("<footer>(.|\n)*?</footer>", "", toAdd, flags=re.DOTALL)
    blogFile = blogFile + toAdd 
    blogFile = blogFile + openFooter("footer.html")
    output = open(outputDir + newFile,"w")
    output.write(blogFile)
    output.close()
    os.remove(newFile)

def generateIndex(outputFiles, titles):
    blogFile = openHeader("header.html") + "<body>\n"
    i = 0
    for x in titles:
        blogFile = blogFile + "<a href=\"" + x.replace(".tex",".html") + "\">" + x.replace(".tex","") + "</a>" + "<br>" + "\n"
        i = i + 1
    blogFile = blogFile + "</body>" + openFooter("footer.html")
    output = open(outputDir + "index.html","w")
    output.write(blogFile)
    output.close()

pathForFiles = "."
if(len(sys.argv) == 2):
    pathForFiles = sys.argv[1] + "\\"
listOfFiles = os.listdir(pathForFiles)
listOfFiles = [x for x in listOfFiles if ".tex" in x]
outputFiles = listOfFiles.copy()
if pathForFiles == ".":
    pathForFiles = ""
outputFiles = [ pathForFiles + x.replace(".tex",".html") for x in outputFiles]
print(outputFiles)
for x in listOfFiles:
    newFile = generateBlog(x, pathForFiles)
generateIndex(outputFiles, listOfFiles)
os.copy("style.css", "output")
