export type BaseResult = {
  code: number;
  msg: string;
};
export type MaterialItem = {
  id?: number;
  uuid?: string;
  name: string;
  model: string;
  depart?: string;
  position: string;
  number: number;
  nowNumber?: number;
  checking?: number;
  borrowing?: number;
  borrowed?: number;
  created_at?: string;
  updated_at?: string;
};
