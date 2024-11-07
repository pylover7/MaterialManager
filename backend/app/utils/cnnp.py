from ldap3 import Server, Connection, ALL


class LDAPAuthentication:
    def __init__(self):
        self.server = Server('127.0.0.1', get_info=ALL, connect_timeout=10)
        self.conn = None
        self.basedn = 'ou=海南核电有限公司,dc=cnnp,dc=com,dc=cn'

    def ldap_connect(self):
        self.conn = Connection(self.server, auto_bind=True)

    def get_user_dn(self, uid):
        self.ldap_connect()
        self.conn.search(self.basedn, '(uid={})'.format(uid), attributes=['dn'])
        entries = self.conn.entries
        if entries:
            return entries[0].dn
        else:
            print("未找到该用户")
            return None

    def authenticate(self, uid, password):
        user_dn = self.get_user_dn(uid)
        if not user_dn:
            return False

        try:
            self.conn = Connection(self.server, user=user_dn, password=password, auto_bind=True)
            print(f"{user_dn} 验证通过")
            return True
        except Exception as e:
            print(f"{user_dn} 验证失败")
            print(e)
            return False

    def close_ctx(self):
        if self.conn:
            self.conn.unbind()


if __name__ == '__main__':
    from ldap3 import Server, Connection, ALL
    server = Server('10.20.21.3', get_info=ALL, connect_timeout=10)
    conn = Connection(server, user='cn=hnadservice,ou=海南核电有限公司,dc=cnnp,dc=com,dc=cn', password='mTQGi4JlIwQ', auto_bind=True, version=2)
    conn = Connection(server, user='hnadservice', password='mTQGi4JlIwQ', auto_bind=True, authentication="SIMPLE")
    conn.search('ou=海南核电有限公司,dc=cnnp,dc=com,dc=cn', '(uid=liushuo)', )
    entries = conn.entries
