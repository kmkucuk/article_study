from collections import deque, namedtuple
from pathlib import Path


def getIndices(yourList, searchElements):
    yourIndices = []
    for i in range(0, len(yourList)):
        currentElement = yourList[i]
        for k in searchElements:
            # print(k)
            if k == currentElement:
                yourIndices.append(i)
                break

    return yourIndices


def roundPosition(pixelCoordinates):
    return int(round(pixelCoordinates))


def eval_metrics(txt, draw, image):
    """Quick helper function to calculate width/height of text."""
    metrics = draw.get_font_metrics(image, txt, True)
    return (metrics.text_width, metrics.text_height)


p = Path(".")
files = deque([x for x in p.iterdir()])
current_path = Path(".")

print(files)

articles = []

while files:
    _file = files.popleft()
    print('**********')
    print("_file: ", _file)

    if _file.is_dir():
        files.extend(_file.iterdir())
        print('skip if directory')
        # print("\n_file.isdir() correct : ", files.extend(_file.iterdir()))
        continue
    # print('**********')
    # print('_file.resolve().parent: ',str(_file.resolve().parent))

    if "output" in str(_file.resolve().parent):
        print('\nskip if output')
        continue
    # print('**********')
    # print('_file.name: ', _file.name)
    # print('_file.suffix: ', _file.suffix)

    if _file.name.startswith("article") and _file.suffix == ".xlsx":
        print('\narticle is added to list')
        articles.append(
            (
                _file.resolve(),
                Path.joinpath(_file.resolve().parent, "fonts_and_kerning.xlsx"),
            )
        )

    # if path.isfile(_file):
    #     if _file.startswith("article") and _file.endswith(".xlsx"):
    #         articles.push(_file)

    # if path.isdir(_file):
    #     files.extend(os.listdir(_file))


print(f"found {len(articles)} article sheets")


ArticleInfo = namedtuple(
    "ArticleInfo",
    [
        "article_sheet",
        "font_sheet",
        "passage_name",
        "headerIndices",
        "textIndices",
        "dateIndex",
        "photoIndex",
        "captionIndex",
        "authorIndex",
    ],
)

# Create a black canvas img_widthximg_height pixels (1024x768)
img_width = 1024
img_height = 1500

img_center_x = roundPosition(img_width / 2)
img_center_y = roundPosition(img_height / 2)

# left - right indent of text (%2.5 for each side)
page_indent_horizontal = roundPosition(img_width / 40)

# length of text wrapping
wrap_width = roundPosition(img_width - page_indent_horizontal * 2)

# top-bottom limit of text (%2.5 for each side)
page_indent_vertical = roundPosition(img_height / 40)

# top - bottom indent
wrap_height = roundPosition(img_height - page_indent_vertical * 2)
