import string
import math
import operator

def ngram_probs(filename = 'raw_sentences.txt'):
    sens = read_file(filename)
    cnt2 = {}
    cnt3 = {}
    cnt2_total = 0
    cnt3_total = 0
    for sen in sens:
        tmp = sen.split()
        for i in range(1, len(tmp)):
            #cnt2
            cnt2_total += 1
            key = tuple(tmp[i-1:i+1])
            if key in cnt2:
                cnt2[key] += 1
            else:
                cnt2[key] = 1
            #cnt3
            if i+1 < len(tmp):
                cnt3_total += 1
                key = tuple(tmp[i-1:i+2])
                if key in cnt3:
                    cnt3[key] += 1
                else:
                    cnt3[key] = 1
    for key, value in cnt2.items():
        cnt2[key] = value / cnt2_total
    for key, value in cnt3.items():
        cnt3[key] = value / cnt3_total    
    return cnt2, cnt3

def prob3(bigram, cnt2, cnt3):
    pro_dic = {}
    
    if bigram in cnt2:
        cnt2_pro = cnt2[bigram]
        for key, value in cnt3.items():
            if bigram[0] == key[0] and bigram[1] == key[1]:
                pro_dic[key[2]] = value
        
        for key, value in pro_dic.items():
            pro_dic[key] = math.log(value / cnt2_pro)
                    
    return pro_dic  

def predict_max(bigram, cnt2, cnt3):
    str = list(bigram)
    while len(str) < 15:
        pro_dic = prob3(bigram, cnt2, cnt3)
        next_word = max(pro_dic.iteritems(), key=operator.itemgetter(1))[0]
        str.append(next_word)
        bigram = tuple(str[-2:])
    return str
    
def skip_punctuation(str):
    return "".join(c for c in str if c not in string.punctuation)

def read_file(filename):
    with open(filename) as fin:
        sens = fin.readlines()
    for i in range(len(sens)):
        sens[i] = skip_punctuation(sens[i].lower())
    return sens

def main():
    cnt2, cnt3 = ngram_probs()
    pro_dic = prob3(('we', 'are'), cnt2, cnt3)
    

if __name__ == '__main__':
    main()