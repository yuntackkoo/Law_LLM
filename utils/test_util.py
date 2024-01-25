import util


def test_single_number_parse_asnwer():
    question = "[4], <답변>"
    result = util.parse_answer(question)
    assert result == ([4], "답변")


def test_multi_number_parse_asnwer():
    question = "[1, 4], <답변>"
    result = util.parse_answer(question)
    assert result == ([1, 4], "답변")


def test_multi_number_no_blank_parse_answer():
    question = "[1,4], <답변>"
    result = util.parse_answer(question)
    assert result == ([1, 4], "답변")


def test_invalid_answer_parse_answer():
    question = "[1, 4], "
    result = util.parse_answer(question)
    assert result == ([0], question)


def test_invalid_number_answer_parse_answer():
    question = "[1, , <답변>"
    result = util.parse_answer(question)
    assert result == ([0], question)
