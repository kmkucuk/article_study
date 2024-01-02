from collections import deque
from pathlib import Path
import os
import pandas as pd
import numpy


def getIndices(yourList, searchElements):
    yourIndices = []
    for i in range(0, len(yourList)):
        currentElement = yourList[i]
        for k in searchElements:
            # print(k)
            if k == currentElement:
                yourIndices.append(i)
                break

    return yourIndices


def roundPosition(pixelCoordinates):
    return int(round(pixelCoordinates))


def eval_metrics(txt, draw, image):
    """Quick helper function to calculate width/height of text."""
    metrics = draw.get_font_metrics(image, txt, True)
    return (metrics.text_width, metrics.text_height)


p = Path(".")
files = deque([x for x in p.iterdir()])
current_path = Path(".")


articles = []

while files:
    _file = files.popleft()

    if _file.is_dir():
        files.extend(_file.iterdir())
        continue

    if "output" in str(_file.resolve().parent):
        continue

    if _file.name.startswith("article") and _file.suffix == ".xlsx":
        articles.append(
            (
                _file.resolve(),
                Path.joinpath(_file.resolve().parent, "fonts_and_kerning.xlsx"),
            )
        )

    # if path.isfile(_file):
    #     if _file.startswith("article") and _file.endswith(".xlsx"):
    #         articles.push(_file)

    # if path.isdir(_file):
    #     files.extend(os.listdir(_file))


print(f"found {len(articles)} article sheets")


article_sheet   = pd.read_excel(articles[0][0])
font_sheet      = pd.read_excel(articles[0][1])


# print("size of excel sheet", numpy.shape(article_sheet))
## ARTICLE SHEET VARIABLES ##
# get headers of the excel file
sheet_headers = article_sheet.columns.tolist()
# print(sheet_headers)
# # get set ID column
# column_type         = 'type'
# # get color column
# column_color        = 'color'
# # get format column
# column_format       = 'format'
# # get weight column
# column_weight       = 'weight'
# # get font column
# column_font         = 'font'
# # get content column
# column_content      = 'content'

headerIndices   = getIndices(article_sheet["type"], ["header"])
textIndices     = getIndices(article_sheet["type"], ["text"])
dateIndex       = getIndices(article_sheet["type"], ["date"])[0]
photoIndex      = getIndices(article_sheet["type"], ["photo"])[0]
captionIndex    = getIndices(article_sheet["type"], ["caption"])[0]
authorIndex     = getIndices(article_sheet["type"], ["author"])[0]


## FONT SHEET VARIABLES ##
font_headers    = font_sheet.columns
# get font name columns
fontColumn      = font_headers[0]
# get scale columns
fontColumn      = font_headers[1]

# Create a black canvas img_widthximg_height pixels (1024x768)
img_width = 1024
img_height = 1500

img_center_x = roundPosition(img_width / 2)
img_center_y = roundPosition(img_height / 2)

# left - right indent of text (%2.5 for each side)
page_indent_horizontal = roundPosition(img_width / 40)

# length of text wrapping
wrap_width = roundPosition(img_width - page_indent_horizontal * 2)

# top-bottom limit of text (%2.5 for each side)
page_indent_vertical = roundPosition(img_height / 40)

# top - bottom indent
wrap_height = roundPosition(img_height - page_indent_vertical * 2)
