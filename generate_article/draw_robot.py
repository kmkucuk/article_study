# text and image size / positions
from generate_article import roundPosition, wrap_width, page_indent_horizontal

from wand.image import Image


size_robotLogo = 70

robot_start = roundPosition(page_indent_horizontal + size_robotLogo / 2)


width_multipler = 1.46


def draw_robot(image, pos_robotLogo):
    with Image(
        width=int(size_robotLogo * width_multipler),
        height=size_robotLogo,
        filename="vrl_robot.png",
    ) as robot:
        # resize robot logo
        robot.resize(int(size_robotLogo * width_multipler), size_robotLogo, blur=1)

        # overlay robot logo on background
        image.composite(robot, left=pos_robotLogo[0], top=pos_robotLogo[1])
