import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

export type MaterialResult = {
  code: number;
  msg: string;
  page: number;
  pageSize: number;
  total: number;
  data: [
    {
      id: number;
      uuid: string;
      name: string;
      model: string;
      depart: string;
      position: string;
      number: string;
      created_at: string;
      updated_at: string;
    }
  ];
};

export type AttentionResult = {
  code: number;
  msg: string;
  data: [
    {
      id: number;
      uuid: string;
      note: string;
    }
  ];
};

type LatestNote = {
  code: number;
  msg: string;
  data: {
    note: string;
    depart: string;
    dutyDate: string;
  };
};

export type DutyInfoResult = {
  code: number;
  msg: string;
  data: {
    dutyPerson: string;
    dutyPersonDepart: string;
  };
};

export const getMaterialMeta = async (depart: string) => {
  return http.request<MaterialResult>("get", baseUrlApi("material/meta"), {
    params: {
      depart
    }
  });
};

export const getGlbAttentionList = () => {
  return http.request<AttentionResult>(
    "get",
    baseUrlApi("material/glb_attention")
  );
};

export const getGlbDutyInfo = () => {
  return http.request<DutyInfoResult>(
    "get",
    baseUrlApi("material/glb_duty_info")
  );
};

export const getLatestNote = () => {
  return http.request<LatestNote>(
    "get",
    baseUrlApi("material/glb_latest_note")
  );
};

export const dutyOver = (data?: object) => {
  return http.request<DutyInfoResult>("post", baseUrlApi("material/dutyOver"), {
    data
  });
};
