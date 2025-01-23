import concurrent.futures
import copy
import logging
from concurrent.futures import as_completed
from typing import List, Union
import random
import dspy
import sys

from src.utils.ArticleTextProcessing import ArticleTextProcessing

# This code is originally sourced from Repository STORM
# URL: [https://github.com/stanford-oval/storm]
class ArticleGenerationModule():
    """
    The interface for article generation stage. Given topic, collected information from
    knowledge curation stage, generated outline from outline generation stage, 
    """

    def __init__(self,
                 retriever,
                 article_gen_lm=Union[dspy.dsp.LM, dspy.dsp.HFModel],
                 retrieve_top_k: int = 10,
                 max_thread_num: int = 10,
                ):
        super().__init__()
        self.retrieve_top_k = retrieve_top_k
        self.article_gen_lm = article_gen_lm
        self.max_thread_num = max_thread_num
        self.retriever = retriever
        self.section_gen = ConvToSection(engine=self.article_gen_lm)


    def generate_section(self, topic, section_name, mindmap, section_query, section_outline):
        collected_info = mindmap.retrieve_information(queries=section_query,
                                                                    search_top_k=self.retrieve_top_k)
        output = self.section_gen(
            topic=topic,
            outline=section_outline,
            section=section_name,
            collected_info=collected_info,
        )

        return {"section_name": section_name, "section_content": output.section, "collected_info": collected_info}

    def generate_article(self,
                         topic: str,
                         mindmap,
                         article_with_outline,
                         ):
        """
        Generate article for the topic based on the information table and article outline.
        """
        mindmap.prepare_table_for_retrieval()

        sections_to_write = article_with_outline.get_first_level_section_names()
        section_output_dict_collection = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_thread_num) as executor:
            future_to_sec_title = {}
            for section_title in sections_to_write:
                section_query = article_with_outline.get_outline_as_list(
                    root_section_name=section_title, add_hashtags=False
                )
                queries_with_hashtags = article_with_outline.get_outline_as_list(
                    root_section_name=section_title, add_hashtags=True
                )
                section_outline = "\n".join(queries_with_hashtags)

                future_to_sec_title[
                    executor.submit(self.generate_section, 
                                    topic, section_title, mindmap, section_query,section_outline)
                ] = section_title

            for future in concurrent.futures.as_completed(future_to_sec_title):
                section_output_dict_collection.append(future.result())

        article = copy.deepcopy(article_with_outline)
        for section_output_dict in section_output_dict_collection:
            article.update_section(parent_section_name=topic,
                                   current_section_content=section_output_dict["section_content"],
                                   current_section_info_list=section_output_dict["collected_info"],
                                )

        article.post_processing()

        return article

class ConvToSection(dspy.Module):
    """Use the information collected from the information-seeking conversation to write a section."""
    def __init__(self, engine: Union[dspy.dsp.LM, dspy.dsp.HFModel]):
        super().__init__()
        self.write_section = dspy.Predict(WriteSection)
        self.engine = engine

    def forward(self, topic: str, outline:str, section: str, collected_info: List):
        all_info = ''
        for idx, info in enumerate(collected_info):
            all_info += f'[{idx + 1}]\n' + '\n'.join(info['snippets'])
            all_info += '\n\n'

        all_info = ArticleTextProcessing.limit_word_count_preserve_newline(all_info, 1500)

        with dspy.settings.context(lm=self.engine):
            section = ArticleTextProcessing.clean_up_section(
                self.write_section(topic=topic, info=info, section=section).output)
         
        section = section.replace('\[','[').replace('\]',']')
        return dspy.Prediction(section=section)

class WriteSection(dspy.Signature):
    """Write a Wikipedia section based on the collected information.

    Here is the format of your writing:
        1. Use "#" Title" to indicate section title, "##" Title" to indicate subsection title, "###" Title" to indicate subsubsection title, and so on.
        2. Use [1], [2], ..., [n] in line (for example, "The capital of the United States is Washington, D.C.[1][3]."). You DO NOT need to include a References or Sources section to list the sources at the end.
        3. The language style should resemble that of Wikipedia: concise yet informative, formal yet accessible.
    """
    info = dspy.InputField(prefix="The Collected information:\n", format=str)
    topic = dspy.InputField(prefix="The topic of the page: ", format=str)
    section = dspy.InputField(prefix="The section you need to write: ", format=str)
    output = dspy.OutputField(
        prefix="Write the section with proper inline citations (Start your writing with # section title. Don't include the page title or try to write other sections):\n",
        format=str)
