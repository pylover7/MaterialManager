import type { BaseResult } from "@/types/base";

export type LatestNote = BaseResult & {
  data: {
    note: string;
    area: string;
    type: string;
    dutyDate: string;
  };
};
export type AttentionResult = BaseResult & {
  data: [
    {
      id: number;
      uuid: string;
      note: string;
    }
  ];
};
export type DutyInfoResult = BaseResult & {
  data: {
    dutyPerson: string;
    dutyPersonDepart: string;
  };
};
export type MaterialItem = {
  id?: number;
  uuid?: string;
  name: string;
  model: string;
  type: string;
  area: string;
  position: string;
  number: number;
  nowNumber?: number;
  checking?: number;
  borrowing?: number;
  borrowed?: number;
  created_at?: string;
  updated_at?: string;
};
