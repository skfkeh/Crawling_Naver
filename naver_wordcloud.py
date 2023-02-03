import sys
import requests
from bs4 import BeautifulSoup as bs
from newspaper import Article
from konlpy.tag import Okt
from collections import Counter, OrderedDict
import matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import datetime

URL_BEFORE_KEYWORD = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query="
URL_BEFORE_PAGE_NUM = "&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=29&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start="
# font_name = 'Apple SD Gothic Neo' # Windows는 Malgun Gothic
font_path = '/Users/watsonjung/Downloads/나눔 글꼴/나눔고딕/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf'
now = datetime.now()

def get_link(key_word, page_range):
    global num_tmp
    link = []

    for page in range(page_range):
        current_page = 1 + page * 10 # 네이버뉴스 URL : 1 → 11 → 21 ...
        crawling_url_list = URL_BEFORE_KEYWORD + key_word + URL_BEFORE_PAGE_NUM + str(current_page)

        response = requests.get(crawling_url_list)
        soup = bs(response.text, 'lxml')
        url_tag = soup.select('div.news_area > a') # . → class  / # → id

        for url in url_tag:
            link.append(url['href'])

    return link

def get_article(file1, link, key_word, page_range):
    print('wait...')

    with open(file1, 'w', encoding='utf8') as f:
        i = 1

        for url2 in link:
            article = Article(url2, language='ko')

            try:
                article.download()
                article.parse()
            except:
                print(f'- {i}번째 URL을 크롤링할 수 없습니다.')
                continue

            news_title = article.title
            news_content = article.text
            # print(f'{i}번째 title : {news_title}\n')

            f.write(news_title)
            f.write(news_content)

            i += 1

    print(f'- 네이버 뉴스 {key_word} 관련 뉴스기사 {page_range} 페이지(기사 {str(i-1)}개)가 저장되었습니다. (crawling.txt\n)')

def wordcloud(filename):
    with open(filename, encoding='utf8') as f:
        data = f.read()

        engine = Okt()
        all_nouns = engine.nouns(data)

        nouns = [n for n in all_nouns if len(n) > 1]
        count = Counter(nouns)

        tags = count.most_common(100)
        wc = WordCloud(font_path=font_path, background_color=(168, 237, 244), width=2500, height=1500)
        cloud = wc.generate_from_frequencies(dict(tags))
        # cloud = wc.generate_from_frequencies(dict(tags))

        plt.imshow(cloud, interpolation="bilinear")
        plt.axis('off')
        plt.savefig('cloud_' + str(now.hour) + str(now.minute) + '.jpg')
        # plt.show()
    print('complete!!')

def main(argv):
    if len(argv) != 3:
        print("인자 값이 부족하거나 많습니다.")

    else:
        filename = 'crawling_wc_' + str(now.hour) + str(now.minute) + '.txt'
        key_word = argv[1]
        page_range = int(argv[2])

        link = get_link(key_word, page_range)
        get_article(filename, link, key_word, page_range)
        wordcloud(filename)

if __name__ == '__main__':
    main(sys.argv)