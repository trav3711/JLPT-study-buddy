import requests
from bs4 import BeautifulSoup as bs

class Scraper():
    def __init__(self):
        self.BASE_URL = "https://www.kanshudo.com/collections/wikipedia_jlpt/"
        self.ENDPOINTS = []

    def set_endpoints(self):
        page = requests.get(self.BASE_URL)
        soup = bs(page.content, 'html.parser')
        for a in soup.find_all('a', href=True):
            if self.BASE_URL[24:] in a['href']:
                self.ENDPOINTS.append(a['href'][28:])

    def get_vocab(self, vocab_list):
        #vocab_list = self.soup.find_all('div', class_='jukugorow')
        for row in vocab_list:

            kanji = row.find('div', class_='f_kanji')
            extra = row.find('div', class_='jukugo')
            furigana = row.find('div', class_='furigana')
            reading  = row.find('div', class_='vm')

            #first = reading.text.find('1.')
            #second = reading.text.find('2.')

            #pos = reading.text[0:first]
            #definition_one = reading.text[first:]
            #definition_two = reading.text[second:]

            try:
                level = 'N' + row.find('div', class_='w_ref').text
                #first = reading.text.find('1.')
                pos = reading.text
                #definition_one = reading.text[first:]
                usefulness = row.find('div', class_='ufn_container').text
            except:
                continue

            print('THE JLPT LEVEL OF THIS WORD IS ' + level)

            try:
                print(furigana.text)
                print((kanji.text + extra.text.replace(furigana.text + kanji.text, '')).replace('\n', ''))
            except:
                print(extra.text.replace('\n', ''))

            print(pos)
            print('USEFULNESS: ' + usefulness.replace('\n', '') + '\n')
            #print(definition_one + '\n')
            #print(definition_two)

    def iterate_endpoints(self):
        #self.BASE_URL = "https://www.kanshudo.com/collections/wikipedia_jlpt/"
        self.set_endpoints()
        #print(self.ENDPOINTS)

        for endpoint in self.ENDPOINTS:

            page = requests.get(self.BASE_URL + endpoint)
            soup = bs(page.content, 'html.parser')

            raw_vocab_list = soup.find_all('div', class_='jukugorow first last')
            self.get_vocab(raw_vocab_list)

def main():
    sc = Scraper()
    #sc.get_endpoints()
    #print(sc.ENDPOINTS)
    sc.iterate_endpoints()

if __name__ == '__main__':
    main()
