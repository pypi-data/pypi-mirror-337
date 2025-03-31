#!/usr/bin/env python3
"""
powerdns-cli: Manage PowerDNS Zones/Records
"""

# pylint: disable=too-many-lines

import json
import sys
from typing import Literal

import click
import requests


# create click command group with 3 global options
@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.option(
    '-a',
    '--apikey',
    help='Provide your apikey manually',
    type=click.STRING,
    default=None,
    required=True
)
@click.option(
    '-u',
    '--url',
    help='DNS servers api url',
    type=click.STRING,
    required=True
)
@click.option(
    '-k',
    '--insecure',
    help='Ignore invalid certificates',
    is_flag=True,
    default=False,
    show_default=True,
)
@click.pass_context
def cli(ctx, apikey, url, insecure):
    """Manage PowerDNS Authoritative Nameservers and their Zones/Records

    Your target server api must be specified through the corresponding cli-flags.
    You can also export them with the prefix POWERDNS_CLI_, for example:
    export POWERDNS_CLI_APIKEY=foobar
    """
    ctx.ensure_object(dict)
    ctx.obj['apihost'] = url
    ctx.obj['key'] = apikey

    session = requests.session()
    session.verify = insecure
    session.headers = {'X-API-Key': ctx.obj['key']}
    ctx.obj['session'] = session


@cli.command()
@click.argument('ip', type=click.STRING)
@click.argument('nameserver', type=click.STRING)
@click.option('-a', '--account', type=click.STRING, help='Option')
@click.pass_context
def add_autoprimary(
    ctx,
    ip,
    nameserver,
    account,
):
    """
    Adds an autoprimary upstream dns server
    """
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/autoprimaries"
    payload = {
            'ip': ip,
            'nameserver': nameserver,
    }
    if account:
        payload['account'] = account

    r = _http_post(uri, ctx, payload)
    if _create_output(
            r,
            (201,),
            optional_json={'message': f'Autoprimary {ip} with nameserver {nameserver} added'}
    ):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.argument('zone', type=click.STRING)
@click.argument('keytype', type=click.Choice(['ksk', 'csk', 'zsk']))
@click.option('-a', '--active', is_flag=True, default=False,
              help='Sets the key to active immediately')
@click.option('-p', '--publish', is_flag=True, default=False,
              help='Set the key to not published')
@click.option(
    '-s',
    '--secret',
    default='',
    type=click.STRING,
    help='Manually set the dnssec private key'
)
@click.option('--bits', type=click.INT, help='Set the key size in bits, required for zsk')
@click.option('--algorithm',
              type=click.Choice([
                  'rsasha1',
                  'rsasha256',
                  'rsasha512',
                  'ecdsap256sha256',
                  'ed25519',
                  'ed448']
              ),
              help='Set the key size in bits, required for zsk')
@click.pass_context
def add_cryptokey(
    ctx,
    zone,
    keytype,
    active,
    publish,
    secret,
    bits,
    algorithm
):
    """
    Adds a cryptokey to your zone
    """
    zone = _make_canonical(zone)
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}/cryptokeys"
    payload = {
        'active': active,
        'published': publish,
        'keytype': keytype
    }
    for key, val in {
        'privatekey': secret.replace('\\n', '\n'),
        'bits': bits,
        'algorithm': algorithm
    }.items():
        if val:
            payload[key] = val
    r = _http_post(uri, ctx, payload)
    if _create_output(
            r,
            (201,),
    ):
        sys.exit(0)
    sys.exit(1)


