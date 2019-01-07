

from bs4 import BeautifulSoup
from exception.sendMailException import SendMailException

class TemplateHelper:
    def __init__(self, name_template):
        self.name_template = name_template
        name_template_xml = 'template.xml'
        try:
            with open('../templates/{}/{}'.format(name_template,name_template_xml)) as infile:
                blob = infile.read()
            # Use LXML for blazing speed
            self.soup = BeautifulSoup(blob, 'lxml')
        except FileNotFoundError as fEx:
            raise Exception('Not found file [{}] into folder /templates/{}'.format(name_template_xml,name_template))

    def get_title_template(self):
        title = ""

        title_tag = self.soup.find("title")

        if (title_tag):
            title = title_tag.text
        else:
            try:
                raise Exception('Not found tag <title> into file /templates/{}/template.xml'.format(self.name_template))
            except Exception as sEx:
                raise SendMailException(sEx)


        return title