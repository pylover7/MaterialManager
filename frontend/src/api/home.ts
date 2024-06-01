import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";
import type { ResultTable, Result } from "@/api/types";

export const createBorrowed = (data: object) => {
  return http.request<Result>("post", baseUrlApi("/home/create"), { data });
};

export const listBorrowed = (area: string, page: number, pageSize: number) => {
  return http.request<ResultTable>("get", baseUrlApi("/home/list"), {
    params: {
      area,
      page,
      pageSize
    }
  });
};
