import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";
import type {
  AttentionResult,
  DutyInfoResult,
  LatestNote,
  MaterialResult,
  addResult,
  BaseResult
} from "@/api/type";

export const getMaterialMeta = async (depart: string) => {
  return http.request<MaterialResult>("get", baseUrlApi("material/meta"), {
    params: {
      depart
    }
  });
};

export const addMaterialMeta = async (data: object) => {
  return http.request<addResult>("post", baseUrlApi("material/add_meta"), {
    data
  });
};

export const deleteMaterialMeta = async (idList: Array<number>) => {
  return http.request<BaseResult>("delete", baseUrlApi("material/delete"), {
    data: {
      idList
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
