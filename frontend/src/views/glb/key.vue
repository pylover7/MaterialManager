<script setup lang="tsx">
import PureTable from "@pureadmin/table";
import { computed, h, onMounted, reactive, ref } from "vue";
import type { MaterialItem } from "@/types/base";
import { dutyOver, getDutyInfo, getLatestNote } from "@/api/material";
import { listBorrowed } from "@/api/home";
import { usePublicHooks } from "@/views/hooks";
import { errorNotification, successNotification } from "@/utils/notification";
import { BorrowedInfo } from "@/types/admin";
import { addDialog } from "@/components/ReDialog/index";
import verifyDialog from "@/views/welcome/dialog/VerifyDialog.vue";
import type { userInfo } from "@/views/welcome/types";
import { getUserInfo } from "@/api/user";

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

const dutyPerson = ref("");
const dutyPersonDepart = ref("");
const dutyOverInfo = reactive({
  username: "",
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
          reference: () => <el-button link>{row.material[0].name}</el-button>,
          default: () => (
            <ul>
              <li>名称：{row.material[0].name}</li>
              <li>型号：{row.material[0].model}</li>
              <li>位置：{row.material[0].position}</li>
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
          reference: () => <el-button link>{row.username}</el-button>,
          default: () => (
            <ul>
              <li>姓名：{row.username}</li>
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
        placement="right"
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
  initInfo();
});

const initInfo = () => {
  loading.value = true;
  tableDataList.length = 0;
  getDutyInfo(area, metaType).then(res => {
    dutyPerson.value = res.data.dutyPerson;
    dutyPersonDepart.value = res.data.dutyPersonDepart;
  });
  listBorrowed(area, 1, 100, false).then(res => {
    tableDataList.push(...res.data);
  });
  listBorrowed(area, 1, 100, true, true, false).then(res => {
    tableDataList.push(...res.data);
    console.log(tableDataList);
  });
  getLatestNote(area, metaType).then(res => {
    lastRemark.value = res.data.note;
  });
  loading.value = false;
};

const handover = () => {
  let data = {
    materialData: tableDataList.map((data: BorrowedInfo) => {
      return {
        name: data.material[0].name,
        model: data.material[0].model,
        position: data.material[0].position,
        number: data.material[0].number,
        nowNumber: data.material[0].number - data.material[0].borrowed,
        dutyPerson: dutyOverInfo.username,
        dutyPersonDepart: dutyOverInfo.depart,
        area: area,
        type: metaType
      };
    }),
    materialNote: {
      note: remark.value,
      area: area,
      type: metaType
    },
    dutyPerson: dutyOverInfo.username,
    dutyPersonDepart: dutyOverInfo.depart
  };
  handleOverBtnLoading.value = true;
  dutyOver(area, metaType, data)
    .then(() => {
      initInfo();
      handleOverBtnLoading.value = false;
      successNotification("交班成功");
    })
    .catch(err => {
      errorNotification(err.message);
      handleOverBtnLoading.value = false;
    });
  dialogVisible.value = false;
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
          getUserInfo({
            username: curData.account,
            password: curData.password
          })
            .then(res => {
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
          <el-step title="核对钥匙借用情况">
            <template #description>
              <el-space direction="vertical" alignment="flex-start">
                <pure-table
                  :columns="columns"
                  :data="tableDataList"
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
          <el-step title="备注异常信息">
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
        <span>接班人员：{{ dutyOverInfo.username }}</span>
        <el-button type="primary" @click="openVerifyDialog">验证</el-button>
      </el-space>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button
            type="primary"
            :loading="handleOverBtnLoading"
            :disabled="dutyOverInfo.username.length === 0"
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
