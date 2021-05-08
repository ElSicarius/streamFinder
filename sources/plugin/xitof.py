

import requests
import bs4


class Movie(set):
    url = "http://okvop.com/"
    url_sane = "http://okvop.com"


    def get_id(self):
        content = requests.get(self.url)
        doc = bs4.BeautifulSoup(content.text, 'html.parser')
        id_ = doc.findAll("a", attrs={"id":"okvopc"})
        id = id_[0]["href"]
        return id


    def search(self, title: str) -> set:
        link = set()
        data = {
        "searchword": title
        }
        content = requests.post(self.url+'/home/okvop', data=data)
        doc = bs4.BeautifulSoup(content.text, 'html.parser')
        div = doc.findAll("div", attrs={"id": 'hann'})
        for element in div:
            elm = element.find("a")["href"]
            # removing useless results
            if not '#top' in elm.__str__():
                # dirty bur meh
                movie_name = element.__str__().split(elm+"\">")[1].split(" <")[0].strip("\n").strip(" ")
                self.add(f"{movie_name}; {self.url_sane+elm.__str__()}")


    def get_movie(self, title:str) -> set:
        id = self.get_id()
        self.url += id
        self.search(title)
        return self
