import type { BaseResult } from "@/types/base";

export type UserInfo = {
  /** uuid */
  uuid: string;
  /** 用户名 */
  username: string;
  /** 部门 */
  depart: string;
  /** 电话 */
  phone: string;
};

export type UserResult = BaseResult & {
  data: UserInfo;
};

export type LoginResult = BaseResult & {
  data: UserInfo & {
    /** 当前登陆用户的角色 */
    roles: [string];
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
