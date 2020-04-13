import textract
import os
import re
import json

def main():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    datas=[]
    for f in files:
        if f.lower().endswith('.pdf') or f.lower().endswith('.docx'):
            text = textract.process(f)
            data = text_parser(text)
            datas.extend(data)

    print(len(datas))
    with open('questions.txt', 'w') as outfile:
        json.dump(datas, outfile, indent=4)
    


def text_parser(text):
    print('#########################################')
    text= unicode(text, "UTF-8")
    text = re.sub(ur'(\u00a0)+', '\n', text)
    l = re.split("(?<!^)(\n|\f)(?=\d+|Ques[0-9]+)", text)
   
    d = []
    category ='None'
    sub_category='none'
    categories = ['infosys', 'amcat', 'accenture','capgemini']
    subcategory=['aptitude','logical reasoning']
    category_check =text[:200].split()
    for i in category_check:
        if i.lower() in categories:
            category = i.lower()
            break
        
    for i in l:
        remove_texts=['Visit PrepInsta.com for more puzzles, placement papers & Interview questions and\ntutorials.\n\nPage\s\d', 'Visit PrepInsta.com for more puzzles, placement papers & Interview questions and\ntutorials.\n\n[\f]*Page\s\d\d', 'Visit PrepInsta.com for more puzzles, placement papers & Page \d Interview questions\nand tutorials.', 'Visit PrepInsta.com for more puzzles, placement papers & Page \d\d Interview questions\nand tutorials.', 'https://www.freshersnow.com/placement-papers-download/','Accenture Aptitude Questions and Answers with Explanation','Accenture Logical Reasoning Questions and Answers with Explanation', 'www.allindiajobs.in','\nllin\n', '\nw\n', '\naj\n', '\ndi\n', '\nob\n', '\nin\n', '\ns.\n', '\n.a\n']
        for sub in subcategory:
            if re.search(sub,i.lower()):
                sub_category=sub
        for r_text in remove_texts:
            i=re.sub(r_text, '', i)
       
        if re.search(r'^[0-9]+[\.|\)]',i):
            block = re.sub(r'^[0-9]+[\.|\)]', '', i)
            quest_block = dict()
            ques=[]
            splitter = ''
            options=[]
            op_splitter = ''
            ans_split=''
            split_sol = block.splitlines()
            print(split_sol)
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
                if (not op_splitter) and (re.search(r'^[A-E](\.|\))', i) or re.search(r'[Op]\s[0-9](:|\.)', i)or re.search(r'^(\s)*\([a-zA-Z]\)', i)):
                    op_splitter=i
                if re.search(r'^Ans(wer)*', i) or re.search(r'Correct\sOp', i):
                    ans_split = i
            
            if op_splitter:
                splitted_with_op= ques_sec[:ques_sec.index(op_splitter)]
                if ans_split:
    
                    option='\n'.join(ques_sec[ques_sec.index(op_splitter):ques_sec.index(ans_split)])
                    
                    answer_line=ques_sec[ques_sec.index(ans_split):]
                    ans = re.sub(r'Ans(wer)*(\.)*(\s)*(-)*', '', '\n'.join(answer_line))
                    quest_block['ans']=ans
                    print(answer_line)
                else:
                   option='\n'.join(ques_sec[ques_sec.index(op_splitter):]) 
                
                ques_sec=splitted_with_op
                
                
                op_lines = re.split('\n(\s)*\([a-zA-Z]\)', option) 
               
                print('\n\n\n\n\n')
                
                # for i in op_lines:
                #     if re.search(r'^Ans(wer)*', i) or re.search(r'Correct\sOp', i):
                        
                for op in op_lines:
                    # op = op.encode('ascii')
                    op = re.sub('Op\s', '', op)
                   
                    if op != ' ':
                        options.append(op)
            for i in ques_sec:
                ques.append(i)

            if options:
                quest_block['options'] = options

            quest_block['category']=category
            quest_block['q']='\n'.join(ques)
            quest_block['sub_category']=sub_category
            
            d.append(quest_block)
    print(len(d))
    return d
    
main()
