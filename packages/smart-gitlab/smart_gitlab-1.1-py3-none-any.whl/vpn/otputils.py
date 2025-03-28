import argparse
import os

import onetimepass as otp

vpn_mapping = {
    'luck': {'secret': 'MNPMSG4VRSSM4C2SUVN47FSYBA======', 'user': 'vpn_wxu', 'host': 'https://182.92.122.124',
             'cert': 'pin-sha256:R1NRH/8/SI7UGNZRzKEHxPLbZsOfFpqbi8NwdAGMP20='},
    'xyz': {'secret': 'ZDVCH5OX42X6SD3C6EX7J6T3YA======', 'user': 'vpn_wuzhuangyuan', 'host': 'https://13.214.103.45',
            'cert': 'pin-sha256:LY8gXKfM34ZpijckNbLk69lqd1kojZT6FO04q29eciI='}
    }


def get_otp(secret_key):
    my_token = otp.get_totp(secret=secret_key, interval_length=30)
    return my_token


def otp_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='vpn name [luck|xyz]')
    args = parser.parse_args()
    name = args.name
    secret = vpn_mapping.get(name).get('secret')
    print(get_otp(secret))


def vpn_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='vpn name [luck|xyz]')
    args = parser.parse_args()
    name = args.name
    secret = vpn_mapping.get(name).get('secret')
    user = vpn_mapping.get(name).get('user')
    host = vpn_mapping.get(name).get('host')
    cert = vpn_mapping.get(name).get('cert')
    otp = get_otp(secret)
    os.system(
        f'(echo "nopass123"; sleep 1; echo "{otp}") | sudo openconnect --user={user} --no-dtls --passwd-on-stdin --servercert {cert} {host}')
