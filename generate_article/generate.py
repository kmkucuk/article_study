from wand.image import Image
from wand.drawing import Drawing
from wand.display import display
from pandas import DataFrame

import os

from generate_article import (
    ArticleInfo,
    roundPosition,
    page_indent_horizontal,
    page_indent_vertical,
    img_height,
    wrap_width,
    img_width,
)

from generate_article.draw_header import draw_header
from generate_article.draw_image import draw_image

from generate_article.draw_text import draw_text

from generate_article.draw_robot import draw_robot


def get_header_pos(header_indices):
    header_postions = []

    previous_pos = [page_indent_horizontal, page_indent_vertical]

    for header_position in header_indices:
        pos = []
        if header_position == 0:  # Blue Box
            pos = [
                page_indent_horizontal,
                previous_pos[1],
            ]
        elif header_position == 1:  # Title
            pos = [
                page_indent_horizontal,
                roundPosition(previous_pos[1] * 1.8),
            ]
        elif header_position == 2:  # Subtitle
            pos = [
                page_indent_horizontal,
                previous_pos[1],
            ]
        else:  # Shouldn't happen
            pos = [
                page_indent_horizontal,
                previous_pos[1],
            ]

        previous_pos = pos
        header_postions.append(pos)
    return header_postions


parentPath = os.getcwd()
os.chdir(parentPath)


def generate(article_info: ArticleInfo):
    font_sheet = article_info.font_sheet
    article_sheet = article_info.article_sheet
    passage_name = article_info.passage_name
    dateIndex = article_info.dateIndex
    authorIndex = article_info.authorIndex

    header_postions: list[list[float]] = get_header_pos(article_info.headerIndices)

    for _, data in font_sheet.iterrows():
        font_name = data["Font"]
        if font_name == "Times":
            font_name = "Times New Roman"
        elif font_name == "Comic Sans":
            font_name = "Comic Sans MS"

        kerning = data["Kerning"]
        print("\nfont: " + font_name + "\n")

        with Image(
            width=img_width,
            height=img_height,
            pseudo="xc:white",
            units="pixelsperinch",  # format="png"
        ) as image_with_links, Image(
            width=img_width, height=img_height, pseudo="xc:white", units="pixelsperinch"
        ) as image_without_links:

            with Drawing() as draw_with_links, Drawing() as draw_without_links:
                draw_with_links.font_family, draw_without_links.font_family = (
                    font_name,
                    font_name,
                )
                draw_with_links.text_kerning, draw_without_links.text_kerning = (
                    kerning,
                    kerning,
                )

                draw_header(
                    draw_with_links,
                    image_with_links,
                    article_info,
                    header_postions,
                )

                draw_header(
                    draw_without_links,
                    image_without_links,
                    article_info,
                    header_postions,
                )

                draw_with_links(image_with_links)
                draw_without_links(image_without_links)

                draw_without_links.pop()
                draw_with_links.pop()

                # draw photo
                def draw_photo(draw, image):
                    draw.push()
                    caption_position = draw_image(
                        image, draw, article_info, header_postions[1][1] * 1.3
                    )
                    draw(image)
                    draw.pop()

                    return caption_position

                draw_photo(draw_with_links, image_with_links)
                caption_position = draw_photo(draw_without_links, image_without_links)

                ####################
                ### ROBOT SECTION ##
                ####################

                robot_position = [
                    page_indent_horizontal,
                    int(caption_position[1] * 1.03),
                ]
                draw_robot(image_with_links, robot_position)
                draw_robot(image_without_links, robot_position)

                author_position = [
                    roundPosition(robot_position[0] * 1.45),
                    roundPosition(robot_position[1] * 1.03),
                ]

                for draw in [draw_without_links, draw_with_links]:
                    draw.push()

                    draw.font_weight = article_sheet["weight"][authorIndex]
                    draw.font_family = "Times New Roman"
                    draw.font_size = 15
                    draw.text(
                        author_position[0],
                        author_position[1],
                        article_sheet["content"][authorIndex],
                    )

                    draw.pop()

                date_position = [
                    page_indent_horizontal,
                    roundPosition(author_position[1] * 1.1),
                ]

                for draw in [draw_without_links, draw_with_links]:
                    draw.push()

                    draw.font_weight = article_sheet["weight"][dateIndex]
                    draw.font_family = "Roboto"
                    draw.font_size = 13
                    draw.text(
                        date_position[0],
                        date_position[1],
                        article_sheet["content"][dateIndex],
                    )

                    draw.pop()

                link_bounds = []

                # draw text
                def _draw_text(draw, image, has_links):
                    draw.push()
                    text_position = [
                        roundPosition(page_indent_horizontal),
                        roundPosition(date_position[1] * 1.05),
                    ]

                    link_bounds = draw_text(
                        image, draw, article_info, text_position, has_links
                    )

                    draw(image)

                    draw.pop()

                    return link_bounds

                for draw, image, has_links in [
                    (draw_without_links, image_without_links, False),
                    (draw_with_links, image_with_links, True),
                ]:
                    link_bounds = _draw_text(draw, image, has_links)
                # path to save images #
                # set_images
            pathSlash = os.path.sep

            save_directory = pathSlash.join((parentPath, "output", "all"))

            # check if save path exists, if not, create one
            if not os.path.isdir(save_directory):
                os.makedirs(save_directory)

            # change directory
            if not save_directory == os.getcwd():
                os.chdir(save_directory)
            # print('Current font: '+fontName+'\t set ID:'+setid+'\n')

            passageImageName = font_name

            image_with_links.save(
                filename=os.path.join(
                    os.getcwd(), f"{passage_name}_{passageImageName}_Link.jpg"
                )
            )

            image_without_links.save(
                filename=os.path.join(
                    os.getcwd(), f"{passage_name}_{passageImageName}_NoLink.jpg"
                )
            )

            link_metrics: DataFrame = DataFrame(
                link_bounds, columns=["text", "x", "y", "width", "height"]
            )

            link_metrics.to_excel(
                os.path.join(
                    os.getcwd(),
                    f"{passage_name}_{passageImageName}_links.xlsx",
                ),
                index=False,
            )

            # Display function may require editing diplsay.py in wand library
            # to display image in a new window
            # Move the "." +
            # to the suffix parameter
            # A pull request has been made to the wand library
            # to fix this issue

            # display(image_with_links)
            # exit(0)

            # print("image finished: ", passageImageName)

            # return to parent path
            os.chdir(parentPath)
