import type { MaterialItem } from "@/types/base";

export type userInfo = {
  account: string;
  password: string;
  name: string;
  phone: string;
  depart: string;
};

export type borrowInfo = {
  uuid: string;
  username: string;
  phone: string;
  depart: string;
  baseData: [MaterialItem];
};
