from textwrap import wrap


def eval_metrics(draw, image, txt):
    """Quick helper function to calculate width/height of text."""
    metrics = draw.get_font_metrics(image, txt, True)
    return (metrics.text_width, metrics.text_height)


def shrink_text(draw):
    """Reduce point-size & restore original text"""
    draw.font_size = draw.font_size - 0.75
    return draw


def word_wrap(image, draw, text, roi_width, roi_height):
    """Break long text to multiple lines, and reduce point size
    until all text fits within a bounding box."""
    mutable_message = text
    iteration_attempts = 100

    while draw.font_size > 0 and iteration_attempts:
        iteration_attempts -= 1
        width, height = eval_metrics(draw, image, mutable_message)
        if height > roi_height:
            raise RuntimeError("Text height is higher than image's pixels")
            # do not shrink text if it doesn't fit vertically
            # shrink_text()
        if width > roi_width:
            columns = len(mutable_message)
            while columns > 0:
                columns -= 1
                mutable_message = "\n".join(wrap(mutable_message, columns))
                wrapped_width, _ = eval_metrics(draw, image, mutable_message)
                if wrapped_width <= roi_width:
                    break
            if columns < 1:
                print('***********text shrinked***********')
                mutable_message = text
                draw = shrink_text(draw)
        else:
            break
    if iteration_attempts < 1:
        raise RuntimeError("Unable to calculate word_wrap for " + text)
    return mutable_message
