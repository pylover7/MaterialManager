export type BaseResult = {
  code: number;
  msg: string;
};

type MaterialItem = {
  id: number;
  uuid: string;
  name: string;
  model: string;
  depart: string;
  position: string;
  number: string;
  created_at: string;
  updated_at: string;
};

export type addResult = BaseResult & {
  data: MaterialItem;
};

export type MaterialResult = BaseResult & {
  page: number;
  pageSize: number;
  total: number;
  data: [MaterialItem];
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

export type LatestNote = BaseResult & {
  data: {
    note: string;
    depart: string;
    dutyDate: string;
  };
};

export type DutyInfoResult = BaseResult & {
  data: {
    dutyPerson: string;
    dutyPersonDepart: string;
  };
};
