from wand.color import Color
from wand.drawing import Drawing

from generate_article import ArticleInfo, roundPosition, center_text


def draw_rectangle(draw, pos_left, pos_right, roi_width, roi_height):
    """Let's draw a blue box so we can identify what
    our region of intrest is."""
    draw.push()
    draw.stroke_color = Color("rgb(100, 100, 100)")
    draw.fill_color = Color("rgb(0, 176, 240)")
    draw.rectangle(left=pos_left, top=pos_right, width=roi_width, height=roi_height)
    draw.pop()


def draw_header(
    draw,
    image,
    article_info: ArticleInfo,
    pos_blueRect,
    size_blueRect,
    header_postions,
):
    draw_rectangle(
        draw,
        pos_blueRect[0],
        pos_blueRect[1],
        size_blueRect[0],
        size_blueRect[1],
    )
    header_indices = article_info.headerIndices
    article_sheet = article_info.article_sheet

    # loop over headers and draw them on image
    for index, header_position in enumerate(header_postions):
        draw.push()
        location = header_indices[index]
        # header text
        currentHeader = article_sheet["content"][location]
        # assign font size

        x_position = header_position[0]

        if index == 0:
            draw.font_size = 30
            draw.font_family = "Arial Narrow"
        elif index == 1:
            draw.font_size = 30
            draw.font_family = "Times New Roman"
            x_position = center_text(draw, image, currentHeader)
        else:
            draw.font_size = 22
            draw.font_family = "Times New Roman"
            x_position = center_text(draw, image, currentHeader)

        # assign letter spacing
        draw.text_kerning = 0
        # text color
        draw.fill_color = article_sheet["color"][location]
        # align text to left
        draw.text_alignment = "left"
        # adjust font style
        draw.font_style = article_sheet["style"][location]
        # adjust font weight
        draw.font_weight = int(str(article_sheet["weight"][location]))

        draw.text(
            roundPosition(x_position),
            roundPosition(header_position[1]),
            currentHeader,
        )
        draw.pop()
