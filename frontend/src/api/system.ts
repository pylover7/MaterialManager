import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";
import type { ResultTable } from "@/types/base";

export const getLoginLogsList = () => {
  return http.request<ResultTable>(
    "get",
    baseUrlApi("/admin/system/getLoginLogs"),
    {}
  );
};
