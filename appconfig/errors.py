class CannotExceeds100(ValueError):
    pass


class SubtypePoints(CannotExceeds100):
    def __init__(self, domain):
        raise ValueError(f"Summary of subtype points cannot be exceed 100 for {domain} domain")


class DomainPoints(CannotExceeds100):
    raise ValueError("Summary of domain points cannot be exceed 100")