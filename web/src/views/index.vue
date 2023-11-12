<template>
  <div class="index">
    <div class="swiper mySwiper">
      <div class="swiper-wrapper" ref="swiperContainer"></div>
    </div>
    <div :class="'hello hello-1' + (init ? ' init-1' : '')">
      <img src="../assets/icon.png" />
    </div>
    <div :class="'hello hello-2' + (init ? ' init-2' : '')">
      <img src="../assets/icon.png" />
    </div>
    <div :class="'hello hello-3' + (init ? ' init-3' : '')">
      <img src="../assets/icon.png" />
    </div>
    <div :class="'hello hello-4' + (init ? ' init-4' : '')">
      <img src="../assets/icon.png" />
    </div>
    <div class="exit" @click="logout">退出登录</div>
  </div>
</template>

<script>
import { getBots } from "@/api/index";
import { removeToken } from "@/utils/auth";
import "@/utils/swiper.css";
import Swiper from "@/utils/swiper.js";
import config from "@/utils/config";
export default {
  data() {
    return {
      init: false,
      bots: [],
      swiper: null,
    };
  },
  methods: {
    logout() {
      removeToken();
      this.$router.push("/login");
    },
  },
  mounted() {
    this.swiper = new Swiper(".mySwiper", {
      effect: "cards",
      grabCursor: true,
    });
    getBots()
      .then((res) => {
        if (res.code === 0) {
          this.bots = res.bots;
          setTimeout(() => {
            this.init = true;
            let index = 0;
            const intervalId = setInterval(() => {
              if (index >= this.bots.length) {
                clearInterval(intervalId);
                this.$nextTick(() => {
                  // 获取新添加的 slide
                  const slide =
                    this.$refs.swiperContainer.querySelectorAll(
                      ".swiper-slide"
                    );
                  slide.forEach((item, index) => {
                    item.addEventListener("click", () => {
                      this.$router.push({
                        path: "/" + this.bots[index],
                      });
                    });
                  });
                });
                return;
              }
              let bot = this.bots[index];
              let info = config.preset[bot] || {
                desc: "待补充描述。",
                avatar: "ChatGPT.png",
              };
              this.swiper.appendSlide(
                `<div class="swiper-slide card" data-content="${info.desc}">
                <div class="info"><img src="${require("../assets/" +
                  info.avatar)}" class="avatar"/>
                  <p class="name">${bot}</p>
                  </div>
                </div>`
              );
              index++;
            }, 100);
          }, 50);
        } else if (res.code === 403) {
          removeToken();
          this.$router.push("/login");
        }
      })
      .catch(() => {
        removeToken();
        this.$router.push("/login");
      });
  },
  created() {},
};
</script>

<style scoped>
.index {
  width: 100vw;
  height: 100vh;
  background-color: #f7f7f7;
  overflow: hidden;
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.hello {
  position: absolute;
  width: 50%;
  height: 50%;
  overflow: hidden;
  transition: all 1.2s cubic-bezier(0.59, 0.48, 0, 0.99) 0.5s;
  background-color: #f7f7f7;
  z-index: 999;
}
.hello img {
  position: absolute;
  width: 250px;
  height: 250px;
}
.hello-1 {
  left: 0;
  top: 0;
}
.hello-1 img {
  right: -125px;
  bottom: -125px;
}
.init-1 {
  left: -50%;
  top: -50%;
  opacity: 0;
}
.hello-2 {
  right: 0;
  top: 0;
}
.hello-2 img {
  left: -125px;
  bottom: -125px;
}
.init-2 {
  right: -50%;
  top: -50%;
  opacity: 0;
}
.hello-3 {
  left: 0;
  bottom: 0;
}
.hello-3 img {
  top: -125px;
  right: -125px;
}
.init-3 {
  left: -50%;
  bottom: -50%;
  opacity: 0;
}
.hello-4 {
  right: 0;
  bottom: 0;
}
.hello-4 img {
  top: -125px;
  left: -125px;
}
.init-4 {
  right: -50%;
  bottom: -50%;
  opacity: 0;
}
.exit {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 15px;
  color: #3b3abe;
  cursor: pointer;
}
</style>
<style>
.swiper {
  width: 240px;
  height: 320px;
}
.swiper-slide {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  font-size: 22px;
  font-weight: bold;
  color: #fff;
  animation: slide-in 0.5s ease-out;
  position: relative;
  overflow: visible !important;
}
.card {
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.212);
  background: #fff;
  display: flex;
  border-radius: 20px;
  justify-content: center;
  position: relative;
  transition: all 0.4s;
}
.swiper-slide-shadow {
  border-radius: 20px;
  margin-top: 0;
  transition: all 0.4s !important;
}
.card::before {
  content: attr(data-content);
  position: absolute;
  bottom: 8px;
  left: 0px;
  width: 100%;
  padding: 18px 10px;
  color: #212121;
  font-size: 15px;
  font-weight: 700;
  height: 120px;
  box-sizing: border-box;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden !important;
  -webkit-line-clamp: 5;
}

.info {
  width: 100%;
  height: 100%;
  border-radius: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.212);
  cursor: pointer;
  z-index: 10;
  transition: all 0.4s;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar {
  width: 100px;
  height: 100px;
  margin-top: 60px;
  border-radius: 50%;
}
.name {
  margin-top: 30px;
  font-size: 17px;
  font-weight: 700;
  color: #212121;
}
.card:hover .info {
  transform: translateY(-120px);
}
.card:hover .swiper-slide-shadow {
  margin-top: -120px;
  height: calc(100% + 120px);
}
@keyframes slide-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>