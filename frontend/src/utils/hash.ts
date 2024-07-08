import { Md5 } from "ts-md5";

const hashPwd = (str: string): string => {
  return Md5.hashStr(str);
};

export { hashPwd };
