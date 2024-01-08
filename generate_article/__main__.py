import os
import pandas as pd


from generate_article import ArticleInfo, articles, getIndices
from generate_article.generate import generate


parentPath = os.getcwd()
os.chdir(parentPath)

for article, font in articles:
    article_sheet = pd.read_excel(article)
    font_sheet = pd.read_excel(font)

    headerIndices = getIndices(article_sheet["type"], ["header"])
    textIndices = getIndices(article_sheet["type"], ["text"])
    dateIndex = getIndices(article_sheet["type"], ["date"])[0]
    photoIndex = getIndices(article_sheet["type"], ["photo"])[0]
    captionIndex = getIndices(article_sheet["type"], ["caption"])[0]
    authorIndex = getIndices(article_sheet["type"], ["author"])[0]

    passage_name = str(article.resolve().parent).split(os.sep)[-1]

    article_info = ArticleInfo(
        article_sheet,
        font_sheet,
        passage_name,
        headerIndices,
        textIndices,
        dateIndex,
        photoIndex,
        captionIndex,
        authorIndex,
    )

    print("\nnew article started: " + passage_name + "\n")
    generate(article_info)
