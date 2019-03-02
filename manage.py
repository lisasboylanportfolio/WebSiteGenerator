import utils
import sys



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
        print("manage.main.DEBUG in main")
        

    # Remove old html files from output directory ./docs    
    if utils.cleanDir(output_dir):
        # Use a dictionary representation of page content
        #  to dynamically create web page content
        pages = utils.getPages(content_dir, output_dir)
        if utils.DEBUG:
           print("manage.main.DEBUG: build.py.main().pages=", pages)
        for page in pages:
            open(page["output"], "w").write(utils.getPage(basefile, page))
                
#    
# Instantiate object instance
#
if __name__ == '__main__':
    main()