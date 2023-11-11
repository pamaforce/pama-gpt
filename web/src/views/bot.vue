<template>
  <div class="chat">
    <div class="top-card">
      <img :src="require('../assets/' + info.avatar)" class="card-avatar" />
      <div class="card-text">
        <div class="card-title">
          <p class="card-title-p">{{ info.name }}</p>
          <div class="back" @click="$router.push('/')">
            <img src="../assets/back.svg" />
            <p>返回主页</p>
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
        :class="'card-' + item.role"
        :style="
          'animation-delay:' +
          (item.delay === undefined ? i * 100 + 500 : 0) +
          'ms'
        "
      >
        <p>{{ item.content }}</p>
      </div>
    </div>
    <div class="bottom-blank"></div>
    <div class="bottom-fixed"></div>
    <div class="user-input">
      <textarea class="textarea" v-model="question" :rows="1" ref="input" />
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
import config from "@/utils/config";
export default {
  data() {
    return {
      info: {},
      question: "",
      loading: false,
      chatList: [],
    };
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
      setTimeout(() => {
        this.loading = false;
        this.chatList.push({
          role: 1,
          content: "这是对" + ques + "的回复",
          delay: 0,
        });
        this.scrollBottom();
      }, 2000);
    },
    scrollBottom() {
      this.$nextTick(() => {
        window.scrollTo({
          top: document.body.scrollHeight,
          behavior: "smooth",
        });
      });
    },
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
  justify-content: flex-end;
}
.chat-card-1 {
  justify-content: flex-start;
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
.chat-card p {
  margin: 0;
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