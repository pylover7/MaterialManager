import { defineStore } from "pinia";

const useDialogStore = defineStore("welcome-dialog", {
  state() {
    return {
      active: 0
    };
  },
  actions: {
    nextActive() {
      this.active += 1;
    },
    prevActive() {
      this.active -= 1;
    },
    resetActive() {
      this.active = 0;
    }
  }
});

export default useDialogStore;