# Add record
@cli.command()
@click.argument('name', type=click.STRING)
@click.argument('zone', type=click.STRING)
@click.argument(
    'record-type',
    type=click.Choice(
        [
            'A',
            'AAAA',
            'CNAME',
            'MX',
            'NS',
            'PTR',
            'SOA',
            'SRV',
            'TXT',
        ],
    ),
)
@click.argument('content', type=click.STRING)
@click.option('--ttl', default=3600, type=click.INT, help='Set default time to live')
@click.pass_context
def add_record(
    ctx,
    name,
    record_type,
    content,
    zone,
    ttl,
):
    """
    Adds a new DNS record of different types. Use @ if you want to enter a
    record for the top level.

    A record:
    powerdns-cli add_single_record test01 exmaple.org A 10.0.0.1
    MX record:
    powerdns-cli add_single_record mail example.org MX "10 10.0.0.1"
    CNAME record:
    powerdns-cli add_single_record test02 example.org CNAME test01.example.org
    """
    zone = _make_canonical(zone)
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}"
    name = _make_dnsname(name, zone)
    rrset = {
        'name': name,
        'type': record_type,
        'ttl': ttl,
        'changetype': 'REPLACE',
        'records': [
            {
                'content': content,
                'disabled': False
            }
        ],
    }
    if _traverse_rrsets(uri, ctx, rrset, 'is_content_present',):
        click.echo(json.dumps({'message': f'{name} {record_type} {content} already present'}))
        sys.exit(0)

    r = _http_patch(uri, ctx, {'rrsets': [rrset]})
    if _create_output(r, (204,),
                      optional_json={'message': f'{name} {record_type} {content} created'}):
        sys.exit(0)
    sys.exit(1)


# Add Tsigkey
@cli.command()
@click.argument('name', type=click.STRING)
@click.argument('algorithm',
                type=click.Choice([
                  'hmac-md5',
                  'hmac-sha1',
                  'hmac-sha224',
                  'hmac-sha256',
                  'hmac-sha384',
                  'hmac-sha512'
                ]))
@click.option('-s', '--secret', type=click.STRING)
@click.pass_context
def add_tsigkey(
    ctx,
    name,
    algorithm,
    secret,
):
    """
    Adds a TSIGKey to the server to sign DNS messages
    """
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/tsigkeys"
    payload = {
        'name': name,
        'algorithm': algorithm
    }
    if secret:
        payload['key'] = secret

    r = _http_post(uri, ctx, payload)
    if _create_output(r, (201,),):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.argument('zone', type=click.STRING)
@click.argument('nameservers', type=click.STRING)
@click.argument(
    'zonetype',
    type=click.Choice(['MASTER', 'NATIVE'], case_sensitive=False),
)
@click.option(
    '-m',
    '--master',
    type=click.STRING,
    help='Set Zone Masters',
    default=None,
)
@click.pass_context
def add_zone(ctx, zone, nameservers, zonetype, master):
    """
    Adds a new zone

    Can create a master or native zone, slaves zones are disabled
    """
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones"
    zone = _make_canonical(zone)
    if zonetype.upper() in ('MASTER', 'NATIVE'):
        payload = {
            'name': zone,
            'kind': zonetype.capitalize(),
            'masters': master.split(',') if master else [],
            'nameservers': [_make_canonical(server) for server in nameservers.split(',')],
        }
    else:
        click.echo(json.dumps({'error': 'Slave entries are not supported right now'}))
        sys.exit(1)
    current_zones = _query_zones(ctx)
    if [z for z in current_zones if z['name'] == zone]:
        click.echo(json.dumps({'message': f'Zone {zone} already present'}))
        sys.exit(0)
    r = _http_post(uri, ctx, payload)
    if _create_output(r,
                      (201,),
                      optional_json={'message': f'Zone {zone} created'}
                      ):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.argument('zone', type=click.STRING)
