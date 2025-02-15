import "./reset.css";
import roleForm from "../form/role.vue";
import editForm from "../form/index.vue";
import { zxcvbn } from "@zxcvbn-ts/core";
import { message } from "@/utils/message";
import { defaultPaginationSizes, usePublicHooks } from "@/views/hooks";
import { addDialog } from "@/components/ReDialog";
import type { PaginationProps } from "@pureadmin/table";
import type { RoleFormItemProps } from "../utils/types";
import { deviceDetection, getKeyList, isAllEmpty } from "@pureadmin/utils";

import { ElMessageBox } from "element-plus";
import {
  computed,
  h,
  onMounted,
  reactive,
  ref,
  type Ref,
  toRaw,
  watch
} from "vue";
import { successNotification } from "@/utils/notification";
import {
  addUser,
  deleteUser,
  getRoleList,
  getUserList,
  updateUserRole,
  updateUserStatus
} from "@/api/admin";

export function useUser(tableRef: Ref) {
  const form = reactive({
    // 左侧部门树的id
    nickname: "",
    departId: "",
    username: "",
    status: ""
  });
  const formRef = ref();
  const dataList = ref([]);
  const loading = ref(false);
  // 上传头像信息
  const switchLoadMap = ref({});
  const { switchStyle } = usePublicHooks();
  const treeData = ref([]);
  const treeLoading = ref(true);
  const selectedNum = ref(0);
  const pagination = reactive<PaginationProps>({
    total: 0,
    pageSize: 15,
    currentPage: 1,
    background: true,
    pageSizes: defaultPaginationSizes
  });
  const columns: TableColumnList = [
    {
      label: "勾选列", // 如果需要表格多选，此处label必须设置
      type: "selection",
      fixed: "left",
      reserveSelection: true // 数据刷新后保留选项
    },
    {
      label: "编号",
      prop: "id",
      width: 60
    },
    {
      label: "用户名称",
      prop: "nickname",
      minWidth: 130
    },
    {
      label: "账号",
      prop: "username",
      minWidth: 130
    },
    {
      label: "工号",
      prop: "employeeID",
      minWidth: 130
    },
    {
      label: "状态",
      prop: "status",
      minWidth: 90,
      cellRenderer: scope => (
        <el-switch
          size={scope.props.size === "small" ? "small" : "default"}
          loading={switchLoadMap.value[scope.index]?.loading}
          v-model={scope.row.status}
          active-value={1}
          inactive-value={0}
          active-text="已启用"
          inactive-text="已停用"
          inline-prompt
          style={switchStyle.value}
          onChange={() => onChange(scope as any)}
        />
      )
    },
    {
      label: "公司",
      prop: "company",
      minWidth: 90
    },
    {
      label: "部门",
      prop: "department",
      minWidth: 90
    },
    {
      label: "手机号码",
      prop: "mobile",
      minWidth: 90
    },
    {
      label: "邮箱",
      prop: "email",
      minWidth: 130
    },
    {
      label: "备注",
      minWidth: 100,
      prop: "remark",
      cellRenderer: ({ row }) => (
        <el-popover
          placement="bottom-start"
          width="100"
          trigger="hover"
          v-slots={{
            reference: () => (
              <el-text style="width: 100px">{row.remark}</el-text>
            ),
            default: () => <p>{row.remark}</p>
          }}
        ></el-popover>
      )
    },
    {
      label: "操作",
      fixed: "right",
      width: 180,
      slot: "operation"
    }
  ];
  const buttonClass = computed(() => {
    return [
      "!h-[20px]",
      "reset-margin",
      "!text-gray-500",
      "dark:!text-white",
      "dark:hover:!text-primary"
    ];
  });
  // 重置的新密码
  const pwdForm = reactive({
    newPwd: ""
  });
  // 当前密码强度（0-4）
  const curScore = ref();

  const roleId = ref();
  const roleOptions = ref([]);

  function onChange({ row, index }) {
    ElMessageBox.confirm(
      `确认要<strong>${
        row.status === 0 ? "停用" : "启用"
      }</strong><strong style='color:var(--el-color-primary)'>${
        row.nickname
      }</strong>用户吗?`,
      "系统提示",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        dangerouslyUseHTMLString: true,
        draggable: true
      }
    )
      .then(() => {
        switchLoadMap.value[index] = Object.assign(
          {},
          switchLoadMap.value[index],
          {
            loading: true
          }
        );
        updateUserStatus({ id: row.id, status: row.status }).then(() => {
          setTimeout(() => {
            switchLoadMap.value[index] = Object.assign(
              {},
              switchLoadMap.value[index],
              {
                loading: false
              }
            );
            message("已成功修改用户状态", {
              type: "success"
            });
          }, 300);
        });
      })
      .catch(() => {
        row.status === 0 ? (row.status = 1) : (row.status = 0);
      });
  }

  function handleDelete(row) {
    deleteUser(row.id, row.username).then(() => {
      successNotification(`您删除了用户名为${row.nickname}的这条数据`);
      onSearch();
    });
  }

  function handleSizeChange(val: number) {
    pagination.pageSize = val;
    onSearch();
  }

  function handleCurrentChange(val: number) {
    pagination.currentPage = val;
    onSearch();
  }

  /** 当CheckBox选择项发生变化时会触发该事件 */
  function handleSelectionChange(val) {
    selectedNum.value = val.length;
    // 重置表格高度
    tableRef.value.setAdaptive();
  }

  /** 取消选择 */
  function onSelectionCancel() {
    selectedNum.value = 0;
    // 用于多选表格，清空用户的选择
    tableRef.value.getTableRef().clearSelection();
  }

  /** 批量删除 */
  function onBatchDel() {
    // 返回当前选中的行
    const curSelected = tableRef.value.getTableRef().getSelectionRows();
    // 接下来根据实际业务，通过选中行的某项数据，比如下面的id，调用接口进行批量删除
    message(`已删除用户编号为【 ${getKeyList(curSelected, "id")} 】的数据`, {
      type: "success"
    });
    tableRef.value.getTableRef().clearSelection();
    onSearch();
  }

  async function onSearch() {
    loading.value = true;
    getUserList(
      pagination.currentPage,
      pagination.pageSize,
      toRaw(form).username,
      toRaw(form).nickname
    )
      .then(({ data, total, currentPage, pageSize }) => {
        dataList.value = data;
        pagination.total = total;
        pagination.pageSize = pageSize;
        pagination.currentPage = currentPage;
      })
      .finally(() => {
        setTimeout(() => {
          loading.value = false;
        }, 500);
      });
  }

  function openDialog() {
    addDialog({
      title: `新增用户`,
      props: {
        formInline: {
          userList: [],
          transferList: [
            // {
            //   username: "zhangsan",
            //   nickname: "张三",
            //   department: "技术部",
            //   mobile: "13888888888",
            //   email: "xxx@xxx.com",
            //   employeeID: "10001",
            //   company: "xxx公司"
            // }
          ]
        }
      },
      width: "50%",
      draggable: true,
      fullscreen: deviceDetection(),
      fullscreenIcon: true,
      closeOnClickModal: false,
      contentRenderer: () => h(editForm, { ref: formRef }),
      beforeSure: (done, { options }) => {
        const FormRef = formRef.value.getRef();
        const curData = options.props.formInline.userList;
        const sourceData = options.props.formInline.transferList;
        const data = sourceData.filter(item =>
          curData.includes(item.employeeID)
        );

        function chores() {
          successNotification(`您新增了用户数据，重复用户数据已自动过滤`);
          done(); // 关闭弹框
          onSearch(); // 刷新表格数据
        }

        FormRef.validate(valid => {
          if (valid) {
            if (curData.length > 0) {
              addUser(roleId.value, data).then(() => {
                chores();
              });
            } else {
              console.log(data);
              done();
            }
          }
        });
      }
    });
  }

  watch(
    pwdForm,
    ({ newPwd }) =>
      (curScore.value = isAllEmpty(newPwd) ? -1 : zxcvbn(newPwd).score)
  );

  /** 分配角色 */
  async function handleRole(row) {
    // 选中的角色列表
    const ids = row.roles.map(item => item.id) ?? [];
    addDialog({
      title: `分配 ${row.username} 用户的角色`,
      props: {
        formInline: {
          username: row?.username ?? "",
          nickname: row?.nickname ?? "",
          roleOptions: roleOptions.value ?? [],
          ids
        }
      },
      width: "400px",
      draggable: true,
      fullscreen: deviceDetection(),
      fullscreenIcon: true,
      closeOnClickModal: false,
      contentRenderer: () => h(roleForm),
      beforeSure: (done, { options }) => {
        const curData = options.props.formInline as RoleFormItemProps;
        // 根据实际业务使用curData.ids和row里的某些字段去调用修改角色接口即可
        updateUserRole(row.id, curData).then(() => {
          successNotification(`角色分配成功`);
          done(); // 关闭弹框
          onSearch(); // 刷新表格数据
        });
      }
    });
  }

  onMounted(async () => {
    treeLoading.value = true;
    onSearch();
    // 角色列表
    roleOptions.value = (
      await getRoleList(1, 100, { code: "", name: "", status: 1 })
    ).data;
  });

  return {
    form,
    roleId,
    loading,
    columns,
    dataList,
    treeData,
    roleOptions,
    treeLoading,
    selectedNum,
    pagination,
    buttonClass,
    deviceDetection,
    onSearch,
    onBatchDel,
    openDialog,
    handleDelete,
    handleRole,
    handleSizeChange,
    onSelectionCancel,
    handleCurrentChange,
    handleSelectionChange
  };
}
