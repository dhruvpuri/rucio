# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Vincent Garonne,  <vincent.garonne@cern.ch> , 2012

from nose.tools import assert_true, assert_false

from rucio.api.permission import has_permission
from rucio.db.session import build_database, destroy_database, create_root_account
from rucio.common.utils import generate_uuid as uuid
from rucio.core.account import add_account


class TestPermissionCoreApi():

    def setUp(self):
        build_database()
        create_root_account()
        self.usr = str(uuid())
        add_account(self.usr, 'user')

    def tearDown(self):
        destroy_database()

    def test_permission_add_account(self):
        """ PERMISSION(CORE): Check permission to add account """
        assert_true(has_permission(issuer='root', action='add_account', kwargs={'accountName': 'account1'}))
        assert_false(has_permission(issuer='self.usr', action='add_account', kwargs={'accountName': 'account1'}))

    def test_permission_add_scope(self):
        """ PERMISSION(CORE): Check permission to add scope """
        assert_true(has_permission(issuer='root', action='add_scope', kwargs={'accountName': 'account1'}))
        assert_false(has_permission(issuer=self.usr, action='add_scope', kwargs={'accountName': 'root'}))
        assert_true(has_permission(issuer=self.usr, action='add_scope', kwargs={'accountName': self.usr}))

    def test_permission_get_auth_token_user_pass(self):
        """ PERMISSION(CORE): Check permission to get_auth_token_user_pass """
        assert_true(has_permission(issuer='root', action='get_auth_token_user_pass', kwargs={'account': 'root', 'username': 'ddmlab', 'password': 'secret'}))
        assert_false(has_permission(issuer='root', action='get_auth_token_user_pass', kwargs={'account': self.usr, 'username': 'ddmlab', 'password': 'secret'}))

    def test_permission_get_auth_token_x509(self):
        """ PERMISSION(CORE): Check permission to get_auth_token_x509 """
        dn = '/C=CH/ST=Geneva/O=CERN/OU=PH-ADP-CO/CN=DDMLAB Client Certificate/emailAddress=ph-adp-ddm-lab@cern.ch'
        assert_true(has_permission(issuer='root', action='get_auth_token_x509', kwargs={'account': 'root', 'dn': dn}))
        assert_false(has_permission(issuer='root', action='get_auth_token_x509', kwargs={'account': self.usr, 'dn': dn}))

    def test_permission_get_auth_token_gss(self):
        """ PERMISSION(CORE): Check permission to get_auth_token_gss """
        gsscred = 'ddmlab@CERN.CH'
        assert_true(has_permission(issuer='root', action='get_auth_token_gss', kwargs={'account': 'root', 'gsscred': gsscred}))
        assert_false(has_permission(issuer='root', action='get_auth_token_gss', kwargs={'account': self.usr, 'gsscred': gsscred}))
