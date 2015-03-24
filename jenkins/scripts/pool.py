import argparse
import os
import random

from novaclient import client as novaclient
from novaclient.exceptions import NotFound


class EmptyServerPool(Exception):
    pass


def get_client():
    return novaclient.Client(
        3,
        username=os.getenv('OS_USERNAME'),
        api_key=os.getenv('OS_PASSWORD'),
        project_id=os.getenv('OS_TENANT_NAME'),
        auth_url=os.getenv('OS_AUTH_URL')
    )


def get_public_v4_address(client, server):
    try:
        return client.floating_ips.find(instance_id=server.id).ip
    except NotFound:
        pass


def get_server_for_v4_address(client, ip):
    try:
        instance_id = client.floating_ips.find(ip=ip).instance_id
        return client.servers.get(instance_id)
    except NotFound:
        pass


def free(ip):
    client = get_client()
    server = get_server_for_v4_address(client, ip)
    server.rebuild(server.image['id'])
    client.servers.delete_meta(server, ['in-use'])


def get_server_address():
    client = get_client()
    servers = filter(
        lambda x: x.name.startswith('ci-peon-'),
        client.servers.list()
    )
    random.shuffle(servers)
    for server in servers:
        if server.status != 'ACTIVE':
            continue
        if 'in-use' in server.metadata:
            continue
        addr = get_public_v4_address(client, server)
        if addr:
            client.servers.set_meta_item(
                server,
                'in-use',
                '1'
            )
            return addr
    raise EmptyServerPool()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser(
        'reserve', help='reserve a server from the pool'
    ).add_argument('outfile')

    subparsers.add_parser(
        'free', help='free a server back into the pool'
    ).add_argument('ip_address')
    ns = parser.parse_args()

    if ns.command == 'reserve':
        address = get_server_address()
        with open(ns.outfile, 'w') as f:
            f.write('\n'.join([
                '[all]',
                '%s ansible_ssh_user=dhc-user' % address
            ]))
            print address
    elif ns.command == 'free':
        free(ns.ip_address)
