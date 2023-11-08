<template>
  <div class="login">
    <img
      src="../assets/icon.png"
      :class="'icon' + (loading ? ' loading-icon' : '')"
    />
    <div
      :class="'form-control' + (loading ? ' loading-form' : '')"
      v-if="!disappear"
    >
      <input required="" type="value" v-model="account" />
      <label>
        <span style="transition-delay: 450ms">账</span>
        <span style="transition-delay: 400ms">号</span>
        <span style="transition-delay: 350ms"> </span>
        <span style="transition-delay: 300ms">A</span>
        <span style="transition-delay: 250ms">c</span>
        <span style="transition-delay: 200ms">c</span>
        <span style="transition-delay: 150ms">o</span>
        <span style="transition-delay: 100ms">u</span>
        <span style="transition-delay: 50ms">n</span>
        <span style="transition-delay: 0ms">t</span>
      </label>
    </div>
    <div
      :class="'form-control' + (loading ? ' loading-form' : '')"
      v-if="!disappear"
    >
      <input required="" type="password" show-password v-model="password" />
      <label>
        <span style="transition-delay: 500ms">密</span>
        <span style="transition-delay: 450ms">码</span>
        <span style="transition-delay: 400ms"> </span>
        <span style="transition-delay: 350ms">P</span>
        <span style="transition-delay: 300ms">a</span>
        <span style="transition-delay: 250ms">s</span>
        <span style="transition-delay: 200ms">s</span>
        <span style="transition-delay: 150ms">w</span>
        <span style="transition-delay: 100ms">o</span>
        <span style="transition-delay: 50ms">r</span>
        <span style="transition-delay: 0ms">d</span>
      </label>
    </div>
    <button
      :class="'btn' + (loading ? ' loading-btn' : '')"
      @click="clickBtn"
      v-if="!disappear"
    >
      <a><span>登录</span></a>
    </button>
    <div :class="'text-wrapper' + (loading ? ' loading-typing' : '')">
      <div
        class="typing"
        v-if="!disappear && stateText"
        :style="'--strLength:' + stateText.length"
      >
        {{ stateText }}
      </div>
    </div>
  </div>
</template>

<script>
import { setToken } from "../utils/auth";
import { setData } from "../utils/data";
import { login } from "../api/index";
import md5 from "js-md5";
export default {
  data() {
    return {
      account: "",
      password: "",
      loading: false,
      disappear: false,
      stateText: "",
    };
  },
  mounted() {},
  methods: {
    clickBtn() {
      if (this.loading) {
        return;
      } else {
        this.toLogin();
      }
    },
    setAlert(str) {
      this.stateText = str;
      setTimeout(() => {
        this.stateText = "";
      }, 3000);
    },
    setLoading() {
      this.loading = true;
      setTimeout(() => {
        this.disappear = true;
      }, 1200);
    },
    cancelLoading() {
      this.disappear = false;
      setTimeout(() => {
        this.loading = false;
      }, 10);
    },
    toLogin() {
      if (!this.account) {
        this.setAlert("请输入您的账号");
        return;
      }
      if (!this.password) {
        this.setAlert("请输入您的密码");
        return;
      }
      this.setLoading();
      login({
        account: this.account,
        password: md5(md5(this.password) + "pamaforce"),
      })
        .then((res) => {
          console.log(res);
          if (res.code === 0) {
            setTimeout(() => {
              setToken(res.token);
              setData("info", res.username);
              this.$router.push("/");
            }, 1000);
          } else {
            setTimeout(() => {
              this.cancelLoading();
              this.setAlert(res.message);
            }, 1200);
          }
        })
        .catch(() => {
          setTimeout(() => {
            this.cancelLoading();
            this.setAlert("登录失败，请检查服务器状态");
          }, 1200);
        });
    },
  },
};
</script>

