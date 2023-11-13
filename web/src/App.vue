<template>
  <div id="app">
    <keep-alive>
      <router-view v-if="$route.meta.keepAlive"></router-view>
    </keep-alive>
    <router-view v-if="!$route.meta.keepAlive"></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {};
  },
};
</script>

<style>
@font-face {
  font-family: "PingFangSC";
  src: url("./assets/font/PingFangSC.ttf");
}
@font-face {
  font-family: "Smiley Sans";
  src: url("./assets/font/SmileySans.otf");
}
* {
  font-family: "PingFangSC";
  box-sizing: border-box;
}
p {
  margin: 0;
}
pre {
  overflow-wrap: break-word;
  word-wrap: break-word;
  overflow: auto;
  white-space: pre-wrap;
}
img {
  max-width: 100%;
}
.el-dialog {
  --el-dialog-title-font-size: 36px !important;
  --el-dialog-font-line-height: unset !important;
  display: flex;
  display: -ms-flex;
  flex-direction: column;
  -ms-flex-direction: column;
  margin: 0 !important;
  padding: 0 30px !important;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-height: calc(100% - 30px);
  max-width: calc(100% - 30px);
  width: max-content !important;
  border-radius: 8px !important;
}

.el-dialog .el-dialog__body {
  max-height: 100%;
  flex: 1;
  -ms-flex: 1 1 auto;
  overflow-y: auto;
  overflow-x: hidden;
  text-align: center;
}
::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 5px;
}

::-webkit-scrollbar {
  -webkit-appearance: none;
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-thumb {
  cursor: pointer;
  border-radius: 5px;
  background: #ececec;
  transition: color 0.2s ease;
}
.mr-20 {
  margin-right: 20px;
}
img {
  -webkit-user-drag: none;
  user-select: none;
}
</style>