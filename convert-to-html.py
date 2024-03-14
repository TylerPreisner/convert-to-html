#open the file and add the lines to the list
fileList = []
f = open('file\\path\\to\\txt', 'r') 
for x in f:
    x = x.rstrip("\n")
    fileList.append(x)
f.close()

x = 0
a = 0
h = 0
index = 1

#newdictionary that includes a list for each section rather then all of it being just thrown into the dictionary
newdictionary = {
    "title": "",
    "description": "",
    "sections": "",
# example of how the layout of the list is "section1": ['title','test title','paragraphs', '0', 'codeblocks', '0', ';', 'paragraph:', '', 'codeblock:','paragraph:'],
}

#reads through the lines in the file
for i in fileList:
    string = i[0:4] # gets the first 4 letters of each line to determine what type of line it is
    if string == "head": # sets the title and description of the blog post
        head = i.split(";")
        newdictionary["title"] = head[1]
        newdictionary["description"] = head[2]
    elif string == "titl": # starts a new section and creates the list, then adds all starting information to it along with the title
          x += 1
          title = i.split(";")
          newdictionary.update({"sections": x})
          a = "section" + str(x)
          newdictionary[a] = []
          newdictionary[a].append('title:')
          newdictionary[a].append(title[1]) 
          newdictionary[a].append('paragraphs:')
          newdictionary[a].append(0)
          newdictionary[a].append('codeblocks:')
          newdictionary[a].append(0)
          newdictionary[a].append(';')
    elif string == "para": # for each paragraph it finds, it updates the number of paragraphs and then adds the paragraphs to the end of the list
        paragraph = i.split(";")
        newdictionary[a][3] += 1
        newdictionary[a].append('paragraph:')
        newdictionary[a].append(paragraph[1])
    elif string == "code": # same as paragraph just for codeblocks instead
        code = i.split(";")
        newdictionary[a][5] += 1
        newdictionary[a].append('codeblock:')
        newdictionary[a].append(code[1])

# the table of contents base
toctop = """
    <div class="toc">
        <h2>Table of Contents</h2>
        <ul>
"""
tocmiddle = """"""
tocbottom = """
        </ul>
        <div class="tocfooter"></div>
    </div>"""
#the base of the body
htmlbodytop = """
    <div class="blogpost">"""
htmlbodymiddle = ""
htmlbodybottom = """
    </div>
"""

#generate the table of contents by getting the number of sections and then adding the title of each section to each new line
a = 1
for x in range(newdictionary.get("sections")):
    b = "section" + str(a)
    line = '            <li><a href="#Title'+str(a)+'">'+newdictionary[b][1]+'</a></li>\n'
    tocmiddle += line
    a += 1

#creates the html body, similar to how I did the toc but more complicated
a = 1 # determines what section it is creating, starting from 1
for x in range(newdictionary.get("sections")): #loops based on how many sections there are 
    l = 7 #starting index of the tag of the content of the section
    o = 8 #starting index of the content of the sections
    b = "section" + str(a) # creates a string for each section, for example section1

    #the title of each section, with string formatting to input the title id and title
    sectiontitle = '''
      <div class="section">
        <h1 id="Title{0}">{1}</h1>
'''
    
    #the base codeblock code, with string formatting to input the code block text might add support for automatically doing multi lines
    codeblocktop = '''
        <div class="codeblock">
          <div class="codeblock-header"></div>
          <div class="codeblock-text">
            <p class="shell"></p>
'''
    codeblockmiddle = ''
    codeblockbottom = '''
          </div>
        </div>
'''
    h = newdictionary.get(b)[3] + newdictionary.get(b)[5] # gets the number of paragraphs and code blocks in each section
    newtitle = sectiontitle.format(a, newdictionary.get(b)[1]) #formats the title string into a new variable
    for k in range(h): # loops through each section based on variable h
      if newdictionary.get(b)[l] == "paragraph:": #checks if it is a paragraph or codeblock and inserts the correct line
        line = '        <p>'+newdictionary.get(b)[o]+'</p>\n'
        newtitle += line
      elif newdictionary.get(b)[l] == "codeblock:":
        if "," in newdictionary.get(b)[o]: # if it is a multiline code block it splits it into new lines
            multicode = newdictionary.get(b)[o]
            multicode = multicode.split(',')
            for x in multicode:
                line = '            <p>'+x+'</p>\n'
                codeblockmiddle += line
        else:
          codeline = '            <p>'+newdictionary.get(b)[o]+'</p>\n'
          codeblockmiddle += codeline 
        code = codeblocktop + codeblockmiddle + codeblockbottom
        newtitle += code 
      l += 2 # adds 2 indexes to the starting tag and content go correctly go through the content
      o += 2
      
    htmlbodymiddle += newtitle
    
    
    a += 1


#html header for adding to the final html file
htmlheader = """
<!DOCTYPE html>
<html>
  <head>
    <title>Tyler Preisner</title>
    <link rel="stylesheet" href="/css/test.css">
    <link rel="stylesheet" href="/css/blogpost.css">
  </head>
  <body>
    <header class="main-header">
        <nav class="navbar">
          <div class="name">Tyler Preisner</div>
          <div class="subname">IT student and job seeker</div>
          <div></div>
          <div class="buttons">
              <ul>
                <li id="a"><a href="/">HOME</a></li>
                <li id="a" id="a" class="active"><a href="/posts.html">POSTS</a></li>
                <li id="a"><a href="/aboutme.html">ABOUT</a></li>
                <li id="a"><a href="/links.html">LINKS</a></li>
              </ul>
          </div>
          <div></div>
        </nav>
    </header>
    <div>
        <a class="back" href="/posts.html">BACK</a>
    </div>"""

htmltoc = toctop + tocmiddle + tocbottom # adds all the table of content strings together
htmlbody = htmlbodytop + htmlbodymiddle + htmlbodybottom # adds all of the html body strings together
htmlfoot = """
    <footer class="footer">

    </footer>
  </body>
</html>"""

html = htmlheader + htmltoc + htmlbody + htmlfoot # adds all of the html contents together, and will output to a html file
filepath = "file\\path\\to\\output" #filepath to where I want the program to output the file
filename = filepath + newdictionary.get("title") + "-" + newdictionary.get("description") + ".html" # creating the filename
create = open(filename, 'w') #creating the file, writing the html to the file then closing the file
create.write(html)
create.close()