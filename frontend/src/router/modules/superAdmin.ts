export default {
  path: "/superAdmin",
  meta: {
    title: "超管",
    rank: 7,
    icon: "fluent:person-passkey-48-regular"
  },
  children: [
    {
      path: "/superAdmin/userManagement",
      name: "UserManagement",
      component: () => import("@/views/superAdmin/UserManagement/index.vue"),
      meta: {
        title: "用户管理",
        icon: "fluent:people-team-20-regular"
      }
    },
    {
      path: "/superAdmin/deptManagement",
      name: "DeptManagement",
      component: () => import("@/views/superAdmin/departManagement/index.vue"),
      meta: {
        title: "部门管理",
        icon: "fluent:people-community-20-regular"
      }
    },
    {
      path: "/superAdmin/roleManagement",
      name: "RoleManagement",
      component: () => import("@/views/superAdmin/roleManagement/index.vue"),
      meta: {
        title: "角色管理",
        icon: "fluent:people-team-20-regular"
      }
    },
    {
      path: "/superAdmin/logs",
      name: "Logs",
      component: () => import("@/views/superAdmin/Logs.vue"),
      meta: {
        title: "系统日志",
        icon: "fluent:text-bullet-list-square-search-20-regular"
      }
    },
    {
      path: "/superAdmin/settings",
      name: "Settings",
      component: () => import("@/views/superAdmin/Settings.vue"),
      meta: {
        title: "系统设置",
        icon: "fluent:settings-48-regular",
        keepAlive: true
      }
    }
  ]
} satisfies RouteConfigsTable;
