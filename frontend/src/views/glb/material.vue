<script setup lang="tsx">
import { ref, reactive, computed, onMounted } from "vue";
import {
  getMaterialMeta,
  getGlbAttentionList,
  getGlbDutyInfo,
  dutyOver,
  getLatestNote
} from "@/api/material";
import { useUserStoreHook } from "@/store/modules/user";
import { successNotification, errorNotification } from "@/utils/notification";
import formatCurrentTime from "@/utils/formatDatetime";

defineOptions({
  name: "GlbMaterial"
});

enum StepStatus {
  Wait = "wait",
  Process = "process",
  Finish = "finish",
  Success = "success",
  Warning = "warning",
  Error = "error"
}
interface tableDataRow {
  id: number;
  uuid: string;
  name: string;
  model: string;
  position: string;
  number: string;
  nowNumber?: number;
  created_at?: string;
  updated_at?: string;
  dutyPerson?: string;
  dutyPersonDepart?: string;
  depart?: string;
  dutyDate?: string;
}
interface tableData extends Array<tableDataRow> {}

const columns: TableColumnList = [
  { label: "序号", type: "index", width: "60" },
  { label: "位置", prop: "position" },
  { label: "名称", prop: "name" },
  { label: "型号", prop: "model", width: "200" },
  { label: "数量", prop: "number", width: "100" },
  {
    label: "当前数量",
    width: "150",
    prop: "nowNumber",
    cellRenderer: ({ row }) => (
      <>
        <el-input-number
          v-model={row.nowNumber}
          controls={false}
          size="small"
        />
      </>
    )
  },
  {
    label: "确认",
    prop: "confirm",
    width: "100",
    cellRenderer: ({ row }) => (
      <>
        <el-button
          size="small"
          type={row.nowNumber === Number(row.number) ? "success" : "warning"}
          onClick={() => handleConfirm(row)}
          plain
        >
          确认
        </el-button>
      </>
    )
  }
];
const loading = ref(false);
onMounted(() => {
  initGlb();
});

const initGlb = () => {
  loading.value = true;
  getMaterialMeta("glb")
    .then(res => {
      confirmedData.length = 0;
      confirmedData.push(...res.data);
    })
    .finally(() => {
      loading.value = false;
    });
  getGlbAttentionList().then(res => {
    const result = res.data.map(item => item.note);
    attention.length = 0;
    attention.push(...result);
  });
  getLatestNote().then(res => {
    lastRemark.value = res.data.note;
  });
  getGlbDutyInfo().then(res => {
    dutyPerson.value = res.data.dutyPerson;
    dutyPersonDepart.value = res.data.dutyPersonDepart;
  });
  remark.value = "";
  step1Init.value = true;
  step2Init.value = true;
  step3Init.value = true;

  handleOverBtnLoading.value = false;
};

const confirmedData: tableData = reactive([]);
const step1Init = ref(true);

const step1Status = computed(() => {
  return confirmedData.every(item => item.nowNumber === Number(item.number))
    ? StepStatus.Success
    : StepStatus.Error;
});

const handleConfirm = row => {
  row.nowNumber = Number(row.number);
  step1Init.value = false;
};
const handleConfirmAll = () => {
  // 确认所有
  confirmedData.forEach(row => {
    row.nowNumber = Number(row.number);
    step1Init.value = false;
  });
};

const remark = ref("");
const lastRemark = ref("");
const step2Init = ref(true);

const step2Status = computed(() => {
  return remark.value.length > 0 ? StepStatus.Success : StepStatus.Error;
});

const copyLastRemark = () => {
  remark.value = lastRemark.value;
  step2Init.value = false;
};

const burlHandle = () => {
  step2Init.value = false;
};

const attention: string[] = reactive([]);

const step3Init = ref(true);
const attentionStatus = computed(() => {
  return step3Init.value ? StepStatus.Process : StepStatus.Success;
});
const attentionBtn = computed(() => {
  return step3Init.value ? StepStatus.Warning : StepStatus.Success;
});
const readAttention = () => {
  step3Init.value = false;
};

const dutyPerson = ref("");
const dutyPersonDepart = ref("");
const dialogVisible = ref(false);
const handleOverBtnLoading = ref(false);
const popDisabled = computed(() => {
  return !(step2Init.value || step2Init.value || step3Init.value);
});
const handoverConfirm = () => {
  // 交班
  if (popDisabled.value) {
    dialogVisible.value = true;
  }
};

const handover = () => {
  const date = formatCurrentTime();
  let data = {
    materialData: confirmedData.map((data: tableDataRow) => {
      return {
        name: data.name,
        model: data.model,
        position: data.position,
        number: data.number,
        nowNumber: data.nowNumber,
        dutyPerson: useUserStoreHook()?.username,
        dutyPersonDepart: useUserStoreHook()?.depart,
        depart: "glb",
        dutyDate: date
      };
    }),
    materialNote: {
      note: remark.value,
      depart: "glb",
      dutyDate: date
    },
    dutyDate: date,
    dutyPerson: useUserStoreHook()?.username,
    dutyPersonDepart: useUserStoreHook()?.depart
  };
  handleOverBtnLoading.value = true;
  dutyOver(data)
    .then(res => {
      initGlb();
      handleOverBtnLoading.value = false;
      successNotification("交班成功");
    })
    .catch(err => {
      errorNotification(err.message);
      handleOverBtnLoading.value = false;
    });
  dialogVisible.value = false;
};
</script>

<template>
  <div>
    <el-affix :offset="105">
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
                <el-button
                  type="success"
                  plain
                  size="large"
                  @click="handleConfirmAll"
                  >确认所有</el-button
                >
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
          <el-step title="查看注意事项" :status="attentionStatus">
            <template #description>
              <el-space direction="vertical" alignment="flex-start">
                <el-alert
                  title="注意事项"
                  :type="attentionBtn"
                  show-icon
                  :closable="false"
                >
                  <template #default>
                    <ol>
                      <li v-for="(item, index) in attention" :key="index">
                        {{ item }}
                      </li>
                    </ol>
                  </template>
                </el-alert>
                <el-button :type="attentionBtn" plain @click="readAttention"
                  >确认阅读
                </el-button>
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
          <el-button
            type="primary"
            :loading="handleOverBtnLoading"
            @click="handover"
          >
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
