import { http } from "@/utils/http";
import { baseUrlApi } from "@/api/utils";
import type { BaseResult, ResultTable } from "@/types/base";
import type { DutyInfoResult, LatestNote } from "@/types/material";

type ResultDutyNote = BaseResult & {
  data: {
    note?: string;
  };
};

/** 接班 */
export const dutyOver = (area: string, metaType: string, data?: object) => {
  return http.request<DutyInfoResult>("post", baseUrlApi("/duty/dutyOver"), {
    data,
    params: {
      area,
      metaType
    }
  });
};
/** 获取值班备注 */
export const getDutyNote = (id: number) => {
  return http.request<ResultDutyNote>("get", baseUrlApi("/duty/getDutyNote"), {
    params: {
      id
    }
  });
};
/** 获取最新备注 */
export const getLatestNote = (area: string, metaType: string) => {
  return http.request<LatestNote>("get", baseUrlApi("/duty/latestNote"), {
    params: {
      area,
      metaType
    }
  });
};
/** 获取岗位值班人员信息 */
export const getDutyPerson = (area: string, metaType: string) => {
  return http.request<DutyInfoResult>("get", baseUrlApi("/duty/dutyPerson"), {
    params: { area, metaType }
  });
};
/** 获取接班7S清单 */
export const getDutyOverList = (area: string) => {
  return http.request<ResultTable>("get", baseUrlApi("/duty/7s/list"), {
    params: { area }
  });
};
/** 更新接班7S清单 */
export const updateDutyOverList = (area: string, data?: object) => {
  return http.request<BaseResult>("post", baseUrlApi("/duty/7s/update"), {
    data,
    params: { area }
  });
};
/** 删除接班7S清单 */
export const deleteDutyOverList = (id: string) => {
  return http.request<BaseResult>("delete", baseUrlApi("/duty/7s/delete"), {
    params: { id }
  });
};
/** 查询值班日志 */
export const getDutyLogList = (
  area: string,
  metaType: string,
  page: number,
  pageSize: number,
  data?: object
) => {
  return http.request<ResultTable>("post", baseUrlApi("/duty/logs/list"), {
    data,
    params: {
      area,
      metaType,
      page,
      pageSize
    }
  });
};
/** 删除值班日志 */
export const deleteDutyLogs = (idList: Array<number>) => {
  return http.request<BaseResult>("delete", baseUrlApi("/duty/logs/delete"), {
    data: idList
  });
};
