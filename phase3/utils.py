import os
import glob
import re
import os.path
from jinja2 import Template
from shutil import copyfile

DEBUG = True


#
# Remove all *.html file from directory
#
# Input: directory : a pathname to the directory from which to remove hhtml files
# Return:
#   True : if files were removed
#   False : No files were removed
#
def cleanDir(directory):
    if DEBUG:
        print("DEBUG: utils.py.cleanDir()")
    # Get a list of all the file paths that end with .html from the directory
    fileList = glob.glob(directory + "/*.html")
    if DEBUG:
        print("DEBUG: utils.py.cleanDir().fileList=", fileList) 
    if fileList == None or fileList == []:
        if DEBUG:
            print("DEBUG: utils.py.cleanDir().filelist empty")
        return True
                
    # Iterate over the list of filepaths & remove each file.
    if DEBUG:    
        print("DEBUG: utils.py.cleanDir().for()")    
    for filePath in fileList:
        try:
            os.remove(filePath)
            if DEBUG:            
                print("DEBUG: utils.py.cleanDir().return(TRUE)")                
            return True
        except:
            print("Error while deleting file : ", filePath)
            if DEBUG:            
                print("DEBUG: utils.py.cleanDir().return(FALSE)")                            
            return False



#
# Generate files names with '.html' suffix
#
# Input:
#   odir: A directory added to a prefix to create a base file path
#   prefixes: a word which is prefixed by odir and '.html' appended
#
# Ouptuts:
#   a dictionary. The key is a 'prefix' and the value is a html file name
#
# Note: Prior to Templating, this method require output_dir be prefixed to each filename
#       However, with Templating, test confirmed output_dir was not required
#
def getPath(prefixes):
    outputs={} # key = page prefix value = filename
    if DEBUG: 
        print("DEBUG: utils.py.getPath()")
    
    for prefix in prefixes:
        outputs[prefix]= prefix + ".html"
            
    # Special Case: prefix 'Home' is really output file index.html
    outputs["home"]= "index.html"
        
    if DEBUG:
        print("DEBUG: utils.py.getPath().outputs:", outputs)    
    return outputs


#
# Return files in specified directory
#
# Input: Directory to be searched for files
#
# Return:  
#   A list if file names
#
def getContentFiles(content_dir):
    content_files=[]
    
    # get all html files
    content_files=glob.glob(content_dir + "/*.html")
    if DEBUG:
        print("DEBUG: utils.py.getContentFiles().content files=", content_files)
    return content_files
    
    
#
#   Get the prefix of a string. where the prefix is seperated by '_'
#
#   Input:
#       List of files
#
#   Return:
#       List of prefixes       
#
def getPrefixes(strings):
    prefixes=[]   #  file name prefixes help group content files by page
    
    #  list of unique filenam prefixes => filename upto '_'
    for file_path in strings:
        if DEBUG:
            print("DEBUG: utils.py.getPrefixes().filepath=", file_path)        
        file_name = os.path.basename(file_path)
        pos=file_name.index("_")
        file_prefix = file_name[0:pos]
        if file_prefix not in prefixes:
            prefixes.append(file_prefix)
            if DEBUG:
                print("DEBUG: utils.py.getPrefixes().prefixes=", prefixes)
    return prefixes

        
def getTitles(prefixes):
    if DEBUG:   
        print("DEBUG: utils.py.getTitles()")   
    titles={}
    
    for title in prefixes:
        # Capitalize thefirst Letter
        to_upper =  title[0]
        to_lower = title[1:len(title)]
        titles[title]= to_upper.upper() + to_lower.lower()
        if DEBUG:
            print("DEBUG: utils.py.getTitles().titles=", titles)
        
    return titles


