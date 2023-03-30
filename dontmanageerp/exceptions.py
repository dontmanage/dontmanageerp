import dontmanage


# accounts
class PartyFrozen(dontmanage.ValidationError):
	pass


class InvalidAccountCurrency(dontmanage.ValidationError):
	pass


class InvalidCurrency(dontmanage.ValidationError):
	pass


class PartyDisabled(dontmanage.ValidationError):
	pass


class InvalidAccountDimensionError(dontmanage.ValidationError):
	pass


class MandatoryAccountDimensionError(dontmanage.ValidationError):
	pass
