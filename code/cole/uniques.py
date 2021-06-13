# coding: utf-8

'''
Reports of Unique Users Endpoints for REST API.
'''

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from flask import (
    Blueprint,
    request,
    Response,
    current_app,
)
from http import HTTPStatus

from .db import get_db
from .time import (
    UnixEpoch,
    Iso8601
)


# -----------------------------------------------------------------------------
# Flask Set-Up
# -----------------------------------------------------------------------------

blueprint = Blueprint('uniques', __name__)


# -----------------------------------------------------------------------------
# Flask Routes
# -----------------------------------------------------------------------------

@blueprint.route('/daily_uniques')
def daily_uniques() -> Response:
    '''
    Endpoint for getting Daily Unique Users count of the given ISO-8601 date.

    /daily_uniques?d=<ISO-8601>
    '''
    success = True

    # ------------------------------
    # Get params.
    # ------------------------------
    try:
        iso_date = Iso8601.parse(
            request.args.get('d'))
        time_range = UnixEpoch.range_day(iso_date)

    except:
        # except Exception:
        success = False
        # raise

    if not time_range:
        success = False

    if not success:
        # Quit early. No requirements to indicate failure - no requirements at
        # all... so conform to '/collect' endpoint's requirements.
        current_app.logger.error("'daily_uniques/' failed params parsing: "
                                 "range=%s (iso=%s)",
                                 time_range,
                                 iso_date)
        return Response('', HTTPStatus.OK, mimetype='text/plain')

    current_app.logger.info("'daily_uniques/' parsed params successfully: "
                            "range=%s (iso=%s)",
                            time_range,
                            iso_date)

    # ------------------------------
    # Save to database.
    # ------------------------------
    db = get_db()
    results = db.execute(
        'SELECT COUNT(DISTINCT uuid) FROM user '
        'WHERE visited_at BETWEEN ? AND ?',
        time_range
    )

    uniques = results.fetchone()[0]
    current_app.logger.info("'daily_uniques/' database query result: "
                            "uniques=%s",
                            uniques)
    return Response(str(uniques), HTTPStatus.OK, mimetype='text/plain')


@blueprint.route('/monthly_uniques')
def monthly_uniques() -> Response:
    '''
    Endpoint for getting Monthly Unique Users count of the given ISO-8601 date.

    Requirement is a bit vague...:
      - "[...] which should return the number of unique users seen in the month
        prior to and including the given GMT day."
        + What is "month"? Calendar month? Rolling 30 days?
          - I'll just assume this means that, given an input of:
              <year>-<month>-<day>
            we should search for a date range of:
              <year>-<month>-01 to <year>-<month>-<day>.

    /monthly_uniques?d=<ISO-8601>
    '''
    success = True

    # ------------------------------
    # Get params.
    # ------------------------------
    try:
        iso_date = Iso8601.parse(
            request.args.get('d'))
        time_range = UnixEpoch.range_month(iso_date)

    except:
        success = False

    if not time_range:
        success = False

    if not success:
        # Quit early. No requirements to indicate failure - no requirements at
        # all... so conform to '/collect' endpoint's requirements.
        current_app.logger.error("'monthly_uniques/' failed params parsing: "
                                 "range=%s (iso=%s)",
                                 time_range,
                                 iso_date)
        return Response('', HTTPStatus.OK, mimetype='text/plain')

    current_app.logger.info("'monthly_uniques/' parsed params successfully: "
                            "range=%s (iso=%s)",
                            time_range,
                            iso_date)

    # ------------------------------
    # Save to database.
    # ------------------------------
    db = get_db()
    results = db.execute(
        'SELECT COUNT(DISTINCT uuid) FROM user '
        'WHERE visited_at BETWEEN ? AND ?',
        time_range
    )

    uniques = results.fetchone()[0]
    current_app.logger.info("'monthly_uniques/' database query result: "
                            "uniques=%s",
                            uniques)
    return Response(str(uniques), HTTPStatus.OK, mimetype='text/plain')
