from wand.image import Image

from generate_article import (
    ArticleInfo,
    roundPosition,
    center_text,
    eval_metrics,
    page_indent_horizontal,
    img_width,
)

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
        page_indent_horizontal,
        roundPosition(y_position),
    ]

    with Image(filename=article_sheet["content"][photoIndex]) as photo:
        photo.resize(int(img_width * 0.75), 600)

        image.composite(
            photo,
            # left=int(photo_position[0] - photo.width / 2),
            left=photo_position[0],
            top=photo_position[1],
        )

        caption_position_y = roundPosition(photo_position[1] * 1.16 + photo.height)

    draw(image)

    caption: str = article_sheet["content"][captionIndex]

    draw.font_size = 15
    draw.font_weight = article_sheet["weight"][captionIndex]
    draw.font_style = article_sheet["style"][captionIndex]
    draw.fill_color = article_sheet["color"][captionIndex]
    # exit(0)

    draw.text(
        page_indent_horizontal,
        caption_position_y,
        caption,
    )

    caption_metrics = eval_metrics(caption, draw, image)

    return [page_indent_horizontal, caption_position_y]
