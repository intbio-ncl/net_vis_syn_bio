from restriction.abstract_restriction import ActionsRestriction
from annotation import recipes
from identifiers import identifiers

class P1Restriction(ActionsRestriction):
    def __init__(self):
        recipe = recipes.ActivationRecipe()
        super().__init__(recipe)

