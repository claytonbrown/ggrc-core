# Copyright (C) 2020 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Handle the interface to GGRC models for all login methods.
"""

import logging

import flask
import flask_login
from werkzeug import exceptions
from werkzeug.security import generate_password_hash as generate_hash

from ggrc import db, settings
from ggrc.models import all_models
from ggrc.utils.log_event import log_event
from ggrc.utils.user_generator import (
    find_or_create_ext_app_user, is_app_2_app_user_email, parse_user_email
)

logger = logging.getLogger(__name__)


def get_next_url(request, default_url):
  """Returns next url from requres or default url if it's not found."""
  if 'next' in request.args:
    next_url = request.args['next']
    return next_url
  return default_url


def commit_user_and_role(user):
  """Commits and flushes user and its role after the login."""
  db_user, db_role = None, None
  if hasattr(flask.g, "user_cache"):
    db_user = flask.g.user_cache.get(user.email, None)
  if hasattr(flask.g, "user_creator_roles_cache"):
    db_role = flask.g.user_creator_roles_cache.get(user.email, None)
  if db_user or db_role:
    db.session.flush()
    if db_user:
      log_event(db.session, db_user, db_user.id, flush=False)
    elif db_role:
      # log_event of user includes event of role creation.
      # if no user in cache, then it was created before but has no role.
      log_event(db.session, db_role, user.id, flush=False)
    db.session.commit()


def check_appengine_appid(request):
  """Check if appengine app ID in whitelist."""
  inbound_appid = request.headers.get("X-Appengine-Inbound-Appid")

  if not inbound_appid:
    # don't check X-GGRC-user if the request doesn't come from another app
    return None

  if inbound_appid not in settings.ALLOWED_QUERYAPI_APP_IDS:
    # by default, we don't allow incoming app2app connections from
    # non-whitelisted apps
    raise exceptions.BadRequest(
        "X-Appengine-Inbound-Appid header contains "
        "untrusted application id: {}".format(inbound_appid)
    )

  return inbound_appid


def get_ggrc_user(request, mandatory):
  """Find user from email in "X-GGRC-user" header."""
  email = parse_user_email(request, "X-GGRC-user", mandatory=mandatory)

  if not email:
    return None

  if is_app_2_app_user_email(email):
    # External Application User should be created if doesn't exist.
    user = get_external_app_user(email)
  else:
    user = all_models.Person.query.filter_by(email=email).first()

  if not user:
    raise exceptions.BadRequest("No user with such email: %s" % email)

  return user


def get_external_app_user(email):
  """Find or create external app user from email in "X-GGRC-user" header."""
  app_user = find_or_create_ext_app_user(email)

  if app_user.id is None:
    db.session.flush()

  return app_user


def login_user(user):
  """
  For the sake of security, the user_email_hash is added to the session.
  When the database gets updated while users perform the activity,
  ids in the sessions and in the database may mess up.
  This means that a random user can access the data of another.
  To prevent this, the session now has the user_email_hash
  generated by generate_hash. This hash should be used
  to confirm that a user with provided id has the same email stored
  in the database
  """

  commit_user_and_role(user)
  if user.system_wide_role != 'No Access':
    flask_login.login_user(user)
    flask.session["user_email_hash"] = generate_hash(user.email)
    return flask.redirect(get_next_url(
        flask.request, default_url=flask.url_for('dashboard')))

  flask.flash(u'You do not have access. Please contact your administrator.',
              'alert alert-info')
  return flask.redirect('/')
