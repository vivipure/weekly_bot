from util import generate_embeddings_model,remove_newlines
import os
import pandas as pd


def weekly_to_embeddings(dir_name):
    '''
    周刊内容转 embedding 模型
    - dir_name: 目录名称
    '''

    data_file_name = 'data.csv'
    embeddings_file_name = 'embeddings.csv'

    embedding_file_path = dir_name + '/'+embeddings_file_name
    data_file_path = dir_name + '/'+data_file_name

    if os.path.exists(embedding_file_path):
        return 


    markdown_to_csv(data_file_path)

    generate_embeddings_model(data_file_path, embedding_file_path)



def markdown_to_csv(file_path):
    '''
    周刊markdown 转 csv
    '''
    dir = os.path.dirname(file_path)
    if not os.path.exists(dir):
        os.mkdir(dir)

    texts = []
    
    repeat_text1 = "这里记录过去一周，我看到的值得分享的东西，每周五发布。"
    repeat_text2 = "这里记录每周值得分享的科技内容，周五发布。"

    for file in os.listdir("weekly"):
        if file.endswith('.md'):
             with open("weekly/"+file,  "r", encoding="UTF-8") as f:
                line = f.readline()
                h1 = ""
                h2 = ""
                content = ""
                while line:
                    text = line.strip()
                    if text:
                        is_content_add = False
                        temph1 = h1
                        temph2 = h2
                        if text.startswith('# '):
                            title = text.replace('#','')
                            if title.__contains__('：第'):
                                list = title.split('：')
                                title = list[0] +' ('+list[1]+')'
                                h1 = title.strip()
                                pass
                            elif title.__contains__('：'):
                                list = title.split('：')
                                left = list[0].strip()
                                right = list[1].strip()
                                texts.append((left,right))
                                h1 = left
                            else:
                                h1 = title
                            h2 = ''
                        elif text.startswith('## '):
                            h2 = text.replace('##','')
                        else:
                            content +=   '\n'+text if content else text
                            is_content_add = True

                        if is_content_add is False and content:
                            title = '/'.join(filter(lambda x: x, [temph1,temph2])) 
                            content = content.replace(repeat_text1, '').strip()
                            content = content.replace(repeat_text2, '').strip()
                            if content:
                                texts.append((title, content))
                                content = ''
                                
                        
                    line = f.readline()
                    # 最后一行一般为 广告，这里不进行处理

    df = pd.DataFrame(texts, columns = ['fname', 'text'])

    # #Set the text column to be the raw text with the newlines removed
    df['text'] = df.fname + "%% " + remove_newlines(df.text)
    df.to_csv(file_path)
    df.head()

