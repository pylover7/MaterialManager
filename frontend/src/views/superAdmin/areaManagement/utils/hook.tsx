import dayjs from "dayjs";
import editForm from "../form.vue";
import { message } from "@/utils/message";
import { ElMessageBox } from "element-plus";
import { defaultPaginationSizes, usePublicHooks } from "@/views/hooks";
import { addDialog } from "@/components/ReDialog";
import type { FormItemProps } from "../utils/types";
import type { PaginationProps } from "@pureadmin/table";
import { deviceDetection } from "@pureadmin/utils";
import { h, onMounted, reactive, ref } from "vue";
import { successNotification } from "@/utils/notification";
import {
  addArea,
  deleteArea,
  getAreaList,
  updateArea,
  updateAreaStatus
} from "@/api/admin";

export function useRole() {
  const form = reactive({
    name: "",
    code: "",
    status: null
  });
  const curRow = ref();
  const formRef = ref();
  const dataList = ref([]);
  const isShow = ref(false);
  const loading = ref(true);
  const switchLoadMap = ref({});
  ref(0);
  const { switchStyle } = usePublicHooks();
  const pagination = reactive<PaginationProps>({
    total: 0,
    pageSize: 15,
    currentPage: 1,
    background: true,
    pageSizes: defaultPaginationSizes
  });
  const columns: TableColumnList = [
    {
      label: "编号",
      type: "index",
      width: 60
    },
    {
      label: "区域名称",
      prop: "name"
    },
    {
      label: "区域标识",
      prop: "code"
    },
    {
      label: "状态",
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
      ),
      minWidth: 90
    },
    {
      label: "备注",
      prop: "remark",
      minWidth: 160
    },
    {
      label: "创建时间",
      prop: "created_at",
      minWidth: 160,
      formatter: ({ created_at }) =>
        dayjs(created_at).format("YYYY-MM-DD HH:mm:ss")
    },
    {
      label: "操作",
      fixed: "right",
      width: 210,
      slot: "operation"
    }
  ];

  function onChange({ row, index }) {
    ElMessageBox.confirm(
      `确认要<strong>${
        row.status === 0 ? "停用" : "启用"
      }</strong><strong style='color:var(--el-color-primary)'>${
        row.name
      }</strong>吗?`,
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
        delete row.updated_at;
        delete row.created_at;
        updateAreaStatus(row.id, row.status)
          .then(() => {
            setTimeout(() => {
              switchLoadMap.value[index] = Object.assign(
                {},
                switchLoadMap.value[index],
                {
                  loading: false
                }
              );
              message(`已${row.status === 0 ? "停用" : "启用"}${row.name}`, {
                type: "success"
              });
            }, 300);
            onSearch();
          })
          .catch(() => {
            row.status === 0 ? (row.status = 1) : (row.status = 0);
          });
      })
      .catch(() => {
        row.status === 0 ? (row.status = 1) : (row.status = 0);
      });
  }

  function handleDelete(row) {
    deleteArea(row.id).then(() => {
      message(`您删除了区域名称为【${row.name}】的这条数据`, {
        type: "success"
      });
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

  function handleSelectionChange(val) {
    console.log("handleSelectionChange", val);
  }

  async function onSearch() {
    loading.value = true;
    const { data, total, currentPage, pageSize } = await getAreaList(
      pagination.currentPage,
      pagination.pageSize,
      form.name,
      form.code
    );
    dataList.value = data;
    pagination.total = total;
    pagination.pageSize = pageSize;
    pagination.currentPage = currentPage;

    setTimeout(() => {
      loading.value = false;
    }, 500);
  }

  const resetForm = formEl => {
    if (!formEl) return;
    formEl.resetFields();
    onSearch();
  };

  function openDialog(title = "新增", row?: FormItemProps) {
    addDialog({
      title: `${title}区域`,
      props: {
        formInline: {
          id: row?.id ?? 0,
          name: row?.name ?? "",
          code: row?.code ?? "",
          remark: row?.remark ?? ""
        }
      },
      width: "40%",
      draggable: true,
      fullscreen: deviceDetection(),
      fullscreenIcon: true,
      closeOnClickModal: false,
      contentRenderer: () => h(editForm, { ref: formRef }),
      beforeSure: (done, { options }) => {
        const FormRef = formRef.value.getRef();
        const curData = options.props.formInline as FormItemProps;

        function chores() {
          successNotification(
            `您${title}了区域名称为${curData.name}的这条数据`
          );
          done(); // 关闭弹框
          onSearch(); // 刷新表格数据
        }

        FormRef.validate(valid => {
          if (valid) {
            // 表单规则校验通过
            if (title === "新增") {
              delete curData.id;
              // 实际开发先调用新增接口，再进行下面操作
              addArea(curData.name, curData.code, curData.remark)
                .then(() => {
                  chores();
                })
                .catch(err => {
                  message(`新增失败：${err.msg}`, { type: "error" });
                  done();
                });
            } else {
              updateArea(curData)
                .then(() => {
                  // 实际开发先调用修改接口，再进行下面操作
                  chores();
                })
                .catch(err => {
                  message(`修改失败：${err.msg}`, { type: "error" });
                  done();
                });
            }
          }
        });
      }
    });
  }

  /** 高亮当前权限选中行 */
  function rowStyle({ row: { id } }) {
    return {
      cursor: "pointer",
      background: id === curRow.value?.id ? "var(--el-fill-color-light)" : ""
    };
  }

  onMounted(async () => {
    onSearch();
  });

  return {
    form,
    isShow,
    loading,
    columns,
    rowStyle,
    dataList,
    pagination,
    onSearch,
    resetForm,
    openDialog,
    handleDelete,
    handleSizeChange,
    handleCurrentChange,
    handleSelectionChange
  };
}
