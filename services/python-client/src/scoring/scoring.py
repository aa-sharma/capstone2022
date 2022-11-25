def get_expected():
    """
    For the selected exercise, retrieve the expected values from DB
    """
    pass

def dexterity_score(expected, actual):
    """
    Compare actual sensor data (angle) to the expected value
    Args: expected angle, actual angle
    Returns: Dexterity score based on closeness of position
    """
    score = 10
    for x in range(8):
        if x < 4:
            score = score - abs(expected[x] - actual[x])
        else :
            # thumb, yaw, pitch, roll (elements [7], [6], [5], [4] amount to 1
            score = score - abs(0,25*expected[x] - 0.25*actual[x])
    
    normalized_score = (score/8) * (10/88)
    return(normalized_score)

def agility_score(time_taken):
    """
    Args: time taken by user to complete exercise
    Returns: agility score
    """
    agility = 10 - (10/500 * time_taken)
    return(agility)
