// 最简代码，也就是这些字段必须有
export default {
  path: "/test",
  meta: {
    title: "测试页"
  },
  component: () => import("@/views/testView/index.vue"),
};
