export default {
  path: "/superAdmin",
  meta: {
    title: "超管",
    rank: 7,
    icon: "fluent:shield-person-20-regular"
  },
  children: [
    {
      path: "/superAdmin/settings",
      name: "Settings",
      component: () => import("@/views/superAdmin/Settings.vue"),
      meta: {
        title: "设置",
        icon: "fluent:person-edit-48-regular",
        keepAlive: true
      }
    }
  ]
} satisfies RouteConfigsTable;
