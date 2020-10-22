import requests
from bs4 import BeautifulSoup as bs

class Scraper():
    def __init__(self):
        self.BASE_URL = "https://www.kanshudo.com/collections/wikipedia_jlpt/"
        self.ENDPOINTS = []
        #self.database = db

    def set_endpoints(self):
        page = requests.get(self.BASE_URL)
        soup = bs(page.content, 'html.parser')
        for a in soup.find_all('a', href=True):
            if self.BASE_URL[24:] in a['href']:
                self.ENDPOINTS.append(a['href'][28:])

    def get_vocab(self, vocab_list):

        for row in vocab_list:
            try:
                kanji = row.find('div', class_='f_kanji').text
                extra = row.find('div', class_='jukugo').text.replace('\n', '')
                reading  = row.find('div', class_='vm').text
                furigana = row.find('div', class_='furigana').text

                word = kanji + extra.replace(furigana + kanji, '').replace('\n', '')
                level = 'N' + row.find('div', class_='w_ref').text
                pos = row.find('div', class_='vm').find('span').text
                definition = reading.replace(pos, '').replace('1. ', '')

                usefulness = row.find('div', class_='ufn_container').text.replace('\n', '')
            except:
                continue

            print('THE JLPT LEVEL OF THIS WORD IS ' + level)
            print('FURIGANA: ' + furigana)
            print('WORD: ' + word)
            print('PART OF SPEACH: ' + pos)
            print('DEFINITION: ' + definition)
            print('USEFULNESS: ' + usefulness + '\n')

            #def fill_db(self):
                #myDB = self.database
                #myDB.execute(
                #    'INSERT INTO JLPTVocab (level, kanji, furigana, hirigana, pos, definition, example, used)'
                #)
                #continue

            #print(definition_one + '\n')
            #print(definition_two)

    def iterate_endpoints(self):
        self.set_endpoints()

        for endpoint in self.ENDPOINTS:

            page = requests.get(self.BASE_URL + endpoint)
            soup = bs(page.content, 'html.parser')

            raw_vocab_list = soup.find_all('div', class_='jukugorow first last')
            self.get_vocab(raw_vocab_list)

def main():
    sc = Scraper()
    sc.iterate_endpoints()

if __name__ == '__main__':
    main()
