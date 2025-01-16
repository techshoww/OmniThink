import time
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from http import HTTPStatus
# from src.DeepThink.modules.mindmap import MindMap
# from src.DeepThink.modules.outline_generation import OutlineGenerationModule
# from src.DeepThink.modules.storm_dataclass import Article
# from src.DeepThink.modules.article_generation import ArticleGenerationModule
# from src.DeepThink.modules.article_polish import ArticlePolishingModule
from src.lm import OpenAIModel, OpenAIModel_New, OpenAIModel_6M
from src.rm import BingSearch, BingSearchAli, GoogleSearchAli
from src.utils import load_api_key
import random
import sys
sys.path.append('./src/DeepThink/modules')
import json
from mindmap import MindMap
from outline_generation import OutlineGenerationModule
from storm_dataclass import Article

from article_generation import ArticleGenerationModule
from article_polish import ArticlePolishingModule

import jsonlines
from streamlit_timeline import st_timeline
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables and API keys
load_api_key(toml_file_path='/mnt/8t/xzk/reDeepThink/secrets.toml')
load_dotenv()

openai_kwargs = {
    'api_key': os.getenv("OPENAI_API_KEY"),
    'api_provider': os.getenv('OPENAI_API_TYPE'),
    'temperature': 1.0,
    'top_p': 0.9,
    'api_base': os.getenv('AZURE_API_BASE'),
    'api_version': os.getenv('AZURE_API_VERSION'),
}

# Initialize models
lm = OpenAIModel_New(model='gpt-4o', max_tokens=1000, **openai_kwargs)

lm4outline = OpenAIModel_New(model='gpt-4o', max_tokens=1000, **openai_kwargs)
lm4gensection = OpenAIModel_New(model='gpt-4o', max_tokens=2000, **openai_kwargs)
lm4polish = OpenAIModel_New(model='gpt-4o', max_tokens=8000, **openai_kwargs)
rm = GoogleSearchAli(ydc_api_key=os.getenv('SEARCH_ALI_API_KEY'), k=5)



# Set Streamlit configuration and title
st.set_page_config(page_title='OmniThink', layout="wide")
st.title('🤔 OmniThink')

# Sidebar for configuration and examples
with st.sidebar:
    st.header('Configuration')
    MAX_ROUNDS = st.number_input('检索深度：', min_value=0, max_value=10, value=2, step=1)
    n_max_doc = st.number_input('单次检索网页数量：', min_value=1, max_value=50, value=10, step=5)
    st.header('Examples')
    examples = ['AlphaFold', '2024 Hualien City Earthquake', 'Taylor Swift']
    selected_example = st.selectbox('示例：', examples)

mind_map = MindMap(
    retriever=rm,
    gen_concept_lm = lm4outline,
    search_top_k = n_max_doc,
    depth= MAX_ROUNDS
)

def Think(input_topic):

    generator = mind_map.build_map(input_topic)   

    st.markdown(f'正在深度检索关于 **{input_topic}** 的内容...')
    for idx, layer in enumerate(generator):
        print(layer)
        print('layer!!!')
        st.markdown(f'**第{idx + 1}层深度思考检索...**')
        for node in layer:
            category = node.category.replace('[', '').replace(']', '')

            print(f'category: {category}')
            with st.expander(f'{category}'):
                st.markdown(f'### {node.category}')
                for concept in node.concept:
                    st.markdown(f'* {concept}')
    
    mind_map.prepare_table_for_retrieval()
    return '__finish__', '__finish__'

def GenOutline(input_topic):
    ogm = OutlineGenerationModule(lm)
    outline = ogm.generate_outline(topic= input_topic, mindmap = mind_map)

    return outline

def GenArticle(input_topic, outline):

    article_with_outline = Article.from_outline_str(topic=input_topic, outline_str=outline)
    ag = ArticleGenerationModule(retriever = rm, article_gen_lm = lm, retrieve_top_k = 3, max_thread_num = 10)
    article = ag.generate_article(topic = topic, mindmap = mind_map, article_with_outline = article_with_outline)
    ap = ArticlePolishingModule(article_gen_lm = lm, article_polish_lm = lm)
    article = ap.polish_article(topic = topic, draft_article = article)
    return article.to_string()

with st.form('my_form'):
    topic = st.text_input('请输入你感兴趣的主题', value=selected_example, placeholder='请输入你感兴趣的主题')
    submit_button = st.form_submit_button('生成')

    if submit_button:
        if topic:
            st.markdown('### 思考过程')
            summary, news_timeline = Think(topic)
            st.session_state.summary = summary
            st.session_state.news_timeline = news_timeline
            with st.expander("大纲生成", expanded=True):
                outline = GenOutline(topic)
                st.text(outline)
            with st.expander("文章生成", expanded=True):
                article = GenArticle(topic, outline)
                st.text(article)
        else:
            st.error('请输入主题')


