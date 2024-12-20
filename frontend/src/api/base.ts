import { http } from "@/utils/http";
import type {
  LoginResult,
  RefreshTokenResult,
  updatePwdData,
  UserPwdData,
  UserResult
} from "@/types/user";
import type { BaseResult, ResultList } from "@/types/base";
import { baseUrlApi } from "@/api/utils";

/** 登录获取token */
export const getLogin = (data?: UserPwdData) => {
  data.password = btoa(data.password);
  return http.request<LoginResult>("post", baseUrlApi("/base/accessToken"), {
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
/** 用户验证 */
export const auth = (data?: UserPwdData) => {
  data.password = btoa(data.password);
  return http.request<UserResult>("post", baseUrlApi("/base/auth"), {
    data
  });
};

/** 获取本人菜单 */
export const getAsyncRoutes = () => {
  return http.request<ResultList>("get", baseUrlApi("/base/userMenu"));
};
/** 查看本人API */
export const getApiList = () => {
  return http.request<ResultList>("get", baseUrlApi("/base/userApi"));
};
/** 更新本人密码 */
export const updatePassword = (data?: updatePwdData) => {
  return http.request<BaseResult>("post", baseUrlApi("/base/updatePwd"), {
    data
  });
};

export const getAreaList = () => {
  return http.request<ResultList>("get", baseUrlApi("/base/userArea"));
};