@click.argument(
    'metadata-key',
    type=click.STRING
)
@click.argument(
    'metadata-value',
    type=click.STRING
)
@click.pass_context
def add_zonemetadata(ctx, zone, metadata_key, metadata_value):
    """
    Appends metadata to a zone. Metadata is not arbitrary and must conform
    to the expected content from the powerdns configuration

    Example:
    powerdns-cli add-zonemetadata example.org ALSO-NOTIFY 192.0.2.1:5300
    """
    zone = _make_canonical(zone)
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}/metadata"
    payload = {
        'kind': metadata_key,
        'metadata': [
            metadata_value
        ]
    }
    r = _http_post(uri, ctx, payload)
    if _create_output(r, (201,)):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.argument('ip', type=click.STRING)
@click.argument('nameserver', type=click.STRING)
@click.pass_context
def delete_autoprimary(
    ctx,
    ip,
    nameserver,
):
    """
    Deletes an autoprimary from the dns server configuration
    """
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/autoprimaries/{ip}/{nameserver}"

    r = _http_delete(uri, ctx)
    if _create_output(
            r,
            (204,),
            optional_json={'message': f'Autoprimary {ip} with nameserver {nameserver} deleted'}
    ):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.pass_context
@click.argument('zone', type=click.STRING)
@click.argument('cryptokey-id', type=click.INT)
def delete_cryptokey(ctx, zone, cryptokey_id):
    """
    Lists all currently configured cryptokeys for this zone
    """
    zone = _make_canonical(zone)
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}/cryptokeys/{cryptokey_id}"
    r = _http_delete(uri, ctx)
    if _create_output(r,
                      (204,),
                      optional_json={
                          'message': f'Deleted id {cryptokey_id} for zone {zone}'}
                      ):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.argument('keyid', type=click.STRING)
@click.pass_context
def delete_tsigkey(
    ctx,
    keyid
):
    """
    Delete the TSIG-Key with the given server-side id
    """
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/tsigkeys/{keyid}"

    r = _http_delete(uri, ctx)
    if _create_output(r, (204,), optional_json={'message': f'Deleted tsigkey with id {keyid}'}):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.argument('name', type=click.STRING)
@click.argument('zone')
@click.argument(
    'record-type',
    type=click.Choice(
        [
            'A',
            'AAAA',
            'CNAME',
            'MX',
            'NS',
            'PTR',
            'SOA',
            'SRV',
            'TXT',
        ],
        case_sensitive=False,
    ),
)
@click.argument('content', type=click.STRING)
@click.option(
    '--ttl',
    default=3600,
    type=click.INT,
    help='Set default time to live')
@click.option(
    '-a',
    '-all',
    'delete_all',
    is_flag=True,
    default=False,
    help='Deletes all records of the selected type',)
@click.pass_context
def delete_record(ctx, name, zone, record_type, content, ttl, delete_all):
    """
    Deletes the DNS record of the given types and content

    If all is specified, all entries of given type and name will be removed

    Example:
    powerdns-cli delete_record mail example.org A 10.0.0.1
    """
    zone = _make_canonical(zone)
    name = _make_dnsname(name, zone)
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}"
    if delete_all:
        rrset = {
            'name': name,
            'type': record_type,
            'ttl': ttl,
            'changetype': 'DELETE',
            'records': []
        }
        if not _traverse_rrsets(uri, ctx, rrset, 'matching_rrset'):
            click.echo(json.dumps({'message': f'{record_type} records in {name} already absent'}))
            sys.exit(0)
        r = _http_patch(uri, ctx, {'rrsets': [rrset]})
        msg = {'message': f'All {record_type} records for {name} removed'}
        if _create_output(r, (204,), optional_json=msg):
            sys.exit(0)
        sys.exit(1)

    rrset = {
        'name': name,
        'type': record_type,
        'ttl': ttl,
        'changetype': 'REPLACE',
        'records': [
            {
                'content': content,
                'disabled': False,
            }
        ]
    }
    if not _traverse_rrsets(uri, ctx, rrset, 'is_content_present'):
        msg = {'message': f'{name} {record_type} {content} already absent'}
        click.echo(json.dumps(msg))
        sys.exit(0)
    matching_rrsets = _traverse_rrsets(uri, ctx, rrset, 'matching_rrset')
    indizes_to_remove = []
    for index in range(len(matching_rrsets['records'])):
        if matching_rrsets['records'][index] == rrset['records'][0]:
            indizes_to_remove.append(index)
    indizes_to_remove.reverse()
    for index in indizes_to_remove:
        matching_rrsets['records'].pop(index)
    rrset['records'] = matching_rrsets['records']
    r = _http_patch(uri, ctx, {'rrsets': [rrset]})
    msg = {'message': f'{name} {record_type} {content} removed'}
    if _create_output(r, (204,), optional_json=msg):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.argument('zone', type=click.STRING)
