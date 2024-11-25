# from preferences. models import Preference
# from user_profile.models import Profile


def calculate_matching_score(user1,user2):
    score=0
    max_score = 9
    # profile1 = user1.profile
    preference1 = user1.preference
    profile2 = user2.profile

    if preference1.gender == profile2.gender:
        score += 1
    if preference1.min_age <= profile2.age <= preference1.max_age:
        score += 1
    if preference1.min_height <= profile2.height <= preference1.max_height:
        score += 1
    if preference1.min_weight <= profile2.weight <= preference1.max_weight:
        score += 1
    if preference1.language == profile2.languages:
        score += 1
    if preference1.location == profile2.location:
        score += 1
    if preference1.education == profile2.education:
        score += 1
    if preference1.religion == profile2.religion:
        score += 1
    if preference1.caste == profile2.caste:
        score += 1
    if score >0:
        percentage = (score/max_score)*100
        return percentage
    

