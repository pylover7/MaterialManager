export default {
  path: "/superAdmin",
  meta: {
    title: "超管",
    rank: 7,
    icon: "fluent:person-passkey-48-regular"
  },
  children: [
    {
      path: "/superAdmin/settings",
      name: "Settings",
      component: () => import("@/views/superAdmin/Settings.vue"),
      meta: {
        title: "设置",
        icon: "fluent:settings-48-regular",
        keepAlive: true
      }
    },
    {
      path: "/superAdmin/logs",
      name: "Logs",
      component: () => import("@/views/superAdmin/Logs.vue"),
      meta: {
        title: "日志",
        icon: "fluent:text-bullet-list-square-search-20-regular"
      }
    }
  ]
} satisfies RouteConfigsTable;
