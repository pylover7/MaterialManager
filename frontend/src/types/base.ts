export type BaseResult = {
  code: number;
  msg: string;
  data?: object;
  resetPwd?: boolean;
};

export type ResultList = {
  code: number;
  msg: string;
  data?: Array<any>;
};
export type ResultRoleAuth = BaseResult & {
  data: {
    menus: Array<number>;
    apis: Array<number>;
    areas: Array<number>;
  };
};
export type ResultTable = {
  success: boolean;
  data?: Array<any>;
  /** 总条目数 */
  total?: number;
  /** 每页显示条目个数 */
  pageSize?: number;
  /** 当前页数 */
  currentPage?: number;
};
