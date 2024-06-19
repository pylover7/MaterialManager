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
