from ldap3 import Server, Connection, SUBTREE
from ldap3.core.exceptions import LDAPException

from app.settings import settings


class LDAPAuthentication:
    def __init__(self):
        self.URL = "ldap://192.168.31.83"
        self.BASEDN = "dc=cnnp,dc=com"
        self.ctx = None

    def LDAP_connect(self):
        try:
            self.ctx = Connection(Server(self.URL, 389), auto_bind=True)
        except LDAPException as e:
            print(f"连接失败: {e}")

    def getUserDN(self, uid):
        userDN = ""
        self.LDAP_connect()
        try:
            self.ctx.search(self.BASEDN, f"(uid={uid})", search_scope=SUBTREE)
            if not self.ctx.entries:
                print("未找到该用户")
            else:
                for entry in self.ctx.entries:
                    userDN += str(entry.entry_dn) + "," + self.BASEDN
        except Exception as e:
            print(f"查找用户时产生异常: {e}")
        return userDN

    def authenticate(self, UID, password):
        valid = False
        userDN = self.getUserDN(UID)
        if not userDN:
            return valid
        try:
            self.ctx = Connection(Server(self.URL), user=userDN, password=password, auto_bind=True)
            print(f"{userDN} 验证通过")
            valid = True
        except LDAPException as e:
            print(f"{userDN} 验证失败: {e}")
            valid = False
        return valid

    def closeCtx(self):
        if self.ctx:
            self.ctx.unbind()
            print("LDAP连接已关闭")


ldap_auth = LDAPAuthentication()

if __name__ == '__main__':
    print(ldap_auth.authenticate('some_uid', 'some_password'))
    ldap_auth.closeCtx()
