from app.forms import CriteriaPageNumberForm
from app.models import RatingCriteria, CriteriaPageNumber


def get_form_class(criteria):
    if criteria == RatingCriteria.PAGE_NUMBER:
        return CriteriaPageNumberForm
    return None

def get_criteria_model(criteria):
    if criteria == RatingCriteria.PAGE_NUMBER:
        return CriteriaPageNumber
    return None
