<template>
  <div class="chat">
    <div class="top-card">
      <img :src="require('../assets/' + info.avatar)" class="card-avatar" />
      <div class="card-text">
        <div class="card-title">
          <p class="card-title-p">{{ info.name }}</p>
          <div class="card-btns">
            <div class="refresh" @click="refreshChatId" title="刷新对话">
              <svg
                viewBox="0 0 24 24"
                fill="black"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M19.54 3.66c-.13-.49-.45-.9-.89-1.16-.44-.26-.95-.32-1.45-.19-.49.13-.9.45-1.16.89l-3.48 6.03L10.42 8a.738.738 0 0 0-1.02.27L8.28 10.2c-.1.17-.13.38-.08.57.05.19.18.36.35.46l.31.18c-2.21 2.1-6.06 3.64-6.1 3.66-.26.1-.45.35-.47.63-.03.28.11.55.35.7l2.01 1.25c.19.12.42.15.63.08.03-.01.48-.16 1.07-.42-.1.15-.18.24-.18.24-.15.16-.22.39-.2.61.03.22.16.42.35.54l4.99 3.1c.12.08.26.11.4.11.16 0 .32-.05.45-.15.11-.09 2.63-2.04 3.74-6.29l.31.18a.746.746 0 0 0 1.02-.27l1.12-1.93c.1-.17.13-.38.08-.57a.77.77 0 0 0-.35-.46l-2.21-1.27 3.48-6.03c.25-.45.32-.97.19-1.46Zm-7.91 16.56-3.84-2.39c.28-.49.59-1.2.65-2.07a.758.758 0 0 0-.38-.71.747.747 0 0 0-.8.04c-.74.52-1.65.91-2.13 1.09l-.49-.3c1.51-.71 3.96-2.04 5.56-3.7l4.33 2.5c-.69 3.03-2.2 4.84-2.9 5.54Zm4.68-6.26L9.96 10.3l.36-.63 4.15 2.39 2.2 1.27-.36.63Zm1.74-9.6-3.48 6.03-.7-.4 3.48-6.03c.11-.19.36-.26.55-.15a.405.405 0 0 1 .15.55ZM16.75 21.14a1.25 1.25 0 1 0 0-2.5 1.25 1.25 0 0 0 0 2.5ZM19 17.5a1 1 0 1 0 0-2 1 1 0 0 0 0 2ZM20.25 19.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Z"
                ></path>
              </svg>
            </div>
            <div class="back" @click="$router.push('/')">
              <img src="../assets/back.svg" />
              <p>返回主页</p>
            </div>
          </div>
        </div>
        <p class="card-desc">{{ info.desc }}</p>
      </div>
    </div>
    <div
      :class="'chat-card chat-card-' + item.role"
      v-for="(item, i) in chatList"
      :key="i"
    >
      <div
        class="card-role"
        v-if="item.role === 1"
        :style="
          'animation-delay:' +
          (item.delay === undefined
            ? i * 100 + 500 > 2000
              ? 2000
              : i * 100 + 500
            : 0) +
          'ms;'
        "
      >
        <img :src="require('../assets/' + info.avatar)" class="role-avatar" />
        <p class="role-name">{{ info.name }}</p>
      </div>
      <div
        :class="'card-' + item.role"
        :style="
          'animation-delay:' +
          (item.delay === undefined ? i * 100 + 500 : 0) +
          'ms;' +
          (item.error ? 'background-color:#ad1840;color:white' : '')
        "
      >
        <vue-markdown class="content">{{ item.content }}</vue-markdown>
      </div>
    </div>
    <div class="bottom-blank"></div>
    <div class="bottom-fixed"></div>
    <div class="user-input">
      <textarea
        class="textarea"
        v-model="question"
        :rows="1"
        ref="input"
        placeholder="问点什么吧~"
      />
      <div
        :class="'btn' + (!loading && question !== '' ? '' : ' btn-disable')"
        @click="handleClick()"
      >
        <transition name="fade">
          <div v-if="!loading">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 16 16"
              fill="red"
              class="btn-svg"
            >
              <path
                d="M.5 1.163A1 1 0 0 1 1.97.28l12.868 6.837a1 1 0 0 1 0 1.766L1.969 15.72A1 1 0 0 1 .5 14.836V10.33a1 1 0 0 1 .816-.983L8.5 8 1.316 6.653A1 1 0 0 1 .5 5.67V1.163Z"
                fill="currentColor"
              ></path>
            </svg>
          </div>
          <div class="superballs" v-else>
            <div class="superballs__dot"></div>
            <div class="superballs__dot"></div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import { updateChatId, getChatHistory } from "@/api/index";
