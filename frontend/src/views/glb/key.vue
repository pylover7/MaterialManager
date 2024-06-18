<script setup lang="tsx">
import PureTable from "@pureadmin/table";
import { computed, onMounted, reactive, ref } from "vue";
import type { MaterialItem } from "@/types/base";
import { getDutyInfo, getLatestNote } from "@/api/material";
import { listBorrowed } from "@/api/home";

defineOptions({
  name: "GlbKey"
});

const area = "glb";
const metaType = "key";
enum StepStatus {
  Wait = "wait",
  Process = "process",
  Finish = "finish",
  Success = "success",
  Warning = "warning",
  Error = "error"
}

interface tableData extends Array<MaterialItem> {}

const dialogVisible = ref(false);

const popDisabled = computed(() => {
  return true;
});
const handoverConfirm = () => {
  // 交班
  if (popDisabled.value) {
    dialogVisible.value = true;
  }
};

const dutyPerson = ref("");
const dutyPersonDepart = ref("");
const confirmedData: tableData = reactive([]);
const loading = ref(false);

const remark = ref("");
const lastRemark = ref("");
const step1Init = ref(true);
const step2Init = ref(true);
const step1Status = computed(() => {
  return confirmedData.every(
    item => item.nowNumber === item.number - item.borrowed - item.checking
  )
    ? StepStatus.Success
    : StepStatus.Error;
});
const step2Status = computed(() => {
  return remark.value.length > 0 ? StepStatus.Success : StepStatus.Error;
});
const burlHandle = () => {
  step2Init.value = false;
};
const copyLastRemark = () => {
  remark.value = lastRemark.value;
  step2Init.value = false;
};

const columns: TableColumnList = [
  { label: "序号", type: "index", width: "60" },
  { label: "位置", prop: "position" },
  { label: "名称", prop: "name" },
  { label: "型号", prop: "model", width: "200" },
  { label: "当前数量", prop: "number", width: "100" },
  { label: "外借数量", prop: "borrowed", width: "100" },
  { label: "借用人", prop: "checking", width: "100" }
];

const handleOverBtnLoading = ref(false);

onMounted(() => {
  initInfo();
});

const initInfo = () => {
  loading.value = true;
  getDutyInfo(area, metaType).then(res => {
    dutyPerson.value = res.data.dutyPerson;
    dutyPersonDepart.value = res.data.dutyPersonDepart;
  });
  listBorrowed(area, 1, 100, false).then(res => {
    console.log(res.data);
  });
  listBorrowed(area, 1, 100, true, true, false).then(res => {
    console.log(res.data);
  });
  getLatestNote(area, metaType).then(res => {
    lastRemark.value = res.data.note;
  });
  loading.value = false;
};
</script>

<template>
  <div class="main">
    <el-affix :offset="105" target=".main">
      <el-card class="operationCar" shadow="never" body-style="padding: 0px;">
        <el-row :gutter="20" justify="space-between">
          <el-col class="rowFlex" :span="5">
            <el-popconfirm
              :disabled="dialogVisible"
              title="请确认所有数据已核对！"
              confirm-button-text="好的"
              cancel-button-text="再看看"
            >
              <template #reference>
                <el-button
                  type="success"
                  plain
                  size="large"
                  @click="handoverConfirm"
                  >交班</el-button
                >
              </template>
            </el-popconfirm>
          </el-col>
          <el-col class="rowFlex" :span="5">
            <el-text size="large" type="danger" tag="b"
              >值班员：{{ dutyPerson }}</el-text
            >
          </el-col>
          <el-col class="rowFlex" :span="5"
            ><el-text size="large" tag="b"
              >值班科值：{{ dutyPersonDepart }}</el-text
            >
          </el-col>
          <el-col :span="5" />
        </el-row>
      </el-card>
    </el-affix>

    <el-card shadow="never">
      <div class="flex">
        <el-steps direction="vertical">
          <el-step
            title="核对物资数量"
            :status="step1Init ? 'process' : step1Status"
          >
            <template #description>
              <el-space direction="vertical" alignment="flex-start">
                <pure-table
                  :columns="columns"
                  :data="confirmedData"
                  :border="true"
                  stripe
                  :loading="loading"
                  highlight-current-row
                  :header-cell-style="{ textAlign: 'center' }"
                  :cell-style="{ textAlign: 'center' }"
                  style="width: 70vw"
                />
              </el-space>
            </template>
          </el-step>
          <el-step
            title="备注异常信息"
            :status="step2Init ? 'process' : step2Status"
          >
            <template #description>
              <el-space alignment="flex-start">
                <el-space direction="vertical" alignment="flex-start">
                  <p>当前备注</p>
                  <el-input
                    v-model="remark"
                    type="textarea"
                    placeholder="填写本班备注"
                    :autosize="{ minRows: 2 }"
                    maxlength="510"
                    :show-word-limit="true"
                    style="width: 35vw"
                    @blur="burlHandle"
                  />
                  <el-button type="warning" plain @click="copyLastRemark"
                    >复制上个班</el-button
                  >
                </el-space>
                <el-space direction="vertical" alignment="flex-start">
                  <p>上个班备注</p>
                  <el-input
                    v-model="lastRemark"
                    type="textarea"
                    placeholder="上个班没有备注"
                    :autosize="{ minRows: 2 }"
                    :show-word-limit="true"
                    style="width: 35vw"
                    readonly
                  />
                </el-space>
              </el-space>
            </template>
          </el-step>
        </el-steps>
      </div>
    </el-card>
    <el-dialog v-model="dialogVisible" title="交班确认" width="500">
      <span>确认从 {{ dutyPerson }} 接班</span>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="handleOverBtnLoading">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style lang="scss" scoped>
.operationCar {
  padding: 0;
  margin-bottom: 20px;
}

.rowFlex {
  display: flex;
}
</style>
