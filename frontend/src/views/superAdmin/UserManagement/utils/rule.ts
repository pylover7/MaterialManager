import { reactive } from "vue";
import type { FormRules } from "element-plus";
import { isEmail, isPhone } from "@pureadmin/utils";

/** 自定义表单规则校验 */
export const formRules = reactive(<FormRules>{
  nickname: [{ required: true, message: "用户名称为必填项", trigger: "blur" }],
  username: [{ required: true, message: "职工号为必填项", trigger: "blur" }],
  password: [
    { required: true, message: "用户密码为必填项", trigger: "change" }
  ],
  phone: [
    { required: true, message: "手机号为必填项", trigger: "blur" },
    {
      validator: (rule, value, callback) => {
        if (value === "") {
          callback();
        } else if (!isPhone(value)) {
          callback(new Error("请输入正确的手机号码格式"));
        } else {
          callback();
        }
      },
      trigger: "blur"
      // trigger: "click" // 如果想在点击确定按钮时触发这个校验，trigger 设置成 click 即可
    }
  ],
  email: [
    { required: true, message: "邮箱为必填项", trigger: "blur" },
    {
      validator: (rule, value, callback) => {
        if (value === "") {
          callback();
        } else if (!isEmail(value)) {
          callback(new Error("请输入正确的邮箱格式"));
        } else {
          callback();
        }
      },
      trigger: "blur"
    }
  ],
  sex: [{ required: true, message: "性别为必填项", trigger: "blur" }]
});
