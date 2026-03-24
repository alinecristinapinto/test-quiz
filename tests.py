import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct
    
# Novos testes:

def test_create_question_with_empty_title():
    with pytest.raises(Exception):
        Question(title='', points=1)

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_create_choice_with_empty_text_raises_exception():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.add_choice('')

def test_create_choice_with_text_longer_than_100_characters_raises_exception():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.add_choice('a' * 101)
        
def test_remove_choice_by_invalid_id_raises_exception():
    question = Question(title='q1')
    question.add_choice('a')

    with pytest.raises(Exception):
        question.remove_choice_by_id(999)

def test_remove_all_choices_clears_question_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    question.remove_all_choices()

    assert question.choices == []
        
def test_set_correct_choices_marks_specified_choices_as_correct():
    question = Question(title='q1')
    first = question.add_choice('a')
    question.add_choice('b')
    third = question.add_choice('c')

    question.set_correct_choices([first.id, third.id])

    assert question.choices[0].is_correct is True
    assert question.choices[1].is_correct is False
    assert question.choices[2].is_correct is True


def test_set_correct_choices_with_invalid_id_raises_exception():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    with pytest.raises(Exception):
        question.set_correct_choices([1, 999])
        
def test_correct_selected_choices_returns_only_selected_correct_choice_ids():
    question = Question(title='q1', max_selections=2)
    first = question.add_choice('a', is_correct=True)
    second = question.add_choice('b', is_correct=False)
    question.add_choice('c', is_correct=True)

    corrected = question.correct_selected_choices([first.id, second.id])

    assert corrected == [first.id]

def test_correct_selected_choices_raises_when_selection_exceeds_max_raises_exception():
    question = Question(title='q1', max_selections=1)
    first = question.add_choice('a', False)
    second = question.add_choice('b', True)

    with pytest.raises(Exception):
        question.correct_selected_choices([first.id, second.id])
        