import VueMarkdown from "vue-markdown";
import config from "@/utils/config";
import { getToken } from "@/utils/auth";
import io from "socket.io-client";
export default {
  data() {
    return {
      info: {},
      question: "",
      loading: false,
      chatList: [],
      socket: null,
    };
  },
  components: {
    VueMarkdown,
  },
  methods: {
    handleClick() {
      if (this.loading) return;
      this.question = this.question.trim();
      if (this.question === "") return;
      this.loading = true;
      let ques = this.question;
      this.question = "";
      this.$refs.input.style.height = "auto";
      this.chatList.push({ role: 0, content: ques, delay: 0 });
      this.scrollBottom();
      if (this.socket === null) {
        this.connectSocket()
          .then(() => {
            this.sendMsg(ques);
          })
          .catch((err) => {
            this.loading = false;
            this.chatList.push({
              role: 1,
              content: err,
              error: true,
              delay: 0,
            });
            this.scrollBottom();
          });
      } else {
        this.sendMsg(ques);
      }
    },
    sendMsg(msg) {
      this.chatList.push({
        role: 1,
        content: "",
        delay: 0,
      });
      this.socket.emit("chat", { bot: this.info.name, message: msg });
    },
    refreshChatId() {
      updateChatId({ bot: this.info.name }).then((res) => {
        if (res.code === 0) {
          if (this.socket) {
            this.socket.disconnect();
            this.socket = null;
          }
          this.chatList = [];
          this.loading = false;
          this.scrollBottom();
          this.$refs.input.focus();
          this.$forceUpdate();
        }
      });
    },
    scrollBottom() {
      this.$nextTick(() => {
        window.scrollTo({
          top: document.body.scrollHeight,
          behavior: "smooth",
        });
      });
    },
    handleResponseEnd() {
      this.loading = false;
      this.scrollBottom();
      this.$refs.input.focus();
    },
    connectSocket() {
      return new Promise((resolve, reject) => {
        this.socket = io.connect("http://localhost:5000", {
          extraHeaders: {
            Authorization: "Bearer " + getToken(),
          },
          timeout: 5000,
        });

        this.socket.on("connect", () => {
          console.log("Connected!");
          resolve("Connected");
        });

        this.socket.on("response", (data) => {
          console.log("Response: " + data);
          this.chatList[this.chatList.length - 1].content += data;
        });

        this.socket.on("chat_id", (data) => {
          updateChatId({ bot: this.info.name, chatId: data });
        });

        this.socket.on("response_end", () => {
          this.handleResponseEnd();
        });

        this.socket.on("error", (data) => {
          console.error("Error: " + JSON.stringify(data));
          this.socket = null;
          reject("Error: " + JSON.stringify(data));
        });

        this.socket.on("connect_error", (error) => {
          console.error("Connect error: " + error);
          this.socket = null;
          reject("Connect error: " + error);
        });

        this.socket.on("connect_timeout", () => {
          console.error("Connect timeout");
          this.socket = null;
          reject("Connect timeout");
        });
      });
    },
  },
  beforeDestroy() {
    if (this.socket) {
      this.socket.disconnect();
    }
  },
  mounted() {
    let textarea = document.querySelector("textarea");
    if (textarea) {
      function autoResize() {
        this.style.height = "auto";
        this.style.height = this.scrollHeight + "px";
      }
      textarea.addEventListener("input", autoResize, false);
      textarea.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
          event.preventDefault();
          this.handleClick();
        }
      });
    }
  },
  created() {
    this.info = config.preset[this.$route.params.bot] || {
      desc: "待补充描述。",
      avatar: "ChatGPT.png",
    };
    this.info.name = this.$route.params.bot;
    getChatHistory(this.info.name).then((res) => {
      if (res.code === 0) {
        res.chat_history.map((item) => {
          item.role = item.author === "human" ? 0 : 1;
          item.content = item.text;
        });
        this.chatList = res.chat_history;
        setTimeout(() => {
          this.scrollBottom();
        }, 2000);
      }
    });
  },
};
</script>

