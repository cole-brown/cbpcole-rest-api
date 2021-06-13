# coding: utf-8

'''
Collection Endpoints for REST API.
'''

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from typing import Optional, Type, NewType, Dict, Tuple, TextIO

import uuid
import functools

from flask import (
    Blueprint,
    request,
    Response,
    current_app,
    flash, g, redirect, render_template, session, url_for
)
from http import HTTPStatus

from .db import get_db
from .time import UnixEpoch


# -----------------------------------------------------------------------------
# Flask Set-Up
# -----------------------------------------------------------------------------

blueprint = Blueprint('collect', __name__)


# -----------------------------------------------------------------------------
# Flask Routes
# -----------------------------------------------------------------------------

@blueprint.route('/collect')
def collect():
    '''
    Endpoint for collecting `cid` (UUIDs of visitors) for datetime utcnow (or
    `d`, if defined).

    /collect?cid=<UUID>&d=<UNIX-timestamp>
    '''
    success = True

    # ------------------------------
    # Get params.
    # ------------------------------
    try:
        cid = request.args.get('cid')
        uuid = current_app.url_map.converters['uuid'].to_python(cid)

        # Parse arg if it was provided or get current time. Trim to just
        # seconds resolution.
        unixtime = UnixEpoch.seconds(
            UnixEpoch.parse(
                request.args.get('d')))

    except:
        success = False

    if not uuid or not unixtime:
        success = False

    if not success:
        # Quit early. No requirements to indicate failure - just says to return
        # 200/OK with empty body.
        current_app.logger.error("'collect/' failed params parsing: "
                                 "uuid=%s, d=%s",
                                 uuid, unixtime)
        return Response('', HTTPStatus.OK, mimetype='text/plain')

    current_app.logger.info("'collect/' parsed params successfully: "
                            "uuid=%s, d=%s",
                            uuid, unixtime)

    # ------------------------------
    # Save to database.
    # ------------------------------
    db = get_db()
    db.execute(
        'INSERT INTO user (uuid, visited_at) VALUES (?, ?)',
        (uuid.bytes, )
    )
    db.commit()

    current_app.logger.info("'collect/' saved to database: "
                            "uuid=%s, d=%s",
                            uuid, unixtime)
    return Response('', HTTPStatus.OK, mimetype='text/plain')
