import os
import glob
import os.path

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
#   Create a list containing data to be inserted into a web page via Templating
#
#   prefixes: a list of unique words
#   filesnames: a dictionary where:
#           key: can be found in 'prefixes'
#           values: a list of file names which contain content common to a single web page
#   outputs: the name of the output html file
#   titles: title of a web page. 
#  
#
def getTemplateData(prefixes, filenames, outputs, titles):
    if DEBUG:
        print("DEBUG: utils.py.getTemplateData()")
    pages=[]

    if DEBUG:
        print("DEBUG: utils.py.getTemplateData().filenames=", type(filenames))
        print("DEBUG: utils.py.getTemplateData().outputs", type(outputs))
        print("DEBUG: utils.py.getTemplateData().titles", type(titles))
    
    for prefix in prefixes:
        if DEBUG:
            print("DEBUG: utils.py.getTemplateData().prefix=", prefix)
            print("DEBUG: utils.py.getTemplateData().filenames[",prefix, "]", filenames[prefix])
            print("DEBUG: utils.py.getTemplateData().outputs[", prefix,"]=", outputs[prefix])
            print("DEBUG: utils.py.getTemplateData().titles[", prefix,"]=", titles[prefix])                       
        pages.append({"filenames":filenames[prefix],  "output":outputs[prefix], "title":titles[prefix]})
    return pages


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
# Build a list of files grouped based on common prefix in their filenames
# which compose the site content
#
# Input:
#   files : list containg files which wil be orgainzed in hash/dictionary.
#            Every file is expected to have the following format:
#                <content_dir> + "/<prefix>_<tag>.html"
#            Where:
#               'prefix' is the name of the page for which content comprises and determines the grouping of files
#                      
# Returns:
#   A dictionary of lists containing file names.
#   Each dictionry key is a 'prefix' common to all the corresponding file names
#   Format 
#    "prefix" : [ <content_dir> + "/<prefix>_<tag>.html", ...]
#        
def getFilenames(files, prefixes):
    if DEBUG:
        print("DEBUG: utils.py.getFilenames()")
    # Local varibles
    filenames={}  # files grouped by page

    # Create list of page content by page
    # (group files with the same prefix)
    for filename in files:
        if DEBUG:        
            print("DEBUG: utils.py.getFilenames().file_name=", filename)
        for prefix in prefixes:
            if DEBUG:
                print("DEBUG: utils.py.getFilenames().prefix=", prefix)
            if prefix in filename:
                if DEBUG:
                    print("DEBUG: utils.py.getFilenames().prefix = filename")
                # Add file to page content grouping
                if prefix in filenames.keys():
                    if DEBUG:                    
                        print("DEBUG: utils.py.getFilenames().if: adding element to list")
                    filenames[prefix].append(filename)
                else:
                    # Create new page content grouping with first value                
                    filenames[prefix]=[filename]
                if DEBUG:
                    print("DEBUG: utils.py.getFilenames().grouped files=", filenames)
    return filenames


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
 # Capitalize the first letter of a word and
 # convert remainder to lower case
 #  Inpur:
 #      a string
 #
 #  Output:
 #      lowercase string wit first letter uppercase
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
# Construct a web page using templating technique
#
# Input:
#   base_dir : the directory containg templating base files
#   page : a dictionary representation of page content
#       Where:
#         'page' format:
#            {
#                "filenames" : [ "full_path_of_content_file1.html", ...]  -> content used in templating
#                "title"     :  "web_page_title",
#            }
#           where:
#               "full_path_of_content_file1.html":
#                          Every file is expected to have the following format: <prefix>_'<tag>'.html.
#                          Where
#                               'prefix': the name of the page for which the file content comprises
#                               'tag'   : is either:
#                                   'msg'  -> this content will replace content in a base file with template tag {{content_msg}}
#                                   'main' -> this content will replace content in a base file with template tag {{content_main}}
#
# Return : text representation of a page
#
# TODO:
# 1. make 'msg' and 'main' parameters so for loop can become a function
#    
def getPage(template, page):
    if DEBUG:
        print("DEBUG: utils.py.getPage()")
    
    # Open the templae
    pcontent=open(template, 'r').read()

    # Determmine if any dynamic content exists for page
    if "filenames" in page.keys(): 
        # Determine if there are msg files
        if not any("msg" in s for s in page["filenames"]):
            pcontent=pcontent.replace("{{content_msg}}","") 
        # Determine if there are main files    
        if not any("main" in s for s in page["filenames"]):
            pcontent=pcontent.replace("{{content_main}}","")
            
        # Add title to page
        pcontent=pcontent.replace("{{title}}","")
            
        # Replace base templates with dynamic content
        for mfile in page["filenames"]:
            if DEBUG:
                print("DEBUG: utils.py.getPage().mfile=", mfile)
            if "main" in mfile:
                if DEBUG:                
                    print("DEBUG: utils.py.getPage().if: if main in ", mfile)                                    
                with open(mfile, 'r') as fcontent:
                    pcontent=pcontent.replace("{{content_main}}", fcontent.read())
            elif "msg" in mfile:
                if DEBUG:                
                    print("DEBUG: utils.py.getPage().elif: msg in ", mfile)
                with open( mfile, 'r') as fcontent:
                    pcontent=pcontent.replace("{{content_msg}}", fcontent.read())
    else: # No Dynamic content
        if DEBUG:
            print("DEBUG: utils.py.getPage().else: no Dynamic Content")
        # Create page with no additional content       
        pcontent=pcontent.replace("{{content_msg}}","")
        pcontent=pcontent.replace("{{content_main}}","")
        
    if DEBUG:
        print("DEBUG: utils.py.getPage().return:", pcontent)    
    return pcontent


#
# Create a dictionary representation of page content
# The dictionary format will be:
#{
#    "filenames" : [ content_dir + "/projects_main.html",],
#    "output"    :  output_dir + "/projects.html",
#    "title"     :  "Projects",
#},    
def getPages(content_dir,output_dir):
    filenames = {}
    outputs   = {}
    titles    = {}
    
    # Get Content Files
    content_files=getContentFiles(content_dir)
    # Get list of unique filenam prefixes => filename upto '_'
    prefixes=getPrefixes(content_files)
    
    # Get output ile names
    outputs=getPath(output_dir, prefixes)
    if DEBUG:
        print("DEBUG: utils.py.getPages().outputs=", outputs)
        
    filenames=getFilenames(content_files, prefixes)
    if DEBUG:
        print("DEBUG: utils.py.getPages().filenames=", filenames)    

    titles=getTitles(prefixes)
    if DEBUG:    
        print("DEBUG: utils.py.getPages().titles=", titles)
    
    # Create the pages dictionary
    pages=getTemplateData(prefixes, filenames, outputs, titles)
    if DEBUG:    
        print("DEBUG: utils.py.getPages().pages=", pages)
    return pages