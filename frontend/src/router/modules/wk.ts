// 最简代码，也就是这些字段必须有
export default {
  path: "/wk",
  meta: {
    title: "网控",
    rank: 3,
    icon: "fluent:content-view-gallery-lightning-28-regular"
  },
  children: [
    {
      path: "/wk/material",
      name: "WkMaterial",
      component: () => import("@/views/wk/material.vue"),
      meta: {
        title: "网控物资管理",
        icon: "fluent:box-search-16-regular",
        keepAlive: true
      }
    },
    {
      path: "/wk/key",
      name: "WkKey",
      component: () => import("@/views/wk/key.vue"),
      meta: {
        title: "网控钥匙管理",
        icon: "fluent:key-reset-24-regular",
        keepAlive: true
      }
    }
  ]
} satisfies RouteConfigsTable;
