<script lang="tsx" setup>
import { computed, h, onMounted, reactive, ref } from "vue";
import { getMaterialMeta } from "@/api/material";
import { errorNotification, successNotification } from "@/utils/notification";
import PureTable from "@pureadmin/table";
import { addDialog } from "@/components/ReDialog/index";
import verifyDialog from "@/views/welcome/dialog/VerifyDialog.vue";
import type { userInfo } from "@/views/welcome/types";
import {
  dutyOver,
  getDutyOverList,
  getDutyPerson,
  getLatestNote
} from "@/api/duty";
import { auth } from "@/api/base";
import { MaterialItem } from "@/types/material";

const props = defineProps({
  area: {
    type: String,
    required: true
  },
  metaType: {
    type: String,
    required: true
  }
});

onMounted(() => {
  init();
});

const init = () => {
  loading.value = true;
  getMaterialMeta(props.area, props.metaType)
    .then(res => {
      confirmedData.length = 0;
      confirmedData.push(...res.data);
    })
    .finally(() => {
      loading.value = false;
    });
  getDutyOverList(props.area).then(res => {
    attention.length = 0;
    attention.push(...res.data);
  });
  getLatestNote(props.area, props.metaType).then(res => {
    lastRemark.value = res.data.note;
  });
  getDutyPerson(props.area, props.metaType).then(res => {
    dutyPerson.value = res.data.dutyPerson;
    dutyPersonDepart.value = res.data.dutyPersonDepart;
  });
  remark.value = "";
  step1Init.value = true;
  step2Init.value = true;
  step3Init.value = true;

  handleOverBtnLoading.value = false;
};

enum StepStatus {
  Wait = "wait",
  Process = "process",
  Finish = "finish",
  Success = "success",
  Warning = "warning",
  Error = "error"
}

interface tableData extends Array<MaterialItem> {}

const columns: TableColumnList = [
  { label: "序号", type: "index", width: "60" },
  { label: "位置", prop: "position" },
  { label: "名称", prop: "name" },
  { label: "型号", prop: "model", width: "200" },
  { label: "数量", prop: "number", width: "100" },
  { label: "送检数量", prop: "checking", width: "100" },
  {
    label: "当前数量",
    width: "150",
    prop: "nowNumber",
    cellRenderer: ({ row }) => (
      <el-input-number v-model={row.nowNumber} controls={false} size="small" />
    )
  },
  {
    label: "确认",
    prop: "confirm",
    width: "100",
    cellRenderer: ({ row }) => (
      <el-button
        size="small"
        type={confirmBtnStatus(row)}
        onClick={() => handleConfirm(row)}
        plain
      >
        确认
      </el-button>
    )
  }
];
const loading = ref(false);

const confirmedData: tableData = reactive([]);
const step1Init = ref(true);

const step1Status = computed(() => {
  return confirmedData.every(
    item => item.nowNumber === item.number - item.borrowed - item.checking
  )
    ? StepStatus.Success
    : StepStatus.Error;
});

