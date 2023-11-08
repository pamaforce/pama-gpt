<template>
  <div></div>
</template>

<script>
import { removeToken } from "@/utils/auth";
import { getData } from "@/utils/data";
export default {
  data() {
    return {};
  },
  methods: {
    getData(key) {
      return getData(key) || {};
    },
    handleCommand(val) {
      switch (val) {
        case "logout":
          this.toLogout();
          break;
      }
    },
    toLogout() {
      removeToken();
      this.$message.success("退出登录成功");
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
</style>