@click.option(
    '-f',
    '--force',
    help='Force execution and skip confirmation',
    is_flag=True,
    default=False,
    show_default=True,
)
@click.pass_context
def delete_zone(ctx, zone, force):
    """
    Deletes a Zone
    """
    zone = _make_canonical(zone)
    upstream_zones = _query_zones(ctx)
    if zone not in [single_zone['name'] for single_zone in upstream_zones]:
        click.echo(json.dumps({'message': f'Zone {zone} already absent'}))
        sys.exit(0)

    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}"
    _confirm(
        f'!!!! WARNING !!!!!\n'
        f'You are attempting to delete {zone}\n'
        f'Are you sure? [y/N] ',
        force
    )
    r = _http_delete(uri, ctx)
    msg = {'message': f'Zone {zone} deleted'}
    if _create_output(r, (204,), optional_json=msg):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.argument('zone', type=click.STRING)
@click.argument(
    'metadata-key',
    type=click.STRING
)
@click.pass_context
def delete_zonemetadata(ctx, zone, metadata_key):
    """
    Deletes a metadata entry for the given zone completely

    Example:
    powerdns-cli delete-zonemetadata example.org ALSO-NOTIFY
    """
    zone = _make_canonical(zone)
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}/metadata/{metadata_key}"
    r = _http_delete(uri, ctx)
    if _create_output(
            r,
            (200, 204),
            optional_json={'message': f'Deleted metadata key {metadata_key} for {zone}'}
    ):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.pass_context
@click.argument('zone', type=click.STRING)
@click.argument('cryptokey-id', type=click.INT)
def disable_cryptokey(ctx, zone, cryptokey_id):
    """
    Disables the cryptokey for this zone
    """
    zone = _make_canonical(zone)
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}/cryptokeys/{cryptokey_id}"
    payload = {
        'id': cryptokey_id,
        'active': False,
    }
    r = _http_put(uri, ctx, payload)
    if _create_output(r,
                      (204,),
                      optional_json={
                          'message': f'Disabled id {cryptokey_id} for zone {zone}'}
                      ):
        sys.exit(0)
    sys.exit(1)


# Disable record
@cli.command()
@click.argument('name', type=click.STRING)
@click.argument('zone', type=click.STRING)
@click.argument(
    'record-type',
    type=click.Choice(
        [
            'A',
            'AAAA',
            'CNAME',
            'MX',
            'NS',
            'PTR',
            'SOA',
            'SRV',
            'TXT',
        ],
    ),
)
@click.argument('content', type=click.STRING)
@click.option('--ttl', default=3600, type=click.INT, help='Set time to live')
@click.pass_context
def disable_record(
    ctx,
    name,
    record_type,
    content,
    zone,
    ttl,
):
    """
    Disable an existing DNS record.
    Use @ if you want to enter a record for the top level

    powerdns-cli disable_record test01 example.org A 10.0.0.1
    """
    zone = _make_canonical(zone)
    name = _make_dnsname(name, zone)
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}"

    rrset = {
                'name': name,
                'type': record_type,
                'ttl': ttl,
                'changetype': 'REPLACE',
                'records': [
                    {
                        'content': content,
                        'disabled': True
                    }
                ]
            }

    if _traverse_rrsets(uri, ctx, rrset, 'is_content_present'):
        msg = {'message': f'{name} IN {record_type} {content} already disabled'}
        click.echo(json.dumps(msg))
        sys.exit(0)
    rrset['records'] = _traverse_rrsets(uri, ctx, rrset, 'merge_rrsets')
    r = _http_patch(uri, ctx, {'rrsets': [rrset]})
    msg = {'message': f'{name} IN {record_type} {content} disabled'}
    if _create_output(r, (204,), optional_json=msg):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.pass_context
