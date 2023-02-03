import sys
import requests
from bs4 import BeautifulSoup as bs
from newspaper import Article
from konlpy.tag import Okt
from collections import Counter, OrderedDict
import matplotlib
import matplotlib.pyplot as plt

URL_BEFORE_KEYWORD = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query="
URL_BEFORE_PAGE_NUM = "&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=29&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start="

font_name = 'Apple SD Gothic Neo' # Windows는 Malgun Gothic

def get_link(key_word, page_range):
    global num_tmp
    link = []

    for page in range(page_range):
        current_page = 1 + page * 10 # 네이버누스 URL : 1 → 11 → 21 ...
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

def wordcount(file1, file2):
    f = open(file1, 'r', encoding='utf8')
    g = open(file2, 'w', encoding='utf8')

    engine = Okt()
    data = f.read()
    all_nouns = engine.nouns(data)
    nouns = [n for n in all_nouns if len(n) > 1]

    global count, by_num

    count = Counter(nouns)
    by_num = OrderedDict(sorted(count.items(), key=lambda t: t[1], reverse=True))
# {'뉴진스':50, '하입보이:45'}

    word = [i for i in by_num.keys()]
    number = [i for i in by_num.values()]

    for w, n in zip(word, number):
        final1 = f'{w}  {n}'
        g.write(final1 + '\n')

    print('- 단어 카운팅 Complete!! (wordcount.txt\n)')
    f.close(), g.close()

def full_vis_bar(by_num):
    print('그래프 생성 중...')

    for w, n in list(by_num.items()):
        if n <= 15:
            del by_num[w]

    fig = plt.gcf()             # 현재 시각화 되는 객체에 접근할 필요성이 생길 때 사용
    fig.set_size_inches(20, 10) # 출력할 때 전체 그래프의 크기를 설정
    matplotlib.rc('font', family=font_name, size=10)
    plt.title('기사에 나온 전체 단어 빈도 수', fontsize=30)
    plt.xlabel('기사에 나온 단어', fontsize=20)
    plt.ylabel('기사에 나온 단어의 개수', fontsize=20)
    plt.bar(by_num.keys(), by_num.values(), color='#6799FF')
    plt.xticks(rotation=90)
    plt.savefig('all_words.jpg')
    plt.show()
    print('- all_words.jpg가 저장되었습니다/\n')

def top_n(file2, file3):
    print('가장 많이 나온 단어 10개 추출 중...')
    original = open(file2, 'r', encoding='utf8')
    top10 = open(file3, 'w', encoding='utf8')

    test = original.readlines()
    test_list = test[:10]
    refine_list = []
    print(test_list)

    for i in test_list:
        refine_list.append(i.replace("\n", ""))

    print(refine_list)

    top10.write('\n'.join(refine_list))
    original.close(), top10.close()


def main(argv):
    global num_tmp
    if len(argv) != 3:
        print("인자 값을 정확히 입력하세요")
        return

    file1 = 'crawling.txt'
    file2 = 'wordcount.txt'
    file3 = 'top10.txt'
    key_word = argv[1]
    page_range = int(argv[2])
    link = get_link(key_word, page_range)
    get_article(file1, link, key_word, page_range)
    wordcount(file1, file2)
    full_vis_bar(by_num)
    top_n(file2, file3)

if __name__ == '__main__':
    main(sys.argv)
