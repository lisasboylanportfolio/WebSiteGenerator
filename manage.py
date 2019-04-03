import utils
import sys

def usage():
    if utils.DEBUG:
        print("DEBUG: manage:usage()")
        
    # Allow user to initiate with arguements
    print("manage.py: A web site generator.")
    print(" Usage: python3 manage.py build|new|usage")
    print("Where:")
    print("build: generate an existing site ")
    print("new: add new content")
    print("usage: explains program usage and arguements")


#
#   Main Driver
#       Give:
#           content_dir: which contains html markup web page content
#           basefile_dir: a Template containing tags for which content will be dynamically inserted
#           output_dir:   directory where dynamically generated pages will be output
#            
# NOTE: configure GLOBAL constants using config.py
#
def main():
    
    # Setup variables for content, template , and ouptut directories required for page generation    
    basefile    = "./templates/base.html"
    output_dir  = "./docs/"
    content_dir = "./content/"

    if utils.DEBUG:    
        print("utils.DEBUG in main")
        print("DEBUG: manage.py:main().sys.argv=:", sys.argv)        
        
    # Check Usage
    if len(sys.argv) ==  2:
        arg1 = sys.argv[1]            
        if arg1 == 'build' or arg1 == 'new':
            if utils.cleanDir(output_dir):
                if arg1 == 'build':
                    utils.build(content_dir,basefile, output_dir)
                else:
                    utils.new(content_dir)
            else:
                print("Unable to remove old web pages. Confirm docs/ permissions are properly set.")
        else:
            usage()
    else:
        usage()



#    
# Instantiate object instance
#
if __name__ == '__main__':
    main()