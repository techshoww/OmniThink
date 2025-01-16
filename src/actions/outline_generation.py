import dspy
from src.tools.mindmap import MindMap
from src.utils.ArticleTextProcessing import ArticleTextProcessing
from typing import Union, Optional, Tuple

# This code is originally sourced from Repository STORM
# URL: [https://github.com/stanford-oval/storm]

class OutlineGenerationModule():

    def __init__(self,
                 outline_gen_lm: Union[dspy.dsp.LM, dspy.dsp.HFModel]):
        super().__init__()
        self.outline_gen_lm = outline_gen_lm
        self.write_outline = WriteOutline(engine=self.outline_gen_lm)

    def generate_outline(self,
                         topic: str,
                         mindmap: MindMap,
                         ):

        concepts = mindmap.export_categories_and_concepts()
        result = self.write_outline(topic=topic, concepts=concepts)

        return result

class WriteOutline(dspy.Module):
    """Generate the outline for the Wikipedia page."""

    def __init__(self, engine: Union[dspy.dsp.LM, dspy.dsp.HFModel]):
        super().__init__()
        self.draft_page_outline = dspy.Predict(WritePageOutline)
        self.polish_page_outline = dspy.Predict(PolishPageOutline)
        self.engine = engine

    def forward(self, topic: str, concepts: str):
        
        with dspy.settings.context(lm=self.engine):
            outline = ArticleTextProcessing.clean_up_outline(
                self.draft_page_outline(topic=topic).outline)
            outline = ArticleTextProcessing.clean_up_outline(
                self.polish_page_outline(draft=outline, concepts=concepts).outline)

        return outline


class PolishPageOutline(dspy.Signature):
    """
    Improve an outline for a Wikipedia page. You already have a draft outline that covers the general information. Now you want to improve it based on the concept learned from an information-seeking to make it more informative.
    Here is the format of your writing:
    1. Use "#" Title" to indicate section title, "##" Title" to indicate subsection title, "###" Title" to indicate subsubsection title, and so on.
    2. Do not include other information.
    3. Do not include topic name itself in the outline.
    """

    draft = dspy.InputField(prefix="Current outline:\n ", format=str)
    concepts = dspy.InputField(prefix="The information you learned from the conversation:\n", format=str)
    outline = dspy.OutputField(prefix='Write the page outline:\n', format=str)


class WritePageOutline(dspy.Signature):
    """
    Write an outline for a Wikipedia page.
    Here is the format of your writing:
    1. Use "#" Title" to indicate section title, "##" Title" to indicate subsection title, "###" Title" to indicate subsubsection title, and so on.
    2. Do not include other information.
    3. Do not include topic name itself in the outline.
    """

    topic = dspy.InputField(prefix="The topic you want to write: ", format=str)
    outline = dspy.OutputField(prefix="Write the Wikipedia page outline:\n", format=str)

