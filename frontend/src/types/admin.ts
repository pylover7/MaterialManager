import type { BaseResult } from "@/types/base";
import type { User } from "@/types/user";
import type { MaterialItem } from "@/types/material";

export type addResult = BaseResult & {
  data: MaterialItem;
};
export type MaterialResult = BaseResult & {
  page: number;
  pageSize: number;
  total: number;
  data: [MaterialItem];
};

export type BorrowedInfo = {
  id: number;
  uuid: string;
  username: string;
  nickname: string;
  userDepart: string;
  phone: string;
  reason: string;
  material: MaterialItem;
  borrowing: number;
  borrowTime: string;
  borrowApproveStatus: boolean;
  borrowApproveTime: string;
  borrowApproveUser: [User];
  borrowApproveWhether: boolean;
  returnApproveStatus: boolean;
  returnApproveTime: string;
  returnApproveUser: [User];
};
