import utils


def test_single_number_parse_asnwer():
    result = utils.parse_answer("[4], <답변>")
    assert result == ([4], "답변")


def test_multi_number_parse_asnwer():
    result = utils.parse_answer("[1, 4], <답변>")
    assert result == ([1, 4], "답변")


def test_multi_number_no_blank_parse_answer():
    result = utils.parse_answer("[1,4], <답변>")
    assert result == ([1, 4], "답변")


def test_invalid_answer_parse_answer():
    result = utils.parse_answer("[1, 4], ")
    assert result == None


def test_invalid_number_answer_parse_answer():
    result = utils.parse_answer("[1, , <답변>")
    assert result == None
