import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";
import type { ResultTable } from "@/types/base";

export const getLoginLogsList = (
  currentPage: number,
  pageSize: number,
  username: string = null,
  status: string = null,
  loginTime: any[] = null
) => {
  return http.request<ResultTable>(
    "post",
    baseUrlApi("/admin/system/getLoginLogs"),
    {
      params: { currentPage, pageSize },
      data: {
        username,
        status,
        loginTime
      }
    }
  );
};

export const clearLoginLogs = () => {
  return http.request("get", baseUrlApi("/admin/system/clearLoginLogs"));
};
