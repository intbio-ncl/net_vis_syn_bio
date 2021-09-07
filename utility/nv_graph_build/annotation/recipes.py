from entities import reaction
from annotation.annotation import Annotation

class Recipe(Annotation):
    def __init__(self,recipe):
        super().__init__(recipe=recipe)
    
class ActivationRecipe(Recipe):
    def __init__(self):
        recipe = [reaction.NonCovalentBonding()]
        super().__init__(recipe)

class RepressionRecipe(Recipe):
    def __init__(self):
        recipe = [reaction.NonCovalentBonding()]
        super().__init__(recipe)

class GeneticProductionRecipe(Recipe):
    def __init__(self):
        recipe = [reaction.Transcription(),
                  reaction.Translation()]
        super().__init__(recipe)