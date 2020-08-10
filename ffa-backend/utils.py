from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import TrainingStatusType
from msrest.authentication import CognitiveServicesCredentials
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import io


def set_environ_variables():
    env_file = '.env'
    with open(env_file) as envfile:
        for line in envfile:
            data = line.split('=')
            os.environ[data[0].strip()] = data[1].strip()

set_environ_variables()

face_api_key = os.environ.get('AZURE_API_KEY', None)
assert face_api_key
face_api_endpoint = os.environ.get('AZURE_ENDPOINT', None)
assert face_api_endpoint


credentials = CognitiveServicesCredentials(face_api_key)
face_client = FaceClient(face_api_endpoint, credentials=credentials)


def get_training_status():
    while (True):
        training_status = face_client.person_group.get_training_status(person_group_id)
        print("Training status: {}.".format(training_status.status))
        print()
        if (training_status.status is TrainingStatusType.succeeded):
            break
        elif (training_status.status is TrainingStatusType.failed):
            sys.exit('Training the person group has failed.')
        time.sleep(5)


def register_face(images, person_group_id, person_id):
    try:
        # Check for our group
        face_client.person_group.get(person_group_id)
    except:
        # Create the group
        face_client.person_group.create(person_group_id=person_group_id, name=person_group_id)
        print(f'New Face Group {person_group_id} Created!')
    person = face_client.person_group_person.create(person_group_id, person_id)
    print(person.person_id)
    face_count = 0
    for index, image in enumerate(images):
        image = io.BytesIO(image)
        print(f'Frame {index + 1}')
        try:
            face_client.person_group_person.add_face_from_stream(person_group_id, person.person_id, image)
            face_count += 1
        except Exception as e:
            print(e)
            continue
    print(f'Registered {face_count} faces for {person_id}')
    print('New person added:', person_id)
    print('Starting Training.')
    face_client.person_group.train(person_group_id)
    return person.person_id


def send_email(user_email, username):
    url = f'http://localhost:5000/register?username={username}&email={user_email}'
    message = Mail(
        from_email='auth0demo.teamfeu@gmail.com',
        to_emails=user_email,
        subject='Set-up Face Authentication',
        html_content=f'Hi {username}!<br>Register your FFA with us at {url}'
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)




def find_person(image, person_group_id):
    image = io.BytesIO(image)
    faces = face_client.face.detect_with_stream(image)
    face_ids = [face.face_id for face in faces]
    results = face_client.face.identify(face_ids, person_group_id)
    if not results:
        return None
    else:
        for result in results:
            # Find the top candidate for each face
            candidates = sorted(result.candidates, key=lambda c: c.confidence, reverse=True)
            # Was anyone recognized?
            if len(candidates) > 0:
                # Get just the top candidate
                top_candidate = candidates[0]
                # See who the person is
                person = face_client.person_group_person.get(person_group_id, top_candidate.person_id)
                return str(person.name)
            return None

#face_client.person_group.create(person_group_id=person_group_id, name=person_group_id)