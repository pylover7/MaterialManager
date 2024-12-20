<script lang="ts" setup>
import { reactive, ref } from "vue";
import { FormItemProps, FormProps } from "./types";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Minus from "@iconify-icons/ep/semi-select";
import Add from "@iconify-icons/fluent/add-12-filled";
import { successNotification } from "@/utils/notification";
import { deleteDutyOverList } from "@/api/duty";

const attentionFormRef = ref();

function getRef() {
  return attentionFormRef.value;
}

defineExpose({ getRef });

const props = withDefaults(defineProps<FormProps>(), {
  formData: () => [
    {
      key: 1,
      content: ""
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
    content: ""
  });
};
const removeAttItem = (item: FormItemProps) => {
  deleteDutyOverList(item.id).then(() => {
    const index = attList.indexOf(item);
    if (index !== -1) {
      attList.splice(index, 1);
    }
    successNotification("删除成功");
  });
};

const editAble = ref(true);

const editForm = () => {
  editAble.value = !editAble.value;
};
</script>

<template>
  <el-form ref="attentionFormRef" :model="attList" label-width="82px">
    <el-form-item
      v-for="(item, index) in attList"
      :key="item.key"
      :label="(index + 1).toString()"
      :prop="`${index}.content`"
      :rules="formItemRules"
    >
      <el-row :gutter="10" style="width: 100%">
        <el-col :span="20">
          <el-input v-model="item.content" :disabled="editAble" />
        </el-col>
        <el-col :span="4">
          <el-button
            v-show="!editAble"
            :icon="useRenderIcon(Minus)"
            circle
            size="small"
            type="danger"
            @click.prevent="removeAttItem(item)"
          />
        </el-col>
      </el-row>
    </el-form-item>
    <el-form-item>
      <el-row :gutter="10">
        <el-col :span="12">
          <el-button type="primary" @click="editForm"
            >{{ editAble ? "修改" : "保存" }}
          </el-button>
        </el-col>
        <el-col :span="12">
          <el-button
            :disabled="editAble"
            :icon="useRenderIcon(Add)"
            type="primary"
            @click="addAttention"
            >新建行
          </el-button>
        </el-col>
      </el-row>
    </el-form-item>
  </el-form>
</template>
