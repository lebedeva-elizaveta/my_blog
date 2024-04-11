from bs4 import BeautifulSoup


class Filter:
    @staticmethod
    def filter_tags(inputstr):
        soup = BeautifulSoup(inputstr, 'html.parser')
        allowed_tags = ["b", "i", "h1", "h2", "h3", "h4", "h5", "h6", "tt", "cite", "em", "font", "a", "p",
                        "blockquote", "ol", "li", "ul"]

        for tag in soup.find_all():
            if tag.name not in allowed_tags:
                tag.unwrap()

        return str(soup)

