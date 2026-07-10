from app.services.rule_classifier import classify_by_rules



def classify_page(page):


    result = classify_by_rules(page)



    if result:

        return result



    # Future

    # result = classify_by_ai(page)



    # Future

    # result = request_human_review(page)



    return {


        "document_type":"UNKNOWN",


        "confidence":0.0,


        "source":"NONE"

    }