<style scoped>
.login {
  width: 100vw;
  height: 100vh;
  background-color: #f7f7f7;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.icon {
  width: 100px;
  height: 100px;
  margin-bottom: 40px;
  transition: all 0.7s cubic-bezier(0.59, 0.48, 0, 0.99) 0.5s;
}
.form-control {
  position: relative;
  margin-top: 0;
  margin-bottom: 40px;
  width: 240px;
  transition: all 1.2s cubic-bezier(0.59, 0.48, 0, 0.99);
  max-height: 100px;
}

.form-control input {
  background-color: transparent;
  border: 0;
  border-bottom: 2px #212121 solid;
  display: block;
  width: 100%;
  padding: 15px 0;
  font-size: 22px;
  color: #171717;
}

.form-control input:focus,
.form-control input:valid {
  outline: 0;
  border-bottom-color: #9ca3af;
}

.form-control label {
  position: absolute;
  top: 15px;
  left: 0;
  pointer-events: none;
}

.form-control label span {
  display: inline-block;
  font-size: 18px;
  min-width: 5px;
  color: #171717;
  transition: 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.form-control input:focus + label span,
.form-control input:valid + label span {
  color: #9ca3af;
  transform: translateY(-30px);
}
.btn a {
  position: relative;
  display: inline-block;
  padding: 5px 30px;
  border: 2px solid #212121;
  text-transform: uppercase;
  color: #212121;
  text-decoration: none;
  font-weight: 600;
  font-size: 20px;
  cursor: pointer;
}

.btn a::before {
  content: "";
  position: absolute;
  top: 6px;
  left: -2px;
  width: calc(100% + 4px);
  height: calc(100% - 12px);
  background-color: #f7f7f7;
  transition: 0.3s cubic-bezier(0.59, 0.48, 0, 0.99);
  transform: scaleY(1);
}

.btn a:hover::before {
  transform: scaleY(0);
}

.btn a::after {
  content: "";
  position: absolute;
  left: 6px;
  top: -2px;
  height: calc(100% + 4px);
  width: calc(100% - 12px);
  background-color: #f7f7f7;
  transition: 0.3s cubic-bezier(0.59, 0.48, 0, 0.99);
  transform: scaleX(1);
  transition-delay: 0.5s;
}

.btn a:hover::after {
  transform: scaleX(0);
}

.btn a span {
  position: relative;
  z-index: 3;
}

.btn {
  background-color: none;
  text-decoration: none;
  background-color: #f7f7f7;
  border: none;
  padding-top: 20px;
  transition: all 1.2s cubic-bezier(0.59, 0.48, 0, 0.99);
  max-height: 100px;
}
.text-wrapper {
  height: 30px;
  max-height: 30px;
  transition: all 1.2s cubic-bezier(0.59, 0.48, 0, 0.99);
  margin-top: 14px;
}
.typing {
  position: relative;
  color: #212121;
  font-size: 18px;
  --strLength: 7;
}
.typing::before,
.typing::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
.typing::before {
  background-color: #f7f7f7;
  animation: textTyping 1.2s steps(var(--strLength)) 0.5s forwards;
}
.typing::after {
  width: 2px;
  background-color: #212121;
  animation: textTyping 1.2s steps(var(--strLength)) 0.5s forwards,
    textBlink 0.5s steps(var(--strLength)) 0.1s infinite;
}
@keyframes textTyping {
  to {
    left: 100%;
  }
}
@keyframes textBlink {
  from,
  to {
    background: transparent;
  }
  50% {
    background: #212121;
  }
}
.loading-form {
  opacity: 0;
  max-height: 0;
  padding: 0;
  margin: 0;
}
.loading-btn {
  opacity: 0;
  padding: 0;
  margin: 0;
  max-height: 0;
}
.loading-typing {
  opacity: 0;
  padding: 0;
  margin: 0;
  height: 0;
  max-height: 0;
}
.loading-icon {
  width: 250px;
  height: 250px;
  margin-bottom: 0px;
}
</style>