@click.argument('zone', type=click.STRING)
@click.argument('cryptokey-id', type=click.INT)
def enable_cryptokey(ctx, zone, cryptokey_id):
    """
    Enables the given cryptokey for this zone
    """
    zone = _make_canonical(zone)
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}/cryptokeys/{cryptokey_id}"
    payload = {
        'id': cryptokey_id,
        'active': True,
    }
    r = _http_put(uri, ctx, payload)
    if _create_output(r,
                      (204,),
                      optional_json={'message': f'Enabled id {cryptokey_id} for zone {zone}'}):
        sys.exit(0)
    sys.exit(1)


# Extend record
@cli.command()
@click.argument('name', type=click.STRING)
@click.argument('zone', type=click.STRING)
@click.argument(
    'record-type',
    type=click.Choice(
        [
            'A',
            'AAAA',
            'CNAME',
            'MX',
            'NS',
            'PTR',
            'SOA',
            'SRV',
            'TXT',
        ],
    ),
)
@click.argument('content', type=click.STRING)
@click.option('--ttl', default=3600, type=click.INT, help='Set time to live')
@click.pass_context
def extend_record(
    ctx,
    name,
    record_type,
    content,
    zone,
    ttl,
):
    """
    Extends an existing new recordset.
    Will create a new record if it did not exist beforehand.
    """
    zone = _make_canonical(zone)
    name = _make_dnsname(name, zone)
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}"

    rrset = {
                'name': name,
                'type': record_type,
                'ttl': ttl,
                'changetype': 'REPLACE',
                'records': [
                    {
                        'content': content,
                        'disabled': False
                    }
                ]
            }

    if _traverse_rrsets(uri, ctx, rrset, 'is_content_present'):
        click.echo(json.dumps({'message': f'{name} IN {record_type} {content} already present'}))
        sys.exit(0)
    upstream_rrset = _traverse_rrsets(uri, ctx, rrset, 'matching_rrset')
    if upstream_rrset:
        extra_records = [
            record for record
            in upstream_rrset['records']
            if record['content'] != rrset['records'][0]['content']
        ]
        rrset['records'].extend(extra_records)
    r = _http_patch(uri, ctx, {'rrsets': [rrset]})
    msg = {'message': f'{name} IN {record_type} {content} extended'}
    if _create_output(r, (204,), optional_json=msg):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.pass_context
@click.argument('zone', type=click.STRING)
@click.argument('cryptokey-id', type=click.STRING)
def export_cryptokey(ctx, zone, cryptokey_id):
    """
    Exports the cryptokey including the private key for the given zone
    """
    zone = _make_canonical(zone)
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}/cryptokeys/{cryptokey_id}"
    r = _http_get(uri, ctx)
    if _create_output(r, (200,)):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.argument('serverid', type=click.STRING)
@click.pass_context
def export_server(ctx, serverid):
    """
    List DNS-Servers
    """
    uri = f"{ctx.obj['apihost']}/api/v1/servers/{serverid}"
    r = _http_get(uri, ctx)
    if _create_output(r, (200,)):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.pass_context
@click.argument(
    'keyid',
    type=click.STRING,
)
def export_tsigkey(ctx, keyid):
    """
    Exports the tsigkey with the given id
    """
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/tsigkeys/{keyid}"
    r = _http_get(uri, ctx)
    if _create_output(r, (200,)):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.pass_context
