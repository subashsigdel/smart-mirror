Module.register("youtube_slideshow", {
  defaults: {
    videoIDs: ["MQ_p1qmrxPI", "_OjRClPzU6Y", "CE56q1EpArQ", "b2l5uNkIKRM"],
    autoplay: true,
    mute: false,
  },

  start: function () {
    this.currentVideoIndex = 0;
    this.isShowingVideo = false;

    this.registerKeyEvents();
  },

  registerKeyEvents: function () {
    document.addEventListener("keydown", (event) => {
      if (event.key === "p") {
        this.startVideoPlayback();
      } else if (event.key === "q") {
        this.stopVideoPlayback();
      } else if (event.key === "n") {
        this.nextVideo();
      }
    });
  },

  startVideoPlayback: function () {
    if (!this.isShowingVideo) {
      this.isShowingVideo = true;
      this.updateDom(); // Render the iframe
    }
  },

  stopVideoPlayback: function () {
    if (this.isShowingVideo) {
      this.isShowingVideo = false;
      this.updateDom(); // Remove iframe
    }
  },

  nextVideo: function () {
    this.currentVideoIndex = (this.currentVideoIndex + 1) % this.config.videoIDs.length;
    this.updateDom(); // Load the next video
  },

  getDom: function () {
    const wrapper = document.createElement("div");
    wrapper.style.position = "absolute";
    wrapper.style.top = "0";
    wrapper.style.left = "0";
    wrapper.style.width = "100vw";
    wrapper.style.height = "100vh";

    if (this.isShowingVideo) {
      const videoID = this.config.videoIDs[this.currentVideoIndex];
      const iframe = document.createElement("iframe");

      iframe.style.width = "100%";
      iframe.style.height = "100%";
      iframe.src = `https://www.youtube.com/embed/${videoID}?autoplay=1&mute=${this.config.mute ? 1 : 0}&controls=0&rel=0`;
      iframe.frameBorder = "0";
      iframe.allow = "autoplay; encrypted-media";
      iframe.allowFullscreen = true;

      wrapper.appendChild(iframe);
    }

    return wrapper;
  },
});
