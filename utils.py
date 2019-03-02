import os
import glob
import os.path
from jinja2 import Template

DEBUG=True

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
def getPath(odir,prefixes):
    outputs={} # key = page prefix value = filename
    if DEBUG: 
        print("DEBUG: utils.py.getPath()")
    
    for prefix in prefixes:
        outputs[prefix]= odir + prefix + ".html"
            
    # Special Case: prefix 'Home' is really output file index.html
    outputs["home"]= odir + "index.html"
        
    if DEBUG:
        print("DEBUG: utils.py.getPath().outputs:", outputs)    
    return outputs
        
#
#   Convert a string to a title (first letter capital the rest lower case)
#   Input:
#       string to be converted
#
#   
#
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
        links = getPath(odir, prefixes)
        if DEBUG:
            print("DEBUG: utils.py.render().links:", links)        
            print("DEBUG: utils.py.main_html=", main_html)
            print("DEBUG: utils.py.msg_html=", msg_html)
        result = template.render(
#            title=titles[prefix],
            title=prefix,
            content_main=main_html,
            content_msg=msg_html,
            links=links,           
        )
        
        # Write out template
        if prefix == 'home':
            if DEBUG:
                print("DEBUG: utils.py.render().else: print to->", odir + 'index.html' )                                
            open(odir + 'index.html', 'w+').write(result)
        else:
            if DEBUG:
                print("DEBUG: utils.py.render().else: print to->", odir + prefix + '.html' )                    
            open(odir + prefix + '.html', 'w+').write(result)        
