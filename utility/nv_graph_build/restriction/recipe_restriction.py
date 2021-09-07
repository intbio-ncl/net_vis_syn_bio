from restriction.abstract_restriction import RecipeRestriction
from annotation import recipes
from identifiers import identifiers

class ActivationRecipe(RecipeRestriction):
    def __init__(self):
        recipe = recipes.ActivationRecipe()
        super().__init__(recipe)

class RepressionRecipe(RecipeRestriction):
    def __init__(self):
        recipe = recipes.RepressionRecipe()
        super().__init__(recipe)

class GeneticProductionRecipe(RecipeRestriction):
    def __init__(self):
        recipe = recipes.GeneticProductionRecipe()
        super().__init__(recipe)