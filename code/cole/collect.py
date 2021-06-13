# coding: utf-8

'''
Collection Endpoints for REST API.
'''

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import uuid

from flask import (
    Blueprint,
    request,
    Response,
    current_app,
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
def collect() -> None:
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
        cid = uuid.UUID(request.args.get('cid'))

        # Parse arg if it was provided or get current time. Trim to just
        # seconds resolution.
        unixtime = UnixEpoch.seconds(
            UnixEpoch.parse(
                request.args.get('d')))

    except:
        success = False

    if not cid or not unixtime:
        success = False

    if not success:
        # Quit early. No requirements to indicate failure - just says to return
        # 200/OK with empty body.
        current_app.logger.error("'collect/' failed params parsing: "
                                 "cid=%s, d=%s",
                                 cid, unixtime)
        return Response('', HTTPStatus.OK, mimetype='text/plain')

    current_app.logger.info("'collect/' parsed params successfully: "
                            "cid=%s, d=%s",
                            cid, unixtime)

    # ------------------------------
    # Save to database.
    # ------------------------------
    db = get_db()
    db.execute(
        'INSERT INTO user (uuid, visited_at) VALUES (?, ?)',
        (cid.bytes, unixtime)
    )
    db.commit()

    current_app.logger.info("'collect/' saved to database: "
                            "cid=%s, d=%s",
                            cid, unixtime)
    return Response('', HTTPStatus.OK, mimetype='text/plain')
