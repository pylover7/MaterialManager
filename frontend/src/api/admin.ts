import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";
import type { dbInfoResult } from "@/types/superAdmin";
import type {
  BaseResult,
  ResultList,
  ResultRoleAuth,
  ResultTable
} from "@/types/base";

/** 获取API列表 */
export const getApiList = () => {
  return http.request<ResultTable>("get", baseUrlApi("/admin/api/list"));
};

/** 新增部门 */
export const addDepart = (data?: object) => {
  return http.request<ResultList>("post", baseUrlApi("/admin/depart/add"), {
    data
  });
};
/** 删除部门 */
export const deleteDepart = (id: number, name: string) => {
  return http.request<ResultList>(
    "delete",
    baseUrlApi("/admin/depart/delete"),
    {
      params: { id, name }
    }
  );
};
/** 获取部门列表 */
export const getDeptList = () => {
  return http.request<ResultList>("get", baseUrlApi("/admin/depart/list"));
};
/** 修改部门 */
export const updateDepart = (data?: object) => {
  return http.request<ResultList>("post", baseUrlApi("/admin/depart/update"), {
    data
  });
};

/** 新增菜单 */
export const addMenu = (data?: object) => {
  return http.request<ResultList>("post", baseUrlApi("/admin/menu/add"), {
    data
  });
};
/** 删除菜单 */
export const deleteMenu = (id: number, name: string) => {
  return http.request<ResultList>("delete", baseUrlApi("/admin/menu/delete"), {
    params: { id, name }
  });
};
/** 获取菜单列表 */
export const getMenuList = () => {
  return http.request<ResultList>("get", baseUrlApi("/admin/menu/list"));
};
/** 修改菜单 */
export const updateMenu = (data?: object) => {
  return http.request<ResultList>("post", baseUrlApi("/admin/menu/update"), {
    data
  });
};

/** 新增角色 */
export const addRole = (data?: object) => {
  return http.request<ResultList>("post", baseUrlApi("/admin/role/add"), {
    data
  });
};
/** 删除角色 */
export const deleteRole = (id: number, name: string) => {
  return http.request<ResultList>("delete", baseUrlApi("/admin/role/delete"), {
    params: { id, name }
  });
};
/** 获取角色列表 */
export const getRoleList = (
  currentPage: number,
  pageSize: number,
  data?: object
) => {
  return http.request<ResultTable>("post", baseUrlApi("/admin/role/list"), {
    data,
    params: { currentPage, pageSize }
  });
};
/** 获取角色对应菜单 */
export const getRoleAuth = (id: number) => {
  return http.request<ResultRoleAuth>(
    "get",
    baseUrlApi("/admin/role/getRoleAuth"),
    {
      params: { id }
    }
  );
};
/** 修改角色 */
export const updateRole = (data?: object) => {
  return http.request<ResultList>("post", baseUrlApi("/admin/role/update"), {
    data
  });
};
/** 设置默认角色 */
export const setDefaultRole = (id: number) => {
  return http.request<BaseResult>(
    "get",
    baseUrlApi("/admin/role/setDefaultRole"),
    {
      params: { id }
    }
  );
};

/** 更新角色权限 */
export const updateRoleAuth = (data?: object) => {
  return http.request<BaseResult>(
    "post",
    baseUrlApi("/admin/role/updateRoleAuth"),
    {
      data
    }
  );
};

/** 新增用户 */
export const addUser = (role: number, data?: object) => {
  return http.request<BaseResult>("post", baseUrlApi("/admin/user/add"), {
    data,
    params: { role }
  });
};
/** 删除用户 */
export const deleteUser = (id: number, name: string) => {
  return http.request<BaseResult>("delete", baseUrlApi("/admin/user/delete"), {
    params: { id, name }
  });
};
/** 获取用户列表 */
export const getUserList = (
  currentPage: number,
  pageSize: number,
  username: string = null,
  nickname: string = null
) => {
  return http.request<ResultTable>("get", baseUrlApi("/admin/user/list"), {
    params: {
      currentPage,
      pageSize,
      username,
      nickname
    }
  });
};
/** 获取Ldap用户列表 */
export const getLdapUserList = (filterKey: string, filterValue: string) => {
  return http.request<ResultList>(
    "get",
    baseUrlApi("/admin/user/listLdapUser"),
    {
      params: {
        filterKey,
        filterValue
      }
    }
  );
};
/** 更新用户状态 */
export const updateUserStatus = (data?: object) => {
  return http.request<BaseResult>(
    "post",
    baseUrlApi("/admin/user/updateStatus"),
    {
      data
    }
  );
};
/** 更新用户角色信息 */
export const updateUserRole = (id: number, data?: object) => {
  return http.request<BaseResult>(
    "post",
    baseUrlApi("/admin/user/updateRoles"),
    {
      data,
      params: { id }
    }
  );
};

/** 获取数据库信息 */
export const getDB = async () => {
  return http.request<dbInfoResult>("get", baseUrlApi("/admin/system/db/get"));
};
/** 测试数据库信息 */
export const testDB = async (data: object) => {
  return http.request<BaseResult>("post", baseUrlApi("/admin/system/db/test"), {
    data
  });
};
/** 设置数据库信息 */
export const setDB = async (data: object) => {
  return http.request<BaseResult>("post", baseUrlApi("/admin/system/db/set"), {
    data
  });
};

/** 新增区域 **/
export const addArea = (name: string, code: string, remark?: string) => {
  return http.request<BaseResult>("post", baseUrlApi("/admin/area/add"), {
    data: {
      name,
      code,
      remark
    }
  });
};

/** 删除区域 **/
export const deleteArea = (id: number) => {
  return http.request<BaseResult>("delete", baseUrlApi("/admin/area/delete"), {
    params: { id }
  });
};

/** 更新区域 **/
export const updateArea = (data?: object) => {
  return http.request<BaseResult>("put", baseUrlApi("/admin/area/update"), {
    data
  });
};

/* 更新区域状态 **/
export const updateAreaStatus = (id: number, status: number) => {
  return http.request<BaseResult>(
    "get",
    baseUrlApi("/admin/area/updateStatus"),
    {
      params: { id, status }
    }
  );
};

/** 获取区域列表 **/
export const getAreaList = (
  currentPage: number,
  pageSize: number,
  name: string = null,
  code: string = null
) => {
  return http.request<ResultTable>("get", baseUrlApi("/admin/area/list"), {
    params: {
      currentPage,
      pageSize,
      name,
      code
    }
  });
};

/** 获取所有区域 **/
export const getAllArea = () => {
  return http.request<ResultList>("get", baseUrlApi("/admin/area/all"));
};
