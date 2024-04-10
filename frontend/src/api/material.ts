import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

export type MaterialResult = {
  code: number;
  msg: string;
  data: [
    {
      id: number;
      uuid: string;
      name: string;
      model: string;
      position: string;
      number: string;
      created_at: string;
      updated_at: string;
    }
  ];
};

export type NoteResult = {
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

export const getGlbList = () => {
  return http.request<MaterialResult>("get", baseUrlApi("material/glb_list"));
};

export const getGlbNoteList = () => {
  return http.request<NoteResult>("get", baseUrlApi("material/glb_note"));
};
