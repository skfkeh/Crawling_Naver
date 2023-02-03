# print('가장 많이 나온 단어 10개 추출 중...')
original = open('wordcount.txt', 'r', encoding='utf8')
top10 = open('rank_top10.txt', 'w', encoding='utf8')

test = original.readlines()
test_list = test[:10]
refine_list = []
print(test_list)

for i in test_list:
    refine_list.append(i.replace("\n", ""))

print(refine_list)

top10.write('\n'.join(refine_list))
original.close(), top10.close()