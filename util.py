import os
import numpy as np
import openai
import pandas as pd
import tiktoken
from tenacity import ( 
    retry,
    stop_after_attempt,
    wait_random_exponential,)
import time



def remove_newlines(serie):
    '''
    删除多余换行符和空格
    '''
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie


def load_embeddings_model(dir_name):
    '''
    加载 embeddings model
    '''
    file_path = dir_name +'/'+'embeddings.csv'
    if not os.path.exists(file_path):
        print('模型不存在')
        return 
    
    df = pd.read_csv(file_path, index_col=0)
    df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)
    df.head()
    return df



i = 0

@retry(wait=wait_random_exponential(min=5, max=60), stop=stop_after_attempt(6))
def embedding_with_backoff(x):
    '''
    生成模型接口，支持延迟和重试
    '''
    global i
    i = i+1
    print('模型生成：', i)
    result =  openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding']
    time.sleep(15)
    return result

def generate_embeddings_model(data_file_path, target_embedding_path):
    '''
    生成 embeddings 数据
    '''
    if data_file_path and target_embedding_path:
        df = generate_tokens(data_file_path)
        print("生成模型 开始------")
        df['embeddings'] = df.text.apply(lambda x: embedding_with_backoff(x))
        print("生成模型 结束-----")
        df.to_csv(target_embedding_path)
        df.head()



def generate_tokens(data_file_csv):
    '''
    生成 embeddings token 
    '''
    tokenizer = tiktoken.get_encoding("cl100k_base")

    df = pd.read_csv(data_file_csv, index_col=0)
    df.columns = ['title', 'text']

    # Tokenize the text and save the number of tokens to a new column
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

    # Visualize the distribution of the number of tokens per row using a histogram
    df.n_tokens.hist()


    max_tokens = 500

    # Function to split the text into chunks of a maximum number of tokens
    def split_into_many(text, max_tokens = max_tokens):

        # Split the text into sentences
        sentences = text.split('%% ')

        # Get the number of tokens for each sentence
        n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]
        
        chunks = []
        tokens_so_far = 0
        chunk = []

        # Loop through the sentences and tokens joined together in a tuple
        for sentence, token in zip(sentences, n_tokens):

            # If the number of tokens so far plus the number of tokens in the current sentence is greater 
            # than the max number of tokens, then add the chunk to the list of chunks and reset
            # the chunk and tokens so far
            if tokens_so_far + token > max_tokens:
                chunks.append(". ".join(chunk) + ".")
                chunk = []
                tokens_so_far = 0

            # If the number of tokens in the current sentence is greater than the max number of 
            # tokens, go to the next sentence
            if token > max_tokens:
                continue

            # Otherwise, add the sentence to the chunk and add the number of tokens to the total
            chunk.append(sentence)
            tokens_so_far += token + 1
        
        if len(chunks) == 1 and chunks[0] == '.':
            return []

        return chunks
        

    shortened = []

    # Loop through the dataframe

    for row in df.iterrows():

        if row[1]['text'] is None:
            continue

        if row[1]['n_tokens'] > max_tokens:
            shortened += split_into_many(row[1]['text'])
        
        else:
            shortened += split_into_many(row[1]['text'])
            # shortened.append( row[1]['text'] )

    
    df = pd.DataFrame(shortened, columns = ['text'])
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
    df.n_tokens.hist()

    return df
