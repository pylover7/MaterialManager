import type { MaterialItem } from "@/types/material";

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
  reason: string;
  phone: string;
  depart: string;
  baseData: [MaterialItem];
};
