import { http } from "@/utils/http";
import type {
  LoginResult,
  RefreshTokenResult,
  UserResult,
  UserPwdData,
  updatePwdData
} from "@/types/user";
import type { BaseResult, ResultList } from "@/types/base";
import { baseUrlApi } from "@/api/utils";
import { hashPwd } from "@/utils/hash";

/** 登录获取token */
export const getLogin = (data?: UserPwdData) => {
  data.password = hashPwd(data.password);
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
  data.password = hashPwd(data.password);
  return http.request<UserResult>("post", baseUrlApi("/base/auth"), {
    data
  });
};
/** 查看本人信息 */
export const getUserInfo = () => {
  return http.request<UserResult>("get", baseUrlApi("/base/userInfos"));
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
  data.oldPwd = hashPwd(data.oldPwd);
  data.newPwd = hashPwd(data.newPwd);
  return http.request<BaseResult>("post", baseUrlApi("/base/updatePwd"), {
    data
  });
};
/** 初始化密码 */
export const initPassword = (newPwd: string) => {
  newPwd = hashPwd(newPwd);
  return http.request<BaseResult>("post", baseUrlApi("/base/initPwd"), {
    data: { newPwd }
  });
};
