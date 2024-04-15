export default {
  path: "/admin",
  meta: {
    title: "管理员",
    rank: 5,
    icon: "fluent:shield-person-20-regular"
  },
  children: [
    {
      path: "/admin/approval",
      name: "Approval",
      component: () => import("@/views/admin/Approval.vue"),
      meta: {
        title: "审批",
        icon: "fluent:person-edit-48-regular",
        keepAlive: true
      }
    },
    {
      path: "/admin/material-meta",
      name: "MaterialMeta",
      component: () => import("@/views/admin/MaterialMeta.vue"),
      meta: {
        title: "物资数据",
        icon: "fluent:home-garage-24-regular",
        keepAlive: true
      }
    },
    {
      path: "/admin/operation-logs",
      name: "OperationLogs",
      component: () => import("@/views/admin/OperationLogs.vue"),
      meta: {
        title: "日志审计",
        icon: "fluent:notepad-person-24-regular"
      }
    }
  ]
} satisfies RouteConfigsTable;
