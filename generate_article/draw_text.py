from generate_article import (
    article_sheet,
    textIndices,
    roundPosition,
    eval_metrics,
    word_wrap,
    wrap_height,
    wrap_width,
)

import time 
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


def draw_text(image, draw, text_position, has_links) -> list:
    link_bounds = []
    howManyParagraphs = len(textIndices)
    parit = 0
    for text_index in textIndices:
        parit = parit+1
        text = article_sheet["content"][text_index].strip()
        split_text = text.split(" ")
        num_words = len(split_text)

        parapgrah = ""
        previousWords = []
        line_width = []

        closing_bracket = -1
        buffer = []
        # print("completed paragraphs %"+str(round((parit/howManyParagraphs)*100)), end="\r", flush=True)
        for texti in range(0, num_words):
            if texti < closing_bracket:
                buffer.append(split_text[texti].strip())
                continue
                # current word
                # add space to end of words

            if texti == closing_bracket:
                buffer.append(split_text[texti].strip())
                currentWord = " ".join(buffer).replace("[", "").replace("]", "").strip()
                buffer.clear()
                closing_bracket = -1
                current_color = "blue"
            else:
                current_color = "black"
                currentWord: str = split_text[texti]

            if texti < num_words - 1:
                currentWord += " "

            if "[" in currentWord:
                buffer.append(currentWord.strip())
                closing_bracket = find_next_bracket(split_text, texti)
                continue

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

            # add this word's width to the line's width
            line_width.append(word_width)

            # add new line if wrap width is exceeded
            # Multiple text width to add extra padding
            if text_position[0] * 1.05 >= wrap_width:
                line_width = []
                line_width.append(word_width)
                text_position[0] = roundPosition(indent_from_robot)

                text_position[1] += roundPosition(word_height)

                # append the current word to incomplete passage
            previousWords.append(currentWord)

            # apply wrapping to incomplete passage to get Y axis of next word printing
            joinedWords = "".join(previousWords)
            parapgrah = word_wrap(image, draw, joinedWords, wrap_width, wrap_height)

            partext  = str(round((parit/howManyParagraphs)*100))
            wordtext = str(round(((texti+1)/len(range(0, num_words)))*100))
            print("Progress: paragraphs: %"+ partext+"\t words: %"+wordtext+"\t", end="\r")

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
                previousWords = []
                text_position[0] = roundPosition(indent_from_robot)
                text_position[1] += word_height * 2
    return link_bounds
    
