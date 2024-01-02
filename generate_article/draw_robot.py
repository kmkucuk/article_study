# text and image size / positions
from generate_article import roundPosition, wrap_width, page_indent_horizontal

from wand.image import Image


size_robotLogo = [roundPosition(wrap_width * 0.1), 55]

indent_from_robot = roundPosition(page_indent_horizontal + 1.3 * size_robotLogo[0])


def draw_robot(image, pos_robotLogo):
    with Image(
        width=size_robotLogo[0], height=size_robotLogo[1], filename="vrl_robot.png"
    ) as robot:
        # resize robot logo
        robot.resize(size_robotLogo[0], size_robotLogo[1], blur=1)

        # overlay robot logo on background
        image.composite(robot, left=pos_robotLogo[0], top=pos_robotLogo[1])
