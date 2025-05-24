from app.forms import CriteriaPageNumberForm, CriteriaHeaderFooterForm, CriteriaObjectDetectionForm, \
    CriteriaImageDetectionForm, CriteriaOCRForm, CriteriaObjectGroupsForm
from app.models import RatingCriteria, CriteriaPageNumber, CriteriaHeaderFooter, CriteriaObjectDetection, \
    CriteriaImageDetection, CriteriaOCR, CriteriaObjectGroups


def get_form_class(criteria):
    match criteria:
        case RatingCriteria.PAGE_NUMBER:
            return CriteriaPageNumberForm
        case RatingCriteria.HEADER_FOOTER:
            return CriteriaHeaderFooterForm
        case RatingCriteria.OBJECT_DETECTION:
            return CriteriaObjectDetectionForm
        case RatingCriteria.IMAGE_DETECTION:
            return CriteriaImageDetectionForm
        case RatingCriteria.OCR:
            return CriteriaOCRForm
        case RatingCriteria.OBJECT_GROUPS:
            return CriteriaObjectGroupsForm
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
        case RatingCriteria.IMAGE_DETECTION:
            return CriteriaImageDetection
        case RatingCriteria.OCR:
            return CriteriaOCR
        case RatingCriteria.OBJECT_GROUPS:
            return CriteriaObjectGroups
        case _:
            return None