const handleConfirm = row => {
  row.nowNumber = Number(row.number) - row.borrowed - row.checking;
  step1Init.value = false;
};
const confirmBtnStatus = (row): "success" | "warning" => {
  return row.nowNumber == row.number - row.borrowed - row.checking
    ? "success"
    : "warning";
};
const handleConfirmAll = () => {
  // 确认所有
  confirmedData.forEach(row => {
    row.nowNumber = row.number - row.borrowed - row.checking;
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

const attention = reactive([]);

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
const dutyOverInfo = reactive({
  username: "",
  nickname: "",
  depart: "",
  phone: "",
  uuid: ""
});
const dialogVisible = ref(false);
const handleOverBtnLoading = ref(false);
const popDisabled = computed(() => {
  return !(step1Init.value || step2Init.value || step3Init.value);
});
const handoverConfirm = () => {
  // 交班
  if (popDisabled.value) {
    dialogVisible.value = true;
  }
};
const handoverCancel = () => {
  dutyOverInfo.nickname = "";
  dialogVisible.value = false;
};

const handover = () => {
  let data = {
    materialData: confirmedData.map((data: MaterialItem) => {
      return {
        name: data.name,
        model: data.model,
        position: data.position,
        number: data.number,
        nowNumber: data.nowNumber,
        dutyPerson: dutyOverInfo.nickname,
        dutyPersonDepart: dutyOverInfo.depart,
        area: props.area,
        type: props.metaType
      };
    }),
    materialNote: {
      note: remark.value,
      area: props.area,
      type: props.metaType
    },
    dutyPerson: dutyOverInfo.nickname,
    dutyPersonDepart: dutyOverInfo.depart
  };
  handleOverBtnLoading.value = true;
  dutyOver(props.area, props.metaType, data)
    .then(() => {
      init();
      handleOverBtnLoading.value = false;
      successNotification("交班成功");
    })
    .catch(err => {
      errorNotification(err.message);
      handleOverBtnLoading.value = false;
    });
  dialogVisible.value = false;
  dutyOverInfo.nickname = "";
};

const verifyForm = ref();

const openVerifyDialog = () => {
  addDialog({
    title: "接班人员验证",
    width: "25%",
    props: {
      userInfo: {
        account: "",
        password: "",
        name: "",
        phone: "",
        depart: "",
        disable: true
      }
    },
    contentRenderer: () => h(verifyDialog, { ref: verifyForm }),
    beforeSure(done, { options }) {
      const accountFormRef = verifyForm.value.getAccountRef();
      const curData = options.props.userInfo as userInfo;
      accountFormRef.validate(valid => {
        if (valid) {
          auth({
            username: curData.account,
            password: curData.password
          })
            .then(res => {
              dutyOverInfo.nickname = res.data.nickname;
              dutyOverInfo.username = res.data.username;
              dutyOverInfo.depart = res.data.depart;
              dutyOverInfo.phone = res.data.phone;
              dutyOverInfo.uuid = res.data.uuid;
              done();
            })
            .catch(() => {
              errorNotification("账号或密码错误");
            });
        }
      });
    }
  });
};
</script>

<template>
  <div class="main">
    <el-affix :offset="105" target=".main">
      <el-card body-style="padding: 0px;" class="operationCar" shadow="never">
        <el-row :gutter="20" justify="space-between">
          <el-col :span="5" class="rowFlex">
            <el-popconfirm
              :disabled="dialogVisible"
              cancel-button-text="再看看"
              confirm-button-text="好的"
              title="请确认所有数据已核对！"
            >
              <template #reference>
                <el-button
                  plain
                  size="large"
                  type="success"
                  @click="handoverConfirm"
                  >交班
                </el-button>
              </template>
            </el-popconfirm>
          </el-col>
          <el-col :span="5" class="rowFlex">
            <el-text size="large" tag="b" type="danger"
              >值班员：{{ dutyPerson }}
            </el-text>
          </el-col>
          <el-col :span="5" class="rowFlex">
            <el-text size="large" tag="b"
              >部门：{{ dutyPersonDepart }}
            </el-text>
          </el-col>
          <el-col :span="5" />
        </el-row>
      </el-card>
    </el-affix>

    <el-card shadow="never">
      <div class="flex">
        <el-steps direction="vertical">
          <el-step
            :status="step1Init ? 'process' : step1Status"
            title="核对物资数量"
          >
            <template #description>
              <el-space alignment="flex-start" direction="vertical">
                <pure-table
                  :border="true"
                  :cell-style="{ textAlign: 'center' }"
                  :columns="columns"
                  :data="confirmedData"
                  :header-cell-style="{ textAlign: 'center' }"
                  :loading="loading"
                  highlight-current-row
                  stripe
                  style="width: 70vw"
                />
                <el-button
                  plain
                  size="large"
                  type="primary"
                  @click="handleConfirmAll"
                  >确认所有
                </el-button>
              </el-space>
            </template>
          </el-step>
          <el-step
            :status="step2Init ? 'process' : step2Status"
            title="备注异常信息"
          >
            <template #description>
              <el-space alignment="flex-start">
                <el-space alignment="flex-start" direction="vertical">
                  <p>当前备注</p>
                  <el-input
                    v-model="remark"
                    :autosize="{ minRows: 2 }"
                    :show-word-limit="true"
                    maxlength="510"
                    placeholder="填写本班备注"
                    style="width: 35vw"
                    type="textarea"
                    @blur="burlHandle"
                  />
                  <el-button plain type="warning" @click="copyLastRemark"
                    >复制上个班
                  </el-button>
                </el-space>
                <el-space alignment="flex-start" direction="vertical">
                  <p>上个班备注</p>
                  <el-input
                    v-model="lastRemark"
                    :autosize="{ minRows: 2 }"
                    :show-word-limit="true"
                    placeholder="上个班没有备注"
                    readonly
                    style="width: 35vw"
                    type="textarea"
                  />
                </el-space>
              </el-space>
            </template>
          </el-step>
          <el-step :status="attentionStatus" title="查看注意事项">
            <template #description>
              <el-space alignment="flex-start" direction="vertical">
                <el-alert
                  :closable="false"
                  :type="attentionBtn"
                  show-icon
                  title="注意事项"
                >
                  <template #default>
                    <ol>
                      <li v-for="(item, index) in attention" :key="index">
                        {{ item.content }}
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
    <el-dialog v-model="dialogVisible" title="交班确认" width="400">
      <el-space
        direction="vertical"
        style="align-items: start; padding-left: 10px"
      >
        <span
          >确认从
          <span style="font-size: large; color: red">{{ dutyPerson }}</span>
          接班</span
        >
        <span>接班人员：{{ dutyOverInfo.nickname }}</span>
        <el-button type="primary" @click="openVerifyDialog">验证</el-button>
      </el-space>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handoverCancel">取消</el-button>
          <el-button
            :disabled="dutyOverInfo.nickname.length === 0"
            :loading="handleOverBtnLoading"
            type="primary"
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
