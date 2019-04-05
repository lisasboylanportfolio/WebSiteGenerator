# Static Website Generator
The application generates additional pages to a static website


Built using:

    python
    
    jinja2
    
    css
    
    HTML 5
    

HOW TO USE:
This software is desinged to dynamically add pages to the existing web application (my profile).
With small modifications, it can be used to by an application to dynamically generate the addition of blog pages to a website.


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
        
