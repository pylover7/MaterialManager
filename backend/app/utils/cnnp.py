from typing import Tuple

from fastapi import HTTPException
from ldap3 import Server, Connection, ALL, SUBTREE

from app.utils.log import logger
from app.schemas.users import UserLdap, UserCreate
from app.settings import settings


class LDAPAuthentication:
    def __init__(self):
        self.server = Server(settings.LDAP_HOST, get_info=ALL, connect_timeout=10)
        self.conn = Connection(self.server, user=settings.LDAP_USER, password=settings.LDAP_PWD)
        self.attr = ["company", "department", "employeeID", "mobile", "mail", "distinguishedName", "sAMAccountName", "name"]

    def get_user_info(self, username: str) -> UserLdap:
        if not settings.DEV:
            self.conn.bind()
            if self.conn.search(settings.LDAP_BASE, f'(sAMAccountName={username})', SUBTREE, attributes=self.attr):
                user = self.conn.entries[0]
                self.conn.unbind()
                return UserLdap(
                    company=user.company.value,
                    department=user.department.value,
                    employeeID=user.employeeID.value,
                    mobile=user.mobile.value,
                    mail=user.mail.value,
                    dn=user.distinguishedName.value,
                    sAMAccountName=user.sAMAccountName.value,
                    name=user.name.value,
                )
            else:
                self.conn.unbind()
                raise HTTPException(status_code=400, detail="用户不存在")
        else:
            return UserLdap(
                company="海南核电有限公司",
                department="运行一处运行值",
                employeeID="10000",
                mobile="13800138000",
                mail="EMAIL",
                dn="cn=liushuo,ou=海南核电有限公司,dc=cnnp,dc=com,dc=cn",
                sAMAccountName="liushuo",
                name="张三"
            )


    def authenticate(self, username: str, password: str) -> Tuple[UserLdap | None, bool]:
        if settings.DEV:
            user = self.get_user_info(username)
            return user, True
        else:
            user = self.get_user_info(username)
            try:
                conn = Connection(self.server, user=user.dn, password=password, auto_bind=True)
                conn.unbind()
                return user, True
            except Exception as e:
                logger.error(f"LDAP认证失败: {e}")
                return user, False

    def getUserList(self, fiterKey: str, fiterValue: str) -> list[UserLdap]:
        self.conn.bind()
        if self.conn.search(settings.LDAP_BASE, f'({fiterKey}={fiterValue})', attributes=self.attr):
            userList = self.conn.entries
            for user in userList:
                userList[userList.index(user)] = UserCreate(
                    company=user.company.value,
                    department=user.department.value,
                    employeeID=user.employeeID.value,
                    mobile=user.mobile.value,
                    email=user.mail.value,
                    username=user.sAMAccountName.value,
                    nickname=user.name.value,
                ).model_dump()
            self.conn.unbind()
            return userList
        else:
            self.conn.unbind()
            return []



ldap_auth = LDAPAuthentication()


if __name__ == '__main__':
    from ldap3 import SUBTREE, ALL_ATTRIBUTES
    # server = Server('10.20.21.2', get_info=ALL, connect_timeout=10)
    server = Server('panel2.pylover.net.', get_info=ALL, connect_timeout=10)
    conn = Connection(server, user='uid=test,ou=people,dc=eryajf,dc=net', password='test1234', auto_bind=True, authentication="SIMPLE")
    conn.search('ou=海南核电有限公司,dc=cnnp,dc=com,dc=cn', '(sAMAccountName=liushuo)', SUBTREE, attributes=ALL_ATTRIBUTES)  # 获取所有信息
    attr = ["cn", "company", "department", "employeeID", "mobile", "name", "mail", "distinguishedName"]
    conn.search('ou=海南核电有限公司,dc=cnnp,dc=com,dc=cn', '(sAMAccountName=liushuo)', SUBTREE, attributes=attr)
    entry = conn.entries[0]
    conn.unbind()
    """
    cn: 姓名
    company: 公司
    department: 运行一处运行值
    employeeID: 工号
    mobile: 手机
    name: 姓名
    mail: 邮箱
    distinguishedName: cn=xxx,ou=xxx,dc=cnnp,dc=com,dc=cn
    """

