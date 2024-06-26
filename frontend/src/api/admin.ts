import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";
import type { ResultTable, Result } from "@/api/types";

type ResultDutyNote = Result & {
  data: {
    note?: string;
  };
};

export const getDutyOverList = (area: string) => {
  return http.request<ResultTable>(
    "get",
    baseUrlApi("/material/duty_over_list/list"),
    {
      params: { area }
    }
  );
};

export const updateDutyOverList = (area: string, data?: object) => {
  return http.request<Result>(
    "post",
    baseUrlApi("/material/duty_over_list/update"),
    { data, params: { area } }
  );
};

export const deleteDutyOverList = (id: string) => {
  return http.request<Result>(
    "delete",
    baseUrlApi("/material/duty_over_list/delete"),
    { params: { id } }
  );
};

export const searchDutyLogs = (
  depart: string,
  page: number,
  pageSize: number,
  data?: object
) => {
  return http.request<ResultTable>(
    "post",
    baseUrlApi("/admin/dutyLogs/search"),
    {
      data,
      params: {
        depart,
        page,
        pageSize
      }
    }
  );
};

export const deleteDutyLogs = (idList: Array<number>) => {
  return http.request<Result>("delete", baseUrlApi("/admin/dutyLogs/delete"), {
    data: idList
  });
};

export const getDutyNote = (id: number) => {
  return http.request<ResultDutyNote>("get", baseUrlApi("/admin/getDutyNote"), {
    params: {
      id
    }
  });
};
