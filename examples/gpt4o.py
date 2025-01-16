import os
import sys
from argparse import ArgumentParser
from src.tools.lm import OpenAIModel_dashscope
from src.tools.rm import GoogleSearchAli
from src.tools.mindmap import MindMap
from src.actions.outline_generation import OutlineGenerationModule
from src.dataclass.Article import Article
from src.actions.article_generation import ArticleGenerationModule
from src.actions.article_polish import ArticlePolishingModule

def main(args):
    kwargs = {
        'api_key': os.getenv("OPENAI_API_KEY"),
        'temperature': 1.0,
        'top_p': 0.9,
    }
    if args.retriever == 'google':
        rm = GoogleSearchAli(k=args.retrievernum)

    lm = OpenAIModel_dashscope(model=args.llm, max_tokens=2000, **kwargs)

    topic = input('Topic: ')
    file_name = topic.replace(' ', '_')
    mind_map = MindMap(
        retriever=rm,
        gen_concept_lm=lm,
        depth = args.depth
    )

    generator = mind_map.build_map(topic)   
    for layer in generator:
        print(layer)
    mind_map.prepare_table_for_retrieval()

    ogm = OutlineGenerationModule(lm)
    outline = ogm.generate_outline(topic= topic, mindmap = mind_map)

    article_with_outline = Article.from_outline_str(topic=topic, outline_str=outline)
    ag = ArticleGenerationModule(retriever = rm, article_gen_lm = lm, retrieve_top_k = 3, max_thread_num = 10)
    article = ag.generate_article(topic = topic, mindmap = mind_map, article_with_outline = article_with_outline)
    ap = ArticlePolishingModule(article_gen_lm = lm, article_polish_lm = lm)
    article = ap.polish_article(topic = topic, draft_article = article)

    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir)
    if not os.path.exists(f'{args.outputdir}/map'):
        os.makedirs(f'{args.outputdir}/map')
    if not os.path.exists(f'{args.outputdir}/outline'):
        os.makedirs(f'{args.outputdir}/outline')
    if not os.path.exists(f'{args.outputdir}/article'):
        os.makedirs(f'{args.outputdir}/article')
        
    path = f'{args.outputdir}/map/{file_name}'
    with open(path, 'w', encoding='utf-8') as file:
        mind_map.save_map(mind_map.root, path)

    path = f'{args.outputdir}/outline/{file_name}'
    with open(path, 'w', encoding='utf-8') as file:
        file.write(outline)

    path = f'{args.outputdir}/article/{file_name}'
    with open(path, 'w', encoding='utf-8') as file:
        file.write(article.to_string())


    

if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('--outputdir', type=str, default='./results',
                        help='Directory to store the outputs.')
    parser.add_argument('--threadnum', type=int, default=3,
                        help='Maximum number of threads to use. The information seeking part and the article generation'
                             'part can speed up by using multiple threads. Consider reducing it if keep getting '
                             '"Exceed rate limit" error when calling LM API.')
    parser.add_argument('--retriever', type=str,
                        help='The search engine API to use for retrieving information.')
    parser.add_argument('--retrievernum', type=int, default=5,
                        help='The search engine API to use for retrieving information.')
       
    parser.add_argument('--llm', type=str,
                        help='The language model API to use for generating content.')
    parser.add_argument('--depth', type=int, default=2,
                        help='The depth of knowledge seeking.')


    main(parser.parse_args())