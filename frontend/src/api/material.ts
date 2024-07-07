import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";
import type { BaseResult, ResultTable } from "@/types/base";
import type { addResult, MaterialResult } from "@/types/admin";

/** 添加或修改物资源数据 */
export const addMaterialMeta = async (data: object) => {
  return http.request<addResult>("post", baseUrlApi("/material/addMeta"), {
    data
  });
};
/** 删除物资源数据 */
export const deleteMaterialMeta = async (idList: Array<number>) => {
  return http.request<BaseResult>("delete", baseUrlApi("/material/delete"), {
    data: {
      idList
    }
  });
};
/** 获取物资源数据 */
export const getMaterialMeta = async (
  area: string,
  metaType: string,
  page?: number,
  pageSize?: number
) => {
  return http.request<MaterialResult>("get", baseUrlApi("/material/meta"), {
    params: {
      area,
      metaType,
      page,
      pageSize
    }
  });
};
/** 获取所有物资源数据 */
export const getAllMaterialMeta = async (area: string, metaType: string) => {
  return http.request<MaterialResult>("get", baseUrlApi("/material/allMeta"), {
    params: {
      area,
      metaType
    }
  });
};

/** 新增物资送检信息 */
export const addCheckMaterial = (data: object) => {
  return http.request<BaseResult>("post", baseUrlApi("/material/checked/add"), {
    data
  });
};
/** 删除物资送检信息 */
export const deleteCheckedMaterial = (idList: Array<number>) => {
  return http.request<BaseResult>(
    "delete",
    baseUrlApi("/material/checked/delete"),
    {
      data: {
        idList
      }
    }
  );
};
/** 获取物资送检信息 */
export const getCheckedMaterial = (
  area: string,
  metaType: string,
  returnStatus: boolean,
  page: number,
  pageSize: number
) => {
  return http.request<ResultTable>("get", baseUrlApi("/material/checked/get"), {
    params: {
      area,
      metaType,
      returnStatus,
      page,
      pageSize
    }
  });
};
/** 归还送检物资 */
export const updateCheckedMaterial = (data: object) => {
  return http.request<BaseResult>(
    "post",
    baseUrlApi("/material/checked/update"),
    {
      data
    }
  );
};

/** 创建借用信息 */
export const addBorrowed = (data: object) => {
  return http.request<BaseResult>(
    "post",
    baseUrlApi("/material/borrowed/add"),
    { data }
  );
};
/** 删除借用信息 */
export const deleteBorrowed = (idList: number[]) => {
  return http.request<BaseResult>(
    "post",
    baseUrlApi("/material/borrowed/delete"),
    {
      data: { idList }
    }
  );
};
/** 获取借用信息 */
export const listBorrowed = (
  area: string,
  page: number,
  pageSize: number,
  borrowedStatus?: boolean,
  borrowWhether?: boolean,
  returnStatus?: boolean
) => {
  return http.request<ResultTable>(
    "get",
    baseUrlApi("/material/borrowed/list"),
    {
      params: {
        area,
        page,
        pageSize,
        borrowedStatus,
        borrowWhether,
        returnStatus
      }
    }
  );
};
/** 更新借用信息 */
export const updateBorrowedInfo = (
  idList: number[],
  uuid: string,
  borrowStatus?: boolean,
  borrowWhether?: boolean,
  returnStatus?: boolean
) => {
  return http.request<BaseResult>(
    "post",
    baseUrlApi("/material/borrowed/update"),
    {
      data: { borrowStatus, uuid, idList, borrowWhether, returnStatus }
    }
  );
};
