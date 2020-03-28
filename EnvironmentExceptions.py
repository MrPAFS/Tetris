""" Possui as possíveis exceções de um ambiente"""

"""
    É chamada toda vez que tenta-se executar uma ação que não esta no escopo de ações possíveis de um determinado ambiente
"""
class InvalidAction(Exception):

    def __init__(self, expression, valid_actions):
        self.expression = expression
        self.message = "Use only one of these actions: " + str(valid_actions)
