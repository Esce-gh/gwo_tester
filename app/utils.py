from app.forms import CriteriaPageNumberForm
from app.models import RatingCriteria, CriteriaPageNumber


def get_form_class(criteria):
    match criteria:
        case RatingCriteria.PAGE_NUMBER:
            return CriteriaPageNumberForm
        case _:
            return None


def get_criteria_model(criteria):
    match criteria:
        case RatingCriteria.PAGE_NUMBER:
            return CriteriaPageNumber
        case _:
            return None
