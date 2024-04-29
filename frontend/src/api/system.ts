import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

type Result = {
  code: number;
  msg: string;
  data?: Array<any>;
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
export const getUserList = (data?: object) => {
  // return http.request<ResultTable>("post", "/user", { data });
  console.log(data);
  return {
    code: 200,
    msg: "ok",
    data: [
      {
        avatar: "https://avatars.githubusercontent.com/u/44761321",
        username: "admin",
        nickname: "小铭",
        phone: "15888886789",
        email: "zzz",
        sex: 0,
        id: 1,
        status: 1,
        dept: {
          // 部门id
          id: 103,
          // 部门名称
          name: "研发部门"
        },
        remark: "管理员",
        createTime: 1605456000000
      },
      {
        avatar: "https://avatars.githubusercontent.com/u/52823142",
        username: "common",
        nickname: "小林",
        phone: "18288882345",
        email: "xxx",
        sex: 1,
        id: 2,
        status: 1,
        dept: {
          id: 105,
          name: "测试部门"
        },
        remark: "普通用户",
        createTime: 1605456000000
      }
    ],
    total: 2,
    pageSize: 10,
    currentPage: 1
  };
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

/** 获取系统管理-菜单列表 */
export const getMenuList = () => {
  return http.request<Result>("get", baseUrlApi("/menu/list"));
};

/** 新增菜单 */
export const addMenu = (data?: object) => {
  return http.request<Result>("post", baseUrlApi("/menu/add"), { data });
};

/** 修改菜单 */
export const updateMenu = (data?: object) => {
  return http.request<Result>("post", baseUrlApi("/menu/update"), { data });
};

/** 删除菜单 */
export const deleteMenu = (id: number, name: string) => {
  return http.request<Result>("delete", baseUrlApi("/menu/delete"), {
    params: { id, name }
  });
};

/** 获取系统管理-部门管理列表 */
export const getDeptList = () => {
  return http.request<Result>("get", baseUrlApi("/depart/list"));
};

/** 新增部门 */
export const addDepart = (data?: object) => {
  return http.request<Result>("post", baseUrlApi("/depart/add"), { data });
};

/** 修改部门 */
export const updateDepart = (data?: object) => {
  return http.request<Result>("post", baseUrlApi("/depart/update"), { data });
};

/** 删除部门 */
export const deleteDepart = (id: number, name: string) => {
  return http.request<Result>("delete", baseUrlApi("/depart/delete"), {
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
  return http.request<Result>("post", "/system-logs-detail", { data });
};

/** 获取角色管理-权限-菜单权限 */
export const getRoleMenu = (data?: object) => {
  // return http.request<Result>("post", "/role-menu", { data });
  console.log(data);
  return {
    code: 200,
    msg: "ok",
    data: [
      {
        parentId: 0,
        id: 100,
        menuType: 0, // 菜单类型（0代表菜单、1代表iframe、2代表外链、3代表按钮）
        title: "menus.pureExternalPage"
      },
      {
        parentId: 100,
        id: 101,
        menuType: 0,
        title: "menus.pureExternalDoc"
      },
      {
        parentId: 101,
        id: 102,
        menuType: 2,
        title: "menus.pureExternalLink"
      },
      {
        parentId: 101,
        id: 103,
        menuType: 2,
        title: "menus.pureUtilsLink"
      },
      {
        parentId: 100,
        id: 104,
        menuType: 1,
        title: "menus.pureEmbeddedDoc"
      }
    ]
  };
};

/** 获取角色管理-权限-菜单权限-根据角色 id 查对应菜单 */
export const getRoleMenuIds = (data?: object) => {
  // return http.request<Result>("post", "/role-menu-ids", { data });
  console.log(data);
  return {
    code: 200,
    msg: "ok",
    data: [
      100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 200, 201, 202, 203,
      204, 205, 300, 301, 302, 303, 304, 400, 401, 402, 403, 404, 500, 501, 502,
      503
    ]
  };
};
