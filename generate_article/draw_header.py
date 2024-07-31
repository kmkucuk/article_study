from wand.color import Color
from wand.drawing import Drawing

from generate_article import (
    ArticleInfo,
    eval_metrics,
    roundPosition,
    center_text,
    img_width,
)


def draw_header(
    draw,
    image,
    article_info: ArticleInfo,
    header_postions,
):
    header_indices = article_info.headerIndices
    article_sheet = article_info.article_sheet

    # loop over headers and draw them on image
    for index, header_position in enumerate(header_postions):
        draw.push()
        location = header_indices[index]
        # header text
        currentHeader = article_sheet["content"][location]  # .strip().split(" ")
        # assign font size

        word_width, word_height = eval_metrics(
            currentHeader,
            draw,
            image,
        )

        line_height = 1
        # title
        if index == 0:
            header_position[0] = (img_width / 2) - word_width
            draw.font_size = 40
            draw.font_family = "Apple Chancery"
        elif index == 1:
            draw.font_size = 28
            draw.font_family = "Times New Roman"
            break
        else:
            draw.font_size = 22
            draw.font_family = "Times New Roman"
            break

        # assign letter spacing
        draw.text_kerning = 0
        # align text to left
        draw.text_alignment = "left"
        # adjust font style
        draw.font_style = article_sheet["style"][location]
        # adjust font weight
        draw.font_weight = int(str(article_sheet["weight"][location]))

        print(img_width / 2, word_width, header_position[0])

        draw.text(
            roundPosition(header_position[0]),
            roundPosition(header_position[1]),
            currentHeader,
        )
        draw(image)
        draw.pop()
