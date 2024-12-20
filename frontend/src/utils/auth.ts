import Cookies from "js-cookie";
import { storageLocal } from "@pureadmin/utils";
import { useUserStoreHook } from "@/store/modules/user";
import { Md5 } from "ts-md5";

export interface DataInfo<T> {
  /** token */
  accessToken: string;
  /** `accessToken`的过期时间（时间戳） */
  expires: T;
  /** 用于调用刷新accessToken的接口时所需的token */
  refreshToken: string;
  /** 用户名 */
  username?: string;
  nickname?: string;
  /** uuid */
  uuid?: string;
  /** 部门 */
  depart?: string;
  /** 当前登陆用户的角色 */
  roles?: Array<string>;
}

export const userKey = "user-info";
export const TokenKey = "authorized-token";
/**
 * 通过`multiple-tabs`是否在`cookie`中，判断用户是否已经登录系统，
 * 从而支持多标签页打开已经登录的系统后无需再登录。
 * 浏览器完全关闭后`multiple-tabs`将自动从`cookie`中销毁，
 * 再次打开浏览器需要重新登录系统
 * */
export const multipleTabsKey = "multiple-tabs";

/** 获取`token` */
export function getToken(): DataInfo<number> {
  // 此处与`TokenKey`相同，此写法解决初始化时`Cookies`中不存在`TokenKey`报错
  return Cookies.get(TokenKey)
    ? JSON.parse(Cookies.get(TokenKey))
    : storageLocal().getItem(userKey);
}

/**
 * @description 设置`token`以及一些必要信息并采用无感刷新`token`方案
 * 无感刷新：后端返回`accessToken`（访问接口使用的`token`）、`refreshToken`（用于调用刷新`accessToken`的接口时所需的`token`，`refreshToken`的过期时间（比如30天）应大于`accessToken`的过期时间（比如2小时））、`expires`（`accessToken`的过期时间）
 * 将`accessToken`、`expires`这两条信息放在key值为authorized-token的cookie里（过期自动销毁）
 * 将`username`、`roles`、`refreshToken`、`expires`这四条信息放在key值为`user-info`的localStorage里（利用`multipleTabsKey`当浏览器完全关闭后自动销毁）
 */
export function setToken(data: DataInfo<Date>) {
  let expires = 0;
  const { accessToken, refreshToken } = data;
  const { isRemembered, loginDay } = useUserStoreHook();
  expires = new Date(data.expires).getTime(); // 如果后端直接设置时间戳，将此处代码改为expires = data.expires，然后把上面的DataInfo<Date>改成DataInfo<number>即可
  const cookieString = JSON.stringify({ accessToken, expires });

  expires > 0
    ? Cookies.set(TokenKey, cookieString, {
        expires: (expires - Date.now()) / 86400000
      })
    : Cookies.set(TokenKey, cookieString);

  Cookies.set(
    multipleTabsKey,
    "true",
    isRemembered
      ? {
          expires: loginDay
        }
      : {}
  );

  function setUserKey(
    nickname: string,
    username: string,
    uuid: string,
    depart: string,
    roles: Array<string>
  ) {
    useUserStoreHook().SET_NICKNAME(nickname);
    useUserStoreHook().SET_USERNAME(username);
    useUserStoreHook().SET_UUID(uuid);
    useUserStoreHook().SET_DEPART(depart);
    useUserStoreHook().SET_ROLES(roles);
    storageLocal().setItem(userKey, {
      refreshToken,
      expires,
      username,
      nickname,
      uuid,
      depart,
      roles
    });
  }

  if (data.username && data.roles && data.nickname) {
    const { nickname, username, uuid, depart, roles } = data;
    setUserKey(nickname, username, uuid, depart, roles);
  } else {
    const nickname =
      storageLocal().getItem<DataInfo<number>>(userKey)?.nickname ?? "";
    const username =
      storageLocal().getItem<DataInfo<number>>(userKey)?.username ?? "";
    const uuid = storageLocal().getItem<DataInfo<number>>(userKey)?.uuid ?? "";
    const roles =
      storageLocal().getItem<DataInfo<number>>(userKey)?.roles ?? [];
    const depart =
      storageLocal().getItem<DataInfo<number>>(userKey)?.depart ?? "";
    setUserKey(nickname, username, uuid, depart, roles);
  }
}

/** 删除`token`以及key值为`user-info`的localStorage信息 */
export function removeToken() {
  Cookies.remove(TokenKey);
  Cookies.remove(multipleTabsKey);
  storageLocal().removeItem(userKey);
}

/** 格式化token（jwt格式） */
export const formatToken = (token: string): string => {
  return "Bearer " + token;
};

/** md5 加密 */
export const hashPwd = (str: string): string => {
  return Md5.hashStr(str);
};