<style scoped>
.chat {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.top-card {
  position: relative;
  width: 600px;
  border-radius: 20px;
  background-color: #f7f7f7;
  display: flex;
  padding: 12px;
  margin: 10px 0;
  align-items: center;
  transform: translateY(-100%);
  animation: top-in 0.5s ease-in-out forwards;
}
.card-avatar {
  width: 80px;
  height: 80px;
  border-radius: 15px;
  margin-right: 20px;
}
.card-text {
  display: flex;
  flex-direction: column;
  flex-grow: 2;
}
.refresh {
  width: 18px;
  height: 18px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 10px;
}
.card-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}
.card-title-p {
  font-size: 20px;
  font-weight: 700;
  margin: 0;
}
.card-desc {
  font-size: 15px;
  margin: 0;
}
.back {
  display: flex;
  cursor: pointer;
  align-items: center;
  color: #3b3abe;
  margin-right: 5px;
}
.back img {
  width: 14px;
  height: 14px;
  margin-right: 3px;
}
.back p {
  font-size: 13px;
  margin: 0;
}
.user-input {
  line-height: 0;
  position: fixed;
  bottom: 20px;
  width: 600px;
  padding: 12px;
  padding-left: 18px;
  background-color: #f7f7f7;
  align-items: center;
  display: flex;
  flex-wrap: nowrap;
  border-radius: 12px;
  transform: translateY(100%);
  animation: bottom-in 0.5s ease-in-out forwards;
}
.textarea {
  font-size: 18px;
  width: 100%;
  overflow: hidden;
  resize: none;
  border: none;
  outline: none;
  background: none;
  max-height: 40vh;
  overflow: auto;
}
.btn {
  margin-left: 12px;
  width: 30px;
  height: 30px;
  border-radius: 5px;
  display: flex;
  justify-content: center;
  transition: color, background-color 0.2s;
  align-items: center;
  align-self: flex-end;
  background-color: #5d5cde;
  color: white;
  cursor: pointer;
  flex-shrink: 0;
}
.btn-disable {
  background-color: transparent;
  color: #dedee5;
  cursor: unset;
}
.btn-svg {
  width: 15px;
  height: 15px;
}
.superballs {
  --uib-size: 30px;
  --uib-speed: 1.1s;
  --uib-color: #5d5cde;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: var(--uib-size);
  width: var(--uib-size);
}

.superballs__dot {
  position: absolute;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
}

.superballs__dot::before {
  content: "";
  height: 30%;
  width: 30%;
  border-radius: 50%;
  background-color: var(--uib-color);
  will-change: transform;
  flex-shrink: 0;
}

.superballs__dot:nth-child(1) {
  transform: rotate(45deg);
}

.superballs__dot:nth-child(1)::before {
  animation: orbit82140 var(--uib-speed) linear calc(var(--uib-speed) * -0.143)
    infinite;
}

.superballs__dot:nth-child(2) {
  transform: rotate(-45deg);
}

.superballs__dot:nth-child(2)::before {
  animation: orbit82140 var(--uib-speed) linear calc(var(--uib-speed) / -2)
    infinite;
}

