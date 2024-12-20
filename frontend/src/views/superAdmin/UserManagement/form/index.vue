<script setup lang="ts">
import { ref } from "vue";
import { formRules } from "../utils/rule";
import Search from "@iconify-icons/ep/search";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { getLdapUserList } from "@/api/admin";

const props = withDefaults(
  defineProps<{ formInline: { userList: []; transferList: any[] } }>(),
  {
    formInline: () => ({
      userList: [],
      transferList: []
    })
  }
);

const ruleFormRef = ref();
const newFormInline = ref(props.formInline);
const transferProps = {
  key: "employeeID",
  value: "nickname"
};

function getRef() {
  return ruleFormRef.value;
}

const select = ref("sAMAccountName");
const filter = ref("");

const searchUser = () => {
  getLdapUserList(select.value, filter.value).then(res => {
    newFormInline.value.transferList = res.data;
  });
};

const clearAll = () => {
  newFormInline.value.userList = [];
};

defineExpose({ getRef });
</script>

<template>
  <el-form
    ref="ruleFormRef"
    :model="newFormInline"
    :rules="formRules"
    label-width="82px"
  >
    <el-transfer
      v-model="newFormInline.userList"
      :props="transferProps"
      filter-placeholder="请输入"
      :titles="['搜索用户', '新增用户']"
      :button-texts="['退回', '新增']"
      :data="newFormInline.transferList"
      style="padding: 10px 0"
    >
      <template #default="{ option }">
        <span>{{ option.username }} - {{ option.nickname }}</span>
      </template>
      <template #right-footer>
        <el-button class="transfer-footer" size="small" @click="clearAll"
          >清空已选择</el-button
        >
      </template>
      <template #left-footer>
        <el-input
          v-model="filter"
          style="max-width: 600px"
          placeholder="请输入"
          class="input-with-select"
          @keyup.enter="searchUser"
        >
          <template #prepend>
            <el-select
              v-model="select"
              placeholder="请选择"
              style="width: 90px; height: 100%"
            >
              <el-option label="按账号" value="sAMAccountName" />
              <el-option label="按部门" value="department" />
            </el-select>
          </template>
          <template #append>
            <el-button :icon="useRenderIcon(Search)" @click="searchUser" />
          </template>
        </el-input>
      </template>
    </el-transfer>
  </el-form>
</template>

<style scoped lang="scss">
.transfer-footer {
  margin-left: 15px;
  padding: 6px 5px;
}
:deep(.el-transfer-panel) {
  width: 300px;
}
</style>
