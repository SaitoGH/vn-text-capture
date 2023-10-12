import urllib.request, json


class Request:
    url = 'https://jisho.org/api/v1/search/words?keyword='
    @staticmethod
    def find_word(word):
        with urllib.request.urlopen(Request.url + urllib.parse.quote(word)) as jarurl:
            data = json.load(jarurl)
            return data['data']