@click.argument(
    'zone',
    type=click.STRING,
)
@click.option(
    '-b',
    '--bind',
    help='Use bind format as output',
    is_flag=True,
    default=False,
)
def export_zone(ctx, zone, bind):
    """
    Export the whole zone configuration
    """
    zone = _make_canonical(zone)
    if bind:
        uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}/export"
        r = _http_get(uri, ctx)
        if _create_output(r, (200,), output_text=True):
            sys.exit(0)
        sys.exit(1)
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}"
    r = _http_get(uri, ctx)
    if _create_output(r, (200,)):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.pass_context
@click.argument('zone', type=click.STRING)
def flush_cache(ctx, zone):
    """Flushes the cache of the DNS-Server"""
    zone = _make_canonical(zone)
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/cache/flush"
    r = _http_put(uri, ctx, params={'domain': zone})
    if _create_output(r, (200,)):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.pass_context
def list_autoprimaries(ctx):
    """
    Lists all currently configured autoprimary servers
    """
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/autoprimaries"
    r = _http_get(uri, ctx)
    if _create_output(r, (200,)):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.pass_context
def list_config(ctx):
    """
    Query PDNS Config
    """
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/config"
    r = _http_get(uri, ctx)
    if _create_output(r, (200,)):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.pass_context
@click.argument('zone', type=click.STRING)
def list_cryptokeys(ctx, zone):
    """
    Lists all currently configured cryptokeys for this zone
    """
    zone = _make_canonical(zone)
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}/cryptokeys"
    r = _http_get(uri, ctx)
    if _create_output(r, (200,)):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.pass_context
def list_tsigkeys(ctx):
    """
    Lists all TSIGKeys on the server
    """
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/tsigkeys"
    r = _http_get(uri, ctx)
    if _create_output(r, (200,)):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.pass_context
def list_servers(ctx):
    """
    List DNS-Servers
    """
    uri = f"{ctx.obj['apihost']}/api/v1/servers"
    r = _http_get(uri, ctx)
    if _create_output(r, (200,)):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.pass_context
def list_stats(ctx):
    """
    Query DNS Stats
    """
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/statistics"
    r = _http_get(uri, ctx)
    if _create_output(r, (200,)):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.argument('zone', type=click.STRING)
@click.option(
    '-l',
    '--limit',
    type=click.STRING,
    help='Limit metadata output to this single element'
)
@click.pass_context
def list_zonemetadata(ctx, zone, limit):
    """
    Lists metadata for a given zone. Can optionally be limited to a single metadata key.

    Example:
    powerdns-cli list-zonemetadata -l "IFXR" example.org
    """
    zone = _make_canonical(zone)
    if limit:
        uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}/metadata/{limit}"
    else:
        uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}/metadata"
    r = _http_get(uri, ctx)
    if _create_output(r, (200,)):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.pass_context
def list_zones(ctx):
    """
    Get all zones of dns server
    """
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones"
    r = _http_get(uri, ctx)
    if _create_output(r, (200,)):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.pass_context
@click.argument(
    'zone',
    type=click.STRING,
)
def notify_zone(ctx, zone):
    """
    Notify given zone to its slaves

    Fails when zone kind is not Master or Slave, or master and slave are
    disabled in the configuration. Only works for slave if renotify is on.
    """
    zone = _make_canonical(zone)
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}/notify"
    r = ctx.obj['session'].put(uri)
    if _create_output(r, (200,)):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.pass_context
@click.argument(
    'zone',
    type=click.STRING,
)
def rectify_zone(ctx, zone):
    """
    Rectify a given zone

    Will fail on slave zones and zones without dnssec
    """
    zone = _make_canonical(zone)
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}/rectify"
    r = ctx.obj['session'].put(uri)
    if _create_output(r, (200,)):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.argument('zone', type=click.STRING)
