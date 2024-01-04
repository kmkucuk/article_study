from wand.image import Image

from generate_article import (
    ArticleInfo,
    roundPosition,
    page_indent_horizontal,
)

from generate_article.draw_robot import indent_from_robot


def draw_image(image, draw, article_info: ArticleInfo, y_position) -> list[int]:
    """
    Draws an image on the article sheet.
    Returns the height of the image.
    """
    article_sheet = article_info.article_sheet
    photoIndex = article_info.photoIndex
    captionIndex = article_info.captionIndex

    photo_position = [
        roundPosition(image.width * 0.5),
        roundPosition(y_position),
    ]

    photo_height = 0

    with Image(filename=article_sheet["content"][photoIndex]) as photo:
        photo.resize(525, 296)

        photo_height = photo.height
        image.composite(
            photo,
            left=int(photo_position[0] - photo.width / 2),
            top=photo_position[1],
        )

    caption_position = [
        indent_from_robot,
        roundPosition(photo_position[1] * 1.15 + photo_height),
    ]

    draw.line(
        (caption_position[0] - page_indent_horizontal, caption_position[1] - 20),
        (image.width - page_indent_horizontal, caption_position[1] - 20),
    )

    draw.line(
        (caption_position[0] - page_indent_horizontal, caption_position[1] + 15),
        (image.width - page_indent_horizontal, caption_position[1] + 15),
    )

    draw(image)

    draw.font_weight = 200
    draw.font_size = 12
    draw.font_style = article_sheet["style"][captionIndex]
    draw.fill_color = article_sheet["color"][captionIndex]

    draw.text(
        caption_position[0],
        caption_position[1],
        article_sheet["content"][captionIndex],
    )

    return caption_position
