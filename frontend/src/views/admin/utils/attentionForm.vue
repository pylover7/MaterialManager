<script setup lang="ts">
import { reactive, ref } from "vue";
import { FormProps } from "./types";
import ReCol from "@/components/ReCol";

const attentionFormRef = ref();
function getRef() {
  return attentionFormRef.value;
}
defineExpose({ getRef });

const props = withDefaults(defineProps<FormProps>(), {
  formData: () => [
    {
      key: 1,
      value: ""
    }
  ]
});

const formItemRules = {
  required: true,
  message: "请输入内容",
  trigger: "blur"
};

const attList = reactive(props.formData);

const addAttention = () => {
  attList.push({
    key: Date.now(),
    value: ""
  });
};
</script>

<template>
  <el-form ref="attentionFormRef" :model="attList" label-width="82px">
    <el-form-item
      v-for="(item, index) in attList"
      :key="item.key"
      :prop="`formData.${index}.value`"
      :rules="formItemRules"
      :label="index.toString()"
    >
      <el-row :gutter="10">
        <el-col :span="20">
          <el-input v-model="item.value" />
        </el-col>
        <el-col :span="4">
          <el-button type="primary">删除</el-button>
        </el-col>
      </el-row>
    </el-form-item>
    <el-form-item>
      <el-button @click="addAttention">新建行</el-button>
    </el-form-item>
  </el-form>
</template>

<style scoped lang="scss"></style>