@click.argument(
    'metadata-key',
    type=click.STRING
)
@click.argument(
    'metadata-value',
    type=click.STRING
)
@click.pass_context
def replace_zonemetadata(ctx, zone, metadata_key, metadata_value):
    """
    Replaces a metadataset of a given zone

    Example:
    powerdns-cli replace-zonemetadata example.org ALSO-NOTIFY 192.0.2.1:5300
    """
    zone = _make_canonical(zone)
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones/{zone}/metadata/{metadata_key}"
    payload = {
        'kind': metadata_key,
        'metadata': [
            metadata_value
        ]
    }
    r = _http_put(uri, ctx, payload)
    if _create_output(r, (200,)):
        sys.exit(0)
    sys.exit(1)


@cli.command()
@click.argument('search-string', metavar='STRING')
@click.option('--max', 'max_output', help='Number of items to output', default=5, type=click.INT,)
@click.pass_context
def search(ctx, search_string, max_output):
    """Do fulltext search in dns database"""
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/search-data"
    r = _http_get(
        uri,
        ctx,
        params={'q': f'*{search_string}*', 'max': max_output},
    )
    if _create_output(r, (200,)):
        sys.exit(0)
    sys.exit(1)


# Update Tsigkey
@cli.command()
@click.argument('keyid', type=click.STRING,)
@click.option('-a', '--algorithm',
              type=click.Choice([
                  'hmac-md5',
                  'hmac-sha1',
                  'hmac-sha224',
                  'hmac-sha256',
                  'hmac-sha384',
                  'hmac-sha512'
              ]))
@click.option('-s', '--secret', type=click.STRING)
@click.option('-n', '--name', type=click.STRING)
@click.pass_context
def update_tsigkey(
    ctx,
    keyid,
    algorithm,
    secret,
    name
):
    """
    Updates an existing TSIGKey
    """
    uri = f"{ctx.obj['apihost']}/api/v1/servers/localhost/tsigkeys/{keyid}"
    tsigkey = {}
    if algorithm:
        tsigkey['algorithm'] = algorithm
    if secret:
        tsigkey['secret'] = secret
    if name:
        tsigkey['name'] = name
    r = _http_put(uri, ctx, tsigkey)
    if _create_output(r, (200,),):
        sys.exit(0)
    sys.exit(1)


def _confirm(message: str, force: bool) -> None:
    """Confirmation function to keep users from doing potentially dangerous actions.
    Uses the force flag to determine if a manual confirmation is required."""
    if not force:
        click.echo(message)
        confirmation = input()
        if confirmation not in ('y', 'Y', 'YES', 'yes', 'Yes'):
            click.echo('Aborting')
            sys.exit(1)


def _create_output(
        content: requests.Response,
        exp_status_code: tuple,
        output_text: bool = None,
        optional_json: dict = None) -> bool:
    """Helper function to print a message in the appropriate format.
    Is needed since the powerdns api outputs different content types, not
    json all the time. Sometimes output is empty (each 204 response) or
    needs to be plain text - when you want to the BIND / AFXR export."""
    if content.status_code in exp_status_code and output_text:
        click.echo(content.text)
        return True
    if content.status_code in exp_status_code and optional_json:
        click.echo(json.dumps(optional_json))
        return True
    if content.status_code in exp_status_code:
        click.echo(json.dumps(content.json()))
        return True
    if (content.headers.get('Content-Type') and
            content.headers['Content-Type'].startswith('text/plain')):
        click.echo(json.dumps({'error': content.text}))
        return False
    # Catch unexpected empty responses
    try:
        click.echo(json.dumps(content.json()))
    except json.JSONDecodeError:
        click.echo(
            json.dumps(
                {'error': f'Non json response from server with status {content.status_code}'}
            )
        )
    return False


