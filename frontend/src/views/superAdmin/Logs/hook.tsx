import dayjs from "dayjs";
import { message } from "@/utils/message";
import { clearLoginLogs, getLoginLogsList } from "@/api/system";
import { defaultPaginationSizes, usePublicHooks } from "@/views/hooks";
import type { PaginationProps } from "@pureadmin/table";
import { onMounted, reactive, ref, type Ref } from "vue";

export function useRole(tableRef: Ref) {
  const form = reactive({
    username: "",
    status: "",
    loginTime: [] as [Date, Date] | []
  });
  const dataList = ref([]);
  const loading = ref(true);
  const selectedNum = ref(0);
  const { tagStyle } = usePublicHooks();

  const pagination = reactive<PaginationProps>({
    total: 0,
    pageSize: 15,
    currentPage: 1,
    background: true,
    pageSizes: defaultPaginationSizes
  });
  const columns: TableColumnList = [
    {
      label: "序号",
      type: "index",
      width: 60
    },
    {
      label: "用户名",
      prop: "username",
      minWidth: 80
    },
    {
      label: "登录 IP",
      prop: "ip",
      minWidth: 140
    },
    {
      label: "登录状态",
      prop: "status",
      minWidth: 100,
      cellRenderer: ({ row, props }) => (
        <el-tag size={props.size} style={tagStyle.value(row.status)}>
          {row.status === 1 ? "成功" : "失败"}
        </el-tag>
      )
    },
    {
      label: "登录时间",
      prop: "loginTime",
      minWidth: 180,
      formatter: ({ loginTime }) =>
        dayjs(loginTime).format("YYYY-MM-DD HH:mm:ss")
    }
  ];

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

  /** 清空日志 */
  function clearAll() {
    // 根据实际业务，调用接口删除所有日志数据
    clearLoginLogs().then(() => {
      message("已删除所有日志数据", {
        type: "success"
      });
      onSearch();
    });
  }

  async function onSearch() {
    loading.value = true;
    if (form.loginTime.length > 1) {
      form.loginTime = form.loginTime.map(time =>
        dayjs(time).format("YYYY-MM-DD HH:mm:ss")
      );
    }
    getLoginLogsList(
      pagination.currentPage,
      pagination.pageSize,
      form.username,
      form.status,
      form.loginTime
    )
      .then(({ data, total, pageSize, currentPage }) => {
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

  const resetForm = formEl => {
    if (!formEl) return;
    formEl.resetFields();
    onSearch();
  };

  onMounted(() => {
    onSearch();
  });

  return {
    form,
    loading,
    columns,
    dataList,
    pagination,
    selectedNum,
    onSearch,
    clearAll,
    resetForm,
    handleSizeChange,
    onSelectionCancel,
    handleCurrentChange,
    handleSelectionChange
  };
}
