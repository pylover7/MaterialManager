import type { BaseResult } from "@/types/base";

export type dbInfoResult = BaseResult & {
  data: dbInfoType;
};

export type dbInfoType = object & {
  start: string;
  host: string;
  port: number;
  username: string;
  password: string;
  database: string;
};
