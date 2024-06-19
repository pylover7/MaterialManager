import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";
import type { BaseResult } from "@/types/base";
import type {
  AttentionResult,
  DutyInfoResult,
  LatestNote
} from "@/types/material";
import type { addResult, MaterialResult } from "@/types/admin";

export const getMaterialMeta = async (
  area: string,
  metaType: string,
  page?: number,
  pageSize?: number
) => {
  return http.request<MaterialResult>("get", baseUrlApi("/material/meta"), {
    params: {
      area,
      metaType,
      page,
      pageSize
    }
  });
};

export const getAllMaterialMeta = async (area: string, metaType: string) => {
  return http.request<MaterialResult>("get", baseUrlApi("/material/all_meta"), {
    params: {
      area,
      metaType
    }
  });
};

export const addMaterialMeta = async (data: object) => {
  return http.request<addResult>("post", baseUrlApi("/material/add_meta"), {
    data
  });
};

export const deleteMaterialMeta = async (idList: Array<number>) => {
  return http.request<BaseResult>("delete", baseUrlApi("/material/delete"), {
    data: {
      idList
    }
  });
};

export const getGlbAttentionList = () => {
  return http.request<AttentionResult>(
    "get",
    baseUrlApi("/material/glb_attention")
  );
};

export const getDutyInfo = (area: string, metaType: string) => {
  return http.request<DutyInfoResult>(
    "get",
    baseUrlApi("/material/duty_info"),
    { params: { area, metaType } }
  );
};

export const getLatestNote = (area: string, metaType: string) => {
  return http.request<LatestNote>("get", baseUrlApi("/material/latest_note"), {
    params: {
      area,
      metaType
    }
  });
};

export const dutyOver = (area: string, metaType: string, data?: object) => {
  return http.request<DutyInfoResult>(
    "post",
    baseUrlApi("/material/dutyOver"),
    {
      data,
      params: {
        area,
        metaType
      }
    }
  );
};
