import { defineStore } from "pinia";
import { store } from "@/store";
import type { userType } from "./types";
import { routerArrays } from "@/layout/types";
import { resetRouter, router } from "@/router";
import { storageLocal } from "@pureadmin/utils";
import { useMultiTagsStoreHook } from "@/store/modules/multiTags";
import { type DataInfo, removeToken, setToken, userKey } from "@/utils/auth";
import type { LoginResult, RefreshTokenResult } from "@/types/user";
import { getLogin, refreshTokenApi } from "@/api/base";

export const useUserStore = defineStore({
  id: "pure-user",
  state: (): userType => ({
    nickname: storageLocal().getItem<DataInfo<number>>(userKey)?.nickname ?? "",
    // 用户名
    username: storageLocal().getItem<DataInfo<number>>(userKey)?.username ?? "",
    // 用户uuid
    uuid: storageLocal().getItem<DataInfo<number>>(userKey)?.uuid ?? "",
    // 用户部门
    depart: storageLocal().getItem<DataInfo<number>>(userKey)?.depart ?? "",
    // 页面级别权限
    roles: storageLocal().getItem<DataInfo<number>>(userKey)?.roles ?? [],
    // 是否勾选了登录页的免登录
    isRemembered: false,
    // 登录页的免登录存储几天，默认7天
    loginDay: 7
  }),
  actions: {
    /** 存储用户名 */
    SET_NICKNAME(nickname: string) {
      this.nickname = nickname;
    },
    SET_USERNAME(username: string) {
      this.username = username;
    },
    SET_UUID(uuid: string) {
      this.uuid = uuid;
    },
    /** 储存用户部门 */
    SET_DEPART(depart: string) {
      this.depart = depart;
    },
    /** 存储角色 */
    SET_ROLES(roles: Array<string>) {
      this.roles = roles;
    },
    /** 存储是否勾选了登录页的免登录 */
    SET_ISREMEMBERED(bool: boolean) {
      this.isRemembered = bool;
    },
    /** 设置登录页的免登录存储几天 */
    SET_LOGINDAY(value: number) {
      this.loginDay = Number(value);
    },
    /** 登入 */
    async loginByUsername(data) {
      return new Promise<LoginResult>((resolve, reject) => {
        getLogin(data)
          .then(data => {
            if (data) {
              setToken(data.data);
              resolve(data);
            }
          })
          .catch(error => {
            reject(error);
          });
      });
    },
    /** 前端登出（不调用接口） */
    logOut() {
      this.username = "";
      this.roles = [];
      removeToken();
      useMultiTagsStoreHook().handleTags("equal", [...routerArrays]);
      resetRouter();
      router.push("/login");
    },
    /** 刷新`token` */
    async handRefreshToken(data) {
      return new Promise<RefreshTokenResult>((resolve, reject) => {
        refreshTokenApi(data)
          .then(data => {
            if (data) {
              setToken(data.data);
              resolve(data);
            }
          })
          .catch(error => {
            reject(error);
          });
      });
    }
  }
});

export function useUserStoreHook() {
  return useUserStore(store);
}
