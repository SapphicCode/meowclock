import mastodon
import datetime
import time
import random
import os.path


APP_FILE = '.app_secrets'
SECRETS_FILE = '.oauth_secret'


def current_hour() -> int:
    """Helper function to return the current 12-hour hour."""
    return (datetime.datetime.utcnow().hour % 12) or 12  # 0 is falsey, exploiting


def create_client(username: str, password: str, domain: str = 'botsin.space') -> mastodon.Mastodon:
    api = 'https://{}'.format(domain)

    # app creation
    if not os.path.exists(APP_FILE):
        mastodon.Mastodon.create_app('Big Meow', to_file=APP_FILE, api_base_url=api)

    # login
    secrets = None
    if os.path.exists(SECRETS_FILE):
        secrets = SECRETS_FILE
    client = mastodon.Mastodon(api_base_url=api, client_id=APP_FILE, access_token=secrets)
    if secrets is None:
        client.log_in(username, password, to_file=SECRETS_FILE)

    return client


def send_meows(c: mastodon.Mastodon, amount):
    word = 'meow'
    if random.randint(0, 50) == 50:
        word = 'nya'
    c.status_post(status=' '.join(word for _ in range(amount)))


def run(username, password, domain):
    """This is a print-happy function. Don't use this when integrating this bot into other programs."""
    c = create_client(username, password, domain)
    _last_seen_hour = -1
    print('Client created successfully.')
    while True:
        now = current_hour()
        if _last_seen_hour != now:
            try:
                send_meows(c, now)
                _last_seen_hour = now  # ensures we don't set if we failed to post, ensuring a retry
                print('Post sent.')
            except Exception as e:
                print('Exception {} raised while attempting to send post.'.format(e))
        print('Sleeping...')
        time.sleep(60)
