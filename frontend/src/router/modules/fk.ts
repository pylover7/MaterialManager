// 最简代码，也就是这些字段必须有
export default {
  path: "/fk",
  meta: {
    title: "辅控",
    rank: 2,
    icon: "fluent:brain-circuit-24-regular"
  },
  children: [
    {
      path: "/fk/material",
      name: "FkMaterial",
      component: () => import("@/views/fk/material.vue"),
      meta: {
        title: "辅控物资管理",
        icon: "fluent:box-search-16-regular",
        keepAlive: true
      }
    },
    {
      path: "/fk/key",
      name: "FkKey",
      component: () => import("@/views/fk/key.vue"),
      meta: {
        title: "辅控钥匙管理",
        icon: "fluent:key-reset-24-regular",
        keepAlive: true
      }
    }
  ]
} satisfies RouteConfigsTable;
