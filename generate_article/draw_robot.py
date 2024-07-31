# text and image size / positions
from generate_article import roundPosition, wrap_width, page_indent_horizontal

from wand.image import Image


size_robotLogo = 80

robot_start = roundPosition(page_indent_horizontal + size_robotLogo / 2)
robot_start_without_indent = robot_start


def draw_robot(image, pos_robotLogo):
    with Image(
        width=int(size_robotLogo * 1.46),
        height=size_robotLogo,
        filename="vrl_robot.png",
    ) as robot:
        # resize robot logo
        robot.resize(int(size_robotLogo * 1.46), size_robotLogo, blur=1)

        # overlay robot logo on background
        image.composite(robot, left=pos_robotLogo[0], top=pos_robotLogo[1])