#
# Render a web page using the Templating technique
#
# Input:
#   cdir: directory containing template content used to compase page
#   odir: generated web pages output directory
#   basefile: template file
#
def render(cdir,odir, basefile, prefixes):  
    for prefix in prefixes:
        # open/ reposition file pointer
        template_html = open(basefile).read()
        # initialize template
        template = Template(template_html)
        
        # Get content if no content file exists set variable to " "
        try:
            if DEBUG:
                print("DEBUG: utils.py.render().open(", cdir + prefix + "_main.html).read()")             
            main_html = open(cdir + prefix + "_main.html").read()               
        except:
            main_html = " "

        try:
            if DEBUG:
                print("DEBUG: utils.py.render().open(", cdir + prefix + "_msg.html.read()")                            
            msg_html  = open(cdir + prefix + "_msg.html").read()
        except:
            msg_html = " "

        titles = getTitles(prefixes)
        links = getPath(prefixes)
        if DEBUG:
            print("DEBUG: utils.py.render().links:", links)        
            print("DEBUG: utils.py.render().main_html=", main_html)
            print("DEBUG: utils.py.render().msg_html=", msg_html)
        result = template.render(
            title=prefix,
            content_main=main_html,
            content_msg=msg_html,
            links=links,           
        )
        
        # Write out template
        if DEBUG:
            print("DEBUG: utils.py.render().print to->", odir + prefix + '.html' )
        if prefix == 'home':
            open(odir + 'index.html', 'w+').write(result)
        else:
            open(odir + prefix + '.html', 'w+').write(result)        


#
# Dynamically generate web pages
#
def build(content_dir,basefile, output_dir):
    # Use jinja to dynamically create web page content
    # Get Content Files
    content_files=getContentFiles(content_dir)            
    # Get list of unique content filename prefixes => filename upto '_'
    prefixes=getPrefixes(content_files)
    # Create the final html pages. These will be autogenerated and stored in 'output_dir'
    render(content_dir,output_dir, basefile, prefixes)

#
# Using template/dynamic_base, 
#            <div class="row vl">
#            </div>
#            <div class="row">
#                <div class="col right_col">
#                    <div class="row">
#                        <p>{{new_content}}</p>         
#                    </div>
#                    <div class="row">
#                    </div>
#                </div>
#            </div>    
# create one or both of the following files
# content/<new> main.html,
# content/<new> msg.html,
#
# Input
#   content_dir: Directory containing dynamic web page content
#   basefile:    Dictory containing web page templates     
#
#   TODO: can reduce code by adding grammer functionalit to make word plural or not
#       ex template vs templates
#
def new(content_dir, basefile):
    name=""
    quote=""

    print("What will the title/suject of your content be (must be all alphanumeric or '_'): ")
    name=input("NOTE: all non alphanumeric characters will be converted to'_' : ")
    name = re.sub('[^0-9a-zA-Z]+', '_', name)
    while quote != 'y' and quote!= 'n':
        print("Would you like to include a quote or short text with your content? (must be all alphanumeric),")
        quote=input("Enter 'y' or 'n': ")
        
    if (createTemplate(content_dir, basefile, name, quote)):
        if quote=='y':
            print("Templates have been created for your new content.")
            print("The main content should be added to the file:")
            print("         ",  content_dir + name + "_main.html")
            print("Please replace the following tag with your content:")
            print("                        {{new_content}}         ")
            print("Your message can be entered into")
            print("         ",  content_dir + name + "_msg.html")
            print("No tags need be replaced in the message file. Content can be freely added.")
            print("\nOnce you have completed entering your content, run:")
            print("         python3 manage.py build")
            print("and your web page will automaticall be generated\n\n")
        else:
            print("A template has been created for your new content.")
            print("The main content should be added to the file:")
            print("         ",  content_dir + name + "_main.html")
            print("Please replace the following tag with your content:")
            print("                        {{new_content}}         ")
            print("\nOnce you have completed entering your content, run:")
            print("         python3 manage.py build")
            print("and your web page will automaticall be generated.\n\n")        