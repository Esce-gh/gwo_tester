from app.forms import CriteriaPageNumberForm, CriteriaHeaderFooterForm, CriteriaObjectDetectionForm
from app.models import RatingCriteria, CriteriaPageNumber, CriteriaHeaderFooter, CriteriaObjectDetection


def get_form_class(criteria):
    match criteria:
        case RatingCriteria.PAGE_NUMBER:
            return CriteriaPageNumberForm
        case RatingCriteria.HEADER_FOOTER:
            return CriteriaHeaderFooterForm
        case RatingCriteria.OBJECT_DETECTION:
            return CriteriaObjectDetectionForm
        case _:
            return None


def get_criteria_model(criteria):
    match criteria:
        case RatingCriteria.PAGE_NUMBER:
            return CriteriaPageNumber
        case RatingCriteria.HEADER_FOOTER:
            return CriteriaHeaderFooter
        case RatingCriteria.OBJECT_DETECTION:
            return CriteriaObjectDetection
        case _:
            return None
