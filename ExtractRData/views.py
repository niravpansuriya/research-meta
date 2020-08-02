from django.views.generic import TemplateView
from django.http import HttpResponse
from .pdftotext import *
import nltk
import re
import heapq
from django.shortcuts import render
import json
import spacy
import pickle


noun_finder = spacy.load('en_core_web_lg')

class HomePageView(TemplateView):
    template_name = 'index.html'

class presentationView(TemplateView):
    template_name = 'Presentation.html'


def upload_file(request):
    dirty_text = convert_pdf_to_txt(request.FILES['pdf'])
    # nltk.download('stopwords')
    X = nltk.sent_tokenize(dirty_text)

    for i in range(len(X)):
        X[i] = X[i].lower()
        X[i] = re.sub(r"\W", " ", X[i])
        X[i] = re.sub(r"\d", " ", X[i])
        X[i] = re.sub(r"\s+[a-z]\s+", " ", X[i], flags=re.I)
        X[i] = re.sub(r"\s+", " ", X[i])
        X[i] = re.sub(r"^\s", "", X[i])
        X[i] = re.sub(r"\s$", "", X[i])

    # X[i]=X[i]+'\n \n'
    stop_words = nltk.corpus.stopwords.words('english')
    word2count = {}
    words_token = nltk.word_tokenize(dirty_text)
    for word in (words_token):
        if len(word) == 1:
            words_token.remove(word)
            continue
        if word not in stop_words:
            if word not in word2count.keys():
                word2count[word] = 1
            else:
                word2count[word] += 1
    max_count = max(word2count.values())
    for key in word2count.keys():
        word2count[key] = word2count[key] / max_count
    sent2score = {}
    for sentence in X:
        if len(sentence) < 25:
            X.remove(sentence)
            continue
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word2count.keys():
                if len(sentence.split(' ')) < 25:
                    if sentence not in sent2score.keys():
                        sent2score[sentence] = word2count[word]
                    else:
                        sent2score[sentence] += word2count[word]
    best_sentences = heapq.nlargest(15, sent2score, key=sent2score.get)
    celllist = []
    for d in best_sentences:
        celllist.append(d)

    # Getting Authors
    content = dirty_text
    i = 0
    flag = 0
    ans_content = ''
    while i < len(content):
        if (content[i].lower() == 'a'):
            ans = content[i:i + 8]
            if (ans.lower() == 'abstract'):
                index = i
                ans_content = content[0:index]
                flag = 1
                break
        i += 1

    if (flag == 0):
        ans_content = content

    # The text we want to examine
    text = ans_content

    text = ''.join([i for i in text if not i.isdigit()])

    # Parse the text with spaCy. This runs the entire pipeline.
    doc = noun_finder(text)

    # 'doc' now contains a parsed version of text. We can use it to do anything we want!
    # For example, this will print out all the named entities that were detected:
    c = 0
    al = []
    for entity in doc.ents:
        if (f"({entity.label_})" == '(PERSON)') and f"{entity.text}" != '\n\n' and f"{entity.text}" != '\n':
            s = f"{entity.text}"
            # print(f"{entity.text}", "and")
            if (not (all(x.isspace() for x in s))):
                al.append(s)
            c += 1

    if (flag == 0):
        al = al[0:3]
    dictWordsFreq = extractTitle(dirty_text)
    title = dictWordsFreq['title']

    # Extract Problem Statement
    negative_statements = []
    with open('ExtractRData/classifier.pickle', 'rb') as f:
        clf = pickle.load(f)
    with open('ExtractRData/tfidfmodel.pickle', 'rb') as f:
        tfidf = pickle.load(f)
    for sen in X:
        sen = [sen]
        sample = tfidf.transform(sen).toarray()
        if clf.predict(sample) == 0:
            negative_statements.append(sen)
    if (len(negative_statements) > 5):
        negative_statements = negative_statements[0:5]

    negative_statements_ans = []
    for statement in negative_statements:
        negative_statements_ans.append(statement[0])

    con_lo = dirty_text.lower()

    index = con_lo.find('references\n')

    if index != -1:
        ref = content[index + 12:]
        end_index = re.search(r"\n[a-zA-Z]+\n", dirty_text).start()
        if end_index != -1:
            ref = ref[0:end_index]
        else:
            ref = ref[index:]
    else:
        ref = 'Not Found'



    # print(final_content)
    end_len = len(dirty_text)
    con_lo = dirty_text.lower()
    ref_counter = [i for i in range(len(con_lo)) if con_lo.startswith('reference', i)]

    counter = 0
    maxy = 0
    final_index = 0
    for index in ref_counter:
        if content[index] == content[index].upper():
            checker = content[index:index + 50]
            doc = noun_finder(checker)
            for entity in doc.ents:
                if (f"({entity.label_})" == '(PERSON)'):
                    s = f"{entity.text}"
                    counter = counter + 1

            if counter >= maxy:
                maxy = counter
                final_index = index

    ref = content[final_index + 10:]
    ref = ref.split("\n")

    ans_ref = []
    ans = ''
    for index in range(len(ref)):
        if ref[index] == '' and ans != '':
            ans_ref.append(ans)
            ans = ''
        else:
            ans = ans + ref[index]

    # print(ans_ref)

    #ABSTRACT
    # abs_counter = [i for i in range(len(con_lo)) if con_lo.startswith('abstract', i)]
    #
    # final_index = 0
    # for index in abs_counter:
    #     if content[index] == content[index].upper():
    #         final_index = index
    #         break
    #
    # final_content = ''
    #
    # j = final_index + 8
    # j = j + 1
    # while not (content[j].isalpha()):
    #     j = j + 1;
    #
    # for i in range(len(content)):
    #     if content[j] == '\n' and content[j + 1] == '\n':
    #         break
    #     final_content = final_content + content[j]
    #     j = j + 1

    content = dirty_text
    flag = 0
    con_lo = content.lower()

    abs_counter = [i for i in range(len(con_lo)) if con_lo.startswith('abstract', i)]

    final_index = 0
    for index in abs_counter:
        if content[index] == content[index].upper():
            print(index)
            flag = 1
            final_index = index
            break

    final_content = ''
    paragraphs = content.split('\n\n')
    if flag == 0:
        sentence = []
        for i in range(len(paragraphs)):
            sentence = nltk.word_tokenize(paragraphs[i])
            if (len(sentence) > 120):
                final_content = paragraphs[i]
                break

    j = final_index + 8
    j = j + 1
    while not (content[j].isalpha()):
        j = j + 1

    for i in range(len(content)):
        if content[j] == '\n' and content[j + 1] == '\n':
            break
        final_content = final_content + content[j]
        j = j + 1

    return render(request, 'result.html',
                  {'data': json.dumps(
                      {'summary': [item.capitalize() for item in replaceFiList(celllist)], 'authors': replaceFiList(al),
                       'title': title.replace("ﬁ", "fi").capitalize(),'problem': [negative.capitalize() for negative in negative_statements_ans], 'reference': ans_ref, 'abstract': final_content}, indent=4, sort_keys=True),
                   'authers_ext': replaceFiList(al), 'title_ext': title.replace("ﬁ", "fi").capitalize(),
                   'summary_ext': [item.capitalize() for item in replaceFiList(celllist)], 'neg': [negative.capitalize() for negative in negative_statements_ans],
                   'words_ext': dictWordsFreq['words'], 'abs_ext': final_content,'refe':ans_ref})


def download_file(request):
    fh = request.POST['data']
    fh = json.loads(fh)

    fh['summary'] = [item.capitalize() for item in replaceFiList(fh['summary'])]
    fh['authors'] = replaceFiList(fh['authors'])

    filename = "data.json"
    response = HttpResponse(json.dumps(fh, indent=4), content_type='text/json')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response
