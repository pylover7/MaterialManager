<script lang="tsx" setup>
import PureTable from "@pureadmin/table";
import { computed, h, onMounted, reactive, ref } from "vue";
import { usePublicHooks } from "@/views/hooks";
import { errorNotification, successNotification } from "@/utils/notification";
import { BorrowedInfo } from "@/types/admin";
import { addDialog } from "@/components/ReDialog/index";
import verifyDialog from "@/views/welcome/dialog/VerifyDialog.vue";
import type { userInfo } from "@/views/welcome/types";

import { auth } from "@/api/base";
import { dutyOver, getDutyPerson, getLatestNote } from "@/api/duty";
import { listBorrowed } from "@/api/material";

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

const dialogVisible = ref(false);
/** 标签风格 */
const { tagStyle } = usePublicHooks();

const popDisabled = computed(() => {
  return true;
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

const dutyPerson = ref("");
const dutyPersonDepart = ref("");
const dutyOverInfo = reactive({
  username: "",
  nickname: "",
  depart: "",
  phone: "",
  uuid: ""
});
const tableDataList = reactive([]);
const loading = ref(false);

const remark = ref("");
const lastRemark = ref("");

const copyLastRemark = () => {
  remark.value = lastRemark.value;
};

const columns: TableColumnList = [
  {
    label: "序号",
    type: "index",
    width: 60
  },
  {
    label: "借用物资信息",
    prop: "material",
    cellRenderer: ({ row }) => (
      <el-popover
        placement="right"
        width="200"
        trigger="click"
        v-slots={{
          reference: () => <el-button link>{row.material.name}</el-button>,
          default: () => (
            <ul>
              <li>名称：{row.material.name}</li>
              <li>型号：{row.material.model}</li>
              <li>位置：{row.material.position}</li>
            </ul>
          )
        }}
      ></el-popover>
    )
  },
  {
    label: "借用人信息",
    prop: "username",
    cellRenderer: ({ row }) => (
      <el-popover
        placement="right"
        width="200"
        trigger="click"
        v-slots={{
          reference: () => <el-button link>{row.nickname}</el-button>,
          default: () => (
            <ul>
              <li>工号：{row.nickname}</li>
              <li>电话：{row.phone}</li>
              <li>部门：{row.userDepart}</li>
            </ul>
          )
        }}
      ></el-popover>
    )
  },
  {
    label: "借用人电话",
    prop: "phone"
  },
  {
    label: "数量",
    prop: "borrowing"
  },
  {
    label: "借用理由",
    prop: "reason",
    cellRenderer: ({ row }) => (
      <el-popover
        placement="bottom"
        width="300"
        trigger="hover"
        v-slots={{
          reference: () => (
            <el-text truncated style="width: 100px">
              {row.reason}
            </el-text>
          ),
          default: () => <p>{row.reason}</p>
        }}
      ></el-popover>
    )
  },
  {
    label: "借用时间",
    prop: "borrowTime"
  },
  {
    label: "状态",
    prop: "borrowApproveStatus",
    cellRenderer: ({ row, props }) => (
      <el-tag
        size={props.size}
        style={tagStyle.value(row.borrowApproveStatus ? 1 : 0)}
      >
        {row.borrowApproveStatus ? "待归还" : "待审批"}
      </el-tag>
    )
  }
];

const handleOverBtnLoading = ref(false);

onMounted(() => {
  init();
});

const init = () => {
  loading.value = true;
  tableDataList.length = 0;
  getDutyPerson(props.area, props.metaType).then(res => {
    dutyPerson.value = res.data.dutyPerson;
    dutyPersonDepart.value = res.data.dutyPersonDepart;
  });
  listBorrowed(props.area, 1, 100, false).then(res => {
    tableDataList.push(...res.data);
  });
  listBorrowed(props.area, 1, 100, true, true, false).then(res => {
    tableDataList.push(...res.data);
  });
  getLatestNote(props.area, props.metaType).then(res => {
    lastRemark.value = res.data.note;
  });
  remark.value = "";
  loading.value = false;
};

const handover = () => {
  let data = {
    materialData: tableDataList.map((data: BorrowedInfo) => {
      return {
        name: data.material.name,
        model: data.material.model,
        position: data.material.position,
        number: data.material.number,
        nowNumber: data.material.number - data.material.borrowed,
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
      successNotification("交班成功");
      dialogVisible.value = false;
    })
    .catch(err => {
      errorNotification(err.message);
    })
    .finally(() => {
      handleOverBtnLoading.value = false;
    });
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
          <el-step title="核对钥匙借用情况">
            <template #description>
              <el-space alignment="flex-start" direction="vertical">
                <pure-table
                  :border="true"
                  :cell-style="{ textAlign: 'center' }"
                  :columns="columns"
                  :data="tableDataList"
                  :header-cell-style="{ textAlign: 'center' }"
                  :loading="loading"
                  highlight-current-row
                  stripe
                  style="width: 70vw"
                />
              </el-space>
            </template>
          </el-step>
          <el-step title="备注异常信息">
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