@keyframes orbit82140 {
  0% {
    transform: translate(calc(var(--uib-size) * 0.5)) scale(0.73684);
    opacity: 0.65;
  }

  5% {
    transform: translate(calc(var(--uib-size) * 0.4)) scale(0.684208);
    opacity: 0.58;
  }

  10% {
    transform: translate(calc(var(--uib-size) * 0.3)) scale(0.631576);
    opacity: 0.51;
  }

  15% {
    transform: translate(calc(var(--uib-size) * 0.2)) scale(0.578944);
    opacity: 0.44;
  }

  20% {
    transform: translate(calc(var(--uib-size) * 0.1)) scale(0.526312);
    opacity: 0.37;
  }

  25% {
    transform: translate(0%) scale(0.47368);
    opacity: 0.3;
  }

  30% {
    transform: translate(calc(var(--uib-size) * -0.1)) scale(0.526312);
    opacity: 0.37;
  }

  35% {
    transform: translate(calc(var(--uib-size) * -0.2)) scale(0.578944);
    opacity: 0.44;
  }

  40% {
    transform: translate(calc(var(--uib-size) * -0.3)) scale(0.631576);
    opacity: 0.51;
  }

  45% {
    transform: translate(calc(var(--uib-size) * -0.4)) scale(0.684208);
    opacity: 0.58;
  }

  50% {
    transform: translate(calc(var(--uib-size) * -0.5)) scale(0.73684);
    opacity: 0.65;
  }

  55% {
    transform: translate(calc(var(--uib-size) * -0.4)) scale(0.789472);
    opacity: 0.72;
  }

  60% {
    transform: translate(calc(var(--uib-size) * -0.3)) scale(0.842104);
    opacity: 0.79;
  }

  65% {
    transform: translate(calc(var(--uib-size) * -0.2)) scale(0.894736);
    opacity: 0.86;
  }

  70% {
    transform: translate(calc(var(--uib-size) * -0.1)) scale(0.947368);
    opacity: 0.93;
  }

  75% {
    transform: translate(0%) scale(1);
    opacity: 1;
  }

  80% {
    transform: translate(calc(var(--uib-size) * 0.1)) scale(0.947368);
    opacity: 0.93;
  }

  85% {
    transform: translate(calc(var(--uib-size) * 0.2)) scale(0.894736);
    opacity: 0.86;
  }

  90% {
    transform: translate(calc(var(--uib-size) * 0.3)) scale(0.842104);
    opacity: 0.79;
  }

  95% {
    transform: translate(calc(var(--uib-size) * 0.4)) scale(0.789472);
    opacity: 0.72;
  }

  100% {
    transform: translate(calc(var(--uib-size) * 0.5)) scale(0.73684);
    opacity: 0.65;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.chat-card {
  width: 600px;
  margin: 5px 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.bottom-blank {
  height: 100px;
  transform: translateY(100%);
  animation: bottom-in 0.5s ease-in-out forwards;
}
.bottom-fixed {
  position: fixed;
  bottom: 0;
  width: 100%;
  height: 100px;
  background-image: linear-gradient(
    180deg,
    hsla(0, 0%, 100%, 0) 13.94%,
    #fff 54.73%
  );
  transform: translateY(100%);
  animation: bottom-in 0.5s ease-in-out forwards;
}
.chat-card-0 {
  align-items: flex-end;
}
.chat-card-1 {
  align-items: flex-start;
}
.card-0 {
  background-color: red;
  animation: right-in 0.5s ease-in-out forwards;
  transform: translateX(100%);
  border-radius: 12px;
  background-color: #5d5cde;
  color: #fff;
  padding: 10px;
  max-width: 480px;
}
.card-1 {
  background-color: red;
  animation: left-in 0.5s ease-in-out forwards;
  transform: translateX(-100%);
  border-radius: 12px;
  background-color: #f7f7f7;
  color: #000;
  padding: 10px;
  max-width: 480px;
}
.card-role {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
  transform: translateX(-100%);
  animation: left-in 0.5s ease-in-out forwards;
}
.role-avatar {
  width: 20px;
  height: 20px;
  border-radius: 3px;
  margin-right: 5px;
}
.role-name {
  font-size: 15px;
  margin: 0;
}
.chat-card p {
  margin: 0;
}
.content {
  word-wrap: break-word;
}
.card-btns {
  display: flex;
  align-items: center;
}
@keyframes right-in {
  0% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(0);
  }
}
@keyframes left-in {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(0);
  }
}
@keyframes top-in {
  0% {
    transform: translateY(-100%);
  }
  100% {
    transform: translateX(0);
  }
}
@keyframes bottom-in {
  0% {
    transform: translateY(100%);
  }
  100% {
    transform: translateX(0);
  }
}
</style>