from django.db.models import Choices


class StrikeChoices(Choices):
    LEVEL1 = 'Level 1'
    LEVEL2 = 'Level 2'
    LEVEL3 = 'Level 3'


class StrikeReasonsChoices(Choices):
    RACISM = 'Racism'
    SEXISM = 'Sexism'
    BULLYING = 'Bullying'
