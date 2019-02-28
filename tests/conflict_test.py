import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 

from plotter.core import *
import unittest, pytest
#from unittest import TestCase.assertEqual as assertEqual
"""
class Conflict_tests(unittest.TestCase):

    @pytest.fixture(scope='module')
    def setup(self):
        self.myconflict1 = Conflict(soup, "628", [],{}, {})
        self.myconflict2 = Conflict(soup, "628", [],{"B":"B-3"}, {})
        return self.myconflict1
        
    def test_get_conflict_by_id(self, self.setup):
        self.assertEqual(self.setup.plain_text, 'A, in need of money to finance an enterprise, holds up a stage. A, robbing a stage, discovers that B, who knows and recognizes him, is one of the passengers.')
        
    #def test_initiating_a_conflict_with_transpositions_self_masks_them(self,setup):
    #    self.assertEqual(self.myconflict2.plain_text, 'A, in need of money to finance an enterprise, holds up a stage. A, robbing a stage, discovers that #B-3, who knows and recognizes him, is one of the passengers.')

"""

@pytest.fixture(scope='module')
def root_conflict_vanilla():
    conflict = Conflict(soup, "628")#, [],{}, {})
    return conflict

@pytest.mark.basic
def test_get_conflict_by_id(root_conflict_vanilla):
    assert root_conflict_vanilla.plain_text == 'A, in need of money to finance an enterprise, holds up a stage. A, robbing a stage, discovers that B, who knows and recognizes him, is one of the passengers.'

@pytest.mark.dev    
def test_choose_carry_on_conflict(root_conflict_vanilla):
    for i in range(5):
        assert root_conflict_vanilla.generate_next("-", 1).__next__().plain_text == 'A is a fugitive from justice, who discovers that a relative, A-8, has died and left him a rich estate. A is a fugitive from justice who dares not show himself to receive a rich estate that has been left to him, for he knows he will be arrested.'

@pytest.mark.dev
def test_choose_carry_on_conflict__several_subconflicts_to_choose_from(root_conflict_vanilla):
    for i in range(5):
        assert root_conflict_vanilla.generate_next("-", 2).__next__().plain_text == 'A, driven to bay by pursuers, takes refuge in an old house. A is rescued from pursuers, A-6, A-6, when the old house in which he has taken refuge is blown away by a tornado.'

@pytest.mark.dev
def test_choose_lead_up_conflict(root_conflict_vanilla):
    for i in range(5):
        assert root_conflict_vanilla.generate_next("-", 0).__next__().plain_text == 'A, in love with B, is required by F-B, father of B, to secure a certain amount of money before he will be seriously considered as a son-in-law'

@pytest.mark.basic
def test_mask_untransposed_conflict(root_conflict_vanilla):
    root_conflict_vanilla.add_character("B","Joan")
    assert root_conflict_vanilla.plain_text == 'A, in need of money to finance an enterprise, holds up a stage. A, robbing a stage, discovers that Joan, who knows and recognizes him, is one of the passengers.'

@pytest.mark.basic
def test_fixture(root_conflict_vanilla):
    assert root_conflict_vanilla.characters == {'B': 'Joan'}
#    !!!!!!!!check if character is masked on lead up/ carry on !!!!!!!!!!

@pytest.mark.dev
def test_lead_up_masking(root_conflict_vanilla):
        assert root_conflict_vanilla.generate_next("-", 0).__next__().plain_text == 'A, in love with Joan, is required by F-B, father of Joan, to secure a certain amount of money before he will be seriously considered as a son-in-law'

@pytest.mark.basic
@pytest.fixture(scope='module')    
def root_conflict_transposed():
    conflict = Conflict(soup, "628", [],{"B":"B-3"}, {})
    return conflict
    

@pytest.mark.basic
def test_initiating_a_conflict_with_transpositions_self_masks_them(root_conflict_transposed):
    assert root_conflict_transposed.plain_text == 'A, in need of money to finance an enterprise, holds up a stage. A, robbing a stage, discovers that B-3, who knows and recognizes him, is one of the passengers.'

@pytest.mark.basic
def test_mask_transposed_away_character_in_conflict(root_conflict_transposed):
    root_conflict_transposed.add_character("B","Joan")
    assert root_conflict_transposed.plain_text == 'A, in need of money to finance an enterprise, holds up a stage. A, robbing a stage, discovers that B-3, who knows and recognizes him, is one of the passengers.'

    
@pytest.mark.basic
def test_mask_transposed_in_character_in_conflict(root_conflict_transposed):
    root_conflict_transposed.add_character("B-3","Jane")
    assert root_conflict_transposed.plain_text == 'A, in need of money to finance an enterprise, holds up a stage. A, robbing a stage, discovers that Jane, who knows and recognizes him, is one of the passengers.'
    

@pytest.mark.dev
def test_plain_text_transposition():
    conflict = Conflict(soup, "402", [],{}, {})
    assert conflict.generate_next("-", 0).__next__().plain_text == 'A and B, man and wife, meet with tragic misfortune but escape death. A and B, man and wife, escaping death in a tragic misfortune, each believes the other has perished.'

@pytest.fixture(scope='module')    
def conflict_with_additional_characters_on_links():
    conflict = Conflict(soup, "77", [],{}, {})
    return conflict

@pytest.mark.dev
def test_transposition_that_adds_a_character__simple(conflict_with_additional_characters_on_links):
    carryOnText = conflict_with_additional_characters_on_links.generate_next("+", 0).__next__().plain_text
    assert (carryOnText == 'A and A-3, in love with B, is required by F-B, father of B, to secure a certain amount of money before he will be seriously considered as a son-in-law.' or\
    carryOnText == 'A and A-3, in love with B, are required by F-B, father of B, to secure a certain amount of money before they will be seriously considered as sons-in-law.')


@pytest.mark.NLP
def test_transposition_that_adds_a_character_pronoun_adjustment(conflict_with_additional_characters_on_links):
    carryOnText = conflict_with_additional_characters_on_links.generate_next("+", 0).__next__().plain_text
    assert carryOnText == 'A and A-3, in love with B, are required by F-B, father of B, to secure a certain amount of money before they will be seriously considered as sons-in-law.'
    
    
 