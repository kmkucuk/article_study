from generate_article import (
    roundPosition,
    eval_metrics,
    word_wrap,
    wrap_height,
    wrap_width,
)

from generate_article.draw_robot import indent_from_robot
from generate_article.word_wrap import word_wrap

###########################
# !TEXT SIZE MULTIPLIERS! #
###########################
# These ensure that we use the same font sizes (in pix)
# as we did it in PsychoPy's text components in previous
# interlude of 3-experiments (Rashid's) study (kurtulusmertkucuk@gmail.com, date: 18/05/2023).
passageSizeMultiplier = 1.2
textSizeInPixels = 16


def find_next_bracket(word_array, start):
    """Find the next bracket in the word array."""
    for i in range(start, len(word_array)):
        if "]" in word_array[i]:
            return i
    raise RuntimeError("Unable to find next bracket")


def draw_text(image, draw, article_info, text_position, has_links) -> list:
    textIndices = article_info.textIndices
    article_sheet = article_info.article_sheet

    link_bounds = []
    howManyParagraphs = len(textIndices)
    parit = 0
    for text_index in textIndices:
        parit = parit + 1
        text = article_sheet["content"][text_index].strip()
        split_text = text.split(" ")
        num_words = len(split_text)

        evaluating_bracket = False

        for texti in range(0, num_words):
            currentWord = split_text[texti].strip()

            if "[" in currentWord:
                evaluating_bracket = True
                currentWord = currentWord.replace("[", "")

                # if the bracket is empty, skip it
                if len(currentWord.strip()) == 0:
                    continue

            if evaluating_bracket:
                current_color = "blue"
                if "]" in currentWord:
                    currentWord = currentWord.replace("]", "")
                    evaluating_bracket = False
                    # if the bracket is empty, skip it
                    if len(currentWord.strip()) == 0:
                        continue
            else:
                current_color = "black"

            if texti < num_words - 1:
                currentWord += " "

            if not has_links:
                current_color = "black"

                # adjust the font size
            current_font_size = textSizeInPixels * passageSizeMultiplier

            # assign font size
            draw.font_size = current_font_size
            # text color
            draw.fill_color = current_color
            # align text to left
            draw.text_alignment = "left"

            word_width, word_height = eval_metrics(currentWord, draw, image)

            # add new line if wrap width is exceeded
            # Multiple text width to add extra padding
            paragraph_right_padding = 1.07

            if text_position[0] * paragraph_right_padding >= wrap_width:
                text_position[0] = roundPosition(indent_from_robot)

                text_position[1] += roundPosition(word_height)

            partext = str(((parit / howManyParagraphs) * 100) // 1)
            wordtext = str((((texti + 1) / num_words) * 100) // 1)
            print(
                "Progress: paragraphs: %" + partext + "\t words: %" + wordtext + "\t",
                end="\r",
            )

            draw.text(
                roundPosition(text_position[0]),
                roundPosition(text_position[1]),
                currentWord,
            )

            if current_color == "blue":
                link_bounds.append(
                    [
                        currentWord,
                        text_position[0],  # type: ignore
                        text_position[1],
                        word_width,
                        word_height,
                    ]
                )

            text_position[0] = roundPosition(word_width + text_position[0])

            if texti == num_words - 1:
                text_position[0] = roundPosition(indent_from_robot)
                text_position[1] += word_height * 2

    return link_bounds
