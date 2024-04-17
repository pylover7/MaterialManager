import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";
import type { BaseResult } from "@/api/type";

export const testDB = async (data: object) => {
  return http.request<BaseResult>("post", baseUrlApi("admin/test_db"), {
    data
  });
};
