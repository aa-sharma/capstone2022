import logging
from utils.config import config

logger = logging.getLogger('logger')


def dexterity_score(expected_angles, actual_angles):
    """
    Compare actual sensor data (angle) to the expected value
    Args: expected angles, actual angles
    Returns: Dexterity score based on closeness of position
    """
    score = 0
    angle_difference = average_angle_difference(expected_angles, actual_angles)
    if angle_difference <= 2:
        score = 10
    else:
        score = 10 - angle_difference * 10/85

    return score


def agility_score(time_taken):
    """
    Args: time taken by user to complete exercise
    Returns: agility score
    """
    score = 10 - time_taken * 10/config.AGILITY_DIFFICULTY
    if score < 0:
        score = 0
    return score


def average_angle_difference(expected_angles, actual_angles):
    """
    Args: expected angles, actual angles in the form of a list
    Returns: average of all the angles 
    """
    absolute_sum = 0
    for idx in range(len(expected_angles)):
        if idx <= 4:  # is index, middle, ring, pinky
            absolute_sum += abs(expected_angles[idx] - actual_angles[idx])
        else:  # is thumb, roll, pitch, yaw... decrease the weight
            absolute_sum += 0.3333 * abs(expected_angles[idx] - actual_angles[idx])

    average_of_angles = absolute_sum / 6

    return average_of_angles
