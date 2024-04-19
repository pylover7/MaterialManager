import type { BaseResult, MaterialItem } from "@/types/base";

export type addResult = BaseResult & {
  data: MaterialItem;
};
export type MaterialResult = BaseResult & {
  page: number;
  page_size: number;
  total: number;
  data: [MaterialItem];
};
