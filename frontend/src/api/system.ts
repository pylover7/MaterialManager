import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

type Result = {
  code: number;
  msg: string;
  data?: object;
};

type ResultList = {
  code: number;
  msg: string;
  data?: Array<any>;
};

type ResultRoleAuth = Result & {
  data: {
    menus: Array<number>;
    apis: Array<number>;
  };
};

type ResultTable = {
  success: boolean;
  data?: Array<any>;
  /** 总条目数 */
  total?: number;
  /** 每页显示条目个数 */
  pageSize?: number;
  /** 当前页数 */
  currentPage?: number;
};

/** 获取系统管理-用户管理列表 */
export const getUserList = (
  currentPage: number,
  pageSize: number,
  username: string = null,
  phone: string = null
) => {
  return http.request<ResultTable>("get", baseUrlApi("/user/list"), {
    params: {
      currentPage,
      pageSize,
      username,
      phone
    }
  });
};

/** 新增用户 */
export const addUser = (data?: object) => {
  return http.request<Result>("post", baseUrlApi("/user/add"), { data });
};

/** 系统管理-用户管理-获取所有角色列表 */
export const getAllRoleList = () => {
  // return http.request<Result>("get", "/list-all-role");
  return {
    code: 200,
    msg: "ok",
    data: [
      { id: 1, name: "超级管理员" },
      { id: 2, name: "普通角色" }
    ]
  };
};

/** 系统管理-用户管理-根据userId，获取对应角色id列表（userId：用户id） */
export const getRoleIds = (data?: object) => {
  // return http.request<Result>("post", "/list-role-ids", { data });
  console.log(data);
  return {
    code: 200,
    msg: "ok",
    data: [1]
  };
};

/** 获取系统管理-角色管理列表 */
export const getRoleList = (
  currentPage: number,
  pageSize: number,
  data?: object
) => {
  return http.request<ResultTable>("post", baseUrlApi("/role/list"), {
    data,
    params: { currentPage, pageSize }
  });
};

/** 新增角色 */
export const addRole = (data?: object) => {
  return http.request<ResultList>("post", baseUrlApi("/role/add"), { data });
};

/** 修改角色 */
export const updateRole = (data?: object) => {
  return http.request<ResultList>("post", baseUrlApi("/role/update"), { data });
};

/** 删除角色 */
export const deleteRole = (id: number, name: string) => {
  return http.request<ResultList>("delete", baseUrlApi("/role/delete"), {
    params: { id, name }
  });
};

/** 获取角色管理-权限-菜单权限和API权限-根据角色 id 查对应菜单 */
export const getRoleAuth = (id: number) => {
  return http.request<ResultRoleAuth>("get", baseUrlApi("/role/getRoleAuth"), {
    params: { id }
  });
};

/** 更新角色权限 */
export const updateRoleAuth = (data?: object) => {
  return http.request<Result>("post", baseUrlApi("/role/updateRoleAuth"), {
    data
  });
};

/** 获取API列表 */
export const getApiList = () => {
  return http.request<ResultTable>("get", baseUrlApi("/api/list"));
};

/** 获取系统管理-菜单列表 */
export const getMenuList = () => {
  return http.request<ResultList>("get", baseUrlApi("/menu/list"));
};

/** 新增菜单 */
export const addMenu = (data?: object) => {
  return http.request<ResultList>("post", baseUrlApi("/menu/add"), { data });
};

/** 修改菜单 */
export const updateMenu = (data?: object) => {
  return http.request<ResultList>("post", baseUrlApi("/menu/update"), { data });
};

/** 删除菜单 */
export const deleteMenu = (id: number, name: string) => {
  return http.request<ResultList>("delete", baseUrlApi("/menu/delete"), {
    params: { id, name }
  });
};

/** 获取系统管理-部门管理列表 */
export const getDeptList = () => {
  return http.request<ResultList>("get", baseUrlApi("/depart/list"));
};

/** 新增部门 */
export const addDepart = (data?: object) => {
  return http.request<ResultList>("post", baseUrlApi("/depart/add"), { data });
};

/** 修改部门 */
export const updateDepart = (data?: object) => {
  return http.request<ResultList>("post", baseUrlApi("/depart/update"), {
    data
  });
};

/** 删除部门 */
export const deleteDepart = (id: number, name: string) => {
  return http.request<ResultList>("delete", baseUrlApi("/depart/delete"), {
    params: { id, name }
  });
};

/** 获取系统监控-在线用户列表 */
export const getOnlineLogsList = (data?: object) => {
  return http.request<ResultTable>("post", "/online-logs", { data });
};

/** 获取系统监控-登录日志列表 */
export const getLoginLogsList = (data?: object) => {
  return http.request<ResultTable>("post", "/login-logs", { data });
};

/** 获取系统监控-操作日志列表 */
export const getOperationLogsList = (data?: object) => {
  return http.request<ResultTable>("post", "/operation-logs", { data });
};

/** 获取系统监控-系统日志列表 */
export const getSystemLogsList = (data?: object) => {
  return http.request<ResultTable>("post", "/system-logs", { data });
};

/** 获取系统监控-系统日志-根据 id 查日志详情 */
export const getSystemLogsDetail = (data?: object) => {
  return http.request<ResultList>("post", "/system-logs-detail", { data });
};
