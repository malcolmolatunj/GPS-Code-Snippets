class User:
    def __init__(self, sub=None, active=True):
        self.sub = sub
        self.active = True

    def __str__(self):
        return self.name


def is_valid_sub(user, desired_substitute, substitution_chain=None):
    if not desired_substitute.active:
        return False
    if not desired_substitute.sub:
        return True

    if not substitution_chain:
        substitution_chain = {user}
    substitution_chain.add(desired_substitute)

    if desired_substitute.sub in substitution_chain:
        return False
    return is_valid_sub(desired_substitute, desired_substitute.sub, substitution_chain)
