import socketio
import logging
import time
import json
import requests
from utils.config import config
from data_collection import data_collection
from process_coordinates import process_coordinates
from scoring import scoring

sio = socketio.Client()
logger = logging.getLogger('logger')


@sio.on("user_stop_exercise")
def stop_exercise(data):
    logger.info(data)
    sio.init_start_exercise = False
    sio.start_exercise = False


@sio.on("user_start_exercise")
def start_exercise(exercise):
    logger.info(f'User requested to start exercise:\n{json.dumps(exercise, indent=4)}')

    angles_list_starting = data_collection.parse_expected_position_into_array(exercise['position'][0])
    angles_list_finish = data_collection.parse_expected_position_into_array(exercise['position'][1])
    sio.init_start_exercise = True
    sio.start_exercise = True
    average_angle_difference = 90

    while sio.init_start_exercise and average_angle_difference > 2:
        actual_angles_list = data_collection.read_serial()  # read values from arduino, outputs angles list

        average_angle_difference = scoring.average_angle_difference(angles_list_starting, actual_angles_list)
        raw_xyz = process_coordinates.generate_xyz(actual_angles_list)  # computes xyz coordinates in unwanted form
        # repackages xyz coordinates in form expected by webclient
        processed_xyz = data_collection.repackage_cartesian(raw_xyz)
        sio.emit('receive_actual_position', processed_xyz)  # emits event with xyz coordinates for each point
        time.sleep(0.1)

    if not sio.init_start_exercise:
        return

    sio.emit("data_processor_start_exercise")
    time.sleep(3)

    start_time = time.time()
    average_angle_difference = 90
    best_dexterity_score = 0
    while sio.start_exercise and average_angle_difference > 2:
        actual_angles_list = data_collection.read_serial()  # read values from arduino, outputs angles list

        average_angle_difference = scoring.average_angle_difference(angles_list_finish, actual_angles_list)
        dexterity_score = scoring.dexterity_score(angles_list_finish, actual_angles_list)
        best_dexterity_score = dexterity_score if dexterity_score > best_dexterity_score else best_dexterity_score

        raw_xyz = process_coordinates.generate_xyz(actual_angles_list)  # computes xyz coordinates in unwanted form
        # repackages xyz coordinates in form expected by webclient
        processed_xyz = data_collection.repackage_cartesian(raw_xyz)
        sio.emit('receive_actual_position', processed_xyz)  # emits event with xyz coordinates for each point
        time.sleep(0.1)

    time_taken = time.time() - start_time
    agility_score = scoring.agility_score(time_taken)

    headers = {'x-auth-token': sio.token_data.json()['token']}
    user_level_progress = {"exercise": exercise, "agilityScore": agility_score, "dexterityScore": best_dexterity_score}

    r = requests.post(f'{config.BASE_SERVER_URL}/api/user-level-progress', json=user_level_progress, headers=headers)
    if r.status_code != 200:
        error = f"There was an error creating user_level_progress report {r.json()}"
        logger.error(error)
        sio.emit("exercise_completed", {"error": error})
        exit(0)

    sio.emit("exercise_completed", {"dexterityScore": r.json()['dexterityScore'], "agilityScore": r.json()[
             'agilityScore'], "overallScore": r.json()['overallScore']})


@sio.on("fetch_expected_position")
def fetch_expected_position(exercise):
    angles_list_starting = data_collection.parse_expected_position_into_array(exercise['position'][0])
    angles_list_finish = data_collection.parse_expected_position_into_array(exercise['position'][1])

    raw_xyz_starting = process_coordinates.generate_xyz(angles_list_starting)
    processed_xyz_starting = data_collection.repackage_cartesian(raw_xyz_starting)
    raw_xyz_finish = process_coordinates.generate_xyz(angles_list_finish)
    processed_xyz_finish = data_collection.repackage_cartesian(raw_xyz_finish)
    sio.emit('receive_expected_position', [processed_xyz_starting, processed_xyz_finish])


@sio.event
def connect():
    logger.info(f"Successfully connected websocket server: {config.BASE_SERVER_URL}")


@sio.on('connect_error')
def connect_error(data):
    logger.warning(f"Websocket connection to {config.BASE_SERVER_URL} failed, with reason: {data}")


@sio.event
def disconnect():
    logger.info(f"Disconnected from websocket server: {config.BASE_SERVER_URL}")
