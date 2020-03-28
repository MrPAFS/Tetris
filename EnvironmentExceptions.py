""" Possui as possíveis exceções de um ambiente"""

"""
    É chamada toda vez que tenta-se executar uma ação que não esta no escopo de ações possíveis de um determinado ambiente
"""
class InvalidAction(Exception):
    pass
    def __init__(self, invalid_action, valid_actions):
        self.message = "{} is invalid, instead of this use only one of these actions: {}".format(invalid_action, valid_actions)

    def __str__(self):
        return self.message
