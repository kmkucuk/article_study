from wand.color import Color
from wand.drawing import Drawing

from generate_article import roundPosition


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
    header_indices,
    article_sheet,
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
    # loop over headers and draw them on image
    for header_position in header_indices:
        # header text
        currentHeader = str(article_sheet["content"][header_position])
        # assign font size
        if header_position == 0:
            draw.font_size = 30
        elif header_position == 1:
            draw.font_size = 25
        else:
            draw.font_size = 20
        # assign letter spacing
        draw.text_kerning = 0
        # text color
        draw.fill_color = article_sheet["color"][header_position]
        # align text to left
        draw.text_alignment = "left"
        # adjust font style
        draw.font_style = article_sheet["style"][header_position]
        # adjust font weight
        draw.font_weight = int(str(article_sheet["weight"][header_position]))

        draw.text(
            roundPosition(header_postions[header_position][0]),
            roundPosition(header_postions[header_position][1]),
            currentHeader,
        )
