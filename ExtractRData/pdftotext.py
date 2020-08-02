from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import nltk
import re
from nltk.corpus import stopwords

def convert_pdf_to_txt(fp):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def extractTitle(content):
    temp = []
    sentence = nltk.sent_tokenize(content)
    for i in range(len(sentence)):
        tempo = sentence[i].split('\n')
        for j in range(len(tempo)):
            if (len(tempo[j]) > 5):
                temp.append(tempo[j])

    for i in range(len(sentence)):
        sentence[i] = sentence[i].lower()
        sentence[i] = re.sub(r"\W", " ", sentence[i])
        sentence[i] = re.sub(r"\d", " ", sentence[i])
        sentence[i] = re.sub(r"\s+[a-z]\s+", " ", sentence[i], flags=re.I)
        sentence[i] = re.sub(r"\s+", " ", sentence[i])
        sentence[i] = re.sub(r"^\s", "", sentence[i])
        sentence[i] = re.sub(r"\s$", "", sentence[i])
        words = nltk.word_tokenize(sentence[i])
        words = [word for word in words if word not in stopwords.words('english')]
        sentence[i] = ' '.join(words)

    final_words = []
    for i in range(len(sentence)):
        words = nltk.word_tokenize(sentence[i])
        final_words.append(words)

    word2count = {}
    stop_words = nltk.corpus.stopwords.words('english')

    for word in (final_words):
        for j in (word):
            if j not in stop_words and len(j) > 3:
                if j not in word2count.keys():
                    word2count[j] = 1
                else:
                    word2count[j] += 1
    a1_sorted_keys = sorted(word2count, key=word2count.get, reverse=True)

    # for r in a1_sorted_keys:
    #    print r, a1[r]
    summation = []
    names = []
    for i in range(0, 7):
        sum = 0
        counter = 0
        power = []
        temp[i] = temp[i].lower()
        temp[i] = re.sub(r"\W", " ", temp[i])
        temp[i] = re.sub(r"\d", " ", temp[i])
        temp[i] = re.sub(r"\s+[a-z]\s+", " ", temp[i], flags=re.I)
        temp[i] = re.sub(r"\s+", " ", temp[i])
        temp[i] = re.sub(r"^\s", "", temp[i])
        temp[i] = re.sub(r"\s$", "", temp[i])

        wordize = nltk.word_tokenize(temp[i])
        for j in wordize:
            if j not in stop_words:
                if j in word2count:
                    sum = sum + word2count[j]
                    power.append(word2count[j])
                    counter = counter + 1
        # print(sum,temp[i])
        summation.append(sum)
        names.append(temp[i])

    # print(power)
    # if(counter!=0):
    #    print(sum/counter)

    temp_summation = summation
    temp_summation = sorted(temp_summation)
    temp_summation = temp_summation[::-1]

    final_names = []
    for i in range(0, len(temp_summation)):
        ind = summation.index(temp_summation[i])
        final_names.append(names[ind])
    # print(final_names)
    # print(temp_summation)

    # Concatention of last of first and first of second
    word_first = nltk.word_tokenize(final_names[0])
    word_second = nltk.word_tokenize(names[names.index(final_names[0]) + 1])
    last_first_word = word_first[-1]
    first_second_word = word_second[0]
    count_my_title = last_first_word + " " + first_second_word
    # print(names[names.index(final_names[0])+1])

    # Counting the score

    content = content.lower()
    content = re.sub(r"\W", " ", content)

    # print(content.count(count_my_title))

    if content.count(count_my_title) >= 3:
        title = final_names[0] + " " + names[names.index(final_names[0]) + 1]
    else:
        if temp_summation[0] - temp_summation[1] < 5:
            title = final_names[0] + " " + names[names.index(final_names[0]) + 1]
        else:
            if summation[names.index(final_names[0]) + 1] > 40:
                title = final_names[0] + " " + names[names.index(final_names[0]) + 1]
            else:
                title = final_names[0]

    countDict = {}
    for word in a1_sorted_keys[0:19]:
        countDict[word] = word2count[word]
    return {'title':title, 'words':countDict}

def replaceFiList(al):
    for i in range(len(al)):
        al[i] = al[i].replace("ﬁ","fi")
        al[i] = re.sub(r"\W", " ", al[i])
        al[i] = al[i].replace("\n","")
        z = al[i].split('\u2022')
        al.remove(al[i])
        for item in z:
            al.append(item)
    return al


