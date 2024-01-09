from wand.image import Image

from generate_article import (
    ArticleInfo,
    roundPosition,
    page_indent_horizontal,
    center_text,
)

from generate_article.draw_robot import indent_from_robot, robot_start


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

    caption_position_y = roundPosition(photo_position[1] * 1.15 + photo_height)

    draw.line(
        (robot_start * 1.8, caption_position_y - 20),
        (image.width - robot_start * 1.8, caption_position_y - 20),
    )

    draw.line(
        (robot_start * 1.8, caption_position_y + 15),
        (image.width - robot_start * 1.8, caption_position_y + 15),
    )

    draw(image)

    draw.font_size = 20
    draw.font_weight = article_sheet["weight"][captionIndex]
    draw.font_style = article_sheet["style"][captionIndex]
    draw.fill_color = article_sheet["color"][captionIndex]

    print(article_sheet["content"][captionIndex])
    caption_position_x = roundPosition(
        center_text(draw, image, article_sheet["content"][captionIndex])
    )

    if caption_position_x < 0:
        caption_position_x = 0

    draw.text(
        caption_position_x,
        caption_position_y,
        article_sheet["content"][captionIndex],
    )

    return [caption_position_x, caption_position_y]
