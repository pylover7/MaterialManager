import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";
import type { ResultTable } from "@/api/types";

export const getDutyOverList = (area: string) => {
  return http.request<ResultTable>(
    "get",
    baseUrlApi("/material/duty_over_list/list"),
    {
      params: { area }
    }
  );
};
