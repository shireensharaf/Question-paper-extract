import textract
import os
import re
import json

def main():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    datas=[]
    for f in files:
        if f.lower().endswith('.pdf'):
            text = textract.process(f,input_encoding=None, output_encoding="utf8")
            data = text_parser_pdf(text)
            datas.extend(data)

        if f.lower().endswith('.docx'):
            text = textract.process(f)
            data = text_parser_doc(text)
            datas.extend(data)

    print(len(datas))
    with open('questions.txt', 'w') as outfile:
        json.dump(datas, outfile, indent=4)

def parser_main(text):
    l = re.split("(?<!^)(\n|\f)(?=(\d+)|(Ques[0-9]+)|(Question\s\d)|(Ques))(?!.,)", text)
    
    y=[]
    d = []
    category ='None'
    sub_category='none'
    categories = ['infosys', 'amcat', 'accenture','capgemini','ibm', 'lg','l&t','mindtree']
    subcategory=['aptitude','logical reasoning','english','number series','logical section','quantitative']
  
    category_check =text[:500].split()

    for i in category_check:
        try:
            text_encode= unicode(i, "UTF-8")
        except:
            text_encode=i
        if text_encode.lower() in categories:
            category = i.lower()
            break
    # for i in l:
    #     try:
    #         y.append(unicode(i, "UTF-8"))
    #     except:
    #         y.append(i)
    # print(y)
    for i in l:
        remove_texts=['Visit PrepInsta.com for more puzzles, placement papers & Interview questions and\ntutorials.\n\nPage\s\d', 'Visit PrepInsta.com for more puzzles, placement papers & Interview questions and\ntutorials.\n\n[\f]*Page\s\d\d', 'Visit PrepInsta.com for more puzzles, placement papers & Page \d Interview questions\nand tutorials.', 'Visit PrepInsta.com for more puzzles, placement papers & Page \d\d Interview questions\nand tutorials.', 'https://www.freshersnow.com/placement-papers-download/','Accenture Aptitude Questions and Answers with Explanation','Accenture Logical Reasoning Questions and Answers with Explanation', 'www.allindiajobs.in','\nllin\n', '\nw\n', '\naj\n', '\ndi\n', '\nob\n', '\nin\n', '\ns.\n', '\n.a\n', 'https://www.freshersnow.com/']
        for sub in subcategory:
            try:
                if re.search(sub,i.lower()):
                    sub_category=sub
            except:
                pass
        for r_text in remove_texts:
            try:
                i=re.sub(r_text, '', i)
            except:
                pass
        try:
            if re.search(r'(^[0-9]+[\.|\)])|(Question\s\d+)|(Question\s\d)|(Ques)',i):
                # print(i)
                block = re.sub(r'^[0-9]+[\.|\)]', '', i)
                block = re.sub(r'Question\s\d+(\n)*', '', i)
                block = re.sub(r'Ques(\.)*', '', i)
                quest_block = dict()
                ques=[]
                splitter = ''
                options=[]
                op_splitter = ''
                ans_split=''
                split_sol = block.splitlines()
                # print(split_sol)
                for i in split_sol:
                    if re.search(r'^Sol(ution)*:', i):
                        splitter=i
                    elif re.search(r'^Explanation(:)*', i):
                        splitter=i
                    
               
            
                if splitter:
                    splitted_with_sol = split_sol[:split_sol.index(splitter)]
                    ques_sec = splitted_with_sol
                    solution__text='\n'.join(split_sol[split_sol.index(splitter):])
                    quest_block['solution']=solution__text
                
                
                else:
                    ques_sec = split_sol
                
                for i in ques_sec:
                    if (not op_splitter) and (re.search(r'^[a-eA-E](\.|\))', i) or re.search(r'Op(tion)*\s[0-9](:|\.)', i)or re.search(r'^(\s)*\([a-zA-Z]\)', i)):
                        op_splitter=i
                    if re.search(r'Ans(wer)*', i) or re.search(r'Correct\sOp(tion is)*', i):
                        ans_split = i
              
                if op_splitter:
                    splitted_with_op= ques_sec[:ques_sec.index(op_splitter)]
                    if ans_split:
                    
                        option='\n'.join(ques_sec[ques_sec.index(op_splitter):ques_sec.index(ans_split)])
                    
                        answer_line=ques_sec[ques_sec.index(ans_split):]
                        ans = re.sub(r'Ans(wer)*(\.)*(\s)*(-)*', '', '\n'.join(answer_line))
                        ans = re.sub(r'Correct Option is:', '', '\n'.join(answer_line))
                        quest_block['ans']=ans
                        # print(answer_line)
                    else:
                        option='\n'.join(ques_sec[ques_sec.index(op_splitter):]) 
                    
                    ques_sec=splitted_with_op
                   
                    op_lines = re.split(r'([\f|\n](\s)*\([a-fA-F]\))', option)
                    if len(op_lines) < 2:
                        op_lines = re.split(r'[\f|\n](\s)*[a-fA-F]\)', option)
                    if len(op_lines) < 2:
                        op_lines = re.split(r'([\f|\n]Op\s\d:)', option)
                    if len(op_lines) < 2:
                        op_lines = re.split(r'([\f|\n]Option\s\d:)', option)
                    if len(op_lines) < 2:
                        op_lines = re.split(r'[\f|\n](\s)*[a-fA-F]\.', option)
                    print('\n')
                   
                    # for i in op_lines:
                    #     if re.search(r'^Ans(wer)*', i) or re.search(r'Correct\sOp', i):
                   
                    for op in op_lines:
                        # op = re.sub(r'Option\s\d:', '', op)
                        # op = re.sub(r'Op\s\d:', '', op)
                        # op = re.sub(r'\n\n', ' ', op)
                        if op != ' ' and op != None and op != '\n' and op != '\f':
                            options.append(op)
                    print(ques_sec)
                      
                elif ans_split:
                    splitted_with_answer= ques_sec[:ques_sec.index(ans_split)]
                    answer_line=ques_sec[ques_sec.index(ans_split):]
                    ans = re.sub(r'Ans(wer)*(\.)*(\s)*(-)*', '', '\n'.join(answer_line))
                    
                    quest_block['ans']=ans
                    # print(answer_line)
                    ques_sec=splitted_with_answer
               
                for i in ques_sec:
                    ques.append(i)
                ques[0]= re.sub(r'^[0-9]+[\.|\)]', '', ques[0])
                if options:
                    quest_block['options'] = options
                
                quest_block['category']=category
                quest_block['q']='\n'.join(ques)
                quest_block['sub_category']=sub_category
                if quest_block['q'] != '':
                    d.append(quest_block)
        except:
            pass
    print(len(d))
    return d

def text_parser_pdf(text):
    d=parser_main(text)
    return d

def text_parser_doc(text):
    text= unicode(text, "UTF-8")
    text = re.sub(ur'(\u00a0)+', '\n', text)
    d=parser_main(text)
    return d
    
    
main()
