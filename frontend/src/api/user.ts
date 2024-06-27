import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";
import type { RefreshTokenResult, LoginResult, UserResult } from "@/types/user";

/** 登录 */
export const getLogin = (data?: object) => {
  return http.request<LoginResult>("post", baseUrlApi("/base/accessToken"), {
    data
  });
};

/** 获取用户信息 */
export const getUserInfo = (data?: object) => {
  return http.request<UserResult>("post", baseUrlApi("/base/userinfo"), {
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
