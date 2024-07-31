from wand.image import Image

from generate_article import ArticleInfo, roundPosition, center_text, eval_metrics

from generate_article.draw_robot import indent_from_robot, robot_start


def draw_image(image, draw, article_info: ArticleInfo, y_position: float) -> list[int]:
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

    img_width = 600
    with Image(filename=article_sheet["content"][photoIndex]) as photo:
        photo.resize(int(img_width * 1.8), img_width)

        photo_height = photo.height
        image.composite(
            photo,
            left=int(photo_position[0] - photo.width / 2),
            top=photo_position[1],
        )

    caption_position_y = roundPosition(photo_position[1] * 1.16 + photo_height)

    draw.line(
        (robot_start * 1.8, caption_position_y - 25),
        (image.width - robot_start * 1.8, caption_position_y - 25),
    )

    draw(image)

    caption: str = article_sheet["content"][captionIndex]

    caption, author = caption[: caption.index("(")], caption[caption.index("(") :]

    draw.font_size = 20
    draw.font_weight = article_sheet["weight"][captionIndex]
    draw.font_style = article_sheet["style"][captionIndex]
    draw.fill_color = article_sheet["color"][captionIndex]

    caption_position_x = roundPosition(center_text(draw, image, caption))

    draw.text(
        caption_position_x,
        caption_position_y,
        caption,
    )

    caption_metrics = eval_metrics(caption, draw, image)
    draw.font_size = 18

    author_position_x = roundPosition(center_text(draw, image, author))
    author_position_y = roundPosition(caption_position_y + caption_metrics[1])

    draw.text(
        roundPosition(center_text(draw, image, author)),
        roundPosition(caption_position_y + caption_metrics[1]),
        author,
    )

    author_metrics = eval_metrics(author, draw, image)

    draw.line(
        (robot_start * 1.8, author_position_y + 15),
        (image.width - robot_start * 1.8, author_position_y + 15),
    )

    return [author_position_x, author_position_y]
