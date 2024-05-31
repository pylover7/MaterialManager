import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";
import type { ResultTable, Result } from "@/api/types";

export const createBorrowed = (data: object) => {
  return http.request<Result>("post", baseUrlApi("/home/create"), { data });
};

export const listBorrowed = (page: number, pageSize: number) => {
  return http.request<ResultTable>("post", baseUrlApi("/home/list"), {
    params: {
      page,
      pageSize
    }
  });
};