def _http_delete(uri: str, ctx: click.Context, params: dict = None) -> requests.Response:
    """HTTP DELETE request"""
    try:
        request = ctx.obj['session'].delete(uri, params=params)
        return request
    except requests.RequestException as e:
        click.echo(json.dumps({'error': f'Request error: {e}'}))
        sys.exit(1)


def _http_get(uri: str, ctx: click.Context, params: dict = None) -> requests.Response:
    try:
        request = ctx.obj['session'].get(uri, params=params)
        return request
    except requests.RequestException as e:
        click.echo(json.dumps({'error': f'Request error: {e}'}))
        sys.exit(1)


def _http_patch(uri: str, ctx: click.Context, payload: dict, ) -> requests.Response:
    try:
        request = ctx.obj['session'].patch(uri, json=payload)
        return request
    except requests.RequestException as e:
        click.echo(json.dumps({'error': f'Request error: {e}'}))
        sys.exit(1)


def _http_post(uri: str, ctx: click.Context, payload: dict) -> requests.Response:
    try:
        request = ctx.obj['session'].post(uri, json=payload)
        return request
    except requests.RequestException as e:
        click.echo(json.dumps({'error': f'Request error: {e}'}))
        sys.exit(1)


def _http_put(
        uri: str,
        ctx: click.Context,
        payload: dict = None,
        params: dict = None
) -> requests.Response:
    try:
        request = ctx.obj['session'].put(uri, json=payload, params=params)
        return request
    except requests.RequestException as e:
        click.echo(json.dumps({'error': f'Request error: {e}'}))
        sys.exit(1)


def _query_zones(ctx) -> list:
    """Returns all zones of the dns server"""
    r = _http_get(f"{ctx.obj['apihost']}/api/v1/servers/localhost/zones", ctx)
    if r.status_code != 200:
        click.echo(json.dumps({'error': r.json()}))
        sys.exit(1)
    return r.json()


def _query_zone_rrsets(uri: str, ctx) -> list:
    """Queries the configuration of the given zone"""
    r = _http_get(uri, ctx)
    if r.status_code != 200:
        click.echo(json.dumps({'error': r.json()}))
        sys.exit(1)
    return r.json()['rrsets']


def _make_canonical(zone: str) -> str:
    """Returns the zone in caonical format with a trailing dot"""
    if not zone.endswith('.'):
        zone += '.'
    return zone


def _make_dnsname(name: str, zone: str) -> str:
    """Returns either the combination or zone
    or just a zone when @ is provided as name"""
    if name == '@':
        return zone
    return f'{name}.{zone}'


def _traverse_rrsets(
        uri: str,
        ctx: click.Context,
        new_rrset: dict,
        query: Literal[
            'matching_rrset',
            'is_content_present',
            'merge_rrsets'],
        ):
    """Helper function to compare upstream and downstream rrsets / records"""
    zone_rrsets = _query_zone_rrsets(uri, ctx)
    if query == 'matching_rrset':
        for upstream_rrset in zone_rrsets:
            if all(upstream_rrset[key] == new_rrset[key] for key in ('name', 'type')):
                return upstream_rrset
        return {}
    if query == 'is_content_present':
        for rrset in zone_rrsets:
            # go through all the records to find matching rrset
            if (
                    all(rrset[key] == new_rrset[key] for key in ('name', 'type'))
                    and
                    all(entry in rrset['records'] for entry in new_rrset['records'])
            ):
                return True
        return False
    if query == 'merge_rrsets':
        merged_rrsets = new_rrset['records'].copy()
        for upstream_rrset in zone_rrsets:
            if all(upstream_rrset[key] == new_rrset[key] for key in ('name', 'type')):
                merged_rrsets.extend([record for record in upstream_rrset['records']
                                      if record['content'] != new_rrset['records'][0]['content']])
        return merged_rrsets
    return None


def main():
    """Main entrypoint to the cli application"""
    cli(auto_envvar_prefix='POWERDNS_CLI')


if __name__ == '__main__':
    main()
