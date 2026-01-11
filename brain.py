def is_eligible(user, scheme):
    if user["income"] > scheme["max_income"]:
        return False

    if user["category"] not in scheme["category"]:
        return False

    if scheme.get("student") and not user["student"]:
        return False

    if "gender" in scheme and scheme["gender"] != user["gender"]:
        return False

    return True