import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";
import type { BaseResult } from "@/types/base";
import type { dbInfoResult } from "@/types/superAdmin";

export const getDB = async () => {
  return http.request<dbInfoResult>("get", baseUrlApi("admin/get_db_info"));
};

export const testDB = async (data: object) => {
  return http.request<BaseResult>("post", baseUrlApi("admin/test_db_info"), {
    data
  });
};

export const setDB = async (data: object) => {
  return http.request<BaseResult>("post", baseUrlApi("admin/set_db_info"), {
    data
  });
};
