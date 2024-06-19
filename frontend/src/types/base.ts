export type BaseResult = {
  code: number;
  msg: string;
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

export type User = {
  id: number;
  uuid: string;
  username: string;
  nickname: string;
  email: string;
  phone: string;
  avatar?: string;
  depart_id: number;
  is_superuser: boolean;
  remark: string;
  sex: number;
  status: number;
  created_at: string;
  updated_at: string;
  last_login: string;
};
