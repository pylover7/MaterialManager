import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";
import type { ResultTable, Result } from "@/api/types";

export const createBorrowed = (data: object) => {
  return http.request<Result>("post", baseUrlApi("/home/create"), { data });
};

export const listBorrowed = (
  area: string,
  page: number,
  pageSize: number,
  borrowedStatus?: boolean,
  borrowWhether?: boolean,
  returnStatus?: boolean
) => {
  return http.request<ResultTable>("get", baseUrlApi("/home/list"), {
    params: {
      area,
      page,
      pageSize,
      borrowedStatus,
      borrowWhether,
      returnStatus
    }
  });
};

export const updateBorrowedInfo = (
  idList: number[],
  uuid: string,
  borrowStatus?: boolean,
  borrowWhether?: boolean,
  returnStatus?: boolean
) => {
  return http.request<Result>("post", baseUrlApi("/home/update"), {
    data: { borrowStatus, uuid, idList, borrowWhether, returnStatus }
  });
};

export const deleteBorrowed = (idList: number[]) => {
  return http.request<Result>("post", baseUrlApi("/home/delete"), {
    data: { idList }
  });
};
