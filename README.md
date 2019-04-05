# Static Website Generator
The application generates additional pages for a static website.
With small modifications, it can be used to by an application to dynamically generate the addition of blog pages or other information to a website.


Built using:

    Python
    
    Jinja2
    
    CSS
    
    HTML 5
    

To run:

    pipenv --python 3
    
    pipenv shell
    
    pipenv install jinja2
    
    python [build | new]    where:
    
                                new: add new content. Generates page templates and instructs how to complete them
                                
                                build: builds site producing *.html pages and storing them to docs/*.html
                                
                                usage: explains program usage and arguements


To view web site:
    
        drop docs/index.html into browser
        
