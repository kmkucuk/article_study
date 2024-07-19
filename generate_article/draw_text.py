from generate_article import (
    roundPosition,
    eval_metrics,
    wrap_width,
    page_indent_horizontal,
)

from generate_article.draw_robot import indent_from_robot, robot_start_without_indent

###########################
# !TEXT SIZE MULTIPLIERS! #
###########################
# These ensure that we use the same font sizes (in pix)
# as we did it in PsychoPy's text components in previous
# interlude of 3-experiments (Rashid's) study (kurtulusmertkucuk@gmail.com, date: 18/05/2023).
textSizeInPixels = 20


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

        spaceLength, _ = eval_metrics(" ", draw, image)
        evaluating_bracket = False
        current_link_bounds = []
        underlined_words = []

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

                # add this word to the underlined word list
                underlined_words.append(currentWord)
            else:
                current_color = "black"

            if texti < num_words - 1:
                currentWord += " "

            if not has_links:
                current_color = "black"

            # adjust the font size
            # current_font_size = textSizeInPixels * passageSizeMultiplier

            # assign font size
            draw.font_size = textSizeInPixels
            # text color
            draw.fill_color = current_color
            # align text to left
            draw.text_alignment = "left"

            word_width, word_height = eval_metrics(currentWord, draw, image)

            # add new line if wrap width is exceeded
            # Multiple text width to add extra padding
            if text_position[0] + word_width >= wrap_width + page_indent_horizontal:
                text_position[0] = roundPosition(page_indent_horizontal)

                text_position[1] += roundPosition(word_height * 1.25)

                if (
                    current_color == "blue" and len(current_link_bounds) > 0
                ):  # Can be skipped if list is empty as we will handle later
                    current_link_bounds[3].append(word_width)

                    current_link_bounds[1].append(text_position[0])
                    current_link_bounds[2].append(text_position[1])

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
                if evaluating_bracket:
                    # initialize underlined word text metrics for the first word after [
                    if len(current_link_bounds) < 1:
                        current_link_bounds = [
                            "",
                            [text_position[0]],
                            [text_position[1]],
                            [word_width],
                            word_height,
                        ]
                    else:
                        # sum the words and the word widths for multiple underlined words
                        current_link_bounds[3][-1] = (
                            current_link_bounds[3][-1] + word_width + spaceLength
                        )

                else:
                    # initialize underlined word text metrics for the first word after [
                    # Can happen when there is a single underlined word
                    if len(current_link_bounds) < 1:
                        current_link_bounds = [
                            currentWord,
                            [text_position[0]],
                            [text_position[1]],
                            [word_width],
                            word_height,
                        ]
                    else:
                        # sum the words and the word widths for multiple underlined words
                        current_link_bounds[0] = " ".join(underlined_words)
                        current_link_bounds[3][-1] = (
                            current_link_bounds[3][-1] + word_width + spaceLength
                        )

                    # register  underlined word metrics when algorithm reaches to ] symbol.
                    link_bounds.append(current_link_bounds)
                    current_link_bounds = []
                    underlined_words = []

            text_position[0] = roundPosition(word_width + text_position[0])

            if texti == num_words - 1:
                text_position[0] = roundPosition(robot_start_without_indent)
                text_position[1] += word_height * 1.8

    return link_bounds
