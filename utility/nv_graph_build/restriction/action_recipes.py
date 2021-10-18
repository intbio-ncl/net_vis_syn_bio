from restriction.abstract_restriction import RecipeRestriction
from annotation import action_recipes as ar
import entities.action

class ActionRecipe(RecipeRestriction):
    def __init__(self,recipe):
        i_range = [entities.action.Action]
        super().__init__(recipe,i_range)
        
class TransferRecipe(ActionRecipe):
    def __init__(self):
        recipe = ar.TransferRecipe()
        super().__init__(recipe)

