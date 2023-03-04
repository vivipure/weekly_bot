import openai
from config import HTTP_PROXY,HTTPS_PROXY,OPENAI_API_KEY
from util import load_embeddings_model
from weekly import weekly_to_embeddings
from openai_bot import answer_question

def init_openai_env():
    '''
    初始化代理和token
    '''
    proxies = {
        'http': HTTP_PROXY,
        'https': HTTPS_PROXY
    }
    openai.proxy = proxies
    openai.api_key = OPENAI_API_KEY




def main():
    init_openai_env()
    # 数据和模型生成目录
    dir_name = 'processed/weekly'

    weekly_to_embeddings(dir_name)
    
    df = load_embeddings_model(dir_name)

    question = input('请输入问题：')
    while question:
        print("Q1: ",answer_question(df, question=question, debug=False))
        question = input('请输入问题：')
   

if __name__ == '__main__':
    main()