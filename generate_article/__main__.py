# Needed this on macOS Monterey:
# export WAND_MAGICK_LIBRARY_SUFFIX="-7.Q16HDRI"
# export MAGICK_HOME=/opt/homebrew

# activate image processing environment through conda
# conda activate image_processing

# instal image magick's python bind library "wand" through pip, conda's installation fails.
# e.g:  pip install wand

# how to resize and adjust spacing?
# first resize to target font using gen_normalization function in js, then space the font using code below

import os
from collections import deque
from pathlib import Path
import numpy
import pandas as pd



from generate_article import articles
from generate_article.generate import generate


parentPath = os.getcwd()
os.chdir(parentPath)


########################################
# Name of the study passages belong to #
# e.g. child_study
studyName = "images"

link_bounds = []


for article, font in articles:
    article_sheet = pd.read_excel(article)
    font_sheet = pd.read_excel(font)


    passage_name = str(article.resolve().parent).split(os.sep)[-1]
    
    # print(str(article.resolve().parent))
    # print(str(article.resolve().parent).split(os.sep))
    print('\nnew article started: '+passage_name+"\n")
    generate(article_sheet, font_sheet, passage_name)
