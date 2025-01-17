import copy
from typing import Union
import dspy
from src.utils.ArticleTextProcessing import ArticleTextProcessing

# This code is originally sourced from Repository STORM
# URL: [https://github.com/stanford-oval/storm]
class ArticlePolishingModule():
    """
    The interface for article generation stage. Given topic, collected information from
    knowledge curation stage, generated outline from outline generation stage.
    """

    def __init__(self,
                 article_gen_lm: Union[dspy.dsp.LM, dspy.dsp.HFModel],
                 article_polish_lm: Union[dspy.dsp.LM, dspy.dsp.HFModel]):
        self.article_gen_lm = article_gen_lm
        self.article_polish_lm = article_polish_lm

        self.polish_page = PolishPageModule(
            write_lead_engine=self.article_gen_lm,
            polish_engine=self.article_polish_lm
        )

    def polish_article(self,
                       topic: str,
                       draft_article,
                       remove_duplicate: bool = False):
        """
        Polish article.

        Args:
            topic (str): The topic of the article.
            draft_article (StormArticle): The draft article.
            remove_duplicate (bool): Whether to use one additional LM call to remove duplicates from the article.
        """

        article_text = draft_article.to_string()
        remove_duplicate = True
        polish_result = self.polish_page(topic=topic, draft_page=article_text, polish_whole_page=remove_duplicate)

        polished_article = polish_result.page

        polished_article_dict = ArticleTextProcessing.parse_article_into_dict(polished_article)
        polished_article = copy.deepcopy(draft_article)
        polished_article.insert_or_create_section(article_dict=polished_article_dict)
        polished_article.post_processing()
        return polished_article



class PolishPage(dspy.Signature):
    """You are a faithful text editor that is good at finding repeated information in the article and deleting them to make sure there is no repetition in the article. You won't delete any non-repeated part in the article. You will keep the inline citations and article structure (indicated by "#", "##", etc.) appropriately. Do your job for the following article."""
    article = dspy.InputField(prefix="The article you need to polish:\n", format=str)
    page = dspy.OutputField(
        prefix="Your revised article:\n",
        format=str)


class PolishPageModule(dspy.Module):
    def __init__(self, write_lead_engine: Union[dspy.dsp.LM, dspy.dsp.HFModel],
                 polish_engine: Union[dspy.dsp.LM, dspy.dsp.HFModel]):
        super().__init__()
        self.write_lead_engine = write_lead_engine
        self.polish_engine = polish_engine
        self.polish_page = dspy.Predict(PolishPage)

    def forward(self, topic: str, draft_page: str, polish_whole_page: bool = True):

        with dspy.settings.context(lm=self.polish_engine):
            page = self.polish_page(article=draft_page).page

        return dspy.Prediction(page=page)


