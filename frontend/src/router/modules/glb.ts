import { $t } from "@/plugins/i18n";

export default {
  path: "/glb",
  meta: {
    title: $t("glb.title"),
    icon: "fluent:desktop-flow-24-regular",
    rank: 1
  },
  children: [
    {
      path: "/glb/material",
      name: "GlbMaterial",
      component: () => import("@/views/glb/material.vue"),
      meta: {
        title: $t("glb.glbMaterialTitle"),
        icon: "fluent:box-search-16-regular",
        keepAlive: true
      }
    },
    {
      path: "/glb/key",
      name: "GlbKey",
      component: () => import("@/views/glb/key.vue"),
      meta: {
        title: $t("glb.glbKeyTitle"),
        icon: "fluent:key-reset-24-regular",
        keepAlive: true
      }
    }
  ]
} satisfies RouteConfigsTable;
