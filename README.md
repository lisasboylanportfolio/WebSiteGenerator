Web Site Generator
Built using:
    python
    jinja2
    css
    HTML 5


HOW TO USE:
This software is desinged to dynamically add pages to the existing web application (my profile).
To run:
    pipenv --python 3
    pipenv shell
    pipenv install jinja2
    python [build | new]    where:
                                new: generates page templates and instructs how to complete them
                                build: builds site producing *.html pages and storeing them to docs/*.html
    to view web site:
        drop docs/index.html into browser
        
