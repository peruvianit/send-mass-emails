

from bs4 import BeautifulSoup


class TemplateHelper:
    def __init__(self, name_template):
        self.name = name_template
        with open('../templates/{}/template.xml'.format(name_template)) as infile:
            blob = infile.read()
        # Use LXML for blazing speed
        self.soup = BeautifulSoup(blob, 'lxml')


    def get_title_template(self):
        title = ""

        title_tag = self.soup.find("title")

        if (title_tag):
            title = title_tag.text

        return title