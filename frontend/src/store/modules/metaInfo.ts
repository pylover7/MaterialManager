import { store } from "@/store";
import { defineStore } from "pinia";

export const useMetaInfoStore = defineStore({
  id: "metaInfo",
  state: () => ({
    area: {
      glb: "glb",
      fk: "fk",
      wk: "wk"
    },
    metaType: {
      tool: "tool",
      key: "key"
    }
  })
});

export function useMetaInfoStoreHook() {
  return useMetaInfoStore(store);
}
