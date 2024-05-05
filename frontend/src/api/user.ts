import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

export type UserResult = {
  code: number;
  success: boolean;
  msg: string;
  data: {
    /** 用户名 */
    username: string;
    /** 部门 */
    depart: string;
    /** 当前登陆用户的角色 */
    roles: Array<number>;
    /** `token` */
    accessToken: string;
    /** 用于调用刷新`accessToken`的接口时所需的`token` */
    refreshToken: string;
    /** `accessToken`的过期时间（格式'xxxx/xx/xx xx:xx:xx'） */
    expires: Date;
  };
};

export type RefreshTokenResult = {
  code: number;
  success: boolean;
  msg: string;
  data: {
    /** `token` */
    accessToken: string;
    /** 用于调用刷新`accessToken`的接口时所需的`token` */
    refreshToken: string;
    /** `accessToken`的过期时间（格式'xxxx/xx/xx xx:xx:xx'） */
    expires: Date;
  };
};

/** 登录 */
export const getLogin = (data?: object) => {
  return http.request<UserResult>("post", baseUrlApi("/base/accessToken"), {
    data
  });
};

/** 刷新token */
export const refreshTokenApi = (data?: object) => {
  return http.request<RefreshTokenResult>(
    "post",
    baseUrlApi("/base/refreshToken"),
    { data }
  );
};
